/// 증기기관차 도메인 모델.
///
/// assets/data/locomotives.json 의 스키마(schemaVersion 1)와 1:1로 대응한다.
/// 데이터 추가는 tools/build_seed.py 에서 하고 JSON을 다시 생성할 것.
library;

import 'dart:ui' show Brightness, Color;

int? _i(dynamic v) => v == null ? null : (v as num).toInt();
double? _d(dynamic v) => v == null ? null : (v as num).toDouble();
List<String> _s(dynamic v) =>
    v == null ? const [] : (v as List).map((e) => e.toString()).toList();

/// 보존/운행 상태.
enum LocoStatus {
  operational, // 운행 중 (본선·관광열차 견인)
  operable, // 동태보존 (움직일 수 있음)
  static_, // 정태보존 (전시)
  restoration, // 복원 중
  scrapped, // 현존 개체 없음
  replica; // 복제품만 존재

  static LocoStatus parse(String? raw) => switch (raw) {
        'operational' => LocoStatus.operational,
        'operable' => LocoStatus.operable,
        'restoration' => LocoStatus.restoration,
        'scrapped' => LocoStatus.scrapped,
        'replica' => LocoStatus.replica,
        _ => LocoStatus.static_,
      };

  String get labelKo => switch (this) {
        LocoStatus.operational => '운행 중',
        LocoStatus.operable => '동태보존',
        LocoStatus.static_ => '정태보존',
        LocoStatus.restoration => '복원 중',
        LocoStatus.scrapped => '현존 없음',
        LocoStatus.replica => '복제품',
      };

  /// 실제로 증기를 올릴 수 있는 상태인가.
  bool get isAlive => this == LocoStatus.operational || this == LocoStatus.operable;
}

/// 용도 분류.
enum ServiceType {
  express, // 급행 여객
  mixed, // 혼합
  freight, // 화물
  tank, // 탱크식·입환
  articulated, // 관절식
  narrow, // 협궤
  rack; // 치차(등판)

  static ServiceType parse(String? raw) => switch (raw) {
        'express' => ServiceType.express,
        'freight' => ServiceType.freight,
        'tank' => ServiceType.tank,
        'articulated' => ServiceType.articulated,
        'narrow' => ServiceType.narrow,
        'rack' => ServiceType.rack,
        _ => ServiceType.mixed,
      };

  String get labelKo => switch (this) {
        ServiceType.express => '급행 여객',
        ServiceType.mixed => '혼합용',
        ServiceType.freight => '화물',
        ServiceType.tank => '탱크식',
        ServiceType.articulated => '관절식',
        ServiceType.narrow => '협궤',
        ServiceType.rack => '치차식',
      };
}

/// 차륜 배치. Whyte 표기가 1차 키.
class Wheel {
  final String whyte; // 예: "4-6-2"
  final String? uic; // 예: "2'C1'h3"
  final String? typeName; // 예: "Pacific"

  const Wheel({required this.whyte, this.uic, this.typeName});

  factory Wheel.fromJson(Map<String, dynamic> j) => Wheel(
        whyte: j['whyte'] as String,
        uic: j['uic'] as String?,
        typeName: j['typeName'] as String?,
      );

