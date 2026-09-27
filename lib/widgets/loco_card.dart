import 'dart:ui' show FontFeature;

import 'package:flutter/material.dart';

import '../core/format.dart';
import '../core/theme.dart';
import '../models/locomotive.dart';
import 'country_flag.dart';
import 'whyte_diagram.dart';

/// 목록에 쓰는 기관차 카드.
///
/// 사진 자산이 아직 없으므로 차륜 도식 + 핵심 수치 3개로 구분되게 만들었다.
/// 이미지가 붙으면 [leading] 자리를 썸네일로 교체하면 된다.
class LocoCard extends StatelessWidget {
  const LocoCard({
    super.key,
    required this.loco,
    this.onTap,
    this.isFavorite = false,
    this.onFavorite,
    this.dense = false,
    this.livery,
    this.shape,
  });

  final Locomotive loco;
  final VoidCallback? onTap;
  final bool isFavorite;
  final VoidCallback? onFavorite;
  final bool dense;

  /// 도색. 화면에서 `app.liveryOf(loco)` 로 넘긴다. null이면 무채색 도식.
  final Livery? livery;

  /// 실루엣 유형. `app.shapeOf(loco)` 로 넘긴다.
  final LocoShape? shape;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final statusColor = AppTheme.statusColor(loco.status, scheme);

    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: EdgeInsets.all(dense ? 12 : 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(top: 2),
                    child: CountryFlag(code: loco.countryCode, width: 24),
                  ),
                  const SizedBox(width: 9),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Flexible(
                              child: Text(
                                loco.nameKo,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: -0.2,
                                ),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            if (loco.iconic) ...[
                              const SizedBox(width: 6),
                              Icon(Icons.star_rounded,
                                  size: 15, color: scheme.primary),
                            ],
                          ],
                        ),
                        const SizedBox(height: 2),
                        Text(
                          '${loco.classDesignation} · ${loco.builtLabel}',
                          style: TextStyle(
                            fontSize: 12,
                            color: scheme.onSurfaceVariant,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                  if (onFavorite != null)
                    IconButton(
                      onPressed: onFavorite,
                      visualDensity: VisualDensity.compact,
                      iconSize: 20,
                      icon: Icon(
                        isFavorite
                            ? Icons.bookmark_rounded
                            : Icons.bookmark_border_rounded,
                        color: isFavorite ? scheme.primary : scheme.outline,
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  // 도식 + 차륜배치 표기를 세로로 묶는다.
                  // 가로로 늘어놓으면 탄수차가 붙은 긴 형식에서 수치와 자리를 다툰다.
                  SizedBox(
                    width: dense ? 100 : 118,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // 흰 판 위에 그린다 — 다크 테마에서도 도색이 실제 색으로 보이게
                        DiagramPlate(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 5),
                          height: dense ? 30 : 34,
                          child: WhyteDiagram(
                            wheel: loco.wheel,
                            tenderAxles: loco.effectiveTenderAxles,
                            height: dense ? 30 : 34,
                            livery: livery,
                            shape: shape,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          loco.wheel.typeName == null
                              ? loco.wheel.whyte
                              : '${loco.wheel.whyte} · ${loco.wheel.typeName}',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                            fontFeatures: [FontFeature.tabularFigures()],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),
                  _MiniStat(
                      label: '최고속도', value: Fmt.speed(loco.specs.topSpeedKmh)),
                  const SizedBox(width: 12),
                  _MiniStat(
                      label: '견인력', value: Fmt.te(loco.specs.tractiveEffortKn)),
                ],
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [
                  _Pill(
                    text: loco.status.labelKo,
                    color: statusColor,
                    filled: loco.status.isAlive,
                  ),
                  // 용도가 '협궤' 인 형식은 궤간 칩이 같은 말을 하므로 용도 칩을 뺀다
                  if (loco.serviceType != ServiceType.narrow)
                    _Pill(text: loco.serviceType.labelKo, color: scheme.outline),
                  _Pill(
                      text: Fmt.gaugeShort(loco.gaugeMm), color: scheme.outline),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MiniStat extends StatelessWidget {
  const _MiniStat({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.end,
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(label,
            style: TextStyle(fontSize: 10, color: scheme.onSurfaceVariant)),
        const SizedBox(height: 1),
        Text(
          value,
          maxLines: 1,
          softWrap: false,
          overflow: TextOverflow.visible,
          style: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w700,
            fontFeatures: [FontFeature.tabularFigures()],
          ),
        ),
      ],
    );
  }
}

class _Pill extends StatelessWidget {
  const _Pill({required this.text, required this.color, this.filled = false});
  final String text;
  final Color color;
  final bool filled;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: filled ? color.withValues(alpha: 0.16) : Colors.transparent,
        border: Border.all(color: color.withValues(alpha: filled ? 0.5 : 0.35)),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: filled ? color : Theme.of(context).colorScheme.onSurfaceVariant,
        ),
      ),
    );
  }
}
