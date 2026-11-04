/// 증기기관차 도메인 모델.
///
/// assets/data/locomotives.json 의 스키마(schemaVersion 2)와 1:1로 대응한다.
/// 데이터는 tools/build_seed.py 가 만든다 — 초안 + 출처 대조본(tools/verified.py) + 자료조사 원고
/// (tools/manuscript/entries.json). JSON 을 손으로 고치지 말 것.
library;

import 'dart:ui' show Brightness, Color;

int? _i(dynamic v) => v == null ? null : (v as num).toInt();
double? _d(dynamic v) => v == null ? null : (v as num).toDouble();
List<String> _s(dynamic v) =>
    v == null ? const [] : (v as List).map((e) => e.toString()).toList();
List<int> _ints(dynamic v) =>
    v == null ? const [] : (v as List).map((e) => (e as num).toInt()).toList();

/// 화면 언어. 데이터(이름·설명 글·제원 주석·출처)는 한국어와 영어가 짝으로 들어 있다.
/// 화면 문구는 아직 한국어뿐이다 — 영어 화면은 새 디자인을 옮길 때 붙인다.
enum Lang { ko, en }

/// 한영 짝 글.
class Bilingual {
  const Bilingual(this.ko, this.en);
  final String ko;
  final String en;

  /// 영어가 비어 있으면 한국어로 대신한다.
  String of(Lang lang) => lang == Lang.en && en.isNotEmpty ? en : ko;

  static Bilingual? fromJson(dynamic j) {
    if (j is! Map) return null;
    return Bilingual(j['ko'] as String? ?? '', j['en'] as String? ?? '');
  }
}

/// 출처 번호가 붙은 한영 문장 — 뜻풀이, 본문 한 문장, 표제란 수량 문구.
/// [src] 는 그 항목의 출처 목록([Locomotive.sources]) 번호다.
class SourcedText {
  const SourcedText({required this.ko, required this.en, this.src = const []});
  final String ko;
  final String en;
  final List<int> src;

  String of(Lang lang) => lang == Lang.en && en.isNotEmpty ? en : ko;

  factory SourcedText.fromJson(Map<String, dynamic> j) => SourcedText(
        ko: j['ko'] as String? ?? '',
        en: j['en'] as String? ?? '',
        src: _ints(j['src']),
      );

  static SourcedText? maybe(dynamic j) =>
      j is Map<String, dynamic> ? SourcedText.fromJson(j) : null;

  static List<SourcedText> listFrom(dynamic v) => ((v as List?) ?? const [])
      .map((e) => SourcedText.fromJson(e as Map<String, dynamic>))
      .toList();
}

/// 연혁 한 줄. 날짜는 "1899", "1899-09", "1899-09-18" 중 하나.
class HistoryEvent {
  const HistoryEvent({
    required this.date,
    required this.ko,
    required this.en,
    this.approx = false,
    this.src = const [],
  });

  final String date;

  /// 날짜가 어림값인가("1918년경").
  final bool approx;
  final String ko;
  final String en;
  final List<int> src;

  factory HistoryEvent.fromJson(Map<String, dynamic> j) => HistoryEvent(
        date: j['date'] as String,
        approx: j['approx'] as bool? ?? false,
        ko: j['ko'] as String? ?? '',
        en: j['en'] as String? ?? '',
        src: _ints(j['src']),
      );

  String of(Lang lang) => lang == Lang.en && en.isNotEmpty ? en : ko;

  List<int?> get _parts {
    final p = date.split('-');
    int? at(int i) => i < p.length ? int.tryParse(p[i]) : null;
    return [at(0), at(1), at(2)];
  }

  int? get year => _parts[0];

  static const _months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
  ];

  /// 날짜 표기 — 한국어 "1899. 9. 18." / "1918년경" / "1943년 7월경", 영어 "Sep 18, 1899" / "c. 1918".
  String dateLabel(Lang lang) {
    final [y, m, d] = _parts;
    if (lang == Lang.en) {
      final t = [
        if (m != null) _months[m - 1],
        if (d != null) '$d,',
        '$y',
      ].join(' ');
      return approx ? 'c. $t' : t;
    }
    // 어림값은 '경'을 맨 뒤에 — "1943년 7월경", "1825년 9월 18일경".
    if (approx) {
      if (m == null) return '$y년경';
      return d == null ? '$y년 $m월경' : '$y년 $m월 $d일경';
    }
    if (m == null) return '$y';
    return '$y. $m.${d != null ? ' $d.' : ''}';
  }
}

