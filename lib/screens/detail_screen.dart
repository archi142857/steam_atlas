import 'dart:ui' show FontFeature;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/format.dart';
import '../core/place_maps.dart';
import '../core/theme.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import '../widgets/country_flag.dart';
import '../widgets/whyte_diagram.dart';
import 'compare_screen.dart';

/// 상세 카드 — 한 량의 모든 것.
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
        content: Text(added ? '비교에 넣었습니다 ($n/2)' : '비교에서 뺐습니다 ($n/2)'),
        duration: const Duration(seconds: 3),
        action: n == 2
            ? SnackBarAction(label: '비교 보기', onPressed: () => CompareScreen.push(context))
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
      return const Scaffold(body: Center(child: Text('데이터를 찾을 수 없습니다')));
    }
    final scheme = Theme.of(context).colorScheme;
    final country = repo.country(l.countryCode);
    final era = repo.era(l.eraId);
    final livery = repo.liveryOf(l);
    final shape = repo.shapeOf(l);
    final statusColor = AppTheme.statusColor(l.status, scheme);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            pinned: true,
            expandedHeight: 190,
            actions: [
              // 비교: 최대 2량. 셋째를 넣으면 먼저 넣은 것이 빠진다 (AppState.toggleCompare).
              IconButton(
                tooltip: app.isCompared(l.id) ? '비교에서 빼기' : '비교에 넣기',
                icon: Badge(
                  isLabelVisible: app.compareIds.isNotEmpty,
                  label: Text('${app.compareIds.length}'),
                  child: const Icon(Icons.compare_arrows_rounded),
                ),
                color: app.isCompared(l.id) ? scheme.primary : null,
                onPressed: () => _toggleCompare(context, app, l),
              ),
              IconButton(
                tooltip: app.isFavorite(l.id) ? '북마크 해제' : '북마크',
                icon: Icon(app.isFavorite(l.id)
                    ? Icons.bookmark_rounded
                    : Icons.bookmark_border_rounded),
                color: app.isFavorite(l.id) ? scheme.primary : null,
                onPressed: () => app.toggleFavorite(l.id),
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              // 오른쪽에 액션 버튼이 둘(48×2)이라 접힌 제목이 겹치지 않게 여백을 둔다.
              titlePadding: const EdgeInsets.fromLTRB(56, 0, 100, 14),
              title: Text(
                l.nameKo,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              background: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [
                      scheme.surfaceContainerHighest,
                      scheme.surface,
                    ],
                  ),
                ),
                child: Center(
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(16, 0, 16, 34),
                    // 사진 자산이 붙기 전까지는 차륜 도식이 히어로 역할을 한다.
                    // 4-8-8-4 처럼 긴 형식은 화면 폭을 넘기므로 판 안에서 축소한다.
                    // 판은 테마와 무관하게 흰색 — 다크에서 도색이 묻히지 않게.
                    child: DiagramPlate(
                      padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
                      radius: 16,
                      alignment: Alignment.center,
                      height: 70,
                      child: WhyteDiagram(
                        wheel: l.wheel,
                        tenderAxles: l.effectiveTenderAxles,
                        height: 70,
                        color: scheme.primary,
                        livery: livery,
                        shape: shape,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      CountryFlag(code: l.countryCode, width: 21),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          '${country?.nameKo ?? l.countryCode}'
                          ' · ${l.classDesignation}'
                          '${l.roadNumber != null ? " · ${l.roadNumber}" : ""}',
                          style: TextStyle(
                              fontSize: 13, color: scheme.onSurfaceVariant),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(l.nameEn,
                      style: TextStyle(
                          fontSize: 12.5,
                          fontStyle: FontStyle.italic,
                          color: scheme.outline)),
                  // 별명은 공인 형식명과 섞이지 않게 따로 한 줄
                  if (l.nickname != null) ...[
                    const SizedBox(height: 3),
                    Text('별명 · ${l.nickname}',
                        style: TextStyle(
                            fontSize: 12.5, color: scheme.onSurfaceVariant)),
                  ],
                  const SizedBox(height: 14),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      _Tag(text: l.status.labelKo, color: statusColor, filled: true),
                      if (l.serviceType != ServiceType.narrow) // 궤간 태그와 중복
                        _Tag(text: l.serviceType.labelKo, color: scheme.outline),
                      if (era != null)
                        _Tag(
                            text: '${era.nameKo} ${era.rangeLabel}',
                            color: scheme.outline),
                      _Tag(text: Fmt.gauge(l.gaugeMm), color: scheme.outline),
                      if (!l.verified)
                        _Tag(
                            text: '수치 확인 필요',
                            color: scheme.secondary,
                            filled: true),
                    ],
                  ),
                  if (l.summary.isNotEmpty) ...[
                    const SizedBox(height: 18),
                    Text(l.summary,
                        style: const TextStyle(fontSize: 14.5, height: 1.7)),
                  ],
                  if (l.highlights.isNotEmpty) ...[
                    const SizedBox(height: 18),
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: scheme.primary.withValues(alpha: 0.08),
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          for (final h in l.highlights)
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 3),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Icon(Icons.bolt_rounded,
                                      size: 15, color: scheme.primary),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Text(h,
                                        style: const TextStyle(
                                            fontSize: 13, height: 1.5)),
                                  ),
                                ],
                              ),
                            ),
                        ],
                      ),
                    ),
                  ],
                  const SizedBox(height: 20),
                  Text(
                    _diagramNote(l, shape),
                    style: TextStyle(
                        fontSize: 11, height: 1.5, color: scheme.outline),
                  ),
                  const SizedBox(height: 26),
                  const _Heading('제원'),
                  const SizedBox(height: 10),
                  _SpecGrid(loco: l),
                  const SizedBox(height: 26),
                  const _Heading('이력'),
                  const SizedBox(height: 6),
                  _KeyValue('차륜 배치',
                      '${l.wheel.whyte}${l.wheel.typeName != null ? " (${l.wheel.typeName})" : ""}'),
                  if (l.wheel.uic != null) _KeyValue('UIC 표기', l.wheel.uic!),
                  if (livery != null) _LiveryRow(livery: livery),
                  _KeyValue('제작', l.builtLabel),
                  _KeyValue('생산량', Fmt.count(l.quantityBuilt)),
                  _KeyValue('퇴역',
                      l.withdrawnYear == null ? Fmt.dash : '${l.withdrawnYear}'),
                  _KeyValue('현존', Fmt.count(l.survivors)),
                  if (l.designer != null) _KeyValue('설계', l.designer!),
                  if (l.builders.isNotEmpty)
                    _KeyValue('제조', l.builders.join(', ')),
                  if (l.operators.isNotEmpty)
                    _KeyValue('운영', l.operators.join(', ')),
                  if (l.location != null) ...[
                    const SizedBox(height: 26),
                    const _Heading('지금 있는 곳'),
                    const SizedBox(height: 10),
                    Material(
                      color: scheme.surfaceContainer,
                      borderRadius: BorderRadius.circular(14),
                      clipBehavior: Clip.antiAlias,
                      child: InkWell(
                        // 탭하면 시스템 '다음으로 열기' 선택창 → 고른 지도 앱에서 시설 이름으로 표시
                        onTap: () => PlaceMaps.open(context, l),
                        onLongPress: () =>
                            PlaceMaps.copyCoordinates(context, l),
                        child: Padding(
                          padding: const EdgeInsets.all(14),
                          child: Row(
                            children: [
                              Icon(Icons.place_rounded,
                                  size: 18, color: statusColor),
                              const SizedBox(width: 10),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(l.location!.name,
                                        style: const TextStyle(
                                            fontSize: 13.5,
                                            fontWeight: FontWeight.w600,
                                            height: 1.4)),
                                    const SizedBox(height: 3),
                                    Row(
                                      children: [
                                        Text(
                                          '${l.location!.lat.toStringAsFixed(3)}, '
                                          '${l.location!.lon.toStringAsFixed(3)}',
                                          style: TextStyle(
                                              fontSize: 11,
                                              color: scheme.outline),
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          '지도 앱에서 열기',
                                          style: TextStyle(
                                            fontSize: 11,
                                            fontWeight: FontWeight.w600,
                                            color: scheme.primary,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                              Icon(Icons.open_in_new_rounded,
                                  size: 16, color: scheme.primary),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      '길게 누르면 좌표만 복사됩니다.',
                      style: TextStyle(fontSize: 11, color: scheme.outline),
                    ),
                  ],
                  if (l.tags.isNotEmpty) ...[
                    const SizedBox(height: 26),
                    const _Heading('태그'),
                    const SizedBox(height: 10),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        for (final t in l.tags)
                          _Tag(text: '#$t', color: scheme.outline),
                      ],
                    ),
                  ],
                  // 참고문헌 — 서적·논문·공식 자료. 이 형식을 직접 다룬 것 → 나라 전반 → 종합서 순.
                  const SizedBox(height: 26),
                  const _Heading('참고문헌'),
                  const SizedBox(height: 4),
                  Text(
                    '도서관 목록·출판사·학술 DB 에서 서지를 확인한 것만 실었습니다. 웹 페이지는 아래 "웹 출처"에.',
                    style: TextStyle(fontSize: 11.5, height: 1.5, color: scheme.outline),
                  ),
                  const SizedBox(height: 8),
                  _ReferenceGroup(title: '이 형식을 다룬 문헌', refs: l.references),
                  _ReferenceGroup(
                      title: '${country?.nameKo ?? l.countryCode} 증기기관차 전반',
                      // 같은 책이 형식 문헌에도 있으면 한 번만 (RCTS 형식사 등)
                      refs: Reference.except(country?.references ?? const [], l.references)),
                  _ReferenceGroup(title: '여러 나라에 걸친 종합서', refs: repo.generalReferences, collapsed: true),
                  const SizedBox(height: 26),
                  const _Heading('웹 출처'),
                  const SizedBox(height: 8),
                  if (l.sources.isEmpty)
                    Text(
                      '출처 미확인 — 이 항목의 수치는 교차 검증이 필요합니다.',
                      style: TextStyle(fontSize: 12, color: scheme.secondary),
                    )
                  else
                    for (final s in l.sources)
                      Padding(
                        padding: const EdgeInsets.symmetric(vertical: 3),
                        child: Text(s,
                            style: TextStyle(
                                fontSize: 11.5,
                                height: 1.5,
                                color: scheme.outline)),
                      ),
                  const SizedBox(height: 48),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _SpecGrid extends StatelessWidget {
  const _SpecGrid({required this.loco});
  final Locomotive loco;

  @override
  Widget build(BuildContext context) {
    final s = loco.specs;
    final items = <(String, String)>[
      ('최고속도', Fmt.speed(s.topSpeedKmh)),
      ('견인력', Fmt.te(s.tractiveEffortKn)),
      ('출력', Fmt.power(s.powerKw)),
      // 기관차 단독인지 탄수차 포함인지 모르면 비교가 안 되므로 기준을 같이 적는다
      (s.weightBasis == null ? '중량' : '중량 (${s.weightBasis!.labelKo})',
          Fmt.weight(s.weightT)),
      ('동륜 직경', Fmt.mm(s.driverDiameterMm)),
      ('보일러 압력', Fmt.pressure(s.boilerPressureBar)),
      ('실린더', s.cylinders == null ? Fmt.dash : '${s.cylinders}기통'),
      ('전장', Fmt.mm(s.lengthMm)),
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 2.5,
      ),
      itemCount: items.length,
      itemBuilder: (context, i) {
        final scheme = Theme.of(context).colorScheme;
        final (label, value) = items[i];
        final missing = value == Fmt.dash;
        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
          decoration: BoxDecoration(
            color: scheme.surfaceContainer,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(label,
                  style: TextStyle(fontSize: 11, color: scheme.onSurfaceVariant)),
              const SizedBox(height: 3),
              Text(
                value,
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w700,
                  color: missing ? scheme.outline : scheme.onSurface,
                  fontFeatures: const [FontFeature.tabularFigures()],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class _Heading extends StatelessWidget {
  const _Heading(this.text);
  final String text;

  @override
  Widget build(BuildContext context) => Text(
        text,
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w800,
          letterSpacing: 0.8,
          color: Theme.of(context).colorScheme.onSurfaceVariant,
        ),
      );
}

class _KeyValue extends StatelessWidget {
  const _KeyValue(this.k, this.v);
  final String k;
  final String v;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 7),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 78,
            child: Text(k,
                style: TextStyle(fontSize: 12.5, color: scheme.onSurfaceVariant)),
          ),
          Expanded(
            child: Text(v,
                style: const TextStyle(fontSize: 13, height: 1.5)),
          ),
        ],
      ),
    );
  }
}

/// 히어로 도식 아래 설명문.
///
/// 도식이 무엇을 근거로 그려졌는지 밝힌다 — 특히 **추정이 섞인 부분**을.
/// 그림만 보고 '이게 실제 모습'이라고 읽히면 곤란하기 때문이다.
String _diagramNote(Locomotive l, LocoShape shape) {
  final parts = <String>['위 그림은 차륜 배치와 생김새를 요약한 도식입니다'];
  if (shape.note.isNotEmpty) {
    parts.add('${shape.nameKo} — ${shape.note}');
  }
  if (l.tenderAxles == null && l.effectiveTenderAxles > 0) {
    parts.add('탄수차는 크기로 추정한 개략 표현입니다');
  }
  return '${parts.join('. ')}.';
}

/// 도색 한 줄 — 실제 색 견본 + 이름.
///
/// 견본은 **라이트 테마의 원색**을 보여준다. 다크 테마용 값은 배경에 묻히지
/// 않도록 밝힌 것이라 '실제 도색은 이 색'이라고 말하기 어렵기 때문이다.
class _LiveryRow extends StatelessWidget {
  const _LiveryRow({required this.livery});
  final Livery livery;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 7),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 78,
            child: Text('도색',
                style:
                    TextStyle(fontSize: 12.5, color: scheme.onSurfaceVariant)),
          ),
          _swatch(livery.body, livery.line),
          // 2색 도색은 둘째 색 견본을 나란히 — 어느 부위인지는 아래 한 줄로.
          if (livery.accent != null) _swatch(livery.accent!.color, livery.line),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${livery.nameKo} · ${livery.nameEn}',
                  style: const TextStyle(fontSize: 13, height: 1.5),
                ),
                if (livery.accent case final a?)
                  Text(
                    '${a.role.labelKo}만 둘째 색${a.note.isEmpty ? '' : ' — ${a.note}'}',
                    style: TextStyle(fontSize: 11, height: 1.45, color: scheme.outline),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _swatch(Color fill, Color line) => Container(
        width: 15,
        height: 15,
        margin: const EdgeInsets.only(top: 2, right: 6),
        decoration: BoxDecoration(
          color: fill,
          borderRadius: BorderRadius.circular(4),
          border: Border.all(color: line, width: 1),
        ),
      );
}

class _Tag extends StatelessWidget {
  const _Tag({required this.text, required this.color, this.filled = false});
  final String text;
  final Color color;
  final bool filled;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: filled ? color.withValues(alpha: 0.16) : Colors.transparent,
        border: Border.all(color: color.withValues(alpha: filled ? 0.5 : 0.35)),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 11.5,
          fontWeight: FontWeight.w600,
          color: filled ? color : Theme.of(context).colorScheme.onSurfaceVariant,
        ),
      ),
    );
  }
}


