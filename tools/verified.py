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
        * _src 는 sources 에 덧붙는다(중복은 걸러냄).

여기 없는 기관차는 초안 그대로 나가고 verified=False 로 남는다.
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

def _set(d, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value


def apply(locos):
    """LOCOS(dict 리스트)에 대조본을 덧씌운다. 적용된 기관차 수를 돌려준다."""
    by_id = {l["id"]: l for l in locos}
    missing = [k for k in VERIFIED if k not in by_id]
    if missing:
        raise ValueError(f"verified.py 에 있는데 LOCOS 에 없는 id: {missing}")
    n = 0
    for lid, fix in VERIFIED.items():
        l = by_id[lid]
        for path, value in fix.items():
            if path.startswith("_"):
                continue
            _set(l, path, value)
        l["verified"] = fix.get("_verified", True)
        for url in fix.get("_src", []):
            if url not in l["sources"]:
                l["sources"].append(url)
        n += 1
    # 재대조본 — 1차 대조본 위에 다시 덧씌운다. _verified 를 명시하지 않으면 판정은 그대로.
    missing = [k for k in RECHECK if k not in by_id]
    if missing:
        raise ValueError(f"verified.py RECHECK 에 있는데 LOCOS 에 없는 id: {missing}")
    for lid, fix in RECHECK.items():
        l = by_id[lid]
        for path, value in fix.items():
            if path.startswith("_"):
                continue
            _set(l, path, value)
        if "_verified" in fix:
            l["verified"] = fix["_verified"]
        for url in fix.get("_src", []):
            if url not in l["sources"]:
                l["sources"].append(url)
    return n


def verified_ids():
    return sorted(VERIFIED)
