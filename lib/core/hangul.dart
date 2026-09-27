/// 한글 검색 보조.
///
/// 한국어 검색이 "깨지는" 이유는 대개 두 가지다.
///
/// 1. **자모 분리(NFD)**: iOS/macOS 키보드나 일부 IME는 '맬러드'를 'ㅁ+ㅐ+ㄹ…' 처럼
///    분리된 자모(U+1100~)로 넘겨준다. 데이터 쪽은 완성형(NFC)이라 그대로 비교하면
///    한 글자도 맞지 않는다. Dart 표준 라이브러리에는 유니코드 정규화가 없어서
///    한글 음절에 한해 직접 합친다([composeHangul]).
/// 2. **입력 도중 상태**: '맬'을 치는 도중 'ㅁ', '매', '맬' 이 차례로 들어온다.
///    이때는 검색어를 초성으로 취급하면 자연스럽다([initials], [isChoseongQuery]).
///
/// 공백은 모두 무시한다 ("미카 3형" == "미카3형").
library;

const int _lBase = 0x1100; // 초성 ᄀ
const int _vBase = 0x1161; // 중성 ᅡ
const int _tBase = 0x11A7; // 종성 (없음 = 0)
const int _sBase = 0xAC00; // 가
const int _lCount = 19;
const int _vCount = 21;
const int _tCount = 28;
const int _sCount = _lCount * _vCount * _tCount; // 11172

/// 호환 자모(ㄱ~ㅎ, U+3131~) 순서의 초성 표. 음절 초성 인덱스(0~18)와 짝을 맞춰 둔다.
const List<String> _choseong = [
  'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', //
  'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
];

bool _isL(int c) => c >= _lBase && c < _lBase + _lCount;
bool _isV(int c) => c >= _vBase && c < _vBase + _vCount;
bool _isT(int c) => c > _tBase && c < _tBase + _tCount;
bool _isSyllable(int c) => c >= _sBase && c < _sBase + _sCount;

/// 분리된 한글 자모(NFD)를 완성형 음절(NFC)로 합친다. 한글이 아닌 문자는 그대로 둔다.
String composeHangul(String s) {
  final src = s.runes.toList();
  final out = <int>[];
  var i = 0;
  while (i < src.length) {
    final c = src[i];
    if (_isL(c) && i + 1 < src.length && _isV(src[i + 1])) {
      var syl = _sBase + ((c - _lBase) * _vCount + (src[i + 1] - _vBase)) * _tCount;
      i += 2;
      if (i < src.length && _isT(src[i])) {
        syl += src[i] - _tBase;
        i += 1;
      }
      out.add(syl);
      continue;
    }
    // 이미 완성형인 음절 뒤에 종성 자모만 따로 붙어 오는 경우(받침 없는 음절 + 종성)
    if (_isSyllable(c) && (c - _sBase) % _tCount == 0 && i + 1 < src.length && _isT(src[i + 1])) {
      out.add(c + (src[i + 1] - _tBase));
      i += 2;
      continue;
    }
    out.add(c);
    i += 1;
  }
  return String.fromCharCodes(out);
}

/// 검색 비교용 키. 자모 합치기 → 소문자 → 공백 제거.
String searchKey(String s) =>
    composeHangul(s).toLowerCase().replaceAll(RegExp(r'\s+'), '');

/// 문자열의 한글 음절을 초성으로 바꾼 문자열. 한글이 아닌 문자는 소문자로 그대로.
/// "맬러드 4468" → "ㅁㄹㄷ4468"
String initials(String s) {
  final buf = StringBuffer();
  for (final c in composeHangul(s).runes) {
    if (_isSyllable(c)) {
      buf.write(_choseong[(c - _sBase) ~/ (_vCount * _tCount)]);
    } else if (c == 0x20 || c == 0x09) {
      // 공백 무시
    } else {
      buf.write(String.fromCharCode(c).toLowerCase());
    }
  }
  return buf.toString();
}

/// 검색어가 초성만으로 이뤄졌는지 (예: "ㅁㄹㄷ"). 호환 자모 ㄱ(U+3131)~ㅎ(U+314E) 범위.
/// 빈 문자열은 false.
bool isChoseongQuery(String s) {
  final t = s.replaceAll(RegExp(r'\s+'), '');
  if (t.isEmpty) return false;
  for (final c in t.runes) {
    if (c < 0x3131 || c > 0x314E) return false;
  }
  return true;
}
