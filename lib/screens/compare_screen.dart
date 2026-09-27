import 'dart:ui' show FontFeature;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/format.dart';
import '../models/locomotive.dart';
import '../state/app_state.dart';
import '../widgets/country_flag.dart';
import '../widgets/whyte_diagram.dart';
import 'detail_screen.dart';

/// 두 량 나란히 놓고 제원 대조.
///
/// 상세 화면의 '비교' 버튼으로 2량을 고르면 여기서 표로 본다. 수치는 큰 쪽을 굵게 표시하되,
/// **중량은 기준(기관차 단독 / +탄수차)이 같을 때만** 비교한다 — 기준이 다르면 두 배 가까이 차이가
/// 나므로 굵게 표시하지 않고 기준을 같이 적는다. 값이 없는 쪽(—)이 있으면 비교하지 않는다.
class CompareScreen extends StatelessWidget {
  const CompareScreen({super.key});

  static Future<void> push(BuildContext context) => Navigator.of(context)
      .push(MaterialPageRoute(builder: (_) => const CompareScreen()));

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final locos = app.compareLocos;

    return Scaffold(
      appBar: AppBar(
        title: const Text('비교'),
        actions: [
          if (locos.isNotEmpty)
            TextButton(onPressed: app.clearCompare, child: const Text('비우기')),
        ],
      ),
      body: locos.length < 2
          ? _Empty(count: locos.length)
          : _CompareTable(a: locos[0], b: locos[1]),
    );
  }
}

class _Empty extends StatelessWidget {
  const _Empty({required this.count});
  final int count;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.compare_arrows_rounded, size: 40, color: scheme.outline),
            const SizedBox(height: 12),
            Text(
              count == 0 ? '비교할 기관차를 2량 고르세요' : '한 량 더 고르세요 (지금 $count량)',
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 6),
            Text(
              '상세 화면 오른쪽 위의 비교 버튼(⇄)으로 넣고 뺍니다. 셋째를 넣으면 먼저 넣은 것이 빠집니다.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 12.5, height: 1.5, color: scheme.onSurfaceVariant),
            ),
          ],
        ),
      ),
    );
  }
}

/// 한 행: 라벨 + 두 값. [betterA]/[betterB]는 굵게 표시할 쪽.
class _Row {
  const _Row(this.label, this.a, this.b, {this.betterA = false, this.betterB = false, this.note});
  final String label;
  final String a;
  final String b;
  final bool betterA;
  final bool betterB;
  final String? note;
}

class _CompareTable extends StatelessWidget {
  const _CompareTable({required this.a, required this.b});
  final Locomotive a;
  final Locomotive b;

  /// 숫자 행. 두 값이 모두 있을 때만 큰 쪽(또는 [lowerIsBetter]면 작은 쪽)을 굵게.
  _Row _num(String label, num? x, num? y, String Function(num?) fmt,
      {bool lowerIsBetter = false, String? note}) {
    var ba = false, bb = false;
    if (x != null && y != null && x != y) {
      final aWins = lowerIsBetter ? x < y : x > y;
      ba = aWins;
      bb = !aWins;
    }
    return _Row(label, fmt(x), fmt(y), betterA: ba, betterB: bb, note: note);
  }

