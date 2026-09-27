#!/usr/bin/env python3
"""tools/references.py 의 정리본 `참고문헌.md` 를 만든다 (프로젝트 문서용).

    python3 tools/export_references_md.py > /tmp/참고문헌.md

빌드된 JSON(assets/data)을 읽으므로 먼저 build_seed.py 를 돌릴 것. 손으로 고치지 말고 references.py 를 고친 뒤 다시 생성한다.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "assets", "data")

KIND = {"book": "단행본", "article": "논문·기사", "thesis": "학위논문", "official": "공식 자료", "catalog": "소장품 기록"}


def cite(r):
    parts = [p for p in [r.get("author"), f"『{r['title']}』", r.get("publisher"),
                         "연도 미확인" if r.get("year") is None else str(r["year"])] if p]
    return ", ".join(parts)


def via(r):
    v = r.get("via") or ""
    if r.get("isbn"):
        v += f" · ISBN {r['isbn']}"
    if r.get("url"):
        v += f" · [링크]({r['url']})"
    return v


def cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def table(refs):
    out = ["| 구분 | 언어 | 서지 | 내용 | 확인 |", "|---|---|---|---|---|"]
    for r in refs:
        out.append(f"| {KIND.get(r['kind'], r['kind'])} | {(r.get('lang') or '').upper()} | {cell(cite(r))} | {cell(r.get('note'))} | {cell(via(r))} |")
    return "\n".join(out)


def main():
    with open(os.path.join(DATA, "locomotives.json"), encoding="utf-8") as f:
        d = json.load(f)
    with open(os.path.join(DATA, "countries.json"), encoding="utf-8") as f:
        c = json.load(f)
    locos = d["locomotives"]
    general = d.get("references") or d.get("generalReferences") or []
    n_loco = sum(1 for l in locos if l.get("references"))
    n_country = sum(len(ct.get("references") or []) for ct in c["countries"])
    n_total = len(general) + n_country + sum(len(l.get("references") or []) for l in locos)

    out = []
    out.append("# Steam Atlas — 참고문헌 (서적·논문·공식 자료)\n")
    out.append(f"2026-09-23 기준(0.1.0). `steam_atlas/tools/references.py` 의 정리본이며 앱 상세 화면 '참고문헌' 섹션과 같은 내용이다 — "
               f"종합 {len(general)} · 국가별 {n_country} · 기관차별 {n_loco}량(항목 {n_total}건, 같은 책이 여러 량에 걸리면 각각 셈). "
               "웹 페이지 출처(위키·박물관 웹)는 `고증-대조-기록.md` 에 따로 있다. 이 문서는 `tools/export_references_md.py` 가 만든다.\n")
    out.append("**원칙**")
    out.append("- 현지어 자료 우선: 한국(철도청·국가유산청·조선총독부 사서·철도차량기술검정단), 일본(国鉄·NDL·文化庁), 독일(EK/transpress), 프랑스(Chapelon·La Vie du Rail·CNRS), "
               "폴란드(WKŁ·Problemy Kolejnictwa), 러시아(Раков), 중국(中国铁道出版社), 남아공(Holland/Wardale) …")
    out.append("- 도서관 목록·출판사·학술DB·공식 페이지에서 **서지사항을 확인한 것만** 실었다. 확인 경로를 항목마다 적었다. 학술지 논문은 Crossref DOI 레코드로 제목·저자·권·쪽을 확인했다.")
    out.append("- 확인하지 못한 연도는 '연도 미확인'으로 둔다. 그럴듯하게 채우지 않는다.")
    out.append("- 접근이 막혀 확인하지 못한 것: 러시아어 위키 문헌목록(ru.wikipedia 차단), 중국어 위키(zh.wikipedia 차단), 국립러시아도서관 목록(nlr.ru 시간초과), "
               "국가유산포털·의왕시·roteco 100년사 본문(robots/시간초과). 러시아·중국은 판매·서지 사이트의 ISBN 기록으로 대신 확인했다.\n")

    out.append("## 여러 나라에 걸친 종합서\n")
    out.append(table(general))

    for ct in c["countries"]:
        out.append(f"\n## {ct['nameKo']}\n")
        out.append("### 이 나라 증기기관차 전반\n")
        out.append(table(ct.get("references") or []))
        mine = [l for l in locos if l["countryCode"] == ct["code"] and l.get("references")]
        if mine:
            out.append("\n### 기관차별\n")
            for l in mine:
                out.append(f"**{l['nameKo']}** (`{l['id']}`)\n")
                out.append(table(l["references"]))
                out.append("")
        missing = [l for l in locos if l["countryCode"] == ct["code"] and not l.get("references")]
        if missing:
            out.append("형식 문헌 없음(국가 표준서로 갈음): " + ", ".join(f"{l['nameKo']}(`{l['id']}`)" for l in missing) + "\n")

    out.append("\n## 더 찾아볼 것 (미확인·미수록)\n")
    out.append("- 한국: 정재정 『일제침략과 한국철도』(서울대출판부)·『철도주요연표』(철도청) — 서지 미확인으로 보류. 미카·파시 형식별 한국어 학술논문은 RISS 에서 직접 확인이 필요하다. "
               "국가등록문화유산 **미카형 증기기관차 161호** 등록 기록은 국가유산포털이 robots 로 막혀 못 봤다(129호·304호·파시 23호 기록은 검색 결과로 존재 확인).")
    out.append("- 일본: RM LIBRARY(ネコ・パブリッシング) 형식별 권, 『鉄道ピクトリアル』 특집호 — NDL 검색으로 권호를 특정하지 못해 보류.")
    out.append("- 미국: Bruce 『The Steam Locomotive in America』(1952), Kratville 『Steam Locomotives of the Union Pacific』 — 미확인.")
    out.append("- 프랑스: 『Le Train』 spécial «Les 140 C» — 권호·연도·저자 미확인(출판사 페이지에 서지 없음). 『La Locomotive Crampton』 소책자는 발행연도 미표기.")
    out.append("- 중국: 《中国铁路机车史》·《满铁的车辆》 — 서지 미확인. KF형은 Kenneth Cantlie 의 당시 Railway Gazette 기고가 1차 자료이나 권호 미확인. QJ·JS·SY·JF1 은 严介生 편 화보집으로 갈음.")
    out.append("- 호주: VR R형·NA형 형식 단행본(ARHS Victoria) 미확인 — 『Here comes Puffing Billy!』(보존회 소책자, 18쪽, 연도 미상)는 서지가 약해 뺐다. 스위스: E 3/3·HG 3/4 개별 단행본 미확인(Moser 로 갈음).")
    out.append("- 학술지: Proceedings IMechE(Gresley 관련) — 미확인. Transactions of the Newcomen Society 는 7편 수록(크램프턴 I·II, 레인힐, 트레비식, 스티븐슨, 샤플롱, 복식 3부).")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
