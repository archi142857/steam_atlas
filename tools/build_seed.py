#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Atlas — 시드 데이터 생성기
assets/data/countries.json, assets/data/locomotives.json 을 생성한다.

데이터 추가/수정은 이 파일에서 하고 `python3 tools/build_seed.py` 로 다시 뽑는다.
(JSON을 직접 손으로 고치면 스키마가 어긋나기 쉬움)
"""
import colorsys, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # tools/verified.py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data")

# ─────────────────────────────────────────────────────────────
# 시대 구분 (era)
# ─────────────────────────────────────────────────────────────
ERAS = [
    {"id": "pioneer",   "ko": "개척기",      "en": "Pioneer",       "from": 1804, "to": 1839,
     "note": "트레비식의 첫 주행부터 로켓호까지. 증기기관차가 '가능한가'를 증명한 시기."},
    {"id": "expansion", "ko": "확장기",      "en": "Expansion",     "from": 1840, "to": 1879,
     "note": "철도망이 대륙 단위로 뻗어나가며 형식이 표준화되기 시작한 시기."},
    {"id": "classic",   "ko": "성숙기",      "en": "Classic",       "from": 1880, "to": 1919,
     "note": "과열기·복식팽창 등 열효율 기술이 자리잡고 대형 화물기가 등장."},
    {"id": "golden",    "ko": "황금기·유선형", "en": "Golden Age",    "from": 1920, "to": 1945,
     "note": "속도 경쟁과 유선형 디자인의 시대. 증기기관차 성능의 정점."},
    {"id": "twilight",  "ko": "황혼기",      "en": "Twilight",      "from": 1946, "to": 1979,
     "note": "디젤·전기에 밀려 퇴역이 시작되지만, 마지막 걸작들이 쏟아진 시기."},
    {"id": "revival",   "ko": "보존·신조",    "en": "Preservation",  "from": 1980, "to": 2100,
     "note": "동태보존, 복원, 그리고 신조(new build) 기관차의 시대."},
]

# ─────────────────────────────────────────────────────────────
# 국가 (countries)
# ─────────────────────────────────────────────────────────────
COUNTRIES = [
    ("GB", "영국",       "United Kingdom", "🇬🇧", 54.0, -2.0,
     "증기기관차가 태어난 나라. 1804년 트레비식의 첫 주행부터 1938년 맬러드의 세계 최고속도까지 모든 이정표가 여기서 시작됐다."),
    ("US", "미국",       "United States",  "🇺🇸", 39.5, -98.0,
     "대륙 횡단 규모가 만들어낸 거대 기관차의 나라. 관절식(articulated) 대형기의 극한을 밀어붙였다."),
    ("DE", "독일",       "Germany",        "🇩🇪", 51.0, 10.0,
     "표준화(Einheitsdampflok)와 공학적 완성도. 유선형 고속기와 전시 표준형 대량생산을 동시에 해냈다."),
    ("FR", "프랑스",     "France",         "🇫🇷", 46.5, 2.5,
     "샤플롱(André Chapelon)의 열역학적 개량으로 '가장 효율적인 증기기관차'를 만들어낸 나라."),
    ("JP", "일본",       "Japan",          "🇯🇵", 36.5, 138.0,
     "협궤(1067mm) 제약 안에서 정밀하게 다듬어진 형식들. 지금도 관광열차로 다수가 살아 움직인다."),
    ("KR", "한국",       "Korea",          "🇰🇷", 36.5, 127.8,
     "1899년 경인선 모가형으로 시작해 1967년 증기 운행 종료. 미국·일본식 형식명이 한글 음차로 남았다."),
    ("CN", "중국",       "China",          "🇨🇳", 35.0, 105.0,
     "세계에서 가장 늦게까지 증기기관차를 신조하고 운행한 나라. 2022년에야 정기 증기 화물이 멈췄다."),
    ("IN", "인도",       "India",          "🇮🇳", 22.0, 79.0,
     "광궤 대형기와 산악 협궤가 공존. 세계 최고령 현역 기관차 Fairy Queen이 있다."),
    ("ZA", "남아프리카", "South Africa",   "🇿🇦", -29.0, 24.5,
     "케이프 궤간(1067mm)에서 가라트(Garratt) 관절식이 가장 발달한 나라. 증기 개량의 마지막 실험장."),
    ("RU", "러시아·소련", "Russia / USSR",  "🇷🇺", 60.0, 90.0,
     "광궤(1520mm)의 여유로 대형 보일러를 얹은 기관차들. 4-14-4 같은 극단적 시도도 있었다."),
    ("PL", "폴란드",     "Poland",         "🇵🇱", 52.0, 19.5,
     "볼슈틴(Wolsztyn) 기관고 — 세계에서 유일하게 정기 여객열차를 증기로 끌던 곳."),
    ("AU", "호주",       "Australia",      "🇦🇺", -25.5, 134.0,
     "주(州)마다 궤간이 달랐던 나라. 영국식 설계에 현지 개량을 얹은 형식들이 많다."),
    ("CA", "캐나다",     "Canada",         "🇨🇦", 56.0, -106.0,
     "대륙 횡단 노선과 혹한. CPR 로열 허드슨 같은 장거리 여객기가 상징."),
    ("CH", "스위스",     "Switzerland",    "🇨🇭", 46.8, 8.2,
     "치차(rack) 등판 기관차의 본고장. 알프스 급구배를 증기로 오른다."),
    ("AR", "아르헨티나", "Argentina",      "🇦🇷", -38.0, -64.0,
     "파타고니아의 750mm 협궤 '라 트로치타'가 아직도 달린다."),
    ("IT", "이탈리아",   "Italy",          "🇮🇹", 42.8, 12.5,
     "카프로티 밸브기어 등 독자 기술. 남유럽 특유의 경량 고속기."),
]


def country_objs():
    return [
        {"code": c, "nameKo": ko, "nameEn": en, "flag": f,
         "lat": lat, "lon": lon, "blurb": blurb}
        for (c, ko, en, f, lat, lon, blurb) in COUNTRIES
    ]



# ─────────────────────────────────────────────────────────────
# 도색(livery)
#
# 색은 기관차마다 hex 를 박지 않고 '철도별 도색 이름'으로 관리한다.
# 같은 철도의 기관차가 같은 색을 쓰고, 상세 화면에 도색 이름을 보여줄 수 있다.
#
# 주의: 한 형식도 시기·소속에 따라 도색이 여러 번 바뀌었다.
#       여기 값은 그 형식을 대표하는(가장 널리 알려진) 도색 하나다.
#       (id, 한국어 이름, 영어 이름, 기준색)
# ─────────────────────────────────────────────────────────────
LIVERIES = [
    ("early-iron",           "초기 무도장 철",      "Bare Iron",             "#4A4640"),
    ("early-black",          "초기 흑색",          "Early Black",           "#2E2B28"),
    ("rocket-yellow",        "로켓 옐로",          "Rocket Yellow",         "#C9A227"),
    ("lner-garter-blue",     "LNER 가터 블루",     "LNER Garter Blue",      "#1E3A6E"),
    ("lner-apple-green",     "LNER 애플 그린",     "LNER Apple Green",      "#4E7A4A"),
    ("lms-crimson-lake",     "LMS 크림슨 레이크",   "LMS Crimson Lake",      "#7E2230"),
    ("gwr-middle-chrome",    "GWR 미들 크롬 그린",  "GWR Middle Chrome Green", "#14493A"),
    ("br-brunswick-green",   "BR 브런즈윅 그린",    "BR Brunswick Green",    "#1D4C3B"),
    ("br-black",             "BR 블랙",           "BR Lined Black",        "#2A2D33"),
    ("up-black",             "UP 블랙",           "Union Pacific Black",   "#2B2E34"),
    ("sp-daylight",          "SP 데이라이트",       "SP Daylight",           "#C4471B"),
    ("nw-tuxedo-black",      "N&W 턱시도 블랙",    "N&W Tuxedo Black",      "#24272C"),
    ("nw-black",             "N&W 화물 블랙",      "N&W Freight Black",     "#282A2F"),
    ("prr-brunswick-green",  "PRR 브런즈윅 그린",   "PRR Brunswick Green",   "#1F3A31"),
    ("nyc-black",            "NYC 블랙",          "New York Central Black", "#26292E"),
    ("milw-gray",            "밀워키 로드 그레이",   "Milwaukee Road Gray",   "#8E949C"),
    ("atsf-black",           "ATSF 블랙",         "Santa Fe Black",        "#26292E"),
    ("co-black",             "C&O 블랙",          "C&O Black",             "#282B31"),
    ("drg-black",            "독일 국철 블랙",      "German Railways Black", "#24262B"),
    ("drg-red",              "독일 고속기 레드",    "DRG Streamliner Red",   "#8E2226"),
    ("dr-green",             "동독 DR 그린",       "DR Chrome Oxide Green", "#2C5138"),
    ("adler-green",          "아들러 그린",        "Adler Green",           "#2F5A46"),
    ("sncf-green",           "SNCF 그린",         "SNCF Green",            "#2C5741"),
    ("sncf-black",           "SNCF 블랙",         "SNCF Black",            "#26292E"),
    ("est-green",            "동부철도 그린",       "Chemins de fer de l'Est Green", "#33604A"),
    ("jnr-black",            "일본 국철 블랙",      "Japanese Railways Black", "#23262A"),
    ("korail-black",         "한국철도 흑색",       "Korean Railway Black",  "#23262A"),
    ("cr-black",             "중국철도 블랙",       "China Railways Black",  "#24272C"),
    ("ir-green",             "인도 그린",          "Indian Railways Green", "#1F5540"),
    ("ir-red",               "인도 레드",          "Indian Railways Red",   "#8A2F26"),
    ("ir-black",             "인도 블랙",          "Indian Railways Black", "#26292E"),
    ("dhr-blue",             "다르질링 블루",       "DHR Blue",              "#1D4E7E"),
    ("sar-black",            "남아공 블랙",        "SAR Black",             "#26292E"),
    ("sar-red-devil",        "레드 데블 레드",      "Red Devil Red",         "#A8321F"),
    ("soviet-green",         "소련 그린",          "Soviet Green",          "#2E5741"),
    ("soviet-black",         "소련 블랙",          "Soviet Black",          "#24272C"),
    ("pkp-black",            "PKP 블랙",          "PKP Black",             "#24272C"),
    ("nswgr-green",          "NSWGR 그린",        "NSWGR Green",           "#1F5540"),
    ("vr-black",             "빅토리아 블랙",       "Victorian Railways Black", "#26292E"),
    # 로열 허드슨 표준 도색: 회색 보일러 + 검정 운전실·탄수차 + 터스컨 레드 판넬. 보일러가 지배색이라 회색 기준.
    ("cpr-royal-hudson",     "CPR 로열 허드슨 그레이·터스컨 레드", "CPR Royal Hudson Gray / Tuscan Red", "#75797F"),
    ("cn-green",             "CN 올리브 그린·검정", "Canadian National Olive Green / Black", "#1E4D3C"),
    ("sbb-black",            "스위스 블랙",        "Swiss Black",           "#24272C"),
    ("fcaf-black",           "파타고니아 블랙",     "Patagonian Black",      "#26292E"),
    ("fs-black",             "FS 블랙",           "Italian FS Black",      "#2C2E33"),
]


# ─────────────────────────────────────────────────────────────
# 실루엣 유형 (shape)
#
# 차륜 배치만으로는 로켓호와 현대 기관차가 똑같이 그려진다. 굴뚝 높이·운전실·
# 유선형 케이싱·실린더 배치처럼 '멀리서 봐도 다른' 특징을 유형으로 묶어 도식에 반영한다.
#
# chimney : tall(초기 굴뚝) | mid | short | none(유선형)
# cab     : none(운전실 없음) | open(개방형) | full(전운전실)
# domes   : 보일러 위 증기돔·모래돔 수 (0~2)
# casing  : none | half(부분 스커트) | full(전체 유선형)
# lamp    : 앞 전조등
# pilot   : 카우캐처(배장기)
# cylinder: 실린더 배치 — 로드(연결봉)를 어떻게 그릴지 결정한다
#     outside  실린더가 프레임 바깥. 실린더 블록 + 메인로드가 보인다 (대부분의 20세기 기관차)
#     inside   실린더가 프레임 사이. 옆에서는 안 보이고 커플링로드만 보인다 (초기 영국식)
#     angled   경사 실린더 — 로켓호
#     vertical 보일러 위 수직 실린더 — 로코모션 1호
#     beam     정치기관식. 플라이휠로 구동, 커플링로드가 없다 — 페니다렌
#
# 커플링로드(사이드로드)는 유형과 무관하게 **연결된 동륜이 2축 이상일 때** 그린다.
# 관절식·가라트는 엔진 유닛마다 로드가 따로 걸린다(하나로 이어지지 않는다).
# 동륜이 1축뿐인 단동륜기(로켓 0-2-2, 크램프턴 4-2-0)에는 커플링로드가 없다.
#
# (id, 한국어 이름, chimney, cab, domes, casing, lamp, pilot, cylinder, 설명)
# ─────────────────────────────────────────────────────────────
SHAPES = [
    ("beam", "초기 정치기관형", "tall", "none", 0, "none", False, False, "beam",
     "가로 보일러에 커다란 플라이휠 — 기어로 구동해 커플링로드가 없다"),
    ("rocket", "로켓형", "tall", "none", 0, "none", False, False, "angled",
     "높은 굴뚝과 바깥으로 드러난 경사 실린더. 동륜이 1축이라 커플링로드가 없다"),
    ("vertical", "수직 실린더형", "tall", "none", 0, "none", False, False, "vertical",
     "보일러 위에 선 실린더에서 동륜으로 곧장 내려오는 연결봉"),
    ("early", "초기 텐더형", "tall", "none", 0, "none", False, False, "inside",
     "실린더가 프레임 사이에 숨어 옆에서는 로드가 보이지 않는다"),
    ("victorian", "빅토리아형", "tall", "open", 1, "none", False, False, "outside",
     "높은 굴뚝 + 지붕만 있는 개방형 운전실"),
    ("classic", "표준형", "mid", "full", 2, "none", False, False, "outside",
     "전운전실과 증기돔·모래돔을 갖춘 20세기 표준 형태"),
    ("american", "미국형", "short", "full", 2, "none", True, True, "outside",
     "큰 전조등과 카우캐처, 굴뚝은 짧다"),
    ("headlamp", "대륙형", "short", "full", 2, "none", True, False, "outside",
     "앞면 전조등 — 소련·중국 계열의 특징"),
    ("semi", "부분 유선형", "short", "full", 1, "half", True, False, "outside",
     "앞머리와 옆면만 덮은 스커트"),
    ("streamlined", "유선형", "none", "full", 0, "full", False, False, "outside",
     "굴뚝까지 덮은 통짜 케이싱"),
]


def shape_objs():
    return [{
        "id": sid, "nameKo": ko, "chimney": ch, "cab": cab, "domes": domes,
        "casing": casing, "lamp": lamp, "pilot": pilot,
        "cylinder": cyl, "note": note,
    } for sid, ko, ch, cab, domes, casing, lamp, pilot, cyl, note in SHAPES]


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _to_hex(r, g, b):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v * 255))) for v in (r, g, b))


LIVERY_FAMILY_KO = {"black": "검정", "gray": "회색", "green": "녹색", "blue": "파랑", "red": "빨강", "yellow": "노랑"}

# 2색 도색 (v0.12). 첫 색(body)이 차체 대부분이고, 둘째 색은 정해진 한 부위에만 쓴다.
#   boiler    : 보일러 통 (운전실·치마·탄수차는 body)
#   cabTender : 운전실·탄수차·치마 (보일러는 body)
#   chimney   : 굴뚝
#   wheels    : 바퀴 중심·주행부
# 확실한 것만 넣는다 — 띠·라이닝처럼 도식으로 못 그리는 것(N&W J 의 터스컨 레드 띠, SP 데이라이트의 검정 지붕)은 뺐다.
LIVERY_ACCENTS = {
    "cn-green":         ("boiler",    "#23262A", "CN 6060 (U-1-f): 보일러·연실은 검정, 치마·운전실·탄수차가 올리브 그린"),
    "cpr-royal-hudson": ("cabTender", "#7A2E2A", "CPR 로열 허드슨 2860: 보일러 재킷 회색, 운전실·탄수차·치마는 터스컨 레드"),
    "rocket-yellow":    ("chimney",   "#F2EFE8", "로켓호(1829, 과학박물관 원형·복제): 노란 차체에 흰 굴뚝(검은 테)"),
    "drg-black":        ("wheels",    "#A3281E", "독일 국철 표준 도색: 검정 차체, 빨간 주행부·바퀴"),
    "dr-green":         ("wheels",    "#A3281E", "DR 18 201: 녹색 차체, 빨간 주행부·바퀴"),
    "soviet-green":     ("wheels",    "#A3281E", "P36: 녹색 차체(크림색 띠), 빨간 바퀴"),
    "soviet-black":     ("wheels",    "#A3281E", "소련 표준 도색: 검정 차체, 빨간 바퀴"),
    "cr-black":         ("wheels",    "#A3281E", "중국철도 표준 도색: 검정 차체, 빨간 바퀴 중심(흰 타이어)"),
    "pkp-black":        ("wheels",    "#A3281E", "PKP 표준 도색: 검정 차체, 빨간 주행부·바퀴"),
}


def livery_family(h, l, s):
    """도색의 색상 계열 — 탐색 필터 칩용 (v0.12).

    44종을 칩으로 다 늘어놓을 수는 없어서 기준색의 HLS 로 여섯 계열로 묶는다.
    채도가 낮으면 무채색(어두우면 검정, 아니면 회색), 아니면 색상환으로 나눈다.
    자주·보라 계열(260°~330°)은 해당 도색이 없어 빨강 쪽에 붙였다 — 생기면 계열을 추가할 것.
    """
    if s < 0.18:
        return "black" if l < 0.35 else "gray"
    deg = h * 360
    if deg < 20 or deg >= 260:
        return "red"
    if deg < 70:
        return "yellow"
    if deg < 170:
        return "green"
    return "blue"


def livery_objs():
    """기준색 하나에서 테마별 차체색·외곽선색·내부선색을 만들어낸다.

    색은 세 가지 역할로 나뉜다.
      body : 차체 채움색
      line : 바퀴·레일 등 **배경 위**에 긋는 선 — 배경과 대비돼야 한다
      edge : 보일러·운전실·탄수차 등 **차체 위**에 겹쳐 긋는 선 —
             차체와 대비돼야 한다. 그래서 차체가 어두우면 밝게, 밝으면 어둡게 뽑는다.
             (line 을 그대로 쓰면 검은 도색이 형태 없는 덩어리로 뭉개진다)

    다크 테마 배경(#15171A)에서 검은 도색이 사라지지 않도록 밝기를 끌어올린다.
    색상(hue)은 유지하므로 '가터 블루는 파랗다'는 인상이 두 테마 모두에서 남는다.
    """
    out = []
    for lid, ko, en, base in LIVERIES:
        h, l, s = colorsys.rgb_to_hls(*_hex_to_rgb(base))

        def edge_of(bl, bs):
            if bl < 0.45:
                return _to_hex(*colorsys.hls_to_rgb(h, min(0.92, bl + 0.30), bs * 0.55))
            return _to_hex(*colorsys.hls_to_rgb(h, max(0.05, bl - 0.30), bs * 0.85))

        light_body = base
        light_line = _to_hex(*colorsys.hls_to_rgb(h, max(0.06, l * 0.55), s))
        dl = max(l, 0.42)
        dark_body = _to_hex(*colorsys.hls_to_rgb(h, dl, s * 0.85))
        dark_line = _to_hex(*colorsys.hls_to_rgb(h, min(0.82, dl + 0.20), s * 0.7))
        obj = {
            "id": lid, "nameKo": ko, "nameEn": en, "family": livery_family(h, l, s),
            "body": light_body, "line": light_line, "edge": edge_of(l, s),
            "bodyDark": dark_body, "lineDark": dark_line,
            "edgeDark": edge_of(dl, s * 0.85),
        }
        if lid in LIVERY_ACCENTS:
            role, color, note = LIVERY_ACCENTS[lid]
            obj["accent"] = {"role": role, "color": color, "note": note}
        out.append(obj)
    # 계열 배정을 눈으로 확인할 수 있게 찍는다 — 이름과 계열이 어긋나면(예: '그린'이 파랑) 경계값을 손봐야 한다.
    by_fam = {}
    for o in out:
        by_fam.setdefault(o["family"], []).append(o["nameKo"])
    for fam, names in by_fam.items():
        print(f"  도색 계열 {LIVERY_FAMILY_KO[fam]}: {len(names)}종 — {', '.join(names)}")
    unknown = set(LIVERY_ACCENTS) - {o["id"] for o in out}
    if unknown:
        raise SystemExit(f"LIVERY_ACCENTS 에 없는 도색 id: {sorted(unknown)}")
    print(f"  2색 도색: {len(LIVERY_ACCENTS)}종 ({', '.join(sorted(LIVERY_ACCENTS))})")
    return out


# ─────────────────────────────────────────────────────────────
# 기관차 입력 헬퍼
# ─────────────────────────────────────────────────────────────
_ids = set()


def loco(id, nameKo, nameEn, cls, country, era, whyte, **kw):
    """필수 필드 + 선택 필드를 스키마 순서대로 정규화."""
    if id in _ids:
        raise ValueError(f"중복 id: {id}")
    _ids.add(id)
    d = {
        "id": id,
        "nameKo": nameKo,
        "nameEn": nameEn,
        # 별명·애칭. 공인 형식명이 아닌 이름(Kriegslok, 티거리, 아름다운 헬레나…)은 여기에만 쓴다.
        "nickname": kw.get("nickname"),
        "classDesignation": cls,
        "roadNumber": kw.get("no"),
        "countryCode": country,
        "era": era,
        "operators": kw.get("operators", []),
        "builders": kw.get("builders", []),
        "designer": kw.get("designer"),
        "builtFrom": kw.get("built"),
        "builtTo": kw.get("builtTo", kw.get("built")),
        "quantityBuilt": kw.get("qty"),
        "withdrawnYear": kw.get("withdrawn"),
        "wheel": {
            "whyte": whyte,
            "uic": kw.get("uic"),
            "typeName": kw.get("wheelName"),
        },
        "gaugeMm": kw.get("gauge", 1435),
        # 탄수차 차축 수. None 이면 앱이 크기·시대로 추정한다(도식용 근사).
        # 0 은 '탄수차 없음'(탱크식·가라트 등)을 명시하는 값.
        "tenderAxles": kw.get("tender"),
        # 도색 이름 (LIVERIES 의 id). 없으면 앱이 무채색 도식으로 그린다.
        "livery": kw.get("livery"),
        # 실루엣 유형 (SHAPES 의 id). 굴뚝·운전실·유선형 여부를 도식에 반영한다.
        "shape": kw.get("shape"),
        "serviceType": kw.get("service", "mixed"),
        "specs": {
            "lengthMm": kw.get("length"),
            "weightT": kw.get("weight"),
            # 중량 기준: "loco"(기관차 단독) | "locoAndTender"(기관차+탄수차). 모르면 None.
            "weightBasis": kw.get("weightBasis"),
            "driverDiameterMm": kw.get("driver"),
            "boilerPressureBar": kw.get("pressure"),
            "cylinders": kw.get("cyl"),
            "tractiveEffortKn": kw.get("te"),
            "powerKw": kw.get("power"),
            "topSpeedKmh": kw.get("speed"),
        },
        "status": kw.get("status", "static"),
        "survivors": kw.get("survivors"),
        # query 는 지도 앱 검색어(MAP_QUERIES). 빌드 마지막에 장소명으로 채운다.
        "location": ({"name": kw["place"], "lat": kw["lat"], "lon": kw["lon"], "query": None}
                     if kw.get("place") else None),
        "iconic": kw.get("iconic", False),
        "highlights": kw.get("highlights", []),
        "summary": kw.get("summary", ""),
        "tags": kw.get("tags", []),
        "sources": kw.get("sources", []),
        "verified": kw.get("verified", False),
    }
    return d


# ─────────────────────────────────────────────────────────────
# 지도 앱 검색어 (location.query)
#
# 좌표에 라벨을 붙이는 방식은 지도 앱마다 다르게 다뤄지고(Google 지도는 라벨을 버리고 좌표만
# 보여주기도 한다), 우리 장소명은 한국어라 검색어로 쓰기엔 어색하다. 그래서 실제 시설(박물관·
# 기관고·역)이 있는 곳은 **그 지도 앱이 알아듣는 공식 명칭**을 따로 둔다. 지도 앱은 이 검색어로
# 실제 장소(주소·사진·운영시간까지)를 찾아 보여준다.
#
# '각지 보존', '특별열차 운행' 처럼 특정 시설이 아닌 곳은 검색어를 두지 않는다 — 그런 곳의 좌표는
# 도시 중심일 뿐이라 검색어를 붙이면 엉뚱한 장소가 잡힌다. 그 경우 앱은 좌표 핀 + 라벨로 연다.
#
# 키는 place 문자열 그대로(verified.py 에서 덮어쓴 이름 포함). 안 쓰이는 키가 남으면 빌드가 실패한다.
# ─────────────────────────────────────────────────────────────
MAP_QUERIES = {
    # 영국
    "복제품: 웨일스 국립박물관, 카디프": "National Museum Cardiff",
    "Locomotion, 실던": "Locomotion Shildon",
    "과학박물관, 런던 (Science Museum)": "Science Museum London",
    "국립철도박물관, 요크 (NRM York)": "National Railway Museum York",
    "국립철도박물관, 요크 (NRM York) — KF7": "National Railway Museum York",
    "STEAM 박물관, 스윈던": "STEAM Museum of the Great Western Railway",
    "다수 보존 철도 (예: 세번 밸리)": "Severn Valley Railway",
    "달링턴 기관차 공장 / 본선 운행": "Darlington Locomotive Works",
    # 미국
    "유니언 퍼시픽 증기기관고, 샤이엔 (WY)": "Union Pacific Steam Shop Cheyenne",
    "버지니아 교통박물관, 로어노크": "Virginia Museum of Transportation",
    "오리건 철도유산센터, 포틀랜드": "Oregon Rail Heritage Center",
    "펜실베이니아 철도박물관, 스트라스버그": "Railroad Museum of Pennsylvania",
    "헨리 포드 박물관, 디어본 (MI)": "Henry Ford Museum of American Innovation",
    "San Bernardino History & Railroad Museum (CA)": "San Bernardino History and Railroad Museum",
    "미국 국립교통박물관, 세인트루이스": "National Museum of Transportation St. Louis",
    # 독일
    "DB 박물관, 뉘른베르크": "DB Museum Nürnberg",
    "05 001: DB 박물관, 뉘른베르크": "DB Museum Nürnberg",
    "다수 보존 (예: DB 박물관 / 각 보존회)": "DB Museum Nürnberg",
    "교통박물관, 드레스덴": "Verkehrsmuseum Dresden",
    "Deutsches Dampflokomotiv-Museum, 노이엔마르크트": "Deutsches Dampflokomotiv-Museum Neuenmarkt",
    # 프랑스
    "Cité du Train, 뮐루즈 / 르 크뢰조": "Cité du Train Mulhouse",
    "Cité du Train, 뮐루즈": "Cité du Train Mulhouse",
    "Cité du Train, 뮐루즈 — 231 E 22": "Cité du Train Mulhouse",
    # 일본
    "철도박물관, 오미야": "鉄道博物館 さいたま市",
    "교토 철도박물관": "京都鉄道博物館",
    "오이가와 철도 (시즈오카)": "大井川鐵道 新金谷駅",
    # 한국
    "모형: 인천역 한국철도 탄생역 기념비": "인천역",
    "국립대전현충원 호국철도기념관": "국립대전현충원",
    "철도박물관 옥외전시장, 의왕": "철도박물관 의왕",
    "철도박물관, 의왕": "철도박물관 의왕",
    "국립어린이과학관 야외 전시, 서울 종로 — 혀기8형 28호": "국립어린이과학관",
    # 중국
    "중국철도박물관, 베이징": "中国铁道博物馆 东郊馆",
    # 인도
    "레와리 증기기관고 / 국립철도박물관, 뉴델리": "Rewari Railway Heritage Museum",
    "다르질링 히말라야 철도, 서벵골": "Darjeeling Railway Station",
    "국립철도박물관, 뉴델리": "National Rail Museum New Delhi",
    # 남아프리카
    "Outeniqua 교통박물관, 조지 — 2351 'Princess Alice'": "Outeniqua Transport Museum",
    "Reefsteamers, 크루거스도르프 (요하네스버그 근교)": "Reefsteamers Krugersdorp",
    # 러시아 · 폴란드
    "러시아 철도박물관, 상트페테르부르크": "Музей железных дорог России",
    "볼슈틴 기관고 (Parowozownia Wolsztyn)": "Parowozownia Wolsztyn",
    "볼슈틴 기관고": "Parowozownia Wolsztyn",
    # 호주 · 캐나다
    "NSW 철도박물관, 설미어": "NSW Rail Museum Thirlmere",
    "퍼핑 빌리 철도, 벨그레이브": "Puffing Billy Railway Belgrave",
    "Railway Museum of British Columbia (WCRA), 스쿼미시": "Railway Museum of British Columbia",
    "Alberta Prairie Railway, 스테틀러 (앨버타)": "Alberta Prairie Railway Excursions",
    # 스위스 · 아르헨티나 · 이탈리아
    "Dampfbahn Furka-Bergstrecke, 레알프": "Dampfbahn Furka-Bergstrecke Realp",
    "에스켈, 추부트주": "La Trochita Esquel",
    "피에트라르사 국립철도박물관, 나폴리": "Museo Nazionale Ferroviario di Pietrarsa",
}


def apply_map_queries(locos):
    """장소명 → 지도 앱 검색어. 안 쓰인 키는 오타이므로 오류로 돌려준다."""
    used = set()
    for l in locos:
        loc = l["location"]
        if not loc:
            continue
        q = MAP_QUERIES.get(loc["name"])
        loc["query"] = q
        if q:
            used.add(loc["name"])
    return sorted(set(MAP_QUERIES) - used)


NRM = dict(place="국립철도박물관, 요크 (NRM York)", lat=53.9603, lon=-1.0951)
SCIMUS = dict(place="과학박물관, 런던 (Science Museum)", lat=51.4978, lon=-0.1746)
SHILDON = dict(place="Locomotion, 실던", lat=54.6300, lon=-1.6480)

LOCOS = []
LOCOS += [
    # ── 영국 ────────────────────────────────────────────────
    loco("gb-trevithick-pendarren",  "페니다렌 기관차", "Penydarren Locomotive",
         "Trevithick Penydarren", "GB", "pioneer", "0-4-0",
         no=None, built=1804, qty=1, designer="Richard Trevithick",
         builders=["Penydarren Ironworks"], operators=["Penydarren Tramroad"],
         gauge=1219, service="freight", speed=8, iconic=True, status="replica",
         highlights=["세계 최초로 궤도 위를 달린 증기기관차 (1804-02-21)"],
         summary="철 10톤과 사람 70명을 싣고 페니다렌 제철소에서 아버시넌까지 약 16km를 달렸다. "
                 "상업적으로는 실패했지만 '레일 위의 증기'가 성립한다는 것을 증명한 출발점.",
         tags=["최초", "이정표"], verified=True,
         sources=["https://www.sciencemuseum.org.uk/"],
         **{"place": "복제품: 웨일스 국립박물관, 카디프", "lat": 51.4860, "lon": -3.1780}, tender=0, livery="early-iron", shape="beam"),

    loco("gb-locomotion-1",  "로코모션 1호", "Locomotion No. 1",
         "Stockton & Darlington", "GB", "pioneer", "0-4-0",
         no="1", built=1825, qty=1, designer="George Stephenson",
         builders=["Robert Stephenson and Company"], operators=["Stockton & Darlington Railway"],
         service="mixed", weight=6.5, speed=24, iconic=True, status="static", survivors=1,
         highlights=["세계 최초의 공공 증기철도 개통 열차를 견인 (1825-09-27)"],
         summary="스톡턴~달링턴 개통일에 승객 450여 명을 태운 열차를 끌었다. "
                 "증기기관차가 '광산 설비'에서 '공공 교통'으로 넘어온 순간.",
         tags=["최초", "이정표"], verified=True,
         **{"place": "Locomotion, 실던", "lat": 54.6300, "lon": -1.6480}, tender=2, livery="early-black", shape="vertical"),

    loco("gb-rocket",  "로켓호", "Stephenson's Rocket",
         "Rocket", "GB", "pioneer", "0-2-2",
         built=1829, qty=1, designer="Robert Stephenson",
         builders=["Robert Stephenson and Company"], operators=["Liverpool & Manchester Railway"],
         service="express", weight=4.3, driver=1435, pressure=3.4, cyl=2, speed=48,
         iconic=True, status="static", survivors=1, withdrawn=1862,
         highlights=["레인힐 트라이얼 우승 (1829)", "다관식 보일러 + 배기 유도 통풍의 원형을 확립"],
         summary="이후 100년 넘게 이어지는 증기기관차 설계 문법 — 다관식 보일러, 실린더 직결 구동, "
                 "배기증기를 이용한 통풍 — 을 하나로 묶어낸 기관차. 사실상 모든 후속 기관차의 조상.",
         tags=["최초", "이정표", "설계원형"], verified=True, **SCIMUS, tender=2, livery="rocket-yellow", shape="rocket"),

    loco("gb-lner-a4-mallard",  "맬러드", "Mallard",
         "LNER Class A4", "GB", "golden", "4-6-2",
         no="4468", built=1938, qty=35, designer="Nigel Gresley",
         builders=["Doncaster Works"], operators=["LNER", "British Railways"],
         uic="2'C1'h3", wheelName="Pacific", service="express",
         length=21600, weight=165.0, driver=2032, pressure=17.6, cyl=3,
         te=156.0, power=1640, speed=202.8,
         withdrawn=1963, status="static", survivors=6, iconic=True,
         highlights=["증기기관차 세계 최고속도 202.8 km/h (1938-07-03, 스토크 뱅크)",
                     "기네스 공인 기록 — 이후 88년간 깨지지 않음"],
         summary="그레슬리가 설계한 유선형 A4형의 4번째 기관차. 243톤 객차 7량을 달고 스토크 뱅크 내리막에서 "
                 "126 mph를 찍었다. 기록 직후 중앙 빅엔드가 과열돼 견인을 중단했을 만큼 한계에 가까운 주행이었다.",
         tags=["속도기록", "유선형", "명차"], verified=True,
         sources=["https://www.guinnessworldrecords.com/world-records/62943-fastest-steam-locomotive"],
         **NRM, tender=4, livery="lner-garter-blue", shape="streamlined"),

    loco("gb-lner-a3-flyingscotsman",  "플라잉 스코츠맨", "Flying Scotsman",
         "LNER Class A3", "GB", "golden", "4-6-2",
         no="60103", built=1923, qty=79, designer="Nigel Gresley",
         builders=["Doncaster Works"], operators=["LNER", "British Railways"],
         uic="2'C1'h3", wheelName="Pacific", service="express",
         weight=157.0, driver=2032, pressure=15.5, cyl=3, te=131.0, speed=160,
         withdrawn=1963, status="operational", survivors=1, iconic=True,
         highlights=["공식 기록상 최초로 100 mph(161 km/h)를 달성한 기관차 (1934)",
                     "런던~에든버러 무정차 주행 (1928)"],
         summary="세계에서 가장 유명한 증기기관차. 은퇴 후에도 호주·미국을 순회했고 지금도 영국 본선에서 "
                 "특별열차를 끈다. 보일러 검사 주기마다 운행 여부가 갈리므로 최신 상태 확인이 필요하다.",
         tags=["명차", "동태보존", "아이콘"], verified=True, **NRM, tender=4, livery="lner-apple-green", shape="classic"),

    loco("gb-lms-duchess",  "프린세스 코로네이션급", "Princess Coronation Class",
         "LMS Princess Coronation", "GB", "golden", "4-6-2",
         no="6229 Duchess of Hamilton", built=1937, builtTo=1948, qty=38,
         designer="William Stanier", builders=["Crewe Works"], operators=["LMS", "British Railways"],
         uic="2'C1'h4", wheelName="Pacific", service="express",
         weight=161.0, driver=2057, pressure=17.2, cyl=4, te=180.0, power=1900, speed=183,
         withdrawn=1964, status="static", survivors=3, iconic=True,
         highlights=["영국에서 가장 강력한 여객용 증기기관차", "1937년 시운전에서 114 mph 기록"],
         summary="A4와 함께 영국 유선형 시대의 쌍벽. 4기통 배치로 출력에서는 A4를 앞섰다. "
                 "6229호는 유선형 외피가 복원되어 요크에 전시 중.",
         tags=["명차", "유선형"], verified=False, **NRM, tender=4, livery="lms-crimson-lake", shape="streamlined"),

    loco("gb-gwr-king",  "킹급", "King Class",
         "GWR 6000 Class", "GB", "golden", "4-6-0",
         no="6000 King George V", built=1927, builtTo=1930, qty=30,
         designer="Charles Collett", builders=["Swindon Works"], operators=["GWR", "British Railways"],
         wheelName="Ten-wheeler", service="express",
         weight=136.0, driver=1969, pressure=17.2, cyl=4, te=178.0, speed=175,
         withdrawn=1962, status="static", survivors=3,
         highlights=["1927년 미국 B&O 100주년 기념행사에 초청되어 순회"],
         summary="GWR 표준 설계의 정점. 4기통 4-6-0이라는 GWR 특유의 문법으로 대형 퍼시픽 없이도 "
                 "최고 등급 급행을 감당했다.",
         tags=["명차"], verified=False,
         **{"place": "STEAM 박물관, 스윈던", "lat": 51.5620, "lon": -1.7940}, tender=3, livery="gwr-middle-chrome", shape="classic"),

    loco("gb-lms-black5",  "블랙 파이브", "Black Five",
         "LMS Stanier Class 5", "GB", "golden", "4-6-0",
         built=1934, builtTo=1951, qty=842, designer="William Stanier",
         builders=["Crewe Works", "Armstrong Whitworth", "Vulcan Foundry"],
         operators=["LMS", "British Railways"], service="mixed",
         weight=126.0, driver=1829, pressure=15.5, cyl=2, te=115.0, speed=145,
         withdrawn=1968, status="operational", survivors=18,
         highlights=["842량 생산 — 영국 혼합용 기관차의 표준", "1968년 영국 본선 증기 종운까지 살아남음"],
         summary="화려하진 않지만 어디든 갈 수 있고 무엇이든 끌 수 있던 만능기. 보존 철도에서 가장 흔히 "
                 "볼 수 있는 영국 기관차이기도 하다.",
         tags=["대량생산", "실용기"], verified=False,
         **{"place": "다수 보존 철도 (예: 세번 밸리)", "lat": 52.3760, "lon": -2.3480}, tender=3, livery="br-black", shape="classic"),

    loco("gb-br-britannia",  "브리타니아", "Britannia",
         "BR Standard Class 7", "GB", "twilight", "4-6-2",
         no="70000", built=1951, qty=55, designer="Robert Riddles",
         builders=["Crewe Works"], operators=["British Railways"],
         wheelName="Pacific", service="express",
         weight=142.0, driver=1880, pressure=17.2, cyl=2, te=145.0, speed=160,
         withdrawn=1968, status="operational", survivors=2,
         highlights=["영국국철 표준형(BR Standard) 시리즈의 첫 기관차"],
         summary="국유화 이후 정비 편의와 부품 공통화를 최우선으로 다시 그린 표준 설계. "
                 "증기의 마지막 세대이면서 가장 합리적인 세대이기도 했다.",
         tags=["표준형"], verified=False, **SHILDON, tender=4, livery="br-brunswick-green", shape="classic"),

    loco("gb-a1-tornado",  "토네이도", "Tornado",
         "LNER Peppercorn Class A1", "GB", "revival", "4-6-2",
         no="60163", built=2008, qty=1, designer="Arthur Peppercorn (설계) / A1 Trust (신조)",
         builders=["Darlington Locomotive Works"], operators=["A1 Steam Locomotive Trust"],
         wheelName="Pacific", service="express",
         weight=167.0, driver=2032, pressure=17.2, cyl=3, te=168.0, speed=160,
         status="operational", survivors=1, iconic=True,
         highlights=["1960년 이후 영국에서 처음 새로 만들어진 본선 증기기관차",
                     "2017년 본선 시험에서 100 mph 인가 주행"],
         summary="원형 A1형은 49량 전부 해체돼 한 량도 남지 않았다. 그래서 아예 새로 만들었다. "
                 "18년의 모금과 제작 끝에 2008년 완성 — 보존이 아니라 '재창조'의 사례.",
         tags=["신조", "명차"], verified=True,
         **{"place": "달링턴 기관차 공장 / 본선 운행", "lat": 54.5290, "lon": -1.5490}, tender=4, livery="lner-apple-green", shape="classic"),
]

LOCOS += [
    # ── 미국 ────────────────────────────────────────────────
    loco("us-up-bigboy-4014",  "빅보이", "Big Boy",
         "Union Pacific Class 4000", "US", "golden", "4-8-8-4",
         no="4014", built=1941, builtTo=1944, qty=25, designer="Otto Jabelmann",
         builders=["American Locomotive Company (ALCO)"], operators=["Union Pacific"],
         uic="(2'D)D2'", wheelName="Big Boy", service="articulated",
         length=40470, weight=548.0, driver=1727, pressure=20.0, cyl=4,
         te=602.0, power=4700, speed=129,
         withdrawn=1962, status="operational", survivors=8, iconic=True,
         highlights=["현존 최대의 운행 가능한 증기기관차", "2019년 복원 후 재운행",
                     "2026년 미국 건국 250주년 대륙횡단 투어 — 4-8-8-4로서 최초로 시카고 동쪽 운행"],
         summary="와사치 산맥의 1.14% 구배에서 3,600톤 화물을 보조기 없이 끌기 위해 만들어진 관절식 괴물. "
                 "25량 중 8량이 남았고 그중 4014호만 살아 움직인다.",
         tags=["최대", "관절식", "명차", "동태보존"], verified=True,
         sources=["https://railfan.com/union-pacific-2026-big-boy-eastern-tour/"],
         **{"place": "유니언 퍼시픽 증기기관고, 샤이엔 (WY)", "lat": 41.1400, "lon": -104.8200}, tender=7, livery="up-black", shape="american"),

    loco("us-up-844", "리빙 레전드 844", "Living Legend 844",
         "Union Pacific FEF-3", "US", "golden", "4-8-4",
         no="844", built=1944, qty=10, builders=["ALCO"], operators=["Union Pacific"],
         wheelName="Northern", service="express",
         weight=417.0, driver=2032, pressure=21.4, cyl=2, te=282.0, speed=193,
         status="operational", survivors=3, iconic=True,
         highlights=["유니언 퍼시픽이 한 번도 퇴역시키지 않은 유일한 미국 1급 철도 증기기관차"],
         summary="1944년 인도 이후 지금까지 단 한 번도 정식 퇴역 처리된 적이 없다. "
                 "디젤 전환기에 그대로 사내 행사용으로 남겨진 덕에 '끊긴 적 없는 현역'이 됐다.",
         tags=["동태보존", "명차"], verified=False,
         **{"place": "유니언 퍼시픽 증기기관고, 샤이엔 (WY)", "lat": 41.1400, "lon": -104.8200}, livery="up-black", shape="american"),

    loco("us-nw-611", "N&W J형 611", "Norfolk & Western Class J 611",
         "N&W Class J", "US", "golden", "4-8-4",
         no="611", built=1950, builtTo=1950, qty=14, builders=["Roanoke Shops"],
         operators=["Norfolk and Western Railway"], wheelName="Northern", service="express",
         weight=436.0, driver=1778, pressure=20.0, cyl=2, te=356.0, speed=177,
         withdrawn=1959, status="operational", survivors=1, iconic=True,
         highlights=["미국 여객용 증기기관차 중 최고 수준의 견인력", "시운전에서 110 mph 기록"],
         summary="철도회사가 자기 공장에서 직접 만든 유선형 여객기. 소구경 동륜에 고출력을 얹어 "
                 "산악 노선에서도 급행을 유지했다. 유일하게 남은 1량이 지금도 운행한다.",
         tags=["유선형", "명차", "동태보존"], verified=False,
         **{"place": "버지니아 교통박물관, 로어노크", "lat": 37.2740, "lon": -79.9440}, livery="nw-tuxedo-black", shape="streamlined"),

    loco("us-sp-4449", "데이라이트 4449", "Daylight 4449",
         "Southern Pacific GS-4", "US", "golden", "4-8-4",
         no="4449", built=1941, qty=28, builders=["Lima Locomotive Works"],
         operators=["Southern Pacific"], wheelName="Northern", service="express",
         weight=413.0, driver=2032, pressure=20.0, cyl=2, te=282.0, speed=177,
         withdrawn=1957, status="operational", survivors=2, iconic=True,
         highlights=["1976년 미국 독립 200주년 '자유의 열차(Freedom Train)' 견인"],
         summary="주황·적색 '데이라이트' 도색으로 가장 사진이 많이 찍힌 미국 기관차. "
                 "폐차 직전 공원에 전시됐다가 200주년 행사를 위해 되살아났다.",
         tags=["유선형", "명차", "동태보존"], verified=False,
         **{"place": "오리건 철도유산센터, 포틀랜드", "lat": 45.5060, "lon": -122.6650}, livery="sp-daylight", shape="semi"),

    loco("us-prr-k4", "PRR K4s", "Pennsylvania K4s",
         "PRR K4s", "US", "classic", "4-6-2",
         no="1361", built=1914, builtTo=1928, qty=425, builders=["Juniata Shops", "Baldwin"],
         operators=["Pennsylvania Railroad"], wheelName="Pacific", service="express",
         weight=243.0, driver=2032, pressure=14.8, cyl=2, te=200.0, speed=148,
         withdrawn=1957, status="static", survivors=2,
         highlights=["펜실베이니아 철도의 상징 — 425량 생산"],
         summary="미국 동부 간선 여객의 표준. 한 형식이 40년 넘게 최고 등급 열차를 맡은 드문 사례다.",
         tags=["대량생산"], verified=False,
         **{"place": "펜실베이니아 철도박물관, 스트라스버그", "lat": 40.0000, "lon": -76.1500}, livery="prr-brunswick-green", shape="american"),

    loco("us-nyc-hudson", "NYC 허드슨 J-3a", "New York Central Hudson J-3a",
         "NYC J-3a", "US", "golden", "4-6-4",
         built=1937, builtTo=1938, qty=50, builders=["ALCO"], designer="Henry Dreyfuss (외장)",
         operators=["New York Central"], wheelName="Hudson", service="express",
         weight=331.0, driver=2007, pressure=18.6, cyl=2, te=196.0, speed=180,
         withdrawn=1956, status="scrapped", survivors=0, iconic=True,
         highlights=["'20세기 특급(20th Century Limited)' 견인", "허드슨형 전량이 해체되어 한 량도 남지 않음"],
         summary="드레이퍼스의 유선형 외장으로 아르데코 시대의 아이콘이 됐지만, "
                 "디젤 전환이 워낙 빨라 보존 논의가 시작되기도 전에 전량 고철이 됐다.",
         tags=["유선형", "현존없음", "명차"], verified=False, livery="nyc-black", shape="streamlined"),

    loco("us-co-allegheny",  "앨러게이니", "Allegheny",
         "C&O Class H-8", "US", "golden", "2-6-6-6",
         no="1601", built=1941, builtTo=1948, qty=60, builders=["Lima Locomotive Works"],
         operators=["Chesapeake and Ohio", "Virginian Railway"], service="articulated",
         weight=544.0, driver=1676, pressure=18.6, cyl=4, te=498.0, power=5300, speed=97,
         withdrawn=1956, status="static", survivors=2,
         highlights=["측정된 지시마력 기준 세계 최고 출력의 증기기관차 (약 7,500 hp)"],
         summary="빅보이가 '가장 큰' 기관차라면 앨러게이니는 '가장 힘센' 기관차. "
                 "석탄을 산 너머로 넘기기 위해 출력만 극단적으로 밀어붙인 설계.",
         tags=["관절식", "최고출력"], verified=False,
         **{"place": "헨리 포드 박물관, 디어본 (MI)", "lat": 42.3030, "lon": -83.2340}, tender=6, livery="co-black", shape="american"),

    loco("us-milw-classa", "밀워키 로드 A형", "Milwaukee Road Class A",
         "Milwaukee Road Class A", "US", "golden", "4-4-2",
         built=1935, qty=4, builders=["ALCO"], operators=["Chicago, Milwaukee, St. Paul and Pacific"],
         wheelName="Atlantic", service="express",
         weight=245.0, driver=2134, pressure=20.0, cyl=2, te=133.0, speed=193,
         withdrawn=1951, status="scrapped", survivors=0,
         highlights=["'히아와타' 견인 — 정기 운행에서 상시 100 mph 이상을 유지한 드문 사례"],
         summary="유선형 애틀랜틱. 가벼운 편성을 아주 빠르게 굴린다는 전략으로, 스케줄상 평균속도에서는 "
                 "세계에서 가장 빠른 증기 열차였다는 평가를 받는다. 4량 모두 해체.",
         tags=["유선형", "고속", "현존없음"], verified=False, livery="milw-gray", shape="streamlined"),

    loco("us-atsf-3751", "ATSF 3751", "Santa Fe 3751",
         "ATSF 3751 Class", "US", "golden", "4-8-4",
         no="3751", built=1927, qty=14, builders=["Baldwin Locomotive Works"],
         operators=["Atchison, Topeka and Santa Fe"], wheelName="Northern", service="express",
         weight=433.0, driver=2032, pressure=15.5, cyl=2, te=294.0, speed=161,
         withdrawn=1957, status="operable", survivors=1,
         highlights=["볼드윈이 만든 최초의 4-8-4 노던형"],
         summary="미국 서부 사막 구간을 무급수로 길게 달리기 위해 대형 탄수차를 단 장거리 여객기. "
                 "노던형이라는 이름 자체가 이 계열에서 굳어졌다.",
         tags=["동태보존"], verified=False,
         **{"place": "San Bernardino History & Railroad Museum (CA)", "lat": 34.1060, "lon": -117.2960}, livery="atsf-black", shape="american"),

    loco("us-nw-y6b", "N&W Y6b", "Norfolk & Western Y6b",
         "N&W Class Y6b", "US", "twilight", "2-8-8-2",
         built=1948, builtTo=1952, qty=30, builders=["Roanoke Shops"],
         operators=["Norfolk and Western Railway"], service="articulated",
         weight=513.0, driver=1448, pressure=20.0, cyl=4, te=741.0, speed=80,
         withdrawn=1960, status="static", survivors=1,
         highlights=["단순팽창 보조 사용 시 견인력 약 170,000 lbf — 미국 증기 최고 수준"],
         summary="복식팽창(compound) 관절식의 완성형. N&W는 디젤이 대세가 된 1950년대에도 "
                 "자체 계산으로 증기가 더 싸다고 판단해 계속 신조했다.",
         tags=["관절식", "복식팽창"], verified=False,
         **{"place": "미국 국립교통박물관, 세인트루이스", "lat": 38.5720, "lon": -90.4700}, livery="nw-black", shape="american"),
]

LOCOS += [
    # ── 독일 ────────────────────────────────────────────────
    loco("de-adler",  "아들러", "Adler",
         "Adler", "DE", "pioneer", "2-2-2",
         built=1835, qty=1, designer="Robert Stephenson",
         builders=["Robert Stephenson and Company"], operators=["Ludwigseisenbahn"],
         service="express", weight=14.0, speed=65,
         status="replica", survivors=0, iconic=True,
         highlights=["독일 최초의 상업 운행 증기기관차 (뉘른베르크~퓌르트, 1835)"],
         summary="영국에서 수입해 독일 철도의 문을 연 기관차. 원형은 남지 않았고 "
                 "1935년 제작된 복제품이 DB 박물관에 있다.",
         tags=["최초", "복제품"], verified=False,
         **{"place": "DB 박물관, 뉘른베르크", "lat": 49.4450, "lon": 11.0740}, tender=2, livery="adler-green", shape="early"),

    loco("de-drg-05", "05형", "DRG Class 05",
         "DRG Baureihe 05", "DE", "golden", "4-6-4",
         no="05 002", built=1935, qty=3, builders=["Borsig"], operators=["Deutsche Reichsbahn"],
         uic="2'C2'h3", wheelName="Hudson", service="express",
         weight=214.0, driver=2300, pressure=20.0, cyl=3, te=137.0, power=2360, speed=200.4,
         withdrawn=1958, status="static", survivors=1, iconic=True,
         highlights=["1936-05-11, 베를린~함부르크 구간에서 200.4 km/h 기록",
                     "05 002는 1960년 해체 — 남은 것은 05 001뿐"],
         summary="맬러드 이전의 세계 기록 보유기. 197톤 편성을 끌고 200 km/h를 넘겼다. "
                 "완전 유선형 외피에 붉은 도색이라는 파격적인 외형으로도 유명하다.",
         tags=["속도기록", "유선형", "명차"], verified=True,
         sources=["https://en.wikipedia.org/wiki/DRG_Class_05"],
         **{"place": "05 001: DB 박물관, 뉘른베르크", "lat": 49.4450, "lon": 11.0740}, livery="drg-red", shape="streamlined"),

    loco("de-drg-01", "01형", "DRG Class 01",
         "DRG Baureihe 01", "DE", "golden", "4-6-2",
         built=1926, builtTo=1938, qty=241, builders=["Borsig", "AEG", "Henschel"],
         operators=["Deutsche Reichsbahn", "DB", "DR"], uic="2'C1'h2", wheelName="Pacific",
         service="express", weight=170.0, driver=2000, pressure=16.0, cyl=2,
         te=162.0, power=1650, speed=130,
         withdrawn=1982, status="operational", survivors=30,
         highlights=["독일 통일형 증기기관차(Einheitsdampflokomotive)의 첫 형식"],
         summary="부품 공통화를 전제로 처음부터 '시리즈'로 설계된 기관차. 이후 독일 증기 설계 전체가 "
                 "이 문법을 따랐다. 지금도 여러 량이 특별열차를 끈다.",
         tags=["표준형", "동태보존"], verified=False,
         **{"place": "다수 보존 (예: DB 박물관 / 각 보존회)", "lat": 49.4450, "lon": 11.0740}, livery="drg-black", shape="classic"),

    loco("de-drg-52", "52형 전시표준형", "Kriegslokomotive Class 52",
         "DRG Baureihe 52", "DE", "golden", "2-10-0",
         built=1942, builtTo=1945, qty=6719, builders=["Borsig", "Henschel", "Krupp", "외 다수"],
         operators=["Deutsche Reichsbahn", "유럽 각국 철도"], uic="1'Eh2", wheelName="Decapod",
         service="freight", weight=140.0, driver=1400, pressure=16.0, cyl=2,
         te=176.0, speed=80,
         status="operational", survivors=200,
         highlights=["6,700량 이상 생산 — 유럽에서 가장 많이 만들어진 증기기관차 계열"],
         summary="전시 물자난 속에서 '최소 재료·최단 공정'으로 다시 설계한 화물기. 전후 소련·폴란드·"
                 "동유럽 전역으로 흩어져 1980년대까지 일했다. 지금도 가장 흔한 유럽 보존 증기기관차.",
         tags=["대량생산", "전시표준"], verified=False,
         **{"place": "유럽 각지 다수 보존", "lat": 52.5200, "lon": 13.4050}, livery="drg-black", shape="classic"),

    loco("de-dr-18201", "18 201", "DR 18 201",
         "DR Baureihe 18.2", "DE", "twilight", "4-6-2",
         no="18 201", built=1961, qty=1, operators=["Deutsche Reichsbahn"],
         builders=["Raw Meiningen"], uic="2'C1'h3", wheelName="Pacific", service="express",
         weight=148.0, driver=2300, pressure=16.0, cyl=3, speed=182.4,
         status="operational", survivors=1, iconic=True,
         highlights=["세계에서 가장 빠른 운행 가능 증기기관차 (182.4 km/h)"],
         summary="객차 시험용 견인기로 여러 기관차의 부품을 조합해 만든 한 량짜리 형식. "
                 "지금도 특별열차에서 시속 180km대를 낼 수 있는 유일한 증기기관차다.",
         tags=["고속", "동태보존", "명차"], verified=False,
         **{"place": "독일 (특별열차 운행)", "lat": 51.1657, "lon": 10.4515}, livery="drg-red", shape="semi"),

    loco("de-drg-0310", "03.10형", "DRG Class 03.10",
         "DRG Baureihe 03.10", "DE", "golden", "4-6-2",
         built=1939, builtTo=1941, qty=60, builders=["Borsig", "Krupp"],
         operators=["Deutsche Reichsbahn"], wheelName="Pacific", service="express",
         weight=185.0, driver=2000, pressure=16.0, cyl=3, speed=140,
         withdrawn=1980, status="static", survivors=4,
         highlights=["01형의 유선형 파생 — 전후 대부분 외피를 제거"],
         summary="유선형 외피는 정비를 어렵게 만든다는 것이 전후에 확인되면서 대부분 벗겨졌다. "
                 "유선형 시대의 이상과 현실을 동시에 보여주는 형식.",
         tags=["유선형"], verified=False,
         **{"place": "교통박물관, 드레스덴", "lat": 51.0530, "lon": 13.7400}, livery="drg-black", shape="streamlined"),

    loco("de-drg-44", "44형", "DRG Class 44",
         "DRG Baureihe 44", "DE", "golden", "2-10-0",
         built=1926, builtTo=1949, qty=1989, builders=["Henschel", "Krupp", "외"],
         operators=["Deutsche Reichsbahn", "DB", "DR"], wheelName="Decapod", service="freight",
         weight=175.0, driver=1400, pressure=16.0, cyl=3, te=245.0, speed=80,
         withdrawn=1982, status="operable", survivors=20,
         summary="독일 중량 화물의 주력. 3기통 배치로 저속에서 매끄러운 견인력을 냈다.",
         tags=["화물", "표준형"], verified=False,
         **{"place": "독일 각지 보존", "lat": 51.1657, "lon": 10.4515}, livery="drg-black", shape="classic"),

    loco("de-br-10", "10형", "DB Class 10",
         "DB Baureihe 10", "DE", "twilight", "4-6-2",
         built=1957, qty=2, builders=["Krupp"], operators=["Deutsche Bundesbahn"],
         wheelName="Pacific", service="express",
         weight=190.0, driver=2000, pressure=18.0, cyl=3, power=1650, speed=140,
         withdrawn=1968, status="static", survivors=1,
         highlights=["서독이 마지막으로 신조한 급행 여객용 증기기관차"],
         summary="증기 시대의 마지막 인사. 완성된 지 10년 만에 전기·디젤에 자리를 내줬다.",
         tags=["마지막"], verified=False,
         **{"place": "Deutsches Dampflokomotiv-Museum, 노이엔마르크트", "lat": 50.1490, "lon": 11.5570}, livery="drg-black", shape="semi"),

    # ── 프랑스 ──────────────────────────────────────────────
    loco("fr-242a1", "242 A 1", "SNCF 242 A 1",
         "SNCF 242 A 1", "FR", "twilight", "4-8-4",
         no="242 A 1", built=1946, qty=1, designer="André Chapelon",
         builders=["Société des Batignolles (개조)"], operators=["SNCF"],
         uic="2'D2'h3", wheelName="Northern", service="express",
         weight=222.0, driver=1950, pressure=20.0, cyl=3, power=4000, speed=140,
         withdrawn=1960, status="scrapped", survivors=0, iconic=True,
         highlights=["유럽에서 가장 강력했던 증기기관차 (약 5,500 hp)", "1960년 해체 — 현존하지 않음"],
         summary="샤플롱이 실패작 하나를 뜯어고쳐 만든 단 한 량. 열역학적 개량만으로 출력을 두 배 가까이 "
                 "끌어올려 '증기기관차 공학의 정점'으로 불린다. 보존 요청에도 불구하고 폐기됐다.",
         tags=["최고출력", "현존없음", "명차"], verified=False, livery="sncf-green", shape="classic"),

    loco("fr-241p", "241 P형", "SNCF 241 P",
         "SNCF 241 P", "FR", "twilight", "4-8-2",
         no="241 P 17", built=1948, builtTo=1952, qty=35, builders=["Schneider"],
         operators=["SNCF"], uic="2'D1'h4v", wheelName="Mountain", service="express",
         weight=213.0, driver=2020, pressure=20.0, cyl=4, power=2650, speed=120,
         withdrawn=1969, status="operable", survivors=3,
         highlights=["프랑스 최대의 급행 여객용 증기기관차", "복식팽창(compound) 4기통"],
         summary="프랑스 증기의 상징인 복식팽창 방식을 마지막까지 밀고 나간 형식. "
                 "241 P 17호는 동태보존되어 유럽 각지에서 특별열차를 끌었다.",
         tags=["복식팽창", "동태보존"], verified=False,
         **{"place": "Cité du Train, 뮐루즈 / 르 크뢰조", "lat": 47.7490, "lon": 7.3210}, livery="sncf-green", shape="classic"),

    loco("fr-231e", "231 E형", "PO/SNCF 231 E",
         "Chapelon 231 E", "FR", "golden", "4-6-2",
         built=1934, qty=48, designer="André Chapelon",
         builders=["Paris-Orléans (개조)"], operators=["Chemin de fer de Paris à Orléans", "SNCF"],
         wheelName="Pacific", service="express",
         weight=145.0, driver=1950, pressure=20.0, cyl=4, power=2200, speed=130,
         withdrawn=1965, status="static", survivors=2,
         highlights=["기존 퍼시픽을 개조해 출력을 약 두 배로 끌어올린 개량의 교과서"],
         summary="증기 통로 저항을 줄이고 배기를 다듬는 것만으로 성능이 얼마나 달라지는지 보여준 사례. "
                 "이 결과가 영국·미국 설계자들에게도 큰 영향을 줬다.",
         tags=["복식팽창", "개량"], verified=False,
         **{"place": "Cité du Train, 뮐루즈", "lat": 47.7490, "lon": 7.3210}, livery="sncf-green", shape="classic"),

    loco("fr-crampton",  "크램프턴", "Crampton",
         "Crampton Type", "FR", "expansion", "4-2-0",
         no="80 Le Continent", built=1852, qty=127, designer="Thomas Russell Crampton",
         builders=["Cail"], operators=["Chemins de fer de l'Est"], service="express",
         weight=48.0, driver=2100, speed=120,
         status="static", survivors=1,
         highlights=["19세기 중반 유럽에서 가장 빠른 축에 속했던 기관차"],
         summary="동륜을 화실 뒤로 빼서 보일러를 낮게 앉힌 독특한 배치. 영국에서는 외면받았지만 "
                 "프랑스·독일에서 크게 유행해 'prendre le Crampton(기차 타다)'이라는 말까지 남겼다.",
         tags=["고전", "이정표"], verified=False,
         **{"place": "Cité du Train, 뮐루즈", "lat": 47.7490, "lon": 7.3210}, tender=3, livery="est-green", shape="victorian"),

    loco("fr-140c", "140 C형", "SNCF 140 C",
         "SNCF 140 C", "FR", "classic", "2-8-0",
         built=1913, builtTo=1920, qty=370, builders=["Fives-Lille", "북미 제작사"],
         operators=["SNCF", "Chemins de fer de l'Est"], wheelName="Consolidation",
         service="freight", weight=120.0, driver=1450, pressure=12.0, cyl=2, speed=65,
         withdrawn=1970, status="operable", survivors=5,
         summary="1차 대전기 물자 수송을 위해 대량 도입된 화물기. 프랑스 보존 철도의 단골 손님이다.",
         tags=["화물"], verified=False,
         **{"place": "프랑스 각지 보존 철도", "lat": 46.5000, "lon": 2.5000}, livery="sncf-black", shape="classic"),
]

KYOTO = dict(place="교토 철도박물관", lat=34.9870, lon=135.7370)
OMIYA = dict(place="철도박물관, 오미야", lat=35.9200, lon=139.6210)

LOCOS += [
    # ── 일본 ────────────────────────────────────────────────
    loco("jp-class150", "1호 기관차", "Class 150",
         "JGR Class 150", "JP", "expansion", "2-4-0T",
         no="150", built=1871, qty=1, builders=["Vulcan Foundry"],
         operators=["일본 철도료"], gauge=1067, service="tank", weight=16.5, weightBasis="loco",
         driver=1321, speed=40, tender=0,
         status="static", survivors=1, iconic=True,
         highlights=["일본 최초의 철도 개통(1872, 신바시~요코하마)에 사용된 기관차"],
         summary="영국에서 수입된 일본 철도의 1번 기관차. 중요문화재로 지정되어 오미야에 있다.",
         tags=["최초", "이정표"], verified=False, **OMIYA, livery="jnr-black", shape="victorian"),

    loco("jp-c62",  "C62형", "JNR Class C62",
         "JNR C62", "JP", "twilight", "4-6-4",
         no="C62 2", built=1948, builtTo=1949, qty=49, builders=["가와사키", "히타치", "미쓰비시"],
         operators=["일본국유철도"], uic="2'C2'", wheelName="Hudson", gauge=1067, service="express",
         length=21475, weight=145.2, driver=1750, pressure=15.0, cyl=2, te=134.0, speed=129,
         withdrawn=1973, status="static", survivors=3, iconic=True,
         highlights=["일본 최대·최고속 여객용 증기기관차", "1954년 협궤 세계 최고속도 129 km/h 기록",
                     "C62 2 '스완(つばめ)'은 데플렉터의 제비 마크로 유명"],
         summary="전후 남아도는 D51의 보일러를 얹어 만든 대형 여객기. 협궤(1067mm)라는 제약 안에서 "
                 "가능한 최대치를 뽑아낸 형식으로, 일본 증기의 상징으로 통한다.",
         tags=["협궤", "고속", "명차"], verified=False, **KYOTO, tender=4, livery="jnr-black", shape="classic"),

    loco("jp-d51",  "D51형 데고이치", "JNR Class D51",
         "JNR D51", "JP", "golden", "2-8-2",
         no="D51 200", built=1936, builtTo=1945, qty=1115, builders=["가와사키", "히타치", "국철 공장"],
         operators=["일본국유철도"], uic="1'D1'", wheelName="Mikado", gauge=1067, service="freight",
         weight=125.8, driver=1400, pressure=15.0, cyl=2, te=157.0, speed=85,
         withdrawn=1976, status="operational", survivors=170, iconic=True,
         highlights=["일본에서 가장 많이 만들어진 증기기관차 — 1,115량", "D51 200호는 현재 SL 야마구치호를 견인"],
         summary="'데고이치(デゴイチ)'라는 애칭이 곧 증기기관차의 대명사가 될 만큼 흔했다. "
                 "170량 넘게 보존되어 있고 그중 몇 량은 지금도 관광열차로 달린다.",
         tags=["대량생산", "협궤", "명차", "동태보존"], verified=False, **KYOTO, tender=4, livery="jnr-black", shape="classic"),

    loco("jp-c57", "C57형 귀부인", "JNR Class C57",
         "JNR C57", "JP", "golden", "4-6-2",
         no="C57 1", built=1937, builtTo=1947, qty=201, builders=["가와사키", "미쓰비시", "히타치"],
         operators=["일본국유철도"], wheelName="Pacific", gauge=1067, service="express",
         weight=115.5, driver=1750, pressure=16.0, cyl=2, te=120.0, speed=100,
         withdrawn=1975, status="operational", survivors=20, iconic=True,
         highlights=["가느다란 보일러 실루엣으로 '귀부인(貴婦人)'이라 불림", "C57 1호가 SL 야마구치호 견인"],
         summary="일본 여객용 증기의 표준형이자 가장 아름답다는 평을 듣는 형식. "
                 "1975년 일본 국철 마지막 정기 여객 증기열차를 끈 것도 C57(135호)이었다.",
         tags=["협궤", "동태보존", "명차"], verified=False, **OMIYA, livery="jnr-black", shape="classic"),

    loco("jp-c11", "C11형", "JNR Class C11",
         "JNR C11", "JP", "golden", "2-6-4T",
         built=1932, builtTo=1947, qty=381, builders=["가와사키", "히타치", "니혼샤료"],
         operators=["일본국유철도"], gauge=1067, service="tank",
         weight=68.1, driver=1520, pressure=15.0, cyl=2, speed=85,
         withdrawn=1975, status="operational", survivors=50,
         highlights=["오이가와 철도의 '토마스' 등 관광 운행에 다수 현역"],
         summary="탄수차가 없는 탱크식이라 방향 전환이 쉬워 지선·입환에 널리 쓰였다. "
                 "지금은 일본 관광 증기열차의 주력.",
         tags=["탱크식", "동태보존"], verified=False,
         **{"place": "오이가와 철도 (시즈오카)", "lat": 34.8180, "lon": 138.1300}, livery="jnr-black", shape="classic"),

    loco("jp-8620", "8620형 하치로쿠", "JNR Class 8620",
         "JNR 8620", "JP", "classic", "2-6-0",
         no="58654", built=1914, builtTo=1929, qty=687, builders=["기샤세이조", "가와사키", "히타치"],
         operators=["일본국유철도"], wheelName="Mogul", gauge=1067, service="mixed",
         weight=83.0, driver=1600, pressure=13.0, cyl=2, speed=95,
         withdrawn=1975, status="operable", survivors=10,
         highlights=["일본이 자국 설계로 대량생산한 최초의 여객용 기관차"],
         summary="'하치로쿠(ハチロク)'. 수입 의존을 끝내고 일본 철도가 스스로 형식을 굴리기 시작한 지점. "
                 "58654호는 SL 히토요시로 오래 운행했다.",
         tags=["국산화"], verified=False,
         **{"place": "규슈 (JR 규슈)", "lat": 32.8030, "lon": 130.7080}, livery="jnr-black", shape="classic"),

    loco("jp-9600", "9600형", "JNR Class 9600",
         "JNR 9600", "JP", "classic", "2-8-0",
         built=1913, builtTo=1926, qty=770, builders=["가와사키", "기샤세이조"],
         operators=["일본국유철도"], wheelName="Consolidation", gauge=1067, service="freight",
         weight=94.0, driver=1250, pressure=13.0, cyl=2, speed=65,
         withdrawn=1976, status="static", survivors=20,
         highlights=["일본 최초의 국산 대량생산 화물용 기관차", "일본 국철 증기 중 가장 오래 현역"],
         summary="'큐로쿠(キューロク)'. 1976년 일본 국철의 마지막 증기 운행까지 살아남은 장수 형식이다.",
         tags=["국산화", "화물"], verified=False, **OMIYA, livery="jnr-black", shape="classic"),

    loco("jp-c58", "C58형", "JNR Class C58",
         "JNR C58", "JP", "golden", "2-6-2",
         no="C58 239", built=1938, builtTo=1947, qty=427, builders=["가와사키", "기샤세이조"],
         operators=["일본국유철도"], wheelName="Prairie", gauge=1067, service="mixed",
         weight=100.2, driver=1520, pressure=16.0, cyl=2, speed=85,
         withdrawn=1975, status="operational", survivors=40,
         highlights=["C58 239호가 SL 긴가(銀河)를 견인 — 미야자와 겐지 테마 열차"],
         summary="지방 간선의 여객·화물을 함께 맡던 중형 만능기. 보존 상태가 좋아 관광 운행 복귀 사례가 많다.",
         tags=["동태보존"], verified=False,
         **{"place": "이와테 (JR 동일본)", "lat": 39.7020, "lon": 141.1360}, livery="jnr-black", shape="classic"),

    # ── 한국 ────────────────────────────────────────────────
    loco("kr-moga", "모가형", "Moga (Mogul)",
         "모가형 (Moga)", "KR", "classic", "2-6-0T",
         built=1899, qty=4, builders=["Brooks Locomotive Works (부품)", "인천공작창 (조립)"],
         operators=["경인철도합자회사", "조선총독부 철도국"], wheelName="Mogul",
         # 탱크식(탄수차 없음). 탄수차식으로 그리면 고증 오류 — tools/verified.py 참조
         service="tank", speed=55, tender=0,
         status="replica", survivors=0, iconic=True,
         highlights=["1899년 경인선 개통 — 한국 철도 최초의 증기기관차"],
         summary="미국 브룩스사에서 부품을 들여와 인천공작창에서 조립했다. 총 4량. "
                 "원형은 남아 있지 않고, 인천역과 동인천역에 실물 크기 모형이 세워져 있다.",
         tags=["최초", "이정표"], verified=True,
         sources=["https://namu.wiki/w/모가형 증기기관차"],
         **{"place": "모형: 인천역 한국철도 탄생역 기념비", "lat": 37.4760, "lon": 126.6170}, livery="korail-black", shape="american"),

    loco("kr-mika3-129",  "미카3형 129호", "Mika-3 No. 129",
         "미카3형 (Mika-3)", "KR", "golden", "2-8-2",
         no="129", built=1927, builtTo=1945, qty=300, builders=["경성공작창", "일본 제작사"],
         operators=["조선총독부 철도국", "대한민국 교통부"], wheelName="Mikado",
         service="freight", weight=110.0, driver=1370, speed=80,
         withdrawn=1967, status="static", survivors=5, iconic=True,
         highlights=["국가등록문화재 제415호", "한국전쟁 당시 특별공작대 수송 임무로 알려진 기관차"],
         summary="1919년부터 300량 이상 도입된 한국 철도의 대표 화물기. 129호는 국립대전현충원 "
                 "호국철도기념관에 보존되어 있다.",
         tags=["문화재", "명차"], verified=True,
         sources=["https://ko.wikipedia.org/wiki/미카형_증기_기관차"],
         **{"place": "국립대전현충원 호국철도기념관", "lat": 36.3610, "lon": 127.2900}, tender=4, livery="korail-black", shape="american"),

    loco("kr-mika3-161",  "미카3형 161호", "Mika-3 No. 161",
         "미카3형 (Mika-3)", "KR", "golden", "2-8-2",
         no="161", built=1940, qty=300, builders=["경성공작창"],
         operators=["조선총독부 철도국", "대한민국 교통부"], wheelName="Mikado",
         service="freight", weight=110.0, driver=1370, speed=80,
         withdrawn=1967, status="static", survivors=5,
         highlights=["안도현 시집 《증기기관차 미카》(2001)의 소재"],
         summary="의왕 철도박물관 옥외전시장에 있는 미카3형. 한국인에게 가장 익숙한 증기기관차 실물이다.",
         tags=["문화재"], verified=True,
         sources=["https://ko.wikipedia.org/wiki/미카형_증기_기관차"],
         **{"place": "철도박물관 옥외전시장, 의왕", "lat": 37.3390, "lon": 126.9670}, tender=4, livery="korail-black", shape="american"),

    loco("kr-pashi5",  "파시5형", "Pashi-5 (Pacific)",
         "파시5형 (Pashi-5)", "KR", "golden", "4-6-2",
         no="23", built=1942, qty=None, builders=["경성공작창", "가와사키"],
         operators=["조선총독부 철도국", "대한민국 교통부"], wheelName="Pacific",
         service="express", driver=1750, speed=110,
         withdrawn=1967, status="static", survivors=1, iconic=True,
         highlights=["한국 증기기관차 중 최고속도 110 km/h", "국내에서 처음 조립 생산된 기관차 계열"],
         summary="파시형은 한국 급행 여객의 주력이었다. 파시5형은 그중 가장 빠른 형식이며 "
                 "23호가 의왕 철도박물관에 보존되어 있다.",
         tags=["최고속도", "명차"], verified=True,
         sources=["https://namu.wiki/w/파시형 증기기관차"],
         **{"place": "철도박물관, 의왕", "lat": 37.3390, "lon": 126.9670}, tender=4, livery="korail-black", shape="american"),

    loco("kr-teou", "터우형", "Teou (Ten-wheeler)",
         "터우형 (Teou)", "KR", "classic", "4-6-0",
         built=1905, qty=40, builders=["Baldwin Locomotive Works", "ALCO"],
         operators=["통감부 철도관리국", "조선총독부 철도국"], wheelName="Ten-wheeler",
         service="mixed", speed=70,
         withdrawn=1950, status="scrapped", survivors=0,
         highlights=["경부선 개통기의 주력 여객기"],
         summary="미국에서 수입된 4-6-0 텐휠러. 초기 한국 간선의 여객·혼합 열차를 맡았다. "
                 "현존 실물은 확인되지 않는다.",
         tags=["초기"], verified=False, livery="korail-black", shape="american"),

    loco("kr-hyeogi", "혀기형", "Hyeogi (Narrow Gauge)",
         "혀기형 (Hyeogi)", "KR", "golden", "2-8-2T",
         built=1930, qty=None, builders=["일본 제작사"],
         operators=["조선경동철도", "대한민국 교통부"], gauge=762, service="narrow", tender=0,
         speed=50, withdrawn=1970, status="static", survivors=1,
         highlights=["수인선·수여선 등 762mm 협궤 노선용"],
         summary="한국에도 협궤 철도가 있었다. 수원~인천 수인선의 좁은 궤간을 달리던 소형 기관차 계열로, "
                 "협궤 객차와 함께 일부가 보존되어 있다.",
         tags=["협궤"], verified=False,
         **{"place": "철도박물관, 의왕", "lat": 37.3390, "lon": 126.9670}, livery="korail-black", shape="classic"),
]

LOCOS += [
    # ── 중국 ────────────────────────────────────────────────
    loco("cn-qj", "첸진(前進) QJ형", "QJ Class",
         "China Railways QJ", "CN", "twilight", "2-10-2",
         built=1956, builtTo=1988, qty=4714, builders=["다롄 기관차공장", "다퉁 기관차공장"],
         operators=["중국철도"], wheelName="Santa Fe", service="freight",
         length=26000, weight=246.0, driver=1500, pressure=15.0, cyl=2, te=274.0, speed=80,
         status="operable", survivors=100, iconic=True,
         highlights=["세계에서 가장 늦게까지 신조된 대형 간선 증기기관차 (1988년까지)",
                     "2005년 지퉁(集通)철도 — 세계 마지막 간선 증기 운행"],
         summary="증기 시대가 끝난 뒤에도 30년을 더 만들어진 기관차. 내몽골 지퉁철도의 QJ 중련 화물열차는 "
                 "전 세계 철도 팬의 마지막 순례지였다.",
         tags=["대량생산", "마지막", "명차"], verified=False,
         **{"place": "중국철도박물관, 베이징", "lat": 40.0570, "lon": 116.4650}, livery="cr-black", shape="headlamp"),

    loco("cn-js", "젠서(建設) JS형", "JS Class",
         "China Railways JS", "CN", "twilight", "2-8-2",
         built=1957, builtTo=1988, qty=1916, builders=["다롄", "칭다오", "다퉁"],
         operators=["중국철도", "산다오링 탄광철도"], wheelName="Mikado", service="freight",
         weight=180.0, driver=1370, pressure=15.0, cyl=2, te=234.0, speed=85,
         status="operable", survivors=50, iconic=True,
         highlights=["2022-04-25, 산다오링 탄광철도의 마지막 증기 화물열차 — 세계 마지막 정기 증기 화물 운행 종료"],
         summary="신장 하미의 산다오링 노천탄광에서 2022년까지 매일 석탄을 실어 날랐다. "
                 "'영업 운전 중인 증기기관차'를 볼 수 있던 지구상 마지막 장소였다.",
         tags=["마지막", "화물"], verified=True,
         sources=["https://railfan.com/end-of-an-era-chinas-last-steam-railroad-closes/"],
         **{"place": "산다오링 탄광, 하미 (신장)", "lat": 43.0000, "lon": 92.7000}, livery="cr-black", shape="headlamp"),

    loco("cn-sy", "상유(上游) SY형", "SY Class",
         "China Railways SY", "CN", "twilight", "2-8-2",
         built=1960, builtTo=1999, qty=1800, builders=["탕산 기관차공장"],
         operators=["중국 산업철도"], wheelName="Mikado", service="freight",
         weight=140.0, driver=1370, pressure=13.0, cyl=2, te=170.0, speed=80,
         status="operational", survivors=200,
         highlights=["1999년까지 생산 — 세계에서 마지막으로 신조된 증기기관차 계열 중 하나"],
         summary="공장·탄광 전용 중형기. 일부는 미국 보존 철도로 수출되어 지금도 관광열차를 끈다.",
         tags=["산업용", "동태보존"], verified=False,
         **{"place": "중국 각지 산업철도 / 해외 보존 철도", "lat": 39.6300, "lon": 118.1800}, livery="cr-black", shape="headlamp"),

    loco("cn-jf", "제팡(解放) JF형", "JF Class",
         "China Railways JF", "CN", "classic", "2-8-2",
         no="JF 304 (毛泽东号)", built=1918, builtTo=1960, qty=2000,
         builders=["ALCO", "만주 기관차공장", "다롄"], operators=["중국철도"],
         wheelName="Mikado", service="freight", weight=175.0, driver=1370, speed=80,
         status="static", survivors=30,
         highlights=["'마오쩌둥호'로 명명된 기관차가 이 계열"],
         summary="만주에서 만들어진 미카도형 계열이 전후 중국철도의 기반이 됐다. "
                 "한국의 미카형과 뿌리를 공유한다.",
         tags=["화물", "역사"], verified=False,
         **{"place": "중국철도박물관, 베이징", "lat": 40.0570, "lon": 116.4650}, livery="cr-black", shape="headlamp"),

    loco("cn-km", "KD/KF형", "KF Class",
         "Chinese National Railways KF", "CN", "golden", "4-8-4",
         no="KF7", built=1935, qty=24, designer="Kenneth Cantlie",
         builders=["Vulcan Foundry"], operators=["중화민국 철도"], wheelName="Northern",
         service="mixed", weight=193.0, driver=1750, pressure=15.8, cyl=2, speed=100,
         withdrawn=1980, status="static", survivors=2,
         highlights=["영국이 중국을 위해 설계·수출한 4-8-4", "1량이 영국 과학박물관에 반환 전시"],
         summary="영국 설계·영국 제작으로 중국에서 40년 넘게 일한 기관차. 마지막에 한 량이 "
                 "고향 영국으로 돌아가 전시되고 있다는 점이 특이하다.",
         tags=["수출형"], verified=False,
         **{"place": "과학박물관, 런던 / 중국철도박물관", "lat": 51.4978, "lon": -0.1746}, livery="cr-black", shape="headlamp"),

    # ── 인도 ────────────────────────────────────────────────
    loco("in-fairyqueen",  "페어리 퀸", "Fairy Queen",
         "EIR-21 Fairy Queen", "IN", "expansion", "2-2-2",
         no="22", built=1855, qty=2, builders=["Kitson, Thompson & Hewitson"],
         operators=["East Indian Railway", "Indian Railways"], service="express",
         weight=26.0, driver=1830, speed=40,
         status="operable", survivors=1, iconic=True,
         highlights=["기네스 공인 — 세계에서 가장 오래된 운행 가능 증기기관차 (1855년 제작)",
                     "1997년부터 델리~알와르 유산열차 운행"],
         summary="1909년 퇴역 후 반세기를 전시품으로 있다가 1997년 복원되어 다시 달렸다. "
                 "170년 된 기계가 여전히 증기를 뿜는다는 것 자체가 기록이다.",
         tags=["최고령", "동태보존", "명차"], verified=True,
         sources=["https://www.guinnessworldrecords.com/world-records/62971-oldest-steam-locomotive-in-use"],
         **{"place": "레와리 증기기관고 / 국립철도박물관, 뉴델리", "lat": 28.1990, "lon": 76.6180}, tender=2, livery="ir-green", shape="victorian"),

    loco("in-dhr-b", "다르질링 B형", "Darjeeling Himalayan B Class",
         "DHR B Class", "IN", "classic", "0-4-0ST",
         built=1889, builtTo=1927, qty=34, builders=["Sharp, Stewart", "North British"],
         operators=["Darjeeling Himalayan Railway"], gauge=610, service="narrow",
         weight=14.0, driver=660, pressure=9.7, cyl=2, speed=20,
         status="operational", survivors=12, iconic=True,
         highlights=["유네스코 세계유산 (인도 산악철도)", "610mm 협궤로 해발 2,200m까지 등반"],
         summary="'토이 트레인'. 100년 넘은 소형 탱크기가 지금도 히말라야 산자락을 오른다. "
                 "세계에서 가장 오래 지속된 증기 정기 여객 운행 중 하나.",
         tags=["협궤", "세계유산", "동태보존", "명차"], verified=False,
         **{"place": "다르질링 히말라야 철도, 서벵골", "lat": 27.0410, "lon": 88.2630}, livery="dhr-blue", shape="victorian"),

    loco("in-wp", "WP형", "WP Class",
         "Indian Railways WP", "IN", "twilight", "4-6-2",
         built=1947, builtTo=1967, qty=755, builders=["Baldwin", "Chittaranjan Locomotive Works"],
         operators=["Indian Railways"], gauge=1676, wheelName="Pacific", service="express",
         weight=172.0, driver=1705, pressure=14.8, cyl=2, te=134.0, speed=110,
         withdrawn=1995, status="operable", survivors=15, iconic=True,
         highlights=["원뿔형 노즈콘이 상징 — 인도 광궤 여객의 얼굴"],
         summary="독립 인도가 자국 공장에서 대량생산한 첫 대형 여객기. 은색 별이 박힌 붉은 노즈콘 덕에 "
                 "멀리서도 바로 알아볼 수 있다.",
         tags=["광궤", "명차"], verified=False,
         **{"place": "국립철도박물관, 뉴델리", "lat": 28.5830, "lon": 77.1740}, livery="ir-red", shape="semi"),

    loco("in-wg", "WG형", "WG Class",
         "Indian Railways WG", "IN", "twilight", "2-8-2",
         built=1950, builtTo=1970, qty=2450, builders=["Chittaranjan Locomotive Works", "외"],
         operators=["Indian Railways"], gauge=1676, wheelName="Mikado", service="freight",
         weight=180.0, driver=1560, pressure=14.8, cyl=2, te=175.0, speed=80,
         withdrawn=1995, status="static", survivors=20,
         highlights=["인도에서 가장 많이 만들어진 증기기관차 — 2,450량"],
         summary="인도 광궤 화물의 주력. WP와 부품을 공유하도록 설계되어 정비 부담을 줄였다.",
         tags=["광궤", "대량생산"], verified=False,
         **{"place": "국립철도박물관, 뉴델리", "lat": 28.5830, "lon": 77.1740}, livery="ir-black", shape="classic"),

    # ── 남아프리카 ──────────────────────────────────────────
    loco("za-class25nc", "25NC형", "Class 25NC",
         "SAR Class 25NC", "ZA", "twilight", "4-8-4",
         built=1953, builtTo=1955, qty=140, builders=["Henschel", "North British"],
         operators=["South African Railways"], gauge=1067, wheelName="Northern", service="mixed",
         weight=234.0, driver=1524, pressure=15.9, cyl=2, te=228.0, speed=110,
         status="operable", survivors=30,
         highlights=["케이프 궤간(1067mm)에서 가장 큰 비관절식 기관차 중 하나"],
         summary="1990년대까지 남아공 간선 화물을 끌었다. 좁은 궤간에 얹을 수 있는 보일러 크기의 "
                 "실질적 한계를 보여주는 형식.",
         tags=["케이프궤간"], verified=False,
         **{"place": "남아프리카 각지 보존", "lat": -26.2000, "lon": 28.0500}, livery="sar-black", shape="classic"),

    loco("za-class26", "26형 레드 데블", "Red Devil",
         "SAR Class 26", "ZA", "revival", "4-8-4",
         no="3450", built=1981, qty=1, designer="David Wardale",
         builders=["Salt River Works (개조)"], operators=["South African Railways"],
         gauge=1067, wheelName="Northern", service="mixed",
         weight=234.0, driver=1524, pressure=15.9, cyl=2, power=3400, speed=110,
         status="static", survivors=1, iconic=True,
         highlights=["증기기관차 열효율 개량의 마지막 대규모 실험 (출력 +43%, 연료 소비 -30%)"],
         summary="25NC 한 량을 뜯어 가스 흐름·연소·배기를 전면 재설계한 '현대 증기(Modern Steam)'의 상징. "
                 "샤플롱의 방법론을 20세기 말에 되살린 사례다.",
         tags=["개량", "현대증기", "명차"], verified=False,
         **{"place": "남아프리카 (보존)", "lat": -33.9250, "lon": 18.4230}, livery="sar-red-devil", shape="classic"),

    loco("za-classgl", "GL형 가라트", "Class GL Garratt",
         "SAR Class GL", "ZA", "golden", "4-8-2+2-8-4",
         built=1929, builtTo=1930, qty=8, builders=["Beyer, Peacock and Company"],
         operators=["South African Railways"], gauge=1067, service="articulated",
         weight=214.0, driver=1372, pressure=13.8, cyl=4, te=390.0, speed=64,
         withdrawn=1972, status="static", survivors=2,
         highlights=["세계에서 가장 강력한 가라트형 기관차"],
         summary="보일러를 두 대차 사이에 매단 가라트 방식은 좁은 궤간·급곡선에서 대출력을 내는 해법이었다. "
                 "GL형은 그 방식이 도달한 최대치.",
         tags=["가라트", "관절식", "명차"], verified=False,
         **{"place": "남아프리카 (보존)", "lat": -29.7700, "lon": 30.6600}, livery="sar-black", shape="classic"),

    loco("za-class15f", "15F형", "Class 15F",
         "SAR Class 15F", "ZA", "golden", "4-8-2",
         built=1938, builtTo=1948, qty=255, builders=["North British", "Beyer, Peacock"],
         operators=["South African Railways"], gauge=1067, wheelName="Mountain", service="mixed",
         weight=180.0, driver=1524, pressure=14.5, cyl=2, te=190.0, speed=100,
         status="operable", survivors=25,
         summary="남아공에서 가장 많이 만들어진 대형기. 여객·화물을 가리지 않고 어디에나 투입됐다.",
         tags=["케이프궤간", "대량생산"], verified=False,
         **{"place": "Outeniqua 교통박물관, 조지", "lat": -33.9600, "lon": 22.4560}, livery="sar-black", shape="classic"),

    # ── 러시아·소련 ────────────────────────────────────────
    loco("ru-class-p36", "P36형", "Class P36",
         "Soviet Railways P36", "RU", "twilight", "4-8-4",
         built=1950, builtTo=1956, qty=251, builders=["Kolomna Locomotive Works"],
         operators=["소련 철도(SZD)"], gauge=1520, wheelName="Northern", service="express",
         weight=235.0, driver=1850, pressure=15.0, cyl=3, te=180.0, speed=125,
         withdrawn=1974, status="operational", survivors=20, iconic=True,
         highlights=["소련이 마지막으로 만든 급행 여객용 증기기관차"],
         summary="시베리아 횡단 급행을 끌던 대형 퍼시픽급. 지금도 몇 량이 관광열차로 운행하며 "
                 "붉은 별과 초록 도색이 상징이다.",
         tags=["광궤", "동태보존"], verified=False,
         **{"place": "러시아 철도박물관, 상트페테르부르크", "lat": 59.9070, "lon": 30.2950}, livery="soviet-green", shape="headlamp"),

    loco("ru-class-l", "L형", "Class L",
         "Soviet Railways L", "RU", "golden", "2-10-0",
         built=1945, builtTo=1955, qty=4200, builders=["Kolomna", "Bryansk", "Voroshilovgrad"],
         operators=["소련 철도(SZD)"], gauge=1520, wheelName="Decapod", service="freight",
         weight=190.0, driver=1500, pressure=14.0, cyl=2, te=245.0, speed=80,
         withdrawn=1980, status="operable", survivors=50,
         highlights=["전후 소련 재건을 떠받친 4,200량의 화물기"],
         summary="설계자 레베댠스키의 성을 따 'L형'. 단순하고 튼튼해 러시아 각지에서 오래 살아남았다.",
         tags=["광궤", "대량생산"], verified=False,
         **{"place": "러시아 각지 보존", "lat": 55.7940, "lon": 37.6390}, livery="soviet-black", shape="headlamp"),

    loco("ru-aa20", "AA20-1", "AA20-1",
         "Soviet Railways AA20", "RU", "golden", "4-14-4",
         no="AA20-1", built=1934, qty=1, builders=["Voroshilovgrad Locomotive Works"],
         operators=["소련 철도(SZD)"], gauge=1520, service="freight",
         weight=209.0, driver=1600, pressure=15.0, cyl=2, te=400.0, speed=70,
         withdrawn=1960, status="scrapped", survivors=0,
         highlights=["세계 유일의 4-14-4 — 동륜 7축을 강체 프레임에 배치"],
         summary="관절 없이 동륜 7축을 한 프레임에 넣은 실험작. 축거가 너무 길어 곡선에서 궤도를 밀어내는 "
                 "바람에 사실상 운용 불가 판정을 받았다. '크면 좋다'가 틀릴 수 있음을 보여준 사례.",
         tags=["실험작", "현존없음"], verified=False, livery="soviet-black", shape="headlamp"),

    loco("ru-class-e", "E형", "Class E",
         "Russian Railways E", "RU", "classic", "0-10-0",
         built=1912, builtTo=1957, qty=11000, builders=["러시아·소련·동유럽 다수 공장"],
         operators=["러시아 제국철도", "소련 철도(SZD)"], gauge=1520, service="freight",
         weight=160.0, driver=1320, pressure=12.0, cyl=2, te=225.0, speed=65,
         status="static", survivors=100,
         highlights=["약 11,000량 — 세계에서 가장 많이 만들어진 증기기관차 계열"],
         summary="45년에 걸쳐 만들어진 초장수 형식. 제정 러시아에서 시작해 소련이 끝냈다. "
                 "총 생산량 기준 세계 최다 기록.",
         tags=["대량생산", "광궤"], verified=False,
         **{"place": "러시아 각지 보존", "lat": 55.7940, "lon": 37.6390}, livery="soviet-black", shape="headlamp"),
]

LOCOS += [
    # ── 폴란드 ──────────────────────────────────────────────
    loco("pl-ol49", "Ol49형", "Ol49",
         "PKP Ol49", "PL", "twilight", "2-6-2",
         built=1951, builtTo=1954, qty=116, builders=["Fablok Chrzanów"],
         operators=["PKP"], wheelName="Prairie", service="mixed",
         weight=142.0, driver=1720, pressure=15.0, cyl=2, te=130.0, speed=100,
         status="operational", survivors=15, iconic=True,
         highlights=["볼슈틴 기관고 — 세계에서 유일하게 남았던 정기 증기 여객 운행"],
         summary="폴란드 볼슈틴에서 Ol49가 끄는 통근열차는 '박물관 운행'이 아니라 실제 시간표 열차였다. "
                 "운행 형태는 계속 바뀌므로 방문 전 최신 운행 일정 확인이 필요하다.",
         tags=["정기운행", "동태보존", "명차"], verified=True,
         sources=["https://railwayworld.net/2026/03/21/daily-steam-services-resume-at-wolsztyn/"],
         **{"place": "볼슈틴 기관고 (Parowozownia Wolsztyn)", "lat": 52.1120, "lon": 16.1200}, livery="pkp-black", shape="classic"),

    loco("pl-pm36", "Pm36-2 아름다운 헬레나", "Piękna Helena",
         "PKP Pm36", "PL", "golden", "4-6-2",
         no="Pm36-2", built=1937, qty=2, builders=["Fablok Chrzanów"], operators=["PKP"],
         wheelName="Pacific", service="express",
         weight=150.0, driver=2000, pressure=18.0, cyl=2, speed=140,
         status="operable", survivors=1,
         highlights=["1937년 파리 만국박람회 금메달"],
         summary="폴란드가 만든 유선형 퍼시픽. 2량 중 유선형 외피가 없는 2호만 살아남아 "
                 "'아름다운 헬레나'라는 별명으로 불린다.",
         tags=["유선형"], verified=False,
         **{"place": "볼슈틴 기관고", "lat": 52.1120, "lon": 16.1200}, livery="pkp-black", shape="classic"),

    loco("pl-ty51", "Ty51형", "Ty51",
         "PKP Ty51", "PL", "twilight", "2-10-0",
         built=1953, builtTo=1958, qty=232, builders=["Fablok Chrzanów"], operators=["PKP"],
         wheelName="Decapod", service="freight",
         weight=185.0, driver=1450, pressure=15.0, cyl=2, te=215.0, speed=80,
         status="static", survivors=10,
         summary="폴란드가 자국 설계로 만든 마지막 대형 화물기 계열.",
         tags=["화물"], verified=False,
         **{"place": "폴란드 각지 보존", "lat": 52.2300, "lon": 21.0100}, livery="pkp-black", shape="classic"),

    # ── 호주 ────────────────────────────────────────────────
    loco("au-c38-3801", "C38형 3801호", "NSWGR C38 Class 3801",
         "NSWGR C38", "AU", "golden", "4-6-2",
         no="3801", built=1943, builtTo=1949, qty=30, builders=["Clyde Engineering", "Cardiff Works"],
         operators=["New South Wales Government Railways"], wheelName="Pacific", service="express",
         weight=201.0, driver=1753, pressure=17.2, cyl=2, te=161.0, speed=130,
         withdrawn=1975, status="operational", survivors=4, iconic=True,
         highlights=["호주를 일주한 최초의 증기기관차 (1970)"],
         summary="유선형 노즈를 단 호주 증기의 아이콘. 3801호는 여러 차례 복원을 거쳐 지금도 시드니 근교에서 "
                 "특별열차를 끈다.",
         tags=["유선형", "동태보존", "명차"], verified=False,
         **{"place": "NSW 철도박물관, 설미어", "lat": -34.2100, "lon": 150.5600}, livery="nswgr-green", shape="streamlined"),

    loco("au-vr-r", "R형", "Victorian Railways R Class",
         "VR R Class", "AU", "twilight", "4-6-4",
         no="R707", built=1951, qty=70, builders=["North British Locomotive Company"],
         operators=["Victorian Railways"], gauge=1600, wheelName="Hudson", service="express",
         weight=200.0, driver=1854, pressure=14.5, cyl=2, te=145.0, speed=130,
         withdrawn=1974, status="operable", survivors=10,
         highlights=["1600mm 아이리시 광궤 — 세계에서 드문 궤간"],
         summary="빅토리아주 특유의 1600mm 궤간용 대형 여객기. 도입되자마자 디젤이 들어와 "
                 "가장 짧게 일한 대형 증기 중 하나가 됐다.",
         tags=["광궤"], verified=False,
         **{"place": "빅토리아주 보존 철도", "lat": -37.8140, "lon": 144.9630}, livery="vr-black", shape="classic"),

    loco("au-na-puffingbilly", "NA형 퍼핑 빌리", "Puffing Billy NA Class",
         "VR NA Class", "AU", "classic", "2-6-2T",
         built=1898, builtTo=1915, qty=17, builders=["Newport Workshops"],
         operators=["Victorian Railways", "Puffing Billy Railway"], gauge=762, service="narrow",
         weight=34.0, driver=838, pressure=11.7, cyl=2, speed=40,
         status="operational", survivors=6,
         highlights=["호주에서 가장 오래 이어진 협궤 증기 관광철도"],
         summary="멜버른 근교 단데농 산맥을 오르는 762mm 협궤 열차. 창밖으로 다리를 내놓고 타는 것으로 유명하다.",
         tags=["협궤", "동태보존"], verified=False,
         **{"place": "퍼핑 빌리 철도, 벨그레이브", "lat": -37.9080, "lon": 145.3540}, livery="vr-black", shape="victorian"),

    # ── 캐나다 ──────────────────────────────────────────────
    loco("ca-royalhudson", "로열 허드슨 2860", "Royal Hudson 2860",
         "CPR Class H1e", "CA", "golden", "4-6-4",
         no="2860", built=1940, qty=45, builders=["Montreal Locomotive Works"],
         operators=["Canadian Pacific Railway"], wheelName="Hudson", service="express",
         weight=300.0, driver=1905, pressure=19.3, cyl=2, te=201.0, speed=145,
         withdrawn=1960, status="operable", survivors=5, iconic=True,
         highlights=["1939년 국왕 조지 6세 순방 열차 견인 — '로열' 칭호 수여"],
         summary="캐나다 태평양철도의 상징. 왕실 문장을 달 수 있는 유일한 북미 기관차 계열이다.",
         tags=["명차", "동태보존"], verified=False,
         **{"place": "West Coast Railway Heritage Park, 스쿼미시", "lat": 49.7100, "lon": -123.1500}, livery="cpr-royal-hudson", shape="semi"),

    loco("ca-cn-6060", "CN 6060", "Canadian National 6060",
         "CN Class U-1-f", "CA", "golden", "4-8-2",
         no="6060", built=1944, qty=20, builders=["Montreal Locomotive Works"],
         operators=["Canadian National Railway"], wheelName="Mountain", service="mixed",
         weight=291.0, driver=1880, pressure=17.9, cyl=2, te=200.0, speed=120,
         withdrawn=1959, status="operable", survivors=5,
         summary="'불릿 노즈 베티'. 원뿔형 연기실 문 커버가 특징인 캐나다 국철의 대표 마운틴형.",
         tags=["동태보존"], verified=False,
         **{"place": "앨버타주 보존", "lat": 53.5460, "lon": -113.4940}, livery="cn-green", shape="semi"),

    # ── 스위스 ──────────────────────────────────────────────
    loco("ch-hg34", "HG 3/4형", "Furka HG 3/4",
         "DFB HG 3/4", "CH", "classic", "2-6-0T",
         built=1913, qty=10, builders=["SLM Winterthur"],
         operators=["Furka Oberalp Bahn", "Dampfbahn Furka-Bergstrecke"],
         gauge=1000, service="rack", weight=42.0, driver=910, pressure=14.0, cyl=4, speed=45,
         status="operational", survivors=8, iconic=True,
         highlights=["아프트식 치차 구간 최대 11.8% 구배 등반",
                     "1990년대 베트남에서 3량을 다시 스위스로 반입해 복원"],
         summary="푸르카 고개를 넘던 치차 기관차. 1940년대에 베트남으로 팔려갔던 차량들을 "
                 "50년 만에 되찾아와 복원한 이야기로 유명하다.",
         tags=["치차", "협궤", "동태보존", "명차"], verified=False,
         **{"place": "Dampfbahn Furka-Bergstrecke, 레알프", "lat": 46.5900, "lon": 8.4800}, livery="sbb-black", shape="classic"),

    loco("ch-e33", "E 3/3 티거리", "E 3/3 Tigerli",
         "SBB E 3/3", "CH", "classic", "0-6-0T",
         built=1894, builtTo=1917, qty=100, builders=["SLM Winterthur"], operators=["SBB"],
         service="tank", weight=40.0, driver=1030, pressure=12.0, cyl=2, speed=45,
         status="operable", survivors=20,
         summary="스위스 역 구내 입환의 표준 소형 탱크기. '작은 호랑이'라는 애칭으로 불렸다.",
         tags=["탱크식"], verified=False,
         **{"place": "스위스 각지 보존", "lat": 47.0500, "lon": 8.3100}, livery="sbb-black", shape="classic"),

    # ── 아르헨티나 · 이탈리아 ───────────────────────────────
    loco("ar-latrochita", "라 트로치타", "La Trochita",
         "Ferrocarril Esquel Baldwin/Henschel 2-8-2", "AR", "golden", "2-8-2",
         built=1922, qty=75, builders=["Baldwin Locomotive Works", "Henschel"],
         operators=["Ferrocarriles Argentinos", "Viejo Expreso Patagónico"],
         gauge=750, wheelName="Mikado", service="narrow",
         weight=52.0, driver=825, pressure=12.0, cyl=2, speed=45,
         status="operational", survivors=20, iconic=True,
         highlights=["파타고니아 750mm 협궤 — 폴 서루의 여행기로 세계에 알려짐"],
         summary="에스켈에서 출발하는 파타고니아 협궤 증기열차. 관광용으로 남은 것이 아니라 "
                 "오랫동안 실제 생활 노선이었다는 점이 특별하다.",
         tags=["협궤", "동태보존", "명차"], verified=False,
         **{"place": "에스켈, 추부트주", "lat": -42.9110, "lon": -71.3200}, livery="fcaf-black", shape="classic"),

    loco("it-fs685", "FS 685형", "FS Class 685",
         "FS 685", "IT", "classic", "2-6-2",
         built=1912, builtTo=1928, qty=271, builders=["Breda", "Ansaldo"],
         operators=["Ferrovie dello Stato"], wheelName="Prairie", service="express",
         weight=131.0, driver=1850, pressure=12.0, cyl=4, speed=110,
         withdrawn=1975, status="static", survivors=5,
         highlights=["카프로티(Caprotti) 밸브기어를 적용한 형식이 다수"],
         summary="이탈리아 간선 급행의 주력. 자동차 엔진식 포핏 밸브를 증기기관차에 옮긴 "
                 "카프로티 밸브기어의 실험장이기도 했다.",
         tags=["밸브기어"], verified=False,
         **{"place": "피에트라르사 국립철도박물관, 나폴리", "lat": 40.8100, "lon": 14.2900}, livery="fs-black", shape="classic"),
]


# ─────────────────────────────────────────────────────────────
# 검증 + 출력
# ─────────────────────────────────────────────────────────────
# 탱크식(Whyte 에 T)인데 실제로 탄수차를 끄는 예외. 페어리 퀸은 2-2-2WT(웰탱크)지만
# 석탄용 2축 소형 탄수차를 달고 다닌다 — 도식도 그렇게 그려야 맞다.
TANK_WITH_TENDER = {"in-fairyqueen"}

VALID_STATUS = {"operational", "operable", "static", "restoration", "scrapped", "replica"}
VALID_SERVICE = {"express", "mixed", "freight", "tank", "articulated", "narrow", "rack"}
VALID_ERAS = {e["id"] for e in ERAS}
VALID_COUNTRIES = {c[0] for c in COUNTRIES}


def era_for(year):
    """제작 시작 연도 → 시대 id. 구간 밖(1804 이전)이면 None."""
    for e in ERAS:
        if e["from"] <= year <= e["to"]:
            return e["id"]
    return None


def assign_eras(locos):
    """시대(era)는 손으로 적은 값이 아니라 **제작 시작 연도로 계산**한다.

    초안의 era 는 참고용일 뿐이다. 대조본이 builtFrom 을 바로잡으면(예: JF1 1918) 시대도 따라가야
    연표에서 '1920–1945' 머리글 아래 1918년 차가 서는 일이 없다. 바뀐 id 목록을 돌려준다.
    """
    moved = []
    for l in locos:
        bf = l["builtFrom"]
        if bf is None:
            continue
        e = era_for(bf)
        if e and e != l["era"]:
            moved.append((l["id"], l["era"], e, bf))
            l["era"] = e
    return moved


def validate(locos):
    errs = []
    for l in locos:
        p = f"[{l['id']}]"
        if l["status"] not in VALID_STATUS:
            errs.append(f"{p} status 값 오류: {l['status']}")
        if l["serviceType"] not in VALID_SERVICE:
            errs.append(f"{p} serviceType 값 오류: {l['serviceType']}")
        if l["era"] not in VALID_ERAS:
            errs.append(f"{p} era 값 오류: {l['era']}")
        if l["countryCode"] not in VALID_COUNTRIES:
            errs.append(f"{p} countryCode 미등록: {l['countryCode']}")
        bf, bt = l["builtFrom"], l["builtTo"]
        if bf and bt and bt < bf:
            errs.append(f"{p} builtTo({bt}) < builtFrom({bf})")
        if bf and l["withdrawnYear"] and l["withdrawnYear"] < bf:
            errs.append(f"{p} withdrawnYear가 제작연도보다 이름")
        # era 구간과 제작연도 정합성 — 여유 없이 정확히. (연표가 era 로 묶고 그 안에서 연도순으로
        # 늘어놓으므로, 1918년 차가 '1920–1945' 머리글 아래 서면 그대로 오류로 보인다)
        era = next(e for e in ERAS if e["id"] == l["era"])
        if bf and not (era["from"] <= bf <= era["to"]):
            errs.append(f"{p} 제작연도 {bf}가 era '{l['era']}'({era['from']}~{era['to']}) 범위 밖")
        if l["status"] == "scrapped" and (l["survivors"] or 0) > 0:
            errs.append(f"{p} scrapped인데 survivors>0")
        if l["status"] == "scrapped" and l["location"]:
            errs.append(f"{p} scrapped인데 보존 위치가 지정됨")
        if l["status"] in ("operational", "operable", "static") and l["survivors"] == 0:
            errs.append(f"{p} 보존 상태인데 survivors=0")
        loc = l["location"]
        if loc:
            if not (-90 <= loc["lat"] <= 90) or not (-180 <= loc["lon"] <= 180):
                errs.append(f"{p} 좌표 범위 오류")
        sp = l["specs"]
        if sp["topSpeedKmh"] and sp["topSpeedKmh"] > 210:
            errs.append(f"{p} 최고속도 {sp['topSpeedKmh']} — 세계기록(202.8)보다 큼, 확인 필요")
        if sp["driverDiameterMm"] and not (500 <= sp["driverDiameterMm"] <= 2600):
            errs.append(f"{p} 동륜 직경 이상: {sp['driverDiameterMm']}")
        if l["gaugeMm"] not in (610, 750, 762, 1000, 1067, 1219, 1321, 1435, 1520, 1600, 1676):
            errs.append(f"{p} 궤간 확인 필요: {l['gaugeMm']}")
        ta = l["tenderAxles"]
        if ta is not None and not (0 <= ta <= 8):
            errs.append(f"{p} 탄수차 차축 수 범위 이상: {ta}")
        if ta and ("T" in l["wheel"]["whyte"].upper() or "+" in l["wheel"]["whyte"]) \
                and l["id"] not in TANK_WITH_TENDER:
            errs.append(f"{p} 탱크식/가라트인데 탄수차가 지정됨")
        if l["livery"] is None:
            errs.append(f"{p} livery 미지정")
        elif l["livery"] not in {x[0] for x in LIVERIES}:
            errs.append(f"{p} 등록되지 않은 livery: {l['livery']}")
        if l["serviceType"] == "tank" and "T" not in l["wheel"]["whyte"].upper():
            errs.append(f"{p} serviceType=tank 인데 Whyte 표기에 T가 없음 "
                        f"({l['wheel']['whyte']}) — 탄수차가 그려지지 않는다")
        if sp.get("weightBasis") not in (None, "loco", "locoAndTender"):
            errs.append(f"{p} weightBasis 값 오류: {sp.get('weightBasis')}")
        if sp.get("weightBasis") and sp["weightT"] is None:
            errs.append(f"{p} 중량이 없는데 weightBasis 만 지정됨")
        if "T" in l["wheel"]["whyte"].upper() and l["tenderAxles"] not in (None, 0) \
                and l["id"] not in TANK_WITH_TENDER:
            errs.append(f"{p} 탱크식(T)인데 tenderAxles={l['tenderAxles']}")
        if l["shape"] is None:
            errs.append(f"{p} shape 미지정")
        elif l["shape"] not in {x[0] for x in SHAPES}:
            errs.append(f"{p} 등록되지 않은 shape: {l['shape']}")

    for table, key, label in ((LIVERIES, "livery", "livery"), (SHAPES, "shape", "shape")):
        ids = [x[0] for x in table]
        if len(ids) != len(set(ids)):
            errs.append(f"{label} 표에 중복 id가 있음")
        unused = set(ids) - {l[key] for l in locos}
        if unused:
            errs.append(f"쓰이지 않는 {label}: {', '.join(sorted(unused))}")
    return errs


def main():
    os.makedirs(OUT, exist_ok=True)
    # 초안(LOCOS) 위에 출처로 확인한 값(tools/verified.py)을 덧씌운 뒤 검증한다.
    import verified
    fixed = verified.apply(LOCOS)
    unused_q = apply_map_queries(LOCOS)   # 장소명이 확정된 뒤(대조본 적용 후)에 검색어를 붙인다
    era_moved = assign_eras(LOCOS)        # 시대는 (대조본 적용 후의) 제작 시작 연도로 결정한다
    errs = validate(LOCOS)
    errs += [f"MAP_QUERIES 에 있는데 어느 장소명과도 맞지 않는 키: {k!r}" for k in unused_q]
    if errs:
        print("검증 실패:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    used = {l["countryCode"] for l in LOCOS}
    countries = [c for c in country_objs() if c["code"] in used]
    # 서적·논문·공식 자료 (tools/references.py) — 웹 출처(sources)와 별도
    import references
    n_loco_refs, n_country_refs = references.attach(LOCOS, countries)

    payload = {
        "schemaVersion": 1,
        "generatedBy": "tools/build_seed.py",
        "eras": ERAS,
        "liveries": livery_objs(),
        "shapes": shape_objs(),
        # 여러 나라에 걸친 종합 문헌. 국가별 문헌은 countries.json 의 references, 기관차별은 각 항목의 references.
        "references": references.GENERAL,
        "locomotives": LOCOS,
    }
    with open(os.path.join(OUT, "locomotives.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, "countries.json"), "w", encoding="utf-8") as f:
        json.dump({"schemaVersion": 1, "countries": countries}, f, ensure_ascii=False, indent=2)

    print(f"기관차 {len(LOCOS)}량 / 국가 {len(countries)}개 저장 완료")
    for c in sorted(countries, key=lambda x: x["code"]):
        n = sum(1 for l in LOCOS if l["countryCode"] == c["code"])
        print(f"  {c['flag']} {c['nameKo']:<10} {n:>2}량")
    print(f"  도색(livery) {len(LIVERIES)}종 · 실루엣(shape) {len(SHAPES)}종 사용")
    print(f"  출처 대조본 적용: {fixed}량 (tools/verified.py)")
    print(f"  참고문헌: 기관차별 {n_loco_refs}량 · 국가별+종합 {n_country_refs}건 (tools/references.py)")
    n_loc = sum(1 for l in LOCOS if l["location"])
    n_q = sum(1 for l in LOCOS if l["location"] and l["location"]["query"])
    print(f"  보존 위치 {n_loc}곳 · 지도 앱 검색어 있음 {n_q}곳 (나머지는 좌표 핀 + 라벨)")
    if era_moved:
        print("  시대 재배정(제작연도 기준): " + ", ".join(f"{i} {a}→{b} ({y})" for i,a,b,y in era_moved))
    print(f"  검증완료(verified=true): {sum(1 for l in LOCOS if l['verified'])}량")
    print(f"  대표 명차(iconic): {sum(1 for l in LOCOS if l['iconic'])}량")


if __name__ == "__main__":
    main()