  List<_Row> _rows() {
    final sa = a.specs, sb = b.specs;
    // 중량: 기준이 같을 때만 대조. 다르면 굵게 표시하지 않고 기준을 같이 적는다.
    final sameBasis = sa.weightBasis != null && sa.weightBasis == sb.weightBasis;
    String w(LocoSpecs s) => s.weightT == null
        ? Fmt.dash
        : '${Fmt.weight(s.weightT)}${s.weightBasis == null ? '' : ' (${s.weightBasis!.labelKo})'}';
    final weightRow = sameBasis
        ? _num('중량 (${sa.weightBasis!.labelKo})', sa.weightT, sb.weightT, (v) => Fmt.weight(v as double?))
        : _Row('중량', w(sa), w(sb),
            note: sa.weightT == null || sb.weightT == null
                ? null
                : '중량 기준이 달라 직접 비교하지 않습니다');

    return [
      _Row('형식', a.classDesignation, b.classDesignation),
      _Row('차륜 배치', a.wheel.whyte, b.wheel.whyte),
      _Row('용도', a.serviceType.labelKo, b.serviceType.labelKo),
      _Row('궤간', Fmt.gauge(a.gaugeMm), Fmt.gauge(b.gaugeMm)),
      _Row('제작', a.builtLabel, b.builtLabel),
      _num('생산량', a.quantityBuilt, b.quantityBuilt, (v) => Fmt.count(v as int?)),
      _num('현존', a.survivors, b.survivors, (v) => Fmt.count(v as int?)),
      _Row('상태', a.status.labelKo, b.status.labelKo),
      _num('최고속도', sa.topSpeedKmh, sb.topSpeedKmh, (v) => Fmt.speed(v as double?)),
      _num('견인력', sa.tractiveEffortKn, sb.tractiveEffortKn, (v) => Fmt.te(v as double?)),
      _num('출력', sa.powerKw, sb.powerKw, (v) => Fmt.power(v as int?)),
      weightRow,
      _num('동륜 직경', sa.driverDiameterMm, sb.driverDiameterMm, (v) => Fmt.mm(v as int?)),
      _num('보일러 압력', sa.boilerPressureBar, sb.boilerPressureBar, (v) => Fmt.pressure(v as double?)),
      _Row('실린더', sa.cylinders == null ? Fmt.dash : '${sa.cylinders}기통',
          sb.cylinders == null ? Fmt.dash : '${sb.cylinders}기통'),
      _num('전장', sa.lengthMm, sb.lengthMm, (v) => Fmt.mm(v as int?)),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();
    final scheme = Theme.of(context).colorScheme;
    final rows = _rows();

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 40),
      children: [
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(child: _Head(loco: a, livery: app.liveryOf(a), shape: app.shapeOf(a))),
            const SizedBox(width: 10),
            Expanded(child: _Head(loco: b, livery: app.liveryOf(b), shape: app.shapeOf(b))),
          ],
        ),
        const SizedBox(height: 14),
        Container(
          decoration: BoxDecoration(
            color: scheme.surfaceContainer,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: scheme.outlineVariant),
          ),
          child: Column(
            children: [
              for (var i = 0; i < rows.length; i++) ...[
                if (i > 0) Divider(height: 1, color: scheme.outlineVariant),
                _RowView(row: rows[i]),
              ],
            ],
          ),
        ),
        const SizedBox(height: 12),
        Text(
          '굵은 값이 큰 쪽입니다. 값이 없는(—) 항목과 기준이 다른 중량은 비교하지 않습니다. '
          '"수치 확인 필요" 표시가 있는 기관차의 값은 출처 대조가 끝나지 않은 것입니다.',
          style: TextStyle(fontSize: 11.5, height: 1.5, color: scheme.outline),
        ),
      ],
    );
  }
}

class _Head extends StatelessWidget {
  const _Head({required this.loco, required this.livery, required this.shape});
  final Locomotive loco;
  final Livery? livery;
  final LocoShape shape;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return InkWell(
      onTap: () => DetailScreen.push(context, loco.id),
      borderRadius: BorderRadius.circular(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DiagramPlate(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            height: 34,
            child: WhyteDiagram(
              wheel: loco.wheel,
              tenderAxles: loco.effectiveTenderAxles,
              height: 34,
              livery: livery,
              shape: shape,
            ),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              CountryFlag(code: loco.countryCode, width: 18),
              const SizedBox(width: 6),
              Expanded(
                child: Text(loco.nameKo,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, height: 1.25)),
              ),
            ],
          ),
          const SizedBox(height: 2),
          Text(loco.nameEn,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(fontSize: 11.5, fontStyle: FontStyle.italic, color: scheme.outline)),
          if (!loco.verified)
            Padding(
              padding: const EdgeInsets.only(top: 4),
              child: Text('수치 확인 필요',
                  style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: scheme.secondary)),
            ),
        ],
      ),
    );
  }
}

class _RowView extends StatelessWidget {
  const _RowView({required this.row});
  final _Row row;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    TextStyle cell(bool better, String v) => TextStyle(
          fontSize: 13,
          height: 1.4,
          fontWeight: better ? FontWeight.w800 : FontWeight.w500,
          color: v == Fmt.dash ? scheme.outline : (better ? scheme.primary : scheme.onSurface),
          fontFeatures: const [FontFeature.tabularFigures()],
        );
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(row.label, style: TextStyle(fontSize: 11, color: scheme.onSurfaceVariant)),
          const SizedBox(height: 3),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: Text(row.a, style: cell(row.betterA, row.a))),
              const SizedBox(width: 10),
              Expanded(child: Text(row.b, style: cell(row.betterB, row.b))),
            ],
          ),
          if (row.note != null)
            Padding(
              padding: const EdgeInsets.only(top: 3),
              child: Text(row.note!, style: TextStyle(fontSize: 10.5, color: scheme.outline)),
            ),
        ],
      ),
    );
  }
}
