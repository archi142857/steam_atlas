import 'locomotive.dart';

/// 정렬 기준.
enum SortBy {
  year, // 제작연도
  speed, // 최고속도
  power, // 견인력
  weight, // 중량
  name; // 이름(가나다)

  String get labelKo => switch (this) {
        SortBy.year => '제작연도',
        SortBy.speed => '최고속도',
        SortBy.power => '견인력',
        SortBy.weight => '중량',
        SortBy.name => '이름',
      };
}

/// 검색·필터 상태를 하나의 불변 값으로 들고 다닌다.
///
/// 화면(탐색 / 연표 / 지도)이 모두 같은 타입을 쓰기 때문에
/// "국가 탭에서 필터를 걸어둔 채 지도로 넘어가기" 같은 흐름이 자연스럽게 된다.
class FilterQuery {
  final String text;
  final Set<String> countries;
  final Set<String> eras;
  final Set<ServiceType> serviceTypes;
  final Set<LocoStatus> statuses;
  final Set<int> gauges;

  /// 도색 색상 계열 / 생김새(실루엣) — v0.12. 둘 다 카탈로그 값이라 id 로 든다.
  final Set<LiveryFamily> liveryFamilies;
  final Set<String> shapes;
  final bool iconicOnly;
  final bool aliveOnly; // 지금 움직일 수 있는 것만
  final RangeYear? builtRange;
  final SortBy sortBy;
  final bool descending;

  const FilterQuery({
    this.text = '',
    this.countries = const {},
    this.eras = const {},
    this.serviceTypes = const {},
    this.statuses = const {},
    this.gauges = const {},
    this.liveryFamilies = const {},
    this.shapes = const {},
    this.iconicOnly = false,
    this.aliveOnly = false,
    this.builtRange,
    this.sortBy = SortBy.year,
    this.descending = false,
  });

  bool get isEmpty =>
      text.isEmpty &&
      countries.isEmpty &&
      eras.isEmpty &&
      serviceTypes.isEmpty &&
      statuses.isEmpty &&
      gauges.isEmpty &&
      liveryFamilies.isEmpty &&
      shapes.isEmpty &&
      !iconicOnly &&
      !aliveOnly &&
      builtRange == null;

  /// 활성화된 필터 개수 — 뱃지 표시용.
  int get activeCount =>
      (text.isNotEmpty ? 1 : 0) +
      countries.length +
      eras.length +
      serviceTypes.length +
      statuses.length +
      gauges.length +
      liveryFamilies.length +
      shapes.length +
      (iconicOnly ? 1 : 0) +
      (aliveOnly ? 1 : 0) +
      (builtRange != null ? 1 : 0);

  FilterQuery copyWith({
    String? text,
    Set<String>? countries,
    Set<String>? eras,
    Set<ServiceType>? serviceTypes,
    Set<LocoStatus>? statuses,
    Set<int>? gauges,
    Set<LiveryFamily>? liveryFamilies,
    Set<String>? shapes,
    bool? iconicOnly,
    bool? aliveOnly,
    RangeYear? builtRange,
    bool clearBuiltRange = false,
    SortBy? sortBy,
    bool? descending,
  }) {
    return FilterQuery(
      text: text ?? this.text,
      countries: countries ?? this.countries,
      eras: eras ?? this.eras,
      serviceTypes: serviceTypes ?? this.serviceTypes,
      statuses: statuses ?? this.statuses,
      gauges: gauges ?? this.gauges,
      liveryFamilies: liveryFamilies ?? this.liveryFamilies,
      shapes: shapes ?? this.shapes,
      iconicOnly: iconicOnly ?? this.iconicOnly,
      aliveOnly: aliveOnly ?? this.aliveOnly,
      builtRange: clearBuiltRange ? null : (builtRange ?? this.builtRange),
      sortBy: sortBy ?? this.sortBy,
      descending: descending ?? this.descending,
    );
  }

  /// 집합형 필터를 토글하는 헬퍼.
  static Set<T> toggled<T>(Set<T> src, T value) {
    final next = Set<T>.from(src);
    if (!next.remove(value)) next.add(value);
    return next;
  }
}

class RangeYear {
  final int from;
  final int to;
  const RangeYear(this.from, this.to);
  bool contains(int? y) => y != null && y >= from && y <= to;
}