/// 제원 한 칸의 주석 — 원래 단위 표기, 짧은 단서, 출처 번호.
class SpecNote {
  const SpecNote({this.orig, this.noteKo, this.noteEn, this.src = const []});

  /// 출처에 적힌 원래 단위의 값("42 in", "140 psi"). 출처가 처음부터 미터법이면 null.
  final String? orig;
  final String? noteKo;
  final String? noteEn;
  final List<int> src;

  String? note(Lang lang) =>
      lang == Lang.en && (noteEn?.isNotEmpty ?? false) ? noteEn : noteKo;

  factory SpecNote.fromJson(Map<String, dynamic> j) => SpecNote(
        orig: j['orig'] as String?,
        noteKo: j['noteKo'] as String?,
        noteEn: j['noteEn'] as String?,
        src: _ints(j['src']),
      );
}

/// 항목 글에 번호로 단 출처 한 건.
class SourceRef {
  const SourceRef({
    required this.n,
    required this.ko,
    required this.en,
    this.kind,
    this.tier,
    this.lang,
    this.url,
  });

  final int n;

  /// 출처 표기(한국어 / 영어).
  final String ko;
  final String en;

  /// book | journal | newspaper | web | museum … (원고 그대로)
  final String? kind;

  /// primary | secondary | encyclopedia | enthusiast
  final String? tier;
  final String? lang;
  final String? url;

  String of(Lang lang) => lang == Lang.en && en.isNotEmpty ? en : ko;

  factory SourceRef.fromJson(Map<String, dynamic> j) => SourceRef(
        n: (j['n'] as num).toInt(),
        ko: j['ko'] as String? ?? '',
        en: j['en'] as String? ?? '',
        kind: j['kind'] as String?,
        tier: j['tier'] as String?,
        lang: j['lang'] as String?,
        url: j['url'] as String?,
      );
}

/// 보존/운행 상태.
enum LocoStatus {
  operational, // 운행 (본선·관광열차 견인)
  operable, // 동태 보존 (움직일 수 있음)
  static_, // 정태 보존 (전시)
  restoration, // 복원 중
  scrapped, // 남은 차량 없음
  replica; // 복제품만 남음

  static LocoStatus parse(String? raw) => switch (raw) {
        'operational' => LocoStatus.operational,
        'operable' => LocoStatus.operable,
        'restoration' => LocoStatus.restoration,
        'scrapped' => LocoStatus.scrapped,
        'replica' => LocoStatus.replica,
        _ => LocoStatus.static_,
      };

  String get labelKo => switch (this) {
        LocoStatus.operational => '운행',
        LocoStatus.operable => '동태 보존',
        LocoStatus.static_ => '정태 보존',
        LocoStatus.restoration => '복원 중',
        LocoStatus.scrapped => '해체',
        LocoStatus.replica => '복제품',
      };

  String get labelEn => switch (this) {
        LocoStatus.operational => 'Operational',
        LocoStatus.operable => 'Operable',
        LocoStatus.static_ => 'Static display',
        LocoStatus.restoration => 'Under restoration',
        LocoStatus.scrapped => 'Scrapped',
        LocoStatus.replica => 'Replica',
      };

  String label(Lang lang) => lang == Lang.en ? labelEn : labelKo;

  /// 실제로 증기를 올릴 수 있는 상태인가.
  bool get isAlive => this == LocoStatus.operational || this == LocoStatus.operable;
}

/// 용도 분류.
enum ServiceType {
  express, // 급행 여객
  passenger, // 여객
  mixed, // 객화 겸용
  freight, // 화물
  tank, // 탱크식·입환
  articulated, // 관절식
  narrow, // 협궤
  rack; // 치차(등판)

