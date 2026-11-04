#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Atlas — 출처 대조본(verified overlay)

build_seed.py 의 LOCOS 는 '초안'이다. 이 파일은 그 초안 위에 **웹 출처로 직접 확인한 값만**
덧씌운다. 값 하나마다 왜 그렇게 고쳤는지(`_why`)와 어디서 봤는지(`_src`)를 남겨 두므로,
나중에 다른 값이 들어와도 무엇이 확인된 값인지 구분할 수 있다.

    - 키: 기관차 id (build_seed.LOCOS 의 id)
    - 값: {"필드.경로": 값, ..., "_why": "...", "_src": [url, ...], "_verified": False}
        * "필드.경로" 는 점 표기. 예) "specs.weightT", "wheel.whyte", "nameKo"
        * 값이 None 이면 '확인 불가 → 비움' 이라는 뜻이다(초안의 추정치를 지운다).
        * _verified 를 명시하지 않으면 True 로 찍힌다. 출처끼리 충돌해 확정할 수 없으면 False.
        * _src 는 확인에 쓴 출처 링크. 앱 화면에는 나가지 않는다(화면의 출처는 원고의 번호 붙은 출처).

여기 없는 기관차는 초안 그대로 나가고 verified=False 로 남는다.

덧씌우는 순서: VERIFIED(1차, 2026-09-12) → RECHECK(재대조, 2026-09-16~17) → RESEARCH(자료조사 원고, 2026-10-23).
앞의 두 대조본에 남아 있는 이름·별명·위치 값은 기록으로 둔 것이다. 지금은 원고(tools/manuscript/entries.json)가
이름·별명·위치·설명 글을 정하고, build_seed.py 가 덧씌우기가 끝난 뒤 원고를 병합한다.
"""

KO = "https://ko.wikipedia.org/wiki/"
EN = "https://en.wikipedia.org/wiki/"
DE = "https://de.wikipedia.org/wiki/"

VERIFIED = {
    # ── 한국 ──────────────────────────────────────────────────────
    "kr-moga": {
        "wheel.whyte": "2-6-0T", "serviceType": "tank", "tenderAxles": 0,
        "specs.topSpeedKmh": 55, "specs.weightT": None,
        "_why": "모가형은 탄수차가 없는 탱크식(2-6-0T)이다. 초안이 탄수차식으로 잘못 그려졌었다. "
                "중량은 출처마다 달라 비움.",
        "_src": [KO + "모가형_증기_기관차", EN + "Sentetsu_Mogai-class"],
    },
    "kr-mika3-129": {
        "builtFrom": 1940, "builtTo": 1940, "quantityBuilt": None,
        "specs.weightT": 90.65, "specs.weightBasis": "loco",
        "specs.driverDiameterMm": 1400, "specs.topSpeedKmh": 70,
        "highlights": ["한국전쟁 당시 특별공작대 수송 임무로 알려진 기관차",
                       "2025년 6월 진위 논란으로 국가등록문화유산(제415호) 지위 상실"],
        "_why": "129호는 1940년 제작 1량이므로 '형식 총 생산량'은 이 항목에 쓰지 않는다. "
                "중량은 기관차 단독 기준.",
        "_src": [KO + "미카형_증기기관차_129호", EN + "Sentetsu_Mikasa-class"],
    },
    "kr-mika3-161": {
        "quantityBuilt": None, "specs.weightT": 90.65, "specs.weightBasis": "loco",
        "specs.driverDiameterMm": 1400, "specs.topSpeedKmh": 70,
        "_verified": False,
        "_why": "제작연도가 출처마다 1939/1940 으로 갈려 확정 보류.",
        "_src": [KO + "미카형_증기_기관차", EN + "Sentetsu_Mikasa-class"],
    },
    "kr-pashi5": {
        "builtFrom": 1939, "builtTo": 1944,
        "specs.weightT": 112.0, "specs.weightBasis": "loco", "specs.driverDiameterMm": 1850,
        "_why": "파시5형(Pashiko) 제작 기간·동륜 직경을 출처대로.",
        "_src": [EN + "Sentetsu_Pashiko-class"],
    },
    "kr-teou": {
        "builtFrom": 1906, "builtTo": 1906, "quantityBuilt": None, "tenderAxles": 3,
        "specs.weightT": 78.1, "specs.weightBasis": "loco",
        "specs.driverDiameterMm": 1680, "specs.topSpeedKmh": 95,
        "_verified": False,
        "_why": "터우형은 여러 하위 형식(터우1~6)의 총칭이라 대표값을 하나로 고정하기 어렵다. "
                "터우1형(Tehoi) 기준으로 적고 보류.",
        "_src": [KO + "터우형_증기_기관차", EN + "Sentetsu_Tehoi-class"],
    },
    "kr-hyeogi": {
        "nameKo": "혀기8형", "nameEn": "Hyeogi-8 (Narrow Gauge)", "classDesignation": "혀기8형 (Hyeogi-8)",
        "wheel.whyte": "2-8-2T", "serviceType": "tank", "tenderAxles": 0,
        "builtFrom": 1934, "builtTo": 1936, "withdrawnYear": 1972, "specs.topSpeedKmh": None,
        "builders": ["히타치", "니혼샤료"],
        "location": {"name": "국립어린이과학관 야외 전시, 서울 종로 — 혀기8형 28호", "lat": 37.5797, "lon": 126.9962},
        "summary": "혀기형은 수인선·수여선 등 762mm 협궤 노선에서 쓰인 소형 기관차 계열(혀기1~11형)의 총칭으로, "
                   "혀기11형을 제외하면 모두 탄수차 없는 탱크식이다. 그중 혀기8형은 2-8-2T 배치의 주력 형식(60량 이상)으로 "
                   "1934~1972년 운행했고, 28호가 협궤 객차와 함께 보존되어 있다.",
        "highlights": ["수인선·수여선 등 762mm 협궤 노선용", "혀기11형(2-8-2, 탄수차식) 13호는 철도박물관 이관 예정"],
        "_verified": False,
        "_why": "혀기8형은 탄수차가 없는 탱크식 2-8-2T(초안은 탄수차식). 형식별 상세는 한국어 위키백과에 없어 "
                "나무위키(사용자 편집)로 보강했으므로 확정하지 않음.",
        "_src": [KO + "혀기형_증기_기관차", "https://namu.wiki/w/혀기형 증기기관차"],
    },

    # ── 일본 ──────────────────────────────────────────────────────
    "jp-class150": {
        "wheel.whyte": "2-4-0T", "serviceType": "tank", "tenderAxles": 0,
        "specs.weightT": 16.5, "specs.weightBasis": "loco",
        "specs.driverDiameterMm": 1321, "specs.topSpeedKmh": 40,
        "_why": "150형(1호 기관차)은 탱크식 2-4-0T. 초안은 탄수차식으로 잘못 그려졌다.",
        "_src": [EN + "JGR_Class_150"],
    },
    "jp-8620": {"quantityBuilt": 672, "specs.topSpeedKmh": 90,
                "_why": "국내용 672량(대만·사할린용 제외).", "_src": [EN + "JNR_Class_8620"]},
    "jp-d51": {"specs.weightBasis": "locoAndTender", "_why": "중량은 기관차+탄수차 운전정비중량.",
               "_src": [EN + "JNR_Class_D51"]},
    "jp-c57": {"specs.weightBasis": "locoAndTender", "_why": "중량은 기관차+탄수차 운전정비중량.",
               "_src": [EN + "JNR_Class_C57"]},
    "jp-c58": {"specs.weightBasis": "locoAndTender", "_why": "중량은 기관차+탄수차 운전정비중량.",
               "_src": [EN + "JNR_Class_C58"]},
    "jp-c62": {"specs.weightBasis": "locoAndTender", "_why": "중량은 기관차+탄수차 운전정비중량.",
               "_src": [EN + "JNR_Class_C62"]},
    "jp-c11": {"_why": "2-6-4T 탱크식·제원 확인, 변경 없음.", "_src": [EN + "JNR_Class_C11"]},
    "jp-9600": {"_why": "9600형 제원 확인, 변경 없음.", "_src": [EN + "JNR_Class_9600"]},

    # ── 영국 ──────────────────────────────────────────────────────
    "gb-trevithick-pendarren": {
        "gaugeMm": 1321, "specs.weightT": 5.0, "specs.weightBasis": "loco",
        "specs.driverDiameterMm": 914,
        "_why": "페니다렌 트램로드는 4ft 4in(1,321mm) 궤간. 표준궤가 아니다.",
        "_src": [EN + "Penydarren_locomotive"],
    },
    "gb-locomotion-1": {"specs.weightBasis": "loco", "specs.driverDiameterMm": 1219,
                        "_why": "동륜 4ft(1,219mm).", "_src": [EN + "Locomotion_No._1"]},
    "gb-gwr-king": {"specs.driverDiameterMm": 1981,
                    "_why": "킹급 동륜은 6ft 6in(1,981mm).", "_src": [EN + "GWR_6000_Class"]},
    "gb-lms-duchess": {"tenderAxles": 3,
                       "_why": "스태니어 표준 탄수차는 3축(6륜).", "_src": [EN + "LMS_Princess_Coronation_Class"]},
    "gb-br-britannia": {"builtTo": 1954,
                        "_why": "브리타니아급 제작 1951~1954.", "_src": [EN + "BR_Standard_Class_7"]},
    "gb-lms-black5": {"_why": "제원 확인, 변경 없음.", "_src": [EN + "LMS_Stanier_Class_5_4-6-0"]},
    "gb-lner-a3-flyingscotsman": {"_why": "제원 확인, 변경 없음.",
                                  "_src": [EN + "LNER_Class_A3_4472_Flying_Scotsman"]},
    "gb-lner-a4-mallard": {"_why": "제원 확인, 변경 없음.", "_src": [EN + "LNER_Class_A4_4468_Mallard"]},
    "gb-a1-tornado": {"_why": "제원 확인, 변경 없음.", "_src": [EN + "LNER_Peppercorn_Class_A1_60163_Tornado"]},
    "gb-rocket": {"_why": "0-2-2·제원 확인, 변경 없음.", "_src": [EN + "Stephenson%27s_Rocket"]},

    # ── 미국 ──────────────────────────────────────────────────────
    "us-nyc-hudson": {
        "shape": "american", "livery": "nyc-black",
        "specs.weightT": 356.3, "specs.weightBasis": "locoAndTender", "specs.topSpeedKmh": 177,
        "designer": "Paul Kiefer (설계) / Henry Dreyfuss (유선형 10량 외장)",
        "tags": ["현존없음", "명차"],
        "summary": "1937~38년 제작된 J-3a 50량 중 '20세기 특급' 전용 10량(5445~5454)만 헨리 드레이퍼스의 "
                   "유선형 외장을 받았고, 나머지 40량은 일반 외형의 검은 기관차였다. 디젤 전환이 워낙 빨라 "
                   "보존 논의가 시작되기도 전에 전량 고철이 됐다.",
        "_why": "유선형은 50량 중 10량뿐이므로 형식 대표 실루엣·도색은 일반형(검정)으로. "
                "설계자는 폴 키퍼, 드레이퍼스는 외장 디자인.",
        "_src": [EN + "New_York_Central_Hudson"],
    },
    "us-co-allegheny": {
        "specs.driverDiameterMm": 1702, "tenderAxles": 7, "specs.topSpeedKmh": 113,
        "specs.weightBasis": "locoAndTender", "_verified": False,
        "_why": "동륜 67in(1,702mm), 탄수차 7축. 출력·중량은 출처마다 달라 보류.",
        "_src": [EN + "Chesapeake_and_Ohio_class_H-8"],
    },
    "us-milw-classa": {"builtTo": 1937, "specs.weightBasis": "locoAndTender",
                       "_why": "A형 4량은 1935~1937 제작.", "_src": [EN + "Milwaukee_Road_class_A"]},
    "us-atsf-3751": {"specs.weightT": 396.6, "specs.weightBasis": "locoAndTender",
                     "specs.topSpeedKmh": 145, "tenderAxles": 6,
                     "_why": "중량은 기관차+탄수차. 탄수차 6축.", "_src": [EN + "Santa_Fe_3751"]},
    "us-nw-611": {"builtFrom": 1941, "builtTo": 1950,
                  "specs.weightT": 403.4, "specs.weightBasis": "locoAndTender",
                  "_why": "J형 14량은 1941~1950 제작(611호는 1950).", "_src": [EN + "Norfolk_and_Western_611"]},
    "us-sp-4449": {"builtTo": 1942, "specs.weightT": 394.6, "specs.weightBasis": "locoAndTender",
                   "_why": "GS-4 는 1941~1942 제작.", "_src": [EN + "Southern_Pacific_4449"]},
    "us-prr-k4": {"specs.topSpeedKmh": 140, "specs.weightBasis": "locoAndTender",
                  "_why": "공식 최고속도 표기 기준.", "_src": [EN + "Pennsylvania_Railroad_class_K4s"]},
    "us-nw-y6b": {"specs.weightT": None, "_verified": False,
                  "_why": "중량이 출처마다 크게 달라 비움."},
    "us-up-bigboy-4014": {"specs.weightBasis": "locoAndTender",
                          "_why": "중량은 기관차+탄수차.", "_src": [EN + "Union_Pacific_Big_Boy"]},
    "us-up-844": {"tenderAxles": 7, "specs.weightBasis": "locoAndTender",
                  "_why": "센티페드 탄수차 7축(4-10-0 배치).", "_src": [EN + "Union_Pacific_844"]},

    # ── 독일 ──────────────────────────────────────────────────────
    "de-adler": {"specs.weightT": 14.3, "specs.weightBasis": "loco",
                 "_why": "기관차 단독 중량.", "_src": [EN + "Adler_(locomotive)"]},
    "de-drg-05": {"builtTo": 1937, "specs.weightBasis": "locoAndTender",
                  "_why": "05 001~003 은 1935~1937 제작.", "_src": [EN + "DRG_Class_05"]},
    "de-drg-01": {"specs.weightBasis": "locoAndTender", "_why": "중량은 기관차+탄수차.",
                  "_src": [EN + "DRG_Class_01"]},
    "de-drg-52": {
        "nameKo": "52형", "nameEn": "DRB Class 52", "classDesignation": "DRB Baureihe 52",
        "nickname": "전시표준형 (Kriegslok)", "builtTo": 1951,
        "specs.weightT": 142.7, "specs.weightBasis": "locoAndTender",
        "_why": "공식 형식명은 DRB 52형. '전시표준형(Kriegslok)'은 별명이라 별명 칸으로. "
                "전후 생산분까지 1942~1951.",
        "_src": [EN + "DRB_Class_52"],
    },
    "de-drg-44": {"nickname": "점보 (Jumbo)", "specs.weightT": 110.2, "specs.weightBasis": "loco",
                  "_why": "기관차 단독 중량. 별명 '점보'.", "_src": [EN + "DRG_Class_44"]},
    "de-drg-0310": {"shape": "classic", "specs.weightT": 181.7, "specs.weightBasis": "locoAndTender",
                    "_why": "유선형 외장은 전후 모두 철거됐고 보존기도 일반형이라 대표 실루엣은 일반형.",
                    "_src": [EN + "DRG_Class_03.10"]},
    "de-dr-18201": {"classDesignation": "DR 18 201", "livery": "dr-green",
                    "specs.weightT": 186.8, "specs.weightBasis": "locoAndTender",
                    "_why": "형식명이 아니라 단일 차호(18 201). 현재 도색은 DR 그린(2002년 이후 잠시 빨간색이었던 적 있음).",
                    "_src": [EN + "DR_18_201"]},
    "de-br-10": {"nickname": "검은 백조 (Schwarze Schwäne)",
                 "specs.weightT": 208.0, "specs.weightBasis": "locoAndTender",
                 "_why": "별명 '검은 백조'. 중량은 기관차+탄수차.", "_src": [EN + "DB_Class_10"]},

    # ── 프랑스 ────────────────────────────────────────────────────
    "fr-242a1": {"specs.topSpeedKmh": 130, "specs.weightT": 226.0, "specs.weightBasis": "locoAndTender",
                 "_why": "인가 최고속도 130km/h. 중량은 기관차+탄수차.", "_src": [EN + "SNCF_242A1"]},
    "fr-241p": {"nickname": "grosses P", "_why": "별명 'grosses P'.", "_src": [EN + "SNCF_Class_241P"]},
    "fr-231e": {
        "nameEn": "Nord 231 E", "classDesignation": "Nord 231 E / SNCF 2-231 E",
        "nickname": "샤플롱 퍼시픽", "builtFrom": 1934, "builtTo": 1938, "quantityBuilt": 48, "survivors": 2,
        "builders": ["PO 3500형 개조 20량 (1934)", "Nord 신조 28량 (1936~38)"],
        "location": {"name": "Cité du Train, 뮐루즈 — 231 E 22", "lat": 47.749, "lon": 7.321},
        "highlights": ["기존 퍼시픽을 개조해 출력을 약 두 배로 끌어올린 개량의 교과서",
                       "노르(Nord)철도가 PO 3500형 개조 20량을 사들이고 28량을 신조 — 총 48량",
                       "보존 2량: 231 E 22(뮐루즈 Cité du Train)·231 E 41(생피에르데코르, AAATV)"],
        "_why": "231 E 는 PO 개조기가 아니라 노르(Nord)철도가 도입한 샤플롱 퍼시픽. 개조 20 + 신조 28 = 48량, "
                "보존 2량으로 프랑스어 위키 형식 문서에서 확정.",
        "_src": ["https://fr.wikipedia.org/wiki/231_Nord_3.1111_%C3%A0_3.1130_et_3.1171_%C3%A0_3.1198"],
    },
    "fr-crampton": {"classDesignation": "Est n° 80 «Le Continent» (크램프턴식)", "_verified": False,
                    "_why": "'크램프턴'은 형식이 아니라 방식 이름. 보존기는 동부철도 80호 '르 콩티낭'. "
                            "제원은 개체별로 달라 보류.",
                    "_src": [EN + "Crampton_locomotive"]},
    "fr-140c": {"_why": "제원 확인, 변경 없음."},

    # ── 폴란드 ────────────────────────────────────────────────────
    "pl-ol49": {"specs.driverDiameterMm": 1750, "specs.weightT": 145.3, "specs.weightBasis": "locoAndTender",
                "_why": "동륜 1,750mm. 중량은 기관차+탄수차.", "_src": [EN + "PKP_class_Ol49"]},
    "pl-pm36": {"nameKo": "Pm36-2", "nameEn": "PKP Pm36", "nickname": "아름다운 헬레나 (Piękna Helena)",
                "specs.topSpeedKmh": 130,
                "_why": "'아름다운 헬레나'는 Pm36-2 의 별명. 이름 칸에서 별명 칸으로.",
                "_src": [EN + "PKP_class_Pm36"]},
    "pl-ty51": {"specs.weightT": 188.9, "specs.weightBasis": "locoAndTender",
                "_why": "중량은 기관차+탄수차.", "_src": [EN + "PKP_class_Ty51"]},

    # ── 스위스 · 이탈리아 ─────────────────────────────────────────
    "ch-hg34": {"classDesignation": "BFD HG 3/4", "builtTo": 1914, "specs.weightBasis": "loco",
                "_why": "원 소속은 브리크-푸르카-디센티스(BFD)철도. 1913~1914 제작."},
    "ch-e33": {"nameKo": "E 3/3", "nameEn": "SBB E 3/3", "nickname": "티거리 (Tigerli)",
               "builtFrom": 1896, "builtTo": 1915, "quantityBuilt": 118,
               "specs.weightT": 33.6, "specs.weightBasis": "loco", "specs.driverDiameterMm": 1040,
               "_why": "'티거리'는 별명. 1896~1915 118량.", "_src": [DE + "SBB_E_3/3"]},
    "it-fs685": {"classDesignation": "FS Gruppo 685", "specs.topSpeedKmh": 120, "_verified": False,
                 "_why": "이탈리아 표기는 Gruppo. 하위 형식(685.0/1/5…)별 수치 차이가 있어 보류.",
                 "_src": [EN + "FS_Class_685"]},
    # ── 중국 ──────────────────────────────────────────────────────
    "cn-qj": {
        "quantityBuilt": 4717, "tenderAxles": 6,
        "specs.weightT": 133.8, "specs.weightBasis": "loco", "specs.boilerPressureBar": 14.7,
        "specs.tractiveEffortKn": 326.5, "survivors": 25, "status": "static",
        "_why": "4,717량. 양산형 기관차 중량 133.8t(단독), 12륜(6축) 탄수차. 보존 25량(중국 21·미국 3·독일 1). "
                "정기 운행 중인 개체는 확인되지 않아 정태보존으로.",
        "_src": [EN + "China_Railways_QJ"],
    },
    "cn-js": {
        "builtFrom": 1957, "builtTo": 1988, "quantityBuilt": 1916, "tenderAxles": 4,
        "specs.weightT": 104.0, "specs.weightBasis": "loco", "specs.boilerPressureBar": 15.0,
        "specs.tractiveEffortKn": 250.0, "specs.topSpeedKmh": 85, "survivors": 30,
        "builders": ["다롄 기관차공장", "치수옌 기관차공장", "다퉁 기관차공장", "베이징 2·7 공장"],
        "_why": "1957~65·1981~88 두 차례 생산 1,916량. 중량 104t(단독). 보존 30량, 미국 스트라스버그·분 앤 시닉 밸리에서 2량 운행.",
        "_src": [EN + "China_Railways_JS"],
    },
    "cn-sy": {
        "livery": "cr-black", "specs.weightT": 84.0, "specs.weightBasis": "loco",
        "specs.boilerPressureBar": 14.0, "specs.tractiveEffortKn": 200.8, "survivors": 61,
        "builders": ["탕산 기관차공장", "창춘·지난·퉁링 공장 외"],
        "highlights": ["1999년 10월 탕산에서 완성된 SY-1772 — 중국 국철용으로 만들어진 마지막 증기기관차"],
        "_verified": False,
        "_why": "제원·수량·보존(61량, 미국 2량 운행)은 출처 확인. 도색은 출처에 없음 — 현역 사진 대부분 검정이라 "
                "검정으로 두되 확정하지 않음(초안의 녹색은 근거 없음).",
        "_src": [EN + "China_Railways_SY"],
    },
    "cn-jf": {
        "nameKo": "제팡(解放) JF1형", "nameEn": "JF1 Class", "classDesignation": "China Railways JF1 (원 만철 ミカイ 계열)",
        "roadNumber": "JF1-304 (毛泽东号)", "quantityBuilt": 2095, "survivors": 13,
        "builders": ["ALCO", "가와사키", "히타치", "쓰팡·다롄·치치하얼 공장 (전후 475량)"],
        "specs.weightT": 103.85, "specs.weightBasis": "loco", "specs.driverDiameterMm": 1370,
        "specs.boilerPressureBar": 14.0, "specs.tractiveEffortKn": 235.6, "specs.topSpeedKmh": 80,
        "_why": "JF 는 하위 형식(JF1~JF51)의 총칭이라 대표 형식인 JF1(구 만철 미카이 계열, 毛泽东号 포함)로 항목을 좁혔다. "
                "JF1 합계 2,095량(전후 475량 포함), 제원은 JF1 문서 기준. 보존은 JF 계열 13량(중국 9·한국 4).",
        "_src": [EN + "China_Railways_JF1", EN + "China_Railways_JF"],
    },
    "cn-km": {
        "nameKo": "KF형", "nameEn": "KF Class", "classDesignation": "China Railways KF (원 중화민국 철도부 600계)",
        "builtFrom": 1935, "builtTo": 1936, "withdrawnYear": 1977,
        "specs.weightT": 259.5, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 15.2,
        "specs.tractiveEffortKn": 160.5, "specs.topSpeedKmh": 120,
        "location": {"name": "국립철도박물관, 요크 (NRM York) — KF7", "lat": 53.9603, "lon": -1.0951},
        "highlights": ["영국(벌컨 파운드리)이 중국을 위해 설계·제작한 4-8-4 24량",
                       "KF7(원 607호)은 1983년 영국으로 돌아가 요크 국립철도박물관에, KF1은 베이징 중국철도박물관에 보존"],
        "summary": "영국 설계·영국 제작으로 중국에서 40년 넘게 일한 기관차. 마지막에 한 량이 고향 영국으로 돌아가 "
                   "요크 국립철도박물관에 전시되고 있다는 점이 특이하다.",
        "_why": "'KD'는 별개 형식(2-8-0 계열)이라 이름에서 제거. 최고속도 120km/h, 총중량 259.5t. "
                "보존기 KF7 은 런던 과학박물관이 아니라 요크 NRM 에 있다.",
        "_src": [EN + "China_Railways_KF"],
    },

    # ── 인도 ──────────────────────────────────────────────────────
    "in-fairyqueen": {
        "wheel.whyte": "2-2-2WT", "gaugeMm": 1676, "quantityBuilt": None,
        "specs.weightT": 26.0, "specs.weightBasis": "loco", "specs.driverDiameterMm": 1829,
        "highlights": ["1998년 기네스북 등재 — 정기 운행 중인 세계 최고령 증기기관차 (1855년 제작)",
                       "1909년 퇴역 후 1997년 복원, 델리~알와르 유산열차 운행",
                       "웰탱크(WT)식이지만 석탄용 소형 탄수차를 달고 다닌다"],
        "_why": "공식 배치는 2-2-2WT(웰탱크). 다만 실제로 2축 소형 탄수차를 끌기 때문에 도식에는 탄수차를 그린다. "
                "궤간은 인도 광궤 1,676mm(초안 1,435 오류). 동륜 1,829mm.",
        "_src": [EN + "Fairy_Queen_(locomotive)"],
    },
    "in-dhr-b": {
        "builtTo": 1925, "builders": ["Sharp, Stewart", "North British", "Baldwin", "DHR Tindharia Works"],
        "specs.tractiveEffortKn": 34.5, "specs.topSpeedKmh": None, "survivors": None,
        "_why": "1889~1925 34량(샤프 스튜어트 12·노스 브리티시 16·볼드윈 3·틴다리아 3). 현재 도색은 칼레도니안 블루. "
                "최고속도·현존 수는 출처에 없어 비움.",
        "_src": [EN + "DHR_B_Class"],
    },
    "in-wp": {
        "specs.driverDiameterMm": 1702, "specs.weightT": 176.3, "specs.weightBasis": "locoAndTender",
        "specs.boilerPressureBar": 14.5, "specs.tractiveEffortKn": 136.1, "specs.topSpeedKmh": 110,
        "withdrawnYear": None, "survivors": 9,
        "builders": ["Baldwin", "Canadian Locomotive Co.", "Montreal Locomotive Works", "Fablok", "Floridsdorf",
                     "Chittaranjan Locomotive Works"],
        "summary": "독립 인도가 자국 공장에서 대량생산한 첫 대형 여객기. 원뿔형 노즈콘에 그려진 은색 별 덕에 멀리서도 바로 알아볼 수 있다.",
        "_verified": False,
        "_why": "제원은 출처대로(최고속도는 위키 115 / IRFCA 110 — 보수적으로 110). 보존 9량 중 3량 가동. "
                "도색은 창고별로 달라 형식 대표색을 확정하지 못함 — 붉은색은 초안값 그대로 두고 미확정 표시.",
        "_src": [EN + "Indian_locomotive_class_WP", "https://irfca.org/faq/faq-loco-steam.html"],
    },
    "in-wg": {
        "specs.driverDiameterMm": 1562, "specs.weightT": 176.4, "specs.weightBasis": "locoAndTender",
        "specs.boilerPressureBar": 14.5, "specs.tractiveEffortKn": 173.0,
        "withdrawnYear": None, "survivors": 9, "status": "operable",
        "builders": ["Chittaranjan Locomotive Works (1,908량)", "North British", "Hitachi", "Henschel", "Floridsdorf",
                     "Baldwin", "Krupp 외"],
        "_why": "2,450량 중 1,908량이 치타란잔 제작. 보존 9량, WG 10253 'Ashoka' 1량 가동 상태.",
        "_src": [EN + "Indian_locomotive_class_WG"],
    },

    # ── 남아프리카 ────────────────────────────────────────────────
    "za-class25nc": {
        "builtTo": 1954, "quantityBuilt": 137, "tenderAxles": 6,
        "specs.weightT": 226.6, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 15.5,
        "specs.tractiveEffortKn": 201.8, "specs.topSpeedKmh": None, "survivors": 24,
        "_why": "신조 50량(1953~54) + 25형 응축식에서 개조된 87량 = 137량. EW1 탄수차 3축 보기 2개(6축). 보존 약 24량.",
        "_src": [EN + "South_African_Class_25NC_4-8-4"],
    },
    "za-class26": {
        "nameKo": "26형", "nameEn": "SAR Class 26", "nickname": "레드 데블 (Red Devil)",
        "specs.weightT": 235.7, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 15.5,
        "specs.tractiveEffortKn": 231.0, "specs.powerKw": 3350, "specs.topSpeedKmh": 100,
        "location": {"name": "Ceres Rail 차량기지, 케이프타운 (보관)", "lat": -33.925, "lon": 18.423},
        "highlights": ["증기기관차 열효율 개량의 마지막 대규모 실험 — 25NC 대비 석탄 28%·물 30% 절감(측정값)",
                       "최대 기록 출력 3,350kW"],
        "_why": "'레드 데블'은 케이프타운 언론이 붙인 별명. 25NC 3450호를 1981년 솔트리버 공장에서 개조.",
        "_src": [EN + "South_African_Class_26_4-8-4"],
    },
    "za-classgl": {
        "specs.driverDiameterMm": 1219, "specs.weightT": 214.4, "specs.weightBasis": "loco",
        "specs.tractiveEffortKn": 349.9, "specs.topSpeedKmh": None,
        "location": {"name": "Outeniqua 교통박물관, 조지 — 2351 'Princess Alice'", "lat": -33.96, "lon": 22.456},
        "highlights": ["당시 남반구에서 운행된 가장 강력한 증기기관차", "8량 중 2량 보존 — 조지(2351)·맨체스터(2352)"],
        "_why": "동륜 48in(1,219mm). 가라트는 탄수차가 없어 운전정비중량 214.4t 이 곧 기관차 중량. 견인력 349.9kN.",
        "_src": [EN + "South_African_Class_GL_4-8-2%2B2-8-4"],
    },
    "za-class15f": {
        "specs.weightT": None, "specs.tractiveEffortKn": 188.3, "specs.topSpeedKmh": None, "survivors": 60,
        "builders": ["North British", "Beyer, Peacock", "Henschel", "Berliner Maschinenbau"],
        "location": {"name": "Reefsteamers, 크루거스도르프 (요하네스버그 근교)", "lat": -26.10, "lon": 27.77},
        "highlights": ["남아공 철도(SAR)에서 가장 많이 만들어진 증기기관차 형식 — 255량"],
        "_why": "중량은 탄수차 종류(JT/JV/ET/EW)에 따라 180~224t 로 달라 비움. 21세기까지 약 60량 잔존.",
        "_src": [EN + "South_African_Class_15F_4-8-2"],
    },

    # ── 러시아 ────────────────────────────────────────────────────
    "ru-class-p36": {
        "classDesignation": "SŽD П36 (P36)", "nickname": "제너럴 (Генерал)",
        "withdrawnYear": 1987, "tenderAxles": 6, "specs.cylinders": 2,
        "specs.weightT": 133.2, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 178.8, "survivors": 26,
        "highlights": ["러시아(RSFSR)에서 마지막으로 제작된 간선 증기기관차 형식 — P36-0251은 콜롬나 공장의 마지막 증기기관차",
                       "붉은 띠 도색 때문에 '제너럴'로 불림"],
        "_why": "실린더는 2기통(초안 3 오류). 중량 133.2t(단독). 1963~87년 퇴역, 보존 26량.",
        "_src": [EN + "Soviet_locomotive_class_P36"],
    },
    "ru-class-l": {
        "classDesignation": "SŽD Л (L)", "quantityBuilt": 4199, "withdrawnYear": 1995,
        "builders": ["Kolomna", "Voroshilovgrad (Luhansk)", "Bryansk"],
        "specs.weightT": 103.0, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 271.5, "specs.topSpeedKmh": 85,
        "survivors": 300, "designer": "Lev Lebedyansky",
        "_why": "처음엔 П(Победа) 형식이었다가 설계자 레베댠스키의 이름을 따 Л 로 개칭. 300량 이상 잔존, 33량 가동.",
        "_src": [EN + "Soviet_locomotive_class_L", "https://loco-info.com/view.aspx?id=11831&t="],
    },
    "ru-aa20": {
        "specs.weightT": 140.0, "specs.weightBasis": "loco", "specs.boilerPressureBar": 17.0,
        "specs.tractiveEffortKn": 320.0,
        "summary": "관절 없이 동륜 7축을 한 프레임에 넣은 실험작. 시험 운행에서 곡선·분기기 통과 등 문제가 드러나 실용화되지 못했고, "
                   "한 량만 만들어진 채 1960년 해체됐다. '크면 좋다'가 틀릴 수 있음을 보여준 사례.",
        "highlights": ["세계 유일의 4-14-4 — 동륜 7축을 강체 프레임에 배치", "형식명 AA 는 교통인민위원 A. A. 안드레예프의 머리글자, 20 은 축중(t)"],
        "_why": "중량 140t(단독), 보일러 압력 17kgf/cm², 견인력 320kN 으로 출처 정정.",
        "_src": [EN + "Soviet_locomotive_class_AA20"],
    },
    "ru-class-e": {
        "classDesignation": "Russian/SŽD Э (E)", "builtTo": 1957, "quantityBuilt": 10632,
        "designer": "Wacław Łopuszyński (블라디캅카스 철도)",
        "specs.weightT": 81.2, "specs.weightBasis": "loco", "specs.boilerPressureBar": 12.0,
        "specs.tractiveEffortKn": 194.7, "specs.topSpeedKmh": 55, "survivors": 33, "status": "operable",
        "highlights": ["Э 1,528 · Эш 500 · Эг 700 · Эу 2,535 · Эм 2,325 · Эр 3,044 — 계열 합계 약 10,600량, 세계 최다 생산 증기기관차 계열"],
        "_why": "제원은 원형 Э 기준(중량 81.2t, 12kgf/cm², 55km/h; 후기형 Эм은 65km/h). 하위 형식 합계 10,632량. "
                "마지막 Эр 생산은 1957년(독일어 위키는 1955). 보존 33량, 6량 가동.",
        "_src": [DE + "Russische_Baureihe_%D0%AD", "https://loco-info.com/view.aspx?id=16947&t=Type"],
    },

    # ── 호주 · 캐나다 · 아르헨티나 ───────────────────────────────
    "au-c38-3801": {
        "shape": "semi", "designer": "Harold Young", "withdrawnYear": 1970,
        "builders": ["Clyde Engineering (3801~3805)", "Eveleigh Workshops", "Cardiff Workshops"],
        "specs.weightT": 204.0, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 16.9,
        "specs.tractiveEffortKn": 161.4, "specs.topSpeedKmh": None,
        "highlights": ["30량 중 클라이드제 3801~3805 5량만 반유선형 — 3801 이 그 첫 량",
                       "1970년 '웨스턴 인데버' — 호주 대륙(시드니~퍼스)을 횡단한 첫 증기기관차",
                       "2021년 3월 재복원 후 운행 복귀"],
        "_why": "유선형은 5량뿐이지만 이 항목은 3801호 개체라 반유선형(semi)으로 그린다. 중량 204t(운전정비, 탄수차 포함). "
                "최고속도는 출처에 없어 비움. 마지막 퇴역 1970년 12월.",
        "_src": [EN + "New_South_Wales_C38_class_locomotive", EN + "3801"],
    },
    "au-vr-r": {
        "builtTo": 1953, "specs.weightT": 190.4, "specs.weightBasis": "locoAndTender",
        "specs.tractiveEffortKn": 142.7, "specs.topSpeedKmh": None, "survivors": 7, "status": "operational",
        "_why": "1951~53 70량. 보존 7량 중 R707·R711·R761·R766 가동. 공식 최고속도 없음(129km/h 초과 기록만).",
        "_src": [EN + "Victorian_Railways_R_class"],
    },
    "au-na-puffingbilly": {
        "builders": ["Baldwin (1A·2A)", "VR Newport Workshops (15량)"],
        "specs.weightT": 34.9, "specs.weightBasis": "loco", "specs.driverDiameterMm": 914,
        "specs.boilerPressureBar": 12.4, "specs.tractiveEffortKn": 54.1, "specs.topSpeedKmh": None,
        "_why": "동륜 36in(914mm). 압력 180psi. 보존 6량 중 5량이 퍼핑 빌리 철도에서 운행.",
        "_src": [EN + "Victorian_Railways_NA_class"],
    },
    "ca-royalhudson": {
        "classDesignation": "CPR Class H1e (Royal Hudson)", "quantityBuilt": 5, "livery": "cpr-royal-hudson",
        "specs.weightT": 293.8, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 19.0,
        "specs.tractiveEffortKn": 201.3, "specs.topSpeedKmh": 144, "survivors": 4, "status": "static",
        "location": {"name": "Railway Museum of British Columbia (WCRA), 스쿼미시", "lat": 49.71, "lon": -123.15},
        "highlights": ["1939년 국왕 조지 6세 순방열차를 2850호가 견인 — 이후 유선형 허드슨 45량(H1c·H1d·H1e)에 '로열' 칭호",
                       "2860은 1940년 제작된 마지막 H1e 5량 중 하나. 1974~99년 BC Rail 관광열차로 운행"],
        "summary": "캐나다 태평양철도의 상징. 영국 밖에서 군주가 왕실 칭호를 내린 유일한 기관차 계열이다. "
                   "회색 보일러에 검은 운전실·탄수차, 터스컨 레드 판넬이 표준 도색.",
        "_why": "H1e 는 5량(2860~2864). 로열 허드슨 전체는 45량. 표준 도색은 회색 보일러 + 검정 + 터스컨 레드 판넬 — "
                "'마룬 단색' 초안을 정정. 2010년 12월 이후 운행 인증 만료로 정태 전시.",
        "_src": [EN + "Canadian_Pacific_Royal_Hudson", "https://www.wcra.org/exhibit/canadian-pacific-railway-royal-hudson-2860/",
                 "https://rapidotrains.com/cpr-royal-hudson-master-class/"],
    },
    "ca-cn-6060": {
        "builtTo": 1945, "specs.driverDiameterMm": 1854, "specs.weightT": 161.3, "specs.weightBasis": "loco",
        "specs.tractiveEffortKn": 232.7, "specs.topSpeedKmh": None, "survivors": 3, "status": "restoration",
        "location": {"name": "Alberta Prairie Railway, 스테틀러 (앨버타)", "lat": 52.32, "lon": -112.72},
        "highlights": ["원뿔형 연기실 문 커버 때문에 '불릿 노즈 베티'로 불린 U-1-f 20량 중 하나",
                       "1959년 퇴역 → 1970년대 CN 관광열차로 복귀 → 2012년까지 운행, 현재 스테틀러에서 재복원 중"],
        "_verified": False,
        "_why": "제원·보존(3량: 6060·6069·6077)·상태는 출처 확인. 도색(녹색 보일러 재킷)은 출처에서 확인하지 못해 미확정.",
        "_src": [EN + "Canadian_National_Class_U-1-f",
                 "https://railfan.com/restoration-work-continues-on-canadian-nationals-bullet-nosed-betty/"],
    },
    "ar-latrochita": {
        "nameKo": "파타고니아 협궤 2-8-2 (헨셸·볼드윈)", "nameEn": "Patagonian 750 mm 2-8-2 (Henschel / Baldwin)",
        "classDesignation": "FC Patagónico 750 mm Henschel/Baldwin 2-8-2", "nickname": "라 트로치타 (La Trochita)",
        "builders": ["Henschel & Sohn (50량)", "Baldwin Locomotive Works (25량)"],
        "specs.weightT": 47.2, "specs.weightBasis": "locoAndTender", "specs.driverDiameterMm": 800,
        "specs.boilerPressureBar": 12.0, "specs.powerKw": 306, "specs.topSpeedKmh": None, "survivors": 22,
        "highlights": ["'라 트로치타'는 기관차 형식명이 아니라 750mm 협궤 노선(비에호 엑스프레소 파타고니코)의 애칭",
                       "1922년 도입 75량 중 22량 잔존, 7량 가동 — 에스켈~나우엘판·엘 마이텐 구간 관광열차",
                       "폴 서루의 여행기 《The Old Patagonian Express》(1978)로 세계에 알려짐"],
        "_why": "공식 형식명이 없는 노선 애칭이라 이름 칸은 제작사·배치로, '라 트로치타'는 별명 칸으로. "
                "제원은 운영사 자료(볼드윈: 탄수차 포함 47.2t, 동륜 800mm, 12kg/cm², 410~431HP).",
        "_src": [EN + "La_Trochita",
                 "https://www.patagoniaexpress.com/index.php/component/content/article/150-datos-tecnicos-y-detalles-de-funcionamiento-del-viejo-expreso-patagonico-la-trochita.html?catid=51&Itemid=166"],
    },
}


# ── 재대조 (2026-09-16) ─────────────────────────────────────────────────────
# 1차 대조본은 숫자를 '출처와 같은가'만 봤고 **단위**를 보지 않았다. 영국 자료의 long ton(1.016 t)이
# 그대로 t 로 들어와 있었고(맬러드 165 → 실제 165 long tons = 167.6 t), 견인력은 lbf→kN 환산이 어긋난
# 값이 몇 개 있었다. 여기서는 위키백과 인포박스의 **미터법 값**을 그대로 옮기고, 중량은 반드시 기준
# (loco / locoAndTender)을 붙인다. 탄수차 축수는 인포박스의 탄수차 형식(2'2'T34, EW1 3-axle bogies…)이나
# 탄수차 중량÷축중(축당 20~28 t)으로 정했다 — 그림용 값이라 사진과 형식 자료로 충분하다.
# VERIFIED 뒤에 덧씌워지며, _verified 를 명시하지 않으면 1차 대조본의 판정을 그대로 둔다.
RECHECK = {
    # ── 영국: long ton → t 환산, 기관차 단독 중량으로 통일 ──
    "gb-rocket": {"specs.weightBasis": "loco",
        "_why": "4 long tons 5 cwt = 4.3 t, 기관차 단독.", "_src": [EN + "Stephenson%27s_Rocket"]},
    "gb-lner-a4-mallard": {
        "specs.weightT": 104.6, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 157.7,
        "specs.lengthMm": 21340,
        "highlights": ["증기기관차 세계 최고속도 202.8 km/h (1938-07-03, 스토크 뱅크)",
                       "기네스 공인 기록 — 지금까지 깨지지 않음"],
        "_why": "165 는 long tons(기관차+탄수차 = 167.6 t)였다. 기관차 단독 102.95 long tons = 104.6 t. "
                "견인력 35,455 lbf = 157.7 kN. 전장 70 ft = 21.34 m. '88년간' 처럼 해가 바뀌면 틀리는 표현은 뺐다.",
        "_src": [EN + "LNER_Class_A4_4468_Mallard"]},
    "gb-lner-a3-flyingscotsman": {
        "specs.weightT": 97.8, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 146.4,
        "specs.boilerPressureBar": 15.2, "specs.lengthMm": 21340,
        "_why": "기관차 단독 96.25 long tons = 97.8 t. A3 개조 후(19in 실린더) 견인력 32,910 lbf = 146.4 kN, "
                "보일러 220 psi = 15.2 bar. 초안의 131 kN·15.5 bar 는 A1 원형/근사값.",
        "_src": [EN + "LNER_Class_A3_4472_Flying_Scotsman", EN + "LNER_Class_A3"]},
    "gb-lms-duchess": {
        "specs.weightT": 110.0, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 177.9,
        "specs.driverDiameterMm": 2057, "specs.lengthMm": 22498,
        "_why": "대표 개체 6229(유선형) 기관차 단독 108.1 long tons = 110 t. 견인력 40,000 lbf = 177.9 kN. "
                "전장(유선형) 73 ft 9¾ in = 22.50 m.",
        "_src": [EN + "LMS_Princess_Coronation_Class"]},
    "gb-gwr-king": {
        "specs.weightT": 90.4, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 179.3,
        "specs.lengthMm": 20780,
        "highlights": ["1927년 미국 B&O 100주년 기념행사에 초청되어 순회",
                       "6000~6029 30량. 1936년 사고로 부서진 6007호를 새로 만든 것까지 세면 31량"],
        "_why": "기관차 단독 89 long tons = 90.4 t. 견인력 40,300 lbf(원형) = 179.3 kN. 전장 68 ft 2 in.",
        "_src": [EN + "GWR_6000_Class"]},
    "gb-lms-black5": {
        "specs.weightT": 73.3, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 113.2,
        "specs.lengthMm": 19400,
        "_why": "기관차 단독 72.1 long tons = 73.3 t(최소형). 견인력 25,455 lbf = 113.2 kN.",
        "_src": [EN + "LMS_Stanier_Class_5_4-6-0"]},
    "gb-br-britannia": {
        "specs.weightT": 95.5, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 143.0,
        "specs.lengthMm": 20960, "tenderAxles": 3,
        "_why": "기관차 단독 94 long tons = 95.5 t. 견인력 32,150 lbf = 143.0 kN. BR1 계열 탄수차는 전부 3축(6륜).",
        "_src": [EN + "BR_Standard_Class_7"]},
    "gb-a1-tornado": {
        "highlights": ["1960년 이후 영국에서 처음 새로 만들어진 본선 증기기관차",
                       "2017년 본선 시험 주행에서 100 mph 도달 — 운행 인가 속도는 90 mph"],
        "specs.weightT": 106.9, "specs.weightBasis": "loco", "specs.tractiveEffortKn": 166.4,
        "specs.lengthMm": 22240,
        "_why": "기관차 단독 105.2 long tons = 106.9 t (합계 168.8 t). 견인력 37,400 lbf = 166.4 kN.",
        "_src": [EN + "LNER_Peppercorn_Class_A1_60163_Tornado"]},

    # ── 미국 ──
    "us-up-bigboy-4014": {
        "specs.weightT": 539.6, "specs.boilerPressureBar": 20.7,
        "_why": "4014 는 1941년 1차(4884-1). 합계 1,189,500 lb = 539.6 t (548 은 2차분 4884-2 값). 300 psi = 20.7 bar.",
        "_src": [EN + "Union_Pacific_Big_Boy"]},
    "us-up-844": {
        "specs.weightT": 411.8, "specs.boilerPressureBar": 20.7, "specs.tractiveEffortKn": 283.8,
        "specs.lengthMm": 34810,
        "_why": "합계 907,890 lb = 411.8 t. 300 psi = 20.7 bar. 63,800 lbf = 283.8 kN.",
        "_src": [EN + "Union_Pacific_844"]},
    "us-nw-611": {
        "specs.weightT": 395.8, "specs.tractiveEffortKn": 355.9, "specs.lengthMm": 33270, "tenderAxles": 8,
        "_why": "합계 872,600 lb = 395.8 t. 80,000 lbf = 355.9 kN. 22D 탄수차(171.7 t)는 4축 대차 2개 = 8축(16륜).",
        "_src": [EN + "Norfolk_and_Western_611"]},
    "us-sp-4449": {
        "survivors": 1,  # GS-4 는 4449 만 남았다 (4460 은 GS-6)
        "specs.weightT": 394.9, "specs.tractiveEffortKn": 288.2, "specs.topSpeedKmh": 193,
        "specs.lengthMm": 33530, "tenderAxles": 8,
        "_why": "합계 870,600 lb = 394.9 t. 기관차 견인력 64,800 lbf = 288.2 kN(부스터 제외). 최고 120 mph = 193 km/h. "
                "GS-4 탄수차(179.4 t)는 4축 대차 2개(16륜).",
        "_src": [EN + "Southern_Pacific_4449"]},
    "us-atsf-3751": {
        "summary": "미국 서부 사막 구간을 무급수로 길게 달리기 위해 대형 탄수차를 단 장거리 여객기. 4-8-4 배치의 이름 '노던(Northern)'은 "
                   "1926년 노던 퍼시픽 철도가 먼저 도입해 붙은 것이고, 3751은 그 이듬해 볼드윈이 처음 만든 4-8-4다.",
        "specs.boilerPressureBar": 15.9, "specs.topSpeedKmh": 161, "tenderAxles": 8,
        "_why": "230 psi = 15.9 bar(원형 210). '100 mph 이상' = 161 km/h. 탄수차 179.7 t → 4축 대차 2개(16륜).",
        "_src": [EN + "Santa_Fe_3751"]},
    "us-co-allegheny": {
        "specs.weightT": 545.7, "specs.powerKw": 5590, "_verified": True,
        "_why_2": "(2차) 합계는 탄수차 종류에 따라 1,183,540~1,208,900 lb(537~548 t). 보존 1601·1604호가 속한 1600~1644 배치(25-RB 탄수차) "
                  "= 771,300 + 431,700 lb = 545.7 t 로 확정. 출력은 동력계 실측 7,500 hp(drawbar) = 5,590 kW. 1차의 '출처마다 달라 보류'는 해소.",
        "highlights": ["동력계 실측 견인마력(drawbar) 기준 세계 최고 출력의 증기기관차 (약 7,500 hp)"],
        "specs.tractiveEffortKn": 490.2, "specs.boilerPressureBar": 17.9,
        "_why": "110,211 lbf = 490.2 kN. 260 psi = 17.9 bar. 탄수차 7축(앞 3축 + 뒤 4축)은 그대로.",
        "_src": [EN + "Chesapeake_and_Ohio_class_H-8"]},
    "us-milw-classa": {
        "specs.weightT": 244.0, "specs.tractiveEffortKn": 136.5, "specs.topSpeedKmh": 181, "tenderAxles": 6,
        "_why": "합계 537,000 lb = 244 t. 30,685 lbf = 136.5 kN. 기록 112.5 mph = 181 km/h(초안 193 은 근거 없음). "
                "탄수차 13,000 gal + 4,000 gal 유류 → 3축 대차 2개.",
        "_src": [EN + "Milwaukee_Road_class_A"]},
    "us-prr-k4": {
        "summary": "미국 동부 간선 여객의 표준. 1914년 등장부터 1957년 마지막 퇴역까지 40년 넘게 펜실베이니아 철도 여객 견인의 주력이었다.",
        "specs.tractiveEffortKn": 197.8, "tenderAxles": 4,
        "_why": "44,460 lbf = 197.8 kN. 원형 70-P-70 탄수차는 2축 대차 2개(8륜).",
        "_src": [EN + "Pennsylvania_Railroad_class_K4s"]},
    "us-nyc-hudson": {"tenderAxles": 6,
        "_why": "J-3a 탄수차(143.5 t)는 12륜(3축 대차 2개)이 표준. 일부 14륜 PT형.",
        "_src": [EN + "New_York_Central_Hudson"]},
    "us-nw-y6b": {
        "specs.weightT": 436.1, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 20.7,
        "specs.tractiveEffortKn": 738.4, "specs.powerKw": 4200, "specs.lengthMm": 35010, "tenderAxles": 8,
        "_verified": True,
        "highlights": ["단순팽창 사용 시 견인력 166,000 lbf(738 kN) — 2197호 부스터 장착 시 170,000 lbf, 미국 증기 최고 수준",
                       "유일한 보존기는 Y6a 2156호(1942, 세인트루이스 국립교통박물관) — Y6b 와 사실상 같은 설계"],
        "_src": [EN + "Norfolk_and_Western_classes_Y6,_Y6a_and_Y6b"],
        "_why_2": "(2차) Y6 계열 인포박스: 합계 961,500 lb = 436.1 t(기관차 264.4 + 탄수차 171.7). 300 psi = 20.7 bar. "
                  "Y6b 단순팽창 166,000 lbf = 738.4 kN, 출력 5,600 hp = 4,200 kW. 탄수차 171.7 t → 4축 대차 2개(16륜). "
                  "1차 대조에서 비웠던 중량이 출처로 확정되어 verified 로.","tenderAxles": 6, "_why": "탄수차 3축 대차 2개(12륜)."},

    # ── 독일: 인포박스 Dienstmasse(기관차 단독)로 통일, 탄수차 형식으로 축수 ──
    "de-drg-05": {"specs.weightT": 129.9, "specs.weightBasis": "loco", "specs.lengthMm": 26265, "tenderAxles": 5,
        "_why": "05 001/002 운전정비중량 129.9 t. 탄수차 2'3 T 37 = 5축. 전장 26,265 mm.",
        "_src": [EN + "DRG_Class_05"]},
    "de-drg-01": {
        "survivors": 17,
        "specs.weightT": 111.3, "specs.weightBasis": "loco", "specs.lengthMm": 23940, "tenderAxles": 4,
        "_why": "운전정비중량 108.9~111.3 t(후기형 111.3). 탄수차 2'2' T 30/32/34 = 4축. 전장 23,940 mm. 보존 17량(영어 위키).",
        "_src": [EN + "DRG_Class_01"]},
    "de-drg-52": {"specs.weightT": 84.0, "specs.weightBasis": "loco", "specs.lengthMm": 22975, "tenderAxles": 4,
        "highlights": ["약 6,700량(전후 생산까지 세면 7,000량 이상) — 유럽에서 가장 많이 만들어진 증기기관차 계열"],
        "_why": "운전정비중량 84.0 t. 탄수차 2'2' T 30(Wannentender) = 4축. 총 생산량은 자료마다 6,700~7,800 으로 갈려 "
                "'약 6,700 / 7,000 이상'으로 적는다.",
        "_src": [EN + "DRB_Class_52", DE + "DR-Baureihe_52"]},
    "de-dr-18201": {"specs.weightT": 113.6, "specs.weightBasis": "loco", "specs.lengthMm": 25145, "tenderAxles": 4,
        "_why": "운전정비중량 113.6 t. 탄수차 2'2' T 34 = 4축.", "_src": [EN + "DR_18_201"]},
    "de-drg-0310": {
        "survivors": 3,
        "specs.weightT": 104.2, "specs.weightBasis": "loco", "tenderAxles": 4,
        "_why": "운전정비중량 104.2 t. 탄수차 2'2' T 38/34 = 4축. 보존 3량(03 1010·1090·1015).", "_src": [EN + "DRG_Class_03.10"]},
    "de-drg-44": {"specs.lengthMm": 22620, "tenderAxles": 4,
        "_why": "탄수차 2'2' T 32/34 = 4축(초안 추정 3축). 전장 22,620 mm.", "_src": [EN + "DRG_Class_44"]},
    "de-br-10": {"specs.weightT": 118.9, "specs.weightBasis": "loco", "specs.lengthMm": 26503, "tenderAxles": 4,
        "_why": "운전정비중량 118.9 t. 탄수차 2'2' T 40 = 4축.", "_src": [EN + "DB_Class_10"]},

    # ── 프랑스 ──
    "fr-241p": {
        "survivors": 4,
        "specs.weightT": 215.4, "specs.weightBasis": "locoAndTender", "specs.driverDiameterMm": 2000,
        "specs.boilerPressureBar": 19.6, "specs.tractiveEffortKn": 202.7, "specs.powerKw": 3000,
        "specs.lengthMm": 27117, "tenderAxles": 4,
        "_why": "기관차 131.4 + 탄수차 81.6 = 215.4 t. 동륜 2,000 mm(초안 2,020 오류). 20 kg/cm² = 19.6 bar. "
                "탄수차 34 P 는 2축 대차 2개. 보존 4량(P9·P16·P17·P30).",
        "_src": [EN + "SNCF_Class_241P"]},
    "fr-231e": {"specs.weightT": 182.0, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 16.7,
        "specs.tractiveEffortKn": 152.0, "specs.powerKw": 2723, "specs.topSpeedKmh": 140, "tenderAxles": 4,
        "_why": "기관차 102 + 탄수차 80 = 182 t. 압력 17 kg/cm² = 16.7 bar(초안 20 오류). 견인력 152 kN. "
                "최고 140 km/h. 탄수차는 보기 2개(4축).",
        "_src": ["https://fr.wikipedia.org/wiki/231_Nord_3.1111_%C3%A0_3.1130_et_3.1171_%C3%A0_3.1198"]},
    "fr-242a1": {
        "specs.boilerPressureBar": 20.7, "specs.tractiveEffortKn": 265.0, "specs.powerKw": 3680, "specs.lengthMm": 27330,
        "highlights": ["유럽에서 가장 강력했던 증기기관차 (약 5,500 hp)",
                       "1955년 말 운행 중지 후 해체 — 현존하지 않음"],
        "_src": ["https://fr.wikipedia.org/wiki/242_A_1"],
        "_why_2": "(2차) 프랑스어 위키 인포박스: 합계 226 t, 21.1 kg/cm² = 20.7 bar, 견인력 265 kN, 최대 지시 출력 3,680 kW, "
                  "전장 27.33 m, 보기 탄수차 34 m³. 1955-12-23 운행 중지 — 초안의 '1960년 해체'는 근거가 없어 연도를 뺐다.","tenderAxles": 4, "_why": "36 m³ 보기 탄수차(4축)."},
    "fr-140c": {
        "quantityBuilt": 340, "specs.driverDiameterMm": 1440, "specs.weightT": 77.4, "specs.weightBasis": "loco",
        "specs.boilerPressureBar": 13.7, "specs.tractiveEffortKn": 185.0, "specs.powerKw": 1030, "specs.topSpeedKmh": 80,
        "survivors": 8,
        "_src": ["https://fr.wikipedia.org/wiki/140-101_%C3%A0_370_%C3%89tat_ou_140_C_SNCF"],
        "_why_2": "(2차) 프랑스어 위키: 340량(État 70 + 영국제 200 + ALVF 70; 초안 370 은 마지막 차번). 동륜 1,440 mm. "
                  "기관차 단독 73.2~77.4 t(최대값). 14 kg/cm² = 13.7 bar. 견인력 185 kN, 출력 1,030 kW. 최고 80 km/h(Ouest). "
                  "보존 8량(140 C 22·27·38·60·231·267·289·306). 탄수차 18 C = 3축.","tenderAxles": 3, "_why": "18 m³ 3축 탄수차."},

    # ── 일본 ──
    "jp-c62": {"specs.tractiveEffortKn": 136.0, "survivors": 5,
        "summary": "전후 남아도는 D52의 보일러를 얹어 만든 대형 여객기. 협궤(1067mm)라는 제약 안에서 가능한 최대치를 "
                   "뽑아낸 형식으로, 일본 증기의 상징으로 통한다.",
        "highlights": ["일본 최대·최고속 여객용 증기기관차",
                       "1954년 협궤 세계 최고속도 129 km/h 기록",
                       "C62 2 '스왈로 엔젤(スワローエンゼル)' — 데플렉터의 제비(つばめ) 마크로 유명"],
        "_why": "보일러 출처는 D51 이 아니라 **D52**(D51 보일러를 쓴 것은 C61). 2호기 별칭은 '스완'이 아니라 "
                "'스왈로 엔젤'(제비). 견인력 13,870 kgf = 136.0 kN. 보존 5량(1·2·3·17·26).",
        "_src": [EN + "JNR_Class_C62"]},
    "jp-d51": {"survivors": 174, "specs.weightT": 123.0, "specs.tractiveEffortKn": 184.3, "specs.lengthMm": 19730,
        "_why": "합계 123.0 t. 견인력 41,400 lbf = 184.3 kN. 전장 19,730 mm. 일본 내 보존 174량.", "_src": [EN + "JNR_Class_D51"]},
    "jp-c57": {"survivors": 32, "specs.tractiveEffortKn": 125.7, "specs.boilerPressureBar": 15.7, "specs.lengthMm": 20280, "tenderAxles": 4,
        "_why": "12,820 kgf = 125.7 kN. 227.5 psi = 15.7 bar. 탄수차 12-17 형은 2축 보기 2개. 보존 32량.",
        "_src": [EN + "JNR_Class_C57"]},
    "jp-c11": {"survivors": 52, "specs.weightT": 66.05, "specs.weightBasis": "loco", "specs.lengthMm": 12650,
        "_why": "탱크식이므로 기관차 단독 = 전체. 66.05 t. 보존 52량(6량 가동).", "_src": [EN + "JNR_Class_C11"]},
    "jp-8620": {
        "specs.weightT": 48.83, "specs.weightBasis": "loco", "specs.boilerPressureBar": 12.5, "specs.tractiveEffortKn": 91.2,
        "_src": ["https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%848620%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A"],
        "_why_2": "(2차) 일본어 위키 제원표: 기관차 운전정비중량 48.83 t, 12.7 kgf/cm² = 12.5 bar, 실린더 견인력 91.2 kN. "
                  "초안의 83 t 는 기준이 없어 기관차 단독으로 바꿨다.","survivors": 21, "tenderAxles": 3, "_why": "6-13 형 3축 탄수차. 보존 일본 20 + 대만 1."},
    "jp-9600": {
        "specs.weightT": 60.35, "specs.weightBasis": "loco", "specs.boilerPressureBar": 12.7, "specs.tractiveEffortKn": 139.0,
        "specs.lengthMm": 16563, "survivors": 43,
        "_src": [EN + "JNR_Class_9600"],
        "_why_2": "(2차) 영어 위키 인포박스: 기관차 60.35 t(합계 94.85 t), 13 kg/cm² = 12.7 bar, 14,200 kgf = 139 kN, 전장 16.563 m, 보존 43량.","tenderAxles": 3, "_why": "9600형 3축 탄수차."},

    # ── 중국 ──
    "cn-jf": {"specs.cylinders": 2, "tenderAxles": 4, "_why": "2기통 외측. 탄수차 2축 보기 2개.",
        "_src": [EN + "China_Railways_JF1"]},
    "cn-sy": {"tenderAxles": 4, "_why": "탄수차 54.5 t, 2축 보기 2개."},
    "cn-km": {"specs.lengthMm": 28410, "tenderAxles": 6,
        "_why": "전장 28.41 m. 합계 259.5 t 중 탄수차 약 130 t → 3축 보기 2개(12륜).", "_src": [EN + "China_Railways_KF"]},

    # ── 인도·남아공 ──
    "in-wp": {"specs.topSpeedKmh": 115, "specs.lengthMm": 23610, "tenderAxles": 4,
        "_why": "인포박스 115 km/h. 전장 77 ft 5⅜ in. 탄수차 73.2 t → 2축 보기 2개.",
        "_src": [EN + "Indian_locomotive_class_WP"]},
    "in-wg": {"tenderAxles": 4, "_why": "탄수차 73 t → 2축 보기 2개."},
    "in-dhr-b": {"specs.weightBasis": "loco", "_why": "탱크식(0-4-0ST) — 기관차 단독이 곧 전체 중량."},
    "za-class26": {"tenderAxles": 6, "_why": "25NC 계 EW 탄수차: 3축 보기 2개."},
    "za-class15f": {"specs.weightT": 110.3, "specs.weightBasis": "loco", "specs.lengthMm": 22401, "tenderAxles": 4,
        "_why": "기관차 단독 108 LT 12 cwt = 110.3 t(초기형). JT 탄수차 = 2축 보기 2개.",
        "_src": [EN + "South_African_Class_15F_4-8-2"]},

    # ── 러시아·폴란드·오스트레일리아·캐나다·기타 ──
    "ru-class-l": {"specs.boilerPressureBar": 13.7, "tenderAxles": 4,
        "_why": "14 kgf/cm² = 13.7 bar. П27 탄수차 2축 보기 2개.", "_src": [EN + "Soviet_locomotive_class_L"]},
    "ru-aa20": {"tenderAxles": 6, "_why": "6축 탄수차."},
    "ru-class-e": {"tenderAxles": 3, "_why": "3축 탄수차."},
    "pl-pm36": {"specs.weightT": 166.9, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 17.7,
        "specs.tractiveEffortKn": 147.5, "specs.powerKw": 1325, "specs.lengthMm": 24843, "tenderAxles": 4,
        "_why": "기관차 94.0 + 탄수차 72.9 = 166.9 t. 18 kg/cm² = 17.7 bar. 견인력 147.5 kN, 출력 1,325 kW.",
        "_src": [EN + "PKP_class_Pm36"]},
    "pl-ol49": {"specs.boilerPressureBar": 16.0, "specs.tractiveEffortKn": 124.0, "tenderAxles": 4,
        "_why": "16.3 kg/cm² = 16.0 bar. 견인력 124 kN. 26D49 탄수차 4축.", "_src": [EN + "PKP_class_Ol49"]},
    "pl-ty51": {
        "specs.boilerPressureBar": 15.7, "specs.powerKw": 1589,
        "_src": ["https://www.parowozy.pl/ekspozycja/lokomotywy-parowe/ty51/"],
        "_why_2": "(2차) 하부프카 박물관 자료: 16 at = 15.7 bar, 2,160 KM = 1,589 kW, 운전정비 188.9 t(탄수차 27D51 79 t 포함). "
                  "PKP 탄수차 기호의 D 는 4축.","tenderAxles": 4, "_why": "32D48 계 탄수차 4축."},
    "au-c38-3801": {"specs.lengthMm": 23290, "tenderAxles": 4,
        "_why": "전장 76 ft 5 in. 보기 탄수차 4축.", "_src": [EN + "New_South_Wales_C38_class_locomotive"]},
    "au-vr-r": {"specs.lengthMm": 23550, "tenderAxles": 4,
        "_why": "전장 77 ft 3¼ in. 보기 탄수차 4축.", "_src": [EN + "Victorian_Railways_R_class"]},
    "ca-royalhudson": {"quantityBuilt": 45, "builtFrom": 1937, "builtTo": 1940,
        "specs.weightT": 166.0, "specs.weightBasis": "loco", "tenderAxles": 6,
        "_why": "'로열 허드슨'은 H1c·H1d·H1e 45량(1937~40) 전체의 칭호이고 보존 4량도 그 범위이므로 생산량을 45 로. "
                "2860(H1e) 기관차 단독 366,000 lb = 166 t. 탄수차 3축 대차 2개(12륜).",
        "_src": [EN + "Canadian_Pacific_Royal_Hudson"]},
    "ca-cn-6060": {
        "_verified": True,
        "_src": [EN + "Canadian_National_6060"],
        "_why_2": "(2차) 도색 확인: CN 올리브 그린은 러닝보드 스커트·운전실·탄수차에, 보일러 재킷은 검정(영어 위키 6060 문서). "
                  "팔레트는 지배색 하나라 녹색으로 두되 도색 이름에 범위를 적었다. 2020년부터 Rocky Mountain Rail Society 가 동태 복원 중.","specs.lengthMm": 27440, "tenderAxles": 6,
        "_why": "전장 90 ft. 탄수차 127.8 t → 3축 대차 2개(12륜).", "_src": [EN + "Canadian_National_Class_U-1-f"]},
    "ar-latrochita": {"tenderAxles": 4, "_why": "보기 탄수차(8륜)."},
    "in-fairyqueen": {
        "summary": "1909년 퇴역 후 반세기를 전시품으로 있다가 1997년 복원되어 다시 달렸다. 170년 넘은 기계가 여전히 증기를 뿜는다는 것 자체가 기록이다.",
        "_why": "'170년 된' 은 해가 바뀌면 틀리는 표현이라 '170년 넘은' 으로."},
    "ch-hg34": {
        "highlights": ["아프트식 치차 구간 최대 11.8% 구배 등반",
                       "1990년 베트남에서 되찾아 온 HG 3/4 1·9호(HG 4/4 2량과 함께 총 4량)를 복원"],
        "_why": "베트남에서 돌아온 HG 3/4 는 2량(1·9호). 초안의 '3량' 은 HG 4/4 를 섞어 센 것."},

    "fr-crampton": {
        "specs.weightT": 27.0, "specs.weightBasis": "loco", "tenderAxles": 2, "quantityBuilt": None,
        "specs.driverDiameterMm": 2300, "specs.boilerPressureBar": 6.9, "specs.cylinders": 2,
        "builtFrom": 1852, "builtTo": 1852, "_verified": True,
        "_why": "동부철도 80호 'Le Continent'(Cail 1852, 제작번호 189) 개체 기준: 운전정비 27 t, 2축 탄수차(Graffenstaden 1852), "
                "인가 속도 100 → 1853년 120 km/h. 동륜은 초기 크램프턴의 2,100 이 아니라 Cail 1852년형의 **2,300 mm**, "
                "보일러 7 kg/cm² = 6.9 bar, 외측 2기통(Lamming). 프랑스 각 사의 크램프턴 총수는 자료마다 달라 비웠다(초안 127 은 근거 없음). "
                "있는 값은 모두 출처가 있으므로 확정.",
        "_src": ["https://www.patrimoine-ferroviaire.fr/esst-vapeur-210-crampton-n80/", "https://fr.wikipedia.org/wiki/Crampton_(locomotive)",
                 "https://trainconsultant.com/2024/09/12/la-crampton-reine-un-peu-anglaise-dune-vitesse-tres-francaise/"]},
    "it-fs685": {
        "_verified": True,
        "_why_2": "(2차) 인포박스(685.0 기준) 값으로 제원을 채웠으므로 확정. 하위 형식(685.1·685.5 등)은 보일러·중량이 조금씩 다르다.","specs.weightT": 119.4, "specs.weightBasis": "locoAndTender", "specs.boilerPressureBar": 11.8,
        "specs.tractiveEffortKn": 111.0, "specs.powerKw": 919, "tenderAxles": 4,
        "_why": "기관차 70.8 + 탄수차 48.6 = 119.4 t. 12 kg/cm² = 11.8 bar. 견인력 111 kN, 출력 919 kW. 보기 탄수차 4축.",
        "_src": [EN + "FS_Class_685"]},
}

# ── 자료조사 원고 반영 (2026-10-23) ──────────────────────────────────────────────
# 자료조사 세션이 76량을 1차 자료·현지어 자료·당대 잡지 스캔본까지 다시 대조해 만든 원고
# (tools/manuscript/entries.json)와 정정안(corrections.json, 576건)에서 채택한 값.
#
#   - 표제란(제작·수량·보존 상태·퇴역·현존·차량 번호·차륜 배치), 궤간, 기존 제원 8칸과 중량 기준:
#     원고와 같게 맞췄다. build_seed.py 가 빌드할 때 이 값들이 원고와 같은지 검사한다(다르면 실패).
#     원고가 바뀌면 그 차이를 여기에 이유와 함께 옮긴 뒤 다시 빌드한다.
#   - 원고에 없는 앱 칸(제조사·운영·설계·형식 기호·UIC·탄수차 축수·용도·생김새·태그):
#     정정안에서 고른 것만 넣었다. '확인 필요'로만 끝난 정정안과 다른 자료로 확인되지 않은 제안은 넣지 않았다.
#   - 이름·별명·지금 있는 곳·설명 글·새 제원(기록 속도, 선륜·종륜 지름, 실린더 크기, 축거, 물탱크)은
#     원고가 정한다. build_seed.py 가 원고에서 그대로 가져온다(tools/manuscript.py).
#
# 칸마다 이유는 `_whyBy`, 출처는 `_src`(원고에서 그 값에 단 출처 + 정정안의 출처 링크).
# `_verified` 는 적지 않았다 — 1차 대조본의 판정을 그대로 둔다.
RESEARCH = {
    "gb-trevithick-pendarren": {
        "withdrawnYear": 1804,
        "specs.driverDiameterMm": None,
        "specs.cylinders": 1,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "1804년 7월 초 이후 레일 운행 기록이 없고 이후 고정식 동력기로 쓰였다.",
            "specs.driverDiameterMm": "원래 기관차의 바퀴 지름은 당대 기록이 없다. 루이스(1975)는 2 ft 10 in 남짓이라고 추정하면서 추측일 뿐이라고 밝혔다.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "specs.topSpeedKmh": "시속 8 km(5 mph 가까이)는 1804년 2월 21일 주행 때 트레비식이 적은 속도다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
        },
        "_src": ["https://shop.irsociety.co.uk/Archives/59/Locos.htm", "https://archive.org/details/liferichardtrev00trevgoog"],
    },
    "gb-locomotion-1": {
        "gaugeMm": 1422,
        "specs.weightT": 6.6,
        "specs.boilerPressureBar": 1.7,
        "specs.cylinders": 2,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "gaugeMm": "개통 당시 스톡턴·달링턴 철도의 궤간은 4 ft 8 in였다. 4 ft 8½ in라는 우드(1838)의 주장은 톰린슨이 반박했다.",
            "specs.weightT": "자료의 6 tons 10 cwt는 영국 톤(롱톤) 기준이라 6.6 t이다. 운전 정비 상태 무게다.",
            "specs.boilerPressureBar": "톰린슨(1915)이 1–4호 공통 제원으로 수직 실린더 2개, 10 × 24 in, 25 psi를 적었다.",
            "specs.cylinders": "톰린슨(1915)이 1–4호 공통 제원으로 수직 실린더 2개, 10 × 24 in, 25 psi를 적었다.",
            "specs.topSpeedKmh": "시속 24 km(15–16 mph)는 1825년 9월 27일 개통 열차가 스톡턴 앞 내리막에서 낸 속도다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
        },
        "_src": ["https://archive.org/details/northeasternrail00tomlrich", "https://en.wikipedia.org/wiki/Stockton_and_Darlington_Railway", "https://www.railwaymuseum.org.uk/sites/default/files/2023-10/Pages%20from%20LOCOMOTION%20report%20part%201.pdf"],
    },
    "gb-rocket": {
        "withdrawnYear": 1840,
        "specs.topSpeedKmh": None,
        "operators": ["Liverpool & Manchester Railway", "Brampton Railway"],
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "1840년 브램프턴 광산 철도에서 운행을 멈췄고, 1862년은 특허청 박물관에 기증한 해다.",
            "specs.topSpeedKmh": "시속 48 km(30 mph)는 레인힐 트라이얼에서 낸 속도다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "operators": "1837년부터 1840년까지 브램프턴의 광산 철도에서 일했다.",
        },
        "_src": ["https://collection.sciencemuseumgroup.org.uk/objects/co8084947/stephensons-rocket-steam-locomotive", "https://en.wikipedia.org/wiki/Stephenson%27s_Rocket"],
    },
    "gb-lner-a4-mallard": {
        "specs.lengthMm": 21650,
        "specs.boilerPressureBar": 17.2,
        "specs.powerKw": None,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "21,340 mm(70 ft)는 A3형 플라잉 스코츠맨의 값이다. 소장 기관 기록의 완충기 사이 길이는 21,650 mm(71 ft 0⅜ in)다.",
            "specs.boilerPressureBar": "250 psi를 환산하면 17.2 bar다.",
            "specs.powerKw": "맬러드의 출력 측정값이 아니다. 1940년 4901호가 낸 견인봉 출력 2,200 hp와 같은 값이다.",
            "specs.topSpeedKmh": "202.8 km/h(126 mph)는 1948년 기념판 값이다. 1938년 7월 LNER 발표와 당시 『디 엔지니어』, 기네스 세계 기록은 201.2 km/h(125 mph)다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
        },
        "_src": ["https://collection.sciencemuseumgroup.org.uk/objects/co205732/london-north-eastern-railway-steam-locomotive-mallard-4-6-2-a4-pacific-class-no-4468-1938-steam-locomotive", "https://en.wikipedia.org/wiki/LNER_Class_A4", "https://www.lner.info/locos/A/a4.php", "https://archive.org/details/sim_engineer_july-december-1938_166", "https://www.guinnessworldrecords.com/world-records/62943-fastest-steam-locomotive"],
    },
    "gb-lner-a3-flyingscotsman": {
        "specs.lengthMm": 21396,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "소장품 기록의 완충기 사이 길이는 21,396 mm다. 21,340 mm는 위키백과의 70 ft 근삿값이다.",
            "specs.topSpeedKmh": "160 km/h는 1934년 11월 30일 시험 운행의 동력계차 기록 100 mph이고, 환산하면 160.9 km/h다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
        },
        "_src": ["https://collection.sciencemuseumgroup.org.uk/objects/co8052657/london-north-eastern-railway-steam-locomotive-flying-scotsman", "https://archive.org/details/sim_railway-gazette-international_1934-12-07_61_23"],
    },
    "gb-lms-duchess": {
        "specs.weightT": 109.8,
        "specs.powerKw": 1872,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.weightT": "108.1 롱톤은 109.8 t다.",
            "specs.powerKw": "출처가 있는 값은 2,511 dbhp(1,872 kW) 측정값이다.",
            "specs.topSpeedKmh": "183 km/h는 1937년 6월 29일 6220호의 하슬러 속도계 기록 114 mph이고, 환산하면 183.5 km/h다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/LMS_Princess_Coronation_Class_6229_Duchess_of_Hamilton", "https://en.wikipedia.org/wiki/LMS_Princess_Coronation_Class", "https://archive.org/details/sim_railway-gazette-international_1937-07-02_67_1"],
    },
    "gb-gwr-king": {
        "specs.lengthMm": 20777,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "소장품 기록은 20,777 mm(68 ft 2 in)다.",
            "specs.topSpeedKmh": "열어 본 자료에 최고 속도가 없다. 1955년 6015호의 시속 108.5마일 주장 등은 확인하지 못했다.",
        },
        "_src": ["https://collection.sciencemuseumgroup.org.uk/objects/co205794/great-western-railway-steam-locomotive-king-george-v-4-6-0-king-class-no-6000-1927-steam-locomotive", "https://en.wikipedia.org/wiki/GWR_6000_Class"],
    },
    "gb-lms-black5": {
        "specs.lengthMm": 19399,
        "specs.topSpeedKmh": None,
        "builders": ["Crewe Works", "Horwich Works", "Derby Works", "Armstrong Whitworth", "Vulcan Foundry"],
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "63 ft 7¾ in는 19,399 mm다.",
            "specs.topSpeedKmh": "145 km/h는 근거를 찾지 못했다. 위키백과에 운행 중 96 mph(154.5 km/h) 기록이 있다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "builders": "호리치(120량)와 더비(54량)가 빠졌다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/LMS_Stanier_Class_5_4-6-0"],
    },
    "gb-br-britannia": {
        "specs.lengthMm": 20955,
        "specs.tractiveEffortKn": 143.1,
        "specs.topSpeedKmh": 144.8,
        "serviceType": "mixed",
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "68 ft 9 in는 20,955 mm다.",
            "specs.tractiveEffortKn": "1951년 보도는 기동 견인력 32,160 lb라고 적었다.",
            "specs.topSpeedKmh": "160 km/h의 근거가 없다. 위키백과는 최고 90 mph(144.8 km/h)라고만 쓴다.",
            "serviceType": "1951년 발표는 7급 객화 겸용으로, 본선 여객과 빠른 화물용이라 했다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/BR_Standard_Class_7", "https://archive.org/details/sim_railway-gazette-international_1951-02-02_94_5"],
    },
    "gb-a1-tornado": {
        "specs.lengthMm": 22244,
        "specs.topSpeedKmh": 144.8,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "72 ft 11¾ in는 22,244 mm다.",
            "specs.topSpeedKmh": "160 km/h는 2017년 4월 12일 시험의 100 mph(160.9 km/h)다. 시험 뒤 본선에서 허가받은 속도는 90 mph(144.8 km/h)다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
        },
        "_src": ["https://www.a1steam.com/tornado/about-tornado/tornado-facts-figures", "https://en.wikipedia.org/wiki/LNER_Peppercorn_Class_A1_60163_Tornado", "https://www.a1steam.com/tornado/about-tornado/tornados-story"],
    },
    "us-up-bigboy-4014": {
        "specs.lengthMm": 40484,
        "specs.weightT": 539.5,
        "specs.tractiveEffortKn": 602.2,
        "specs.powerKw": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "유니언 퍼시픽 자료는 132 ft 9⅞ in. 40,470 mm는 위키백과의 9¼ in 값이다.",
            "specs.weightT": "유니언 퍼시픽 형식도의 기관차·탄수차 1,189,500 lb는 539.5 t다(0.45359237 kg/lb). 1941년 두 업계지의 1,197,800 lb(543.3 t)는 주석에 둔다. 앱의 check_facts.py 고정값 539.6도 함께 고쳐야 한다.",
            "specs.tractiveEffortKn": "135,375 lbf × 4.448222 = 602.2 kN.",
            "specs.powerKw": "출력은 자료마다 5,937 hp(시험 평균), 6,290 hp(1943년 견인봉), 7,000 hp(ALCO 설계)로 다르다. 기준을 정할 1차 자료를 찾지 못했다.",
        },
        "_src": ["https://www.up.com/content/dam/upcom/migration/uprr/newsinfo/documents/up-pdf-nativedocs/pdf-up-media-4014-fact-sheet.pdf", "https://en.wikipedia.org/wiki/Union_Pacific_Big_Boy", "https://utahrails.net/up/up-steam-big-boy-differences.php", "https://archive.org/details/sim_railway-age_1941-10-04_111_14", "https://archive.org/details/sim_railway-locomotives-and-cars_1941-11_115_11", "https://forneymuseum.org/Featured_Exhibit.html"],
    },
    "us-up-844": {
        "survivors": 2,
        "specs.lengthMm": 34814,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "FEF-3형으로 남은 것은 844호와 부품용 838호 2량이다. FEF 계열 전체로 세면 814·833·838·844호 4량이다. 3은 어느 범위와도 맞지 않는다.",
            "specs.lengthMm": "114 ft 2⅝ in = 34,814 mm.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Union_Pacific_FEF_Series", "https://www.up.com/content/dam/upcom/migration/uprr/newsinfo/documents/up-pdf-nativedocs/pdf-up-media-844-fact-sheet.pdf", "https://en.wikipedia.org/wiki/Union_Pacific_844"],
    },
    "us-nw-611": {
        "specs.lengthMm": 33274,
        "specs.boilerPressureBar": 20.7,
        "specs.topSpeedKmh": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "109 ft 2 in = 33,274 mm.",
            "specs.boilerPressureBar": "611호의 보일러 압력은 300 psi(20.7 bar)다. 20.0 bar에 해당하는 값을 준 자료는 없다.",
            "specs.topSpeedKmh": "177 km/h(110 mph)는 설계 최고 속도가 아니라 다른 차량의 시험 기록이다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Norfolk_and_Western_611", "https://en.wikipedia.org/wiki/Norfolk_and_Western_Class_J_(1941)"],
    },
    "us-sp-4449": {
        "specs.lengthMm": 33528,
        "specs.boilerPressureBar": 20.7,
        "specs.powerKw": 4101,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "110 ft = 33,528 mm.",
            "specs.boilerPressureBar": "운영 단체와 백과사전 모두 300 psi(20.7 bar)로 쓴다. 20.0 bar에 맞는 자료는 없다.",
            "specs.powerKw": "운영 단체가 레일 출력 5,500 hp라고 밝힌다(주체 표시 필요).",
        },
        "_src": ["http://www.4449.com/aboutus.html", "https://en.wikipedia.org/wiki/Southern_Pacific_4449"],
    },
    "us-prr-k4": {
        "status": "restoration",
        "specs.weightT": None,
        "specs.boilerPressureBar": 14.1,
        "specs.topSpeedKmh": None,
        "specs.weightBasis": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "1361호는 2021년부터 운행 가능 상태로 복원하는 작업이 진행 중이며 2026년 7월에도 끝나지 않았다.",
            "specs.weightT": "243.0 t은 어떤 자료와도 맞지 않고, 자료마다 무게와 탄수차 기준이 다르다.",
            "specs.boilerPressureBar": "1914년 기사와 다른 자료 모두 205 psi(14.1 bar)다.",
            "specs.topSpeedKmh": "140 km/h(87 mph)는 출처가 없는 위키백과 정보상자 값이다.",
            "specs.weightBasis": "243.0 t은 어떤 자료와도 맞지 않고, 자료마다 무게와 탄수차 기준이 다르다.",
        },
        "_src": ["https://www.trains.com/trn/news-reviews/news-wire/prr-k4s-engine-no-1361-to-be-restored-in-2-6-million-campaign/", "https://www.altoonamirror.com/znewsletter-sunday/2026/07/k4-steam-engine-needs-2-5-million-to-return-to-service-2/", "https://www.hmdb.org/m.asp?m=19955", "https://en.wikipedia.org/wiki/Pennsylvania_Railroad_class_K4", "https://railarchive.net/randomsteam/prr5492.htm", "https://archive.org/details/sim_railway-locomotives-and-cars_1914-07_88_7"],
    },
    "us-nyc-hudson": {
        "specs.weightT": None,
        "specs.boilerPressureBar": 18.3,
        "specs.tractiveEffortKn": 186.2,
        "specs.topSpeedKmh": None,
        "specs.weightBasis": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.weightT": "356.3 t는 한 팬 사이트가 유선형 5445–5454호에 대해 적은 탄수차 포함 785,500 lb와 같아 형식 전체 값이 아니다. 기관차 무게도 365,500 lb(위키백과·american-rails.com)와 약 360,000 lb(뉴욕 센트럴 역사학회 자료·railarchive.net)로 엇갈려 비운다.",
            "specs.boilerPressureBar": "보일러 압력은 265 psi이고, 이는 18.3 bar다.",
            "specs.tractiveEffortKn": "기관차 본체의 견인력은 41,860 lbf(186.2 kN)이고, 부스터를 더하면 53,960 lbf(240.0 kN)이다. 196.0 kN은 어느 값과도 맞지 않는다.",
            "specs.topSpeedKmh": "177 km/h를 뒷받침하는 자료를 찾지 못했다.",
            "specs.weightBasis": "356.3 t는 한 팬 사이트가 유선형 5445–5454호에 대해 적은 탄수차 포함 785,500 lb와 같아 형식 전체 값이 아니다. 기관차 무게도 365,500 lb(위키백과·american-rails.com)와 약 360,000 lb(뉴욕 센트럴 역사학회 자료·railarchive.net)로 엇갈려 비운다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/New_York_Central_Hudson", "https://nycshs.files.wordpress.com/2014/07/pages-from-1981q3.pdf"],
    },
    "us-co-allegheny": {
        "specs.weightT": 349.9,
        "specs.powerKw": 5591,
        "specs.topSpeedKmh": 97,
        "specs.weightBasis": "loco",
        "operators": ["Chesapeake and Ohio"],
        "wheel.typeName": "Allegheny",
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.weightT": "앱 값은 C&O 자료의 기관차 771,300 lb에 탄수차 한 종류(431,700 lb)를 더한 것이다. 탄수차가 세 종류라 합계가 536.8–548.3 t로 갈리므로 기관차 무게만 적고, 1942년 발표치 328.6 t(724,500 lb)는 주석에 둔다.",
            "specs.powerKw": "원고 값으로 맞춘다(이전 5590).",
            "specs.topSpeedKmh": "1942년 기사는 설계 최고 속도를 60 mph(97 km/h)로 적었다. 70 mph는 위키백과 정보상자 값이다.",
            "specs.weightBasis": "앱 값은 C&O 자료의 기관차 771,300 lb에 탄수차 한 종류(431,700 lb)를 더한 것이다. 탄수차가 세 종류라 합계가 536.8–548.3 t로 갈리므로 기관차 무게만 적고, 1942년 발표치 328.6 t(724,500 lb)는 주석에 둔다.",
            "operators": "버지니언 철도의 2-6-6-6 8량은 별도 형식(AG)이다. 수량 60량도 C&O H-8만 센 것이다.",
            "wheel.typeName": "C&O는 이 배치를 앨러게이니형이라 불렀다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Chesapeake_and_Ohio_class_H-8", "https://www.thehenryford.org/collections/explore/popular-research-topics/the-allegheny-locomotive", "https://archive.org/details/sim_railway-locomotives-and-cars_1942-05_116_5", "https://trn.trains.com/railroads/railroad-history/2018/02/big-boy-versus-allegheny", "https://en.wikipedia.org/wiki/2-6-6-6"],
    },
    "us-milw-classa": {
        "specs.weightT": 127.0,
        "specs.boilerPressureBar": 20.7,
        "specs.topSpeedKmh": None,
        "specs.weightBasis": "loco",
        "tenderAxles": 5,
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.weightT": "1935년 기사는 기관차 280,000 lb만 분명히 밝힌다. 탄수차 포함 537,000 lb는 위키백과 값이다.",
            "specs.boilerPressureBar": "300 psi는 20.7 bar다.",
            "specs.topSpeedKmh": "1935년 『레일웨이 에이지』와 『레일웨이 메커니컬 엔지니어』는 모두 111.5 mph(179.4 km/h)로 보도했다. 112.5 mph(181.1 km/h)는 뒤의 문헌 값이라 주석에 둔다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "specs.weightBasis": "1935년 기사는 기관차 280,000 lb만 분명히 밝힌다. 탄수차 포함 537,000 lb는 위키백과 값이다.",
            "tenderAxles": "1935년 기사에 따르면 탄수차는 앞쪽 3축(6륜) 대차와 뒤쪽 2축(4륜) 대차로 받쳤다.",
        },
        "_src": ["https://archive.org/details/sim_railway-locomotives-and-cars_1935-06_109_6", "https://en.wikipedia.org/wiki/Milwaukee_Road_class_A", "https://archive.org/details/sim_railway-age_1935-05-18_98_20", "http://www.germansteam.co.uk/FastestLoco/fastestloco.html"],
    },
    "us-atsf-3751": {
        "survivors": 2,
        "specs.tractiveEffortKn": 293.5,
        "specs.topSpeedKmh": 144.8,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "같은 3751형 가운데 3759호가 애리조나주 킹먼에 전시되어 있다.",
            "specs.tractiveEffortKn": "65,981 lbf는 293.5 kN이다.",
            "specs.topSpeedKmh": "소유 단체는 1941년 개조 뒤 허용 최고 속도를 시속 90마일(144.8 km)로 적는다. 앱의 161 km/h는 위키백과의 '시속 100마일 이상'을 바꾼 값으로, 측정값이 아니다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/4-8-4", "https://en.wikipedia.org/wiki/Santa_Fe_3751", "https://www.sbrhs.org/equipment/santa-fe-3751/history.html"],
    },
    "us-nw-y6b": {
        "status": "scrapped",
        "survivors": 0,
        "specs.lengthMm": None,
        "specs.weightT": None,
        "specs.driverDiameterMm": 1473,
        "specs.powerKw": None,
        "specs.topSpeedKmh": None,
        "specs.weightBasis": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 8개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "보존된 Y6b가 없다. 정태 보존은 같은 계열 Y6a 2156호의 상태다.",
            "survivors": "Y6b는 1958–1961년과 1976년에 모두 해체됐다. 남은 2156호는 1942년에 만든 Y6a다.",
            "specs.lengthMm": "모두 위키백과의 Y6/Y6a 정보상자 값이다. Y6b는 연소실이 길어지고 급수가열기를 다는 등 달라졌으므로 그대로 옮길 수 없다.",
            "specs.weightT": "모두 위키백과의 Y6/Y6a 정보상자 값이다. Y6b는 연소실이 길어지고 급수가열기를 다는 등 달라졌으므로 그대로 옮길 수 없다.",
            "specs.driverDiameterMm": "Y6b의 동륜 지름은 58 in(1,473 mm)이다. 1,448 mm(57 in)는 Y6/Y6a 출고 당시 값이다.",
            "specs.powerKw": "모두 위키백과의 Y6/Y6a 정보상자 값이다. Y6b는 연소실이 길어지고 급수가열기를 다는 등 달라졌으므로 그대로 옮길 수 없다.",
            "specs.topSpeedKmh": "모두 위키백과의 Y6/Y6a 정보상자 값이다. Y6b는 연소실이 길어지고 급수가열기를 다는 등 달라졌으므로 그대로 옮길 수 없다.",
            "specs.weightBasis": "모두 위키백과의 Y6/Y6a 정보상자 값이다. Y6b는 연소실이 길어지고 급수가열기를 다는 등 달라졌으므로 그대로 옮길 수 없다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Norfolk_and_Western_classes_Y6,_Y6a_and_Y6b", "https://tnmot.org/collection", "https://www.trains.com/trn/news-reviews/news-wire/19-nw-y6a-to-return-to-st-louis-after-five-years-in-virginia/"],
    },
    "de-adler": {
        "withdrawnYear": 1857,
        "specs.weightT": None,
        "specs.driverDiameterMm": 1372,
        "specs.boilerPressureBar": 3.3,
        "specs.cylinders": 2,
        "specs.topSpeedKmh": None,
        "specs.weightBasis": None,
        "serviceType": "passenger",
        "_why": "자료조사 원고(2026-10-23) 반영: 8개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "1857년 운행에서 물러나 바퀴 없이 팔렸다. DB 박물관은 매각 연도를 1858년으로 쓴다.",
            "specs.weightT": "DB 박물관의 14 t와 위키백과의 14.3 t는 1935년 복제품의 무게로 보인다. 1835년 자료는 계약상 6 t, 회사 보고서 120 바이에른 첸트너(약 6.7 t)로 크게 달라 원형의 무게로 쓸 수 없다.",
            "specs.driverDiameterMm": "원고가 출처와 함께 채운 값.",
            "specs.boilerPressureBar": "원고가 출처와 함께 채운 값.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "specs.topSpeedKmh": "시속 65 km는 객차 없이 달린 시범 운행의 속도이고, 영업 운행은 시속 28–35 km 안팎이었다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "specs.weightBasis": "DB 박물관의 14 t와 위키백과의 14.3 t는 1935년 복제품의 무게로 보인다. 1835년 자료는 계약상 6 t, 회사 보고서 120 바이에른 첸트너(약 6.7 t)로 크게 달라 원형의 무게로 쓸 수 없다.",
            "serviceType": "6 km 구간에서 말이 끄는 열차와 번갈아 다닌 여객 열차였다.",
        },
        "_src": ["https://de.wikipedia.org/wiki/Bayerische_Ludwigsbahn", "https://www.nuernberginfos.de/ludwigseisenbahn/adler-lokomotive.php", "https://dbmuseum.de/nuernberg/fahrzeuge/adler", "https://en.wikipedia.org/wiki/Adler_(locomotive)", "https://de.wikipedia.org/wiki/Adler_(Lokomotive)", "https://dingler.bbaw.de/articles/mi063004_3.html"],
    },
    "de-drg-05": {
        "specs.boilerPressureBar": 19.6,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 1736,
        "specs.topSpeedKmh": 175,
        "operators": ["Deutsche Reichsbahn", "Deutsche Bundesbahn"],
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.boilerPressureBar": "원래 단위는 20 at(kgf/cm²)로 19.6 bar다. 1950년 16 bar로 낮췄다.",
            "specs.tractiveEffortKn": "137.0 kN을 뒷받침하는 자료를 찾지 못했다. 자료마다 148.2 kN, 118.5 kN 등으로 다르다.",
            "specs.powerKw": "2,360은 마력(PS) 값이다. DB 박물관은 2,360 HP/1,735 kW로 적는다.",
            "specs.topSpeedKmh": "설계 최고 속도는 175 km/h다. 200.4 km/h는 1936년 5월 11일 05 002의 시험 기록이다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "operators": "전후 3량 모두 독일연방철도 함 기관구에서 1958년까지 운행했다.",
        },
        "_src": ["https://archive.org/details/sim_railway-gazette-international_1935-03-01_62_9", "https://en.wikipedia.org/wiki/DRG_Class_05", "https://de.wikipedia.org/wiki/DR-Baureihe_05", "https://loco-info.com/view.aspx?id=11593", "https://dbmuseum.de/nuernberg/fahrzeuge/schnellzuglokomotive-05001", "https://www.berliner-zeitung.de/article/borsig-lokomitoven-aus-berlin-die-schnellste-lok-der-welt-kam-aus-berlin-59991"],
    },
    "de-drg-01": {
        "quantityBuilt": 231,
        "survivors": 19,
        "specs.weightT": 111.1,
        "specs.boilerPressureBar": 15.7,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 1648,
        "builders": ["AEG", "Borsig", "Henschel", "Hohenzollern", "Krupp", "BMAG"],
        "_why": "자료조사 원고(2026-10-23) 반영: 7개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "quantityBuilt": "새로 만든 것은 231량이다. 241량은 02형에서 개조한 10량을 더한 형식 전체 수이므로 본문에 따로 적는다.",
            "survivors": "보존 차량 데이터베이스는 일반형 14량과 01.5형 5량을 든다. 두 위키백과의 17량은 서로 다른 목록이다.",
            "specs.weightT": "01 102 이후 차량의 운전 정비 중량은 111.1 t(탄수차 제외)이다.",
            "specs.boilerPressureBar": "노이엔마르크트 박물관의 01 111 자료표는 16 kp/cm²로 적는다. 16 kp/cm²는 15.7 bar다. 같은 박물관 자료를 쓴 44형·52형·10형과 단위 기준을 맞춘다.",
            "specs.tractiveEffortKn": "162.0 kN의 근거를 찾지 못했다.",
            "specs.powerKw": "2,240 PSi를 환산하면 1,648 kW이며, 도시마력임을 밝힌다.",
            "builders": "제작사는 6곳이다.",
        },
        "_src": ["https://de.wikipedia.org/wiki/DR-Baureihe_01", "https://en.wikipedia.org/wiki/DRG_Class_01", "https://www.eisenbahnfreunde-berlin.net/de/dampflok-br-01/", "https://de.wikipedia.org/wiki/DR-Baureihe_01.5", "http://www.eisenbahn-museumsfahrzeuge.de/index.php/deutschland/staatsbahnfahrzeuge/dampflokomotiven/baureihe-01", "https://www.eisenbahn-museumsfahrzeuge.de/index.php/deutschland/staatsbahnfahrzeuge/dampflokomotiven/baureihe-015", "https://www.dampflokmuseum.de/das-museum/exponate/01-111"],
    },
    "de-drg-52": {
        "specs.boilerPressureBar": 15.7,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 1192,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.boilerPressureBar": "원래 값은 16 kp/cm²로 15.7 bar다.",
            "specs.tractiveEffortKn": "176.0 kN의 근거를 찾지 못했다.",
            "specs.powerKw": "도시마력 1,620 PS를 환산한 값이다.",
        },
        "_src": ["https://www.dampflokmuseum.de/das-museum/exponate/52-5804", "https://en.wikipedia.org/wiki/DRB_Class_52"],
    },
    "de-dr-18201": {
        "builtFrom": 1960,
        "status": "restoration",
        "specs.powerKw": 1581,
        "specs.topSpeedKmh": 175,
        "operators": ["Deutsche Reichsbahn", "Deutsche Bahn AG", "Dampf-Plus", "WFL"],
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "builtFrom": "1960년에 개조를 시작해 1961년에 완성했다.",
            "status": "2018년 뒤로 운행하지 않았고, 2026년 1월 기준 노센 기관구에서 운행 재개를 위한 정비 중이다.",
            "specs.powerKw": "도시마력 2,150 PS를 환산했다.",
            "specs.topSpeedKmh": "허용 최고 속도는 175 km/h이고, 182.4 km/h는 1972년 10월 시험 기록이다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "operators": "1994년 이후 소유자가 여러 번 바뀌었다.",
        },
        "_src": ["https://de.wikipedia.org/wiki/DR_18_201", "https://www.eisenbahn-museumsfahrzeuge.de/index.php/deutschland/staatsbahnfahrzeuge/dampflokomotiven/baureihe-182", "https://en.wikipedia.org/wiki/DR_18_201"],
    },
    "de-drg-0310": {
        "specs.lengthMm": 23905,
        "specs.weightT": 103.2,
        "specs.boilerPressureBar": 20.0,
        "builders": ["Borsig", "Krupp", "Krauss-Maffei"],
        "wheel.uic": "2'C1'h3",
        "operators": ["Deutsche Reichsbahn", "Deutsche Bundesbahn", "Deutsche Reichsbahn (GDR)", "PKP"],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "보존 차량 데이터베이스의 형식 자료.",
            "specs.weightT": "원고 값으로 맞춘다(이전 104.2).",
            "specs.boilerPressureBar": "형식 자료는 20 bar이다. 16 bar의 근거는 찾지 못했다.",
            "builders": "크라우스마파이도 20량을 만들었다(영어판 기준).",
            "wheel.uic": "축 배치 표기 보충.",
            "operators": "전후 서독, 동독, 폴란드 국철(Pm3)이 운용했다.",
        },
        "_src": ["https://www.eisenbahn-museumsfahrzeuge.de/index.php/deutschland/staatsbahnfahrzeuge/dampflokomotiven/baureihe-0310", "https://de.wikipedia.org/wiki/DR-Baureihe_03.10", "https://en.wikipedia.org/wiki/DRB_Class_03.10"],
    },
    "de-drg-44": {
        "survivors": 54,
        "specs.weightT": 110.0,
        "specs.boilerPressureBar": 15.7,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 1405,
        "builders": ["Krupp", "Henschel", "Borsig", "Krauss-Maffei", "Schichau", "Floridsdorf", "Fives-Lille", "SACM", "외"],
        "wheel.uic": "1'Eh3",
        "operators": ["Deutsche Reichsbahn", "DB", "DR", "SNCF"],
        "_why": "자료조사 원고(2026-10-23) 반영: 8개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "보존 차량 데이터베이스는 54량이 남아 있다고 집계한다(2016–2021년 목록). 20량의 근거는 찾지 못했다.",
            "specs.weightT": "박물관 자료는 기관차 운전 정비 중량을 110 Mp로 적는다. 110.2 t의 근거는 찾지 못했다.",
            "specs.boilerPressureBar": "원자료 단위는 16 kp/cm²이고 15.7 bar로 환산된다.",
            "specs.tractiveEffortKn": "열어 본 자료 가운데 견인력을 적은 것이 없다.",
            "specs.powerKw": "석탄 연소식 도시마력 1,910 PS를 환산한 값.",
            "builders": "제작사는 15곳 이상이다. 크루프가 가장 많은 309량을 만들었고, 프랑스와 오스트리아, 폴란드 공장도 만들었다.",
            "wheel.uic": "박물관 자료의 축 배치 표기.",
            "operators": "226량이 전후 프랑스 국유철도에 직접 인도되었다.",
        },
        "_src": ["http://www.eisenbahn-museumsfahrzeuge.de/index.php/deutschland/staatsbahnfahrzeuge/dampflokomotiven/baureihe-44", "https://www.dampflokmuseum.de/das-museum/exponate/44-276", "https://stoomtrein.org/collectie/baureihe-44/", "https://de.wikipedia.org/wiki/DR-Baureihe_44", "https://en.wikipedia.org/wiki/DRG_Class_44", "https://www.eisenbahn-museumsfahrzeuge.de/index.php/deutschland/staatsbahnfahrzeuge/dampflokomotiven/baureihe-44/44-1593"],
    },
    "de-br-10": {
        "specs.boilerPressureBar": 17.7,
        "specs.powerKw": 1839,
        "wheel.uic": "2'C1'h3",
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.boilerPressureBar": "원자료 단위는 18 kp/cm²이고 17.7 bar로 환산된다.",
            "specs.powerKw": "박물관과 위키백과 모두 도시마력 2,500 PS(1,839 kW)를 적는다. 1,650 kW(약 2,240 PS)의 근거는 찾지 못했다.",
            "wheel.uic": "박물관 자료의 축 배치 표기.",
        },
        "_src": ["https://www.dampflokmuseum.de/das-museum/exponate/10-001", "https://en.wikipedia.org/wiki/DB_Class_10", "https://de.wikipedia.org/wiki/DB-Baureihe_10"],
    },
    "fr-242a1": {
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 2942,
        "builders": ["Fives-Lille (1932, 241-101)", "Marine-Homécourt, Saint-Chamond (1943–1946 개조)"],
        "wheel.uic": "2'D2'h3v",
        "tags": ["복식팽창", "현존없음"],
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.tractiveEffortKn": "265 kN(프랑스어 위키), 199–239 kN(loco-info), 206–292 kN(영어 위키)로 엇갈린다.",
            "specs.powerKw": "지시 출력은 자료마다 3,680–4,100 kW로 엇갈린다. 자료가 일치하는 연결기 출력 4,000 ch(2,942 kW)를 기준을 밝혀 표시한다.",
            "builders": "개조는 생샤몽의 마린-오메쿠르사 공장에서 했다 [1, 3]. 바티뇰은 241-101이 잠시 있던 파리의 기관구 이름이다 [1].",
            "wheel.uic": "복식 기관차이므로 v를 붙인다 [2].",
            "tags": "'명차'는 평가어, '최고출력'은 출처가 엇갈려 뺀다. 복식 기관차라 '복식팽창'을 단다. '명차'는 금지 평가어이고 '최고출력'은 출처가 엇갈린다.",
        },
        "_src": ["https://fr.wikipedia.org/wiki/242_A_1", "https://en.wikipedia.org/wiki/4-8-4", "https://www.loco-info.com/view.aspx?id=11051", "https://de.wikipedia.org/wiki/SNCF_242_A_1", "https://trainconsultant.com/2021/11/15/lage-chapelon-excellence-de-la-vapeur-francaise/"],
    },
    "fr-241p": {
        "withdrawnYear": 1973,
        "specs.weightT": 131.4,
        "specs.driverDiameterMm": 2020,
        "specs.tractiveEffortKn": 200.4,
        "specs.powerKw": 2942,
        "specs.weightBasis": "loco",
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "정기 운행은 1969년 9월에 끝났지만 마지막 2량(P 9, P 16)은 1973년에 차적에서 빠졌다 [1, 2].",
            "specs.weightT": "기관차 중량 131.4 t는 자료가 일치하지만 합계는 214.1 t, 215.4 t, 216.2 t로 엇갈린다 [1, 2, 6]. 이전 세션이 탄수차 중량으로 쓴 81.6 t는 점착 중량이다 [1].",
            "specs.driverDiameterMm": "프랑스어 위키 2,020 mm, 소유 협회 자료 2,022 mm(새 바퀴 테)다 [1, 6]. 2,000 mm는 영어 위키백과에만 있다 [2].",
            "specs.tractiveEffortKn": "소유 협회 자료의 20,434 kg(100 % 차단비)을 환산했다 [6].",
            "specs.powerKw": "실린더 출력 약 4,000 ch를 환산한 값이다 [1, 6]. 연결기 출력은 시속 100 km에서 2,900 ch다 [6].",
            "specs.weightBasis": "기관차 중량 131.4 t는 자료가 일치하지만 합계는 214.1 t, 215.4 t, 216.2 t로 엇갈린다 [1, 2, 6]. 이전 세션이 탄수차 중량으로 쓴 81.6 t는 점착 중량이다 [1].",
        },
        "_src": ["https://fr.wikipedia.org/wiki/241_P", "https://en.wikipedia.org/wiki/SNCF_Class_241P", "https://www.train-vapeur.fr/accueil/carte-d-identité-241p17/"],
    },
    "fr-231e": {
        "withdrawnYear": 1967,
        "specs.lengthMm": 23440,
        "operators": ["Compagnie du chemin de fer du Nord", "SNCF"],
        "builders": ["PO 투르 공장 개조 20량 (1934)", "Marine-Homécourt 10량, Fives-Lille 10량, ANF Blanc-Misseron 8량 (1936–1938)"],
        "classDesignation": "Nord 3.1111–3.1130, 3.1171–3.1198 / SNCF 2-231 E 1–48",
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "칼레 기관구의 마지막 4량이 1967년까지 아미앵–칼레 선을 달렸다 [1].",
            "specs.lengthMm": "기관차와 탄수차 합계 23.44 m [1].",
            "operators": "이 형식을 운용한 회사는 노르 철도다. PO는 투르 공장에서 20량을 개조해 넘겼을 뿐이다 [1].",
            "builders": "신조 28량은 노르가 아니라 민간 제작사 3곳이 만들었다 [1].",
            "classDesignation": "노르 시절에는 '231 E'라는 기호를 쓰지 않았다 [1].",
        },
        "_src": ["https://fr.wikipedia.org/wiki/231_Nord_3.1111_%C3%A0_3.1130_et_3.1171_%C3%A0_3.1198"],
    },
    "fr-crampton": {
        "withdrawnYear": 1914,
        "_why": "자료조사 원고(2026-10-23) 반영: 1개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "80호의 마지막 영업 운행은 1914년 7월 31일이다.",
        },
        "_src": ["https://www.patrimoine-ferroviaire.fr/esst-vapeur-210-crampton-n80/"],
    },
    "fr-140c": {
        "withdrawnYear": 1975,
        "specs.lengthMm": 11750,
        "builders": ["SACM", "Schneider", "Fives-Lille", "North British Locomotive", "Nasmyth, Wilson", "Vulcan Foundry"],
        "operators": ["Chemins de fer de l'État", "Chemins de fer de l'Est", "PLM", "SNCF"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "마지막 SNCF 차량은 1973년에 차적에서 빠졌고, CFTA에 임대된 140 C 287이 1975년 9월 24일까지 영업 열차를 끌었다 [1, 2].",
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "builders": "북미 제작사가 만든 차량은 없다. 프랑스 3사가 70량, 영국의 노스브리티시·네이즈미스 윌슨·벌컨 파운드리가 270량을 만들었다 [1, 2].",
            "operators": "주문하고 처음 운용한 것은 에타 철도이고, ALVF 차량 35량은 PLM으로 갔다 [1].",
        },
        "_src": ["https://fr.wikipedia.org/wiki/140-101_%C3%A0_370_%C3%89tat_ou_140_C_SNCF", "https://en.wikipedia.org/wiki/%C3%89tat_140-101_to_140-370"],
    },
    "jp-class150": {
        "specs.lengthMm": 7417,
        "specs.weightT": 23.45,
        "specs.driverDiameterMm": None,
        "specs.boilerPressureBar": 9.7,
        "specs.cylinders": 2,
        "specs.topSpeedKmh": None,
        "operators": ["관설 철도 (1872–1911)", "시마바라 철도 (1911–1930)"],
        "_why": "자료조사 원고(2026-10-23) 반영: 7개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.weightT": "16.5 t의 근거를 찾지 못했다. 영어 위키백과 정보상자는 23.45 t를 준다(정비 상태 구분 없음). 1차 형식도로 다시 확인해야 한다.",
            "specs.driverDiameterMm": "1,321 mm(52 in)와 1,295 mm(51 in, 1892년 도면)로 자료가 엇갈린다.",
            "specs.boilerPressureBar": "원고가 출처와 함께 채운 값.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "specs.topSpeedKmh": "시속 40 km를 뒷받침하는 자료가 없다.",
            "operators": "1911년부터 1930년까지 시마바라 철도에서 일했고 1930년 보존을 위해 돌아왔다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/JGR_Class_150", "https://ja.wikipedia.org/wiki/国鉄150形蒸気機関車", "https://www.shimatetsu.co.jp/first-locomotive/"],
    },
    "jp-c62": {
        "status": "operable",
        "specs.weightT": 145.17,
        "specs.boilerPressureBar": 15.7,
        "specs.powerKw": 1192,
        "specs.topSpeedKmh": None,
        "builders": ["히타치 제작소", "가와사키 차량", "기샤세이조"],
        "operators": ["운수성", "일본국유철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 7개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "C62 2는 운전 가능한 상태로 보존되어 2026년 10월에도 교토 철도박물관 구내 'SL 스팀호'를 끌었다. 본선 운행은 하지 않는다.",
            "specs.weightT": "원고 값으로 맞춘다(이전 145.2).",
            "specs.boilerPressureBar": "보일러 압력은 16.0 kg/cm²이며 15.7 bar로 환산된다.",
            "specs.powerKw": "원고가 출처와 함께 채운 값.",
            "specs.topSpeedKmh": "129 km/h는 1954년 12월 15일 C62 17의 시험 기록이다. 설계·허용 최고 속도는 확인하지 못했다. 기록 속도는 새 칸(recordSpeedKmh)에 옮기고, 최고속도 칸에는 설계·허용 최고 속도만 둔다.",
            "builders": "미쓰비시는 C62형을 만들지 않았다. 히타치 21량(1–21호), 가와사키 차량 15량(22–36호), 기샤세이조 13량(37–49호)이다.",
            "operators": "1948년 첫 차량은 국철 발족(1949년 6월) 전 운수성 시절에 나왔다.",
        },
        "_src": ["https://www.kyotorailwaymuseum.jp/news/sysimg/01914/link_9N9lr.pdf", "https://www.kyotorailwaymuseum.jp/enjoying/watching/vehicle/roundhouse-platform/", "https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%84C62%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A", "https://kurogane-rail.jp/kurogane-doc/sl/elococ62.html", "https://www.westjr.co.jp/railway-cultural-property/pages/00017.html", "https://museum.jr-central.co.jp/rolling-stock/"],
    },
    "jp-d51": {
        "withdrawnYear": 1975,
        "specs.weightT": 125.77,
        "specs.boilerPressureBar": 14.7,
        "specs.powerKw": 1030,
        "builders": ["철도성 공장", "가와사키 차량", "기샤세이조", "히타치 제작소", "닛폰샤료", "미쓰비시 중공업"],
        "operators": ["철도성", "일본국유철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "국철 본선 운행은 1975년 12월 24일 D51 241의 화물 열차로 끝났다.",
            "specs.weightT": "일본 자료는 운전 정비 상태 기관차 78.37 t, 탄수차 47.40 t, 합계 125.77 t로 적는다. 123.0 t는 영어 위키백과의 값이며 근거가 밝혀져 있지 않다.",
            "specs.boilerPressureBar": "15.0은 kgf/cm² 값이다. bar로는 14.7이며, 처음 만들 때는 14.0 kgf/cm²(13.7 bar)였다.",
            "specs.powerKw": "원고가 출처와 함께 채운 값.",
            "builders": "민간 5개사와 철도성 공장 8곳이 만들었다. 기샤세이조, 닛폰샤료, 미쓰비시가 빠져 있다.",
            "operators": "1936–1945년 제조 당시 소유자는 철도성이다.",
        },
        "_src": ["https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%84D51%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A", "https://en.wikipedia.org/wiki/JNR_Class_D51", "https://kurogane-rail.jp/kurogane-doc/sl/elocod51.html"],
    },
    "jp-c57": {
        "specs.powerKw": 949,
        "builders": ["미쓰비시 중공업", "가와사키 차량", "히타치 제작소", "기샤세이조"],
        "operators": ["철도성", "일본국유철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.powerKw": "최대 출력 1,290 PS(948.8 kW)가 확인된다.",
            "builders": "기샤세이조가 5량을 만들었다. 미쓰비시 106, 가와사키 60, 히타치 30량이다.",
            "operators": "1937–1947년 제조 당시 소유자는 철도성(이후 운수성)이다.",
        },
        "_src": ["https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%84C57%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A"],
    },
    "jp-c11": {
        "specs.boilerPressureBar": 14.7,
        "specs.powerKw": 576,
        "builders": ["닛폰샤료", "가와사키 차량", "기샤세이조", "히타치 제작소"],
        "operators": ["철도성", "일본국유철도"],
        "serviceType": "mixed",
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.boilerPressureBar": "15.0은 kgf/cm² 값이다. bar로는 14.7이다.",
            "specs.powerKw": "원고가 출처와 함께 채운 값.",
            "builders": "기샤세이조가 60량을 만들었다. 닛폰샤료 180, 가와사키 88, 히타치 53량이다.",
            "operators": "1932–1947년 제조 당시 소유자는 철도성(이후 운수성)이다.",
            "serviceType": "JR 서일본은 C11형을 객화 겸용 탱크 기관차로 적는다. '탱크'는 형태이지 용도가 아니다.",
        },
        "_src": ["https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%84C11%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A", "https://kurogane-rail.jp/kurogane-doc/sl/elococ11.html", "https://www.westjr.co.jp/company/info/issue/data/pdf/data2026_23.pdf"],
    },
    "jp-8620": {
        "status": "static",
        "specs.lengthMm": 16765,
        "specs.boilerPressureBar": 12.7,
        "specs.powerKw": 463,
        "builders": ["기샤세이조", "히타치 제작소", "가와사키 조선소", "닛폰샤료", "미쓰비시 조선소"],
        "operators": ["철도원", "철도성", "일본국유철도", "JR 규슈"],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "58654는 증기로는 달리지 않고 2025년 11월부터 압축 공기로 움직이는 전시만 한다. 형식 전체로는 교토의 8630이 박물관 구내에서 '스팀호'를 끄는 일이 있으므로 operable로 둘 수도 있다.",
            "specs.lengthMm": "교토 철도박물관(8630)과 위키백과 제원표가 16,765 mm로 같다.",
            "specs.boilerPressureBar": "보일러 압력은 13.0 kg/cm²이며 12.7 bar로 환산된다.",
            "specs.powerKw": "원고가 출처와 함께 채운 값.",
            "builders": "닛폰샤료와 미쓰비시 조선소도 만들었다. 기샤세이조가 384량으로 절반이 넘는다.",
            "operators": "1914–1929년 도입 당시 소유자는 철도원과 철도성이다.",
        },
        "_src": ["https://www.city.hitoyoshi.lg.jp/kanko/kankojyoho/2450957", "https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%848620%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A", "https://www.kyotorailwaymuseum.jp/enjoying/watching/vehicle/roundhouse-platform/", "https://kurogane-rail.jp/kurogane-doc/sl/eloco8620.html"],
    },
    "jp-9600": {
        "roadNumber": "9633",
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 640,
        "specs.topSpeedKmh": 70,
        "builders": ["가와사키 조선소", "기샤세이조", "철도원 고쿠라 공장"],
        "operators": ["철도원", "철도성", "일본국유철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "roadNumber": "위치를 교토 철도박물관으로 하면 대표 차량은 9633이다.",
            "specs.tractiveEffortKn": "일본어 위키백과 13,702 kg(134.4 kN)은 그쪽의 보일러 압력 12.7 kg/cm²와 실린더 지름 510 mm로 계산한 값이라 여기 적은 13.0 kg/cm²·508 mm와 맞지 않고, 영어 위키백과의 14,200 kgf(139 kN)는 어느 조합과도 맞지 않아 비운다.",
            "specs.powerKw": "출력 870 PS(639.9 kW)가 확인된다.",
            "specs.topSpeedKmh": "일본어 위키백과는 70 km/h, 영어 위키백과는 65 km/h로 적는다. 백과사전끼리만 엇갈리는 경우 그 나라 말 판을 따른다는 기준에 따라 70 km/h를 쓴다.",
            "builders": "철도원 고쿠라 공장도 15량을 만들었다. 가와사키 686, 기샤세이조 69량이다.",
            "operators": "1913–1926년 제조 당시 소유자는 철도원·철도성이다.",
        },
        "_src": ["https://www.kyotorailwaymuseum.jp/enjoying/watching/vehicle/roundhouse-platform/", "https://www.westjr.co.jp/company/info/issue/data/pdf/data2026_23.pdf", "https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%849600%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A", "https://en.wikipedia.org/wiki/JNR_Class_9600", "https://kurogane-rail.jp/kurogane-doc/sl/eloco9600.html"],
    },
    "jp-c58": {
        "withdrawnYear": None,
        "specs.lengthMm": 18275,
        "specs.boilerPressureBar": 15.7,
        "specs.tractiveEffortKn": 123.3,
        "specs.powerKw": 807,
        "operators": ["철도성", "일본국유철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "1975년의 근거를 찾지 못했다. 일본어·영어 위키백과 정보상자는 1973년으로 적지만, 일본어 위키백과 본문에는 1974년에 폐차된 차량도 나와 형식 전체가 물러난 해를 정할 수 없다.",
            "specs.lengthMm": "교토 철도박물관과 위키백과 제원표로 확인된다.",
            "specs.boilerPressureBar": "16.0은 kgf/cm² 값이다. bar로는 15.7이다.",
            "specs.tractiveEffortKn": "교토 철도박물관과 위키백과 제원표로 확인된다.",
            "specs.powerKw": "교토 철도박물관과 위키백과 제원표로 확인된다.",
            "operators": "1938–1947년 제조 당시 소유자는 철도성(이후 운수성)이다.",
        },
        "_src": ["https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%89%84C58%E5%BD%A2%E8%92%B8%E6%B0%97%E6%A9%9F%E9%96%A2%E8%BB%8A", "https://en.wikipedia.org/wiki/JNR_Class_C58", "https://www.kyotorailwaymuseum.jp/enjoying/watching/vehicle/roundhouse-platform/", "https://kurogane-rail.jp/kurogane-doc/sl/elococ58.html"],
    },
    "kr-moga": {
        "specs.lengthMm": 9169,
        "specs.weightT": 35.7,
        "specs.driverDiameterMm": 1067,
        "specs.boilerPressureBar": 9.7,
        "specs.cylinders": 2,
        "specs.weightBasis": "loco",
        "builders": ["Brooks Locomotive Works (조립은 경인철도 인천 공장)"],
        "operators": ["경인철도합자회사", "경부철도", "통감부 철도관리국", "조선총독부 철도국", "대한민국 교통부"],
        "shape": "classic",
        "_why": "자료조사 원고(2026-10-23) 반영: 9개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.weightT": "원고가 출처와 함께 채운 값.",
            "specs.driverDiameterMm": "원고가 출처와 함께 채운 값.",
            "specs.boilerPressureBar": "원고가 출처와 함께 채운 값.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "specs.weightBasis": "중량 기준을 원고 값에 맞춘다.",
            "builders": "브룩스는 부품이 아니라 완성 기관차 4량을 만들었고, 분해 상태로 운송해 인천에서 다시 조립했다. '인천공작창'은 후대 명칭이다.",
            "operators": "1903년 경부철도 합병, 1906년 국유화, 1947년 남북 분할 기록이 있다.",
            "shape": "1898년 3월호 Railway Master Mechanic 의 출고 사진은 영국식 완충기·스크루 연결기·석유등이고 카우캐처가 없다(삽화 작업 kr_moga.py 와 같은 근거). 정정안도 classic 을 권했다. 원래 버퍼와 체인 연결기를 달았고 1904–1905년경 자동연결기로 바꿨다. 출고 사진 확인 후 확정.",
        },
        "_src": ["https://archive.org/details/railwaymastermec21newy", "https://archive.org/details/sim_railway-locomotives-and-cars_1898-04_72_4", "https://en.wikipedia.org/wiki/Sentetsu_Mogai-class_locomotive", "https://archive.org/details/sim_railway-age_1898-03-04_30_9", "https://ko.wikipedia.org/wiki/모가형_증기_기관차", "https://librewiki.net/wiki/모가형_증기기관차"],
    },
    "kr-mika3-129": {
        "survivors": 6,
        "specs.lengthMm": 22094,
        "specs.driverDiameterMm": None,
        "specs.cylinders": 2,
        "builders": ["기샤세이조 (제작)", "조선총독부 철도국 경성공장 (조립)"],
        "classDesignation": "미카3형 (Mika3)",
        "tags": [],
        "_why": "자료조사 원고(2026-10-23) 반영: 7개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "영어 위키백과는 남한 4량, 북한 1량, 중국 1량(JF9)을 든다.",
            "specs.lengthMm": "국가유산청 기록에 129호 길이가 있다.",
            "specs.driverDiameterMm": "1,400 mm를 적은 자료를 찾지 못했다.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "builders": "1940년 미카사 110–129호는 기샤세이조 제작으로 나오고, 국가유산청의 옛 등록 설명은 일본에서 만들어 경성 공장에서 조립했다고 적었다. 앱 값은 제작사 이름과 제작·조립 구분이 빠졌다.",
            "classDesignation": "원고의 이름 결정(영문-이름-표)에 맞춰 로마자에서 하이픈을 뺐다(Mika3).",
            "tags": "2025년 6월 국가등록문화유산 등록이 말소되어 '문화재' 태그를 뺀다. '명차'는 평가어라 뺀다. 2025년 등록 말소. '명차'는 문체 규칙의 금지어다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Sentetsu_Mikasa-class_locomotive", "http://www.khs.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd=79&ccbaAsno=0004150000000&ccbaCtcd=25", "https://namu.wiki/w/미카형 증기기관차", "https://www.khan.co.kr/article/202506120957001/"],
    },
    "kr-mika3-161": {
        "survivors": 6,
        "specs.driverDiameterMm": None,
        "specs.cylinders": 2,
        "builders": ["닛폰샤료"],
        "classDesignation": "미카3형 (Mika3)",
        "tags": [],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "영어 위키백과는 남한 4, 북한 1, 중국 1량을 든다.",
            "specs.driverDiameterMm": "1,400 mm를 적은 자료를 찾지 못했다.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "builders": "미카사 148–172호는 닛폰샤료 제조번호 817–841로 나오고, 나무위키도 129호 외 보존 3량을 일본차량제조 제작으로 적는다.",
            "classDesignation": "원고의 이름 결정(영문-이름-표)에 맞춰 로마자에서 하이픈을 뺐다(Mika3).",
            "tags": "국가유산청 공공데이터의 증기기관차 등록문화유산 7건에 161호는 없다. 국가유산청 공공데이터의 증기기관차 등록문화유산 7건에 161호는 없다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Sentetsu_Mikasa-class_locomotive", "https://namu.wiki/w/미카형 증기기관차", "https://ko.wikipedia.org/wiki/미카형_증기_기관차", "http://www.khs.go.kr/cha/SearchKindOpenapiList.do?ccbaMnm1=%EC%A6%9D%EA%B8%B0%EA%B8%B0%EA%B4%80%EC%B0%A8&pageUnit=50"],
    },
    "kr-pashi5": {
        "quantityBuilt": 42,
        "withdrawnYear": None,
        "specs.lengthMm": 23756,
        "specs.boilerPressureBar": 14.7,
        "specs.cylinders": 2,
        "specs.tractiveEffortKn": 162.0,
        "tags": ["문화재"],
        "classDesignation": "파시5형 (Pasi5)",
        "_why": "자료조사 원고(2026-10-23) 반영: 8개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "quantityBuilt": "경성공장 2량과 가와사키 40량.",
            "withdrawnYear": "1967년은 23호가 운행을 마친 해다. 영어 위키백과의 한국 국철 표에는 1968년에도 운행한 파시5-37이 있어, 형식 전체가 물러난 해는 정할 수 없다.",
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.boilerPressureBar": "원고가 출처와 함께 채운 값.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "specs.tractiveEffortKn": "원고가 출처와 함께 채운 값.",
            "tags": "23호는 국가등록문화유산이다. '최고속도'는 근거 없는 비교, '명차'는 평가어라 뺀다. '최고속도'는 근거 없는 비교이고 '명차'는 금지어다.",
            "classDesignation": "원고의 이름 결정(영문-이름-표)에 맞춤: 국어의 로마자 표기법으로 파시 → Pasi, 하이픈 없음.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Sentetsu_Pashiko-class_locomotive", "http://www.khs.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd=79&ccbaAsno=0004170000000&ccbaCtcd=31"],
    },
    "kr-teou": {
        "specs.lengthMm": 18808,
        "specs.boilerPressureBar": 13.7,
        "specs.tractiveEffortKn": 119.0,
        "builders": ["Baldwin Locomotive Works"],
        "classDesignation": "터우1형 (Teou1)",
        "serviceType": "passenger",
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.boilerPressureBar": "원고가 출처와 함께 채운 값.",
            "specs.tractiveEffortKn": "원고가 출처와 함께 채운 값.",
            "builders": "터우1형은 볼드윈 제작이다. ALCO는 1917–1918년 터우5형을 만들었다.",
            "classDesignation": "원고가 항목을 터우1형으로 좁혔다(값이 모두 터우1형의 것). 로마자는 Teou1.",
            "serviceType": "자료는 여객용이라고 적는다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Sentetsu_Tehoi-class_locomotive", "https://en.wikipedia.org/wiki/Sentetsu_Tehoko-class_locomotive", "https://ko.wikipedia.org/wiki/터우형_증기_기관차"],
    },
    "kr-hyeogi": {
        "classDesignation": "혀기8형 (Hyeogi8)",
        "_why": "자료조사 원고(2026-10-23) 반영: 1개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "classDesignation": "원고의 이름 결정(영문-이름-표)에 맞춰 로마자에서 하이픈을 뺐다(Hyeogi8).",
        },
        "_src": [],
    },
    "cn-qj": {
        "specs.powerKw": 2192,
        "tenderAxles": 4,
        "builders": ["다롄 기관차공장", "다퉁 기관차공장", "탕산·선양·무단장·창춘 공장 (1958–1961 시제·소량)"],
        "operators": ["중국철도", "지퉁 철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.powerKw": "최대 동륜 주위 출력 2,980마력(PS) = 2,192 kW.",
            "tenderAxles": "원고의 전장 26,000 mm 는 4축 탄수차 기준이다(6축이면 29,181 mm). 도식의 탄수차를 그 값에 맞춘다. QJ는 4축과 6축 탄수차를 모두 썼다. 앱의 전장 26,000 mm는 4축 탄수차 기준이라 탄수차 6축 표기와 맞지 않는다.",
            "builders": "1961년까지 시제차 42량을 여섯 공장이 나누어 만들었다.",
            "operators": "마지막 간선 운행은 국철이 아닌 지퉁 철도 회사였다.",
        },
        "_src": ["https://zh.wikipedia.org/wiki/前进型蒸汽机车", "https://www.loco-info.com/view.aspx?id=13548", "https://en.wikipedia.org/wiki/China_Railways_QJ", "https://m.thepaper.cn/baijiahao_24248489", "https://en.wikipedia.org/wiki/Jining%E2%80%93Tongliao_railway", "https://trains.com/?p=185593"],
    },
    "cn-js": {
        "withdrawnYear": 2024,
        "specs.lengthMm": 23370,
        "specs.tractiveEffortKn": 249.8,
        "operators": ["중국철도", "산다오링 탄광철도", "분 앤드 시닉 밸리 철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "정기 운행한 마지막 JS인 8089호가 2024년 1월 15일 퇴역했다.",
            "specs.lengthMm": "탄수차 포함 전장 23,370 mm.",
            "specs.tractiveEffortKn": "원 수치 25,476 kgf를 정확히 환산한 값이다.",
            "operators": "8419호가 1990년부터 미국에서 운행했다.",
        },
        "_src": ["https://trains.com/?p=185593", "https://en.wikipedia.org/wiki/China_Railways_JS", "https://en.wikipedia.org/wiki/Boone_and_Scenic_Valley_Railroad_8419"],
    },
    "cn-sy": {
        "status": "static",
        "specs.lengthMm": 21643,
        "specs.powerKw": 1103,
        "builders": ["탕산 기관차공장", "창춘·칭다오 쓰팡·타이위안·퉁링 공장 등"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "트레인스는 중국의 일상 증기 운행이 2024년 1월 끝났다고 보도했다. 미국 보존기의 2024–2026년 운행 여부는 확인하지 못했다.",
            "specs.lengthMm": "탄수차 포함 전장과 최대 출력 1,500마력(PS)을 추가한다.",
            "specs.powerKw": "탄수차 포함 전장과 최대 출력 1,500마력(PS)을 추가한다.",
            "builders": "인민철도보가 밝힌 제작 공장 목록에 맞춘다.",
        },
        "_src": ["https://trains.com/?p=185593", "https://en.wikipedia.org/wiki/China_Railways_SY", "https://zh.wikipedia.org/wiki/%E4%B8%8A%E6%B8%B8%E5%9E%8B%E8%92%B8%E6%B1%BD%E6%9C%BA%E8%BD%A6", "http://www.peoplerail.com/rail/show-456-361528-1.html"],
    },
    "cn-jf": {
        "roadNumber": "JF1 304",
        "specs.lengthMm": 21906,
        "specs.boilerPressureBar": 13.7,
        "builders": ["ALCO", "사허커우 공장 (만철)", "가와사키·기샤세이조·닛폰샤료·히타치", "쓰팡·다롄·치치하얼·타이위안 (전후)"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "roadNumber": "이름은 번호 칸에 넣지 않는다. 304호의 이름판은 'MAO ZEDONG', 1191호는 'ZHU DE'로 기록되어 있다(2003년). 이 이름은 본문과 위치 설명에 둔다.",
            "specs.lengthMm": "신국대미카/JF1 전장 21,906 mm.",
            "specs.boilerPressureBar": "출처 값은 14.0 kgf/cm²이고 이는 13.7 bar다. 단위를 바꾸지 않고 옮긴 값이다.",
            "builders": "전쟁 전 최다 제작처인 사허커우 공장 등이 빠져 있다. 전후 수량은 455량과 475량으로 엇갈려 괄호에서 뺀다.",
        },
        "_src": ["https://www.internationalsteam.co.uk/china/trains/china210.htm", "https://en.wikipedia.org/wiki/China_Railways_JF1", "https://archive.org/details/report-on-progress-in-manchuria-1907-1928"],
    },
    "cn-km": {
        "specs.weightT": 195.8,
        "specs.driverDiameterMm": 1753,
        "specs.tractiveEffortKn": None,
        "operators": ["중국 철도부 (광저우–한커우 철도, 난징–상하이 철도)", "중국철도 (1949년 이후)"],
        "classDesignation": "China Railways KF (원 번호 601–624)",
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.weightT": "1935년 레일웨이 가제트는 기관차와 탄수차 합계 192 tons 14 cwt 2 qr(195.8 t)로 적었고, 박물관 기록도 194,870 kg이다. 259.5 t는 근거를 찾지 못했다.",
            "specs.driverDiameterMm": "1935년 『레일웨이 가제트』는 5 ft 9 in으로 적었다. 1,753 mm다.",
            "specs.tractiveEffortKn": "앱의 160.5 kN(36,100 lb)은 뒤의 8량(실린더 지름 540 mm) 값이다. KF7이 속한 1차분의 값은 1935년 기사 OCR이 32,920 lb로 읽히지만 같은 기사의 다른 치수로 계산하면 34,919 lb라 지면을 확인할 때까지 비운다.",
            "operators": "1935년 배치 계획과 박물관 기록에 맞춘다.",
            "classDesignation": "KF7이 원래 607호였다는 박물관 기록은 601–624 번호와 맞는다.",
        },
        "_src": ["https://archive.org/details/sim_railway-gazette-international_1935-11-01_63_18", "https://collection.sciencemuseumgroup.org.uk/objects/co205814/chinese-government-railways-steam-locomotive-4-8-4-kf-class-no-7", "https://en.wikipedia.org/wiki/China_Railways_KF"],
    },
    "in-fairyqueen": {
        "withdrawnYear": 1909,
        "specs.cylinders": 2,
        "specs.powerKw": 97,
        "classDesignation": "EIR No. 22",
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "1909년까지 비하르의 선로 건설에 쓰였다.",
            "specs.cylinders": "원고가 출처와 함께 채운 값.",
            "specs.powerKw": "원고가 출처와 함께 채운 값.",
            "classDesignation": "동인도 철도가 도착 때 붙인 번호는 22호다. 21호는 'Express'라는 다른 기관차다.",
        },
        "_src": ["https://pib.gov.in/newsite/PrintRelease.aspx?relid=158386", "https://www.angelfire.com/ak5/nrmindia/fairyqn.htm", "https://en.wikipedia.org/wiki/Fairy_Queen_(locomotive)", "https://loco-info.com/view.aspx?id=14229"],
    },
    "in-dhr-b": {
        "builtTo": 1927,
        "specs.weightT": 14.2,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "builtTo": "802호(DHR 49)가 1927년 노스브리티시 제작(제작번호 23678)이라는 자료가 여럿이다. 1차 자료는 확인하지 못해 최종 판단은 보류가 필요하다. 1928년설(Vardhan 목록)도 있다.",
            "specs.weightT": "출처 값은 14 롱톤이다. 1.016047을 곱하면 14.2 t이다.",
        },
        "_src": ["https://irfca.org/docs/locolists/steam-india.html", "https://irfca.org/articles/vikas/dhr-locos.html", "https://en.wikipedia.org/wiki/DHR_B_Class_778", "https://kurogane-rail.jp/kurogane-doc/darjeeling/edarjeeling-sl.html", "https://en.wikipedia.org/wiki/DHR_B_Class", "https://archive.org/details/darjeelinghimal00unkngoog"],
    },
    "in-wp": {
        "specs.lengthMm": 23606,
        "specs.topSpeedKmh": 110,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "77 ft 5⅜ in의 정확한 환산값.",
            "specs.topSpeedKmh": "IRFCA와 위키백과 본문은 모두 최대 110 km/h로 적는다. 115 km/h는 위키백과 정보상자에만 있다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Indian_locomotive_class_WP", "https://irfca.org/faq/faq-loco-steam.html"],
    },
    "in-wg": {
        "specs.topSpeedKmh": None,
        "builders": ["Chittaranjan 1,908량", "North British 115량 (+Vulcan 10량)", "Anglo-Franco-Belge 18량 (+Henschel 64량)", "Hitachi 100량", "Henschel 60량", "Floridsdorf 60량", "Baldwin 50량", "Krupp 40량", "Ansaldo 25량"],
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.topSpeedKmh": "위키백과 80 km/h와 IRFCA 약 88 km/h가 충돌하고 1차 자료가 없다.",
            "builders": "제작사 목록을 수량과 함께 완전하게 적는다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Indian_locomotive_class_WG", "https://irfca.org/faq/faq-loco-steam.html", "http://www.irfca.org/steam/postwar.html"],
    },
    "za-class25nc": {
        "specs.lengthMm": 27903,
        "specs.tractiveEffortKn": 194.8,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.tractiveEffortKn": "1953년 Railway Gazette는 75% 기준 43,800 lb로 적는다. 1차 자료 우선 원칙을 따랐으나 같은 잡지의 치수로 계산하면 45,360 lbf가 나와 재확인이 필요하다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/South_African_Class_25NC_4-8-4", "https://archive.org/details/sim_railway-gazette-international_1953-05-15_98_20"],
    },
    "za-class26": {
        "specs.weightT": None,
        "specs.powerKw": None,
        "specs.weightBasis": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.weightT": "위키백과 정보상자의 합계 232 LT(235.7 t)는 같은 상자의 기관차 117 LT 9 cwt와 탄수차 105 LT 11 cwt를 더한 223 LT(226.6 t)와 맞지 않아 비운다.",
            "specs.powerKw": "3,350 kW(4,492 지시마력)는 위키백과가 메일링 리스트 글을 인용한 것이 유일한 근거라 비운다.",
            "specs.weightBasis": "위키백과 정보상자의 합계 232 LT(235.7 t)는 같은 상자의 기관차 117 LT 9 cwt와 탄수차 105 LT 11 cwt를 더한 223 LT(226.6 t)와 맞지 않아 비운다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/South_African_Class_26_4-8-4"],
    },
    "za-classgl": {
        "specs.lengthMm": 27632,
        "specs.weightT": None,
        "specs.weightBasis": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.weightT": "214.4 t(인포박스)과 217.5 t(본문)이 충돌하고 박물관 기록은 단위 없는 '214 tons'다.",
            "specs.weightBasis": "214.4 t(인포박스)과 217.5 t(본문)이 충돌하고 박물관 기록은 단위 없는 '214 tons'다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/South_African_Class_GL_4-8-2%2B2-8-4", "https://collection.sciencemuseumgroup.org.uk/objects/co8405990/beyer-garratt-south-african-railways-locomotive"],
    },
    "za-class15f": {
        "status": "static",
        "specs.topSpeedKmh": 96.6,
        "builders": ["North British 204량", "Beyer, Peacock 30량", "Henschel 14량", "Berliner Maschinenbau 7량"],
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "대표 차량 3007호는 정태 전시다. 남아프리카의 3117호가 2024년 6월 운행 준비 중인 사진 기록이 있으나 운행을 확인한 자료는 찾지 못했다.",
            "specs.topSpeedKmh": "1946년 Railway Gazette가 60 mph를 여객열차 견인 가능 속도로 적었다.",
            "builders": "제작사별 수량을 덧붙인다.",
        },
        "_src": ["https://www.glasgowlife.org.uk/museums/digital-welcome-pack/riverside-museum/south-african-loco-3007", "https://mobile.railpictures.net/photo/859912", "https://archive.org/details/sim_railway-gazette-international_1946-09-20_85_12", "https://en.wikipedia.org/wiki/South_African_Class_15F_4-8-2"],
    },
    "ru-class-p36": {
        "survivors": None,
        "specs.lengthMm": 29800,
        "specs.weightT": None,
        "specs.boilerPressureBar": 14.7,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 2263,
        "specs.weightBasis": None,
        "designer": "L. S. Lebedyanskiy (Kolomna)",
        "_why": "자료조사 원고(2026-10-23) 반영: 8개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "26량은 영어 위키 정보상자뿐이고 같은 문서 목록은 22량이다. P36-0044가 2025년 박물관으로 옮겨진 기록도 있어 수가 확정되지 않는다.",
            "specs.lengthMm": "빈 칸을 출처 있는 값으로 채운다.",
            "specs.weightT": "두 값의 출처를 찾지 못했다. 확인될 때까지 '—'로 둔다.",
            "specs.boilerPressureBar": "원 수치는 15 kgf/cm²이며 bar로 바꾸면 14.7이다.",
            "specs.tractiveEffortKn": "두 값의 출처를 찾지 못했다. 확인될 때까지 '—'로 둔다.",
            "specs.powerKw": "빈 칸을 출처 있는 값으로 채운다.",
            "specs.weightBasis": "두 값의 출처를 찾지 못했다. 확인될 때까지 '—'로 둔다.",
            "designer": "1974년 기사와 영어 위키 모두 레베댠스키가 설계팀을 이끌었다고 적는다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Soviet_locomotive_class_P36", "https://railgallery.ru/railcar/87088?lang=en", "https://de.wikipedia.org/wiki/S%C5%BDD-Baureihe_%D0%9F36", "http://zdrus.narod.ru/lib/journal/tm_1974/tm_1974_12.html", "https://rzd-museum.ru/expositions/exhibits"],
    },
    "ru-class-l": {
        "survivors": None,
        "specs.lengthMm": 23750,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 1618,
        "designer": "Lev S. Lebedyanskiy",
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "'300량 이상'은 각주 없는 영어 위키 문장뿐이고, loco-info는 '여러 량, 운행 가능 5량'으로 적는다. 33량 가동설도 각주 없음.",
            "specs.lengthMm": "빈 칸을 출처 있는 값으로 채운다.",
            "specs.tractiveEffortKn": "271.5 kN(영어 위키)과 268.1 kN(loco-info)이 엇갈린다.",
            "specs.powerKw": "빈 칸을 출처 있는 값으로 채운다.",
            "designer": "러시아어 로마자 표기 규칙(BGN/PCGN)에 맞춤.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Soviet_locomotive_class_L", "https://loco-info.com/view.aspx?id=11831&t="],
    },
    "ru-aa20": {
        "gaugeMm": 1524,
        "specs.lengthMm": 33730,
        "specs.weightT": 206.0,
        "specs.boilerPressureBar": None,
        "specs.tractiveEffortKn": 313.8,
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "gaugeMm": "1960년에 해체돼 1,524 mm 시기에만 존재했다.",
            "specs.lengthMm": "두 자료가 탄수차 포함 33,730 mm로 일치한다.",
            "specs.weightT": "loco-info와 skyrocket이 기관차 운전 정비 중량 206 t로 일치한다(탄수차 포함 전체 330 t). 140 t는 영어 위키에서 1931년 예비 설계 수치와 함께 나온다.",
            "specs.boilerPressureBar": "17 kgf/cm²는 16.7 bar이고, skyrocket은 16.9 kp/cm²(16.6 bar)로 적는다.",
            "specs.tractiveEffortKn": "원 수치 32.0 tf를 정확히 바꾸면 313.8 kN이다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Soviet_locomotive_class_AA20", "http://loco.skyrocket.de/data/szd_aa20.htm", "https://loco-info.com/view.aspx?id=13530"],
    },
    "ru-class-e": {
        "survivors": None,
        "specs.lengthMm": 11460,
        "specs.boilerPressureBar": 11.8,
        "tenderAxles": 4,
        "builders": ["러시아·소련, 독일, 스웨덴, 동유럽의 여러 공장"],
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "33은 기념물로 남은 Eu·Em·Er 수의 합일 뿐이다. 스웨덴제 기념물 3량, 운행 가능 6량, 박물관 차량이 따로 있어 전체 수가 확정되지 않는다.",
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.boilerPressureBar": "loco-info는 단위 없이 12로 적는다. 러시아 기관차의 보일러 압력은 kgf/cm²로 적으므로 12 kgf/cm², 곧 11.8 bar로 본다.",
            "tenderAxles": "1915–1918년 무렵부터 푸틸로프 공장제 4축 탄수차로 통일됐다.",
            "builders": "Eg형은 독일, Esh형은 스웨덴 공장이 만들었다.",
        },
        "_src": ["https://de.wikipedia.org/wiki/Russische_Baureihe_%D0%AD", "https://loco-info.com/view.aspx?id=16947&t=Type", "http://www.historiskt.nu/rullande/lokbyggandet/lok_nydqvist&holm_15.html"],
    },
    "pl-ol49": {
        "quantityBuilt": 115,
        "status": "restoration",
        "survivors": None,
        "specs.lengthMm": 20675,
        "specs.weightT": None,
        "specs.boilerPressureBar": None,
        "specs.tractiveEffortKn": None,
        "specs.powerKw": 949,
        "specs.weightBasis": None,
        "serviceType": "passenger",
        "_why": "자료조사 원고(2026-10-23) 반영: 10개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "quantityBuilt": "기관고 도록(2023)과 독일어 위키가 115량으로 적는다. 116은 북한 수출을 4량으로 세는 자료의 값이다.",
            "status": "2026년 3월 볼슈틴의 정기 증기 열차가 다시 다니기 시작했을 때 운행한 것은 Pt47-65였고, Ol49-69는 2월에 새 보일러가 완성되어 복귀를 기다리고 있었다. 지금 운행 중인 Ol49는 확인되지 않는다.",
            "survivors": "독일어 위키는 폴란드에 36량이 남았다고 하고, 볼슈틴 도록에만 8량이 있다. 15의 근거를 찾지 못했다.",
            "specs.lengthMm": "빈 칸을 출처 있는 값으로 채운다.",
            "specs.weightT": "영어 위키와 parowozy.pl의 값이 서로 다르다(견인력은 124 kN 대 94.1 kN).",
            "specs.boilerPressureBar": "영어 위키와 parowozy.pl의 값이 서로 다르다(견인력은 124 kN 대 94.1 kN).",
            "specs.tractiveEffortKn": "영어 위키와 parowozy.pl의 값이 서로 다르다(견인력은 124 kN 대 94.1 kN).",
            "specs.powerKw": "빈 칸을 출처 있는 값으로 채운다.",
            "specs.weightBasis": "영어 위키와 parowozy.pl의 값이 서로 다르다(견인력은 124 kN 대 94.1 kN).",
            "serviceType": "여객용 형식(O)이며 화물·입환은 볼슈틴에서의 부수적 사용이다.",
        },
        "_src": ["http://parowozowniawolsztyn.pl/wp-content/uploads/2024/10/ebook.pdf", "https://de.wikipedia.org/wiki/PKP-Baureihe_Ol49", "https://en.wikipedia.org/wiki/PKP_class_Ol49", "https://www.parowozy.pl/ekspozycja/lokomotywy-parowe/ol49/", "https://railwayworld.net/2026/03/21/daily-steam-services-resume-at-wolsztyn/", "http://parowozowniawolsztyn.pl/?page_id=2141"],
    },
    "pl-pm36": {
        "status": "static",
        "designer": "Kazimierz Zembrzuski",
        "operators": ["PKP", "DRB (전쟁 중)"],
        "tags": [],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "status": "2026년 3월 볼슈틴에서 운행하던 대형 기관차는 Pt47-65뿐이었고, 영어 위키는 Pm36-2가 볼슈틴에서 수리를 기다린다고 적는다.",
            "designer": "영어 위키가 설계자와 외형 디자인을 젬브주스키로 적는다.",
            "operators": "Pm36-1은 전쟁 중 독일 국영철도 18 601로 쓰였다.",
            "tags": "이 항목의 Pm36-2에는 유선형 덮개가 없다. 이 항목의 Pm36-2에는 유선형 덮개가 없다.",
        },
        "_src": ["https://railwayworld.net/2026/03/21/daily-steam-services-resume-at-wolsztyn/", "https://en.wikipedia.org/wiki/PKP_class_Pm36", "https://de.wikipedia.org/wiki/PKP-Baureihe_Pm36", "http://parowozowniawolsztyn.pl/wp-content/uploads/2024/10/ebook.pdf"],
    },
    "pl-ty51": {
        "quantityBuilt": 242,
        "survivors": None,
        "specs.cylinders": None,
        "specs.tractiveEffortKn": None,
        "builders": ["H. Cegielski, Poznań (당시 Zakłady Przemysłu Metalowego im. J. Stalina)"],
        "operators": ["PKP", "산업 철도"],
        "_why": "자료조사 원고(2026-10-23) 반영: 6개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "quantityBuilt": "볼슈틴 도록(2023)과 독일어 위키가 242량으로 적는다. 232는 PKP 번호 범위일 가능성이 있으나 확인하지 못했다.",
            "survivors": "확인된 보존 차량은 5량이며 10량의 근거를 찾지 못했다.",
            "specs.cylinders": "두 값의 출처를 찾지 못했다.",
            "specs.tractiveEffortKn": "두 값의 출처를 찾지 못했다.",
            "builders": "볼슈틴 도록, parowozy.pl, 독일어 위키가 모두 포즈난의 체기엘스키 공장을 제작사로 적는다.",
            "operators": "PKP와 산업용으로 함께 만들었다.",
        },
        "_src": ["http://parowozowniawolsztyn.pl/wp-content/uploads/2024/10/ebook.pdf", "https://de.wikipedia.org/wiki/PKP-Baureihe_Ty51", "https://www.parowozy.pl/ekspozycja/lokomotywy-parowe/ty51/"],
    },
    "au-c38-3801": {
        "specs.lengthMm": 23292,
        "specs.weightT": 199.1,
        "specs.tractiveEffortKn": 161.0,
        "builders": ["Clyde Engineering (3801–3805)"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고 값으로 맞춘다(이전 23290).",
            "specs.weightT": "1943년 Railway Gazette는 기관차와 탄수차를 합쳐 196 롱톤(199.1 t)이라 적는다. 204 t는 후대 2차 자료의 값으로, 탄수차 물 용량(7,000 → 8,100 gal) 차이일 가능성이 있으나 확인하지 못했다.",
            "specs.tractiveEffortKn": "1943년 기사 값 36,200 lb(보일러 압력 85% 기준)를 따랐다. 후대 자료는 36,273 lbf(161.35 kN).",
            "builders": "범위에는 물결표 대신 en dash를 쓴다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/New_South_Wales_C38_class_locomotive", "https://archive.org/details/sim_railway-gazette-international_1943-06-25_78_26", "https://www.railtram.com.au/3801", "https://apps.environment.nsw.gov.au/dpcheritageapp/ViewHeritageItemDetails.aspx?ID=4807230"],
    },
    "au-vr-r": {
        "builtTo": 1952,
        "specs.lengthMm": 23552,
        "specs.powerKw": 1372,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "builtTo": "노스브리티시 기관차 회사의 제작 연도는 1951–1952년이다. 1953년은 마지막 R 769가 운행에 들어간 해다.",
            "specs.lengthMm": "77 ft 3¼ in의 정확한 환산값.",
            "specs.powerKw": "동력계차 시험의 견인봉 출력 1,840 hp(시속 60.4 km).",
        },
        "_src": ["https://preservedbritishsteamlocomotives.com/north-british-locomotive-company-works-no-27056-class-r-r-766-4-6-4/", "https://en.wikipedia.org/wiki/Steamrail_Victoria", "https://en.wikipedia.org/wiki/Victorian_Railways_R_class"],
    },
    "au-na-puffingbilly": {
        "specs.lengthMm": 9398,
        "specs.weightT": 35,
        "_why": "자료조사 원고(2026-10-23) 반영: 2개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "운영사 제원표의 전장 30 ft 10 in.",
            "specs.weightT": "운영사 제원표는 운행 상태 중량을 35 t로 적는다. 34.9는 위키백과의 롱톤 값을 미터 톤으로 옮긴 것으로 보인다. 단위 확인이 필요하다.",
        },
        "_src": ["https://puffingbillyrailway.org.au/about/rolling-stock/locomotive-fleet/", "https://en.wikipedia.org/wiki/Victorian_Railways_NA_class"],
    },
    "ca-royalhudson": {
        "withdrawnYear": 1959,
        "specs.topSpeedKmh": None,
        "classDesignation": "CPR H1e",
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "위키백과 2860호 문서는 1959년 5월 퇴역으로 적는다. 『캐나디언 레일』 510호(2006)는 CPR 기록상 이 형식이 1960년까지 모두 퇴역했다고 적어, 1959년 퇴역과 어긋나지 않는다. 2860호만의 날짜를 밝힌 1차 자료는 찾지 못했다.",
            "specs.topSpeedKmh": "근거는 2839호를 소장한 박물관이 허드슨형 전체를 두고 쓴 '최고 시속 90마일'뿐이라 2860호 값으로 쓰지 않는다.",
            "classDesignation": "괄호를 뺀다.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Canadian_Pacific_2860", "https://exporail.org/canrail/canadian_rail_1990_plus/canadian-rail-510-2006.pdf", "https://nethercuttcollection.org/the-museum/the-museum-locomotive-private-car/", "https://en.wikipedia.org/wiki/Canadian_Pacific_Royal_Hudson"],
    },
    "ca-cn-6060": {
        "specs.lengthMm": 27435,
        "_why": "자료조사 원고(2026-10-23) 반영: 1개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "90 ft 0⅛ in의 정확한 환산값.",
        },
        "_src": ["https://en.wikipedia.org/wiki/Canadian_National_Class_U-1-f", "https://en.wikipedia.org/wiki/Canadian_National_6060"],
    },
    "ch-hg34": {
        "survivors": 4,
        "specs.lengthMm": 8750,
        "operators": ["Brig-Furka-Disentis-Bahn", "Furka-Oberalp-Bahn", "Dampfbahn Furka-Bergstrecke"],
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "남은 차량은 1·3·4·9호 4량이다 [1]. 10호는 눈사태로 부서졌고 5·6·7호는 해체됐으며, 2·8호는 1·9호 복원에 부품으로 쓰였다 [1, 2].",
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "operators": "처음 주문하고 쓴 것은 BFD이고, 1923년 파산 뒤 FO로 넘어갔다 [1].",
        },
        "_src": ["https://de.wikipedia.org/wiki/BFD_HG_3/4", "https://de.wikipedia.org/wiki/Dampfbahn_Furka-Bergstrecke", "https://www.loco-info.com/view.aspx?id=11796"],
    },
    "ch-e33": {
        "survivors": 26,
        "specs.lengthMm": 8700,
        "specs.weightT": 34.9,
        "operators": ["Schweizerische Centralbahn", "SBB"],
        "_why": "자료조사 원고(2026-10-23) 반영: 4개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "survivors": "영어 위키백과는 26량 보존과 그 목록을 싣는다 [2]. 독일어 위키는 이 목록에 없는 차량도 들어 실제 수가 더 많을 수 있다 [1].",
            "specs.lengthMm": "8511호의 완충기 포함 길이 8.7 m [3].",
            "specs.weightT": "운전 정비 중량은 묶음에 따라 32.7–34.9 t이고 [2], 제원 기준 차량 8511호는 34.9 t다 [3]. 33.6 t의 출처는 찾지 못했다.",
            "operators": "처음 차량은 1896년 스위스 중앙철도용이었다 [1].",
        },
        "_src": ["https://de.wikipedia.org/wiki/SBB_E_3/3", "https://en.wikipedia.org/wiki/SBB_E_3/3", "https://www.vvt.ch/locomotives"],
    },
    "ar-latrochita": {
        "specs.lengthMm": 14830,
        "specs.boilerPressureBar": 11.8,
        "classDesignation": None,
        "_why": "자료조사 원고(2026-10-23) 반영: 3개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.boilerPressureBar": "출처 값은 12 kg/cm²이며 11.8 bar로 환산해야 한다.",
            "classDesignation": "이 형식명을 뒷받침하는 출처를 찾지 못했다.",
        },
        "_src": ["https://www.patagoniaexpress.com/index.php/component/content/article/150-datos-tecnicos-y-detalles-de-funcionamiento-del-viejo-expreso-patagonico-la-trochita.html?catid=51&Itemid=166", "https://en.wikipedia.org/wiki/La_Trochita"],
    },
    "it-fs685": {
        "withdrawnYear": None,
        "specs.lengthMm": 11730,
        "specs.tractiveEffortKn": 110.8,
        "builders": ["Breda", "CEMSA", "Officine Meccaniche (Milano)", "Officine Meccaniche e Navali (Napoli)", "Reggiane"],
        "designer": "FS Ufficio Studi, Firenze",
        "_why": "자료조사 원고(2026-10-23) 반영: 5개 칸. 칸마다 이유는 _whyBy.",
        "_whyBy": {
            "withdrawnYear": "마지막 정기 운행이 685.222의 1975년 초(영어 위키)와 685.196의 1976년(이탈리아어 위키)으로 엇갈린다 [1, 2].",
            "specs.lengthMm": "원고가 출처와 함께 채운 값.",
            "specs.tractiveEffortKn": "11,300 kgf를 정확히 환산했다 [2].",
            "builders": "영어 위키백과가 브레다 221량, CEMSA 20량, 밀라노 OM·나폴리 OMN·레지아네 각 10량을 든다 [2]. 안살도는 열람한 자료 어디에도 없다.",
            "designer": "FS 피렌체 설계국이 설계했다 [1].",
        },
        "_src": ["https://it.wikipedia.org/wiki/Locomotiva_FS_685", "https://en.wikipedia.org/wiki/FS_Class_685", "https://www.fondazionefs.it/content/dam/fondazionefs/fondazione-fs-new/pdf/cataloghi-rotabili/03_locomotive_a_vapore.pdf", "https://it.wikipedia.org/wiki/Museo_nazionale_ferroviario_di_Pietrarsa"],
    },
}

def _set(d, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value


def _overlay(by_id, table, name, set_verified_default):
    missing = [k for k in table if k not in by_id]
    if missing:
        raise ValueError(f"verified.py {name} 에 있는데 LOCOS 에 없는 id: {missing}")
    for lid, fix in table.items():
        l = by_id[lid]
        for path, value in fix.items():
            if path.startswith("_"):
                continue
            _set(l, path, value)
        if set_verified_default:
            l["verified"] = fix.get("_verified", True)
        elif "_verified" in fix:
            l["verified"] = fix["_verified"]
        checked = l.setdefault("_checkedUrls", [])
        for url in fix.get("_src", []):
            if url not in checked:
                checked.append(url)


def apply(locos):
    """LOCOS(dict 리스트)에 대조본을 덧씌운다. 1차 대조본이 적용된 기관차 수를 돌려준다.

    확인에 쓴 링크는 `_checkedUrls` 에 모인다. 밑줄로 시작하는 키라 빌드 결과(JSON)에는 나가지 않는다.
    """
    by_id = {l["id"]: l for l in locos}
    _overlay(by_id, VERIFIED, "VERIFIED", True)
    # 재대조본·원고 반영 — 앞의 것 위에 다시 덧씌운다. _verified 를 명시하지 않으면 판정은 그대로.
    _overlay(by_id, RECHECK, "RECHECK", False)
    _overlay(by_id, RESEARCH, "RESEARCH", False)
    return len(VERIFIED)


def verified_ids():
    return sorted(VERIFIED)
