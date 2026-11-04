# 자료조사 원고

`entries.json` 은 자료조사 세션이 쓴 76량 한영 원고의 사본이다. 손으로 고치지 않는다.

- 원본: `D:\프로젝트 폴더\코딩\Steam Atlas\자료조사\entries.json` (공유 폴더 `공유\자료조사\entries.json` 에 같은 판)
- 지금 판: 2026-10-23 (`generated`), schemaVersion 2
- 내용: 항목마다 이름·별명(한영), 표제란 값(`head`), 뜻풀이·본문·연혁(한영 문장 짝 + 출처 번호), 제원(미터법 값,
  원래 단위 원문 `orig`, 단서 `note`), 지금 있는 곳, 출처 목록, 더 읽을거리. 시대·나라 설명, 생김새 이름·설명, 태그 대응표.
- 근거 인용 원문(`evidence.json`), 정정안(`corrections.json`), 대조 보고서는 자료조사 폴더에만 있다.

## 앱에 들어가는 길

`tools/build_seed.py` 가 `tools/manuscript.py` 로 이 파일을 읽는다.

1. 초안(`LOCOS`) 위에 출처 대조본(`tools/verified.py`: VERIFIED → RECHECK → RESEARCH)을 덧씌운다.
2. 덧씌운 값이 원고의 표제란(`head`)·궤간·제원과 같은지 본다(`manuscript.check`). 다르면 빌드가 실패한다.
3. 원고가 정하는 칸(이름·별명·설명 글·제원 주석·새 제원·위치·출처·더 읽을거리·시대/나라/생김새 설명)을 합친다(`manuscript.merge`).

원래 단위(`orig`)는 출처 원문이라 화면에 그대로 쓰지 않는다. 수치와 단위만 뽑아 `specNotes.*.orig` 로 넣는다.
결과는 `python3 tools/manuscript.py` 로 볼 수 있고, 규칙으로 안 되는 것은 `ORIG_DISPLAY` 에 손으로 적었다.

## 새 판이 왔을 때

1. 이 파일을 새 판으로 덮어쓴다.
2. `python3 tools/build_seed.py` — 앱 값과 다른 칸이 목록으로 나온다.
3. 받아들일 값은 `tools/verified.py` 의 `RESEARCH` 에 이유·출처와 함께 옮기고, 받아들이지 않을 값은 공유 폴더 `메모\` 로 자료조사 쪽에 돌려보낸다.
4. `python3 tools/build_seed.py && python3 tools/check_facts.py && python3 tools/build_preview.py`
