import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;
import 'package:latlong2/latlong.dart';

/// 오프라인 세계지도(육지 폴리곤).
///
/// `assets/map/world_110m.json` — Natural Earth 110m(퍼블릭 도메인)을
/// `tools/build_worldmap.py` 로 변환한 것. 약 10,500점 / 115KB.
///
/// 용도: 지도 화면에서 OSM 타일 **아래에 깔리는 밑그림**.
/// 타일이 뜨면 가려지고, 오프라인이거나 타일이 차단된 환경에서는 이 레이어가
/// 그대로 보여서 지도가 빈 화면이 되지 않는다. 프리뷰 HTML도 같은 데이터를 쓴다.
class WorldMap {
  const WorldMap({required this.rings, required this.source});

  /// 국가 경계 링. 각 링은 닫힌 폴리곤 하나.
  final List<List<LatLng>> rings;
  final String source;

  static Future<WorldMap>? _cached;

  /// 앱 수명 동안 한 번만 파싱한다.
  static Future<WorldMap> load() => _cached ??= _parse();

  static Future<WorldMap> _parse() async {
    final raw = await rootBundle.loadString('assets/map/world_110m.json');
    final json = jsonDecode(raw) as Map<String, dynamic>;

    final rings = <List<LatLng>>[];
    for (final country in (json['countries'] as List)) {
      final ringList = (country as Map<String, dynamic>)['rings'] as List;
      for (final ring in ringList) {
        // [lon, lat, lon, lat, ...] 평면 배열
        final flat = (ring as List).cast<num>();
        final points = <LatLng>[];
        for (var i = 0; i + 1 < flat.length; i += 2) {
          points.add(LatLng(flat[i + 1].toDouble(), flat[i].toDouble()));
        }
        if (points.length >= 3) rings.add(points);
      }
    }

    return WorldMap(
      rings: rings,
      source: json['source'] as String? ?? 'Natural Earth',
    );
  }
}
