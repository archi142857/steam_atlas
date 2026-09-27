# Steam Atlas — 전 세계 증기기관차 아카이브

전 세계에서 운행했던 증기기관차를 모아 검색·비교·탐색하는 모바일 앱.
이 저장소는 **동작하는 뼈대**다. 데이터 스키마, 화면 구조, 상태 관리, 검증까지 자리를 잡아뒀고
그 위에 데이터와 사진을 얹으면 된다.

**버전 0.1.0** (`pubspec.yaml`, 첫 공개본). 본문과 `CHANGELOG.md` 에 보이는 v0.5 … v0.12 는 개발 중 붙인 **내부 작업 회차** 표시이고,
공개 버전은 0.1.0 부터 센다. 이 회차까지의 결과가 전부 0.1.0 에 들어 있다.

---

## 1. 지금 들어있는 것

| 항목 | 수량 |
|---|---|
| 기관차 | **76량** |
| 국가 | **16개국** |
| 시대 구분 | 6구간 (1804~현재) |
| 화면 | 5개 (홈·탐색·연표·지도·설정) + 상세 — 국가별 탭은 v0.9에서 뺌(탐색의 국가 필터와 중복) |
| 지도 | 오프라인 육지 폴리곤 177개국 / 10,281점 · 상하 제한 + 좌우 순환 (flutter_map 8) |
| 도색(livery) | 44종 · 전량 배정 |
| 실루엣(shape) | 10종 · 전량 배정 |
| 출처 확인 완료 | 76량 대조 완료 · 66량 확정 (`verified: true`) — `tools/verified.py` |
| 참고문헌 | 종합 5 · 국가별 42 · 기관차별 56량 (`tools/references.py`, 서적·논문·공식) |
| 중량 기준 표기 | 53량 (`weightBasis`) · 별명 분리 10량 (`nickname`) |
| 대표 명차 | 35량 (`iconic: true`) |

국가별: 🇬🇧 10 · 🇺🇸 10 · 🇩🇪 8 · 🇯🇵 8 · 🇰🇷 6 · 🇨🇳 5 · 🇫🇷 5 · 🇮🇳 4 · 🇿🇦 4 · 🇷🇺 4 · 🇦🇺 3 · 🇵🇱 3 · 🇨🇦 2 · 🇨🇭 2 · 🇦🇷 1 · 🇮🇹 1

---

## 2. 실행

### 코드 없이 먼저 보기
`preview/steam-atlas-preview.html` 를 브라우저로 열면 됩니다. 설치 필요 없음.
Flutter 앱과 같은 데이터·화면 구조를 그대로 담았고 검색·필터·국가탭·연표·지도·설정이 실제로 동작합니다.
설정 탭에서 라이트/다크를 바꿔볼 수 있습니다.

### Flutter 앱 실행

이 저장소에는 `lib/`, `assets/`, `test/` 만 들어 있습니다.
플랫폼 폴더(android/ios/web)는 한 번 만들어줘야 합니다.

```bash
cd steam_atlas
flutter create . --project-name steam_atlas   # 플랫폼 스캐폴딩 생성 (최초 1회)
flutter pub get
flutter run                                    # Flutter 3.32 이상 권장
flutter test                                   # 정합성 31개 + 지도 앱 연동 3개 + 지도 카메라 4개 + 클러스터 6개 + 비교 2개 (v0.10 이후 컴파일 미검증 — analyze 먼저)
```

> `flutter create .` 는 기존 `lib/`, `pubspec.yaml` 을 덮어쓰지 않습니다.

데이터를 고친 뒤에는 반드시 JSON을 다시 생성한다.

```bash
python3 tools/build_seed.py      # 기관차·국가 JSON
python3 tools/build_worldmap.py  # 육지 폴리곤 (국가 추가 시에만 다시 돌리면 됨)
python3 tools/build_preview.py   # HTML 프리뷰 (위 두 결과를 인라인)
```

---

## 3. 구조

```
lib/
├── main.dart                     진입점
├── app.dart                      MaterialApp + 하단 탭 셸
├── core/
│   ├── theme.dart                'Coal & Brass' 팔레트, 상태별 색
│   ├── format.dart               단위 표기 (— 처리 포함)
│   ├── hangul.dart               한글 검색 (자모 합치기·초성·공백 무시)
│   ├── map_geometry.dart         지도 카메라 규칙 — 세계가 세로로 꼭 맞는 최소 줌, 첫 화면 중심
│   ├── marker_cluster.dart       마커 클러스터링 — 웹 메르카토르 투영 + 화면 거리로 묶기 (순수 Dart)
│   └── place_maps.dart           지도 앱으로 열기 — 안드로이드 시스템 선택창 + 시설명 검색
├── models/
│   ├── locomotive.dart           Locomotive / Wheel / LocoSpecs / Era / Country
│   └── filter_query.dart         검색·필터·정렬 상태를 담는 불변 값
├── data/
│   ├── locomotive_repository.dart  로딩(교체 가능) + 질의/집계
│   └── world_map.dart              오프라인 육지 폴리곤 로더
├── state/
│   └── app_state.dart            ChangeNotifier — 전역 필터, 즐겨찾기, 비교 목록
├── screens/
│   ├── home_screen.dart          통계 → 대표 명차 → 시대 바로가기
│   ├── explore_screen.dart       검색 + 필터
│   ├── timeline_screen.dart      시대별 세로 연표
│   ├── map_screen.dart           세계 지도 (오프라인 폴리곤 + OSM 타일) — 상하 제한·좌우 순환
│   ├── settings_screen.dart      테마 전환·저장 관리·데이터 출처
│   ├── detail_screen.dart        상세 카드 (⇄ 비교 넣기)
│   └── compare_screen.dart       두 량 제원 대조 (v0.12)
└── widgets/
    ├── loco_card.dart            목록용 카드
    ├── country_flag.dart         국기 SVG 렌더링
    ├── filter_sheet.dart         공용 필터 시트
    └── whyte_diagram.dart        Whyte 표기 → 차륜 도식 (CustomPainter)

assets/flags/                     국기 SVG 16개 (flag-icons, MIT, 합계 12KB)
assets/map/world_110m.json        육지 폴리곤 (Natural Earth 110m, PD, 112KB)
```

### 두 량 비교 (v0.12)

