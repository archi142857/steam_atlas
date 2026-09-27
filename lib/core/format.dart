/// 표시용 포맷 헬퍼. 값이 없으면 항상 '—'.
class Fmt {
  static const dash = '—';

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
