import 'dart:convert';
import 'dart:io';
import 'dart:math' as math;
import 'dart:ui' show Color;

import 'package:flutter_test/flutter_test.dart';
import 'package:steam_atlas/core/hangul.dart';
import 'package:steam_atlas/data/locomotive_repository.dart';
import 'package:steam_atlas/models/filter_query.dart';
import 'package:steam_atlas/models/locomotive.dart';
import 'package:steam_atlas/widgets/whyte_diagram.dart';

/// 번들 JSON을 실제 모델로 파싱해 스키마가 깨지지 않았는지 확인한다.
/// (rootBundle 대신 파일에서 직접 읽어 flutter test 로 바로 돌아가게 함)
LocomotiveDataset _loadFromDisk() {
  final locoJson =
      jsonDecode(File('assets/data/locomotives.json').readAsStringSync())
          as Map<String, dynamic>;
  final countryJson =
      jsonDecode(File('assets/data/countries.json').readAsStringSync())
          as Map<String, dynamic>;
  return LocomotiveDataset(
    locomotives: (locoJson['locomotives'] as List)
        .map((e) => Locomotive.fromJson(e as Map<String, dynamic>))
        .toList(),
    eras: (locoJson['eras'] as List)
        .map((e) => Era.fromJson(e as Map<String, dynamic>))
        .toList(),
    liveries: ((locoJson['liveries'] as List?) ?? const [])
        .map((e) => Livery.fromJson(e as Map<String, dynamic>))
        .toList(),
    shapes: ((locoJson['shapes'] as List?) ?? const [])
        .map((e) => LocoShape.fromJson(e as Map<String, dynamic>))
        .toList(),
    countries: (countryJson['countries'] as List)
        .map((e) => Country.fromJson(e as Map<String, dynamic>))
        .toList(),
  );
}

