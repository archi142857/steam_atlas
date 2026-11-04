#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Atlas — 자료조사 원고 병합 (tools/manuscript/entries.json)

자료조사 세션이 76량을 다시 대조해 쓴 한영 원고를 앱 데이터에 합친다. build_seed.py 가 덧씌우기
(verified.py 의 VERIFIED → RECHECK → RESEARCH)를 마친 뒤 부른다.

원고가 정하는 것 (그대로 가져온다)
    이름·별명(한영), 뜻풀이·본문·연혁(한영 문장 짝 + 출처 번호), 제원 주석(원래 단위·단서·출처 번호),
    새 제원(기록 속도, 선륜·종륜 지름, 실린더 크기, 축거, 물탱크), 제원 기준, 표제란 수량 문구(quantityNote),
    지금 있는 곳(한영 + 좌표·지도 검색어), 출처 목록, 더 읽을거리, 시대·나라·생김새 설명(한영), 태그 영어 이름.

앱이 정하고 원고와 같아야 하는 것 (check 가 비교한다)
    표제란(제작·수량·보존 상태·퇴역·현존·차량 번호·차륜 배치), 궤간, 기존 제원 8칸과 중량 기준.
    값을 바꾸려면 verified.py 의 RESEARCH 에 이유·출처와 함께 적는다. 다르면 빌드가 실패한다.

원고 파일은 손으로 고치지 않는다. 자료조사 세션이 고친 판(공유\\자료조사\\entries.json)을 그대로 덮어쓴다.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "manuscript", "entries.json")

# 상세 화면의 제원 순서. 원고의 출처 번호가 이 순서로 읽을 때 1, 2, 3… 으로 늘어난다(빌드 때 검사).
SPEC_ORDER = [
    "gaugeMm", "driverDiameterMm", "leadingWheelDiameterMm", "trailingWheelDiameterMm",
    "cylinderSize", "cylinders", "boilerPressureBar", "wheelbaseMm", "waterL",
    "topSpeedKmh", "recordSpeedKmh", "tractiveEffortKn", "powerKw", "weightT", "lengthMm",
]
# 앱에 원래 있던 제원 칸(verified.py 가 값을 정하고 원고와 비교한다)
OLD_SPECS = ["lengthMm", "weightT", "driverDiameterMm", "boilerPressureBar", "cylinders",
             "tractiveEffortKn", "powerKw", "topSpeedKmh"]
# 원고가 새로 들여온 제원 칸(원고에서 그대로 가져온다)
NEW_SPECS = ["recordSpeedKmh", "leadingWheelDiameterMm", "trailingWheelDiameterMm",
             "cylinderSize", "wheelbaseMm", "waterL"]
HEAD = [("builtFrom", "builtFrom"), ("builtTo", "builtTo"), ("quantityBuilt", "quantityBuilt"),
        ("status", "status"), ("wheel", "wheel.whyte"), ("roadNumber", "roadNumber"),
        ("withdrawnYear", "withdrawnYear"), ("survivors", "survivors")]

# 장단역 증기기관차를 다룬 석사 논문. 그 기관차와 무관한 형식에서는 뺀다(자료조사 세션 권고, 대조 보고서 서지 메모).
JANGDAN_THESIS = "근대문화유산 경의선장단역증기기관차의 보존에 관한 연구 : 문화유산적 가치와 보존방침을 중심으로"
JANGDAN_DROP = {"kr-moga", "kr-teou", "kr-hyeogi"}


def load(path=PATH):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schemaVersion") != 2:
        raise ValueError(f"원고 schemaVersion {doc.get('schemaVersion')} — 2 를 기대함")
    return doc


def _get(d, path):
    for k in path.split("."):
        d = d[k]
    return d


def _same(a, b):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(float(a) - float(b)) < 1e-9
    return a == b