- **넣는 곳은 상세 화면 하나.** 상세 오른쪽 위 ⇄ 버튼으로 넣고 뺀다(최대 2량, 셋째를 넣으면 먼저 넣은 것이 빠진다 —
  `AppState.toggleCompare`). 2량이 차면 스낵바의 '비교 보기'로 바로 간다. 탐색 목록 아래에는 알약이 떠서 진행 상태(1/2)를
  보여주고, 2량이면 누르면 비교 화면, 길게 누르면 비운다. 비교 목록은 저장하지 않는다(앱을 껐다 켜면 빈다) — 즐겨찾기와 달리
  '지금 보고 있는 두 량'이라 영속화할 이유가 없었다.
- **굵은 값이 큰 쪽.** 두 값이 모두 있을 때만 대조한다. **중량은 기준(`weightBasis`)이 같을 때만** — 기관차 단독 5 t 과
  기관차+탄수차 540 t 을 나란히 굵게 표시하면 비교가 아니라 오해다. 기준이 다르면 각 값 뒤에 기준을 적고 "직접 비교하지
  않습니다"를 붙인다 (`compare_screen.dart` `_CompareTable._rows`, 프리뷰 `compareRows`).
- 헤더의 '수치 확인 필요' 표시는 상세와 같은 `verified` 플래그다 — 대조가 끝나지 않은 값끼리의 비교라는 뜻.
- 프리뷰는 비교 시트를 상세 시트 **아래**에 그린다(`render()` 의 `html+cmp+det`). 비교에서 이름을 눌러 상세로 갔다가 ← 로
  돌아오는 흐름이 앱의 화면 스택과 같아진다.

### 도색 계열·생김새 필터 (v0.12)

- **도색은 44종을 그대로 칩으로 못 쓴다.** `tools/build_seed.py` 의 `livery_family` 가 기준색의 HLS 로 검정·회색·녹색·
  파랑·빨강·노랑 여섯 계열을 정해 JSON 의 `family` 로 넣는다(채도 0.18 미만은 무채색 → 밝기 0.35 로 검정/회색, 나머지는
  색상환 20°/70°/170°/260°). 앱(`LiveryFamily`)과 프리뷰(`LIVERY_FAMILIES`)는 계산하지 않고 값을 읽기만 한다.
  빌드 로그가 계열별 도색 이름을 찍으니 '그린'이 파랑에 들어가는 식의 어긋남은 거기서 잡는다(테스트도 있다).
- 생김새는 도식 카탈로그(`LocoShape`) 10종을 그대로 칩으로 쓴다 — 데이터에 실제로 쓰인 것만, 카탈로그 순서(대체로 시대순).
- 칩에는 량 수를 옅게 붙였다. 빈 결과를 미리 피하게.
- 필터 규칙은 `LocomotiveRepository.query` 와 프리뷰 `query()` 가 같다: 도색 계열은 도색 카탈로그를 거쳐 보고, 도색이 없는
  량은 어떤 계열에도 걸리지 않는다.

### 마커 클러스터링 (v0.12)

- **화면 픽셀 거리로 묶는다.** 유럽·일본처럼 몰린 곳은 축소하면 마커가 겹쳐 하나처럼 보였다. 이제 현재 줌에서
  28px(프리뷰 22px) 안에 드는 마커끼리 숫자 하나로 그린다 — `core/marker_cluster.dart` `clusterMarkers`, 프리뷰
  `clusterPoints`. 탐욕적·결정적(위→아래, 왼→오른 순으로 씨앗을 잡고 반지름 안을 전부 붙임)이라 격자 방식처럼 격자
  경계에서 갈라지지 않고, x 거리는 세계 한 벌 폭을 법으로 재서 경도 180° 근처도 이웃으로 본다. 위젯 없이 테스트한다
  (`test/marker_cluster_test.dart`). 앱은 `MapCamera.of(context)` 로 카메라가 움직일 때마다 마커 레이어만 다시 묶는다.
- **누르면 확대, 같은 자리면 목록.** 구성원이 화면의 60% 안에 들어오는 줌으로 간다(최소 +1). 같은 박물관처럼 좌표가
  같은 것들(요크 NRM 4량, 오미야 3량…)은 아무리 확대해도 안 풀리므로 — 화면에서 4px 도 안 벌어지거나 이미 최대 줌이면 —
  아래 시트에서 한 량을 고른다. 묶음 색은 구성원 상태가 전부 같으면 그 상태색, 섞이면 중립색.
- 선택된 량은 묶지 않고 항상 낱개로 맨 위에 그린다 — 아래 카드가 가리키는 마커가 숫자 속으로 사라지면 안 되니까.
- 프리뷰 최대 배율을 14 → 60 으로 올렸다(같은 도시 안의 시설이 갈라질 만큼). 110m 해안선이 각져 보이지만 프리뷰라 감수.

### 2색 도색 (v0.12)

- 도색은 여전히 **기준색 하나**(`LIVERIES`)로 정의하고, 둘째 색은 `tools/build_seed.py` 의 `LIVERY_ACCENTS` 에서 **부위**와
  함께 준다 — `boiler`(보일러 통), `cabTender`(운전실·탄수차·치마), `chimney`(굴뚝), `wheels`(바퀴 중심·주행부). JSON 의
  `livery.accent = {role, color, note}`. 앱은 `_WhytePainter.fillFor(role)`, 프리뷰는 `BA(role)` 이 그 부위만 둘째 색으로 채운다.
- 넣은 것 9종: CN 6060(검정 보일러), CPR 로열 허드슨(터스컨 레드 운전실·탄수차), 로켓호(흰 굴뚝), 그리고 빨간 주행부 —
  독일 국철 표준, DR 18 201, 소련 P36·표준 흑색, 중국철도 표준, PKP 표준. **확실한 것만** 넣었다. 띠·라이닝처럼 도식으로 못
  그리는 것(N&W J 의 터스컨 레드 띠, SP 데이라이트의 검정 지붕, LNER·GWR 라이닝)은 일부러 뺐다 — 반쯤 그린 고증은 틀린 고증이다.
- 상세 화면 '도색' 줄에 견본 둘과 "○○만 둘째 색 — 근거" 한 줄이 붙는다. CN 6060 의 도색 이름에 끼워 넣었던 부위 설명은
  데이터(`accent.note`)로 옮기고 이름을 `CN 올리브 그린·검정` 으로 줄였다.

### 궤간·정렬·칩 (v0.11)

