import 'package:flutter_test/flutter_test.dart';
import 'package:steam_atlas/core/map_geometry.dart';
import 'package:steam_atlas/core/marker_cluster.dart';

void main() {
  group('MapProjection', () {
    test('줌 0 에서 세계가 256px, (0,0)° 은 한가운데', () {
      final p = MapProjection.project(0, 0, 0);
      expect(p.x, closeTo(128, 1e-9));
      expect(p.y, closeTo(128, 1e-9));
      expect(MapProjection.project(MapGeometry.maxLatitude, -180, 0).y, closeTo(0, 1e-6));
      expect(MapProjection.project(-MapGeometry.maxLatitude, 180, 0).y, closeTo(256, 1e-6));
      expect(MapProjection.project(-MapGeometry.maxLatitude, 180, 0).x, closeTo(256, 1e-9));
    });

    test('project ∘ unproject 는 항등 (경도는 -180..180 으로 접음)', () {
      for (final (lat, lon) in [(37.5, 127.0), (-33.9, 151.2), (51.5, -0.1), (64.0, -179.5), (0.0, 179.9)]) {
        final p = MapProjection.project(lat, lon, 5);
        final back = MapProjection.unproject(p.x, p.y, 5);
        expect(back.lat, closeTo(lat, 1e-6), reason: '$lat,$lon');
        expect(back.lon, closeTo(lon, 1e-6), reason: '$lat,$lon');
      }
    });
  });

  group('clusterMarkers', () {
    ({double x, double y}) id(({double x, double y}) p) => p;

    test('반지름 안이면 묶이고 밖이면 따로', () {
      final pts = [(x: 10.0, y: 10.0), (x: 20.0, y: 10.0), (x: 100.0, y: 10.0), (x: 10.0, y: 25.0)];
      final c = clusterMarkers(pts, id, radiusPx: 20);
      expect(c.length, 2);
      expect(c[0].count, 3); // (10,10) 씨앗 + (20,10) + (10,25)
      expect(c[1].count, 1);
      expect(c[0].x, closeTo((10 + 20 + 10) / 3, 1e-9));
      expect(c[0].y, closeTo((10 + 10 + 25) / 3, 1e-9));
    });

    test('반지름 0 이면 전부 낱개, 순서는 y→x', () {
      final pts = [(x: 5.0, y: 9.0), (x: 1.0, y: 9.0), (x: 0.0, y: 1.0)];
      final c = clusterMarkers(pts, id, radiusPx: 0);
      expect(c.every((k) => k.isSingle), isTrue);
      expect(c.map((k) => k.members.single), [(x: 0.0, y: 1.0), (x: 1.0, y: 9.0), (x: 5.0, y: 9.0)]);
    });

    test('좌우 순환: 세계 양끝의 마커는 이웃이라 묶인다', () {
      const w = 256.0;
      final pts = [(x: 2.0, y: 50.0), (x: 254.0, y: 50.0)];
      final c = clusterMarkers(pts, id, radiusPx: 10, worldWidthPx: w);
      expect(c.length, 1);
      // 중심은 씨앗 기준으로 평균한다: 씨앗 2, 상대 x -4 → 평균 상대 -2 → 절대 0 (=경계 위)
      expect(c.single.x, closeTo(0, 1e-9));
      // 순환을 안 주면 252px 떨어진 것으로 보고 따로 둔다
      expect(clusterMarkers(pts, id, radiusPx: 10).length, 2);
    });

    test('확대하면 같은 두 점이 풀린다 (픽셀 거리가 2배씩 커진다)', () {
      // 서울역 근처 두 지점 — 실제 데이터처럼 위경도로
      final a = (lat: 37.5547, lon: 126.9707), b = (lat: 37.5665, lon: 126.9780);
      int clustersAt(double z) => clusterMarkers(
            [a, b],
            (p) => MapProjection.project(p.lat, p.lon, z),
            radiusPx: 28,
            worldWidthPx: MapGeometry.worldSizePx(z),
          ).length;
      expect(clustersAt(3), 1);
      expect(clustersAt(12), 2);
      // 줌을 올리면 묶음 수는 줄지 않는다
      var prev = 0;
      for (var z = 1.0; z <= 12; z += 0.5) {
        final n = clustersAt(z);
        expect(n, greaterThanOrEqualTo(prev), reason: 'zoom $z');
        prev = n;
      }
    });
  });
}