  static ServiceType parse(String? raw) => switch (raw) {
        'express' => ServiceType.express,
        'passenger' => ServiceType.passenger,
        'freight' => ServiceType.freight,
        'tank' => ServiceType.tank,
        'articulated' => ServiceType.articulated,
        'narrow' => ServiceType.narrow,
        'rack' => ServiceType.rack,
        _ => ServiceType.mixed,
      };

  String get labelKo => switch (this) {
        ServiceType.express => '급행 여객',
        ServiceType.passenger => '여객',
        ServiceType.mixed => '객화 겸용',
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
/// 도색의 색상 계열 — 탐색 필터 칩용.
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

/// 2색 도색에서 둘째 색이 칠해지는 부위.
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
  final String nameEn;
  final ChimneyStyle chimney;
  final CabStyle cab;
  final int domes; // 보일러 위 증기돔·모래돔 수 (0~2)
  final CasingStyle casing;
  final bool lamp; // 앞 전조등
  final bool pilot; // 카우캐처(배장기)
  final CylinderStyle cylinder;

  /// 생김새 설명(한국어 / 영어). 필터의 도움말과 도식 아래 설명에 쓴다.
  final String note;
  final String noteEn;

  const LocoShape({
    required this.id,
    required this.nameKo,
    this.nameEn = '',
    required this.chimney,
    required this.cab,
    required this.domes,
    required this.casing,
    required this.lamp,
    required this.pilot,
    required this.cylinder,
    required this.note,
    this.noteEn = '',
  });

  /// 데이터가 없을 때 쓰는 기본형 — 예전 도식과 같은 모습.
  static const fallback = LocoShape(
    id: 'classic',
    nameKo: '표준형',
    nameEn: 'Standard type',
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
        nameEn: j['nameEn'] as String? ?? '',
        chimney: ChimneyStyle.parse(j['chimney'] as String?),
        cab: CabStyle.parse(j['cab'] as String?),
        domes: _i(j['domes']) ?? 0,
        casing: CasingStyle.parse(j['casing'] as String?),
        lamp: j['lamp'] as bool? ?? false,
        pilot: j['pilot'] as bool? ?? false,
        cylinder: CylinderStyle.parse(j['cylinder'] as String?),
        note: (j['noteKo'] ?? j['note']) as String? ?? '',
        noteEn: j['noteEn'] as String? ?? '',
      );

  bool get isStreamlined => casing == CasingStyle.full;
}

/// 중량이 무엇을 잰 것인지. 기관차만 잰 중량과 탄수차까지 합친 운전정비중량은
/// 두 배 가까이 차이가 나므로 숫자만 보여주면 비교가 틀어진다.
enum WeightBasis {
  loco('기관차만', 'Locomotive only'),
  locoAndTender('탄수차 포함', 'With tender');

  const WeightBasis(this.labelKo, this.labelEn);
  final String labelKo;
  final String labelEn;

  String label(Lang lang) => lang == Lang.en ? labelEn : labelKo;

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

/// 제원. 값이 없는 항목은 null — 화면에서는 줄을 빼거나 '자료 없음'으로 표시한다.
///
/// 원고의 기준: 1차 자료 없이 두 자료가 정면으로 엇갈리는 값은 비운다.
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

  /// 설계·허용 최고 속도만. 시험이나 운행 중에 낸 기록은 [recordSpeedKmh] 에 따로 둔다.
  final double? topSpeedKmh;

  /// 시험·운행 중 기록 속도(맬러드 201.2 km/h 등). 최고속도와 섞지 않는다.
  final double? recordSpeedKmh;
  final int? leadingWheelDiameterMm;
  final int? trailingWheelDiameterMm;

  /// 실린더 지름 × 행정(mm) 표기. 예: "356 × 559"
  final String? cylinderSize;
  final int? wheelbaseMm;
  final int? waterL;

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
    this.recordSpeedKmh,
    this.leadingWheelDiameterMm,
    this.trailingWheelDiameterMm,
    this.cylinderSize,
    this.wheelbaseMm,
    this.waterL,
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
        recordSpeedKmh: _d(j['recordSpeedKmh']),
        leadingWheelDiameterMm: _i(j['leadingWheelDiameterMm']),
        trailingWheelDiameterMm: _i(j['trailingWheelDiameterMm']),
        cylinderSize: j['cylinderSize'] as String?,
        wheelbaseMm: _i(j['wheelbaseMm']),
        waterL: _i(j['waterL']),
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

/// 지금 있는 곳. 장소명과 단서는 한영 짝이고, 좌표가 없는 곳('러시아 각지')도 있다.
class LocoLocation {
  /// 장소명(한국어). 지도 마커 라벨과 지도 앱 라벨에 쓴다.
  final String name;
  final String nameEn;

