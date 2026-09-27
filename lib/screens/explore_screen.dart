import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/app_state.dart';
import '../widgets/filter_sheet.dart';
import '../widgets/loco_card.dart';
import 'compare_screen.dart';
import 'detail_screen.dart';

/// 탐색 — 검색어 + 필터로 전체를 훑는 화면.
class ExploreScreen extends StatefulWidget {
  const ExploreScreen({super.key});

  @override
  State<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends State<ExploreScreen> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: context.read<AppState>().query.text);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final results = app.results;
    final scheme = Theme.of(context).colorScheme;

    // 다른 화면에서 필터를 바꿔 들어온 경우 검색어를 동기화
    if (_controller.text != app.query.text) {
      _controller.value = TextEditingValue(
        text: app.query.text,
        selection: TextSelection.collapsed(offset: app.query.text.length),
      );
    }

    return Column(
      children: [
        SafeArea(
          bottom: false,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    onChanged: app.setText,
                    textInputAction: TextInputAction.search,
                    decoration: InputDecoration(
                      hintText: '이름 · 형식 · 차륜배치(4-6-2) · 제조사',
                      prefixIcon: const Icon(Icons.search_rounded, size: 20),
                      suffixIcon: app.query.text.isEmpty
                          ? null
                          : IconButton(
                              icon: const Icon(Icons.close_rounded, size: 18),
                              onPressed: () {
                                _controller.clear();
                                app.setText('');
                              },
                            ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Badge(
                  isLabelVisible: app.query.activeCount > 0,
                  label: Text('${app.query.activeCount}'),
                  child: IconButton.filledTonal(
                    icon: const Icon(Icons.tune_rounded),
                    onPressed: () => FilterSheet.show(context),
                  ),
                ),
              ],
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(18, 0, 16, 8),
          child: Row(
            children: [
              Text(
                '${results.length}량',
                style: TextStyle(
                    fontSize: 12.5,
                    fontWeight: FontWeight.w700,
                    color: scheme.onSurfaceVariant),
              ),
              const SizedBox(width: 8),
              Text(
                '${app.query.sortBy.labelKo} ${app.query.descending ? "↓" : "↑"}',
                style: TextStyle(fontSize: 12, color: scheme.outline),
              ),
              const Spacer(),
              if (!app.query.isEmpty)
                TextButton(
                  onPressed: app.clearFilters,
                  style: TextButton.styleFrom(
                      visualDensity: VisualDensity.compact),
                  child: const Text('필터 해제'),
                ),
            ],
          ),
        ),
        Expanded(
          child: Stack(
            children: [
              results.isEmpty
                  ? _EmptyState(onReset: app.clearFilters)
                  : ListView.separated(
                      // 비교 알약이 마지막 카드를 가리지 않게 아래 여백을 넉넉히 둔다.
                      padding: EdgeInsets.fromLTRB(
                          16, 4, 16, app.compareIds.isEmpty ? 24 : 76),
                      itemCount: results.length,
                      separatorBuilder: (_, __) => const SizedBox(height: 10),
                      itemBuilder: (context, i) {
                        final l = results[i];
                        return LocoCard(
                          loco: l,
                          livery: app.liveryOf(l),
                          shape: app.shapeOf(l),
                          isFavorite: app.isFavorite(l.id),
                          onFavorite: () => app.toggleFavorite(l.id),
                          onTap: () => DetailScreen.push(context, l.id),
                        );
                      },
                    ),
              if (app.compareIds.isNotEmpty)
                Positioned(
                  left: 0,
                  right: 0,
                  bottom: 14,
                  child: Center(child: _ComparePill(count: app.compareIds.length)),
                ),
            ],
          ),
        ),
      ],
    );
  }
}

/// 결과 목록 위에 떠 있는 비교 알약. 2량이 차면 탭으로 비교 화면, 길게 누르면 비우기.
class _ComparePill extends StatelessWidget {
  const _ComparePill({required this.count});
  final int count;

  @override
  Widget build(BuildContext context) {
    final app = context.read<AppState>();
    final scheme = Theme.of(context).colorScheme;
    final ready = count >= 2;
    return Material(
      color: ready ? scheme.primary : scheme.surfaceContainerHighest,
      elevation: 3,
      shadowColor: Colors.black38,
      borderRadius: BorderRadius.circular(24),
      child: InkWell(
        borderRadius: BorderRadius.circular(24),
        onTap: ready ? () => CompareScreen.push(context) : null,
        onLongPress: () {
          app.clearCompare();
          ScaffoldMessenger.of(context)
            ..hideCurrentSnackBar()
            ..showSnackBar(const SnackBar(content: Text('비교 목록을 비웠습니다')));
        },
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.compare_arrows_rounded,
                  size: 18, color: ready ? scheme.onPrimary : scheme.onSurfaceVariant),
              const SizedBox(width: 8),
              Text(
                ready ? '비교 보기 (2)' : '비교 $count/2 — 상세에서 한 량 더',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: ready ? scheme.onPrimary : scheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  const _EmptyState({required this.onReset});
  final VoidCallback onReset;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.filter_alt_off_rounded, size: 40, color: scheme.outline),
          const SizedBox(height: 12),
          Text('조건에 맞는 기관차가 없습니다',
              style: TextStyle(fontSize: 14, color: scheme.onSurfaceVariant)),
          const SizedBox(height: 8),
          TextButton(onPressed: onReset, child: const Text('필터 초기화')),
        ],
      ),
    );
  }
}