  /// 엔진 유닛별 차륜 그룹. 가라트("4-8-2+2-8-4")는 유닛이 둘이라 [[4,8,2],[2,8,4]].
  /// 탱크식 접미사(T/ST)는 숫자만 뽑으면서 자연히 걸러진다.
  List<List<int>> get unitGroups => whyte
      .split('+')
      .map((u) => u
          .split('-')
          .map((p) => int.tryParse(p.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0)
          .toList())
      .toList();

  /// 동륜 개수(구동축 바퀴 수). 도식 그리기와 정렬에 쓴다.
  ///
  /// **유닛별로 세야 한다.** 가라트를 통째로 이어 붙여 세면
  /// 앞 유닛의 종륜과 뒤 유닛의 선륜까지 동륜으로 잡힌다
  /// (4-8-2+2-8-4 가 16이 아니라 20으로 나왔다).
  int get drivingWheels {
    var total = 0;
    for (final g in unitGroups) {
      if (g.length < 3) {
        total += g.isEmpty ? 0 : g.reduce((a, b) => a > b ? a : b);
      } else {
        // 첫 그룹(선륜)과 마지막 그룹(종륜)을 제외한 나머지가 동륜
        total += g.sublist(1, g.length - 1).fold(0, (a, b) => a + b);
      }
    }
    return total;
  }

  bool get isTank => whyte.toUpperCase().contains('T');
  bool get isGarratt => whyte.contains('+');
}

/// 도색(livery).
///
/// 기관차마다 색을 따로 적지 않고 팔레트로 뽑아 놓았다. 같은 철도의 기관차가
/// 자동으로 같은 색을 쓰고, 상세 화면에 도색 이름("LNER 가터 블루")을 띄울 수 있다.
///
/// 라이트/다크 두 벌을 갖는 이유: 실제 도색의 8할은 검정에 가까운데,
/// 다크 테마 배경(#15171A) 위에 그대로 칠하면 형체가 사라진다.
/// 그래서 색상(hue)은 유지한 채 밝기만 끌어올린 다크용 값을 따로 만든다.
/// (생성은 tools/build_seed.py 의 `livery_objs()`)
/// 도색의 색상 계열 — 탐색 필터 칩용 (v0.12).
///
/// 값은 `tools/build_seed.py` 의 `livery_family` 가 기준색의 HLS 로 정해 JSON 에 넣는다.
/// 44종을 칩으로 다 늘어놓을 수 없어서 여섯 계열로 묶었다. 앱은 계산하지 않고 읽기만 한다.
enum LiveryFamily {
  black,
  gray,
  green,
  blue,
  red,
  yellow;

  static LiveryFamily? parse(String? raw) => switch (raw) {
        'black' => LiveryFamily.black,
        'gray' => LiveryFamily.gray,
        'green' => LiveryFamily.green,
        'blue' => LiveryFamily.blue,
        'red' => LiveryFamily.red,
        'yellow' => LiveryFamily.yellow,
        _ => null,
      };

  String get labelKo => switch (this) {
        LiveryFamily.black => '검정',
        LiveryFamily.gray => '회색',
        LiveryFamily.green => '녹색',
        LiveryFamily.blue => '파랑',
        LiveryFamily.red => '빨강',
        LiveryFamily.yellow => '노랑',
      };

  /// 칩에 찍는 견본색 — 계열의 대표 도색(라이트 기준색)에서 가져왔다.
  Color get swatch => switch (this) {
        LiveryFamily.black => const Color(0xFF2A2D33), // BR 블랙
        LiveryFamily.gray => const Color(0xFF8E949C), // 밀워키 로드 그레이
        LiveryFamily.green => const Color(0xFF2C5741), // SNCF 그린
        LiveryFamily.blue => const Color(0xFF1E3A6E), // LNER 가터 블루
        LiveryFamily.red => const Color(0xFF8E2226), // 독일 고속기 레드
        LiveryFamily.yellow => const Color(0xFFC9A227), // 로켓 옐로
      };
}

/// 2색 도색에서 둘째 색이 칠해지는 부위 (v0.12).
enum AccentRole {
  boiler, // 보일러 통 (운전실·치마·탄수차는 body)
  cabTender, // 운전실·탄수차·치마 (보일러는 body)
  chimney, // 굴뚝
  wheels; // 바퀴 중심·주행부

  static AccentRole? parse(String? raw) => switch (raw) {
        'boiler' => AccentRole.boiler,
        'cabTender' => AccentRole.cabTender,
        'chimney' => AccentRole.chimney,
        'wheels' => AccentRole.wheels,
        _ => null,
      };

  String get labelKo => switch (this) {
        AccentRole.boiler => '보일러',
        AccentRole.cabTender => '운전실·탄수차',
        AccentRole.chimney => '굴뚝',
        AccentRole.wheels => '바퀴',
      };
}

/// 2색 도색의 둘째 색. 판이 항상 흰색이라 테마별 변형은 두지 않는다.
class LiveryAccent {
  const LiveryAccent({required this.role, required this.color, this.note = ''});
  final AccentRole role;
  final Color color;