# ─────────────────────────────────────────────────────────────
# 원래 단위 표시
#
# 원고의 `orig` 는 출처에 적힌 그대로다("35,455 lbf at 85% boiler pressure", "84 Mp", "voie normale").
# 화면에는 미터법 값 옆에 **원래 단위의 수치만** 짧게 붙인다(1,067 mm  42 in). 조건과 단서는 원고의
# `note` 가 따로 한국어·영어로 갖고 있으므로 여기서는 버린다.
#   - 출처가 처음부터 미터법(mm, t, kN, km/h, bar, m³ …)이면 붙이지 않는다 — 같은 값을 두 번 쓰게 된다.
#   - 영미 단위(in, ft, lb, psi, gal, mph, long ton, hp …)와 옛 미터계 단위(at, kgf/cm², kp/cm², kgf, PS)는 붙인다.
#   - 실린더 수의 원문("compound 4 cylindres")은 단위가 아니라 설명이라 붙이지 않는다(단서는 note 에 있다).
# 규칙으로 정리되지 않는 몇 개는 ORIG_DISPLAY 에 손으로 적었다. 결과 전체는 `python3 tools/manuscript.py`
# 로 볼 수 있다.
# ─────────────────────────────────────────────────────────────
ORIG_DISPLAY = {
    # (id, 제원 칸): 화면에 붙일 원래 단위 표기 — None 이면 붙이지 않는다
    ("gb-trevithick-pendarren", "gaugeMm"): "4 ft 4 in",
    ("gb-trevithick-pendarren", "recordSpeedKmh"): "5 mph",
    ("gb-trevithick-pendarren", "weightT"): "5 tons",
    ("gb-locomotion-1", "recordSpeedKmh"): "15–16 mph",
    ("gb-locomotion-1", "weightT"): "6 tons 10 cwt",
    ("gb-lms-black5", "weightT"): "72.1 long tons",
    ("us-up-844", "weightT"): "907,890 lb",
    ("us-nw-611", "weightT"): "872,600 lb",
    ("us-sp-4449", "weightT"): "870,600 lb",
    ("in-wp", "weightT"): "173.5 long tons",
    ("in-wg", "weightT"): "173 long tons 13 cwt",
    ("za-class25nc", "weightT"): "223 long tons",
    ("za-class15f", "weightT"): "108 long tons 12 cwt",
    ("za-class25nc", "lengthMm"): "91 ft 6 9⁄16 in",
    ("za-class15f", "lengthMm"): "73 ft 5 15⁄16 in",
    ("za-classgl", "waterL"): "7,000 imp gal",
    ("cn-km", "weightT"): "192 long tons 14 cwt 2 qr",
    ("au-c38-3801", "weightT"): "196 tons",
    ("au-vr-r", "powerKw"): "1,840 dbhp",
    ("ar-latrochita", "boilerPressureBar"): "12 kgf/cm²",
    ("ar-latrochita", "powerKw"): "410 hp",
    ("ch-hg34", "topSpeedKmh"): None,
    ("fr-242a1", "powerKw"): "4,000 PS",
    ("fr-241p", "powerKw"): "4,000 PS",
    ("fr-241p", "tractiveEffortKn"): "20,434 kgf",
    ("fr-crampton", "weightT"): None,
    ("fr-140c", "weightT"): None,
    ("it-fs685", "powerKw"): "1,250 PS",
    ("ru-aa20", "tractiveEffortKn"): "32.0 Mp",
    ("jp-c62", "tractiveEffortKn"): "13,870 kgf",
    ("jp-c57", "tractiveEffortKn"): "12,820 kgf",
    # 영국에서 만든 기관차는 출처가 미터법을 앞에 적었어도 원래 단위(피트·인치·psi·영국 갤런)를 붙인다
    ("jp-class150", "boilerPressureBar"): "140 psi",
    ("jp-class150", "waterL"): "450 imp gal",
    ("jp-class150", "lengthMm"): "24 ft 4 in",
    ("de-adler", "leadingWheelDiameterMm"): "3 ft 0 in",
    ("de-adler", "trailingWheelDiameterMm"): "3 ft 0 in",
    ("cn-km", "lengthMm"): "93 ft 2½ in",
    ("cn-km", "waterL"): "6,600 imp gal",
    ("za-class25nc", "waterL"): "10,500 imp gal",
    # 위키백과가 mm 값을 인치로 바꿔 적은 것이라 원래 단위가 아니다
    ("kr-mika3-129", "cylinderSize"): None,
    ("kr-mika3-161", "cylinderSize"): None,
}