  /// 단서 — 어느 차량이 어떤 상태로 있는지("C57 1 소속. 2026년 10월 3일부터 …").
  final String? note;
  final String? noteEn;

  /// 좌표. 특정 장소가 없으면 둘 다 null 이고 지도에 찍지 않는다.
  final double? lat;
  final double? lon;

  /// 지도 앱에 넘길 검색어 — 그 지도 앱이 알아듣는 시설의 공식 명칭(예: "National Railway Museum York").
  /// 있으면 지도 앱이 실제 장소(주소·사진 포함)를 찾아 보여주고, 없으면 좌표 핀에 [name] 라벨만 붙인다.
  final String? query;

  /// 이 칸의 출처 번호([Locomotive.sources]).
  final List<int> src;

  const LocoLocation({
    required this.name,
    this.nameEn = '',
    this.note,
    this.noteEn,
    this.lat,
    this.lon,
    this.query,
    this.src = const [],
  });

  bool get hasPoint => lat != null && lon != null;

  String nameOf(Lang lang) => lang == Lang.en && nameEn.isNotEmpty ? nameEn : name;
  String? noteOf(Lang lang) =>
      lang == Lang.en && (noteEn?.isNotEmpty ?? false) ? noteEn : note;

  factory LocoLocation.fromJson(Map<String, dynamic> j) => LocoLocation(
        name: (j['nameKo'] ?? j['name']) as String,
        nameEn: j['nameEn'] as String? ?? '',
        note: j['noteKo'] as String?,
        noteEn: j['noteEn'] as String?,
        lat: _d(j['lat']),
        lon: _d(j['lon']),
        query: j['query'] as String?,
        src: _ints(j['src']),
      );
}

class Locomotive {
  final String id;
  final String nameKo;
  final String nameEn;

  /// 별명·애칭(데고이치, 티거리, 아름다운 헬레나…). 공인 형식명이 아니므로
  /// [nameKo]/[nameEn] 에는 넣지 않고 여기에만 둔다.
  final String? nicknameKo;
  final String? nicknameEn;

  /// 형식 기호. 출처로 뒷받침되는 기호가 없으면 null(라 트로치타).
  final String? classDesignation;

  /// 대표 차량 번호. 항목이 한 량을 가리킬 때만 있다("C57 1", "4014").
  final String? roadNumber;
  final String countryCode;
  final String eraId;
  final List<String> operators;
  final List<String> builders;
  final String? designer;
  final int? builtFrom;
  final int? builtTo;
  final int? quantityBuilt;

  /// 자료마다 수량이 달라 숫자 하나로 쓸 수 없을 때의 표기("7,000량 이상"). 있으면 표제란에 이것을 쓴다.
  final SourcedText? quantityNote;
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

  /// 제원이 어느 시점·차량 기준인지("1897년 출고 당시").
  final Bilingual? specsBasis;

  /// 제원 칸별 주석(원래 단위·단서·출처 번호). 키는 제원 칸 이름이고, 순서가 곧 화면 순서다.
  /// 궤간은 `gaugeMm` 키로 들어 있다.
  final Map<String, SpecNote> specNotes;
  final LocoStatus status;
  final int? survivors;
  final LocoLocation? location;
  final bool iconic;

  /// 뜻풀이 — 명사로 끝나는 한 줄.
  final SourcedText gloss;

  /// 본문 — '~다' 문장들. 문장마다 출처 번호가 있다.
  final List<SourcedText> body;

  /// 연혁 — 날짜순.
  final List<HistoryEvent> history;
  final List<String> tags;
  final List<String> tagsEn;