- **표준궤보다 좁으면 전부 협궤다.** 1,067mm(일본 재래선·남아공 케이프궤간)도 협궤. 예전 칩의 '중간궤'는 없는 용어였다.
  칩은 표준궤가 아니면 mm 를 같이 적는다(`협궤 1,067`, `광궤 1,676`) — `Fmt.gaugeShort`, 프리뷰 `gaugeShort`.
  용도가 '협궤'인 형식은 궤간 칩이 같은 말을 하므로 용도 칩을 뺀다("협궤 협궤"가 나란히 서지 않게).
- **내림차순은 목록을 뒤집지 않는다.** 뒤집으면 값 없는 항목(—)이 맨 위로 온다. 비교 함수에 방향을 곱하고 값 없는 항목은
  어느 방향이든 맨 뒤 — `LocomotiveRepository._compare`, 프리뷰 `query()`.
- **참고문헌은 한 번만.** 형식 문헌에 있는 책이 나라 문헌에도 있으면(RCTS 형식사) 나라 쪽에서 뺀다 — `Reference.except`.
- **저장 아이콘은 북마크.** 프리뷰가 ☆를 쓰면 이름 옆 '대표 명차' ★와 헷갈린다. 앱과 같은 북마크 모양으로, 상세 헤더에도 있다.

### 도식은 항상 흰 판 위에 (v0.9)

기관차 그림(카드·연표·상세 히어로)은 테마와 상관없이 **흰 판(`DiagramPlate`, `AppTheme.plate`)** 위에 그린다.
판은 주어진 폭을 꽉 채우고 그림은 그 안에서 **가운데** 놓인다 — 로켓호·페니다렌처럼 짧은 형식이 왼쪽에 몰리지 않게.
다크 배경에서는 검정·진녹·진청 도색이 전부 묻혀 형식이 구분되지 않았다. 판이 항상 흰색이라 도색은
실제 색(라이트 팔레트 `body/line/edge`)을 그대로 쓰고, `*Dark` 값은 더 이상 그리기에 쓰지 않는다
(JSON 에는 남아 있다). 프리뷰도 `.plate` 로 같은 규칙.

**판 높이는 그림 높이다.** `DiagramPlate` 는 `height`(그림의 원래 높이)를 받는다. 폭만 꽉 채운 `Container` 안에 `FittedBox` 만 두면
폭에 맞춰 세로도 늘려 잡아(비율 보존) 짧은 형식일수록 판이 더 높아졌다. 폭·높이가 모두 정해진 `SizedBox` 안의 `FittedBox` 는
칸을 그대로 쓰고 그림이 칸보다 넓을 때만 줄인다(v0.11). 프리뷰의 연표 판은 `.tlsvg{display:block}` 이 `.plate` 의 flex 를 덮어써
왼쪽에 붙어 있었다 — `.tlsvg.plate` 에서 `display:flex` 를 다시 세운다.

### 설계상 중요한 세 가지

**① 필터가 하나다.** `FilterQuery` 값 하나를 탐색·연표·지도가 공유한다.
연표에서 "황금기 + 영국"을 걸고 지도 탭으로 넘어가면 그 조건이 그대로 지도에 적용된다.
화면마다 별도 필터 상태를 두지 않았기 때문에 새 화면을 추가해도 규칙이 갈라지지 않는다.

**② 데이터 소스가 갈아끼워진다.** `LocomotiveSource`는 인터페이스다.
지금은 `AssetLocomotiveSource`(번들 JSON)지만, 나중에 서버 API나 SQLite로 바꿔도
`load()` 구현만 교체하면 화면 코드는 그대로다.

**③ 사진 없이도 형식이 구분된다.** 저작권 문제로 사진 확보가 가장 오래 걸린다.
그동안 `WhyteDiagram`이 기관차 측면 도식을 그려서 고속형(큰 동륜 3축)과 견인형(작은 동륜 5축),
관절식·탱크식이 목록에서 한눈에 갈린다. 여기에 **도색**과 **생김새**까지 입혀서
가터 블루의 유선형 맬러드, 높은 굴뚝에 경사 실린더가 붙은 로켓호, 카우캐처를 단 빅보이가
각각 다른 그림으로 나온다. 사진이 붙으면 카드의 도식 자리를 썸네일로 바꾸면 된다.

#### 도식이 표현하는 것

| 요소 | 근거 |
|---|---|
| 선륜·종륜(작은 바퀴) / 동륜(큰 바퀴 + 크랭크 핀) | Whyte 표기의 첫·마지막 그룹 vs 가운데 |
| 엔진 유닛 분리 | 가라트 표기(`4-8-2+2-8-4`)의 `+` |
| 보일러 옆 물탱크 | 탱크식 접미사(`T`/`ST`) — 탄수차가 없는 이유 |
| 운전실 위치 | 텐더식은 뒤, 가라트는 가운데(보일러가 두 유닛 사이) |
| **탄수차** | `tenderAxles` 필드. 없으면 중량·연대로 추정 |
| **도색** | `livery` 필드 → `liveries` 팔레트의 색으로 차체를 칠한다 |
| **생김새** | `shape` 필드 → 굴뚝 높이·운전실·유선형 케이싱이 유형별로 달라진다 |

**폭 계산과 그리기가 같은 코드(`WhyteLayout`)를 쓴다.** 예전에는 폭을 어림잡아서
`4-8-8-4` 같은 긴 형식이 캔버스 밖으로 잘렸다. 지금은 레이아웃이 정확한 폭을 돌려주고,
카드·연표·상세 히어로 모두 `FittedBox(scaleDown)` 으로 감싸서 어느 화면에서도 잘리지 않는다.
테스트가 모든 데이터에 대해 '바퀴가 폭 안에 들어오는지'를 검사한다.

**탄수차는 형식마다 달랐다.** Whyte 표기에는 탄수차 정보가 없어서
`tools/build_seed.py` 에서 `tender=` 로 명시하고(현재 20량), 나머지는 중량·연대로 추정한다.
추정값이 쓰인 항목은 상세 화면에 "탄수차는 크기로 추정한 개략 표현입니다"라고 밝힌다.

#### 도색 (livery)

기관차마다 색을 따로 적지 않고 **팔레트(`liveries`)로 뽑아** `livery` id 로 참조한다.
같은 철도의 기관차가 자동으로 같은 색을 쓰고, 색을 고치면 한 곳만 고치면 된다.
현재 44종 · 76량 전량 배정됐다(검증 스크립트가 미지정·오타·미사용 항목을 잡는다).

팔레트 항목 하나에 색이 여섯 개 들어가는데, 역할이 셋이고 테마가 둘이기 때문이다.

