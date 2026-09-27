/// 하단 탭. 화면 점프에 인덱스를 직접 쓰지 않는다 — 탭을 빼거나 더할 때
/// 점프 대상이 어긋나는 것을 막는다. `IndexedStack` 순서와 같아야 한다.
///
/// 국가별 탭은 v0.9에서 뺐다: 탐색의 국가 필터와 하는 일이 같았다.
enum AppTab { home, explore, timeline, map, settings }