  /// 항목 글에 번호로 단 출처. [SourcedText.src] 등의 번호가 [SourceRef.n] 을 가리킨다.
  final List<SourceRef> sources;

  /// 더 읽을거리 — 이 형식·개체를 다룬 책·논문·공식 자료.
  final List<Reference> furtherReading;
  final bool verified;

  const Locomotive({
    required this.id,
    required this.nameKo,
    required this.nameEn,
    this.nicknameKo,
    this.nicknameEn,
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
    this.quantityNote,
    required this.withdrawnYear,
    required this.wheel,
    required this.tenderAxles,
    required this.liveryId,
    required this.shapeId,
    required this.gaugeMm,
    required this.serviceType,
    required this.specs,
    this.specsBasis,
    this.specNotes = const {},
    required this.status,
    required this.survivors,
    required this.location,
    required this.iconic,
    this.gloss = const SourcedText(ko: '', en: ''),
    this.body = const [],
    this.history = const [],
    required this.tags,
    this.tagsEn = const [],
    this.sources = const [],
    this.furtherReading = const [],
    required this.verified,
  });

  factory Locomotive.fromJson(Map<String, dynamic> j) => Locomotive(
        id: j['id'] as String,
        nameKo: j['nameKo'] as String,
        nameEn: j['nameEn'] as String,
        nicknameKo: j['nicknameKo'] as String?,
        nicknameEn: j['nicknameEn'] as String?,
        classDesignation: j['classDesignation'] as String?,
        roadNumber: j['roadNumber'] as String?,
        countryCode: j['countryCode'] as String,
        eraId: j['era'] as String,
        operators: _s(j['operators']),
        builders: _s(j['builders']),
        designer: j['designer'] as String?,
        builtFrom: _i(j['builtFrom']),
        builtTo: _i(j['builtTo']),
        quantityBuilt: _i(j['quantityBuilt']),
        quantityNote: SourcedText.maybe(j['quantityNote']),
        withdrawnYear: _i(j['withdrawnYear']),
        wheel: Wheel.fromJson(j['wheel'] as Map<String, dynamic>),
        tenderAxles: _i(j['tenderAxles']),
        liveryId: j['livery'] as String?,
        shapeId: j['shape'] as String?,
        gaugeMm: _i(j['gaugeMm']) ?? 1435,
        serviceType: ServiceType.parse(j['serviceType'] as String?),
        specs: LocoSpecs.fromJson(j['specs'] as Map<String, dynamic>),
        specsBasis: Bilingual.fromJson(j['specsBasis']),
        specNotes: {
          for (final e in ((j['specNotes'] as Map<String, dynamic>?) ?? const {}).entries)
            e.key: SpecNote.fromJson(e.value as Map<String, dynamic>),
        },
        status: LocoStatus.parse(j['status'] as String?),
        survivors: _i(j['survivors']),
        location: j['location'] == null
            ? null
            : LocoLocation.fromJson(j['location'] as Map<String, dynamic>),
        iconic: j['iconic'] as bool? ?? false,
        gloss: SourcedText.maybe(j['gloss']) ?? const SourcedText(ko: '', en: ''),
        body: SourcedText.listFrom(j['body']),
        history: ((j['history'] as List?) ?? const [])
            .map((e) => HistoryEvent.fromJson(e as Map<String, dynamic>))
            .toList(),
        tags: _s(j['tags']),
        tagsEn: _s(j['tagsEn']),
        sources: ((j['sources'] as List?) ?? const [])
            .map((e) => SourceRef.fromJson(e as Map<String, dynamic>))
            .toList(),
        furtherReading: Reference.listFrom(j['furtherReading']),
        verified: j['verified'] as bool? ?? false,
      );

  String nameOf(Lang lang) => lang == Lang.en ? nameEn : nameKo;
  String? nicknameOf(Lang lang) => lang == Lang.en ? nicknameEn : nicknameKo;

  /// 별명(한국어). 예전 이름을 쓰는 코드를 위한 별칭.
  String? get nickname => nicknameKo;

