import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

import '../core/format.dart';
import '../core/place_maps.dart';
import '../data/locomotive_repository.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import '../widgets/country_flag.dart';
import '../widgets/whyte_diagram.dart';
import 'compare_screen.dart';

/// 항목 화면 — 사전 한 장.
///
/// 순서는 디자인 확정안(S-entry)을 따른다:
/// 그림 → 표제란(형식, 차륜 배치 / 제작, 수량, 보존 상태) → 뜻풀이 → 본문 → 제원 → 연혁 → 지금 있는 곳
/// → 출처 → 더 읽을거리.
///
/// 글은 자료조사 원고(tools/manuscript/entries.json)에서 온다. 문장·제원·연혁 끝의 작은 숫자는 아래
/// '출처' 목록의 번호다. 색과 글꼴은 지금 테마를 따른다 — 확정안의 글꼴·색은 디자인 시스템을 옮길 때 바꾼다.
class DetailScreen extends StatelessWidget {
  const DetailScreen({super.key, required this.locoId});

  final String locoId;

  static Future<void> push(BuildContext context, String id) {
    return Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => DetailScreen(locoId: id)),
    );
  }

  /// 비교 목록에 넣고 빼기. 2량이 차면 스낵바에서 바로 비교 화면으로 갈 수 있다.
  void _toggleCompare(BuildContext context, AppState app, Locomotive l) {
    final added = app.toggleCompare(l.id);
    final n = app.compareIds.length;
    final messenger = ScaffoldMessenger.of(context)..hideCurrentSnackBar();
    messenger.showSnackBar(
      SnackBar(
        content: Text(added ? '비교에 넣었어요 ($n/2)' : '비교에서 뺐어요 ($n/2)'),
        duration: const Duration(seconds: 3),
        action: n == 2
            ? SnackBarAction(label: '나란히 보기', onPressed: () => CompareScreen.push(context))
            : null,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final repo = app.repo!;
    final l = repo.byId(locoId);
    if (l == null) {
      return const Scaffold(body: Center(child: Text('항목을 찾지 못했어요')));
    }
    final scheme = Theme.of(context).colorScheme;
    final lang = app.lang;
    final country = repo.country(l.countryCode);
    final livery = repo.liveryOf(l);
    final shape = repo.shapeOf(l);
    final compared = app.isCompared(l.id);

    return Scaffold(
      appBar: AppBar(
        actions: [
          // 비교: 최대 2량. 셋째를 넣으면 먼저 넣은 것이 빠진다 (AppState.toggleCompare).
          TextButton(
            onPressed: () => _toggleCompare(context, app, l),
            child: Text(
              compared ? '비교 중 ${app.compareIds.length}/2' : '비교',
              style: TextStyle(
                fontWeight: compared ? FontWeight.w700 : FontWeight.w500,
                color: compared ? scheme.primary : scheme.onSurface,
              ),
            ),
          ),
          IconButton(
            tooltip: app.isFavorite(l.id) ? '저장 취소' : '저장',
            icon: Icon(app.isFavorite(l.id) ? Icons.bookmark_rounded : Icons.bookmark_border_rounded),
            color: app.isFavorite(l.id) ? scheme.primary : null,
            onPressed: () => app.toggleFavorite(l.id),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 48),
        children: [
          // ── 그림 ── 삽화가 붙기 전까지는 차륜 도식. 판은 테마와 무관하게 흰색(다크에서 도색이 묻히지 않게).
          DiagramPlate(
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
            radius: 4,
            alignment: Alignment.center,
            height: 64,
            child: WhyteDiagram(
              wheel: l.wheel,
              tenderAxles: l.effectiveTenderAxles,
              height: 64,
              color: scheme.primary,
              livery: livery,
              shape: shape,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            Fmt.keepAll(_diagramNote(l, shape)),
            style: TextStyle(fontSize: 11, height: 1.5, color: scheme.outline),
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              CountryFlag(code: l.countryCode, width: 18),
              const SizedBox(width: 7),
              Expanded(
                child: Text(
                  [
                    country?.nameKo ?? l.countryCode,
                    if (l.roadNumber != null) '대표 차량 ${l.roadNumber}',
                  ].join(' · '),
                  style: TextStyle(fontSize: 12.5, color: scheme.onSurfaceVariant),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          _TitleBlock(loco: l, lang: lang),
          if (!l.verified) ...[
            const SizedBox(height: 8),
            Text(
              '일부 수치는 출처끼리 엇갈려 아직 확인하고 있어요.',
              style: TextStyle(fontSize: 12, color: scheme.secondary),
            ),
          ],

          // ── 뜻풀이 · 본문 ──
          const SizedBox(height: 18),
          Text.rich(
            TextSpan(children: [
              TextSpan(text: Fmt.keepAll(l.gloss.of(lang))),
              _sup(context, l.gloss.src),
            ]),
            style: TextStyle(fontSize: 18, height: 1.5, fontWeight: FontWeight.w600, color: scheme.onSurface),
          ),
          if (l.body.isNotEmpty) ...[
            const SizedBox(height: 10),
            Text.rich(
              TextSpan(children: [
                for (final s in l.body) ...[
                  TextSpan(text: Fmt.keepAll(s.of(lang))),
                  _sup(context, s.src),
                  const TextSpan(text: ' '),
                ],
              ]),
              style: TextStyle(fontSize: 15, height: 1.75, color: scheme.onSurface),
            ),
          ],

          // ── 제원 ──
          const SizedBox(height: 28),
          const _SectionTitle('제원'),
          if (l.specsBasis != null)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Text(
                Fmt.keepAll('기준: ${l.specsBasis!.of(lang)}'),
                style: TextStyle(fontSize: 12, height: 1.5, color: scheme.onSurfaceVariant),
              ),
            ),
          _SpecTable(loco: l, lang: lang, showOriginal: app.showOriginalUnits),

          // ── 연혁 ──
          if (l.history.isNotEmpty) ...[
            const SizedBox(height: 28),
            const _SectionTitle('연혁'),
            for (final h in l.history)
              _Row(
                label: h.dateLabel(lang),
                child: Text.rich(
                  TextSpan(children: [TextSpan(text: Fmt.keepAll(h.of(lang))), _sup(context, h.src)]),
                  style: const TextStyle(fontSize: 14.5, height: 1.55),
                ),
              ),
          ],

          // ── 지금 있는 곳 ──
          const SizedBox(height: 28),
          const _SectionTitle('지금 있는 곳'),
          _LocationBlock(loco: l, lang: lang),

          // ── 출처 ──
          if (l.sources.isNotEmpty) ...[
            const SizedBox(height: 28),
            const _SectionTitle('출처'),
            for (final s in l.sources) _SourceTile(source: s, lang: lang),
          ],

          // ── 더 읽을거리 ──
          const SizedBox(height: 28),
          const _SectionTitle('더 읽을거리'),
          _FurtherReading(loco: l, country: country, repo: repo, lang: lang),
        ],
      ),
    );
  }
}

/// 출처 번호 위첨자. 번호가 없으면 빈 칸.
InlineSpan _sup(BuildContext context, List<int> src) {
  if (src.isEmpty) return const TextSpan(text: '');
  final color = Theme.of(context).colorScheme.primary;
  return WidgetSpan(
    alignment: PlaceholderAlignment.top,
    child: Padding(
      padding: const EdgeInsets.only(left: 2),
      child: Text(
        src.join(','),
        style: TextStyle(
          fontSize: 10,
          height: 1.1,
          fontWeight: FontWeight.w600,
          color: color,
          fontFeatures: const [FontFeature.tabularFigures()],
        ),
      ),
    ),
  );
}

/// 절 제목 — 제목 아래 글자색 1px 선.
class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.text);
  final String text;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.only(bottom: 8),
      decoration: BoxDecoration(border: Border(bottom: BorderSide(color: scheme.onSurface, width: 1))),
      child: Text(text, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
    );
  }
}

/// 표 한 줄 — 왼쪽 이름(96px), 오른쪽 내용. 줄 사이는 가는 선.
class _Row extends StatelessWidget {
  const _Row({required this.label, required this.child});
  final String label;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 11),
      decoration: BoxDecoration(border: Border(bottom: BorderSide(color: scheme.outlineVariant))),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 96,
            child: Padding(
              padding: const EdgeInsets.only(top: 2, right: 8),
              child: Text(label,
                  style: TextStyle(
                    fontSize: 12.5,
                    color: scheme.onSurfaceVariant,
                    fontFeatures: const [FontFeature.tabularFigures()],
                  )),
            ),
          ),
          Expanded(child: child),
        ],
      ),
    );
  }
}

