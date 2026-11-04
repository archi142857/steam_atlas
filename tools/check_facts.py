#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Atlas — 고증 회귀 검사

한 번 출처로 바로잡은 값이 나중에 다시 틀어지는 것을 막는다.
`python3 tools/build_seed.py` 뒤에 `python3 tools/check_facts.py` 를 돌린다. 하나라도 틀리면 exit 1.

FACTS 항목: (기관차 id, 점 표기 경로, 기대값, 왜 이 값인지)
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(ROOT, "assets", "data", "locomotives.json")

FACTS = [
    # 단위 — long ton 을 t 로 옮겨 적었던 값들 (2026-09-16 재대조). 중량은 기준이 같이 붙어야 한다
    ("gb-lner-a4-mallard", "specs.weightT",     104.6,   "기관차 단독 102.95 long tons = 104.6 t (165 는 long tons 합계)"),
    ("gb-lner-a4-mallard", "specs.weightBasis", "loco",  "위 값의 기준"),
    ("gb-lner-a4-mallard", "specs.tractiveEffortKn", 157.7, "35,455 lbf = 157.7 kN"),
    ("gb-gwr-king",        "specs.weightT",     90.4,    "89 long tons = 90.4 t 기관차 단독"),
    ("us-up-bigboy-4014",  "specs.weightT",     539.5,   "형식도 1,189,500 lb × 0.45359237 = 539.5 t (2026-10-23 원고, 이전 539.6)"),
    ("us-nw-611",          "tenderAxles",       8,       "22D 탄수차 4축 대차 2개 = 16륜"),
    ("fr-231e",            "specs.boilerPressureBar", 16.7, "17 kg/cm² = 16.7 bar (초안 20 은 오류)"),
    ("fr-241p",            "specs.driverDiameterMm", 2020, "프랑스어 위키 2,020 mm, 소유 협회 2,022 mm(새 바퀴 테). 2,000 은 영어 위키만 (2026-10-23)"),
    ("jp-c62",             "survivors",         5,       "C62 보존 1·2·3·17·26 = 5량"),
    ("ca-royalhudson",     "quantityBuilt",     45,      "로열 허드슨 칭호는 H1c·d·e 45량 전체"),
    # 2차 재대조 (2026-09-17)
    ("us-nw-y6b",          "specs.weightT",     None,    "436.1 t 는 Y6/Y6a 값 — Y6b 값은 확인하지 못해 비움 (2026-10-23)"),
    ("us-co-allegheny",    "specs.weightT",     349.9,   "기관차만 771,300 lb. 탄수차가 세 종류라 합계는 쓰지 않는다 (2026-10-23, 이전 545.7)"),
    ("us-co-allegheny",    "specs.weightBasis", "loco",  "위 값의 기준"),
    ("fr-crampton",        "specs.driverDiameterMm", 2300, "Cail 1852년형 동륜 2,300 mm (초기형 2,100 아님)"),
    ("fr-crampton",        "specs.weightT",     27.0,    "Le Continent 운전정비 27 t (초안 48 은 근거 없음)"),
    ("fr-140c",            "quantityBuilt",     340,     "340량 (370 은 마지막 차번)"),
    ("jp-9600",            "specs.weightT",     60.35,   "9600형 기관차 단독 60.35 t"),
    ("jp-8620",            "specs.weightT",     48.83,   "8620형 기관차 운전정비중량 48.83 t"),
    # 시대는 제작 시작 연도로 계산한다 (1918년 차가 1920–1945 머리글 아래 서지 않게)
    ("cn-jf",              "era",               "classic", "JF1(ミカイ) 제작 시작 1918 → 성숙기"),
    ("us-nw-611",          "era",               "golden",  "1941 → 황금기"),
    # 탱크식/탄수차식 — 이 앱에서 가장 자주 틀렸던 부분
    ("kr-moga",        "wheel.whyte",           "2-6-0T",  "모가형은 탱크식"),
    ("kr-moga",        "tenderAxles",           0,         "탱크식은 탄수차 없음"),
    ("jp-class150",    "wheel.whyte",           "2-4-0T",  "150형(1호 기관차)은 탱크식"),
    ("kr-hyeogi",      "wheel.whyte",           "2-8-2T",  "혀기형은 탱크식"),
    ("jp-c11",         "wheel.whyte",           "2-6-4T",  "C11은 탱크식"),
    ("ch-e33",         "wheel.whyte",           "0-6-0T",  "E 3/3 티거리는 탱크식"),
    # 유선형은 '형식 전체'가 아니라 일부 개체만인 경우 — 대표 실루엣은 일반형
    ("us-nyc-hudson",  "shape",                 "american", "J-3a 50량 중 유선형은 10량"),
    ("de-drg-0310",    "shape",                 "classic",  "03.10 유선형 외장은 전후 전부 철거"),
    # 도색
    ("de-dr-18201",    "livery",                "dr-green", "18 201 현재 도색은 DR 그린"),
    ("us-nyc-hudson",  "livery",                "nyc-black", "형식 대표 도색은 검정(회색은 드레이퍼스 10량)"),
    # 공인 형식명 ↔ 별명 분리
    ("de-drg-52",      "nameKo",                "52형",     "Kriegslok 은 별명"),
    ("de-drg-52",      "nicknameKo",            "전시 기관차", "'Kriegslok'는 '전쟁 기관차'. '표준형'의 뜻은 없다 (2026-10-23)"),
    ("de-drg-52",      "nicknameEn",            "Kriegslok", "별명 칸(영어)"),
    ("pl-pm36",        "nameKo",                "Pm36-2",   "Piękna Helena 는 별명"),
    ("ch-e33",         "nameKo",                "E 3/3",    "Tigerli 는 별명"),
    ("fr-231e",        "classDesignation",      "Nord 3.1111–3.1130, 3.1171–3.1198 / SNCF 2-231 E 1–48",
     "노르 시절에는 '231 E' 기호를 쓰지 않았다 (2026-10-23)"),
    ("de-dr-18201",    "classDesignation",      "DR 18 201", "형식이 아니라 단일 차호"),
    # 제원
    ("gb-gwr-king",    "specs.driverDiameterMm", 1981,     "6ft 6in"),
    ("gb-lms-duchess", "tenderAxles",            3,        "스태니어 표준 탄수차 6륜"),
    ("gb-trevithick-pendarren", "gaugeMm",       1321,     "페니다렌 트램로드 4ft 4in"),
    ("us-co-allegheny", "specs.driverDiameterMm", 1702,    "67in"),
    ("us-up-844",      "tenderAxles",            7,        "센티페드 탄수차"),
    ("kr-mika3-129",   "specs.weightBasis",      "loco",   "기관차 단독 중량"),
    ("jp-d51",         "specs.weightBasis",      "locoAndTender", "운전정비중량(탄수차 포함)"),
    ("de-drg-05",      "builtTo",                1937,     "05 003 은 1937"),
]