_METRIC_UNITS = r"(?:mm|m|cm|km/h|t|tonnes|kg|kN|kW|bar|BAR|bars|kPa|m³|l|L|Mp)"
_LEAD = re.compile(r"^(?:about|nearly|approx\.?|environ|ca\.|c\.)\s+", re.I)
_PRIMARY_END = re.compile(r"\s*(?:\(|;|,\s|\s+at\s+(?=[\d.]+\s*(?:%|mph|km))|\s+in working order|\s+with\s|\s+au\s|\s+à\s|\s+over\s)")
_NONMETRIC = re.compile(
    r"\b(?:in|ft|lb|lbf|psi|gal|mph|tons?|cwt|qr|LT|hp|dbhp|ihp|at|kgf|PS|PSi|ch|CV|KM)\b|lb/sq in|kgf/cm²|kg/cm²|kp/cm²|л\.\s?с\.|马力")


def _num_fix(s):
    # "1 620 PS" 처럼 공백으로 끊은 천 단위를 쉼표로
    return re.sub(r"(?<=\d) (?=\d{3}\b)", ",", s)


def orig_display(lid, key, orig):
    """출처 원문 `orig` → 화면에 붙일 원래 단위 표기(없으면 None)."""
    if (lid, key) in ORIG_DISPLAY:
        return ORIG_DISPLAY[(lid, key)]
    if orig is None or key == "cylinders":
        return None
    s = _LEAD.sub("", orig.strip())
    m = _PRIMARY_END.search(s)
    primary = (s[:m.start()] if m else s).strip()
    if not primary or not _NONMETRIC.search(primary):
        return None
    primary = (primary.replace("lb/sq in", "psi").replace("PSi", "PS")
               .replace("imperial", "imp").replace(" LT", " long tons"))
    primary = re.sub(r"\bkg/cm²", "kgf/cm²", primary)
    primary = re.sub(r"\s*马力", " PS", primary)
    primary = re.sub(r"\s*л\.\s?с\.", " PS", primary)
    primary = re.sub(r"\b(\d[\d,.]*) (?:KM|ch|CV)\b", r"\1 PS", primary)
    if key == "tractiveEffortKn":
        primary = re.sub(r"\blb\b", "lbf", primary)
    primary = re.sub(r"(\d),(\d{1,2})\b", r"\1.\2", primary)  # 소수점 쉼표(21,1) → 21.1
    primary = re.sub(r"\b(\d[\d,.]*) kg\b", r"\1 kgf", primary)
    primary = re.sub(r"(?<=\d)(\d{3}) PS", r"\1 PS", primary)
    primary = _num_fix(primary)
    # 네 자리 이상 숫자에 쉼표 (원문이 "3077 л. с." 처럼 붙여 쓴 경우)
    primary = re.sub(r"\b(\d{1,3})(\d{3})\b(?![.,]\d)", r"\1,\2", primary)
    return primary