/// 표제란 — 1px 테두리 표. 첫 줄: 형식 | 차륜 배치, 둘째 줄: 제작 | 수량 | 보존 상태.
class _TitleBlock extends StatelessWidget {
  const _TitleBlock({required this.loco, required this.lang});
  final Locomotive loco;
  final Lang lang;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final line = BorderSide(color: scheme.onSurface, width: 1);
    final l = loco;
    final nick = l.nicknameOf(lang);

    Widget cell(String label, Widget value, {bool right = true, bool bottom = true}) => Container(
          padding: const EdgeInsets.fromLTRB(10, 8, 10, 10),
          decoration: BoxDecoration(
            border: Border(right: right ? line : BorderSide.none, bottom: bottom ? line : BorderSide.none),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: TextStyle(fontSize: 11, color: scheme.onSurfaceVariant)),
              const SizedBox(height: 4),
              value,
            ],
          ),
        );

    TextStyle big([double size = 18]) => TextStyle(
          fontSize: size,
          height: 1.25,
          fontWeight: FontWeight.w700,
          color: scheme.onSurface,
          fontFeatures: const [FontFeature.tabularFigures()],
        );

    return Container(
      decoration: BoxDecoration(border: Border.fromBorderSide(line)),
      child: Column(
        children: [
          IntrinsicHeight(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(
                  flex: 2,
                  child: cell(
                    '형식',
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(Fmt.keepAll(l.nameKo), style: big(l.nameKo.length > 8 ? 20 : 25)),
                        const SizedBox(height: 2),
                        Text(l.nameEn, style: TextStyle(fontSize: 12.5, color: scheme.onSurfaceVariant)),
                        if (nick != null) ...[
                          const SizedBox(height: 2),
                          Text(Fmt.keepAll('별명 $nick'),
                              style: TextStyle(fontSize: 12, color: scheme.onSurfaceVariant)),
                        ],
                      ],
                    ),
                  ),
                ),
                Expanded(
                  child: cell(
                    '차륜 배치',
                    // 가라트(4-8-2+2-8-4)처럼 긴 표기는 줄을 바꾸지 않고 칸 폭에 맞춰 줄인다
                    FittedBox(
                      fit: BoxFit.scaleDown,
                      alignment: Alignment.centerLeft,
                      child: Text(l.wheel.whyte, style: big(20), maxLines: 1),
                    ),
                    right: false,
                  ),
                ),
              ],
            ),
          ),
          IntrinsicHeight(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(child: cell('제작', Text(l.builtLabel, style: big()), bottom: false)),
                Expanded(
                  child: cell(
                    '수량',
                    Text(Fmt.keepAll(l.quantityLabel(lang) ?? '자료 없음'),
                        style: l.quantityBuilt == null && l.quantityNote == null
                            ? TextStyle(fontSize: 14, color: scheme.outline)
                            : big(l.quantityNote != null ? 15 : 18)),
                    bottom: false,
                  ),
                ),
                Expanded(
                  child: cell('보존 상태', Text(l.status.label(lang), style: big(16)), right: false, bottom: false),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// 제원표 — 원고의 순서(궤간 → 바퀴 → 실린더 → 압력 → 축거 → 물 → 속도 → 견인력 → 출력 → 중량 → 전장).
///
/// 값은 미터법, 그 옆에 원래 단위(설정에서 끌 수 있다)와 출처 번호. 단서(기준·변형)는 아래 줄에.
/// 최고속도는 설계·허용 값, 기록 속도는 시험·운행 중에 낸 값이라 따로 적는다.
class _SpecTable extends StatelessWidget {
  const _SpecTable({required this.loco, required this.lang, required this.showOriginal});
  final Locomotive loco;
  final Lang lang;
  final bool showOriginal;

  static const _labels = <String, (String, String)>{
    'gaugeMm': ('궤간', 'mm'),
    'driverDiameterMm': ('동륜 지름', 'mm'),
    'leadingWheelDiameterMm': ('선륜 지름', 'mm'),
    'trailingWheelDiameterMm': ('종륜 지름', 'mm'),
    'cylinderSize': ('실린더', 'mm'),
    'cylinders': ('실린더 수', ''),
    'boilerPressureBar': ('보일러 압력', 'bar'),
    'wheelbaseMm': ('축거', 'mm'),
    'waterL': ('물탱크', 'L'),
    'topSpeedKmh': ('최고속도', 'km/h'),
    'recordSpeedKmh': ('기록 속도', 'km/h'),
    'tractiveEffortKn': ('견인력', 'kN'),
    'powerKw': ('출력', 'kW'),
    'weightT': ('중량', 't'),
    'lengthMm': ('전장', 'mm'),
  };

  /// 칸 이름 → 표시할 값(숫자는 원고의 자릿수 그대로). 값이 없으면 null.
  String? _value(String key) {
    final s = loco.specs;
    final num? n = switch (key) {
      'gaugeMm' => loco.gaugeMm,
      'driverDiameterMm' => s.driverDiameterMm,
      'leadingWheelDiameterMm' => s.leadingWheelDiameterMm,
      'trailingWheelDiameterMm' => s.trailingWheelDiameterMm,
      'cylinders' => s.cylinders,
      'boilerPressureBar' => s.boilerPressureBar,
      'wheelbaseMm' => s.wheelbaseMm,
      'waterL' => s.waterL,
      'topSpeedKmh' => s.topSpeedKmh,
      'recordSpeedKmh' => s.recordSpeedKmh,
      'tractiveEffortKn' => s.tractiveEffortKn,
      'powerKw' => s.powerKw,
      'weightT' => s.weightT,
      'lengthMm' => s.lengthMm,
      _ => null,
    };
    if (key == 'cylinderSize') return s.cylinderSize;
    return n == null ? null : Fmt.plain(n);
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final rows = <Widget>[];
    for (final e in loco.specNotes.entries) {
      final key = e.key;
      final note = e.value;
      final label = _labels[key];
      final value = _value(key);
      if (label == null || value == null) continue;
      final (name, unit) = label;
      final extra = <String>[
        if (key == 'gaugeMm') Fmt.gaugeClass(loco.gaugeMm),
        if (key == 'weightT' && loco.specs.weightBasis != null) loco.specs.weightBasis!.label(lang),
      ];
      final noteText = note.note(lang);
      rows.add(_Row(
        label: name,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text.rich(
              TextSpan(children: [
                TextSpan(
                  text: value,
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: scheme.onSurface),
                ),
                if (unit.isNotEmpty)
                  TextSpan(text: ' $unit', style: TextStyle(fontSize: 13, color: scheme.onSurface)),
                if (showOriginal && note.orig != null)
                  TextSpan(text: '   ${note.orig}', style: TextStyle(fontSize: 12.5, color: scheme.onSurfaceVariant)),
                for (final x in extra)
                  TextSpan(text: '   $x', style: TextStyle(fontSize: 12.5, color: scheme.onSurfaceVariant)),
                _sup(context, note.src),
              ]),
              style: const TextStyle(height: 1.45, fontFeatures: [FontFeature.tabularFigures()]),
            ),
            if (noteText != null && noteText.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 3),
                child: Text(Fmt.keepAll(noteText),
                    style: TextStyle(fontSize: 12, height: 1.5, color: scheme.onSurfaceVariant)),
              ),
          ],
        ),
      ));
    }
    if (rows.isEmpty) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 12),
        child: Text('출처로 확인한 제원이 아직 없어요.', style: TextStyle(fontSize: 13, color: scheme.outline)),
      );
    }
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: rows);
  }
}

