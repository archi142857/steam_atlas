import 'package:flutter_test/flutter_test.dart';
import 'package:steam_atlas/core/place_maps.dart';
import 'package:steam_atlas/models/locomotive.dart';

void main() {
  const withQ = LocoLocation(
      name: '국립철도박물관, 요크 (NRM York)',
      lat: 53.9603,
      lon: -1.0951,
      query: 'National Railway Museum York');
  const noQ = LocoLocation(name: '러시아 각지 보존', lat: 55.794, lon: 37.639);

  test('안드로이드 geo: 주소 — 검색어가 있으면 이름 검색, 없으면 라벨 붙은 좌표 핀', () {
    expect(PlaceMaps.androidUri(withQ).toString(),
        'geo:53.9603,-1.0951?q=National%20Railway%20Museum%20York');
    final a = PlaceMaps.androidUri(noQ).toString();
    expect(a, startsWith('geo:0,0?q=55.794,37.639('));
    expect(Uri.decodeComponent(a), 'geo:0,0?q=55.794,37.639(러시아 각지 보존)');
  });

  test('라벨에는 쉼표·괄호가 없다 (라벨을 통째로 버리는 파서 방지)', () {
    expect(PlaceMaps.markerTitle('국립철도박물관, 요크 (NRM York)'), '국립철도박물관 요크 NRM York');
    expect(PlaceMaps.markerTitle('  Locomotion, 실던 '), 'Locomotion 실던');
  });

  test('Apple 지도는 ll + q(라벨), 웹은 검색어 우선', () {
    final apple = PlaceMaps.appleUri(withQ);
    expect(apple.scheme, 'maps');
    expect(apple.queryParameters['ll'], '53.9603,-1.0951');
    expect(apple.queryParameters['q'], '국립철도박물관, 요크 (NRM York)');
    expect(PlaceMaps.webUri(withQ).queryParameters['query'], 'National Railway Museum York');
    expect(PlaceMaps.webUri(noQ).queryParameters['query'], '55.794,37.639');
  });
}
