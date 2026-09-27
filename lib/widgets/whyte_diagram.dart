import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../core/theme.dart';
import '../models/locomotive.dart';

/// Whyte 표기를 기관차 측면 도식으로 그린다.
///
/// 사진 자산이 없어도 형식의 성격이 한눈에 보이도록 하는 게 목적이다.
///
/// - 선륜·종륜은 작게, 동륜은 크게
/// - 관절식(`4-8-8-4`)과 가라트(`4-8-2+2-8-4`)는 엔진 유닛을 나눠서 그린다
/// - **탄수차(tender)를 뒤에 붙인다.** 탱크식·가라트는 탄수차가 없다
/// - [livery] 를 주면 차체를 그 도색으로 칠한다 (없으면 무채색 선화)
/// - [shape] 로 굴뚝 높이·운전실·유선형 케이싱·실린더 배치를 바꾼다
/// - **커플링로드(사이드로드)** 를 실제 규칙대로 건다 — [WhyteLayout.driverGroups] 참조
///
/// 폭은 [WhyteLayout] 이 정확히 계산해서 넘긴다. 예전에는 대략치를 썼기 때문에
/// 4-8-8-4 같은 긴 형식이 캔버스 밖으로 잘렸다.
class WhyteDiagram extends StatelessWidget {
  const WhyteDiagram({
    super.key,
    required this.wheel,
    this.tenderAxles = 0,
    this.height = 34,
    this.color,
    this.livery,
    this.shape,
  });

  final Wheel wheel;

  /// 탄수차 차축 수. 0이면 탄수차를 그리지 않는다.
  final int tenderAxles;

  final double height;

  /// 선화 색 강제 지정. [livery] 가 있으면 도색의 윤곽색이 우선한다.
  final Color? color;

  /// 도색. 주면 차체가 채워지고, 없으면 예전처럼 선화로만 그린다.
  final Livery? livery;

  /// 실루엣 유형. 없으면 [LocoShape.fallback](표준형).
  final LocoShape? shape;

  @override
  Widget build(BuildContext context) {
    final lv = livery;
    final sh = shape ?? LocoShape.fallback;
    // 그림은 항상 흰 판([DiagramPlate]) 위에 놓이므로 테마와 무관하게 실제 도색(라이트 팔레트)을 쓴다.
    // (예전에는 다크 테마에서 밝힌 값을 썼는데, 그래도 검정 계열은 배경에 묻혔다)
    final lineColor = lv?.line ?? color ?? AppTheme.ink;
    final layout = WhyteLayout(
      whyte: wheel.whyte,
      tenderAxles: tenderAxles,
      height: height,
      shape: sh,
    );
    return CustomPaint(
      size: Size(layout.width, height),
      painter: _WhytePainter(
        layout: layout,
        shape: sh,
        color: lineColor,
        bodyColor: lv?.body,
        edgeColor: lv?.edge ?? lineColor,
        accent: lv?.accent,
      ),
    );
  }
}

/// 도식을 얹는 흰 판. 라이트·다크 어느 테마에서도 같은 흰색이라 도색이 실제 색으로 보인다.
///
/// 카드(34px)·연표(24px)·상세 히어로(70px) 모두 이 위젯으로 감싼다. 판은 주어진 폭을 꽉 채우고,
/// 그림은 판 안에서 **가운데** 놓인다 — 로켓호·페니다렌처럼 짧은 형식이 왼쪽에 몰려 있으면
/// 빅보이와 나란히 놓였을 때 어색하다. 긴 형식은 [FittedBox] 로 줄어들되 짧은 형식을 키우지는 않는다.
///
/// [height] 는 그림의 원래 높이(= `WhyteDiagram.height`). 판 높이는 항상 `height + 위아래 여백` 이다.
/// 이 값 없이 폭만 꽉 채우면 `FittedBox` 가 폭에 맞춰 세로도 늘려 잡아서(가로세로 비율 보존),
/// 짧은 형식일수록 판이 **더 높아지는** 이상한 결과가 났다.
class DiagramPlate extends StatelessWidget {
  const DiagramPlate({
    super.key,
    required this.child,
    required this.height,
    this.padding = const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
    this.radius = 10,
    this.alignment = Alignment.center,
  });