/// 지금 있는 곳 — 장소, 단서, 지도 앱 버튼. 좌표가 없는 곳('러시아 각지')은 글로만.
class _LocationBlock extends StatelessWidget {
  const _LocationBlock({required this.loco, required this.lang});
  final Locomotive loco;
  final Lang lang;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final loc = loco.location;
    if (loc == null) {
      final text = loco.status == LocoStatus.scrapped
          ? '남아 있는 차량이 없어요.'
          : '보존 위치를 출처로 확인하지 못했어요.';
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 12),
        child: Text(text, style: TextStyle(fontSize: 14, color: scheme.onSurfaceVariant)),
      );
    }
    final note = loc.noteOf(lang);
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(border: Border(bottom: BorderSide(color: scheme.outlineVariant))),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text.rich(
                  TextSpan(children: [TextSpan(text: Fmt.keepAll(loc.nameOf(lang))), _sup(context, loc.src)]),
                  style: const TextStyle(fontSize: 15, height: 1.45, fontWeight: FontWeight.w600),
                ),
                if (note != null && note.isNotEmpty) ...[
                  const SizedBox(height: 3),
                  Text(Fmt.keepAll(note),
                      style: TextStyle(fontSize: 12.5, height: 1.5, color: scheme.onSurfaceVariant)),
                ],
              ],
            ),
          ),
          if (loc.hasPoint) ...[
            const SizedBox(width: 12),
            // 탭: 시스템 '다음으로 열기' 선택창 → 고른 지도 앱에서 시설 이름으로. 길게 누르면 좌표 복사.
            OutlinedButton(
              onPressed: () => PlaceMaps.open(context, loco),
              onLongPress: () => PlaceMaps.copyCoordinates(context, loco),
              style: OutlinedButton.styleFrom(
                foregroundColor: scheme.onSurface,
                side: BorderSide(color: scheme.onSurface),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
                padding: const EdgeInsets.symmetric(horizontal: 12),
                minimumSize: const Size(0, 40),
              ),
              child: const Text('지도 앱에서 열기', style: TextStyle(fontSize: 13)),
            ),
          ],
        ],
      ),
    );
  }
}

