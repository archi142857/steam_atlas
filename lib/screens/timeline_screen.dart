import 'dart:ui' show FontFeature;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import '../widgets/country_flag.dart';
import '../widgets/filter_sheet.dart';
import '../widgets/whyte_diagram.dart';
import 'detail_screen.dart';

/// 연표 — 시대 → 연도순으로 세로 타임라인.
class TimelineScreen extends StatelessWidget {
  const TimelineScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final repo = app.repo!;
    final scheme = Theme.of(context).colorScheme;
    final grouped = repo.groupedByEra(app.query);

    return CustomScrollView(
      slivers: [
        SliverAppBar(
          title: const Text('연표'),
          pinned: true,
          actions: [
            Badge(
              isLabelVisible: app.query.activeCount > 0,
              label: Text('${app.query.activeCount}'),
              child: IconButton(
                icon: const Icon(Icons.tune_rounded),
                onPressed: () => FilterSheet.show(context),
              ),
            ),
            const SizedBox(width: 8),
          ],
        ),
        if (grouped.isEmpty)
          SliverFillRemaining(
            hasScrollBody: false,
            child: Center(
              child: Text('조건에 맞는 기관차가 없습니다',
                  style: TextStyle(color: scheme.onSurfaceVariant)),
            ),
          ),
        for (final entry in grouped.entries) ...[
          SliverToBoxAdapter(
            child: _EraHeader(era: entry.key, count: entry.value.length),
          ),
          SliverList.builder(
            itemCount: entry.value.length,
            itemBuilder: (context, i) => _TimelineTile(
              loco: entry.value[i],
              livery: repo.liveryOf(entry.value[i]),
              shape: repo.shapeOf(entry.value[i]),
              isFirst: i == 0,
              isLast: i == entry.value.length - 1,
              onTap: () => DetailScreen.push(context, entry.value[i].id),
            ),
          ),
        ],
        const SliverToBoxAdapter(child: SizedBox(height: 32)),
      ],
    );
  }
}

class _EraHeader extends StatelessWidget {
  const _EraHeader({required this.era, required this.count});
  final Era era;
  final int count;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      margin: const EdgeInsets.fromLTRB(16, 24, 16, 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: scheme.surfaceContainer,
        borderRadius: BorderRadius.circular(16),
        border: Border(
          left: BorderSide(color: scheme.primary, width: 3),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                era.rangeLabel,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w800,
                  color: scheme.primary,
                  fontFeatures: const [FontFeature.tabularFigures()],
                ),
              ),
              const Spacer(),
              Text('$count량',
                  style:
                      TextStyle(fontSize: 11.5, color: scheme.onSurfaceVariant)),
            ],
          ),
          const SizedBox(height: 4),
          Text(era.nameKo,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
          const SizedBox(height: 6),
          Text(
            era.note,
            style: TextStyle(
                fontSize: 12.5, height: 1.5, color: scheme.onSurfaceVariant),
          ),
        ],
      ),
    );
  }
}

class _TimelineTile extends StatelessWidget {
  const _TimelineTile({
    required this.loco,
    required this.livery,
    required this.shape,
    required this.isFirst,
    required this.isLast,
    required this.onTap,
  });

  final Locomotive loco;
  final Livery? livery;
  final LocoShape shape;
  final bool isFirst;
  final bool isLast;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final dotColor = AppTheme.statusColor(loco.status, scheme);

    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              SizedBox(
                width: 52,
                child: Padding(
                  padding: const EdgeInsets.only(top: 14),
                  child: Text(
                    '${loco.builtFrom ?? ""}',
                    textAlign: TextAlign.right,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                      color: scheme.onSurfaceVariant,
                      fontFeatures: const [FontFeature.tabularFigures()],
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              // 타임라인 축
              SizedBox(
                width: 14,
                child: Column(
                  children: [
                    Container(
                      width: 2,
                      height: 14,
                      color: isFirst
                          ? Colors.transparent
                          : scheme.outlineVariant,
                    ),
                    Container(
                      width: 9,
                      height: 9,
                      decoration: BoxDecoration(
                        color: dotColor,
                        shape: BoxShape.circle,
                      ),
                    ),
                    Expanded(
                      child: Container(
                        width: 2,
                        color:
                            isLast ? Colors.transparent : scheme.outlineVariant,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.only(top: 8, bottom: 14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          CountryFlag(code: loco.countryCode, width: 19),
                          const SizedBox(width: 7),
                          Flexible(
                            child: Text(
                              loco.nameKo,
                              style: const TextStyle(
                                  fontSize: 14.5, fontWeight: FontWeight.w700),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (loco.iconic) ...[
                            const SizedBox(width: 4),
                            Icon(Icons.star_rounded,
                                size: 13, color: scheme.primary),
                          ],
                        ],
                      ),
                      const SizedBox(height: 3),
                      Row(
                        children: [
                          SizedBox(
                            width: 92,
                            child: DiagramPlate(
                              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 4),
                              radius: 7,
                              height: 24,
                              child: WhyteDiagram(
                                wheel: loco.wheel,
                                tenderAxles: loco.effectiveTenderAxles,
                                // 24 이상이어야 차체가 그려진다(WhyteLayout._showBody).
                                // 판 안의 FittedBox 가 폭에 맞춰 줄이므로 결과는 여전히 작다.
                                height: 24,
                                livery: livery,
                                shape: shape,
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Flexible(
                            child: Text(
                              '${loco.wheel.whyte} · ${loco.classDesignation}',
                              style: TextStyle(
                                  fontSize: 11.5, color: scheme.onSurfaceVariant),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                      if (loco.highlights.isNotEmpty) ...[
                        const SizedBox(height: 5),
                        Text(
                          '· ${loco.highlights.first}',
                          style: TextStyle(
                            fontSize: 11.5,
                            height: 1.4,
                            color: scheme.primary,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