/// 참고문헌 묶음. 비어 있으면 그리지 않는다. [collapsed] 는 처음에 접어 둔다(종합서처럼 모든 항목에 반복되는 것).
class _ReferenceGroup extends StatelessWidget {
  const _ReferenceGroup({required this.title, required this.refs, this.collapsed = false});
  final String title;
  final List<Reference> refs;
  final bool collapsed;

  @override
  Widget build(BuildContext context) {
    if (refs.isEmpty) return const SizedBox.shrink();
    final scheme = Theme.of(context).colorScheme;
    final items = [for (final r in refs) _ReferenceTile(r: r)];
    if (!collapsed) {
      return Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(title,
                  style: TextStyle(
                      fontSize: 12, fontWeight: FontWeight.w700, color: scheme.onSurfaceVariant)),
            ),
            ...items,
          ],
        ),
      );
    }
    return Theme(
      data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
      child: ExpansionTile(
        tilePadding: EdgeInsets.zero,
        childrenPadding: EdgeInsets.zero,
        dense: true,
        title: Text('$title (${refs.length})',
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: scheme.onSurfaceVariant)),
        children: items,
      ),
    );
  }
}

class _ReferenceTile extends StatelessWidget {
  const _ReferenceTile({required this.r});
  final Reference r;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 5),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _Tag(text: r.kindLabelKo, color: scheme.outline),
              const SizedBox(width: 6),
              _Tag(text: r.lang.toUpperCase(), color: scheme.outline),
              const SizedBox(width: 8),
              Expanded(
                child: Text(r.citation,
                    style: const TextStyle(fontSize: 12.5, height: 1.45, fontWeight: FontWeight.w600)),
              ),
            ],
          ),
          if (r.note.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 2, left: 2),
              child: Text(r.note,
                  style: TextStyle(fontSize: 11.5, height: 1.45, color: scheme.onSurfaceVariant)),
            ),
          Padding(
            padding: const EdgeInsets.only(top: 2, left: 2),
            child: Text(
              [
                if (r.isbn != null) 'ISBN ${r.isbn}',
                '확인: ${r.via}',
                if (r.url != null) r.url!,
              ].join(' · '),
              style: TextStyle(fontSize: 10.5, height: 1.45, color: scheme.outline),
            ),
          ),
        ],
      ),
    );
  }
}