  final Widget child;

  /// 그림의 원래 높이. 판은 이 높이를 그대로 쓴다.
  final double height;
  final EdgeInsets padding;
  final double radius;
  final Alignment alignment;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity, // 판은 폭을 꽉 채우고, 짧은 그림은 그 안에서 가운데
      padding: padding,
      decoration: BoxDecoration(
        color: AppTheme.plate,
        borderRadius: BorderRadius.circular(radius),
        border: Border.all(color: AppTheme.plateEdge),
      ),
      child: SizedBox(
        width: double.infinity,
        height: height,
        // 폭·높이가 모두 정해져 있으면 FittedBox 는 그 칸을 그대로 쓰고, 그림은
        // 칸보다 넓을 때만 줄어든다(scaleDown). 짧은 그림은 원래 크기로 가운데.
        child: FittedBox(fit: BoxFit.scaleDown, alignment: alignment, child: child),
      ),
    );
  }
}

/// 도식의 기하 계산. 그리기와 폭 계산이 **같은 코드**를 쓰도록 분리했다.
class WhyteLayout {
  WhyteLayout({
    required String whyte,
    required this.tenderAxles,
    required this.height,
    LocoShape? shape,
  }) : isTank = whyte.toUpperCase().contains('T') {
    final sh = shape ?? LocoShape.fallback;
    final h = height;
    bigR = h * 0.22;
    smallR = h * 0.13;
    tenderR = h * 0.115;
    baseY = h * 0.88;
    _showBody = h >= 22;

    final pad = h * 0.05;
    final wheelGap = h * 0.05;
    final groupGap = h * 0.06;
    final unitGap = h * 0.14;
    final couplingGap = h * 0.18;

    // "4-8-2+2-8-4" → [[4,8,2], [2,8,4]]  (가라트: 엔진 유닛 2개)
    final units = whyte.split('+').map((unit) {
      return unit
          .split('-')
          .map((p) => int.tryParse(p.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0)
          .toList();
    }).toList();

    // 앞쪽 여유. 카우캐처는 차체보다 앞으로 튀어나오고, 선륜이 없는 형식
    // (0-4-0 등)은 바깥 실린더가 맨 앞에 놓이므로 자리를 비워둬야 잘리지 않는다.
    final noLeading = units.first.isNotEmpty && units.first.first == 0;
    frontPad = (sh.pilot ? h * 0.13 : 0) +
        (sh.cylinder.showsMainRod && noLeading ? h * 0.15 : 0);

    var x = pad + frontPad;

    for (var ui = 0; ui < units.length; ui++) {
      final groups = units[ui];
      final unitStart = x;
      for (var gi = 0; gi < groups.length; gi++) {
        // 첫 그룹은 선륜, 마지막은 종륜, 가운데가 동륜
        final isDriver = groups.length >= 3 && gi > 0 && gi < groups.length - 1;
        final r = isDriver ? bigR : smallR;
        final axles = groups[gi] ~/ 2; // Whyte 는 바퀴 수 → 축 수는 절반
        final groupIdx = <int>[];
        for (var a = 0; a < axles; a++) {
          groupIdx.add(wheels.length);
          wheels.add(_Wheel(x + r, baseY - r, r, isDriver));
          x += r * 2 + wheelGap;
        }
        // 커플링로드는 **한 그룹 안에서만** 걸린다.
        // 관절식(4-8-8-4)은 동륜군이 둘이고 프레임이 따로라 로드도 따로다.
        if (isDriver && groupIdx.isNotEmpty) driverGroups.add(groupIdx);
        if (axles > 0) x += groupGap;
      }
      engineUnits.add(_Span(unitStart, x - wheelGap - groupGap));
      if (ui < units.length - 1) x += unitGap;
    }

    if (tenderAxles > 0) {
      x += couplingGap;
      final start = x;
      for (var i = 0; i < tenderAxles; i++) {
        tenderWheels.add(_Wheel(x + tenderR, baseY - tenderR, tenderR, false));
        x += tenderR * 2 + wheelGap;
      }
      tender = _Span(start, x - wheelGap);
    }

    width = x + pad;
  }

  final int tenderAxles;
  final double height;
  final bool isTank;

  late final double bigR;
  late final double smallR;
  late final double tenderR;
  late final double baseY;
  late final double width;
  late final double frontPad;
  late final bool _showBody;

  final List<_Wheel> wheels = [];
  final List<_Wheel> tenderWheels = [];
  final List<_Span> engineUnits = [];

  /// 서로 커플링로드로 이어진 동륜 묶음(= [wheels] 인덱스).
  /// 관절식·가라트는 묶음이 둘 이상이고, 단동륜기는 원소가 하나인 묶음 하나다.
  final List<List<int>> driverGroups = [];

  _Span? tender;

  bool get showBody => _showBody;
}

class _Wheel {
  const _Wheel(this.cx, this.cy, this.r, this.driver);
  final double cx;
  final double cy;
  final double r;
  final bool driver;

