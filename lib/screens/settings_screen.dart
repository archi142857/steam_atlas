import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';

/// 설정 — 테마 전환, 저장 항목 관리, 데이터 출처 안내.
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final repo = app.repo!;
    final scheme = Theme.of(context).colorScheme;
    final stats = repo.stats;
    final verifiedRatio = stats.total == 0 ? 0.0 : stats.verified / stats.total;

    return CustomScrollView(
      slivers: [
        SliverAppBar.large(title: const Text('설정')),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 40),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ── 화면 테마 ──────────────────────────────
                const _Heading('화면 테마'),
                const SizedBox(height: 10),
                SegmentedButton<ThemeMode>(
                  segments: const [
                    ButtonSegment(
                      value: ThemeMode.system,
                      icon: Icon(Icons.brightness_auto_rounded, size: 18),
                      label: Text('시스템'),
                    ),
                    ButtonSegment(
                      value: ThemeMode.light,
                      icon: Icon(Icons.light_mode_rounded, size: 18),
                      label: Text('라이트'),
                    ),
                    ButtonSegment(
                      value: ThemeMode.dark,
                      icon: Icon(Icons.dark_mode_rounded, size: 18),
                      label: Text('다크'),
                    ),
                  ],
                  selected: {app.themeMode},
                  showSelectedIcon: false,
                  onSelectionChanged: (s) => app.setThemeMode(s.first),
                ),
                const SizedBox(height: 10),
                Text(
                  app.themeMode == ThemeMode.system
                      ? '기기의 다크모드 설정을 따릅니다.'
                      : '기기 설정과 관계없이 ${app.themeMode == ThemeMode.dark ? "다크" : "라이트"} 테마를 씁니다.',
                  style: TextStyle(fontSize: 12, color: scheme.onSurfaceVariant),
                ),
                const SizedBox(height: 14),
                const _ThemePreview(),

                // ── 저장한 항목 ────────────────────────────
                const SizedBox(height: 30),
                const _Heading('저장한 기관차'),
                const SizedBox(height: 8),
                _Row(
                  icon: Icons.bookmark_rounded,
                  title: '${app.favorites.length}량 저장됨',
                  subtitle: '카드의 북마크 아이콘으로 추가/해제합니다.',
                  trailing: TextButton(
                    onPressed:
                        app.favorites.isEmpty ? null : () => _confirmClear(context),
                    child: const Text('전체 해제'),
                  ),
                ),

                // ── 지도 ──────────────────────────────────
                const SizedBox(height: 22),
                const _Heading('지도'),
                const SizedBox(height: 8),
                SwitchListTile(
                  value: app.onlineTiles,
                  onChanged: app.setOnlineTiles,
                  contentPadding: EdgeInsets.zero,
                  dense: true,
                  secondary: Icon(Icons.layers_rounded,
                      size: 18, color: scheme.onSurfaceVariant),
                  title: const Text('온라인 상세 지도',
                      style: TextStyle(
                          fontSize: 13.5, fontWeight: FontWeight.w600)),
                  subtitle: Text(
                    app.onlineTiles
                        ? '지도 타일을 내려받아 도로·지명까지 표시합니다. 데이터를 사용합니다.'
                        : '기기에 저장된 지도만 씁니다. 데이터를 쓰지 않고 비행기 모드에서도 동작합니다.',
                    style: TextStyle(
                        fontSize: 11.5,
                        height: 1.5,
                        color: scheme.onSurfaceVariant),
                  ),
                ),

                // ── 필터 ──────────────────────────────────
                const SizedBox(height: 22),
                const _Heading('필터'),
                const SizedBox(height: 8),
                _Row(
                  icon: Icons.tune_rounded,
                  title: app.query.activeCount == 0
                      ? '적용된 필터 없음'
                      : '${app.query.activeCount}개 적용 중',
                  subtitle: '탐색·연표·지도가 같은 필터를 씁니다.',
                  trailing: TextButton(
                    onPressed: app.query.isEmpty ? null : app.clearFilters,
                    child: const Text('초기화'),
                  ),
                ),

                // ── 데이터 ────────────────────────────────
                const SizedBox(height: 30),
                const _Heading('데이터'),
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: scheme.surfaceContainer,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          _Fig(label: '수록', value: '${stats.total}', unit: '량'),
                          _Fig(
                              label: '국가',
                              value: '${stats.countries}',
                              unit: '개국'),
                          _Fig(
                            label: '아직 달림',
                            value: '${stats.alive}',
                            unit: '량',
                            color: AppTheme.statusColor(
                                LocoStatus.operational, scheme),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          Text('출처 확인 완료',
                              style: TextStyle(
                                  fontSize: 12, color: scheme.onSurfaceVariant)),
                          const Spacer(),
                          Text(
                            '${stats.verified} / ${stats.total}량',
                            style: const TextStyle(
                                fontSize: 12, fontWeight: FontWeight.w700),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(99),
                        child: LinearProgressIndicator(
                          value: verifiedRatio,
                          minHeight: 6,
                          backgroundColor: scheme.surfaceContainerHighest,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        '증기기관차 제원은 자료마다 값이 다릅니다(측정 조건·개조 시점·단위 환산). '
                        '교차 확인을 마친 항목만 위 비율에 들어가고, 나머지는 상세 화면에 '
                        '"수치 확인 필요"로 표시됩니다.',
                        style: TextStyle(
                            fontSize: 11.5,
                            height: 1.6,
                            color: scheme.onSurfaceVariant),
                      ),
                    ],
                  ),
                ),

                // ── 정보 ──────────────────────────────────
                const SizedBox(height: 30),
                const _Heading('정보'),
                const SizedBox(height: 8),
                const _Row(
                  icon: Icons.train_rounded,
                  title: 'Steam Atlas 0.1.0',
                  subtitle: '데이터 스키마 v1',
                ),
                const _Row(
                  icon: Icons.flag_rounded,
                  title: '국기 이미지',
                  subtitle: 'flag-icons (MIT License) — 앱에 번들, 오프라인 동작',
                ),
                const _Row(
                  icon: Icons.map_rounded,
                  title: '지도 데이터',
                  subtitle: '기본 지도는 Natural Earth 110m (public domain) — 앱에 포함되어 '
                      '오프라인에서 동작합니다. 온라인 상세 지도를 켜면 '
                      '© OpenStreetMap contributors 타일을 사용합니다.',
                ),
                const _Row(
                  icon: Icons.info_outline_rounded,
                  title: '운행 상태는 계속 바뀝니다',
                  subtitle: '보일러 검사 주기와 복원 일정에 따라 매년 달라집니다. '
                      '방문 전에는 해당 철도의 최신 공지를 확인하세요.',
                ),
                const _Row(
                  icon: Icons.balance_rounded,
                  title: '라이선스',
                  subtitle: '앱 코드는 MIT, 기관차 데이터·설명문은 CC BY-SA 4.0 '
                      '(© 2026 이영표). 국기 flag-icons(MIT), 지도 Natural Earth(퍼블릭 도메인)·world-atlas(ISC).',
                ),
                // Flutter 가 빌드 때 모은 pub 패키지 라이선스 전문 — BSD/MIT 고지 의무는 여기서 이행된다.
                InkWell(
                  onTap: () => showLicensePage(
                    context: context,
                    applicationName: 'Steam Atlas',
                    applicationVersion: '0.1.0',
                    applicationLegalese: '© 2026 이영표 (LEE YOUNGPYO). 코드 MIT · 데이터 CC BY-SA 4.0',
                  ),
                  borderRadius: BorderRadius.circular(8),
                  child: const _Row(
                    icon: Icons.article_outlined,
                    title: '오픈소스 라이선스',
                    subtitle: '앱에 포함된 패키지(flutter_map, provider, flutter_svg …)의 라이선스 전문',
                    trailing: Icon(Icons.chevron_right_rounded, size: 18),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Future<void> _confirmClear(BuildContext context) async {
    final app = context.read<AppState>();
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('저장한 기관차를 모두 해제할까요?'),
        content: Text('${app.favorites.length}량이 목록에서 사라집니다. 되돌릴 수 없습니다.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: const Text('취소')),
          FilledButton(
              onPressed: () => Navigator.pop(ctx, true),
              child: const Text('전체 해제')),
        ],
      ),
    );
    if (ok == true) app.clearFavorites();
  }
}

