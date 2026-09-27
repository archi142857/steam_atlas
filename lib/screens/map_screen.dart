import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:provider/provider.dart';

import '../core/map_geometry.dart';
import '../core/marker_cluster.dart';
import '../core/theme.dart';
import '../data/world_map.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import '../widgets/filter_sheet.dart';
import '../widgets/loco_card.dart';
import 'detail_screen.dart';

/// 세계 지도 — 현존 개체가 있는 곳을 찍는다.
///
/// 레이어 순서: 바다색 배경 → 오프라인 육지 폴리곤 → (선택) 타일 → 마커.
///
/// **기본은 오프라인 폴리곤만 쓴다.** 네트워크·비용·타일 정책에서 자유롭고,
/// 이 앱의 목적(어느 나라 어느 도시에 있는가)에는 그걸로 충분하다.
/// 설정에서 '온라인 상세 지도'를 켜면 타일이 위에 올라간다.
///
/// **상하는 막히고 좌우는 끝없이 돈다.**
/// - 상하: `CameraConstraint.containLatitude()` — 세계(±85.05°)의 위아래 끝이 화면 안으로
///   들어오지 못한다. 최소 줌은 세계의 세로가 화면 높이에 꼭 맞는 값(`MapGeometry.worldFitZoom`)
///   이라, 가장 멀리 축소하면 상하로는 전혀 움직이지 않고 좌우로만 돈다.
/// - 좌우: flutter_map 8 의 멀티 월드 — 경도 180° 를 넘으면 반대편으로 이어지고,
///   타일·육지 폴리곤·마커가 옆 세계에도 그려진다(따로 복제하지 않는다).
/// - 회전은 끈다. 기울어진 화면에서는 위도 제한이 귀퉁이를 못 막고, 이 앱에 회전은 필요 없다.
class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final _map = MapController();
  Locomotive? _selected;
  WorldMap? _world;

  /// 이 화면 거리(px) 안의 마커끼리 묶는다. 핀이 34px 이니 겹치기 직전에 묶이는 값.
  static const double _clusterRadiusPx = 28;
  static const double _maxZoom = 12;

  @override
  void initState() {
    super.initState();
    WorldMap.load().then((w) {
      if (mounted) setState(() => _world = w);
    });
  }

  Marker _pinMarker(Locomotive l) => Marker(
        point: LatLng(l.location!.lat, l.location!.lon),
        width: 34,
        height: 34,
        child: _Pin(
          loco: l,
          selected: _selected?.id == l.id,
          onTap: () => setState(() => _selected = l),
        ),
      );

  static LatLng _latLngOf(double x, double y, double zoom) {
    final ll = MapProjection.unproject(x, y, zoom);
    return LatLng(ll.lat, ll.lon);
  }

  /// 구성원이 전부 같은 상태면 그 상태색, 섞여 있으면 중립색(테마의 전경색).
  static Color _clusterColor(List<Locomotive> members, ColorScheme scheme) {
    final st = members.first.status;
    return members.every((l) => l.status == st)
        ? AppTheme.statusColor(st, scheme)
        : scheme.onSurface;
  }

  /// 묶음을 누르면 그 자리로 확대한다 — 구성원이 화면의 60% 안에 들어오는 줌, 최소 +1, 최대 [_maxZoom].
  /// 화면에서 4px 도 안 벌어지는 묶음은 같은 시설(같은 좌표)이다 — 아무리 확대해도 안 풀리니 목록에서 고른다.
  void _zoomIntoCluster(MarkerCluster<Locomotive> c, double zoom, BoxConstraints box) {
    var minX = double.infinity, maxX = -double.infinity;
    var minY = double.infinity, maxY = -double.infinity;
    final w = MapGeometry.worldSizePx(zoom);
    for (final l in c.members) {
      final p = MapProjection.project(l.location!.lat, l.location!.lon, zoom);
      // 순환 경계를 넘는 묶음: 중심 기준으로 가까운 쪽에 놓고 잰다
      var dx = p.x - c.x;
      dx = ((dx + w / 2) % w + w) % w - w / 2;
      minX = math.min(minX, dx);
      maxX = math.max(maxX, dx);
      minY = math.min(minY, p.y);
      maxY = math.max(maxY, p.y);
    }
    final spread = math.max(maxX - minX, maxY - minY);
    // 이미 최대 줌이면 더 확대할 수 없으니 역시 목록으로.
    if (spread <= 4 || zoom >= _maxZoom - 0.01) {
      _pickFromCluster(c.members);
      return;
    }
    final room = 0.6 * math.min(box.maxWidth, box.maxHeight);
    final wanted = zoom + math.log(room / spread) / math.ln2;
    final target = math.min(_maxZoom, math.max(zoom + 1, wanted));
    _map.move(_latLngOf(c.x, c.y, zoom), target);
  }

  /// 같은 자리에 겹친 량들 — 아래 시트에서 하나를 고르면 그 마커가 선택된다.
  Future<void> _pickFromCluster(List<Locomotive> members) async {
    final scheme = Theme.of(context).colorScheme;
    final picked = await showModalBottomSheet<Locomotive>(
      context: context,
      showDragHandle: true,
      builder: (ctx) => SafeArea(
        child: ListView(
          shrinkWrap: true,
          padding: const EdgeInsets.fromLTRB(8, 0, 8, 12),
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
              child: Text.rich(
                TextSpan(
                  text: '같은 자리에 ${members.length}량  ',
                  style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800),
                  children: [
                    TextSpan(
                      text: members.first.location!.name,
                      style: TextStyle(
                          fontSize: 12, fontWeight: FontWeight.w500, color: scheme.onSurfaceVariant),
                    ),
                  ],
                ),
              ),
            ),
            for (final l in members)
              ListTile(
                leading: Container(
                  width: 10,
                  height: 10,
                  decoration: BoxDecoration(
                    color: AppTheme.statusColor(l.status, scheme),
                    shape: BoxShape.circle,
                  ),
                ),
                minLeadingWidth: 10,
                title: Text(l.nameKo, style: const TextStyle(fontWeight: FontWeight.w700)),
                subtitle: Text('${l.classDesignation} · ${l.status.labelKo}',
                    style: const TextStyle(fontSize: 12)),
                trailing: const Icon(Icons.chevron_right_rounded),
                onTap: () => Navigator.of(ctx).pop(l),
              ),
          ],
        ),
      ),
    );
    if (picked != null && mounted) setState(() => _selected = picked);
  }

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final repo = app.repo!;
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final items = repo.withLocation(app.query);

    final sea = isDark ? const Color(0xFF101A24) : const Color(0xFFD6E3EC);
    final land = isDark ? const Color(0xFF262D37) : const Color(0xFFF8F5EF);
    final coast = isDark ? const Color(0xFF414A57) : const Color(0xFFBDB5A7);

    return LayoutBuilder(builder: (context, constraints) {
      // 세계의 세로가 이 칸의 높이에 꼭 맞는 줌 = 최소 줌. 첫 화면도 그 줌에서 시작한다
      // (세계 전체가 세로로 보이고, 좌우로 돌려 보는 화면).
      final fitZoom = MapGeometry.worldFitZoom(constraints.maxHeight);

      return Stack(
        children: [
          FlutterMap(
            mapController: _map,
            options: MapOptions(
              // 최소 줌에서는 세로 위치가 하나뿐(위도 0 중심)이라 처음부터 거기서 시작한다.
              initialCenter: const LatLng(0, MapGeometry.homeLongitude),
              initialZoom: fitZoom,
              minZoom: fitZoom,
              maxZoom: _maxZoom,
              backgroundColor: sea,
              // 상하 제한 — 세계 위아래 끝 밖의 빈 공간이 화면에 들어오지 못한다. 좌우는 제한 없음.
              cameraConstraint: const CameraConstraint.containLatitude(),
              interactionOptions: const InteractionOptions(
                flags: InteractiveFlag.all & ~InteractiveFlag.rotate,
              ),
              onTap: (_, __) => setState(() => _selected = null),
            ),
            children: [
              if (_world != null)
                PolygonLayer(
                  polygons: [
                    for (final ring in _world!.rings)
                      Polygon(
                        points: ring,
                        color: land,
                        borderColor: coast,
                        borderStrokeWidth: 0.5,
                      ),
                  ],
                ),
              // 온라인 타일은 설정에서 켰을 때만 올린다 (기본 꺼짐).
              //
              // 여기 박힌 공개 OSM 타일 URL 은 개발 확인용이다.
              // OSM Foundation 의 타일 사용 정책상 앱 프로덕션 트래픽에는 쓸 수 없고,
              // 예고 없이 차단될 수 있다. 출시 전 자체/상용 타일 URL 로 교체할 것.
              //
              // 타일 레이어는 배경을 칠하지 않으므로(배경은 MapOptions.backgroundColor 하나),
              // 아직 안 온 타일 자리에는 폴리곤 밑그림이 그대로 비쳐 보인다.
              if (app.onlineTiles)
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'com.example.steam_atlas',
                ),
              // 마커 — 카메라가 움직일 때마다 현재 줌의 픽셀 거리로 다시 묶는다 (클러스터링).
              // MapCamera.of 는 카메라 변화에 이 Builder 만 다시 그리게 한다. 선택된 량은 묶지 않고
              // 항상 낱개로 위에 그린다 — 아래 카드가 가리키는 마커가 숫자 속으로 사라지면 안 되니까.
              Builder(builder: (context) {
                final camera = MapCamera.of(context);
                final zoom = camera.zoom;
                final selectedId = _selected?.id;
                final clusters = clusterMarkers<Locomotive>(
                  items.where((l) => l.id != selectedId),
                  (l) => MapProjection.project(l.location!.lat, l.location!.lon, zoom),
                  radiusPx: _clusterRadiusPx,
                  worldWidthPx: MapGeometry.worldSizePx(zoom),
                );
                return MarkerLayer(
                  markers: [
                    for (final c in clusters)
                      if (c.isSingle)
                        _pinMarker(c.members.single)
                      else
                        Marker(
                          point: _latLngOf(c.x, c.y, zoom),
                          width: 40,
                          height: 40,
                          child: _ClusterPin(
                            count: c.count,
                            color: _clusterColor(c.members, scheme),
                            onTap: () => _zoomIntoCluster(c, zoom, constraints),
                          ),
                        ),
                    if (_selected != null && items.any((l) => l.id == selectedId))
                      _pinMarker(_selected!),
                  ],
                );
              }),
            ],
          ),
          // 상단 컨트롤
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
              child: Row(
                children: [
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
                    decoration: BoxDecoration(
                      color: scheme.surfaceContainer.withValues(alpha: 0.94),
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      '보존 위치 ${items.length}곳',
                      style: const TextStyle(
                          fontSize: 12.5, fontWeight: FontWeight.w700),
                    ),
                  ),
                  const Spacer(),
                  Badge(
                    isLabelVisible: app.query.activeCount > 0,
                    label: Text('${app.query.activeCount}'),
                    child: FloatingActionButton.small(
                      heroTag: 'map-filter',
                      onPressed: () => FilterSheet.show(context),
                      child: const Icon(Icons.tune_rounded),
                    ),
                  ),
                ],
              ),
            ),
          ),
          // 하단 선택 카드
          if (_selected != null)
            Positioned(
              left: 12,
              right: 12,
              bottom: 16,
              child: LocoCard(
                loco: _selected!,
                livery: app.liveryOf(_selected!),
                shape: app.shapeOf(_selected!),
                dense: true,
                isFavorite: app.isFavorite(_selected!.id),
                onFavorite: () => app.toggleFavorite(_selected!.id),
                onTap: () => DetailScreen.push(context, _selected!.id),
              ),
            ),
          // 범례
          Positioned(
            left: 12,
            bottom: _selected != null ? 210 : 16,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(
                color: scheme.surfaceContainer.withValues(alpha: 0.94),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  for (final s in [
                    LocoStatus.operational,
                    LocoStatus.operable,
                    LocoStatus.static_,
                    LocoStatus.restoration,
                    LocoStatus.replica,
                  ])
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 2),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 8,
                            height: 8,
                            decoration: BoxDecoration(
                              color: AppTheme.statusColor(s, scheme),
                              shape: BoxShape.circle,
                            ),
                          ),
                          const SizedBox(width: 6),
                          Text(s.labelKo, style: const TextStyle(fontSize: 10.5)),
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ),
        ],
      );
    });
  }
}

