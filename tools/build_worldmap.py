#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
world-atlas 의 TopoJSON(Natural Earth 110m) → assets/map/world_110m.json

앱과 프리뷰가 같은 육지 폴리곤을 쓴다.
 - 프리뷰(HTML): 이 데이터로 SVG 경로를 그려 실제 세계지도를 표시
 - Flutter 앱  : OSM 타일이 안 뜨는 상황(오프라인/타일 차단)의 밑그림 레이어

출력 형식 (좌표는 [경도, 위도] 평면 배열):
{
  "source": "...",
  "countries": [ {"name": "Korea", "rings": [[lon,lat, lon,lat, ...], ...]}, ... ]
}

원본: Natural Earth (public domain) / world-atlas 패키지 (ISC)
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "map")
OUT = os.path.join(OUT_DIR, "world_110m.json")

CANDIDATES = [
    os.path.join(ROOT, "..", "node_modules", "world-atlas", "countries-110m.json"),
    os.path.join(ROOT, "node_modules", "world-atlas", "countries-110m.json"),
    "/home/claude/node_modules/world-atlas/countries-110m.json",
]

PRECISION = 1        # 소수점 자리 (0.1° ≈ 11km — 세계지도 축척에는 충분)
MIN_SPAN_DEG = 0.6   # 이보다 작은 섬은 버린다 (점 하나로 뭉개짐)


def find_source():
    for p in CANDIDATES:
        if os.path.exists(p):
            return p
    sys.exit(
        "world-atlas 데이터를 찾지 못했습니다.\n"
        "  npm install world-atlas\n"
        "후 다시 실행하세요."
    )


def decode_arcs(topo):
    """양자화·델타 인코딩된 arc 를 실제 경위도 좌표열로 되돌린다."""
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    out = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out


def ring_points(indices, arcs):
    """TopoJSON 링(arc 인덱스 목록) → 좌표열. 음수 인덱스는 해당 arc의 역방향."""
    pts = []
    for i in indices:
        a = arcs[~i][::-1] if i < 0 else arcs[i]
        # arc 끝점과 다음 arc 시작점이 겹치므로 이어붙일 때 하나를 뺀다
        pts.extend(a[1:] if pts else a)
    return pts


def simplify(pts):
    """좌표를 반올림하고 연속 중복점을 제거한다."""
    out = []
    for lon, lat in pts:
        p = (round(lon, PRECISION), round(lat, PRECISION))
        if not out or out[-1] != p:
            out.append(p)
    return out


def _edge_crossing(a, b):
    """a→b 가 180°를 넘을 때, a 쪽 경계(±180)와 그 교차 위도를 돌려준다."""
    lon_a, lat_a = a
    lon_b, lat_b = b
    # b 를 a 와 이어지는 연속 좌표계로 옮긴다 (예: 179 → -179 는 실제로 179 → 181)
    lon_b_adj = lon_b + (360.0 if lon_b < lon_a else -360.0)
    edge = 180.0 if lon_b_adj > lon_a else -180.0
    span = lon_b_adj - lon_a
    t = 0.0 if span == 0 else (edge - lon_a) / span
    t = max(0.0, min(1.0, t))
    return edge, round(lat_a + (lat_b - lat_a) * t, PRECISION)


def split_antimeridian(pts):
    """180°를 넘어가는 링을 경계에서 끊는다.

    조각은 그대로 **닫힌 폴리곤**으로 그려지므로, 그냥 끊기만 하면
    마지막 점과 첫 점을 잇는 선이 지도를 대각선으로 가로지른다
    (러시아 링이 캄차카에서 연해주로 줄을 긋던 문제).
    그래서 끊는 자리마다 ±180 위의 교차점을 만들어 넣고, 링을 첫 교차 직후로
    회전시켜 **모든 조각의 양 끝이 경계 위에 오도록** 한다.
    그러면 닫는 선이 경도 180° 선을 따라 지도 가장자리에 붙는다.
    """
    ring = pts[:-1] if len(pts) > 1 and pts[0] == pts[-1] else list(pts)
    n = len(ring)
    if n < 3:
        return [ring]

    def wraps(i):
        return abs(ring[(i + 1) % n][0] - ring[i][0]) > 180

    cross = [i for i in range(n) if wraps(i)]
    if not cross:
        return [ring]

    first = cross[0]
    start = (first + 1) % n
    edge, lat = _edge_crossing(ring[first], ring[start])
    segs, cur = [], [(-edge, lat)]  # 반대쪽 경계에서 시작

    for k in range(n):
        i = (start + k) % n
        cur.append(ring[i])
        if wraps(i):
            e, la = _edge_crossing(ring[i], ring[(i + 1) % n])
            cur.append((e, la))
            segs.append(cur)
            cur = [(-e, la)]
    if len(cur) > 2:
        segs.append(cur)
    return segs


def big_enough(pts):
    lons = [p[0] for p in pts]
    lats = [p[1] for p in pts]
    return (max(lons) - min(lons)) >= MIN_SPAN_DEG or (max(lats) - min(lats)) >= MIN_SPAN_DEG


def main():
    src = find_source()
    topo = json.load(open(src, encoding="utf-8"))
    arcs = decode_arcs(topo)

    countries = []
    total_pts = 0
    for geom in topo["objects"]["countries"]["geometries"]:
        name = (geom.get("properties") or {}).get("name", "")
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["arcs"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["arcs"]
        else:
            continue

        rings = []
        for poly in polys:
            for ring in poly:  # 첫 링은 외곽, 나머지는 구멍
                pts = simplify(ring_points(ring, arcs))
                for seg in split_antimeridian(pts):
                    if len(seg) < 4 or not big_enough(seg):
                        continue
                    flat = []
                    for lon, lat in seg:
                        flat.append(lon)
                        flat.append(lat)
                    rings.append(flat)
                    total_pts += len(seg)
        if rings:
            countries.append({"name": name, "rings": rings})

    payload = {
        "source": "Natural Earth 110m (public domain) via world-atlas (ISC)",
        "precisionDeg": 10 ** -PRECISION,
        "countries": countries,
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    size = os.path.getsize(OUT) / 1024
    print(f"{OUT} 생성 완료")
    print(f"  국가 {len(countries)}개 / 링 {sum(len(c['rings']) for c in countries)}개 / "
          f"좌표 {total_pts}점 / {size:.0f} KB")


if __name__ == "__main__":
    main()