# 웰탱크인데 소형 탄수차를 실제로 끄는 예외 (build_seed.TANK_WITH_TENDER 와 같게)
TANK_WITH_TENDER = {"in-fairyqueen"}

# 이번에 출처로 바로잡은 값들
FACTS += [
    ("cn-km",          "nameKo",                 "KF형",    "KD 는 별개 형식"),
    ("cn-km",          "location.nameKo",        "국립철도박물관 그레이트 홀, 영국 요크", "KF7 은 런던이 아니라 요크"),
    ("in-fairyqueen",  "gaugeMm",                1676,     "인도 광궤"),
    ("in-fairyqueen",  "wheel.whyte",            "2-2-2WT", "웰탱크"),
    ("in-fairyqueen",  "tenderAxles",            2,        "소형 탄수차를 실제로 끈다"),
    ("ru-class-p36",   "specs.cylinders",        2,        "3기통 아님"),
    ("za-classgl",     "specs.driverDiameterMm", 1219,     "48in"),
    ("au-c38-3801",    "shape",                  "semi",   "3801 개체는 반유선형"),
    ("ca-royalhudson", "livery",                 "cpr-royal-hudson", "회색 보일러+터스컨 레드 판넬"),
    ("ar-latrochita",  "nameKo",                 "라 트로치타 2-8-2형", "노선 애칭을 이름으로 옮겼다 (2026-10-23)"),
    ("ar-latrochita",  "nicknameKo",             None,     "위와 같음 — 별명 칸은 비운다"),
    ("ar-latrochita",  "classDesignation",       None,     "형식명을 뒷받침하는 출처가 없다 (2026-10-23)"),
    ("za-class26",     "nicknameKo",             "레드 데블", "별명 칸"),
]


# 자료조사 원고 반영 (2026-10-23) — 최고속도와 기록 속도를 나눴다. 최고속도는 설계·허용 값만.
FACTS += [
    ("gb-lner-a4-mallard", "specs.topSpeedKmh",   None,    "202.8 은 1948년 기념판 값. 설계 최고속도는 자료 없음"),
    ("gb-lner-a4-mallard", "specs.recordSpeedKmh", 201.2,  "1938-07-03 125 mph (LNER 발표·기네스)"),
    ("gb-lner-a4-mallard", "specs.lengthMm",      21650,   "21,340 은 A3 값. 소장 기관 기록 71 ft 0⅜ in"),
    ("de-drg-05",          "specs.topSpeedKmh",   175,     "설계 최고속도"),
    ("de-drg-05",          "specs.recordSpeedKmh", 200.4,  "1936-05-11 05 002"),
    ("us-milw-classa",     "specs.recordSpeedKmh", 179.4,  "1935년 업계지 두 곳 111.5 mph"),
    ("gb-rocket",          "withdrawnYear",       1840,    "1840년 브램프턴에서 운행 종료. 1862 는 기증 연도"),
    ("gb-locomotion-1",    "gaugeMm",             1422,    "개통 당시 S&DR 4 ft 8 in"),
    ("ru-aa20",            "gaugeMm",             1524,    "1960년 해체 — 1,524 mm 시기에만 존재"),
    ("kr-moga",            "specs.driverDiameterMm", 1067, "RMM 1898년 3월호 42 in"),
    ("kr-moga",            "shape",               "classic", "출고 사진: 완충기·스크루 연결기, 카우캐처 없음"),
    ("jp-c57",             "roadNumber",          "C57 1", "대표 차량을 교토 소속 C57 1 로 (2026-10-23)"),
    ("de-drg-52",          "quantityNote.ko",     "7,000량 이상", "자료마다 수량이 달라 숫자 하나로 쓰지 않는다"),
    ("cn-qj",              "tenderAxles",         4,       "전장 26,000 mm 는 4축 탄수차 기준"),
    ("ru-class-l",         "location.lat",        None,    "'러시아 각지' — 좌표 없이 글로만"),
]