  /// 크랭크 핀 위치. 한 묶음 안의 동륜은 **모두 같은 위상**이어야
  /// 로드가 뻣뻣한 막대로 성립한다 — 그래서 오프셋이 상수다.
  Offset get pin => Offset(cx + r * 0.45, cy + r * 0.20);
}

class _Span {
  const _Span(this.start, this.end);
  final double start;
  final double end;
}

class _WhytePainter extends CustomPainter {
  _WhytePainter({
    required this.layout,
    required this.shape,
    required this.color,
    required this.edgeColor,
    this.bodyColor,
    this.accent,
  });

  final WhyteLayout layout;
  final LocoShape shape;

  /// 배경 위에 긋는 선 — 바퀴·레일·연결기.
  final Color color;

  /// 차체 위에 겹쳐 긋는 선 — 보일러·운전실·탄수차 윤곽.
  final Color edgeColor;

  /// 차체 채움색. null 이면 예전처럼 선화로만 그린다.
  final Color? bodyColor;

  /// 2색 도색의 둘째 색과 그 부위. 단색이면 null.
  final LiveryAccent? accent;

  @override
  void paint(Canvas canvas, Size size) {
    final l = layout;
    final h = l.height;
    final s = shape;

    final sw = h * 0.022 + 0.5;
    final stroke = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = sw
      ..strokeJoin = StrokeJoin.round;
    final fill = Paint()..color = color.withValues(alpha: 0.15);
    final dot = Paint()..color = color;
    final body = bodyColor == null ? null : (Paint()..color = bodyColor!);
    // 2색 도색 — 해당 부위만 둘째 색으로 채운다. 단색이거나 차체를 안 칠하면 body 그대로.
    final acc = accent;
    Paint? fillFor(AccentRole role) =>
        (body != null && acc != null && acc.role == role) ? (Paint()..color = acc.color) : body;
    // 차체 윤곽은 차체 위에 얹히므로 배경용 색이 아니라 edgeColor 로 긋는다.
    final edge = Paint()
      ..color = edgeColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = sw
      ..strokeJoin = StrokeJoin.round;

    // 도색이 있으면 채운 뒤 윤곽선을 덧그린다. [f] 를 주면 그 색으로(2색 도색의 둘째 색).
    void paintRRect(RRect r, [Paint? f]) {
      final p = f ?? body;
      if (p != null) canvas.drawRRect(r, p);
      canvas.drawRRect(r, edge);
    }

    void paintRect(Rect r, [Paint? f]) {
      final p = f ?? body;
      if (p != null) canvas.drawRect(r, p);
      canvas.drawRect(r, edge);
    }

    void paintPath(Path p) {
      if (body != null) canvas.drawPath(p, body);
      canvas.drawPath(p, edge);
    }

    final fine = h >= 28; // 돔·창문 같은 작은 요소는 이보다 작으면 점이 된다
    final bodyBottom = l.baseY - l.bigR * 2 - h * 0.02;
    final bodyTop = bodyBottom - h * 0.20;
    final cabTop = bodyBottom - h * 0.34;
    final hasBody = l.showBody && l.engineUnits.isNotEmpty;
    final bodyStart = hasBody ? l.engineUnits.first.start : 0.0;
    final bodyEnd = hasBody ? l.engineUnits.last.end : 0.0;

    // ── 차체 ────────────────────────────────────────────
    // 가라트는 보일러가 두 엔진 유닛 **사이에** 걸리고, 물·석탄은 양 끝 유닛 위에 얹힌다.
    // 그래서 보일러 구간과 차체 전체 구간이 다르다.
    final isGarratt = l.engineUnits.length > 1;
    final u0 = hasBody ? l.engineUnits.first : const _Span(0, 0);
    final u1 = hasBody ? l.engineUnits.last : const _Span(0, 0);
    final boilerStart =
        isGarratt ? u0.start + (u0.end - u0.start) * 0.55 : bodyStart;
    final boilerEnd = isGarratt ? u1.end - (u1.end - u1.start) * 0.55 : bodyEnd;
    final boilerW = boilerEnd - boilerStart;

    if (hasBody && boilerW > 0) {
      final cabW = (boilerW * 0.24).clamp(h * 0.16, boilerW * 0.4);
      final cabX = boilerEnd - cabW;

      if (s.casing == CasingStyle.full) {
        // ── 유선형: 굴뚝·운전실 없이 통짜 껍데기 하나 ──
        final shellTop = bodyBottom - h * 0.32;
        final nose = (h * 0.26).clamp(0.0, boilerW * 0.5);
        paintPath(Path()
          ..moveTo(boilerStart, bodyBottom)
          ..lineTo(boilerStart, bodyBottom - h * 0.05)
          ..quadraticBezierTo(
              boilerStart + nose * 0.28, shellTop, boilerStart + nose, shellTop)
          ..lineTo(boilerEnd, shellTop)
          ..lineTo(boilerEnd, bodyBottom)
          ..close());
        // 치마(밸런스) — 동륜 윗부분을 덮는 게 유선형기의 인상이다
        paintRect(
            Rect.fromLTRB(boilerStart, bodyBottom, boilerEnd, bodyBottom + h * 0.07));
        if (fine) {
          canvas.drawLine(
            Offset(cabX + cabW * 0.15, shellTop + h * 0.06),
            Offset(cabX + cabW * 0.85, shellTop + h * 0.06),
            edge,
          );
        }
      } else {
        // ── 일반: 보일러 + 운전실 + 굴뚝 ──
        // 부분 유선형은 앞머리 모서리를 크게 굴려 '깎인 코'를 표현한다
        final frontR = s.casing == CasingStyle.half ? h * 0.11 : h * 0.05;
        paintRRect(
          RRect.fromRectAndCorners(
            Rect.fromLTRB(boilerStart, bodyTop, boilerEnd, bodyBottom),
            topLeft: Radius.circular(frontR),
            bottomLeft: Radius.circular(h * 0.05),
            topRight: Radius.circular(h * 0.05),
            bottomRight: Radius.circular(h * 0.05),
          ),
          fillFor(AccentRole.boiler),
        );

        // 연실(스모크박스) 이음선 — 앞쪽 원통과 보일러 통이 나뉘는 자리
        if (fine && boilerW > h * 0.7) {
          final x = boilerStart + (boilerW * 0.22).clamp(h * 0.14, h * 0.34);
          canvas.drawLine(
              Offset(x, bodyTop + h * 0.01), Offset(x, bodyBottom - h * 0.01), edge);
        }

        // 운전실 — 시대에 따라 없거나(초기), 지붕만 있거나, 전운전실
        if (s.cab != CabStyle.none) {
          final top = s.cab == CabStyle.open ? bodyBottom - h * 0.24 : cabTop;
          final w = s.cab == CabStyle.open ? cabW * 0.85 : cabW;
          final x = boilerEnd - w;
          paintRRect(
              RRect.fromLTRBR(x, top, x + w, bodyBottom, Radius.circular(h * 0.05)),
              fillFor(AccentRole.cabTender));
          // 운전실 창
          if (fine && s.cab == CabStyle.full && w > h * 0.20) {
            canvas.drawRect(
              Rect.fromLTWH(x + w * 0.22, top + h * 0.05, w * 0.36, h * 0.085),
              edge,
            );
          }
        }

        // 굴뚝 — 초기 기관차일수록 높다
        final ch = switch (s.chimney) {
          ChimneyStyle.tall => h * 0.20,
          ChimneyStyle.mid => h * 0.11,
          ChimneyStyle.short => h * 0.07,
          ChimneyStyle.none => 0.0,
        };
        if (ch > 0) {
          final cx0 = boilerStart + h * 0.06;
          paintRect(Rect.fromLTRB(cx0, bodyTop - ch, cx0 + h * 0.10, bodyTop),
              fillFor(AccentRole.chimney));
          // 굴뚝 테두리(립) — 초기 굴뚝일수록 두드러진다. 로켓호처럼 흰 굴뚝은 테가 검다.
          if (fine) {
            final lip = s.chimney == ChimneyStyle.tall ? h * 0.030 : h * 0.020;
            paintRect(Rect.fromLTRB(cx0 - lip, bodyTop - ch,
                cx0 + h * 0.10 + lip, bodyTop - ch + h * 0.035));
          }
        }

        // 부분 유선형 — 옆면 치마
        if (s.casing == CasingStyle.half) {
          paintRect(Rect.fromLTRB(boilerStart, bodyBottom, boilerEnd, bodyBottom + h * 0.06),
              fillFor(AccentRole.cabTender));
        }

        // 증기돔·모래돔 — 보일러 위 반원.
        // 탱크식은 그 자리를 물탱크가 차지하므로 생략한다.
        if (fine && s.domes > 0 && !l.isTank) {
          final r = h * 0.055;
          final xs = s.domes >= 2
              ? [boilerStart + boilerW * 0.42, boilerStart + boilerW * 0.62]
              : [boilerStart + boilerW * 0.48];
          for (final dx in xs) {
            final rect = Rect.fromCircle(center: Offset(dx, bodyTop), radius: r);
            if (body != null) canvas.drawArc(rect, 3.1416, 3.1416, true, body);
            canvas.drawArc(rect, 3.1416, 3.1416, false, edge);
          }
        }
      }

      // 가라트 — 앞뒤 엔진 유닛 위에 얹힌 물탱크·석탄고
      if (isGarratt) {
        for (final t in [
          Rect.fromLTRB(u0.start, bodyBottom - h * 0.10, boilerStart, bodyBottom),
          Rect.fromLTRB(boilerEnd, bodyBottom - h * 0.10, u1.end, bodyBottom),
        ]) {
          if (t.width > h * 0.10) {
            paintRRect(RRect.fromRectAndRadius(t, Radius.circular(h * 0.04)));
          }
        }
      }

      // 탱크식 — 물탱크를 보일러 위로 얹어 탄수차가 없는 이유를 보여준다
      if (l.isTank && s.casing != CasingStyle.full) {
        final avail = cabX - boilerStart - h * 0.20;
        final tw = boilerW * 0.42 < avail ? boilerW * 0.42 : avail;
        if (tw > h * 0.15) {
          paintRRect(RRect.fromLTRBR(boilerStart + h * 0.20, bodyTop - h * 0.07,
              boilerStart + h * 0.20 + tw, bodyBottom, Radius.circular(h * 0.03)));
        }
      }

      // 앞 전조등 — 미국·소련 계열의 눈에 띄는 특징
      if (fine && s.lamp) {
        final cy = s.casing == CasingStyle.full
            ? bodyBottom - h * 0.10
            : (bodyTop + bodyBottom) / 2;
        final c = Offset(boilerStart + h * 0.06, cy);
        if (body != null) canvas.drawCircle(c, h * 0.045, body);
        canvas.drawCircle(c, h * 0.045, edge);
      }

      // 카우캐처 — 앞으로 튀어나온 삼각형 (frontPad 로 자리를 잡아뒀다)
      if (s.pilot) {
        paintPath(Path()
          ..moveTo(bodyStart, bodyBottom + h * 0.02)
          ..lineTo(bodyStart, l.baseY)
          ..lineTo(bodyStart - h * 0.13, l.baseY)
          ..close());
      }
    }

    // ── 바퀴 ────────────────────────────────────────────
    // 바퀴 — 2색 도색의 '바퀴' 색(독일·소련·중국·폴란드의 빨간 주행부)이 있으면 그 색으로 채운다.
    final wheelFill = (body != null && acc != null && acc.role == AccentRole.wheels)
        ? (Paint()..color = acc.color.withValues(alpha: 0.9))
        : fill;
    for (final w in [...l.wheels, ...l.tenderWheels]) {
      canvas.drawCircle(Offset(w.cx, w.cy), w.r, wheelFill);
      canvas.drawCircle(Offset(w.cx, w.cy), w.r, stroke);
    }

    // ── 실린더 ──────────────────────────────────────────
    // 위치는 언제나 **동륜군 바로 앞**이다. 4-6-2 라면 선륜 위, 0-6-0 이라면 맨 앞.
    // 바깥 실린더는 프레임 바깥(= 로드와 같은 면)에 있어 옆에서 보면 바퀴를 가린다.
    // 그래서 바퀴 위에 덧그린다.
    final rodY = l.wheels.isEmpty ? 0.0 : (l.baseY - l.bigR + l.bigR * 0.20);
    final cylH = h * 0.11;
    final cylRears = <double>[];
    if (hasBody && s.cylinder.showsMainRod) {
      for (var gi = 0; gi < l.driverGroups.length; gi++) {
        final group = l.driverGroups[gi];
        // 가라트는 엔진 유닛의 **바깥쪽 끝**에 실린더가 붙는다.
        // 뒤 유닛의 실린더는 기관차 맨 뒤에서 앞을 향한다.
        final rearUnit = isGarratt && gi == l.driverGroups.length - 1;
        if (rearUnit) {
          final last = l.wheels[group.last];
          final front = last.cx + last.r + h * 0.03;
          if (front + h * 0.17 <= l.width) {
            paintRect(Rect.fromLTRB(
                front, rodY - cylH / 2, front + h * 0.17, rodY + cylH / 2));
            cylRears.add(front);
          } else {
            cylRears.add(double.nan);
          }
          continue;
        }
        final firstIdx = group.first;
        final first = l.wheels[firstIdx];
        // 앞 차축과의 간격이 좁으면 실린더도 그만큼 짧아진다 (관절식 뒤쪽 유닛)
        final prevRight = firstIdx == 0
            ? 0.0
            : l.wheels[firstIdx - 1].cx + l.wheels[firstIdx - 1].r;
        final rear = first.cx - first.r - h * 0.03;
        final maxW = gi == 0 ? h * 0.17 : (rear - prevRight + h * 0.06);
        final cylW = maxW < h * 0.17 ? maxW : h * 0.17;
        if (cylW >= h * 0.07 && rear - cylW >= 0) {
          paintRect(
              Rect.fromLTRB(rear - cylW, rodY - cylH / 2, rear, rodY + cylH / 2));
          cylRears.add(rear);
        } else {
          cylRears.add(double.nan);
        }
      }
    }

    // ── 로드 (바퀴 위에) ────────────────────────────────
    if (l.showBody) {
      _paintRods(canvas, l, s, rodY, cylRears, boilerStart, boilerW, isGarratt,
          bodyTop, bodyBottom, edgeColor, body);
    }

    // 크랭크 핀 — 로드가 물리는 자리. 기어 구동(페니다렌)에는 없다.
    if (s.cylinder.coupled) {
      for (final w in l.wheels) {
        if (!w.driver) continue;
        canvas.drawCircle(w.pin, h * 0.028 + 0.6, dot);
      }
    }

    // ── 레일 ────────────────────────────────────────────
    canvas.drawLine(
      Offset(0, l.baseY + h * 0.02),
      Offset(size.width, l.baseY + h * 0.02),
      Paint()
        ..color = color.withValues(alpha: 0.45)
        ..strokeWidth = h * 0.02 + 0.4,
    );

    // ── 탄수차 ──────────────────────────────────────────
    final t = l.tender;
    if (hasBody && t != null) {
      // 초기 기관차의 탄수차는 뚜껑 없는 낮은 화차에 가까웠다
      final low = s.cab != CabStyle.full;
      final tBottom = l.baseY - l.tenderR * 2 - h * 0.02;
      final tTop = tBottom - (low ? h * 0.14 : h * 0.22);
      paintRRect(
          RRect.fromLTRBR(t.start - h * 0.04, tTop, t.end + h * 0.04, tBottom,
              Radius.circular(h * 0.04)),
          fillFor(AccentRole.cabTender));
      canvas.drawLine(
        Offset(l.engineUnits.last.end, tBottom + h * 0.10),
        Offset(t.start - h * 0.04, tBottom + h * 0.10),
        stroke,
      );
    }
  }

