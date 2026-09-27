import 'dart:math' as math;

import 'map_geometry.dart';

/// 마커 클러스터링 — 순수 Dart, 위젯 없이 테스트한다.
///
/// 유럽·일본처럼 보존 차량이 몰린 곳은 축소하면 마커가 겹쳐 하나처럼 보인다. 그래서
/// **화면 픽셀 거리**가 [clusterMarkers] 의 `radiusPx` 안에 드는 마커끼리 묶어 숫자 하나로 그린다.
/// 확대하면 거리가 벌어져 저절로 풀린다. 규칙은 프리뷰 HTML 의 `clusterMarks()` 와 같다:
/// 탐욕적(greedy)·결정적 — 위에서 아래(y), 왼쪽에서 오른쪽(x) 순으로 씨앗을 잡고, 아직 안 묶인
/// 마커 중 반지름 안의 것을 전부 붙인다. 격자 방식과 달리 격자 경계에서 갈라지지 않는다.
///
/// 좌우 순환 지도라 x 거리는 세계 한 벌 폭을 법(mod)으로 잰다 — 경도 180° 근처의 두 마커는
/// 화면상 이웃이므로 함께 묶인다.
class MapProjection {
  const MapProjection._();

  /// 웹 메르카토르 픽셀 좌표 (flutter_map 의 Epsg3857, 타일 256px 과 같은 식).
  /// 줌 [zoom] 에서 세계 한 변이 `256·2^zoom` px 이고, 좌상단이 (0,0).
  static ({double x, double y}) project(double lat, double lon, double zoom) {
    final size = MapGeometry.worldSizePx(zoom);
    final clampedLat =
        lat.clamp(-MapGeometry.maxLatitude, MapGeometry.maxLatitude).toDouble();
    final latR = clampedLat * math.pi / 180;
    final x = (lon + 180) / 360 * size;
    final y = (1 - math.log(math.tan(latR) + 1 / math.cos(latR)) / math.pi) / 2 * size;
    return (x: x, y: y);
  }

  /// [project] 의 역. x 는 세계 폭 밖이어도 된다(순환).
  static ({double lat, double lon}) unproject(double x, double y, double zoom) {
    final size = MapGeometry.worldSizePx(zoom);
    final lon = x / size * 360 - 180;
    final n = math.pi - 2 * math.pi * y / size;
    final lat = 180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)));
    return (lat: lat, lon: ((lon + 180) % 360) - 180);
  }
}

/// 묶음 하나. [members] 가 하나면 낱개 마커다.
class MarkerCluster<T> {
  MarkerCluster(this.members, this.x, this.y);

  final List<T> members;

  /// 픽셀 중심 (구성원 평균; 순환 경계를 넘는 묶음은 씨앗 기준으로 펼쳐 평균한 뒤 세계 폭으로 접음).
  final double x;
  final double y;

  bool get isSingle => members.length == 1;
  int get count => members.length;
}

/// [items] 를 화면 거리 [radiusPx] 로 묶는다. [at] 은 각 항목의 픽셀 좌표(같은 줌에서 [MapProjection.project]).
/// [worldWidthPx] 를 주면 x 거리를 그 폭을 법으로 잰다(좌우 순환 지도). 결과 순서는 결정적이다.
List<MarkerCluster<T>> clusterMarkers<T>(
  Iterable<T> items,
  ({double x, double y}) Function(T item) at, {
  required double radiusPx,
  double? worldWidthPx,
}) {
  assert(radiusPx >= 0);
  final pts = [for (final it in items) (item: it, p: at(it))]
    ..sort((a, b) {
      final dy = a.p.y.compareTo(b.p.y);
      return dy != 0 ? dy : a.p.x.compareTo(b.p.x);
    });
  final w = worldWidthPx;

  // 씨앗 기준 x 차 — 순환이면 가까운 쪽으로 접는다 (-w/2 .. w/2).
  double dx(double from, double to) {
    var d = to - from;
    if (w != null && w > 0) {
      d = ((d + w / 2) % w + w) % w - w / 2;
    }
    return d;
  }

  final taken = List<bool>.filled(pts.length, false);
  final out = <MarkerCluster<T>>[];
  final r2 = radiusPx * radiusPx;
  for (var i = 0; i < pts.length; i++) {
    if (taken[i]) continue;
    taken[i] = true;
    final seed = pts[i].p;
    final members = <T>[pts[i].item];
    var sx = 0.0, sy = seed.y; // 씨앗 기준 상대 x 합
    for (var j = i + 1; j < pts.length; j++) {
      if (taken[j]) continue;
      final ddx = dx(seed.x, pts[j].p.x), ddy = pts[j].p.y - seed.y;
      if (ddy > radiusPx) break; // y 정렬이라 이 뒤는 전부 멀다
      if (ddx * ddx + ddy * ddy <= r2) {
        taken[j] = true;
        members.add(pts[j].item);
        sx += ddx;
        sy += pts[j].p.y;
      }
    }
    var cx = seed.x + sx / members.length;
    if (w != null && w > 0) cx = (cx % w + w) % w;
    out.add(MarkerCluster<T>(members, cx, sy / members.length));
  }
  return out;
}
