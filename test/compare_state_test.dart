import 'package:flutter_test/flutter_test.dart';
import 'package:steam_atlas/state/app_state.dart';

void main() {
  group('비교 목록 (최대 2량)', () {
    test('넣기·빼기·회전', () {
      final app = AppState();
      var notified = 0;
      app.addListener(() => notified++);

      expect(app.toggleCompare('a'), isTrue);
      expect(app.compareIds, ['a']);
      expect(app.isCompared('a'), isTrue);

      expect(app.toggleCompare('b'), isTrue);
      expect(app.compareIds, ['a', 'b']);

      // 셋째를 넣으면 먼저 넣은 것이 빠진다.
      expect(app.toggleCompare('c'), isTrue);
      expect(app.compareIds, ['b', 'c']);
      expect(app.isCompared('a'), isFalse);

      // 이미 있는 것을 누르면 빠진다.
      expect(app.toggleCompare('b'), isFalse);
      expect(app.compareIds, ['c']);

      app.clearCompare();
      expect(app.compareIds, isEmpty);
      expect(notified, 5);

      // 비어 있을 때 비우기는 알리지 않는다.
      app.clearCompare();
      expect(notified, 5);
    });

    test('데이터가 없으면 compareLocos 는 빈 목록', () {
      final app = AppState()..toggleCompare('x');
      expect(app.compareLocos, isEmpty);
    });
  });
}