/// 현재 테마가 카드에 어떻게 보이는지 바로 확인시켜 주는 미리보기 줄.
class _ThemePreview extends StatelessWidget {
  const _ThemePreview();

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: scheme.surfaceContainer,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        children: [
          for (final (label, color) in [
            ('배경', scheme.surface),
            ('카드', scheme.surfaceContainer),
            ('강조', scheme.primary),
            ('본문', scheme.onSurface),
          ])
            Expanded(
              child: Column(
                children: [
                  Container(
                    height: 26,
                    margin: const EdgeInsets.symmetric(horizontal: 3),
                    decoration: BoxDecoration(
                      color: color,
                      borderRadius: BorderRadius.circular(7),
                      border: Border.all(color: scheme.outlineVariant),
                    ),
                  ),
                  const SizedBox(height: 5),
                  Text(label,
                      style:
                          TextStyle(fontSize: 10, color: scheme.onSurfaceVariant)),
                ],
              ),
            ),
        ],
      ),
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

class _Row extends StatelessWidget {
  const _Row({
    required this.icon,
    required this.title,
    this.subtitle,
    this.trailing,
  });

  final IconData icon;
  final String title;
  final String? subtitle;
  final Widget? trailing;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 9),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 18, color: scheme.onSurfaceVariant),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: const TextStyle(
                        fontSize: 13.5, fontWeight: FontWeight.w600)),
                if (subtitle != null) ...[
                  const SizedBox(height: 3),
                  Text(subtitle!,
                      style: TextStyle(
                          fontSize: 11.5,
                          height: 1.5,
                          color: scheme.onSurfaceVariant)),
                ],
              ],
            ),
          ),
          if (trailing != null) trailing!,
        ],
      ),
    );
  }
}

class _Fig extends StatelessWidget {
  const _Fig({
    required this.label,
    required this.value,
    required this.unit,
    this.color,
  });

  final String label;
  final String value;
  final String unit;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label,
              style: TextStyle(fontSize: 10.5, color: scheme.onSurfaceVariant)),
          const SizedBox(height: 3),
          RichText(
            text: TextSpan(children: [
              TextSpan(
                text: value,
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w800,
                  color: color ?? scheme.onSurface,
                ),
              ),
              TextSpan(
                text: ' $unit',
                style: TextStyle(fontSize: 10.5, color: scheme.onSurfaceVariant),
              ),
            ]),
          ),
        ],
      ),
    );
  }
}