| 역할 | 라이트 / 다크 | 쓰이는 곳 | 무엇과 대비돼야 하나 |
|---|---|---|---|
| `body` | `bodyDark` | 차체 채움 | 화면 배경 |
| `line` | `lineDark` | 바퀴·레일·연결기 | 화면 배경 |
| `edge` | `edgeDark` | 보일러·운전실·탄수차 윤곽 | **차체** |

`line` 과 `edge` 를 나눈 이유가 있다. 실제 도색의 8할은 검정에 가까운데, 차체와 윤곽선을
한 색으로 그리면 검은 기관차가 형태 없는 검은 덩어리가 된다. `edge` 는 차체 밝기의
반대쪽(어두우면 밝게, 밝으면 어둡게)으로 뽑으므로 어느 도색에서도 형태가 읽힌다.
다크 테마용 값은 배경(`#15171A`)에 묻히지 않도록 밝기를 끌어올리되 색상(hue)은 유지한다 —
'가터 블루는 파랗다'는 인상이 두 테마 모두에 남는다.

`tools/build_seed.py` 의 `LIVERIES` 에는 **기준색 하나만** 적고 나머지 다섯 색은
`livery_objs()` 가 HSL 로 계산한다. 테스트가 두 테마 모두에서 대비를 검사한다.

> 한 형식도 시기·소속에 따라 도색이 여러 번 바뀌었다. 데이터의 값은 그 형식을
> **대표하는 도색 하나**이며, 상세 화면에도 색 견본과 함께 이름을 밝혀둔다.

#### 생김새 (shape)

차륜 배치만 그리면 **1829년 로켓호와 1950년대 대형기가 똑같이 나온다.** 실제로는
굴뚝 높이, 운전실 유무, 유선형 케이싱 같은 게 멀리서 봐도 다르다.
그래서 '멀리서 봐도 다른' 특징만 골라 **9개 유형**으로 묶고 도식에 반영한다.

| 유형 | 굴뚝 | 운전실 | 특징 | 배정 |
|---|---|---|---|---|
| `beam` | 높음 | 없음 | 대형 플라이휠 | 페니다렌 1 |
| `rocket` | 높음 | 없음 | 경사 실린더 + 연결봉 | 로켓호 1 |
| `early` | 높음 | 없음 | 낮은 탄수차 | 2 |
| `victorian` | 높음 | 개방형 | 돔 1개 | 5 |
| `classic` | 보통 | 전운전실 | 증기·모래돔 2개 | 33 |
| `american` | 낮음 | 전운전실 | 전조등 + **카우캐처** | 11 |
| `headlamp` | 낮음 | 전운전실 | 전조등 (소련·중국 계열) | 9 |
| `semi` | 낮음 | 전운전실 | 앞머리·옆면 스커트 | 6 |
| `streamlined` | 없음 | 케이싱 안 | 통짜 유선형 껍데기 | 8 |

카우캐처는 차체보다 앞으로 튀어나오므로 `WhyteLayout` 이 앞자리(`frontPad`)를
미리 비워둔다. 자리를 안 잡으면 캔버스 밖으로 잘린다.

돔·전조등처럼 작은 요소는 `h >= 28` 에서만 그린다. 그보다 작으면 점으로 뭉개져서
오히려 지저분해진다(연표의 24px 도식은 차체까지만).

상세 화면 도식 아래에 유형 이름과 설명을 적어둔다 —
"로켓형 — 높은 굴뚝과 바깥으로 드러난 경사 실린더".

> 이것도 **근사**다. 같은 형식 안에서도 개체·시기별로 굴뚝과 운전실이 바뀌었다.
> 사진이 붙기 전까지 형식을 구분하기 위한 그림이지, 도면이 아니다.

### 국기와 테마

**국기는 번들 SVG다.** 이모지 국기(🇰🇷)는 플랫폼에 따라 아예 렌더링되지 않거나(윈도우)
모양이 제각각이라 `flag-icons`(MIT)의 SVG를 `assets/flags/`에 넣고 `flutter_svg`로 그린다.
16개국 합쳐 12KB. `CountryFlag(code: 'KR')` 하나로 어디서든 쓴다.
테스트가 국가 추가 시 에셋 누락과 외부 리소스 참조를 잡는다.

### 지도

**기본이 오프라인이다.** 레이어 순서는 `바다색 배경 → 오프라인 육지 폴리곤 → (선택) 타일 → 마커`.
온라인 타일은 설정에서 켜야 올라간다. 증기기관차를 보러 다니는 곳은 산간 보존철도처럼
신호가 약하기 마련이고, 공개 OSM 타일은 앱 프로덕션 트래픽에 쓸 수 없기 때문에
기본값을 오프라인으로 뒀다. 네트워크 요청이 0이라 개인정보 신고도 가장 단순해진다.

폴리곤 원본은 Natural Earth 110m(퍼블릭 도메인). `tools/build_worldmap.py`가
TopoJSON을 풀어서 0.1° 정밀도로 반올림하고 미세 섬을 걸러 112KB / 10,281점으로 줄인다.
프리뷰 HTML도 **같은 파일**을 쓴다 — 지도 모양이 앱과 프리뷰에서 갈리지 않는다.

투영은 웹 메르카토르. 메르카토르 y는 라디안으로 나오므로 `180/π`를 곱해
경도(도)와 축척을 맞춰야 한다. 안 그러면 지도가 납작하게 눌린다.

**180° 경계에서 링을 그냥 끊으면 안 된다.** 러시아처럼 날짜변경선을 넘는 나라는
조각이 닫힌 폴리곤으로 그려지면서 마지막 점과 첫 점을 잇는 선이 지도를 대각선으로
가로질렀다(캄차카에서 연해주로 줄이 그어졌다). 지금은 끊는 자리마다 ±180 위의
교차점을 보간해 넣고 링을 첫 교차 직후로 회전시켜, 모든 조각의 양 끝이 경계 위에
오도록 한다. 그러면 닫는 선이 경도 180° 선을 따라 지도 가장자리에 붙는다.

**상하는 막히고 좌우는 끝없이 돈다 (v0.10).** 지도 위아래로는 세계의 끝(±85.05°) 밖으로
나갈 수 없고, 좌우로는 경도 180°를 넘으면 반대편으로 이어진다.