# 장단역 증기기관차 석사 논문은 그 기관차와 무관한 형식에서 뺀다 (자료조사 권고)
JANGDAN = "근대문화유산 경의선장단역증기기관차의 보존에 관한 연구"
NO_JANGDAN = {"kr-moga", "kr-teou", "kr-hyeogi"}

# 원고 문체 규칙: 설명 글에 줄표(—)·물결표(~)를 쓰지 않는다
BANNED_IN_PROSE = ("—", "~")


_MISSING = object()


def get(d, path):
    for k in path.split("."):
        if not isinstance(d, dict) or k not in d:
            return _MISSING
        d = d[k]
    return d


def main():
    data = json.load(open(JSON, encoding="utf-8"))
    locos = {l["id"]: l for l in data["locomotives"]}
    bad = []

    for lid, path, expect, why in FACTS:
        if lid not in locos:
            bad.append(f"[{lid}] 항목 없음")
            continue
        got = get(locos[lid], path)
        if got is _MISSING:
            bad.append(f"[{lid}] {path} 칸이 없음 — {why}")
        elif got != expect:
            bad.append(f"[{lid}] {path} = {got!r}, 기대 {expect!r} — {why}")

    # 전역 규칙
    for l in locos.values():
        whyte = l["wheel"]["whyte"].upper()
        if l["serviceType"] == "tank" and "T" not in whyte:
            bad.append(f"[{l['id']}] serviceType=tank 인데 Whyte 에 T 없음 ({whyte})")
        if "T" in whyte and l["tenderAxles"] not in (None, 0) and l["id"] not in TANK_WITH_TENDER:
            bad.append(f"[{l['id']}] 탱크식(T)인데 tenderAxles={l['tenderAxles']}")
        if l.get("nicknameKo") and l["nicknameKo"] in l["nameKo"]:
            bad.append(f"[{l['id']}] 별명이 이름 칸에 다시 들어감: {l['nameKo']}")
        if l.get("nicknameEn") and l["nicknameEn"] in l["nameEn"]:
            bad.append(f"[{l['id']}] 영어 별명이 영어 이름 칸에 다시 들어감: {l['nameEn']}")
        if "(" in l["nameEn"] or l["nameEn"].startswith("Class "):
            bad.append(f"[{l['id']}] 영어 이름 규칙(괄호 없음, 'Class'로 시작하지 않음) 위반: {l['nameEn']}")
        # 기록 속도와 최고속도는 따로 — 기록 속도가 최고속도보다 낮을 수는 없다
        sp = l["specs"]
        if sp["topSpeedKmh"] and sp["recordSpeedKmh"] and sp["recordSpeedKmh"] < sp["topSpeedKmh"] - 1e-9:
            bad.append(f"[{l['id']}] 기록 속도 {sp['recordSpeedKmh']} < 최고속도 {sp['topSpeedKmh']}")
        if l["id"] in NO_JANGDAN and any(JANGDAN in r["title"] for r in l["furtherReading"]):
            bad.append(f"[{l['id']}] 장단역 증기기관차 논문이 더 읽을거리에 남아 있음")
        prose = [l["gloss"]["ko"], l["gloss"]["en"]] + [x[k] for x in l["body"] + l["history"] for k in ("ko", "en")]
        for t in prose:
            if any(b in t for b in BANNED_IN_PROSE):
                bad.append(f"[{l['id']}] 설명 글에 줄표·물결표: {t[:40]}…")

    no_basis = [l["id"] for l in locos.values()
                if l["specs"]["weightT"] is not None and l["specs"].get("weightBasis") is None]
    verified = sum(1 for l in locos.values() if l["verified"])

    print(f"고증 검사: {len(FACTS)}개 고정값 + 전역 규칙 / 기관차 {len(locos)}량 / verified {verified}량")
    print(f"  중량 기준(weightBasis) 미표기: {len(no_basis)}량"
          + (f" — {', '.join(no_basis[:12])}{' …' if len(no_basis) > 12 else ''}" if no_basis else ""))
    if bad:
        print("실패:")
        for b in bad:
            print("  -", b)
        sys.exit(1)
    print("  이상 없음")


if __name__ == "__main__":
    main()
