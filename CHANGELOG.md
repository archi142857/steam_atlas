# Changelog

공개 버전은 [Semantic Versioning](https://semver.org/lang/ko/) 을 따른다. 0.x 는 초기 개발 단계 — 화면·데이터 스키마가 예고 없이 바뀔 수 있다.

## 0.1.0 — 2026-09-27 (첫 공개본)

### 데이터 · 고증
- 76량 / 16개국 / 6개 시대구간 / 도색 44종(2색 9종) / 실루엣 10종
- 76량 전부 출처 대조, 71량 확정(`verified`), 5량 '수치 확인 필요' — `tools/verified.py` (1차 `VERIFIED` + 재대조 `RECHECK`, 값마다 `_why`/`_src`)
- 단위 재대조 57건 + 2차 대조 10량: long ton → t, lbf → kN, psi·kgf/cm² → bar, 중량 기준(기관차 단독 / +탄수차) 76량 전부 표기
- 참고문헌 109건 — 종합 5 · 국가별 44 · 기관차별 66량. 서지를 확인한 것만(도서관 목록·출판사·Crossref DOI·공식 기록)
- 고증 회귀 검사 `tools/check_facts.py` (54개 고정값 + 전역 규칙)

### 화면 · 기능
- 홈 / 탐색(검색·필터·정렬) / 연표 / 지도 / 설정 + 상세 카드. 한글 검색은 NFD·공백·초성·IME 대응
- 차륜 도식: Whyte 표기 → `CustomPainter`, 도색·실루엣·커플링로드 고증, 항상 흰 판 위
- 지도: Natural Earth 오프라인 폴리곤 + (옵션) OSM 타일, 상하 제한·좌우 순환, 마커 클러스터링
- 지도 앱 연동: 안드로이드 시스템 선택창 + 시설명 검색, iOS Apple 지도, 폴백 브라우저/좌표 복사
- 두 량 비교 — 중량은 기준이 같을 때만 대조
- 도색 계열·생김새 필터, 2색 도색(보일러·운전실/탄수차·굴뚝·바퀴)
- 테마: 라이트 기본 + 다크, 즐겨찾기·설정 영속화
- 설치 없이 보는 프리뷰 `preview/steam-atlas-preview.html` (앱과 같은 데이터·규칙)
- 라이선스 명시: 코드 MIT(`LICENSE`), 데이터 CC BY-SA 4.0(`LICENSE-DATA`), 제3자 고지(`THIRD_PARTY_NOTICES.md`), 설정 화면 '오픈소스 라이선스' 페이지

### 알려진 제한
- **Flutter 코드는 지도 순환 작업 이후 컴파일 검증을 거치지 않았다** (작업 환경에서 SDK 다운로드 불가). `flutter analyze && flutter test` 를 먼저 돌릴 것. 프리뷰는 Playwright 로 회귀 검사를 마쳤다.
- 사진 없음. 미확정 5량(미카3-161 제작연도, 터우·혀기8형 자료, SY·WP 도색).
- `android/`·`ios/` 스캐폴딩은 저장소에 없다 — `flutter create .` 로 생성 (RELEASE.md).