| | Flutter 앱 (`map_screen.dart`) | 프리뷰 HTML |
|---|---|---|
| 상하 제한 | `CameraConstraint.containLatitude()` — 카메라 **가장자리**가 ±85.05° 안에 있어야 한다. 화면보다 세계가 작아지는 줌은 거부되므로 최소 줌을 `MapGeometry.worldFitZoom(높이)` = 세계 세로가 화면 높이에 꼭 맞는 값으로 둔다 | `clampPan` 이 `ty ∈ [H(1−z), 0]` 로 자른다. z=1 이면 0 고정 |
| 좌우 순환 | flutter_map 8 멀티 월드 — 타일·`PolygonLayer`(8.1+)·`MarkerLayer`(8.0+)가 옆 세계에도 그려진다. 따로 복제할 것 없음 | 세계 3벌(−1·0·+1)을 이어 붙이고 `tx` 를 세계 폭으로 나머지 연산. 땅·격자는 `<use>` 로 복제(경로 데이터 1벌), 마커는 클릭을 받아야 하므로 3벌 다 찍는다 |
| 첫 화면 | 최소 줌, 중심 (0°, 127.5°E) — 세계가 세로로 꽉 차고 한국이 가운데 | z=1, 중심 경도 127.5° (`MAP_HOME_LON`, 테스트가 앱 상수와 대조) |
| 회전 | 끔 (`InteractiveFlag.all & ~rotate`). 기울어진 화면에서는 위도 제한이 귀퉁이를 못 막는다 | 없음 |

최소 줌에서는 세로 위치가 하나뿐이라 상하로 전혀 안 움직이고 좌우로만 돈다 — 이게 의도한 화면이다.
`worldFitZoom` 은 0.001 만큼 더 확대해 둔다. 정확히 맞는 줌은 부동소수 오차로 `containLatitude` 가
거부해 지도가 굳을 수 있다. 프리뷰는 viewBox 세로를 지도 칸의 실제 높이로 맞춘 뒤(처음 한 번 재렌더)
같은 규칙을 적용한다 — 'meet' 여백이 있으면 위아래 끝 제한이 화면과 어긋난다.

flutter_map 은 이 기능 때문에 **8.x** 다 (Flutter 3.27+ / Dart 3.6+). 8.2 에서 공개 OSM 타일 URL 을
쓰면 디버그 콘솔에 경고가 찍히는데, 타일은 그대로 뜬다. `TileLayer` 에는 `backgroundColor` 가 없다
(배경은 `MapOptions.backgroundColor` 하나) — 타일이 안 온 자리에는 폴리곤 밑그림이 비친다.

**라이트가 기본이다.** 모든 레이아웃·여백·테두리는 라이트 기준으로 잡혀 있고, 다크는 변형이다.
- Flutter: `AppTheme.light()` 가 `theme:`, `AppTheme.dark()` 가 `darkTheme:`. 기본 `themeMode`는 `ThemeMode.light`
- 프리뷰 HTML: `:root` 가 라이트 팔레트, `.phone.dark` 가 덮어쓰는 변형

라이트가 기본이라 카드에는 테두리(`--hairline`)가 들어가고, 다크에서는 그 값이 `0`이 되어
배경 밝기 차이만으로 층을 구분한다. 흰 배경에서는 그림자보다 얇은 선이 깔끔하다.

**테마는 색 두 벌이 아니라 `ColorScheme` 한 벌씩이다.** 화면 코드에는 고정 색을 쓰지 않고
`scheme.primary` / `AppTheme.statusColor()` 만 참조한다. `statusColor` 가 `scheme.brightness` 를 보고
같은 색조를 라이트에서 어둡게 돌려주기 때문에 흰 배경에서도 보존 상태 색이 읽힌다.
새 화면을 만들 때 `AppTheme.brassLight` 같은 상수를 직접 쓰면 라이트에서 대비가 무너지니 주의.

### 지도 앱 연동

상세 화면의 '지금 있는 곳' 카드를 탭하면 **안드로이드 시스템의 "다음으로 열기" 선택창**이 뜨고,
고른 지도 앱이 그 시설을 **이름으로** 보여준다 (`lib/core/place_maps.dart`, `android_intent_plus`).
앱 안에 별도 목록 화면은 없다. 길게 누르면 좌표만 복사된다.

| 플랫폼 | 동작 |
|---|---|
| Android | `Intent.createChooser` 로 `geo:` 인텐트 — 기기에 깔린 지도 앱(Google 지도·네이버·TMap·…)이 시스템 창에 나열된다. **기본 앱이 정해져 있어도 매번 뜬다** (일반 `geo:` 인텐트로 열면 기본 앱으로 곧장 넘어가 고를 수 없다) |
| iOS | 시스템 선택창이 없으므로 Apple 지도(`maps://?ll=…&q=장소명`)로 바로. `ll` 과 함께 준 `q` 는 핀 라벨로 쓰인다 |
| 그 외 / 실패 | 브라우저 Google 지도 → 그것도 안 되면 좌표 복사 + 스낵바 |

어느 앱을 고르든 같은 `geo:` 주소가 넘어가므로 **주소 하나로 이름이 보이게** 만든다:

- 시설 공식 명칭(`location.query`)이 있으면 `geo:lat,lng?q=검색어` — 좌표 근처에서 그 이름을 검색해
  지도 앱이 가진 실제 장소(이름·주소·사진)를 연다. 검색어는 `tools/build_seed.py` 의 `MAP_QUERIES`
  (장소명 → 검색어, 71곳 중 56곳)에서 관리한다. 장소명과 안 맞는 키가 남으면 빌드가 실패한다.
- 검색어가 없는 곳('각지 보존' 등 특정 시설이 아닌 위치)은 `geo:0,0?q=lat,lng(라벨)` — 문서화된 라벨 형식.
  일부러 비운 것이다: 그런 좌표는 도시 중심일 뿐이라 검색어를 붙이면 엉뚱한 장소가 잡힌다.
- **좌표에 라벨을 붙이는 방식은 Google 지도가 라벨을 버리고 좌표(`54°37'48.0"N …`)만 보여주는 경우가 있어**
  실제 시설에는 쓰지 않는다. 라벨 파서가 쉼표·괄호를 잘못 다루는 앱이 있어 라벨에서는 빼고 넘긴다(`PlaceMaps.markerTitle`).

**플랫폼 설정.** `flutter create .` 로 만든 폴더에서:

- 안드로이드: 선택창(`createChooser`)은 시스템이 앱을 찾으므로 별도 선언이 없어도 뜬다. 웹 폴백용으로 `<queries>` 에 `https` 인텐트를 두는 것을 권한다:

```xml
<queries>
  <intent>
    <action android:name="android.intent.action.VIEW" />
    <data android:scheme="https" />
  </intent>
</queries>
```

