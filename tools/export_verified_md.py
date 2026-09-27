#!/usr/bin/env python3
"""tools/verified.py 를 마크다운 표로 요약한다 — 프로젝트 문서 `고증-대조-기록.md` 의 원본.

    python3 tools/export_verified_md.py > /tmp/고증-대조-기록.md

1차 대조본(VERIFIED)·재대조본(RECHECK)·2차 대조(`_why_2`)를 그대로 옮긴다. 손으로 고치지 말고 verified.py 를 고친 뒤 다시 생성할 것.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _names():
    with open(os.path.join(HERE, "..", "assets", "data", "locomotives.json"), encoding="utf-8") as f:
        d = json.load(f)
    return {l["id"]: l["nameKo"] for l in d["locomotives"]}, d


def _src(entry):
    srcs = entry.get("_src") or []
    if isinstance(srcs, str):
        srcs = [srcs]
    return " ".join(f"[{i + 1}]({u})" for i, u in enumerate(srcs))


def _fields(entry):
    keys = [k for k in entry if not k.startswith("_")]
    return ", ".join(f"`{k}`" for k in keys) if keys else "변경 없음"


def _cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def main():
    v = _load("verified")
    names, data = _names()
    n_ver = sum(1 for l in data["locomotives"] if l.get("verified"))
    n_all = len(data["locomotives"])
    out = []
    out.append("# Steam Atlas — 고증 대조 기록 (tools/verified.py 요약)\n")
    out.append(f"2026-09-12 1차 대조, 2026-09-16~17 재대조(v0.11) + 2차 대조 10량(v0.11 후반). {n_all}량 전부 웹 출처와 대조했다. "
               f"✅ = `verified=true`({n_ver}량), ⚠️ = 출처 충돌·자료 부족으로 미확정({n_all - n_ver}량).")
    out.append("원본은 `steam_atlas/tools/verified.py` (`VERIFIED` 1차 대조본 + `RECHECK` 재대조본, 각각 `_why`/`_src` 포함; 2차 대조는 `_why_2`). "
               "서적·논문·공식 자료는 `참고문헌.md` 에 따로 있다. 이 문서는 `tools/export_verified_md.py` 가 만든다 — 손으로 고치지 말 것.\n")
    out.append("규칙: 초안(`build_seed.py`)의 값은 추정일 수 있다. 출처로 확인한 값만 대조본에 적고, 확인 불가면 `None`(앱에서 `—`)으로 비운다. 추론으로 값을 고르지 않는다.")
    out.append("**단위도 본다** — long ton·lbf·kgf/cm²·psi 는 반드시 t·kN·bar 로 환산하고, 중량에는 기준(기관차 단독 / +탄수차)을 붙인다(v0.11 부터). "
               "v0.11 2차 대조 뒤로 76량 전부 중량 기준이 있다.\n")

    # 1차
    out.append("## 1차 대조본 (`VERIFIED`)\n")
    out.append("| id | 이름 | 상태 | 확인 내용 (`_why`) | 덧씌운 필드 | 출처 |")
    out.append("|---|---|---|---|---|---|")
    for lid, e in v.VERIFIED.items():
        final_ok = next((l.get("verified") for l in data["locomotives"] if l["id"] == lid), None)
        st = "✅" if e.get("_verified", True) else "⚠️ 미확정"
        if not e.get("_verified", True) and final_ok:
            st = "⚠️→✅ (2차에서 확정)"
        out.append(f"| `{lid}` | {names.get(lid, '')} | {st} | {_cell(e.get('_why'))} | {_fields(e)} | {_src(e)} |")

    # 재대조
    out.append("\n## 재대조 (2026-09-16~17) — 단위·탄수차·본문 (v0.11)\n")
    out.append("1차 대조는 숫자가 출처와 '같은가'만 봤고 **단위**를 보지 않았다. 영국 자료의 long ton(1.016 t)이 그대로 t 로 들어와 있었고 "
               "(맬러드 165 → 실제 165 long tons = 167.6 t, 기관차 단독은 104.6 t), 견인력은 lbf→kN 환산이 어긋난 값이 여럿 있었다. "
               "이번에는 위키백과 인포박스의 **미터법 값**을 그대로 옮기고 중량에는 반드시 기준(기관차 단독 / +탄수차)을 붙였다. "
               "탄수차 축수는 인포박스의 탄수차 형식(2'2'T34 = 4축, EW1 = 3축 보기 2개…)이나 탄수차 중량÷축중(축당 20~28 t)으로 정했다 — "
               "그림용 값이라 이 정도로 충분하다. 본문 오류도 함께 고쳤다(C62 보일러 출처 D51→**D52**, C62 2 별칭 '스완'→'스왈로 엔젤', "
               "ATSF 3751 이 '노던' 이름의 유래라는 잘못된 문장, HG 3/4 베트남 귀환 량수, 시대 구간 밖에 놓인 4량의 era 재배정 등). "
               "원본은 `tools/verified.py` 의 `RECHECK` (1차 대조본 `VERIFIED` 뒤에 덧씌워진다). 회귀 검사는 `tools/check_facts.py`.\n")
    out.append("id `jp-c62-2-note` 는 9600형인데 이름이 잘못 붙어 있어 `jp-9600` 으로 바꿨다.\n")
    out.append("| id | 덧씌운 필드 | 왜 (`_why`) | 출처 |")
    out.append("|---|---|---|---|")
    for lid, e in v.RECHECK.items():
        out.append(f"| `{lid}` | {_fields(e)} | {_cell(e.get('_why'))} | {_src(e)} |")

    # 2차
    second = [(lid, e) for lid, e in v.RECHECK.items() if e.get("_why_2")]
    out.append(f"\n## 2차 대조 (2026-09-17, v0.11 후반) — 미확정·기준 없음 {len(second)}량 마무리\n")
    out.append("1차에서 `_verified: False` 였거나 중량 기준이 없던 량을 프랑스어·일본어 위키 인포박스, parowozy.pl, patrimoine-ferroviaire.fr, "
               "trainconsultant.com 등으로 다시 봤다. `en.wikipedia` 는 이때 캐시 전용이라 새 문서는 못 열었다. 결과: verified 66 → 71량, 중량 기준 미표기 4 → 0.\n")
    out.append("| id | 이름 | 확정 | 2차 확인 내용 (`_why_2`) | 출처 |")
    out.append("|---|---|---|---|---|")
    for lid, e in second:
        st = "✅" if e.get("_verified") else "⚠️"
        out.append(f"| `{lid}` | {names.get(lid, '')} | {st} | {_cell(e.get('_why_2'))} | {_src(e)} |")
    # 크램프턴은 2차에 새로 들어간 항목(_why 만 있음)
    cr = v.RECHECK.get("fr-crampton")
    if cr and not cr.get("_why_2"):
        out.append(f"| `fr-crampton` | {names.get('fr-crampton', '')} | {'✅' if cr.get('_verified') else '⚠️'} | (2차에 새로 넣음) {_cell(cr.get('_why'))} | {_src(cr)} |")

    # 미확정
    left = [l for l in data["locomotives"] if not l.get("verified")]
    out.append(f"\n## 아직 미확정 ({len(left)}량)\n")
    for l in left:
        first = (v.VERIFIED.get(l["id"]) or {}).get("_why") or ""
        again = v.RECHECK.get(l["id"]) or {}
        parts = [f"1차: {first}"] if first else []
        if again.get("_why"):
            parts.append(f"재대조: {again['_why']}")
        if again.get("_why_2"):
            parts.append(f"2차: {again['_why_2']}")
        out.append(f"- `{l['id']}` {l['nameKo']} — " + " / ".join(parts))

    out.append("\n## 접근이 막혔던 출처")
    out.append("- `zh.wikipedia.org`, `ru.wikipedia.org`, `commons.wikimedia.org` — 작업 환경에서 차단(우회하지 않음)")
    out.append("- `railography.co.uk` — https→http 리다이렉트 루프")
    out.append("- `steamlocomotive.com` locobase — 클라이언트 렌더링이라 본문이 비어 있음")
    out.append("- `nlr.ru`(국립러시아도서관) — 시간초과")
    out.append("- (v0.11) `en.wikipedia.org` 는 캐시 전용으로 제한되어 `SNCF_242A1`·`PKP_class_Ty51` 은 다시 보지 못함; `ja.wikipedia.org` 는 검색 결과에 나온 문서만 열림")
    out.append("- (v0.12) `heritage.go.kr`(국가유산포털)·`uiwang.go.kr`·`100year.roteco.or.kr` — robots 차단/시간초과로 미카 161호 등록 기록·『한국철도차량100년사』 본문은 못 봄")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