  /// 근거 메모 (예: "CN 6060: 보일러·연실은 검정…"). 상세 화면 도색 줄에 쓴다.
  final String note;
}

class Livery {
  final String id;
  final String nameKo;
  final String nameEn;

  /// 색상 계열 (필터용). 구버전 JSON 에는 없을 수 있어 null 허용.
  final LiveryFamily? family;

  /// 둘째 색 — 대부분의 도색은 단색이라 null.
  final LiveryAccent? accent;

  /// 라이트 테마용 — 차체 채움색 / 배경 위의 선(바퀴·레일) / 차체 위의 선.
  ///
  /// [line] 과 [edge] 를 나눈 이유: 검은 도색은 차체도 선도 검정이라
  /// 한 색으로 그리면 보일러·운전실 경계가 뭉개진다. [edge] 는 차체 밝기의
  /// 반대쪽으로 뽑으므로 어떤 도색에서도 형태가 읽힌다.
  final Color body;
  final Color line;
  final Color edge;

  /// 같은 도색의 다크 테마용 값.
  final Color bodyDark;
  final Color lineDark;
  final Color edgeDark;

  const Livery({
    required this.id,
    required this.nameKo,
    required this.nameEn,
    this.family,
    this.accent,
    required this.body,
    required this.line,
    required this.edge,
    required this.bodyDark,
    required this.lineDark,
    required this.edgeDark,
  });

  factory Livery.fromJson(Map<String, dynamic> j) => Livery(
        id: j['id'] as String,
        nameKo: j['nameKo'] as String,
        nameEn: j['nameEn'] as String,
        family: LiveryFamily.parse(j['family'] as String?),
        accent: _accent(j['accent']),
        body: _color(j['body']),
        line: _color(j['line']),
        edge: _color(j['edge'] ?? j['line']),
        bodyDark: _color(j['bodyDark']),
        lineDark: _color(j['lineDark']),
        edgeDark: _color(j['edgeDark'] ?? j['lineDark']),
      );

  static LiveryAccent? _accent(dynamic j) {
    if (j is! Map) return null;
    final role = AccentRole.parse(j['role'] as String?);
    if (role == null || j['color'] == null) return null;
    return LiveryAccent(
      role: role,
      color: _color(j['color']),
      note: (j['note'] as String?) ?? '',
    );
  }

  /// "#1E3A6E" → Color. 알파는 항상 불투명.
  static Color _color(dynamic hex) =>
      Color(0xFF000000 | int.parse((hex as String).substring(1), radix: 16));

  Color bodyFor(Brightness b) => b == Brightness.dark ? bodyDark : body;
  Color lineFor(Brightness b) => b == Brightness.dark ? lineDark : line;
  Color edgeFor(Brightness b) => b == Brightness.dark ? edgeDark : edge;
}

/// 굴뚝 높이. 초기 기관차일수록 높다.
enum ChimneyStyle {
  tall,
  mid,
  short,
  none; // 유선형 케이싱에 덮여 보이지 않음

  static ChimneyStyle parse(String? raw) => switch (raw) {
        'tall' => ChimneyStyle.tall,
        'short' => ChimneyStyle.short,
        'none' => ChimneyStyle.none,
        _ => ChimneyStyle.mid,
      };
}

/// 운전실. 초기 기관차에는 아예 없었다.
enum CabStyle {
  none,
  open, // 지붕만 있는 개방형
  full;

  static CabStyle parse(String? raw) => switch (raw) {
        'none' => CabStyle.none,
        'open' => CabStyle.open,
        _ => CabStyle.full,
      };
}

/// 실린더 배치. **로드(연결봉)를 어떻게 그릴지**가 여기서 갈린다.
enum CylinderStyle {
  /// 프레임 바깥 — 실린더 블록과 메인로드가 옆에서 보인다 (20세기 기관차 대부분)
  outside,

  /// 프레임 사이 — 옆에서는 실린더도 메인로드도 안 보이고 커플링로드만 보인다
  inside,

  /// 경사 실린더 — 로켓호
  angled,

  /// 보일러 위 수직 실린더 — 로코모션 1호
  vertical,

  /// 정치기관식. 플라이휠로 구동해 커플링로드가 없다 — 페니다렌
  beam;