- iOS: Apple 지도는 스킴 선언 없이 열린다. `Info.plist` 에 추가할 것 없음.

`android_intent_plus` 는 iOS 에서 호출하면 죽으므로 반드시 `defaultTargetPlatform == TargetPlatform.android` 안에서만 부른다 (코드가 그렇게 돼 있다).

---

## 4. 데이터 스키마

`assets/data/locomotives.json` (`schemaVersion: 1`)

```jsonc
{
  "id": "gb-lner-a4-mallard",       // 국가-철도-형식-이름
  "nameKo": "맬러드",
  "nameEn": "Mallard",
  "nickname": null,                  // 별명·애칭 (Kriegslok, 티거리…). 공인 형식명이 아닌 이름은 여기만
  "classDesignation": "LNER Class A4",
  "roadNumber": "4468",
  "countryCode": "GB",
  "era": "golden",                   // pioneer|expansion|classic|golden|twilight|revival
  "operators": ["LNER", "British Railways"],
  "builders": ["Doncaster Works"],
  "designer": "Nigel Gresley",
  "builtFrom": 1938, "builtTo": 1938,
  "quantityBuilt": 35,               // 형식 전체 생산량
  "withdrawnYear": 1963,
  "wheel": { "whyte": "4-6-2", "uic": "2'C1'h3", "typeName": "Pacific" },
  "tenderAxles": 4,                  // 탄수차 차축 수. null이면 추정, 0은 '없음'
  "livery": "lner-garter-blue",      // liveries 팔레트의 id
  "gaugeMm": 1435,
  "serviceType": "express",          // express|mixed|freight|tank|articulated|narrow|rack
  "specs": {
    "lengthMm": 21600, "weightT": 165.0,
    "weightBasis": "locoAndTender",  // loco(기관차 단독) | locoAndTender(기관차+탄수차) | null(미확인)
    "driverDiameterMm": 2032,
    "boilerPressureBar": 17.6, "cylinders": 3,
    "tractiveEffortKn": 156.0, "powerKw": 1640, "topSpeedKmh": 202.8
  },
  "status": "static",                // operational|operable|static|restoration|scrapped|replica
  "survivors": 6,
  "location": {
    "name": "국립철도박물관, 요크 (NRM York)", "lat": 53.9603, "lon": -1.0951,
    "query": "National Railway Museum York"   // 지도 앱 검색어(MAP_QUERIES). 특정 시설이 아니면 null
  },
  "iconic": true,
  "highlights": ["증기기관차 세계 최고속도 202.8 km/h (1938-07-03)"],
  "summary": "...",
  "tags": ["속도기록", "유선형", "명차"],
  "sources": ["https://..."],
  "references": [                    // 서적·논문·공식 자료 (tools/references.py). 웹 페이지는 sources 에
    { "kind": "book", "title": "Mallard: How the Blue Streak Broke the World Steam Speed Record",
      "author": "Don Hale", "publisher": "Aurum Press, London", "year": 2005, "lang": "en",
      "isbn": "9781854109392", "url": null, "note": "1938년 기록 주행의 전말", "via": "Stanford SearchWorks 서지" }
  ],
  "verified": true                   // 출처 대조를 마쳤는가
}
```

**`verified` 필드가 핵심이다.** 증기기관차 제원은 자료마다 값이 다르다(측정 조건, 개조 시점,
단위 환산 차이). 확인한 것과 아직 못 한 것을 구분해두지 않으면 나중에 어디를 다시 봐야 할지
알 수 없게 된다. 앱에서도 미확인 항목은 상세 화면에 "수치 확인 필요"로 표시된다.

### 값이 없으면 `null`
제원을 0이나 추정치로 채우지 않는다. UI가 `—`로 표시하고, 정렬에서는 뒤로 밀린다.

---

## 5. 데이터 추가하는 법

`tools/build_seed.py`의 `LOCOS` 리스트에 항목을 추가하고 다시 생성한다.

```python
loco("jp-c62", "C62형", "JNR Class C62",
     "JNR C62", "JP", "twilight", "4-6-4",
     no="C62 2", built=1948, builtTo=1949, qty=49,
     gauge=1067, service="express", speed=129, weight=145.2,
     livery="jnr-black", shape="classic", tender=4,
     status="static", survivors=3, iconic=True,
     highlights=["협궤 세계 최고속도 129 km/h (1954)"],
     summary="...", tags=["협궤", "고속"], verified=False,
     place="교토 철도박물관", lat=34.9870, lon=135.7370),
```

생성 시 자동 검증되는 규칙:

- id 중복
- `status` / `serviceType` / `era` / `countryCode` 유효값
- `builtTo >= builtFrom`, `withdrawnYear >= builtFrom`
- 제작연도가 지정한 시대 구간 안에 있는가 (±5년 허용)
- `scrapped`인데 현존 수량이 0보다 큰가 / 보존 위치가 붙어 있는가
- 좌표 범위, 동륜 직경 상식 범위
- 최고속도가 세계기록(202.8 km/h)을 넘는가
- 궤간이 알려진 값 목록에 있는가
- 탄수차 축수가 0~8 범위인가 / 탱크식·가라트인데 탄수차가 지정되지 않았는가
- `livery` 가 지정됐는가 / `LIVERIES` 에 실제로 있는 id 인가 / 쓰이지 않는 도색이 남았는가
- `shape` 가 지정됐는가 / `SHAPES` 에 실제로 있는 id 인가 / 쓰이지 않는 유형이 남았는가
- `serviceType=tank` 인데 Whyte 표기에 `T` 가 없는가 (탄수차가 조용히 그려지는 실수 방지)
- Whyte 에 `T` 가 있는데 `tender=` 가 0 이 아닌가 (예외: `TANK_WITH_TENDER` — 소형 탄수차를 실제로 끄는 페어리 퀸)
- `weightBasis` 유효값 / 중량이 없는데 기준만 적혔는가

JSON을 직접 손으로 고치지 말 것. 스키마가 조용히 어긋난다.

### 고증(출처 대조) 워크플로 — `tools/verified.py`

`LOCOS` 는 **초안**이다. 웹 출처로 직접 확인한 값은 `tools/verified.py` 의 `VERIFIED` 에
기관차 id 별로 `"필드.경로": 값` 형태로 적고, 반드시 `_why`(왜 이 값인지)와 `_src`(어디서 봤는지)를 남긴다.
빌드 때 초안 위에 덧씌워지고 `verified=true` 가 찍힌다. 출처끼리 충돌해 확정할 수 없으면 `_verified: False`.

