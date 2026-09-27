import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:steam_atlas/core/map_geometry.dart';

void main() {
  test('최소 줌에서 세계의 세로가 화면 높이에 꼭 맞는다 (조금 더 크되 0.1% 이내)', () {
    for (final h in [400.0, 512.0, 640.0, 731.5, 1024.0, 2200.0]) {
      final z = MapGeometry.worldFitZoom(h);
      final world = MapGeometry.worldSizePx(z);
      // 세계가 화면보다 작으면 containLatitude 가 이동을 거부해 지도가 굳는다
      expect(world, greaterThanOrEqualTo(h), reason: 'height $h');
      expect(world, lessThan(h * 1.001), reason: 'height $h');
    }
    // 256px 화면 = 줌 0 (+여유)
    expect(MapGeometry.worldFitZoom(256), closeTo(0.001, 1e-9));
  });

  test('높이가 0·무한·NaN 이면 안전한 기본값 1', () {
    expect(MapGeometry.worldFitZoom(0), 1);
    expect(MapGeometry.worldFitZoom(-10), 1);
    expect(MapGeometry.worldFitZoom(double.infinity), 1);
    expect(MapGeometry.worldFitZoom(double.nan), 1);
  });

  test('순환 주기 = 세계 한 변 = 256·2^z', () {
    expect(MapGeometry.worldSizePx(0), 256);
    expect(MapGeometry.worldSizePx(1), 512);
    expect(MapGeometry.worldSizePx(3), 2048);
  });

  test('프리뷰 HTML 과 첫 화면 중심 경도·위도 한계가 같다', () {
    final tpl = File('tools/preview_template.html').readAsStringSync();
    expect(tpl, contains('const MAP_HOME_LON=${MapGeometry.homeLongitude}'));
    expect(tpl, contains('const MERC_MAX_LAT=${MapGeometry.maxLatitude}'));
    expect(MapGeometry.homeLongitude, inInclusiveRange(-180, 180));
  });
}