  static CylinderStyle parse(String? raw) => switch (raw) {
        'inside' => CylinderStyle.inside,
        'angled' => CylinderStyle.angled,
        'vertical' => CylinderStyle.vertical,
        'beam' => CylinderStyle.beam,
        _ => CylinderStyle.outside,
      };

  /// 실린더 블록과 메인로드가 옆에서 보이는가.
  bool get showsMainRod => this == CylinderStyle.outside;

  /// 동륜끼리 커플링로드로 이어지는가.
  /// 페니다렌은 기어 구동이라 커플링로드가 없었다.
  bool get coupled => this != CylinderStyle.beam;
}

/// 유선형 케이싱.
enum CasingStyle {
  none,
  half, // 앞머리·옆면만 덮은 스커트
  full;

  static CasingStyle parse(String? raw) => switch (raw) {
        'half' => CasingStyle.half,
        'full' => CasingStyle.full,
        _ => CasingStyle.none,
      };
}

/// 실루엣 유형.
///
/// 차륜 배치만 그리면 1829년 로켓호와 1950년대 대형기가 똑같이 나온다.
/// 굴뚝 높이·운전실 유무·유선형 케이싱처럼 **멀리서 봐도 다른** 특징을
/// 유형으로 묶어 도식에 반영한다. (생성은 tools/build_seed.py 의 `SHAPES`)
class LocoShape {
  final String id;
  final String nameKo;
  final ChimneyStyle chimney;
  final CabStyle cab;
  final int domes; // 보일러 위 증기돔·모래돔 수 (0~2)
  final CasingStyle casing;
  final bool lamp; // 앞 전조등
  final bool pilot; // 카우캐처(배장기)
  final CylinderStyle cylinder;
  final String note;

  const LocoShape({
    required this.id,
    required this.nameKo,
    required this.chimney,
    required this.cab,
    required this.domes,
    required this.casing,
    required this.lamp,
    required this.pilot,
    required this.cylinder,
    required this.note,
  });

  /// 데이터가 없을 때 쓰는 기본형 — 예전 도식과 같은 모습.
  static const fallback = LocoShape(
    id: 'classic',
    nameKo: '표준형',
    chimney: ChimneyStyle.mid,
    cab: CabStyle.full,
    domes: 0,
    casing: CasingStyle.none,
    lamp: false,
    pilot: false,
    cylinder: CylinderStyle.outside,
    note: '',
  );

  factory LocoShape.fromJson(Map<String, dynamic> j) => LocoShape(
        id: j['id'] as String,
        nameKo: j['nameKo'] as String? ?? '',
        chimney: ChimneyStyle.parse(j['chimney'] as String?),
        cab: CabStyle.parse(j['cab'] as String?),
        domes: _i(j['domes']) ?? 0,
        casing: CasingStyle.parse(j['casing'] as String?),
        lamp: j['lamp'] as bool? ?? false,
        pilot: j['pilot'] as bool? ?? false,
        cylinder: CylinderStyle.parse(j['cylinder'] as String?),
        note: j['note'] as String? ?? '',
      );

  bool get isStreamlined => casing == CasingStyle.full;
}

/// 중량이 무엇을 재 것인지. 기관차 단독 중량과 탄수차까지 합친 운전정비중량은
/// 두 배 가까이 차이가 나므로 숫자만 보여주면 비교가 틀어진다.
enum WeightBasis {
  loco('기관차 단독'),
  locoAndTender('기관차+탄수차');

  const WeightBasis(this.labelKo);
  final String labelKo;

  static WeightBasis? parse(String? v) {
    switch (v) {
      case 'loco':
        return WeightBasis.loco;
      case 'locoAndTender':
        return WeightBasis.locoAndTender;
      default:
        return null;
    }
  }
}

/// 제원. 값이 없는 항목은 null — UI에서 '—'로 표시한다.
class LocoSpecs {
  final int? lengthMm;
  final double? weightT;

  /// [weightT] 의 기준. null 이면 출처에서 확인되지 않은 값이다.
  final WeightBasis? weightBasis;
  final int? driverDiameterMm;
  final double? boilerPressureBar;
  final int? cylinders;
  final double? tractiveEffortKn;
  final int? powerKw;
  final double? topSpeedKmh;

