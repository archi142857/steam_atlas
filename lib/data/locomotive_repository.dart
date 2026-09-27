import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../core/hangul.dart';
import '../models/filter_query.dart';
import '../models/locomotive.dart';

/// 데이터 접근 계층.
///
/// 지금은 앱에 번들된 JSON을 읽지만, 나중에 원격 API나 로컬 DB로 바꿀 때
/// 이 클래스의 [load] 구현만 교체하면 화면 코드는 손대지 않아도 된다.
abstract class LocomotiveSource {
  Future<LocomotiveDataset> load();
}

class AssetLocomotiveSource implements LocomotiveSource {
  const AssetLocomotiveSource();

  @override
  Future<LocomotiveDataset> load() async {
    final locoRaw = await rootBundle.loadString('assets/data/locomotives.json');
    final countryRaw = await rootBundle.loadString('assets/data/countries.json');

    final locoJson = jsonDecode(locoRaw) as Map<String, dynamic>;
    final countryJson = jsonDecode(countryRaw) as Map<String, dynamic>;

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
      generalReferences: Reference.listFrom(locoJson['references']),
      countries: (countryJson['countries'] as List)
          .map((e) => Country.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}

class LocomotiveDataset {
  final List<Locomotive> locomotives;
  final List<Era> eras;
  final List<Country> countries;
  final List<Livery> liveries;
  final List<LocoShape> shapes;

  /// 여러 나라에 걸친 종합 문헌(Chapelon, Durrant 등).
  final List<Reference> generalReferences;

  const LocomotiveDataset({
    required this.locomotives,
    required this.eras,
    required this.countries,
    this.liveries = const [],
    this.shapes = const [],
    this.generalReferences = const [],
  });
}

/// 로드된 데이터 위에서 검색·필터·집계를 수행한다.
class LocomotiveRepository {
  LocomotiveRepository(this._data)
      : _searchIndex = {
          // 자모 합치기·소문자·공백 제거까지 끝낸 키로 인덱싱한다 (core/hangul.dart)
          for (final l in _data.locomotives) l.id: searchKey(l.searchIndex),
        },
        _choseongIndex = {
          for (final l in _data.locomotives) l.id: initials(l.searchIndex),
        },
        _countryByCode = {for (final c in _data.countries) c.code: c},
        _eraById = {for (final e in _data.eras) e.id: e},
        _liveryById = {for (final l in _data.liveries) l.id: l},
        _shapeById = {for (final s in _data.shapes) s.id: s};

  final LocomotiveDataset _data;
  final Map<String, String> _searchIndex;

  /// 초성 검색용("ㅁㄹㄷ" → 맬러드). 한글 음절만 초성으로 바꾼 인덱스.
  final Map<String, String> _choseongIndex;
  final Map<String, Country> _countryByCode;
  final Map<String, Era> _eraById;
  final Map<String, Livery> _liveryById;
  final Map<String, LocoShape> _shapeById;

  List<Locomotive> get all => List.unmodifiable(_data.locomotives);
  List<Country> get countries => List.unmodifiable(_data.countries);
  List<Era> get eras => List.unmodifiable(_data.eras);
  List<Livery> get liveries => List.unmodifiable(_data.liveries);
  List<LocoShape> get shapes => List.unmodifiable(_data.shapes);
  List<Reference> get generalReferences => List.unmodifiable(_data.generalReferences);

  Country? country(String code) => _countryByCode[code];
  Era? era(String id) => _eraById[id];

  /// 도색 팔레트 조회. 데이터에 없거나 id가 비면 null → 화면은 무채색으로 그린다.
  Livery? livery(String? id) => id == null ? null : _liveryById[id];
  Livery? liveryOf(Locomotive l) => livery(l.liveryId);

  /// 실루엣 유형 조회. 없으면 기본형([LocoShape.fallback])으로 그린다.
  LocoShape? shape(String? id) => id == null ? null : _shapeById[id];
  LocoShape shapeOf(Locomotive l) => shape(l.shapeId) ?? LocoShape.fallback;
  Locomotive? byId(String id) =>
      _data.locomotives.where((l) => l.id == id).firstOrNull;

  /// 데이터에 실제로 등장하는 궤간 목록(오름차순). 필터 UI에서 사용.
  List<int> get availableGauges =>
      _data.locomotives.map((l) => l.gaugeMm).toSet().toList()..sort();

  /// 데이터에 실제로 쓰인 도색 계열(enum 순서). 필터 UI에서 사용.
  List<LiveryFamily> get availableLiveryFamilies {
    final used = {for (final l in _data.locomotives) liveryOf(l)?.family};
    return [for (final f in LiveryFamily.values) if (used.contains(f)) f];
  }

  /// 데이터에 실제로 쓰인 생김새(카탈로그 순서 = 대체로 시대순). 필터 UI에서 사용.
  List<LocoShape> get availableShapes {
    final used = {for (final l in _data.locomotives) shapeOf(l).id};
    return [for (final s in _data.shapes) if (used.contains(s.id)) s];
  }

  /// 계열/생김새별 량 수 — 칩 옆 숫자용.
  int countLiveryFamily(LiveryFamily f) =>
      _data.locomotives.where((l) => liveryOf(l)?.family == f).length;
  int countShape(String shapeId) =>
      _data.locomotives.where((l) => shapeOf(l).id == shapeId).length;

  int countFor(String countryCode) =>
      _data.locomotives.where((l) => l.countryCode == countryCode).length;

  /// 핵심 질의. [FilterQuery] 하나로 모든 화면이 같은 규칙을 공유한다.
  List<Locomotive> query(FilterQuery q) {
    // 검색어도 인덱스와 같은 규칙으로 정규화한다. 초성만 친 경우("ㅁㄹㄷ")는 초성 인덱스로.
    final raw = q.text;
    final cho = isChoseongQuery(raw);
    final needle = cho ? initials(raw) : searchKey(raw);
    final index = cho ? _choseongIndex : _searchIndex;
    final result = _data.locomotives.where((l) {
      if (needle.isNotEmpty && !(index[l.id] ?? '').contains(needle)) {
        return false;
      }
      if (q.countries.isNotEmpty && !q.countries.contains(l.countryCode)) {
        return false;
      }
      if (q.eras.isNotEmpty && !q.eras.contains(l.eraId)) return false;
      if (q.serviceTypes.isNotEmpty && !q.serviceTypes.contains(l.serviceType)) {
        return false;
      }
      if (q.statuses.isNotEmpty && !q.statuses.contains(l.status)) return false;
      if (q.gauges.isNotEmpty && !q.gauges.contains(l.gaugeMm)) return false;
      // 도색 계열은 도색 카탈로그를 거쳐 본다 — 도색이 없거나 계열이 없는 량은 어떤 계열에도 안 걸린다.
      if (q.liveryFamilies.isNotEmpty &&
          !q.liveryFamilies.contains(liveryOf(l)?.family)) {
        return false;
      }
      if (q.shapes.isNotEmpty && !q.shapes.contains(shapeOf(l).id)) return false;
      if (q.iconicOnly && !l.iconic) return false;
      if (q.aliveOnly && !l.status.isAlive) return false;
      if (q.builtRange != null && !q.builtRange!.contains(l.builtFrom)) {
        return false;
      }
      return true;
    }).toList();

    // 내림차순은 목록을 통째로 뒤집지 않는다 — 그러면 값이 없는 항목(—)이 맨 위로 올라온다.
    // 값이 있는 것끼리만 방향을 바꾸고, 값이 없는 항목은 어느 방향이든 맨 뒤.
    final dir = q.descending ? -1 : 1;
    result.sort((a, b) => _compare(a, b, q.sortBy, dir));
    return result;
  }

  int _compare(Locomotive a, Locomotive b, SortBy by, int dir) {
    int cmpNullable(num? x, num? y) {
      if (x == null && y == null) return a.nameKo.compareTo(b.nameKo);
      if (x == null) return 1;
      if (y == null) return -1;
      return dir * x.compareTo(y);
    }

    return switch (by) {
      SortBy.year => cmpNullable(a.builtFrom ?? a.builtTo, b.builtFrom ?? b.builtTo),
      SortBy.speed => cmpNullable(a.specs.topSpeedKmh, b.specs.topSpeedKmh),
      SortBy.power =>
        cmpNullable(a.specs.tractiveEffortKn, b.specs.tractiveEffortKn),
      SortBy.weight => cmpNullable(a.specs.weightT, b.specs.weightT),
      SortBy.name => dir * a.nameKo.compareTo(b.nameKo),
    };
  }

  /// 지도에 찍을 수 있는 항목만.
  List<Locomotive> withLocation(FilterQuery q) =>
      query(q).where((l) => l.location != null).toList();

  /// 연표용: 시대 → 해당 기관차 목록(연도순).
  Map<Era, List<Locomotive>> groupedByEra(FilterQuery q) {
    final items = query(q.copyWith(sortBy: SortBy.year, descending: false));
    final map = <Era, List<Locomotive>>{};
    for (final e in _data.eras) {
      final list = items.where((l) => l.eraId == e.id).toList();
      if (list.isNotEmpty) map[e] = list;
    }
    return map;
  }

  /// 홈 화면 통계.
  ({int total, int countries, int alive, int scrapped, int verified}) get stats {
    final all = _data.locomotives;
    return (
      total: all.length,
      countries: all.map((l) => l.countryCode).toSet().length,
      alive: all.where((l) => l.status.isAlive).length,
      scrapped: all.where((l) => l.status == LocoStatus.scrapped).length,
      verified: all.where((l) => l.verified).length,
    );
  }
}

extension _FirstOrNull<T> on Iterable<T> {
  T? get firstOrNull => isEmpty ? null : first;
}