# ─────────────────────────────────────────────────────────────
# 검사 — 덧씌우기가 끝난 앱 값이 원고와 같은가
# ─────────────────────────────────────────────────────────────
def check(locos, doc):
    """원고와 다른 값 목록(문자열)을 돌려준다. 빈 목록이면 통과."""
    ms = {e["id"]: e for e in doc["entries"]}
    errs = []
    app_ids = {l["id"] for l in locos}
    if app_ids != set(ms):
        errs.append(f"원고와 앱의 id 가 다르다: 앱에만 {sorted(app_ids - set(ms))}, 원고에만 {sorted(set(ms) - app_ids)}")
    for l in locos:
        m = ms.get(l["id"])
        if not m:
            continue
        p = f"[{l['id']}]"
        for hk, path in HEAD:
            if not _same(_get(l, path), m["head"][hk]):
                errs.append(f"{p} {path}: 앱 {_get(l, path)!r} / 원고 {m['head'][hk]!r}")
        if "gaugeMm" in m["specs"] and not _same(l["gaugeMm"], m["specs"]["gaugeMm"]["value"]):
            errs.append(f"{p} gaugeMm: 앱 {l['gaugeMm']!r} / 원고 {m['specs']['gaugeMm']['value']!r}")
        for k in OLD_SPECS:
            mv = m["specs"][k]["value"] if k in m["specs"] else None
            if not _same(l["specs"][k], mv):
                errs.append(f"{p} specs.{k}: 앱 {l['specs'][k]!r} / 원고 {mv!r}")
        mb = m["specs"]["weightT"].get("basis") if "weightT" in m["specs"] else None
        if not _same(l["specs"]["weightBasis"], mb):
            errs.append(f"{p} specs.weightBasis: 앱 {l['specs']['weightBasis']!r} / 원고 {mb!r}")
        errs += _check_numbering(m)
    return errs


def _check_numbering(m):
    """출처 번호가 화면 순서(뜻풀이 → 본문 → 제원 → 연혁 → 지금 있는 곳)로 1, 2, 3… 처음 나오는지, 목록과 맞는지."""
    seq = list(m["gloss"]["src"])
    for b in m["body"]:
        seq += b["src"]
    for k in SPEC_ORDER:
        if k in m["specs"]:
            seq += m["specs"][k]["src"]
    for h in m["history"]:
        seq += h["src"]
    if m["location"]:
        seq += m["location"]["src"]
    if m.get("quantityNote"):
        seq += m["quantityNote"]["src"]
    first = []
    for n in seq:
        if n not in first:
            first.append(n)
    errs = []
    listed = sorted(s["n"] for s in m["sources"])
    if listed != list(range(1, len(listed) + 1)):
        errs.append(f"[{m['id']}] 출처 목록 번호가 1부터 이어지지 않는다: {listed}")
    if set(first) != set(listed):
        errs.append(f"[{m['id']}] 본문에 쓴 출처와 출처 목록이 다르다: {sorted(set(first) ^ set(listed))}")
    unknown = [k for k in m["specs"] if k not in SPEC_ORDER]
    if unknown:
        errs.append(f"[{m['id']}] 앱이 모르는 제원 칸: {unknown}")
    return errs


# ─────────────────────────────────────────────────────────────
# 병합
# ─────────────────────────────────────────────────────────────
def _pair(x):
    return {"ko": x["ko"], "en": x["en"], "src": list(x["src"])}