  const LocoSpecs({
    this.lengthMm,
    this.weightT,
    this.weightBasis,
    this.driverDiameterMm,
    this.boilerPressureBar,
    this.cylinders,
    this.tractiveEffortKn,
    this.powerKw,
    this.topSpeedKmh,
  });

  factory LocoSpecs.fromJson(Map<String, dynamic> j) => LocoSpecs(
        lengthMm: _i(j['lengthMm']),
        weightT: _d(j['weightT']),
        weightBasis: WeightBasis.parse(j['weightBasis'] as String?),
        driverDiameterMm: _i(j['driverDiameterMm']),
        boilerPressureBar: _d(j['boilerPressureBar']),
        cylinders: _i(j['cylinders']),
        tractiveEffortKn: _d(j['tractiveEffortKn']),
        powerKw: _i(j['powerKw']),
        topSpeedKmh: _d(j['topSpeedKmh']),
      );

  /// 채워진 항목 비율 — 데이터 완성도 표시용.
  double get completeness {
    final all = [
      lengthMm,
      weightT,
      driverDiameterMm,
      boilerPressureBar,
      cylinders,
      tractiveEffortKn,
      powerKw,
      topSpeedKmh
    ];
    return all.where((e) => e != null).length / all.length;
  }
}

class LocoLocation {
  final String name;
  final double lat;
  final double lon;

  /// 지도 앱에 넘길 검색어 — 그 지도 앱이 알아듣는 시설의 공식 명칭(예: "National Railway Museum York").
  /// 있으면 지도 앱이 실제 장소(주소·사진 포함)를 찾아 보여주고, 없으면 좌표 핀에 [name] 라벨만 붙인다.
  /// '각지 보존' 처럼 특정 시설이 아닌 위치는 일부러 비워 둔다 — 엉뚱한 장소가 잡히는 것보다 낫다.
  final String? query;

  const LocoLocation({
    required this.name,
    required this.lat,
    required this.lon,
    this.query,
  });

  factory LocoLocation.fromJson(Map<String, dynamic> j) => LocoLocation(
        name: j['name'] as String,
        lat: (j['lat'] as num).toDouble(),
        lon: (j['lon'] as num).toDouble(),
        query: j['query'] as String?,
      );
}

class Locomotive {
  final String id;
  final String nameKo;
  final String nameEn;

  /// 별명·애칭(Kriegslok, 티거리, 아름다운 헬레나…). 공인 형식명이 아니므로
  /// [nameKo]/[nameEn] 에는 넣지 않고 여기에만 둔다.
  final String? nickname;
  final String classDesignation;
  final String? roadNumber;
  final String countryCode;
  final String eraId;
  final List<String> operators;
  final List<String> builders;
  final String? designer;
  final int? builtFrom;
  final int? builtTo;
  final int? quantityBuilt;
  final int? withdrawnYear;
  final Wheel wheel;

  /// 탄수차 차축 수. `null` 이면 크기·시대로 추정한다([effectiveTenderAxles]).
  /// `0` 은 '탄수차 없음'을 명시하는 값.
  final int? tenderAxles;

  /// 도색 id([Livery.id]). 실제 색은 리포지토리에서 팔레트를 찾아 쓴다.
  final String? liveryId;

  /// 실루엣 유형 id([LocoShape.id]).
  final String? shapeId;

  final int gaugeMm;
  final ServiceType serviceType;
  final LocoSpecs specs;
  final LocoStatus status;
  final int? survivors;
  final LocoLocation? location;
  final bool iconic;
  final List<String> highlights;
  final String summary;
  final List<String> tags;
  final List<String> sources;

  /// 이 형식·개체를 직접 다루는 서적·논문·공식 자료. 웹 출처는 [sources].
  final List<Reference> references;
  final bool verified;