  /// 커플링로드(사이드로드)·메인로드·특수 구동부.
  ///
  /// 규칙:
  /// - 커플링로드는 **한 동륜군 안에서만** 걸린다. 관절식·가라트는 로드가 따로 논다.
  /// - 동륜이 1축뿐인 단동륜기(로켓 0-2-2, 크램프턴 4-2-0)에는 커플링로드가 없다.
  /// - 메인로드는 바깥 실린더일 때만 보인다. 프레임 사이 실린더는 옆에서 안 보인다.
  void _paintRods(
    Canvas canvas,
    WhyteLayout l,
    LocoShape s,
    double rodY,
    List<double> cylRears,
    double boilerStart,
    double boilerW,
    bool garratt,
    double bodyTop,
    double bodyBottom,
    Color rodColor,
    Paint? body,
  ) {
    final h = l.height;
    final rodW = h * 0.030 + 0.6;
    final mainW = h * 0.038 + 0.7;
    final solid = Paint()..color = rodColor;
    final thinRod = Paint()
      ..color = rodColor
      ..strokeCap = StrokeCap.round
      ..strokeWidth = rodW;
    final mainRod = Paint()
      ..color = rodColor
      ..strokeCap = StrokeCap.round
      ..strokeWidth = mainW;
    final outline = Paint()
      ..color = rodColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = h * 0.022 + 0.5;

    // 페니다렌 — 기어 구동. 커플링로드 대신 큰 플라이휠이 붙는다.
    if (s.cylinder == CylinderStyle.beam) {
      final ws = l.wheels;
      if (ws.isNotEmpty) {
        // 주행륜보다 크고 높이 달린 플라이휠 — 바퀴로 오인되지 않게 크기를 벌린다
        final r = h * 0.26;
        final c = Offset((ws.first.cx + ws.last.cx) / 2, bodyBottom + h * 0.10);
        canvas.drawCircle(c, r, outline);
        canvas.drawCircle(c, h * 0.022 + 0.6, solid);
        if (h >= 28) {
          for (final a in [0.0, 1.047, 2.094]) {
            final dx = r * 0.94 * math.cos(a), dy = r * 0.94 * math.sin(a);
            canvas.drawLine(
                Offset(c.dx - dx, c.dy - dy), Offset(c.dx + dx, c.dy + dy), outline);
          }
        }
        // 보일러 속 실린더에서 플라이휠 크랭크로 가는 연결봉
        final pin = Offset(c.dx + r * 0.55, c.dy + r * 0.25);
        canvas.drawLine(
            Offset(boilerStart + h * 0.14, bodyBottom - h * 0.05), pin, thinRod);
        canvas.drawCircle(pin, h * 0.024 + 0.6, solid);
      }
      return;
    }

    for (final group in l.driverGroups) {
      final ws = group.map((i) => l.wheels[i]).toList();
      // 커플링로드 — 동륜이 2축 이상일 때만.
      if (ws.length >= 2) {
        final a = ws.first.pin, b = ws.last.pin;
        final bar = RRect.fromRectAndRadius(
          Rect.fromLTRB(a.dx - rodW * 0.6, a.dy - rodW / 2, b.dx + rodW * 0.6,
              b.dy + rodW / 2),
          Radius.circular(rodW / 2),
        );
        canvas.drawRRect(bar, solid);
      }
    }

    // 메인로드 + 크로스헤드 — 바깥 실린더일 때만 보인다
    if (s.cylinder.showsMainRod) {
      final rearUnitIdx = garratt ? l.driverGroups.length - 1 : -1;
      for (var gi = 0; gi < cylRears.length && gi < l.driverGroups.length; gi++) {
        if (cylRears[gi].isNaN) continue;
        final group = l.driverGroups[gi];
        // 메인 동륜은 보통 그룹의 두 번째 축 (뒤에서 미는 유닛이면 뒤에서 두 번째)
        final main = gi == rearUnitIdx
            ? l.wheels[group[group.length >= 2 ? group.length - 2 : 0]]
            : l.wheels[group[group.length >= 2 ? 1 : 0]];
        canvas.drawLine(Offset(cylRears[gi], rodY), main.pin, mainRod);
        // 크로스헤드 — 실린더에서 나온 피스톤봉이 메인로드로 넘어가는 자리
        canvas.drawRect(
          Rect.fromCenter(
              center: Offset(
                  cylRears[gi] + (gi == rearUnitIdx ? -h * 0.02 : h * 0.02), rodY),
              width: h * 0.055,
              height: h * 0.07),
          solid,
        );
      }
    }

    // 로켓호 — 보일러 뒤쪽에 얹힌 경사 실린더에서 앞 동륜으로 내려오는 연결봉
    if (s.cylinder == CylinderStyle.angled && l.wheels.isNotEmpty) {
      final driver = l.wheels.where((w) => w.driver).firstOrNull ?? l.wheels.first;
      final from = Offset(boilerStart + boilerW - h * 0.05, bodyTop + h * 0.04);
      canvas.drawLine(from, driver.pin, mainRod);
      if (body != null) canvas.drawCircle(from, h * 0.055, body);
      canvas.drawCircle(from, h * 0.055, outline);
    }

    // 로코모션 1호 — 보일러 위에 선 수직 실린더에서 곧장 내려오는 연결봉
    if (s.cylinder == CylinderStyle.vertical && l.wheels.isNotEmpty) {
      final cx = boilerStart + boilerW * 0.62;
      // 수직 실린더는 바로 아래 동륜을 민다 — 가장 가까운 동륜을 고른다
      final drivers = l.wheels.where((w) => w.driver).toList();
      final driver = drivers.isEmpty
          ? l.wheels.first
          : drivers.reduce((a, b) =>
              (a.cx - cx).abs() <= (b.cx - cx).abs() ? a : b);
      final top = bodyTop - h * 0.12;
      final rect = Rect.fromLTRB(cx - h * 0.04, top, cx + h * 0.04, bodyTop);
      if (body != null) canvas.drawRect(rect, body);
      canvas.drawRect(rect, outline);
      canvas.drawLine(Offset(cx, top + h * 0.02), driver.pin, thinRod);
    }
  }

  @override
  bool shouldRepaint(covariant _WhytePainter old) =>
      old.color != color ||
      old.bodyColor != bodyColor ||
      old.edgeColor != edgeColor ||
      old.accent?.role != accent?.role ||
      old.accent?.color != accent?.color ||
      old.shape.id != shape.id ||
      old.layout.width != layout.width ||
      old.layout.height != layout.height ||
      old.layout.tenderAxles != layout.tenderAxles;
}

extension _FirstOrNull<T> on Iterable<T> {
  T? get firstOrNull => isEmpty ? null : first;
}
