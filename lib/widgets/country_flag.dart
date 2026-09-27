import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

/// 국기 이미지.
///
/// `assets/flags/<코드 소문자>.svg` 를 그린다 (flag-icons, MIT).
/// 이모지 국기는 플랫폼·폰트에 따라 아예 안 나오거나(윈도우) 모양이 제각각이라
/// 번들 SVG로 고정했다. 16개 합쳐 12KB라 용량 부담도 없다.
class CountryFlag extends StatelessWidget {
  const CountryFlag({
    super.key,
    required this.code,
    this.width = 22,
    this.radius = 3,
  });

  final String code;
  final double width;
  final double radius;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final height = width * 3 / 4;
    return Container(
      width: width,
      height: height,
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(radius),
        // 흰 바탕 국기(일본·폴란드 등)가 밝은 배경에서 사라지지 않도록 테두리를 준다
        border: Border.all(color: scheme.outlineVariant, width: 0.6),
      ),
      child: SvgPicture.asset(
        'assets/flags/${code.toLowerCase()}.svg',
        width: width,
        height: height,
        fit: BoxFit.cover,
        placeholderBuilder: (_) => ColoredBox(color: scheme.surfaceContainerHighest),
      ),
    );
  }
}