```python
"kr-moga": {
    "wheel.whyte": "2-6-0T", "serviceType": "tank", "tenderAxles": 0,
    "_why": "모가형은 탄수차가 없는 탱크식. 초안이 탄수차식으로 잘못 그려졌었다.",
    "_src": [KO + "모가형_증기_기관차", EN + "Sentetsu_Mogai-class"],
},
```

값이 `None` 이면 "확인 불가 → 비움" 이다. 초안의 추정치보다 `—` 가 낫다.
빌드 뒤 `python3 tools/check_facts.py` 로 한 번 바로잡은 값이 다시 틀어지지 않았는지 확인한다.

```bash
python3 tools/build_seed.py && python3 tools/check_facts.py && python3 tools/build_preview.py
```

**단위를 본다 (v0.11 재대조).** 1차 대조는 숫자가 출처와 '같은가'만 봤고 단위를 보지 않았다. 영국 자료의 long ton(1.016 t)이
그대로 t 로 들어와 있었고(맬러드 165 → 실제 165 long tons = 167.6 t, 기관차 단독 104.6 t), 견인력은 lbf→kN 환산이 어긋난 값이
여럿 있었다. `VERIFIED` 뒤에 덧씌워지는 **`RECHECK`** 가 인포박스의 미터법 값을 그대로 옮긴 결과이고, 중량에는 반드시 기준
(`weightBasis`: 기관차 단독 / +탄수차)을 붙인다. 탄수차 축수는 탄수차 형식(2'2'T34 = 4축, EW1 = 3축 보기 2개…)이나
탄수차 중량÷축중(축당 20~28 t)으로 정했다 — 그림용 값이라 그 정도면 된다. 기준을 확인할 출처가 없는 4량(크램프턴·140 C·8620·9600)은
기준 없이 '중량'으로만 표시한다.

**시대(era)는 손으로 적지 않는다.** `build_seed.assign_eras()` 가 대조본 적용 후의 제작 시작 연도로 계산한다. 연표가 시대로 묶고
그 안에서 연도순으로 늘어놓기 때문에, 1918년 JF1 이 '1920–1945' 머리글 아래 서 있던 일이 다시 생기지 않게 검증도 여유 없이 정확히 본다.

### 참고문헌 — `tools/references.py`

(v0.12) `tools/export_references_md.py` 와 `tools/export_verified_md.py` 가 프로젝트 문서 `참고문헌.md`·`고증-대조-기록.md` 를 만든다 — 손으로 고치지 말고 원본을 고친 뒤 다시 생성한다.
뉴커먼 학회지 논문은 Crossref DOI 레코드(`api.crossref.org/works/<doi>`)로 서지를 확인해 `_tns()` 로 넣는다.

웹 페이지(`sources`)와 별개로 **서적·논문·공식 간행물**을 따로 둔다. 현지어 자료 우선: 한국은 철도청·국가유산청,
일본은 国鉄 백년사·NDL 소장 문헌, 독일은 EK/transpress 형식별 단행본, 프랑스는 Chapelon 원전, 폴란드는 WKŁ,
러시아는 Раков, 남아공은 Holland/Wardale, 중국은 中国铁道出版社 …

- `GENERAL` (여러 나라에 걸친 종합서) · `COUNTRY_REFS` (국가별 표준 문헌, 16개국 전부) · `LOCO_REFS` (기관차별)
- 항목마다 `via`(서지를 어디서 확인했는지 — NDL·국회도서관·SearchWorks·출판사·학술DB·위키 문헌목록)와
  `note`(무엇을 다루는지)를 적는다. **확인 못 한 연도는 `None` 으로 두고 그럴듯하게 채우지 않는다.**
- 문헌의 `url` 은 도서관 목록·출판사·학술DB·공식 페이지만. 위키·판매 사이트는 넣지 않는다(테스트가 막는다).
- 앱 상세 화면은 "이 형식을 다룬 문헌 → 이 나라 증기기관차 전반 → 종합서(접힘)" 순으로, 그 아래 "웹 출처".
- 정리본은 프로젝트 문서 `참고문헌.md` 에 국가별로 있다.

#### 검증 현황 (2026-09)

76량 전부 출처 대조를 마쳤고, 66량이 `verified=true`. 나머지 10량은 출처가 서로 다르거나
도색처럼 확인할 자료가 없어 `_verified: False` 로 남겨 앱에서 "확인 필요" 표시가 뜬다.

| 구분 | 내용 |
|---|---|
| 탱크식 ↔ 탄수차식 오류 정정 | 모가형 2-6-0T · JGR 150형 2-4-0T · 혀기8형 2-8-2T (초안이 모두 탄수차를 그리고 있었다) |
| 공인 형식명 ↔ 별명 분리 | 52형/Kriegslok · Pm36-2/아름다운 헬레나 · E 3/3/티거리 · 26형/레드 데블 · 파타고니아 2-8-2/라 트로치타 · P36/제너럴 · 44형/점보 · 10형/검은 백조 |
| 형식 이름 정정 | KD/KF형 → KF형 (KD 는 별개 형식) · PO 231 E → Nord 231 E · 크램프턴 → Est n° 80 «Le Continent» · DR 18.2 → DR 18 201 |
| 실루엣 정정 | NYC 허드슨(유선형 10/50량 → 일반형) · DRG 03.10(유선형 외장 철거 → 일반형) · C38 3801(개체 자체가 반유선형 → semi) |
| 도색 정정 | 로열 허드슨: 마룬 단색 → 회색 보일러 + 터스컨 레드 판넬 · 18 201: DR 그린 · NYC 허드슨: 검정 · GWR: 미들 크롬 그린 · 밀워키 A: 그레이 |
| 위치 정정 | KF7 은 런던 과학박물관이 아니라 요크 국립철도박물관 · GL 2351 은 조지 Outeniqua · 혀기8형 28호는 서울 국립어린이과학관 |
| 제원 정정(주요) | P36 실린더 3→2 · GL 동륜 1372→1219 · AA20 중량 209→140 · WP/WG 제원 · 25NC 137량 · QJ 4,717량 · 페어리 퀸 궤간 1,435→1,676 |
| 중량 기준 표기 | 53량에 `weightBasis` 부여. 기관차 단독인지 탄수차 포함인지 표시 없이 숫자만 두던 것을 정리 |

