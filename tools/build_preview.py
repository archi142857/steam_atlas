#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/preview_template.html + assets/data/*.json → preview/steam-atlas-preview.html

Flutter를 설치하지 않고도 화면 구조와 데이터를 그대로 확인할 수 있는
단일 HTML 파일을 만든다. 데이터를 갱신하면 이것도 다시 돌릴 것.
"""
import base64, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data")
FLAGS = os.path.join(ROOT, "assets", "flags")
WORLD = os.path.join(ROOT, "assets", "map", "world_110m.json")
TPL = os.path.join(ROOT, "tools", "preview_template.html")
OUTDIR = os.path.join(ROOT, "preview")
OUT = os.path.join(OUTDIR, "steam-atlas-preview.html")


def flag_data_urls(codes):
    """국기 SVG를 data URL로 인라인 — 프리뷰 HTML 한 장으로 오프라인 동작."""
    out = {}
    missing = []
    for code in codes:
        path = os.path.join(FLAGS, f"{code.lower()}.svg")
        if not os.path.exists(path):
            missing.append(code)
            continue
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        out[code] = f"data:image/svg+xml;base64,{b64}"
    if missing:
        raise SystemExit(f"국기 SVG 없음: {missing} — assets/flags/ 확인 (README 참조)")
    return out


def main():
    with open(os.path.join(DATA, "locomotives.json"), encoding="utf-8") as f:
        locos = json.load(f)
    with open(os.path.join(DATA, "countries.json"), encoding="utf-8") as f:
        countries = json.load(f)
    with open(TPL, encoding="utf-8") as f:
        html = f.read()

    flags = flag_data_urls([c["code"] for c in countries["countries"]])

    if not os.path.exists(WORLD):
        raise SystemExit("assets/map/world_110m.json 없음 — python3 tools/build_worldmap.py 먼저 실행")
    with open(WORLD, encoding="utf-8") as f:
        world = json.load(f)

    html = html.replace("__LOCO_DATA__", json.dumps(locos, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__COUNTRY_DATA__",
                        json.dumps(countries["countries"], ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__FLAG_DATA__", json.dumps(flags, separators=(",", ":")))
    html = html.replace("__WORLD_DATA__", json.dumps(world, ensure_ascii=False, separators=(",", ":")))

    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(OUT) / 1024
    pts = sum(len(r) // 2 for c in world["countries"] for r in c["rings"])
    print(f"{OUT} 생성 완료 ({size:.0f} KB, 기관차 {len(locos['locomotives'])}량, "
          f"국기 {len(flags)}개, 지도 {pts}점 인라인)")


if __name__ == "__main__":
    main()
