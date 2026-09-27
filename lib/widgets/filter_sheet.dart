import 'dart:ui' show FontFeature;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/format.dart';
import '../models/filter_query.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import 'country_flag.dart';

/// 하단 시트 형태의 필터 패널.
/// 탐색/연표/지도 어디서든 같은 시트를 띄운다.
class FilterSheet extends StatelessWidget {
  const FilterSheet({super.key});

  static Future<void> show(BuildContext context) {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (_) => const FilterSheet(),
    );
  }

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final repo = app.repo;
    if (repo == null) return const SizedBox.shrink();
    final q = app.query;

    return DraggableScrollableSheet(
      expand: false,
      initialChildSize: 0.75,
      maxChildSize: 0.92,
      builder: (context, controller) => ListView(
        controller: controller,
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 32),
        children: [
          Row(
            children: [
              const Text('필터',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700)),
              const Spacer(),
              TextButton(
                onPressed: q.isEmpty ? null : app.clearFilters,
                child: const Text('초기화'),
              ),
            ],
          ),
          const SizedBox(height: 8),
          _Section(
            title: '정렬',
            child: Wrap(
              spacing: 8,
              children: [
                for (final s in SortBy.values)
                  ChoiceChip(
                    label: Text(s.labelKo),
                    selected: q.sortBy == s,
                    onSelected: (_) => app.setSort(s),
                  ),
                FilterChip(
                  avatar: Icon(
                    q.descending ? Icons.arrow_downward : Icons.arrow_upward,
                    size: 16,
                  ),
                  label: Text(q.descending ? '내림차순' : '오름차순'),
                  selected: q.descending,
                  onSelected: (v) => app.setSort(q.sortBy, descending: v),
                ),
              ],
            ),
          ),
          _Section(
            title: '빠른 조건',
            child: Wrap(
              spacing: 8,
              children: [
                FilterChip(
                  label: const Text('대표 명차만'),
                  selected: q.iconicOnly,
                  onSelected: (v) =>
                      app.setQuery(q.copyWith(iconicOnly: v)),
                ),
                FilterChip(
                  label: const Text('지금 움직이는 것만'),
                  selected: q.aliveOnly,
                  onSelected: (v) => app.setQuery(q.copyWith(aliveOnly: v)),
                ),
              ],
            ),
          ),
          _Section(
              title: '국가',
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  for (final c in repo.countries)
                    FilterChip(
                      avatar: CountryFlag(code: c.code, width: 20),
                      label: Text('${c.nameKo} ${repo.countFor(c.code)}'),
                      selected: q.countries.contains(c.code),
                      onSelected: (_) => app.toggleCountry(c.code),
                    ),
                ],
              ),
            ),
          _Section(
            title: '시대',
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final e in repo.eras)
                  FilterChip(
                    label: Text('${e.nameKo} · ${e.rangeLabel}'),
                    selected: q.eras.contains(e.id),
                    onSelected: (_) => app.toggleEra(e.id),
                  ),
              ],
            ),
          ),
          _Section(
            title: '용도',
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final t in ServiceType.values)
                  FilterChip(
                    label: Text(t.labelKo),
                    selected: q.serviceTypes.contains(t),
                    onSelected: (_) => app.toggleService(t),
                  ),
              ],
            ),
          ),
          _Section(
            title: '보존 상태',
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final s in LocoStatus.values)
                  FilterChip(
                    label: Text(s.labelKo),
                    selected: q.statuses.contains(s),
                    onSelected: (_) => app.toggleStatus(s),
                  ),
              ],
            ),
          ),
          _Section(
            title: '궤간',
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final g in repo.availableGauges)
                  FilterChip(
                    label: Text(Fmt.gauge(g)),
                    selected: q.gauges.contains(g),
                    onSelected: (_) => app.toggleGauge(g),
                  ),
              ],
            ),
          ),
          // 도색 계열 — 44종 도색을 여섯 색 계열로 묶은 것 (Livery.family). 견본색은 계열 대표색.
          _Section(
            title: '도색',
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final f in repo.availableLiveryFamilies)
                  FilterChip(
                    avatar: CircleAvatar(backgroundColor: f.swatch, radius: 7),
                    label: _CountLabel(f.labelKo, repo.countLiveryFamily(f)),
                    selected: q.liveryFamilies.contains(f),
                    onSelected: (_) => app.toggleLiveryFamily(f),
                  ),
              ],
            ),
          ),
          // 생김새 — 도식의 실루엣 종류 (LocoShape). 카탈로그 순서가 대체로 시대순이다.
          _Section(
            title: '생김새',
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final s in repo.availableShapes)
                  FilterChip(
                    label: _CountLabel(s.nameKo, repo.countShape(s.id)),
                    tooltip: s.note,
                    selected: q.shapes.contains(s.id),
                    onSelected: (_) => app.toggleShape(s.id),
                  ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () => Navigator.of(context).pop(),
            style: FilledButton.styleFrom(
              minimumSize: const Size.fromHeight(50),
            ),
            child: Text('${app.results.length}량 보기'),
          ),
        ],
      ),
    );
  }
}

/// 칩 라벨 "이름 n" — 숫자는 옅게. 몇 량이 걸리는지 미리 보여 빈 결과를 줄인다.
class _CountLabel extends StatelessWidget {
  const _CountLabel(this.text, this.count);
  final String text;
  final int count;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Text.rich(
      TextSpan(
        text: text,
        children: [
          TextSpan(
            text: ' $count',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w500,
              color: scheme.outline,
              fontFeatures: const [FontFeature.tabularFigures()],
            ),
          ),
        ],
      ),
    );
  }
}

class _Section extends StatelessWidget {
  const _Section({required this.title, required this.child});
  final String title;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w700,
              letterSpacing: 0.6,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 10),
          child,
        ],
      ),
    );
  }
}
