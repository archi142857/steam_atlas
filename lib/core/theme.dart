import 'package:flutter/material.dart';

import '../models/locomotive.dart';

/// 'Coal & Brass' — 석탄(짙은 회색)과 놋쇠(황동)를 축으로 한 팔레트.
/// 증기기관차의 재질감에서 가져왔다.
///
/// 다크는 사진·도식이 잘 보이도록, 라이트는 종이 질감(따뜻한 회백색)에
/// 잉크 같은 본문색을 얹어 대비를 확보했다. 강조색은 라이트에서 한 단계
/// 어두운 놋쇠를 써야 흰 배경에서 읽힌다.
class AppTheme {
  static const brass = Color(0xFFC8963E);
  static const brassLight = Color(0xFFE3B863);
  static const brassDeep = Color(0xFF8A6416); // 라이트 테마 강조용
  static const ember = Color(0xFFD9663A); // 화실 불빛
  static const emberDeep = Color(0xFFA8431C);
  static const steam = Color(0xFFE8E6E1);
  static const coal = Color(0xFF15171A);
  static const coalRaised = Color(0xFF1E2126);
  static const iron = Color(0xFF2A2E34);
  static const paper = Color(0xFFFAF8F4);
  static const paperRaised = Color(0xFFFFFFFF);
  static const paperSunk = Color(0xFFEFEBE3);
  static const ink = Color(0xFF1E2024);

  /// 도식 판(plate). 기관차 그림은 테마와 상관없이 **항상 흰 판 위에** 그린다 —
  /// 다크 배경에서는 검정·진녹·진청 도색이 전부 묻혀 형식이 구분되지 않았다.
  /// 도색은 실제 색(라이트 팔레트)을 그대로 쓴다.
  static const plate = Color(0xFFFFFFFF);
  static const plateEdge = Color(0x1F000000);

  static ThemeData dark() {
    final scheme = ColorScheme.fromSeed(
      seedColor: brass,
      brightness: Brightness.dark,
    ).copyWith(
      surface: coal,
      surfaceContainer: coalRaised,
      surfaceContainerHighest: iron,
      primary: brassLight,
      secondary: ember,
      onSurface: steam,
      outlineVariant: const Color(0xFF31363D),
    );
    return _base(scheme);
  }

  static ThemeData light() {
    final scheme = ColorScheme.fromSeed(
      seedColor: brass,
      brightness: Brightness.light,
    ).copyWith(
      surface: paper,
      surfaceContainer: paperRaised,
      surfaceContainerHighest: paperSunk,
      primary: brassDeep,
      secondary: emberDeep,
      onSurface: ink,
      onSurfaceVariant: const Color(0xFF5F6268),
      outlineVariant: const Color(0xFFDFD9CE),
    );
    return _base(scheme);
  }

  static ThemeData _base(ColorScheme scheme) {
    final isDark = scheme.brightness == Brightness.dark;
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: scheme.surface,
      appBarTheme: AppBarTheme(
        backgroundColor: scheme.surface,
        surfaceTintColor: Colors.transparent,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          color: scheme.onSurface,
          fontSize: 20,
          fontWeight: FontWeight.w700,
          letterSpacing: -0.3,
        ),
      ),
      cardTheme: CardThemeData(
        color: scheme.surfaceContainer,
        surfaceTintColor: Colors.transparent,
        elevation: 0,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          // 라이트에서는 카드가 흰색이라 배경과 구분되도록 테두리를 준다
          side: isDark
              ? BorderSide.none
              : BorderSide(color: scheme.outlineVariant),
        ),
      ),
      chipTheme: ChipThemeData(
        side: BorderSide(color: scheme.outlineVariant),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(999)),
        labelStyle: TextStyle(fontSize: 12.5, color: scheme.onSurface),
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: scheme.surfaceContainerHighest,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: scheme.surfaceContainer,
        indicatorColor: scheme.primary.withValues(alpha: isDark ? 0.18 : 0.14),
        elevation: 0,
        labelTextStyle: WidgetStatePropertyAll(
          TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w600,
              color: scheme.onSurface),
        ),
      ),
      segmentedButtonTheme: SegmentedButtonThemeData(
        style: ButtonStyle(
          textStyle: const WidgetStatePropertyAll(
              TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
          side: WidgetStatePropertyAll(
              BorderSide(color: scheme.outlineVariant)),
        ),
      ),
      dividerTheme: DividerThemeData(color: scheme.outlineVariant, space: 1),
    );
  }

  /// 보존 상태별 색 — 목록/지도/상세에서 동일하게 쓴다.
  /// 라이트 테마에서는 같은 색조를 어둡게 잡아야 흰 배경에서 읽힌다.
  static Color statusColor(LocoStatus s, ColorScheme scheme) {
    final isDark = scheme.brightness == Brightness.dark;
    return switch (s) {
      LocoStatus.operational =>
        isDark ? const Color(0xFF4CAF7D) : const Color(0xFF1E7A50),
      LocoStatus.operable =>
        isDark ? const Color(0xFF7FB77E) : const Color(0xFF4A7C46),
      LocoStatus.static_ => isDark ? brassLight : brassDeep,
      LocoStatus.restoration =>
        isDark ? const Color(0xFF6FA8DC) : const Color(0xFF2C6AA0),
      LocoStatus.scrapped => scheme.outline,
      LocoStatus.replica =>
        isDark ? const Color(0xFFB08CC9) : const Color(0xFF6E4A87),
    };
  }
}