void main() {
  late LocomotiveRepository repo;

  setUpAll(() => repo = LocomotiveRepository(_loadFromDisk()));

  test('전체 데이터가 파싱된다', () {
    expect(repo.all, isNotEmpty);
    expect(repo.countries, isNotEmpty);
    expect(repo.eras.length, 6);
  });

  test('id는 중복되지 않는다', () {
    final ids = repo.all.map((l) => l.id).toList();
    expect(ids.toSet().length, ids.length);
  });

  test('모든 기관차의 국가·시대 코드가 실제로 존재한다', () {
    for (final l in repo.all) {
      expect(repo.country(l.countryCode), isNotNull,
          reason: '${l.id}: 알 수 없는 국가 ${l.countryCode}');
      expect(repo.era(l.eraId), isNotNull,
          reason: '${l.id}: 알 수 없는 시대 ${l.eraId}');
    }
  });

  test('Whyte 표기에서 동륜 수가 올바르게 계산된다', () {
    expect(const Wheel(whyte: '4-6-2').drivingWheels, 6);
    expect(const Wheel(whyte: '4-8-8-4').drivingWheels, 16);
    expect(const Wheel(whyte: '2-6-4T').isTank, isTrue);
    expect(const Wheel(whyte: '4-8-2+2-8-4').isGarratt, isTrue);
    // 가라트는 유닛별로 세야 한다. 통째로 이어 세면 앞 유닛 종륜과
    // 뒤 유닛 선륜까지 동륜으로 잡혀 20이 나온다.
    expect(const Wheel(whyte: '4-8-2+2-8-4').drivingWheels, 16);
    expect(const Wheel(whyte: '0-4-0').drivingWheels, 4);
  });

  test('검색이 이름·형식·차륜배치 모두에 걸린다', () {
    expect(repo.query(const FilterQuery(text: '맬러드')), isNotEmpty);
    expect(repo.query(const FilterQuery(text: 'mallard')), isNotEmpty);
    expect(repo.query(const FilterQuery(text: '4-8-8-4')), isNotEmpty);
    expect(repo.query(const FilterQuery(text: 'baldwin')), isNotEmpty);
  });

  test('한글 검색: 자모 분리(NFD)·공백·초성 입력도 같은 결과를 낸다', () {
    // '맬러드'를 자모로 분리해 넘긴 경우 (macOS/iOS 키보드가 흔히 이렇게 보낸다)
    const nfd = '\u1106\u1162\u11AF\u1105\u1165\u1103\u1173'; // ㅁ+ㅐ+ㄹ ㄹ+ㅓ ㄷ+ㅡ
    expect(composeHangul(nfd), '맬러드');
    expect(searchKey('미카 3형 129호'), '미카3형129호');
    expect(initials('맬러드 4468'), 'ㅁㄹㄷ4468');
    expect(isChoseongQuery('ㅁㄹㄷ'), isTrue);
    expect(isChoseongQuery('맬'), isFalse);
    expect(isChoseongQuery(''), isFalse);

    final byNfc = repo.query(const FilterQuery(text: '맬러드')).map((l) => l.id);
    final byNfd = repo.query(const FilterQuery(text: nfd)).map((l) => l.id);
    expect(byNfd, orderedEquals(byNfc));
    expect(repo.query(const FilterQuery(text: 'ㅁㄹㄷ')).map((l) => l.id),
        contains('gb-lner-a4-mallard'));
    expect(repo.query(const FilterQuery(text: '미카 3형')), isNotEmpty);
    // 별명으로도 찾아진다 (이름 칸에는 없어도)
    expect(repo.query(const FilterQuery(text: '티거리')).map((l) => l.id),
        contains('ch-e33'));
  });

  test('별명은 이름 칸에 섞여 들어가지 않는다 (공인 형식명 유지)', () {
    for (final l in repo.all) {
      final n = l.nickname;
      if (n == null) continue;
      expect(l.nameKo.contains(n), isFalse, reason: '${l.id}: nameKo 에 별명이 들어감');
      expect(l.nameEn.contains(n), isFalse, reason: '${l.id}: nameEn 에 별명이 들어감');
    }
  });

  test('중량 기준(weightBasis)이 있으면 라벨이 붙고, 값이 없으면 기준도 없다', () {
    for (final l in repo.all) {
      if (l.specs.weightT == null) {
        expect(l.specs.weightBasis, isNull, reason: '${l.id}: 중량이 없는데 기준만 있음');
      }
    }
    expect(WeightBasis.parse('locoAndTender')?.labelKo, '기관차+탄수차');
    expect(WeightBasis.parse('nonsense'), isNull);
  });

  test('참고문헌: 서지 필수 항목이 채워져 있고 모든 나라에 표준 문헌이 있다', () {
    const kinds = {'book', 'article', 'thesis', 'official', 'catalog'};
    void check(Reference r, String where) {
      expect(r.title, isNotEmpty, reason: '$where: 제목 없음');
      expect(r.publisher, isNotEmpty, reason: '$where: 출판사 없음 (${r.title})');
      expect(r.via, isNotEmpty, reason: '$where: 서지 확인 경로 없음 (${r.title})');
      expect(kinds, contains(r.kind), reason: '$where: kind ${r.kind}');
      if (r.year != null) {
        expect(r.year, inInclusiveRange(1800, 2030), reason: '$where: 연도 ${r.year}');
      }
      // 인용문 한 줄이 만들어진다
      expect(r.citation, contains('『'));
    }

    for (final c in repo.countries) {
      expect(c.references, isNotEmpty, reason: '${c.code}: 국가별 표준 문헌이 없음');
      for (final r in c.references) {
        check(r, c.code);
      }
    }
    for (final l in repo.all) {
      for (final r in l.references) {
        check(r, l.id);
      }
    }
    expect(repo.generalReferences, isNotEmpty);
    // 종이 문헌과 웹 출처는 섞이지 않는다 — 문헌 url 은 도서관·출판사·학술DB·공식 페이지만
    for (final r in [...repo.generalReferences, for (final c in repo.countries) ...c.references]) {
      if (r.url != null) {
        expect(r.url, isNot(contains('wikipedia.org')), reason: '${r.title}: 위키 링크는 sources 로');
      }
    }
  });

  test('필터가 누적 적용된다', () {
    final onlyKorea = repo.query(const FilterQuery(countries: {'KR'}));
    expect(onlyKorea, isNotEmpty);
    expect(onlyKorea.every((l) => l.countryCode == 'KR'), isTrue);

    final alive = repo.query(const FilterQuery(aliveOnly: true));
    expect(alive.every((l) => l.status.isAlive), isTrue);

    final none = repo.query(
      const FilterQuery(countries: {'KR'}, statuses: {LocoStatus.scrapped}, aliveOnly: true),
    );
    expect(none, isEmpty);
  });

  test('도색 계열·생김새 필터 (v0.12)', () {
    // 모든 도색에 계열이 있고, 이름과 계열이 어긋나지 않는다 ('블랙'은 검정, '그린'은 녹색).
    for (final lv in repo.liveries) {
      expect(lv.family, isNotNull, reason: lv.id);
      if (lv.nameKo.contains('블랙') || lv.nameKo.contains('흑색')) {
        expect(lv.family, LiveryFamily.black, reason: lv.id);
      }
      if (lv.nameKo.contains('그린')) expect(lv.family, LiveryFamily.green, reason: lv.id);
      if (lv.nameKo.contains('블루')) expect(lv.family, LiveryFamily.blue, reason: lv.id);
    }
    expect(repo.availableLiveryFamilies, contains(LiveryFamily.black));
    expect(repo.availableShapes.map((s) => s.id), contains('streamlined'));

    final green = repo.query(const FilterQuery(liveryFamilies: {LiveryFamily.green}));
    expect(green, isNotEmpty);
    expect(green.every((l) => repo.liveryOf(l)?.family == LiveryFamily.green), isTrue);
    expect(green.length, repo.countLiveryFamily(LiveryFamily.green));

    final stream = repo.query(const FilterQuery(shapes: {'streamlined'}));
    expect(stream.map((l) => l.id), contains('gb-lner-a4-mallard'));
    expect(stream.every((l) => repo.shapeOf(l).id == 'streamlined'), isTrue);

    // 둘을 겹치면 교집합. 맬러드는 가터 블루 + 유선형.
    final both = repo.query(const FilterQuery(
        liveryFamilies: {LiveryFamily.blue}, shapes: {'streamlined'}));
    expect(both.map((l) => l.id), contains('gb-lner-a4-mallard'));
    expect(both.length, lessThanOrEqualTo(stream.length));

    // 활성 개수에 포함된다.
    expect(const FilterQuery(liveryFamilies: {LiveryFamily.red}, shapes: {'american'}).activeCount, 2);
  });

  test('2색 도색 (v0.12): 둘째 색은 부위와 근거가 같이 있다', () {
    final two = repo.liveries.where((l) => l.accent != null).toList();
    expect(two.length, greaterThanOrEqualTo(9));
    for (final l in two) {
      expect(l.accent!.note, isNotEmpty, reason: l.id);
      expect(l.accent!.color, isNot(equals(l.body)), reason: l.id);
    }
    expect(repo.livery('cn-green')!.accent!.role, AccentRole.boiler);
    expect(repo.livery('cpr-royal-hudson')!.accent!.role, AccentRole.cabTender);
    expect(repo.livery('rocket-yellow')!.accent!.role, AccentRole.chimney);
    expect(repo.livery('drg-black')!.accent!.role, AccentRole.wheels);
    // 단색 도색은 accent 가 없다
    expect(repo.livery('jnr-black')!.accent, isNull);
  });

  test('정렬: 최고속도 내림차순 1위는 맬러드(202.8 km/h)', () {
    final sorted = repo.query(
      const FilterQuery(sortBy: SortBy.speed, descending: true),
    );
    expect(sorted.first.specs.topSpeedKmh, 202.8);
  });

  test('값이 없는 항목은 정렬에서 뒤로 밀린다 — 오름차순·내림차순 모두', () {
    for (final desc in [false, true]) {
      final sorted =
          repo.query(FilterQuery(sortBy: SortBy.speed, descending: desc));
      final firstNull = sorted.indexWhere((l) => l.specs.topSpeedKmh == null);
      expect(firstNull, greaterThan(0), reason: '속도 미상 항목이 있어야 검사가 의미 있다');
      expect(
        sorted.skip(firstNull).every((l) => l.specs.topSpeedKmh == null),
        isTrue,
        reason: 'desc=$desc: 값 없는 항목이 중간에 끼어 있다',
      );
      final known = sorted.take(firstNull).map((l) => l.specs.topSpeedKmh!).toList();
      for (var i = 1; i < known.length; i++) {
        expect(desc ? known[i] <= known[i - 1] : known[i] >= known[i - 1], isTrue,
            reason: 'desc=$desc: 순서가 어긋남 ${known[i - 1]} → ${known[i]}');
      }
    }
    // 예전 구현은 목록을 통째로 뒤집어서 내림차순 1위가 '—' 였다.
    final desc = repo.query(
        const FilterQuery(sortBy: SortBy.power, descending: true));
    expect(desc.first.specs.tractiveEffortKn, isNotNull);
  });

  test('지도에 찍을 좌표가 유효 범위 안에 있다', () {
    for (final l in repo.withLocation(const FilterQuery())) {
      expect(l.location!.lat, inInclusiveRange(-90, 90));
      expect(l.location!.lon, inInclusiveRange(-180, 180));
    }
  });

  test('현존 없음(scrapped)인데 보존 위치가 있으면 안 된다', () {
    for (final l in repo.all.where((l) => l.status == LocoStatus.scrapped)) {
      expect(l.location, isNull, reason: '${l.id}');
    }
  });

  test('모든 국가에 국기 SVG 에셋이 있다', () {
    for (final c in repo.countries) {
      final path = 'assets/flags/${c.code.toLowerCase()}.svg';
      expect(File(path).existsSync(), isTrue,
          reason: '$path 없음 — assets/flags/README.md 참조');
    }
  });

  test('국기 SVG는 외부 리소스를 참조하지 않는다 (오프라인 보장)', () {
    // w3.org URL은 XML 네임스페이스 선언이라 네트워크를 타지 않는다.
    // 실제로 문제가 되는 건 외부를 가리키는 href / url() 뿐이다.
    final external = RegExp(
      r'''(?:xlink:href|href)\s*=\s*["']https?://|url\(\s*['"]?https?://''',
    );
    for (final c in repo.countries) {
      final svg =
          File('assets/flags/${c.code.toLowerCase()}.svg').readAsStringSync();
      expect(external.hasMatch(svg), isFalse,
          reason: '${c.code}: 외부 리소스를 참조하고 있어 오프라인에서 깨질 수 있음');
      expect(svg.contains('<image'), isFalse,
          reason: '${c.code}: 래스터 <image> 포함 — SVG만 허용');
    }
  });

  test('오프라인 세계지도 에셋이 유효하다', () {
    final f = File('assets/map/world_110m.json');
    expect(f.existsSync(), isTrue, reason: 'python3 tools/build_worldmap.py 를 실행하세요');

    final j = jsonDecode(f.readAsStringSync()) as Map<String, dynamic>;
    final countries = j['countries'] as List;
    expect(countries.length, greaterThan(100));

    var points = 0;
    for (final c in countries) {
      for (final ring in ((c as Map<String, dynamic>)['rings'] as List)) {
        final flat = (ring as List).cast<num>();
        expect(flat.length.isEven, isTrue, reason: '좌표가 [lon,lat] 쌍이 아님');
        expect(flat.length, greaterThanOrEqualTo(8), reason: '링이 너무 짧음');
        for (var i = 0; i + 1 < flat.length; i += 2) {
          expect(flat[i], inInclusiveRange(-180, 180), reason: '경도 범위 초과');
          expect(flat[i + 1], inInclusiveRange(-90, 90), reason: '위도 범위 초과');
        }
        points += flat.length ~/ 2;
      }
    }
    // 너무 크면 앱 시작이 느려지고, 너무 작으면 대륙이 뭉개진다
    expect(points, inInclusiveRange(5000, 30000));
  });

  test('탄수차 축수가 상식 범위 안에 있다', () {
    for (final l in repo.all) {
      expect(l.effectiveTenderAxles, inInclusiveRange(0, 8), reason: l.id);
      // 탱크식·가라트는 별도 탄수차가 없다.
      // 예외: 페어리 퀸(2-2-2WT)은 웰탱크지만 석탄용 소형 탄수차를 실제로 끈다.
      if ((l.wheel.isTank || l.wheel.isGarratt) && l.id != 'in-fairyqueen') {
        expect(l.effectiveTenderAxles, 0, reason: l.id);
      }
      // 명시값이 있으면 그대로 쓴다
      if (l.tenderAxles != null) {
        expect(l.effectiveTenderAxles, l.tenderAxles, reason: l.id);
      }
    }
    // 대부분의 텐더 기관차는 탄수차가 그려져야 한다
    final tenderLocos =
        repo.all.where((l) => !l.wheel.isTank && !l.wheel.isGarratt);
    expect(tenderLocos.where((l) => l.effectiveTenderAxles > 0).length,
        greaterThan(tenderLocos.length ~/ 2));
  });

  test('도식 폭이 실제 그린 내용과 맞는다 (잘림 방지)', () {
    // 예전 버전은 폭을 어림잡아서 4-8-8-4 같은 긴 형식이 캔버스 밖으로 잘렸다.
    double w(String whyte, int tender) =>
        WhyteLayout(whyte: whyte, tenderAxles: tender, height: 40).width;

    // 축이 많을수록, 탄수차가 붙을수록 넓어져야 한다
    expect(w('4-8-8-4', 0), greaterThan(w('4-6-2', 0)));
    expect(w('4-6-2', 4), greaterThan(w('4-6-2', 0)));
    expect(w('4-8-8-4', 7), greaterThan(w('4-8-8-4', 0)));

    // 모든 실제 데이터에 대해 폭이 유한하고 최소한 바퀴들을 담을 만큼은 된다
    for (final l in repo.all) {
      final layout = WhyteLayout(
        whyte: l.wheel.whyte,
        tenderAxles: l.effectiveTenderAxles,
        height: 40,
      );
      expect(layout.width.isFinite, isTrue, reason: l.id);
      final all = [...layout.wheels, ...layout.tenderWheels];
      expect(all, isNotEmpty, reason: '${l.id}: 바퀴가 하나도 없음');
      for (final wheel in all) {
        expect(wheel.cx + wheel.r, lessThanOrEqualTo(layout.width),
            reason: '${l.id}: 바퀴가 폭 밖으로 나감');
        expect(wheel.cx - wheel.r, greaterThanOrEqualTo(0), reason: l.id);
      }
    }
  });

  test('가라트는 엔진 유닛이 둘로 나뉜다', () {
    final g = WhyteLayout(whyte: '4-8-2+2-8-4', tenderAxles: 0, height: 40);
    expect(g.engineUnits.length, 2);
    final single = WhyteLayout(whyte: '4-8-8-4', tenderAxles: 0, height: 40);
    expect(single.engineUnits.length, 1, reason: '관절식은 프레임이 하나다');
  });

  test('모든 기관차에 팔레트에 있는 도색이 지정돼 있다', () {
    expect(repo.liveries, isNotEmpty, reason: 'liveries 가 JSON에 없음');
    for (final l in repo.all) {
      expect(l.liveryId, isNotNull, reason: '${l.id}: 도색 미지정');
      expect(repo.liveryOf(l), isNotNull,
          reason: '${l.id}: 팔레트에 없는 도색 ${l.liveryId}');
    }
  });

  test('도색 팔레트에 중복·미사용 항목이 없다', () {
    final ids = repo.liveries.map((v) => v.id).toList();
    expect(ids.toSet().length, ids.length, reason: '중복 id');

    final used = repo.all.map((l) => l.liveryId).toSet();
    expect(ids.where((id) => !used.contains(id)), isEmpty,
        reason: '쓰이지 않는 도색은 팔레트에서 빼거나 기관차에 배정할 것');
  });

  test('도색 색상이 흰 도식 판 위에서 구분된다', () {
    // 도식은 테마와 무관하게 항상 흰 판(AppTheme.plate) 위에 그린다 (v0.9).
    // 실제 도색의 8할이 검정에 가까워서 다크 배경에서는 형식이 구분되지 않았다.
    double lum(Color c) {
      double ch(int v) {
        final s = v / 255;
        return s <= 0.03928
            ? s / 12.92
            : math.pow((s + 0.055) / 1.055, 2.4).toDouble();
      }

      return 0.2126 * ch((c.r * 255).round()) +
          0.7152 * ch((c.g * 255).round()) +
          0.0722 * ch((c.b * 255).round());
    }

    double ratio(Color a, Color b) {
      final x = lum(a), y = lum(b);
      return (math.max(x, y) + 0.05) / (math.min(x, y) + 0.05);
    }

    const plate = Color(0xFFFFFFFF); // AppTheme.plate

    for (final v in repo.liveries) {
      // 차체는 판 위에서 보여야 한다
      expect(ratio(v.body, plate), greaterThan(2.0),
          reason: '${v.id}: 흰 판에서 차체가 잘 안 보임');
      // 바퀴·레일 선도 판 위에 그린다
      expect(ratio(v.line, plate), greaterThan(3.0), reason: '${v.id}: line');
      // 차체 위에 겹쳐 긋는 선은 차체와 구분돼야 형태가 읽힌다
      // (이 검사가 없으면 검은 도색이 형태 없는 덩어리가 된다)
      expect(ratio(v.edge, v.body), greaterThan(1.8), reason: '${v.id}: edge');
    }
  });

  test('모든 기관차에 실루엣 유형이 지정돼 있다', () {
    expect(repo.shapes, isNotEmpty, reason: 'shapes 가 JSON에 없음');
    for (final l in repo.all) {
      expect(l.shapeId, isNotNull, reason: '${l.id}: shape 미지정');
      expect(repo.shape(l.shapeId), isNotNull,
          reason: '${l.id}: 등록되지 않은 shape ${l.shapeId}');
    }
    final ids = repo.shapes.map((s) => s.id).toList();
    expect(ids.toSet().length, ids.length, reason: '중복 id');
    final used = repo.all.map((l) => l.shapeId).toSet();
    expect(ids.where((id) => !used.contains(id)), isEmpty,
        reason: '쓰이지 않는 shape 는 빼거나 기관차에 배정할 것');
  });

  test('실루엣 유형이 실제로 서로 다른 그림을 만든다', () {
    // 유형을 넣어놓고 도식이 똑같이 나오면 의미가 없다.
    // 굴뚝 높이·운전실·유선형 조합이 유형마다 달라야 한다.
    final signatures = <String>{};
    for (final s in repo.shapes) {
      signatures.add([
        s.chimney.name,
        s.cab.name,
        s.domes,
        s.casing.name,
        s.lamp,
        s.pilot,
        s.cylinder.name,
      ].join('/'));
    }
    expect(signatures.length, repo.shapes.length,
        reason: '생김새가 완전히 같은 유형이 둘 이상 있음');

    // 유선형은 굴뚝이 보이지 않아야 하고, 운전실 없는 초기형은 굴뚝이 높다
    for (final s in repo.shapes) {
      if (s.casing == CasingStyle.full) {
        expect(s.chimney, ChimneyStyle.none, reason: '${s.id}: 케이싱에 덮인 굴뚝');
        expect(s.domes, 0, reason: '${s.id}: 케이싱 위로 돔이 튀어나올 수 없다');
      }
      if (s.cab == CabStyle.none) {
        expect(s.chimney, ChimneyStyle.tall, reason: '${s.id}: 초기형은 굴뚝이 높다');
      }
    }
  });

  test('커플링로드가 실제 규칙대로 걸린다', () {
    List<List<int>> groups(String whyte, {LocoShape? shape}) => WhyteLayout(
          whyte: whyte,
          tenderAxles: 0,
          height: 40,
          shape: shape,
        ).driverGroups;

    // 관절식은 동륜군이 둘 — 로드가 하나로 이어지면 안 된다
    expect(groups('4-8-8-4').length, 2);
    expect(groups('4-8-8-4').every((g) => g.length == 4), isTrue);
    // 가라트도 엔진 유닛마다 따로
    expect(groups('4-8-2+2-8-4').length, 2);
    // 단동륜기는 동륜이 1축 — 커플링로드가 없다
    expect(groups('0-2-2').single.length, 1);
    expect(groups('4-2-0').single.length, 1);
    // 일반형은 하나로 이어진다
    expect(groups('4-6-2').single.length, 3);
    expect(groups('2-10-2').single.length, 5);

    // 데이터 전체에서 동륜 수가 Whyte 표기와 맞아야 한다
    for (final l in repo.all) {
      final total = groups(l.wheel.whyte, shape: repo.shapeOf(l))
          .fold<int>(0, (a, g) => a + g.length);
      expect(total * 2, l.wheel.drivingWheels, reason: l.id);
    }
  });

  test('탱크식 분류와 Whyte 표기가 어긋나지 않는다', () {
    // serviceType 만 tank 로 적어두면 탄수차가 조용히 사라진다 (모가형에서 실제로 겪음)
    for (final l in repo.all) {
      if (l.serviceType == ServiceType.tank) {
        expect(l.wheel.isTank, isTrue,
            reason: '${l.id}: 탱크식인데 Whyte(${l.wheel.whyte})에 T가 없다');
      }
    }
  });

  test('카우캐처가 붙어도 도식이 캔버스 밖으로 나가지 않는다', () {
    // 카우캐처는 차체보다 앞으로 튀어나오므로 레이아웃이 앞자리를 비워둬야 한다.
    for (final l in repo.all) {
      final layout = WhyteLayout(
        whyte: l.wheel.whyte,
        tenderAxles: l.effectiveTenderAxles,
        height: 40,
        shape: repo.shapeOf(l),
      );
      expect(layout.frontPad, greaterThanOrEqualTo(0), reason: l.id);
      for (final w in [...layout.wheels, ...layout.tenderWheels]) {
        expect(w.cx - w.r, greaterThanOrEqualTo(layout.frontPad), reason: l.id);
        expect(w.cx + w.r, lessThanOrEqualTo(layout.width), reason: l.id);
      }
    }
  });

  test('연표 그룹은 시대 순서를 유지한다', () {
    final grouped = repo.groupedByEra(const FilterQuery());
    final order = grouped.keys.map((e) => e.from).toList();
    final sorted = [...order]..sort();
    expect(order, sorted);
  });
}