`_verified: False` 로 남은 10량: 미카3형 161호(제작연도 1939/1940 충돌), 터우형(하위 형식 총칭), 혀기8형(나무위키 의존),
C&O 앨러게이니(출력·중량 출처 상이), N&W Y6b(중량), 크램프턴(개체별 제원),
FS 685(하위 형식), SY형(도색 미확인 — 검정으로 두되 미확정), WP형(창고별 도색 상이), CN 6060(도색 미확인).

참고: `zh.wikipedia` · `commons.wikimedia` 는 이 작업 환경에서 접근이 막혀 있어 중국 기관차는 영어 위키·운영사 자료로 대조했다.

### 도색을 새로 추가할 때

`LIVERIES` 에 `(id, 한국어 이름, 영어 이름, 기준색)` 한 줄만 넣으면 된다.
나머지 다섯 색은 `livery_objs()` 가 계산한다.

```python
("nswgr-green", "NSWGR 그린", "NSWGR Green", "#1F5540"),
```

팔레트에 넣고 아무 기관차에도 배정하지 않으면 검증에서 걸린다 — 색만 늘어나는 걸 막기 위해서다.

### 국가를 새로 추가할 때

`COUNTRIES` 에 항목을 넣은 뒤 국기 SVG도 같이 넣어야 한다.

```bash
npm install flag-icons
cp node_modules/flag-icons/flags/4x3/<code>.svg assets/flags/
python3 tools/build_seed.py && python3 tools/build_preview.py
```

빠뜨리면 `flutter test` 의 '모든 국가에 국기 SVG 에셋이 있다' 가 실패한다.

---

## 6. 다음에 할 일

**데이터**
- [ ] `verified: false` 5량 — 자료끼리 어긋나 확정을 미룬 값들 (`tools/verified.py` 의 `_verified: False` 항목, 사유는 `_why`). 원전(제작사 도면·철도 연감)이 나오면 확정 (v0.12: 10 → 5)
- [ ] 사진 확보. Wikimedia Commons의 CC/PD 이미지부터. 라이선스·저작자 필드를 스키마에 추가해야 한다
- [ ] 국가 추가: 스페인, 브라질, 뉴질랜드, 인도네시아, 대만, 북한(가능한 범위)
- [ ] 북한 지역 보존 차량(파시2형 3호, 원산) 정보 확인

**기능**
- [x] 설정 탭 — 라이트/다크/시스템 전환 (기본 라이트)
- [x] 보존 위치 → 기기 지도 앱 연동
- [x] 즐겨찾기·테마 `shared_preferences` 영속화
- [x] 두 기관차 나란히 비교 — 상세 ⇄ 버튼 → 비교 화면, 중량은 기준이 같을 때만 대조 (v0.12)
- [x] 도색 계열·생김새 필터 — 도색 44종을 여섯 색 계열로 묶어 칩으로, 실루엣 10종 칩 (v0.12)
- [x] 오프라인 지도 폴백 (Natural Earth 벡터 밑그림)
- [x] 지도 상하 제한 + 좌우 순환 (v0.10, flutter_map 8)
- [x] 전 기능 재검토 — 연표 판 정렬·정렬 방향·궤간 용어·시대 자동 계산·참고문헌 중복 · 제원 단위 재대조 57건 (v0.11)
- [x] 마커 클러스터링 — 화면 거리로 묶고, 누르면 확대, 같은 자리면 목록 (v0.12)
- [ ] "오늘의 기관차" 위젯 / 알림
- [ ] 다국어 (한/영) — 모델에 이미 `nameKo`/`nameEn`이 분리돼 있다

**품질**
- [ ] 골든 테스트로 카드·상세 레이아웃 회귀 방지
- [ ] 데이터 100량 넘어가면 검색 인덱스를 isolate로 분리

---

## 7. 출시

실제 스토어 출시 절차·비용·리드타임과 이 프로젝트 고유의 차단 요인은 **[RELEASE.md](RELEASE.md)** 에 정리했다.
요약하면:

- 지도는 **기본이 오프라인**이다. 온라인 타일은 설정에서 켜야 동작하고, 그 옵션을 유지할 거라면
  출시 전에 `urlTemplate` 을 자체/상용 타일로 바꿔야 한다 (공개 OSM 타일은 앱 프로덕션 사용 불가)
- Play 개인 계정은 프로덕션 전 **테스터 12명 × 14일 연속** 비공개 테스트가 필요하다 (리드타임 최장)
- 사진은 Wikimedia Commons의 PD/CC만. 스키마에 `license`/`credit` 필드가 필요하다

## 8. 라이선스

- **코드** (`lib/`, `test/`, `tools/*.py`, HTML 뼈대) — MIT, `LICENSE`.
- **기관차 데이터·설명문·참고문헌 정리** (`assets/data/*.json`, `tools/build_seed.py`·`verified.py`·`references.py` 의 본문) — CC BY-SA 4.0, `LICENSE-DATA`.
  제원·연도 같은 사실 자체는 저작권 대상이 아니고, 선정·배열·요약문·대조 설명이 대상이다. 위키백과(CC BY-SA)를 참고했으므로 같은 조건으로 연다.
- **제3자 자료** — 국기 SVG flag-icons(MIT), 지도 폴리곤 Natural Earth(퍼블릭 도메인)·world-atlas(ISC), 선택 기능의 OSM 타일(ODbL): `THIRD_PARTY_NOTICES.md`.
  pub 패키지 라이선스는 앱 설정의 '오픈소스 라이선스'(`showLicensePage`)에 Flutter 가 모아 보여준다.

© 2026 이영표 (LEE YOUNGPYO, [@Archi142857](https://github.com/Archi142857))

## 9. 알아둘 것

- 지도는 OpenStreetMap 공개 타일을 쓴다. 실사용자가 늘면 OSM 타일 사용 정책상
  자체 타일 서버나 유료 타일(MapTiler, Stadia 등)로 옮겨야 한다.
  오프라인 밑그림(Natural Earth)은 퍼블릭 도메인이라 제약이 없다.
- 운행 상태(`operational`)는 계속 바뀐다. 보일러 검사 주기, 복원 일정에 따라 매년 달라지므로
  장기적으로는 원격 데이터 갱신 경로가 필요하다.
- 대한제국~일제강점기 한국 기관차의 형식명(모가·터우·파시·미카 등)은 자료 간 표기가 갈린다.
  `verified: true` 는 `tools/verified.py` 에서 출처(가능하면 현지어 자료·문헌)와 대조해 확정한 값이고,
  `false` 인 10량은 자료끼리 어긋나 값을 비워 두거나 사유를 적어 둔 것이다.
