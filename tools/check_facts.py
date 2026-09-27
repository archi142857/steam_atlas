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
    ("us-up-bigboy-4014",  "specs.weightT",     539.6,   "4014 는 4884-1: 1,189,500 lb = 539.6 t (548 은 4884-2)"),
    ("us-nw-611",          "tenderAxles",       8,       "22D 탄수차 4축 대차 2개 = 16륜"),
    ("fr-231e",            "specs.boilerPressureBar", 16.7, "17 kg/cm² = 16.7 bar (초안 20 은 오류)"),
    ("fr-241p",            "specs.driverDiameterMm", 2000, "241 P 동륜 2,000 mm"),
    ("jp-c62",             "survivors",         5,       "C62 보존 1·2·3·17·26 = 5량"),
    ("ca-royalhudson",     "quantityBuilt",     45,      "로열 허드슨 칭호는 H1c·d·e 45량 전체"),
    # 2차 재대조 (2026-09-17)
    ("us-nw-y6b",          "specs.weightT",     436.1,   "Y6 계열 합계 961,500 lb = 436.1 t"),
    ("us-co-allegheny",    "specs.weightT",     545.7,   "1600~1644 배치(25-RB) 771,300 + 431,700 lb"),
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
    ("de-drg-52",      "nickname",              "전시표준형 (Kriegslok)", "별명 칸"),
    ("pl-pm36",        "nameKo",                "Pm36-2",   "Piękna Helena 는 별명"),
    ("ch-e33",         "nameKo",                "E 3/3",    "Tigerli 는 별명"),
    ("fr-231e",        "classDesignation",      "Nord 231 E / SNCF 2-231 E", "PO 가 아니라 Nord"),
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
    ("cn-km",          "location.name",          "국립철도박물관, 요크 (NRM York) — KF7", "KF7 은 런던이 아니라 요크"),
    ("in-fairyqueen",  "gaugeMm",                1676,     "인도 광궤"),
    ("in-fairyqueen",  "wheel.whyte",            "2-2-2WT", "웰탱크"),
    ("in-fairyqueen",  "tenderAxles",            2,        "소형 탄수차를 실제로 끈다"),
    ("ru-class-p36",   "specs.cylinders",        2,        "3기통 아님"),
    ("za-classgl",     "specs.driverDiameterMm", 1219,     "48in"),
    ("au-c38-3801",    "shape",                  "semi",   "3801 개체는 반유선형"),
    ("ca-royalhudson", "livery",                 "cpr-royal-hudson", "회색 보일러+터스컨 레드 판넬"),
    ("ar-latrochita",  "nickname",               "라 트로치타 (La Trochita)", "노선 애칭은 별명 칸"),
    ("za-class26",     "nickname",               "레드 데블 (Red Devil)", "별명 칸"),
]


def get(d, path):
    for k in path.split("."):
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
        if got != expect:
            bad.append(f"[{lid}] {path} = {got!r}, 기대 {expect!r} — {why}")

    # 전역 규칙
    for l in locos.values():
        whyte = l["wheel"]["whyte"].upper()
        if l["serviceType"] == "tank" and "T" not in whyte:
            bad.append(f"[{l['id']}] serviceType=tank 인데 Whyte 에 T 없음 ({whyte})")
        if "T" in whyte and l["tenderAxles"] not in (None, 0) and l["id"] not in TANK_WITH_TENDER:
            bad.append(f"[{l['id']}] 탱크식(T)인데 tenderAxles={l['tenderAxles']}")
        if l.get("nickname") and l["nickname"] in l["nameKo"]:
            bad.append(f"[{l['id']}] 별명이 이름 칸에 다시 들어감: {l['nameKo']}")

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
