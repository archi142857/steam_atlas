import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart' show ThemeMode;
import 'package:shared_preferences/shared_preferences.dart';

import '../data/locomotive_repository.dart';
import '../models/filter_query.dart';
import '../models/locomotive.dart';

/// 앱 전역 상태.
///
/// - 데이터 로딩 라이프사이클
/// - 화면들이 공유하는 [FilterQuery]
/// - 테마 모드, 즐겨찾기 (shared_preferences 로 영속화)
class AppState extends ChangeNotifier {
  AppState({LocomotiveSource? source})
      : _source = source ?? const AssetLocomotiveSource();

  static const _kTheme = 'themeMode';
  static const _kFavorites = 'favorites';
  static const _kOnlineTiles = 'onlineTiles';

  final LocomotiveSource _source;
  SharedPreferences? _prefs;

  LocomotiveRepository? _repo;
  Object? _error;
  bool _loading = false;

  LocomotiveRepository? get repo => _repo;
  Object? get error => _error;
  bool get isLoading => _loading;
  bool get isReady => _repo != null;

  FilterQuery _query = const FilterQuery();
  FilterQuery get query => _query;

  /// 기본은 라이트 — 레이아웃을 라이트 기준으로 잡았다.
  ThemeMode _themeMode = ThemeMode.light;
  ThemeMode get themeMode => _themeMode;

  /// 온라인 지도 타일 사용 여부.
  ///
  /// **기본은 꺼짐.** 켜면 지도가 도로·지명까지 보이지만 네트워크를 쓰고,
  /// 타일 제공자의 사용 정책을 따라야 한다. 공개 OSM 타일은 앱 프로덕션
  /// 트래픽용이 아니므로, 출시 전에 반드시 자체/상용 타일 URL로 바꿀 것.
  /// (RELEASE.md '지도 타일' 항목 참조)
  bool _onlineTiles = false;
  bool get onlineTiles => _onlineTiles;

  final Set<String> _favorites = <String>{};
  Set<String> get favorites => Set.unmodifiable(_favorites);

  Future<void> init() async {
    if (_loading || _repo != null) return;
    _loading = true;
    _error = null;
    notifyListeners();

    // 설정 복원은 실패해도 앱은 떠야 한다 — 데이터 로딩과 분리해서 감싼다.
    try {
      _prefs = await SharedPreferences.getInstance();
      _themeMode = _parseTheme(_prefs!.getString(_kTheme));
      _favorites.addAll(_prefs!.getStringList(_kFavorites) ?? const []);
      _onlineTiles = _prefs!.getBool(_kOnlineTiles) ?? false;
    } catch (e) {
      debugPrint('설정을 불러오지 못했습니다 (기본값 사용): $e');
    }

    try {
      _repo = LocomotiveRepository(await _source.load());
    } catch (e) {
      _error = e;
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  static ThemeMode _parseTheme(String? raw) => switch (raw) {
        'dark' => ThemeMode.dark,
        'system' => ThemeMode.system,
        _ => ThemeMode.light,
      };

  static String _themeName(ThemeMode m) => switch (m) {
        ThemeMode.light => 'light',
        ThemeMode.system => 'system',
        ThemeMode.dark => 'dark',
      };

  // ── 테마 ────────────────────────────────────────────────
  void setThemeMode(ThemeMode mode) {
    if (_themeMode == mode) return;
    _themeMode = mode;
    notifyListeners();
    _prefs?.setString(_kTheme, _themeName(mode));
  }

  void setOnlineTiles(bool value) {
    if (_onlineTiles == value) return;
    _onlineTiles = value;
    notifyListeners();
    _prefs?.setBool(_kOnlineTiles, value);
  }

  // ── 필터 조작 ────────────────────────────────────────────
  void setQuery(FilterQuery q) {
    _query = q;
    notifyListeners();
  }

  void setText(String text) => setQuery(_query.copyWith(text: text));

  void toggleCountry(String code) => setQuery(
        _query.copyWith(countries: FilterQuery.toggled(_query.countries, code)),
      );

  void toggleEra(String id) =>
      setQuery(_query.copyWith(eras: FilterQuery.toggled(_query.eras, id)));

  void toggleService(ServiceType t) => setQuery(
        _query.copyWith(
            serviceTypes: FilterQuery.toggled(_query.serviceTypes, t)),
      );

  void toggleStatus(LocoStatus s) => setQuery(
        _query.copyWith(statuses: FilterQuery.toggled(_query.statuses, s)),
      );

  void toggleGauge(int mm) =>
      setQuery(_query.copyWith(gauges: FilterQuery.toggled(_query.gauges, mm)));

  void toggleLiveryFamily(LiveryFamily f) => setQuery(
        _query.copyWith(
            liveryFamilies: FilterQuery.toggled(_query.liveryFamilies, f)),
      );

  void toggleShape(String id) =>
      setQuery(_query.copyWith(shapes: FilterQuery.toggled(_query.shapes, id)));

  void setSort(SortBy by, {bool? descending}) =>
      setQuery(_query.copyWith(sortBy: by, descending: descending));

  /// 필터만 지운다. 정렬 기준·방향은 그대로 (프리뷰와 같은 동작).
  void clearFilters() =>
      setQuery(FilterQuery(sortBy: _query.sortBy, descending: _query.descending));

  // ── 비교 ─────────────────────────────────────────────────
  // 두 량을 나란히 놓고 제원을 대조한다. 세션 동안만 유지(저장하지 않는다).
  final List<String> _compare = <String>[];
  List<String> get compareIds => List.unmodifiable(_compare);
  bool isCompared(String id) => _compare.contains(id);

  /// 비교 목록 토글. 최대 2량 — 셋째를 넣으면 가장 먼저 넣은 것이 빠진다. 반환: 넣었으면 true, 뺐으면 false.
  bool toggleCompare(String id) {
    if (_compare.remove(id)) {
      notifyListeners();
      return false;
    }
    if (_compare.length >= 2) _compare.removeAt(0);
    _compare.add(id);
    notifyListeners();
    return true;
  }

  void clearCompare() {
    if (_compare.isEmpty) return;
    _compare.clear();
    notifyListeners();
  }

  List<Locomotive> get compareLocos => _repo == null
      ? const []
      : [for (final id in _compare) if (_repo!.byId(id) case final l?) l];

  // ── 즐겨찾기 ─────────────────────────────────────────────
  bool isFavorite(String id) => _favorites.contains(id);

  void toggleFavorite(String id) {
    if (!_favorites.remove(id)) _favorites.add(id);
    notifyListeners();
    _saveFavorites();
  }

  void clearFavorites() {
    if (_favorites.isEmpty) return;
    _favorites.clear();
    notifyListeners();
    _saveFavorites();
  }

  void _saveFavorites() => _prefs?.setStringList(_kFavorites, _favorites.toList());

  List<Locomotive> get favoriteLocos => _repo == null
      ? const []
      : _repo!.all.where((l) => _favorites.contains(l.id)).toList();

  // ── 조회 헬퍼 ────────────────────────────────────────────
  List<Locomotive> get results => _repo?.query(_query) ?? const [];

  /// 기관차의 도색. 데이터가 아직 안 실렸거나 도색이 없으면 null →
  /// 화면은 무채색 도식으로 그린다.
  Livery? liveryOf(Locomotive l) => _repo?.liveryOf(l);

  /// 기관차의 실루엣 유형. 데이터가 아직 없으면 기본형.
  LocoShape shapeOf(Locomotive l) => _repo?.shapeOf(l) ?? LocoShape.fallback;
}
