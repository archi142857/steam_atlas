# 제3자 자료 고지 (Third-party notices)

이 저장소와 앱·프리뷰에 번들된 남의 자료와 그 라이선스. 소프트웨어 자체는 `LICENSE`(MIT), 기관차 데이터는 `LICENSE-DATA`(CC BY-SA 4.0).
Dart 패키지(flutter_map, provider, flutter_svg, shared_preferences, url_launcher, android_intent_plus, latlong2 등)의 라이선스는
Flutter 가 빌드 때 모아 두며, 앱 설정 화면의 '오픈소스 라이선스'(`showLicensePage`)에서 볼 수 있다.

## 국기 SVG — flag-icons (MIT)

`assets/flags/*.svg` 16개. https://github.com/lipis/flag-icons

```
The MIT License (MIT)

Copyright (c) 2013 Panayiotis Lipiridis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## 육지 폴리곤 — Natural Earth (퍼블릭 도메인) / world-atlas (ISC)

`assets/map/world_110m.json` 은 Natural Earth 1:110m 문화 벡터(국가 경계)를 `world-atlas` npm 패키지의 TopoJSON 에서
`tools/build_worldmap.py` 로 풀어 만든 것이다.

- Natural Earth — 퍼블릭 도메인. "Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com."
- world-atlas — https://github.com/topojson/world-atlas

```
Copyright 2013-2019 Michael Bostock

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```

## 온라인 지도 타일 (선택 기능)

설정에서 '온라인 상세 지도'를 켰을 때만 `tile.openstreetmap.org` 타일을 받는다. 지도 데이터 © OpenStreetMap 기여자, ODbL.
공개 OSM 타일은 앱 프로덕션용이 아니므로 출시 전 교체하거나 기능을 뺄 것(`RELEASE.md`).

## 데이터 출처

기관차 제원·이력의 사실은 위키백과(CC BY-SA 4.0)·각국 철도 박물관·공식 문화유산 기록·서적을 참고했다.
항목별 웹 출처는 `assets/data/locomotives.json` 의 `sources`, 대조 근거는 `tools/verified.py`, 서적·논문은 `tools/references.py`.