  const Locomotive({
    required this.id,
    required this.nameKo,
    required this.nameEn,
    required this.nickname,
    required this.classDesignation,
    required this.roadNumber,
    required this.countryCode,
    required this.eraId,
    required this.operators,
    required this.builders,
    required this.designer,
    required this.builtFrom,
    required this.builtTo,
    required this.quantityBuilt,
    required this.withdrawnYear,
    required this.wheel,
    required this.tenderAxles,
    required this.liveryId,
    required this.shapeId,
    required this.gaugeMm,
    required this.serviceType,
    required this.specs,
    required this.status,
    required this.survivors,
    required this.location,
    required this.iconic,
    required this.highlights,
    required this.summary,
    required this.tags,
    required this.sources,
    this.references = const [],
    required this.verified,
  });

  factory Locomotive.fromJson(Map<String, dynamic> j) => Locomotive(
        id: j['id'] as String,
        nameKo: j['nameKo'] as String,
        nameEn: j['nameEn'] as String,
        nickname: j['nickname'] as String?,
        classDesignation: j['classDesignation'] as String,
        roadNumber: j['roadNumber'] as String?,
        countryCode: j['countryCode'] as String,
        eraId: j['era'] as String,
        operators: _s(j['operators']),
        builders: _s(j['builders']),
        designer: j['designer'] as String?,
        builtFrom: _i(j['builtFrom']),
        builtTo: _i(j['builtTo']),
        quantityBuilt: _i(j['quantityBuilt']),
        withdrawnYear: _i(j['withdrawnYear']),
        wheel: Wheel.fromJson(j['wheel'] as Map<String, dynamic>),
        tenderAxles: _i(j['tenderAxles']),
        liveryId: j['livery'] as String?,
        shapeId: j['shape'] as String?,
        gaugeMm: _i(j['gaugeMm']) ?? 1435,
        serviceType: ServiceType.parse(j['serviceType'] as String?),
        specs: LocoSpecs.fromJson(j['specs'] as Map<String, dynamic>),
        status: LocoStatus.parse(j['status'] as String?),
        survivors: _i(j['survivors']),
        location: j['location'] == null
            ? null
            : LocoLocation.fromJson(j['location'] as Map<String, dynamic>),
        iconic: j['iconic'] as bool? ?? false,
        highlights: _s(j['highlights']),
        summary: j['summary'] as String? ?? '',
        tags: _s(j['tags']),
        sources: _s(j['sources']),
        references: Reference.listFrom(j['references']),
        verified: j['verified'] as bool? ?? false,
      );

  /// 도식에 그릴 탄수차 차축 수.
  ///
  /// 데이터에 값이 있으면 그대로 쓰고, 없으면 중량·연대로 추정한다.
  /// **추정값은 도식용 근사다.** 실제 탄수차 형식은 같은 기관차라도
  /// 시기·소속 철도에 따라 달랐다. 정확한 값이 필요하면
  /// `tools/build_seed.py` 에서 `tender=` 로 명시할 것.
  int get effectiveTenderAxles {
    if (tenderAxles != null) return tenderAxles!;
    // 탱크식은 물·석탄을 기관차가 직접 싣는다. 가라트도 별도 탄수차가 없다.
    if (wheel.isTank || wheel.isGarratt) return 0;
    if (serviceType == ServiceType.tank || serviceType == ServiceType.rack) {
      return 0;
    }
    if (builtFrom != null && builtFrom! < 1850) return 2;
    final w = specs.weightT;
    if (w == null) return 3;
    if (w < 60) return 2;
    if (w < 120) return 3;
    if (w < 260) return 4;
    if (w < 420) return 5;
    return 6;
  }

  /// "1936–1945" / "1938" 형태의 제작 기간 표기.
  String get builtLabel {
    if (builtFrom == null) return '—';
    if (builtTo == null || builtTo == builtFrom) return '$builtFrom';
    return '$builtFrom–$builtTo';
  }

  /// 검색 매칭용 소문자 인덱스. 리포지토리에서 한 번만 만들어 캐싱한다.
  String get searchIndex => [
        nameKo,
        nameEn,
        nickname ?? '',
        classDesignation,
        roadNumber ?? '',
        wheel.whyte,
        wheel.typeName ?? '',
        designer ?? '',
        ...operators,
        ...builders,
        ...tags,
      ].join(' ').toLowerCase();
}

/// 시대 구분.
class Era {
  final String id;
  final String nameKo;
  final String nameEn;
  final int from;
  final int to;
  final String note;