/// 출처 한 줄 — 번호와 서지. 링크가 있으면 눌러서 연다.
class _SourceTile extends StatelessWidget {
  const _SourceTile({required this.source, required this.lang});
  final SourceRef source;
  final Lang lang;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final url = source.url;
    final row = Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 26,
            child: Text('${source.n}',
                style: TextStyle(
                  fontSize: 12.5,
                  height: 1.5,
                  fontWeight: FontWeight.w600,
                  color: scheme.primary,
                  fontFeatures: const [FontFeature.tabularFigures()],
                )),
          ),
          Expanded(
            child: Text(
              source.of(lang),
              style: TextStyle(
                fontSize: 12.5,
                height: 1.5,
                color: scheme.onSurface,
                decoration: url != null ? TextDecoration.underline : null,
                decorationColor: scheme.outlineVariant,
              ),
            ),
          ),
        ],
      ),
    );
    if (url == null) return row;
    return InkWell(
      onTap: () => launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication),
      child: row,
    );
  }
}

/// 더 읽을거리 — 이 형식을 다룬 문헌(원고). 그 아래 나라 전반·여러 나라 종합서는 접어 둔다.
class _FurtherReading extends StatelessWidget {
  const _FurtherReading({required this.loco, required this.country, required this.repo, required this.lang});
  final Locomotive loco;
  final Country? country;
  final LocomotiveRepository repo;
  final Lang lang;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final countryRefs = Reference.except(country?.references ?? const [], loco.furtherReading);
    final general = Reference.except(repo.generalReferences, loco.furtherReading);