/// 묶음 마커 — 숫자 하나. 누르면 그 자리로 확대된다.
class _ClusterPin extends StatelessWidget {
  const _ClusterPin({required this.count, required this.color, required this.onTap});
  final int count;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    // 상태색은 어두운 편이라 흰 글자, 중립색(onSurface)은 테마에 따라 밝기가 바뀌므로 surface 글자.
    final fg = color == scheme.onSurface ? scheme.surface : Colors.white;
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.all(4),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: color,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white.withValues(alpha: 0.75), width: 2),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.35),
              blurRadius: 5,
              offset: const Offset(0, 1),
            ),
          ],
        ),
        child: Text(
          '$count',
          style: TextStyle(
            color: fg,
            fontSize: count >= 100 ? 10 : 12,
            fontWeight: FontWeight.w800,
            height: 1,
          ),
        ),
      ),
    );
  }
}

class _Pin extends StatelessWidget {
  const _Pin({required this.loco, required this.selected, required this.onTap});
  final Locomotive loco;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final c = AppTheme.statusColor(loco.status, scheme);
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        margin: EdgeInsets.all(selected ? 2 : 8),
        decoration: BoxDecoration(
          color: c,
          shape: BoxShape.circle,
          border: Border.all(
            color: Colors.white.withValues(alpha: selected ? 0.95 : 0.6),
            width: selected ? 2.5 : 1.5,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.35),
              blurRadius: 4,
              offset: const Offset(0, 1),
            ),
          ],
        ),
        child: selected
            ? const Icon(Icons.train_rounded, size: 16, color: Colors.white)
            : null,
      ),
    );
  }
}