  const Era({
    required this.id,
    required this.nameKo,
    required this.nameEn,
    required this.from,
    required this.to,
    required this.note,
  });

  factory Era.fromJson(Map<String, dynamic> j) => Era(
        id: j['id'] as String,
        nameKo: j['ko'] as String,
        nameEn: j['en'] as String,
        from: (j['from'] as num).toInt(),
        to: (j['to'] as num).toInt(),
        note: j['note'] as String? ?? '',
      );

  String get rangeLabel => to >= 2100 ? '$from~현재' : '$from–$to';
}

/// 참고문헌 — 서적·논문·공식 간행물. 웹 페이지(sources)와 구분한다.
///
/// 종이 문헌은 링크가 없어도 값이 있다: 도서관 목록·출판사에서 서지를 확인한 것만 데이터에 넣는다
/// (`tools/references.py`). [via] 는 어디서 확인했는지, [note] 는 무엇을 다루는지.
class Reference {
  final String kind; // book | article | thesis | official | catalog
  final String title;
  final String author;
  final String publisher;
  final int? year;
  final String lang;
  final String? isbn;
  final String? url;
  final String note;
  final String via;

  const Reference({
    required this.kind,
    required this.title,
    required this.author,
    required this.publisher,
    required this.year,
    required this.lang,
    required this.isbn,
    required this.url,
    required this.note,
    required this.via,
  });

  factory Reference.fromJson(Map<String, dynamic> j) => Reference(
        kind: j['kind'] as String? ?? 'book',
        title: j['title'] as String,
        author: j['author'] as String? ?? '',
        publisher: j['publisher'] as String? ?? '',
        year: _i(j['year']),
        lang: j['lang'] as String? ?? '',
        isbn: j['isbn'] as String?,
        url: j['url'] as String?,
        note: j['note'] as String? ?? '',
        via: j['via'] as String? ?? '',
      );

  static List<Reference> listFrom(dynamic v) => ((v as List?) ?? const [])
      .map((e) => Reference.fromJson(e as Map<String, dynamic>))
      .toList();

  /// 같은 문헌인지 — 제목·저자·연도로 본다.
  String get dedupeKey => '$title|$author|${year ?? ''}';

  /// [refs] 중 [already] 에 이미 있는 문헌을 뺀 목록. 형식 문헌과 국가 문헌에 같은 책이 겹칠 때 쓴다.
  static List<Reference> except(List<Reference> refs, List<Reference> already) {
    final seen = already.map((r) => r.dedupeKey).toSet();
    return refs.where((r) => !seen.contains(r.dedupeKey)).toList();
  }

  String get kindLabelKo => switch (kind) {
        'article' => '논문·기사',
        'thesis' => '학위논문',
        'official' => '공식 자료',
        'catalog' => '소장품 기록',
        _ => '단행본',
      };

  /// "저자, 『제목』, 출판사, 연도" 꼴의 한 줄 인용.
  String get citation {
    final parts = <String>[
      if (author.isNotEmpty) author,
      '『$title』',
      if (publisher.isNotEmpty) publisher,
      year == null ? '연도 미확인' : '$year',
    ];
    return parts.join(', ');
  }
}

/// 국가.
class Country {
  final String code;
  final String nameKo;
  final String nameEn;
  final String flag;
  final double lat;
  final double lon;
  final String blurb;

  /// 이 나라 증기기관차 전반을 다루는 표준 문헌.
  final List<Reference> references;

  const Country({
    required this.code,
    required this.nameKo,
    required this.nameEn,
    required this.flag,
    required this.lat,
    required this.lon,
    required this.blurb,
    this.references = const [],
  });

  factory Country.fromJson(Map<String, dynamic> j) => Country(
        code: j['code'] as String,
        nameKo: j['nameKo'] as String,
        nameEn: j['nameEn'] as String,
        flag: j['flag'] as String,
        lat: (j['lat'] as num).toDouble(),
        lon: (j['lon'] as num).toDouble(),
        blurb: j['blurb'] as String? ?? '',
        references: Reference.listFrom(j['references']),
      );
}