def merge(locos, doc, tag_keep):
    """원고가 정하는 칸을 기관차 dict 에 넣고, 원고로 대체된 옛 칸(summary·highlights·옛 sources·references)을 뺀다."""
    ms = {e["id"]: e for e in doc["entries"]}
    for l in locos:
        m = ms[l["id"]]
        l["nameKo"], l["nameEn"] = m["nameKo"], m["nameEn"]
        l.pop("nickname", None)
        l["nicknameKo"], l["nicknameEn"] = m["nicknameKo"], m["nicknameEn"]
        qn = m.get("quantityNote")
        l["quantityNote"] = _pair(qn) if qn else None
        # 새 제원 칸 (값은 원고 그대로)
        for k in NEW_SPECS:
            l["specs"][k] = m["specs"][k]["value"] if k in m["specs"] else None
        l["specsBasis"] = {"ko": m["specsBasis"]["ko"], "en": m["specsBasis"]["en"]} if m.get("specsBasis") else None
        notes = {}
        for k in SPEC_ORDER:
            sv = m["specs"].get(k)
            if not sv:
                continue
            note = sv.get("note") or {}
            notes[k] = {
                "orig": orig_display(l["id"], k, sv.get("orig")),
                "noteKo": note.get("ko"),
                "noteEn": note.get("en"),
                "src": list(sv["src"]),
            }
        l["specNotes"] = notes
        loc = m["location"]
        l["location"] = None if loc is None else {
            "nameKo": loc["ko"], "nameEn": loc["en"],
            "noteKo": loc.get("noteKo"), "noteEn": loc.get("noteEn"),
            "lat": loc.get("lat"), "lon": loc.get("lon"),
            "query": loc.get("query"), "src": list(loc["src"]),
        }
        l["gloss"] = _pair(m["gloss"])
        l["body"] = [_pair(b) for b in m["body"]]
        l["history"] = [{"date": h["date"], "approx": bool(h.get("approx")), "ko": h["ko"], "en": h["en"],
                         "src": list(h["src"])} for h in m["history"]]
        l["sources"] = [{"n": s["n"], "kind": s.get("kind"), "tier": s.get("tier"), "lang": s.get("lang"),
                         "ko": s["ko"], "en": s["en"], "url": s.get("url")} for s in sorted(m["sources"], key=lambda s: s["n"])]
        l["furtherReading"] = [_reading(r, l.get("references") or []) for r in m["furtherReading"]
                               if not (l["id"] in JANGDAN_DROP and r["title"] == JANGDAN_THESIS)]
        # 태그: 평가어(원고 태그표의 keep=false)는 뺀다
        l["tags"] = [t for t in l["tags"] if tag_keep.get(t, {}).get("keep", True)]
        l["tagsEn"] = [tag_keep[t]["en"] if t in tag_keep else t for t in l["tags"]]
        for old in ("summary", "highlights", "references"):
            l.pop(old, None)
    return ms


def _reading(r, app_refs):
    """더 읽을거리 한 건. 앱 참고문헌에서 온 것은 서지 확인 경로(via)를 이어받는다."""
    via = None
    if r.get("origin") == "app":
        for a in app_refs:
            if (a["title"] == r["title"] or (a.get("isbn") and a.get("isbn") == r.get("isbn"))
                    or (a.get("url") and a.get("url") == r.get("url"))):
                via = a.get("via")
                break
    return {
        "kind": r.get("kind") or "book",
        "author": r.get("author") or "",
        "title": r["title"],
        "publisher": r.get("publisher") or "",
        "year": r.get("year"),
        "lang": r.get("lang") or "",
        "isbn": r.get("isbn"),
        "url": r.get("url"),
        "noteKo": r.get("noteKo") or "",
        "noteEn": r.get("noteEn") or "",
        "via": via,
    }


def tag_table(doc):
    return doc["tags"]["map"]


def eras(doc, base):
    """시대 설명을 원고의 한영 설명으로 바꾼다(구간·이름은 앱 값과 같아야 한다)."""
    by = {e["id"]: e for e in doc["eras"]}
    out = []
    for e in base:
        m = by[e["id"]]
        if (m["from"], m["to"], m["ko"], m["en"]) != (e["from"], e["to"], e["ko"], e["en"]):
            raise ValueError(f"시대 {e['id']} 의 구간·이름이 원고와 다르다: 앱 {e} / 원고 {m}")
        out.append({"id": e["id"], "ko": e["ko"], "en": e["en"], "from": e["from"], "to": e["to"],
                    "noteKo": m["noteKo"], "noteEn": m["noteEn"]})
    return out


def country_blurbs(doc):
    return {c["code"]: {"ko": c["ko"], "en": c["en"]} for c in doc["countries"]["items"]}


def shape_texts(doc):
    return {s["id"]: s for s in doc["shapes"]}


if __name__ == "__main__":
    # 원래 단위 표시 결과를 모두 보여 준다 (원문 → 화면).
    doc = load()
    shown = hidden = 0
    for m in doc["entries"]:
        for k in SPEC_ORDER:
            sv = m["specs"].get(k)
            if not sv or sv.get("orig") is None:
                continue
            d = orig_display(m["id"], k, sv["orig"])
            if d is None:
                hidden += 1
            else:
                shown += 1
            print(f"{m['id']:<26} {k:<24} {sv['orig']!s:<58} → {d}")
    print(f"붙임 {shown} / 붙이지 않음 {hidden}")
