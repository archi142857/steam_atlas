/// 표시용 포맷 헬퍼. 값이 없으면 항상 '—'.
class Fmt {
  static const dash = '—';

  /// 낱말 중간에서 줄이 바뀌지 않게 한다(CSS 의 `word-break: keep-all`).
  ///
  /// Flutter 는 한글을 글자 단위로 줄바꿈해서 '기관/차'처럼 낱말이 갈린다. 낱말 안의 글자 사이에
  /// 보이지 않는 WORD JOINER(U+2060)를 넣어 띄어쓰기에서만 줄이 바뀌게 한다. 화면 표시에만 쓴다.
  static String keepAll(String s) => s
      .split(' ')
      .map((w) => w.runes.length < 2 ? w : w.runes.map(String.fromCharCode).join('⁠'))
      .join(' ');

  static String _thousands(num v) {
    final s = v.toStringAsFixed(0);
    final buf = StringBuffer();
    for (var i = 0; i < s.length; i++) {
      if (i > 0 && (s.length - i) % 3 == 0) buf.write(',');
      buf.write(s[i]);
    }
    return buf.toString();
  }

  static String num_(num? v, {String unit = '', int decimals = 0}) {
    if (v == null) return dash;
    final body = decimals > 0 ? v.toStringAsFixed(decimals) : _thousands(v);
    return unit.isEmpty ? body : '$body $unit';
  }

  /// 출처 값 그대로의 자릿수로 — 1067 → "1,067", 9.7 → "9.7", 145.17 → "145.17", 84.0 → "84".
  /// 상세 화면 제원표처럼 원고의 값을 고치지 않고 보여 줄 때 쓴다.
  static String plain(num v) {
    final whole = v is int || v == v.truncateToDouble();
    if (whole) return _thousands(v);
    final s = v.toString();
    final dot = s.indexOf('.');
    if (dot < 0 || s.contains('e')) return s;
    return '${_thousands(num.parse(s.substring(0, dot)))}${s.substring(dot)}';
  }

  /// 궤간 분류 — 표준궤(1,435 mm)보다 좁으면 협궤, 넓으면 광궤.
  static String gaugeClass(int mm) => mm == 1435 ? '표준궤' : (mm < 1435 ? '협궤' : '광궤');

  static String speed(double? v) => num_(v, unit: 'km/h', decimals: v == null ? 0 : (v % 1 == 0 ? 0 : 1));
  static String weight(double? v) => num_(v, unit: 't', decimals: 1);
  static String power(int? v) => num_(v, unit: 'kW');
  static String te(double? v) => num_(v, unit: 'kN', decimals: 0);
  static String pressure(double? v) => num_(v, unit: 'bar', decimals: 1);
  static String mm(int? v) => num_(v, unit: 'mm');
  static String count(int? v) => num_(v, unit: '량');

  /// 궤간을 사람이 읽는 이름으로.
  static String gauge(int mm) => switch (mm) {
        1435 => '1,435mm 표준궤',
        1520 => '1,520mm 러시아 광궤',
        1600 => '1,600mm 아이리시 광궤',
        1676 => '1,676mm 인도 광궤',
        1067 => '1,067mm 케이프궤간',
        1000 => '1,000mm 미터궤',
        762 => '762mm 협궤',
        750 => '750mm 협궤',
        610 => '610mm 협궤',
        1219 => '1,219mm (초기 궤간)',
        _ => '${_thousands(mm)}mm',
      };

  /// 궤간 짧은 표기(칩용). 프리뷰(HTML)와 동일한 규칙.
  ///
  /// 표준궤보다 좁으면 전부 **협궤**다 — 1,067mm(일본 재래선·남아공)도 협궤. '중간궤' 같은
  /// 용어는 없다(예전 구현의 오류). 표준궤가 아니면 mm 를 같이 적어 1,067 과 762 가 구분되게 한다.
  static String gaugeShort(int mm) {
    if (mm == 1435) return '표준궤';
    return '${mm > 1435 ? '광궤' : '협궤'} ${_thousands(mm)}';
  }
}
