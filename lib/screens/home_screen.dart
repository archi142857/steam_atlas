import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/tabs.dart';
import '../core/theme.dart';
import '../models/filter_query.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import '../widgets/loco_card.dart';
import 'detail_screen.dart';

/// 홈 — 오늘 뭘 볼지 정해주는 화면.
/// 통계 → 대표 명차 → 시대 바로가기 → 즐겨찾기 순으로 훑는다.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.onJump});

  /// 하단 탭으로 이동시키는 콜백. 인덱스가 아니라 [AppTab] 으로 받는다 — 탭 순서가 바뀌어도 안 깨지게.
  final void Function(AppTab tab) onJump;

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final repo = app.repo!;
    final scheme = Theme.of(context).colorScheme;
    final stats = repo.stats;

    final iconic = repo
        .query(const FilterQuery(iconicOnly: true, sortBy: SortBy.year))
        .take(12)
        .toList();

    return CustomScrollView(
      slivers: [
        SliverAppBar.large(
          title: const Text('Steam Atlas'),
          actions: [
            IconButton(
              icon: const Icon(Icons.search_rounded),
              onPressed: () => onJump(AppTab.explore),
            ),
          ],
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
            child: Text(
              '1804년 첫 주행부터 2022년 마지막 정기 화물까지,\n'
              '세계를 달린 증기기관차 ${stats.total}량.',
              style: TextStyle(
                fontSize: 14,
                height: 1.5,
                color: scheme.onSurfaceVariant,
              ),
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
            child: Row(
              children: [
                _StatTile(
                    label: '수록', value: '${stats.total}', unit: '량', primary: true),
                const SizedBox(width: 10),
                _StatTile(label: '국가', value: '${stats.countries}', unit: '개국'),
                const SizedBox(width: 10),
                _StatTile(
                  label: '아직 달림',
                  value: '${stats.alive}',
                  unit: '량',
                  color: AppTheme.statusColor(LocoStatus.operational, scheme),
                ),
              ],
            ),
          ),
        ),
        _SectionHeader(
          title: '대표 명차',
          subtitle: '먼저 보면 좋을 ${iconic.length}량',
          onMore: () => onJump(AppTab.explore),
        ),
        SliverToBoxAdapter(
          child: SizedBox(
            height: 186,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: iconic.length,
              separatorBuilder: (_, __) => const SizedBox(width: 12),
              itemBuilder: (context, i) {
                final l = iconic[i];
                return SizedBox(
                  width: 290,
                  child: LocoCard(
                    loco: l,
                    livery: app.liveryOf(l),
                    shape: app.shapeOf(l),
                    dense: true,
                    isFavorite: app.isFavorite(l.id),
                    onFavorite: () => app.toggleFavorite(l.id),
                    onTap: () => DetailScreen.push(context, l.id),
                  ),
                );
              },
            ),
          ),
        ),
        _SectionHeader(
          title: '시대로 들어가기',
          subtitle: '증기기관차 200년을 6구간으로',
          onMore: () => onJump(AppTab.timeline),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              children: [
                for (final e in repo.eras)
                  _EraRow(
                    era: e,
                    count: repo
                        .query(FilterQuery(eras: {e.id}))
                        .length,
                    onTap: () {
                      app.setQuery(FilterQuery(eras: {e.id}));
                      onJump(AppTab.timeline);
                    },
                  ),
              ],
            ),
          ),
        ),
        if (app.favoriteLocos.isNotEmpty) ...[
          const _SectionHeader(title: '저장한 기관차'),
          SliverList.separated(
            itemCount: app.favoriteLocos.length,
            separatorBuilder: (_, __) => const SizedBox(height: 10),
            itemBuilder: (context, i) {
              final l = app.favoriteLocos[i];
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: LocoCard(
                  loco: l,
                  livery: app.liveryOf(l),
                  shape: app.shapeOf(l),
                  isFavorite: true,
                  onFavorite: () => app.toggleFavorite(l.id),
                  onTap: () => DetailScreen.push(context, l.id),
                ),
              );
            },
          ),
        ],
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 28, 16, 40),
            child: Text(
              '데이터 ${stats.total}량 중 ${stats.verified}량은 출처 확인을 마쳤습니다. '
              '나머지는 상세 화면에 "확인 필요"로 표시됩니다.',
              style: TextStyle(fontSize: 11.5, color: scheme.outline, height: 1.5),
            ),
          ),
        ),
      ],
    );
  }
}

class _StatTile extends StatelessWidget {
  const _StatTile({
    required this.label,
    required this.value,
    required this.unit,
    this.primary = false,
    this.color,
  });

  final String label;
  final String value;
  final String unit;
  final bool primary;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final c = color ?? (primary ? scheme.primary : scheme.onSurface);
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
        decoration: BoxDecoration(
          color: scheme.surfaceContainer,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label,
                style: TextStyle(fontSize: 11, color: scheme.onSurfaceVariant)),
            const SizedBox(height: 4),
            RichText(
              text: TextSpan(
                children: [
                  TextSpan(
                    text: value,
                    style: TextStyle(
                        fontSize: 22, fontWeight: FontWeight.w800, color: c),
                  ),
                  TextSpan(
                    text: ' $unit',
                    style: TextStyle(
                        fontSize: 11, color: scheme.onSurfaceVariant),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _EraRow extends StatelessWidget {
  const _EraRow({required this.era, required this.count, required this.onTap});
  final Era era;
  final int count;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 4),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              width: 86,
              child: Text(
                era.rangeLabel,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  color: scheme.primary,
                ),
              ),
            ),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(era.nameKo,
                      style: const TextStyle(
                          fontSize: 14.5, fontWeight: FontWeight.w700)),
                  const SizedBox(height: 3),
                  Text(
                    era.note,
                    style: TextStyle(
                        fontSize: 12,
                        height: 1.4,
                        color: scheme.onSurfaceVariant),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Text('$count',
                style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    color: scheme.onSurfaceVariant)),
            Icon(Icons.chevron_right_rounded, size: 18, color: scheme.outline),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({required this.title, this.subtitle, this.onMore});
  final String title;
  final String? subtitle;
  final VoidCallback? onMore;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 28, 8, 12),
        child: Row(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: const TextStyle(
                        fontSize: 17, fontWeight: FontWeight.w800)),
                if (subtitle != null) ...[
                  const SizedBox(height: 2),
                  Text(subtitle!,
                      style: TextStyle(
                          fontSize: 12, color: scheme.onSurfaceVariant)),
                ],
              ],
            ),
            const Spacer(),
            if (onMore != null)
              TextButton(onPressed: onMore, child: const Text('더보기')),
          ],
        ),
      ),
    );
  }
}