  /// 표제란의 수량. 수량 문구([quantityNote])가 있으면 그것을, 없으면 숫자를 쓴다.
  /// 숫자도 없으면 null.
  String? quantityLabel(Lang lang) {
    if (quantityNote != null) return quantityNote!.of(lang);
    final q = quantityBuilt;
    if (q == null) return null;
    final s = q.toString().replaceAllMapped(RegExp(r'\B(?=(\d{3})+(?!\d))'), (_) => ',');
    return lang == Lang.en ? s : '$s량';
  }

  /// 출처 번호 → 출처. 없는 번호면 null.
  SourceRef? source(int n) {
    for (final s in sources) {
      if (s.n == n) return s;
    }
    return null;
  }

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
        nicknameKo ?? '',
        nicknameEn ?? '',
        classDesignation ?? '',
        roadNumber ?? '',
        wheel.whyte,
        wheel.typeName ?? '',
        designer ?? '',
        ...operators,
        ...builders,
        ...tags,
        ...tagsEn,
      ].join(' ').toLowerCase();
}

/// 시대 구분.
class Era {
  final String id;
  final String nameKo;
  final String nameEn;
  final int from;
  final int to;

  /// 시대 설명(한국어 / 영어). 원고의 시대 설명이다.
  final String note;
  final String noteEn;

  const Era({
    required this.id,
    required this.nameKo,
    required this.nameEn,
    required this.from,
    required this.to,
    required this.note,
    this.noteEn = '',
  });

  factory Era.fromJson(Map<String, dynamic> j) => Era(
        id: j['id'] as String,
        nameKo: j['ko'] as String,
        nameEn: j['en'] as String,
        from: (j['from'] as num).toInt(),
        to: (j['to'] as num).toInt(),
        note: (j['noteKo'] ?? j['note']) as String? ?? '',
        noteEn: j['noteEn'] as String? ?? '',
      );

  String get rangeLabel => to >= 2100 ? '$from~현재' : '$from–$to';
}

/// 참고문헌 — 서적·논문·공식 간행물. 항목 글의 번호 붙은 출처([SourceRef])와 구분한다.
///
/// 기관차별 '더 읽을거리'는 자료조사 원고에서, 나라별·종합 문헌은 `tools/references.py` 에서 온다.
/// [via] 는 서지를 어디서 확인했는지(원고가 새로 찾은 문헌은 비어 있다), [note] 는 무엇을 다루는지.
class Reference {
  final String kind; // book | article | journal | thesis | official | catalog | report | web
  final String title;
  final String author;
  final String publisher;
  final int? year;
  final String lang;
  final String? isbn;
  final String? url;

  /// 메모(한국어 / 영어).
  final String note;
  final String noteEn;
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
    this.noteEn = '',
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
        note: (j['noteKo'] ?? j['note']) as String? ?? '',
        noteEn: j['noteEn'] as String? ?? '',
        via: j['via'] as String? ?? '',
      );

  String noteOf(Lang lang) => lang == Lang.en && noteEn.isNotEmpty ? noteEn : note;

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
        'journal' => '학술지 논문',
        'thesis' => '학위논문',
        'official' => '공식 자료',
        'catalog' => '소장품 기록',
        'report' => '보고서',
        'web' => '웹 문서',
        _ => '단행본',
      };

  /// "저자, 『제목』, 출판사, 연도" 꼴의 한 줄 인용. 연도를 모르면 적지 않는다.
  String get citation {
    final parts = <String>[
      if (author.isNotEmpty) author,
      '『$title』',
      if (publisher.isNotEmpty) publisher,
      if (year != null) '$year',
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

  /// 나라 설명(한국어 / 영어). 원고의 나라 설명이다.
  final String blurb;
  final String blurbEn;

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
    this.blurbEn = '',
    this.references = const [],
  });

  factory Country.fromJson(Map<String, dynamic> j) => Country(
        code: j['code'] as String,
        nameKo: j['nameKo'] as String,
        nameEn: j['nameEn'] as String,
        flag: j['flag'] as String,
        lat: (j['lat'] as num).toDouble(),
        lon: (j['lon'] as num).toDouble(),
        blurb: (j['blurbKo'] ?? j['blurb']) as String? ?? '',
        blurbEn: j['blurbEn'] as String? ?? '',
        references: Reference.listFrom(j['references']),
      );
}