    Widget item(Reference r, {bool withNote = true}) {
      final note = r.noteOf(lang);
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 6),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('${r.citation}.', style: const TextStyle(fontSize: 13.5, height: 1.5)),
            if (withNote && note.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(Fmt.keepAll(note),
                    style: TextStyle(fontSize: 12, height: 1.5, color: scheme.onSurfaceVariant)),
              ),
          ],
        ),
      );
    }

    Widget folded(String title, List<Reference> refs) => Theme(
          data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
          child: ExpansionTile(
            tilePadding: EdgeInsets.zero,
            childrenPadding: EdgeInsets.zero,
            dense: true,
            title: Text('$title ${refs.length}건',
                style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: scheme.onSurfaceVariant)),
            children: [for (final r in refs) item(r, withNote: false)],
          ),
        );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const SizedBox(height: 4),
        if (loco.furtherReading.isEmpty)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Text('이 형식만 다룬 책은 아직 찾지 못했어요.',
                style: TextStyle(fontSize: 13, color: scheme.onSurfaceVariant)),
          ),
        for (final r in loco.furtherReading) item(r),
        if (countryRefs.isNotEmpty) folded('${country?.nameKo ?? loco.countryCode} 증기기관차 전반', countryRefs),
        if (general.isNotEmpty) folded('여러 나라를 함께 다룬 책', general),
      ],
    );
  }
}

/// 그림 아래 설명 — 도식이 무엇을 근거로 그려졌는지, 특히 추정이 섞인 부분을 밝힌다.
/// 그림만 보고 '이게 실제 모습'이라고 읽히면 곤란하기 때문이다.
String _diagramNote(Locomotive l, LocoShape shape) {
  String trim(String s) => s.endsWith('.') ? s.substring(0, s.length - 1) : s;
  final parts = <String>['차륜 배치와 생김새를 줄여 그린 도식이에요'];
  if (shape.note.isNotEmpty) parts.add('${shape.nameKo}: ${trim(shape.note)}');
  if (l.tenderAxles == null && l.effectiveTenderAxles > 0) {
    parts.add('탄수차는 크기로 어림한 모양이에요');
  }
  return '${parts.join('. ')}.';
}
