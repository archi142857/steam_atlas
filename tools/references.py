#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Atlas — 참고문헌 (서적·논문·공식 간행물)

웹 페이지(sources)와 별개로, **종이 문헌과 학술·공식 자료**를 따로 둔다. 현지어 자료를 우선한다:
한국은 철도청·국가유산청, 일본은 国鉄·NDL 소장 문헌, 독일은 EK/transpress 형식별 단행본,
프랑스는 Chapelon 원전과 La Vie du Rail, 폴란드는 WKŁ, 러시아는 Раков, 남아공은 Holland/Wardale…

여기 적힌 항목은 전부 **도서관 목록·출판사·학술DB 에서 서지사항을 확인한 것**만이다(`via` 에 확인 경로).
확인하지 못한 값(연도 등)은 비워 두고 note 에 적는다 — 그럴듯하게 채우지 않는다.

    항목 필드
      kind      book | article | thesis | official | catalog
      title     원어 제목
      author    저자/편자 (원어)
      publisher 출판사 (원어)
      year      발행연도 (int) — 확인 못 했으면 None
      lang      ko | ja | en | de | fr | pl | ru | zh | es | it
      isbn      선택
      url       선택 — 도서관 목록·출판사·학술DB·공식 페이지 (구매 사이트는 넣지 않는다)
      note      무엇을 다루는지 / 왜 이 기관차·국가에 붙였는지 (한국어)
      via       서지 확인 경로 (NDL, 국회도서관, SearchWorks, 出版社, de.wikipedia 문헌목록 …)

COUNTRY_REFS : 국가 코드 → 그 나라 증기기관차 전반을 다루는 표준 문헌. "*" 는 여러 나라에 걸친 종합서.
LOCO_REFS    : 기관차 id → 그 형식·개체를 직접 다루는 문헌.
"""

NDL = "https://ndlsearch.ndl.go.jp/books/"


def ref(kind, title, author, publisher, year, lang, note, via, isbn=None, url=None):
    return {"kind": kind, "title": title, "author": author, "publisher": publisher,
            "year": year, "lang": lang, "isbn": isbn, "url": url, "note": note, "via": via}


# ─────────────────────────────────────────────────────────────
# 여러 나라에 걸친 종합서
# ─────────────────────────────────────────────────────────────
GENERAL = [
    ref("book", "La locomotive à vapeur", "André Chapelon", "J.-B. Baillière et fils, Paris", 1938, "fr",
        "증기기관차 설계의 고전. 1952년 제2판(648쪽). 영역판 George Carpenter 역, Camden Miniature Steam Services 2000 "
        "(ISBN 9780953652303, 2024 재쇄). 242 A 1·231 E 등 샤플롱 설계의 원리가 여기 있다.",
        "AbeBooks 판본 목록(1938/1952/영역판 2000)"),
    ref("book", "Chapelon: Genius of French Steam", "H. C. B. Rogers", "Ian Allan, London", 1972, "en",
        "샤플롱 평전이자 프랑스 증기 설계사. SBN 7110 0281 9. 불역판 «André Chapelon, 1892-1978 : le génie français de la vapeur» "
        "(CNRS Éditions, ISBN 978-2-222-04748-3).",
        "advanced-steam.org 서지 / fr.wikipedia 문헌목록", isbn="0711002819"),
    ref("book", "Garratt Locomotives of the World", "A. E. Durrant", "David & Charles, Newton Abbot", 1981, "en",
        "가라트식 관절기관차의 표준 통사. 남아공 GL형 등 전 세계 가라트를 다룬다.",
        "AbeBooks/Amazon 서지(ISBN 0715376411)", isbn="0715376411"),
    ref("book", "The Red Devil and Other Tales from the Age of Steam", "David Wardale", "D. Wardale (자비출판), Inverness", 1998, "en",
        "남아공 26형 '레드 데블' 개조를 설계자가 직접 기록한 현대증기(Modern Steam)의 1차 자료. 2013년 Camden 재판(ISBN 9781909358010).",
        "Biblio/AbeBooks 서지(ISBN 9780952999805)", isbn="9780952999805"),
    ref("book", "Das Handbuch der Lokomotiven", "Brian Hollingsworth, Arthur Cook", "Bechtermünz/Weltbild, Augsburg", 1996, "de",
        "세계 여객용 증기기관차 백과(Salamander 'Illustrated Encyclopedia of the World's Steam Passenger Locomotives' 독역판). "
        "국가별 대표 형식의 제원 비교에 유용.",
        "de.wikipedia 'LEG – Adler und Pfeil' 문헌목록", isbn="3-86047-138-4"),
]

# ─────────────────────────────────────────────────────────────
# 국가별 표준 문헌
# ─────────────────────────────────────────────────────────────
COUNTRY_REFS = {
    "KR": [
        ref("official", "한국철도100년사", "철도청 편", "철도청", 1999, "ko",
            "1899~1999 한국철도 공식 통사. 기관차 도입·형식 변천의 기본 출전.",
            "국립국회도서관(NDL) 서지 R100000002-Ia1000015465 / 교보문고"),
        ref("book", "한국 철도의 역사와 발전 1", "이용상·임병국·정병현·轟博志·윤동희·배은선·최석중·김종만", "북갤러리", 2011, "ko",
            "역사·영향·문화·인물을 다룬 종합 연구서(전 3권 중 1권, 445쪽).",
            "알라딘 서지", isbn="9788964950234"),
        ref("official", "朝鮮鉄道史 第1巻", "朝鮮総督府鉄道局", "朝鮮総督府鉄道局", 1929, "ja",
            "경인선 개통부터 총독부 철도국까지의 공식 사서 — 모가·터우 등 초기 도입 기관차의 1차 사료.",
            "NDL 서지 R100000002-I000000763694 (디지털 컬렉션 공개)", url=NDL + "R100000002-I000000763694"),
        ref("book", "朝鮮交通史 (本編·資料編)", "鮮交会 編", "鮮交会, 東京", 1986, "ja",
            "구 조선총독부 철도국 직원회(鮮交会)가 정리한 조선 철도 통사·자료집. 미카·파시 등 형식별 배치·제원 자료 포함.",
            "NDL 서지 R100000002-I000001816992 (청구 DK55-104)", url=NDL + "R100000002-I000001816992"),
        ref("official", "한국철도차량100년사", "철도차량기술검정단 한국철도차량 100년사 편찬위원회 편", "철도차량기술검정단", 1999, "ko",
            "1899~1999 한국 철도차량 공식 백년사(1582쪽). 1.2장 '증기기관차'가 모가·터우·미카·파시·혀기 등 형식별 이력을 다룬다 "
            "(장별 PDF 파일명으로 장 구성 확인, 본문은 미열람).",
            "NDL 서지 R100000002-Ia1000033298 (청구 DK55-K5)", url=NDL + "R100000002-Ia1000033298"),
        ref("thesis", "근대문화유산 경의선장단역증기기관차의 보존에 관한 연구 : 문화유산적 가치와 보존방침을 중심으로",
            "하은하", "경기대학교 전통예술대학원 (석사학위논문)", 2008, "ko",
            "등록문화재 제78호 장단역 마터2형 기관차의 보존 원칙 연구 — 한국 보존 증기기관차의 문화유산적 접근.",
            "국회도서관 KDMT1200848550", url="https://dl.nanet.go.kr/SearchDetailView.do?cn=KDMT1200848550"),
    ],
    "JP": [
        ref("book", "国鉄蒸気機関車史", "髙木宏之", "ネコ・パブリッシング", 2015, "ja",
            "국철 제식 증기기관차의 설계·표준화 통사. 도면·1차 자료 기반.",
            "출판사(neko.co.jp) 서지", isbn="978-4-7770-5379-7"),
        ref("book", "機関車の系譜図 1〜4", "臼井茂信", "交友社", 1972, "ja",
            "일본 증기기관차 형식 계보의 고전(전 4권, 1972~1978).",
            "NDL 서지(1권 R100000039-I12655624)", url=NDL + "R100000039-I12655624"),
        ref("book", "日本国有鉄道蒸気機関車設計図面集", "国鉄SL図面編集委員会 編", "原書房", 1976, "ja",
            "국철 증기기관차 설계도면집 — 제원의 1차 자료.",
            "NDL 서지 R100000002-I000001144266 / CiNii BN06275528", url=NDL + "R100000002-I000001144266"),
        ref("official", "日本国有鉄道百年史 (全19巻)", "日本国有鉄道", "日本国有鉄道", 1969, "ja",
            "국철 공식 백년사(1969~1974 간행, 1997 成山堂 복각).",
            "NDL 서지 R100000002-I000001167808", url=NDL + "R100000002-I000001167808"),
        ref("book", "国鉄制式蒸気機関車のプロフィール", "『旅と鉄道』編集部", "イカロス出版", 2024, "ja",
            "9600·8620·C11·D51·C57·C58·C62 등 제식기 형식별 제조사·개조·보존기 해설(144쪽).",
            "출판사(books.ikaros.jp) 서지", isbn="9784802214223"),
    ],
    "GB": [
        ref("book", "Locomotives of the L.N.E.R., Part 2A: Tender Engines — Classes A1 to A10", "RCTS (E. V. Fry 편)",
            "Railway Correspondence and Travel Society", 1978, "en",
            "LNER 퍼시픽(A1·A3·A4 포함)의 표준 형식사. 개체별 이력까지 수록.",
            "steamindex.com RCTS 서지"),
        ref("book", "The Locomotives of the Great Western Railway, Part 8: Modern Passenger Classes", "RCTS",
            "Railway Correspondence and Travel Society", 1953, "en",
            "GWR 4-6-0·4-4-2·4-6-2 — 킹급 포함(2판 1960).",
            "steamindex.com RCTS 서지"),
        ref("book", "The British Steam Railway Locomotive 1925–1965", "O. S. Nock", "Ian Allan, London", 1966, "en",
            "Ahrons 의 1825~1925 통사를 잇는 표준 통사(1983 재판 ISBN 0711001251).",
            "Internet Archive 서지(1983판)", isbn="0711001251"),
        ref("book", "The British Steam Railway Locomotive 1825–1925", "E. L. Ahrons", "Locomotive Publishing Co., London", 1927, "en",
            "영국 증기기관차 첫 100년의 고전 통사(재판 ISBN 9781851701032).",
            "AbeBooks/Amazon 서지"),
    ],
    "US": [
        ref("book", "American Steam Locomotives: Design and Development, 1880–1960", "William L. Withuhn", "Indiana University Press, Bloomington", 2019, "en",
            "스미스소니언 큐레이터의 미국 증기기관차 설계사 — 대학 출판부 학술서.",
            "en.wikipedia 'N&W Class J (1941)' 문헌목록", isbn="978-0-253-03933-0"),
        ref("book", "Guide to North American Steam Locomotives", "George H. Drury", "Kalmbach Books, Waukesha", 1993, "en",
            "북미 철도별 증기기관차 편람(454쪽). 개정 2판 2015(ISBN 9781627002592). 캐나다 포함.",
            "Internet Archive 서지", isbn="9780890242063"),
        ref("book", "Motive Power of the Union Pacific", "William W. Kratville, Harold E. Ranks", "Barnhart Press, Omaha", 1960, "en",
            "UP 동력차 전반(300쪽) — 빅보이·FEF 계열의 배경.",
            "utahrails.net UP 증기 문헌목록"),
    ],
    "DE": [
        ref("book", "Dampflokarchiv, Band 1", "Manfred Weisbrod, Hans Müller, Wolfgang Petznick", "transpress VEB Verlag für Verkehrswesen, Berlin", 1976, "de",
            "독일 증기기관차 형식 아카이브(전 4권)의 1권 — 급행·여객기.",
            "de.wikipedia 'DB-Baureihe 10' 문헌목록"),
        ref("book", "Das große Typenbuch deutscher Lokomotiven", "Manfred Weisbrod, Dieter Bäzold, Horst J. Obermayer", "transpress", None, "de",
            "독일 기관차 형식 편람. 발행연도 미확인.",
            "de.wikipedia 'DR 18 201' 문헌목록", isbn="3-344-70751-5"),
    ],
    "FR": [
        ref("book", "L'Âge d'or de la traction vapeur en France (1900/1950)", "Clive Lamming", "Éditions Atlas", 2005, "fr",
            "프랑스 증기 황금기 개설 — 231 E 등 노르·PO·PLM 형식 배경.",
            "fr.wikipedia '231 Nord 3.1111…' 문헌목록", isbn="2-8302-2144-3"),
        ref("book", "La Machine locomotive en France : des origines au milieu du XIXe siècle", "Jacques Payen (avec Bernard Escudié, Jean-Marc Combe)",
            "Presses universitaires de Lyon / Éditions du CNRS, Lyon–Paris", 1988, "fr",
            "프랑스 초기 증기기관차(19세기 중반까지)의 학술 통사 — 크램프턴 시대의 배경.",
            "BnF 종합목록(CCFr) 서지 / 출판사 페이지", isbn="9782729703394"),
    ],
    "PL": [
        ref("book", "Parowozy normalnotorowe produkcji polskiej", "Bogdan Pokropiński", "Wydawnictwa Komunikacji i Łączności (WKŁ), Warszawa", 1987, "pl",
            "폴란드 국산 표준궤 증기기관차 총람(Ol49·Pm36·Ty51 포함). 신판 ISBN 978-83-206-1617-0(292쪽).",
            "WKŁ 출판사 페이지 / parowozy.net 문헌목록", isbn="978-83-206-1617-0",
            url="https://www.wkl.com.pl/parowozy-normalnotorowe-produkcji-polskiej,1,1,437"),
        ref("book", "Atlas parowozów", "Paweł Terczyński", "Poznański Klub Modelarzy Kolejowych, Poznań", 2003, "pl",
            "PKP 증기기관차 형식 도감.", "parowozy.net 문헌목록"),
        ref("book", "Parowozy kolei polskich", "Jan Piwowoński", "WKŁ, Warszawa", 1978, "pl",
            "폴란드 철도 증기기관차 통사.", "parowozy.net 문헌목록"),
    ],
    "RU": [
        ref("book", "Локомотивы отечественных железных дорог (1845–1955 гг.)", "В. А. Раков", "Транспорт, Москва", 1995, "ru",
            "러시아·소련 기관차의 표준 편람(2-е изд., 564쪽). Э·П36·Л·АА20 모두 수록.",
            "CentrMag 서지(ISBN 5-277-00821-7)", isbn="5-277-00821-7"),
        ref("book", "Soviet Locomotive Types: The Union Legacy", "Anthony J. Heywood, Ian D. C. Button", "Luddenden Press / Frank Stenvall", 1995, "en",
            "1992년 1월 기준 1520mm 궤간 전 형식 목록·보존 현황(영문).",
            "AbeBooks 서지", isbn="9172661321"),
        ref("book", "Soviet Locomotive Technology During Industrialization, 1928–1952", "J. N. Westwood", "Macmillan, London", 1982, "en",
            "소련 공업화기 기관차 기술사 — АА20 실험과 표준화 정책의 배경(영문 학술서).",
            "Stanford SearchWorks 서지", isbn="0333275160"),
    ],
    "CN": [
        ref("book", "中国蒸汽机车世纪集影 (1876–2001)", "严介生 编", "中国铁道出版社, 北京", 2001, "zh",
            "중국 증기기관차 125년 화보·형식집(288쪽). QJ·JS·SY·JF·KF 포함.",
            "豆瓣 서지", isbn="9787113041472", url="https://book.douban.com/subject/1434767/"),
    ],
    "IN": [
        ref("book", "Indian Locomotives, Part 1: Broad Gauge 1851–1940", "Hugh Hughes", "Continental Railway Circle", 1990, "en",
            "인도 광궤 증기기관차 형식사 1부 — 페어리 퀸 등 초기 도입기.",
            "AbeBooks 서지", isbn="0950346985"),
        ref("book", "Indian Locomotives, Part 3: Narrow Gauge 1863–1940", "Hugh Hughes", "Continental Railway Circle", 1994, "en",
            "협궤 — 다르질링 B형.", "AbeBooks 서지", isbn="0952165503"),
        ref("book", "Indian Locomotives, Part 4: 1941–1990", "Hugh Hughes", "Continental Railway Circle", 1996, "en",
            "전후 표준형 WP·WG.", "AbeBooks 서지", isbn="0952165511"),
    ],
    "ZA": [
        ref("book", "Steam Locomotives of the South African Railways, Vol. 1: 1859–1910", "D. F. Holland", "David & Charles, Newton Abbot", 1971, "en",
            "남아공 증기기관차 표준 형식사 1권.", "Amazon 서지", isbn="9780715353820"),
        ref("book", "Steam Locomotives of the South African Railways, Vol. 2: 1910–1955", "D. F. Holland", "David & Charles, Newton Abbot", 1972, "en",
            "2권 — 15F·GL·25NC 등 20세기 형식.", "en.wikipedia 'South African Class 25' 문헌목록", isbn="978-0-7153-5427-8"),
        ref("book", "Locomotives of the South African Railways: A Concise Guide", "Leith Paxton, David Bourne", "Struik, Cape Town", 1985, "en",
            "SAR 전 형식 요약 편람.", "en.wikipedia 문헌목록 / AbeBooks", isbn="0869772112"),
        ref("book", "Twilight of South African Steam", "A. E. Durrant", "David & Charles, Newton Abbot", 1989, "en",
            "남아공 증기 말기(1980년대)의 기록.", "en.wikipedia 문헌목록", isbn="0715386387"),
    ],
    "AU": [
        ref("book", "Locomotives of Australia 1850s–2010", "Leon Oberg", "Rosenberg Publishing, Kenthurst NSW", 2010, "en",
            "호주 전 주(州) 기관차 편람 5판.", "en.wikipedia 'NSW C38 class' 문헌목록", isbn="9781921719011"),
    ],
    "CA": [
        ref("book", "Canadian Pacific Steam Locomotives", "Omer Lavallée (Archie Williamson 협력)", "Railfare, Toronto", 1985, "en",
            "CPR 증기기관차 전 형식사 — 로열 허드슨(H1c–e) 포함.", "eBay 상품 서지(ISBN 0919130348)", isbn="0919130348"),
        ref("book", "Canadian National Steam Power", "Anthony Clegg, Ray Corley", "Railfare, Montreal", 1969, "en",
            "CN 증기기관차 형식사 — U-1-f 포함.", "Yesterday's Muse 서지"),
    ],
    "CH": [
        ref("book", "Der Dampfbetrieb der schweizerischen Eisenbahnen 1847–1966", "Alfred Moser (4. Aufl. bearb. Paul Winter u. a.)", "Birkhäuser, Basel", 1967, "de",
            "스위스 전 철도의 증기기관차를 망라한 결정판(4판). E 3/3·HG 3/4 수록.",
            "ZVAB/AbeBooks 서지(1967, 4. Aufl.)"),
    ],
    "AR": [
        ref("book", "La Trochita. Un viaje en el tiempo y la distancia en el Viejo Expreso Patagónico", "Sergio Sepiurka, Jorge Miglioli", "(아르헨티나)", 2001, "es",
            "에스켈선 750mm 협궤의 역사·증언·전망(2판 2022, 개통 100주년).",
            "Red43 기사(2022 2판 발표) / latrochita.com"),
        ref("book", "The Old Patagonian Express", "Paul Theroux", "Houghton Mifflin, Boston", 1979, "en",
            "이 노선을 세계에 알린 여행기.", "en.wikipedia 'La Trochita'"),
    ],
    "IT": [
        ref("book", "Locomotive a vapore FS", "Giovanni Cornolò", "Ermanno Albertelli, Parma", 1998, "it",
            "FS 증기기관차 전 형식(2판, 608쪽; 2014 분책 재간).", "Duegi Editrice 서지 / en.wikipedia 문헌목록"),
        ref("book", "Italian State Railways Steam Locomotives", "P. M. Kalla-Bishop", "Tourret Publishing, Abingdon", 1986, "en",
            "FS 증기기관차 영문 형식사.", "en.wikipedia 'FS Class 835' 문헌목록", isbn="0-905878-03-5"),
    ],
}

# ─────────────────────────────────────────────────────────────
# 기관차별 문헌
# ─────────────────────────────────────────────────────────────
_KR_PASHI = ref("official", "국가등록문화유산 파시형 증기기관차 23호", "국가유산청(구 문화재청)", "국가유산포털", 2008, "ko",
                "2008-10-17 등록. 1942년 제작, 동륜 1,850mm, 철도박물관(의왕) 소장 — 보존 파시5형의 공식 기록.",
                "국가유산포털", url="https://heritage.go.kr/heri/cul/culSelectDetail.do?ccbaCpno=4413104170000")
_KR_MIKA129 = ref("official", "국가등록문화유산 미카형 증기기관차 129호", "국가유산청(구 문화재청)", "국가유산포털", 2008, "ko",
                  "등록 기록(2025년 등록 해제 이전). 국립대전현충원 소장.",
                  "국가유산포털", url="https://heritage.go.kr/heri/cul/culSelectDetail.do?ccbaCpno=4412504150000")
_JP_PROFILE = COUNTRY_REFS["JP"][4]
_RCTS_LNER = COUNTRY_REFS["GB"][0]
_RCTS_GWR = COUNTRY_REFS["GB"][1]
_HOLLAND2 = COUNTRY_REFS["ZA"][1]
_RAKOV = COUNTRY_REFS["RU"][0]
_POKROP = COUNTRY_REFS["PL"][0]
_HUGHES1, _HUGHES3, _HUGHES4 = COUNTRY_REFS["IN"]
_CHAPELON, _ROGERS, _DURRANT_G, _WARDALE = GENERAL[0], GENERAL[1], GENERAL[2], GENERAL[3]

# 뉴커먼 학회지(Transactions of the Newcomen Society) 논문 — 서지는 Crossref DOI 레코드로 확인 (v0.12).
def _tns(title, author, vol, pages, year, doi, note):
    return ref("article", title, author, f"Transactions of the Newcomen Society, vol. {vol}, pp. {pages}", year, "en",
               note, f"Crossref DOI {doi}", url=f"https://doi.org/{doi}")

_TNS_CARPENTER = _tns("André Chapelon, Locomotive Engineer: A Survey of his Work", "G. W. Carpenter", 58, "1–26", 1986,
                      "10.1179/tns.1986.001", "샤플롱의 설계 전반을 정리한 학회 심포지엄 논문.")
_TNS_COMPOUND3 = _tns("The Compound Locomotive, Part III", "J. T. van Riemsdijk", 45, "45–54", 1972,
                      "10.1179/tns.1972.003", "복식 기관차사 3부 — 샤플롱 시대의 복식 설계 (1부 1876–1901, 2부 1901–1921 는 별도 논문).")
_TNS_CRAMPTON1 = _tns("The Crampton Locomotive in England: Part I — The Outside Cylinder Rear-Driver Pattern", "P. C. Dewhurst",
                      30, "99–113", 1955, "10.1179/tns.1955.008", "크램프턴식(후방 단동륜) 기관차 연구 1부.")
_TNS_CRAMPTON2 = _tns("The Crampton Locomotive: Part II", "P. C. Dewhurst", 30, "115–139", 1955,
                      "10.1179/tns.1955.009", "크램프턴식 기관차 연구 2부.")
_TNS_RAINHILL = _tns("The Rainhill Locomotive Trials of 1829", "C. F. Dendy Marshall", 9, "78–93", 1928,
                     "10.1179/tns.1928.007", "레인힐 경주(1829)의 사료 정리 — 로켓호 우승의 1차 기록 검토.")
_TNS_TREVITHICK = _tns("Trevithick's First Rail Locomotive", "W. W. Mason", 12, "85–103", 1931,
                       "10.1179/tns.1931.007", "1804년 페니다렌 기관차의 기록 검토.")
_TNS_STEPHENSON = _tns("George Stephenson: A Commemorative Symposium for the 200th Anniversary of his Birth", "Michael R. Bailey",
                       52, "171–207", 1980, "10.1179/tns.1980.011", "조지 스티븐슨 200주년 심포지엄 — 로코모션 1호 시기의 스티븐슨 기관차.")
_KR_100 = COUNTRY_REFS["KR"][5]

LOCO_REFS = {
    # 한국
    "kr-pashi5": [_KR_PASHI, _KR_100],
    "kr-mika3-129": [_KR_MIKA129, _KR_100],
    "kr-mika3-161": [_KR_100], "kr-moga": [_KR_100], "kr-teou": [_KR_100], "kr-hyeogi": [_KR_100],
    "jp-class150": [
        ref("book", "日本最初の機関車群", "金田茂裕", "機関車史研究会", 1990, "ja",
            "1872년 개업기 수입 기관차 10량(1호 기관차 포함)의 형식 연구.",
            "NDL 서지 R100000002-I000002080612 (청구 NC34-E20)", url=NDL + "R100000002-I000002080612"),
        ref("official", "重要文化財 一号機関車〈／一八七一年、英国製〉", "文化庁", "文化遺産オンライン", 1997, "ja",
            "1997-06-30 중요문화재(역사자료) 지정. 소유 JR東日本, 소재 鉄道博物館(大宮). 철도차량 최초의 중요문화재.",
            "文化遺産オンライン 지정 기록", url="https://online.bunka.go.jp/heritages/detail/187782"),
    ],
    # 일본 — 제식기는 프로필집이 형식별로 다룬다
    "jp-8620": [_JP_PROFILE], "jp-9600": [_JP_PROFILE], "jp-c11": [_JP_PROFILE],
    "jp-d51": [_JP_PROFILE], "jp-c57": [_JP_PROFILE], "jp-c58": [_JP_PROFILE], "jp-c62": [_JP_PROFILE],
    # 영국
    "gb-trevithick-pendarren": [
        ref("book", "Richard Trevithick: Giant of Steam", "Anthony Burton", "Aurum Press, London", 2000, "en",
            "트레비식 평전 — 1804년 페니다렌 주행의 사료 검토.", "AbeBooks/Amazon 서지", isbn="1854107283"),
        _TNS_TREVITHICK,
    ],
    "gb-locomotion-1": [
        ref("book", "George and Robert Stephenson: The Railway Revolution", "L. T. C. Rolt", "Amberley, Stroud (초판 Longmans, London 1960)", 2009, "en",
            "스티븐슨 부자 평전의 고전 — 스톡턴-달링턴 철도와 로코모션 1호. 2009 Amberley 재간 서지.",
            "AbeBooks/Amazon 서지", isbn="9781848681644"),
        _TNS_STEPHENSON,
    ],
    "gb-lms-black5": [
        ref("book", "The Stanier 4-6-0s of the LMS: The Jubilees, Class 5s and the BR Standard Class 5s", "J. W. P. Rowledge, Brian Reed",
            "David & Charles, Newton Abbot (Locomotive Studies)", 1977, "en",
            "스태니어 4-6-0(블랙 파이브 포함) 형식사.", "AbeBooks 서지", isbn="0715373854"),
    ],
    "gb-br-britannia": [
        ref("book", "A Detailed History of British Railways Standard Steam Locomotives, Volume One: Background to Standardisation and the Pacific Classes",
            "P. T. Gilbert (R. K. Taylor 편)", "Railway Correspondence and Travel Society", 1994, "en",
            "BR 표준형 형식사 1권 — 브리타니아급(7급 퍼시픽) 수록.", "AbeBooks 서지", isbn="0901115819"),
    ],
    "gb-rocket": [_TNS_RAINHILL,
        ref("book", "The Engineering and History of Rocket: A Survey Report", "Michael R. Bailey, John P. Glithero",
            "National Railway Museum, York", 2000, "en",
            "1999년 NRM 실물 조사 보고서(186쪽) — 로켓호 현존 차체의 공학적·역사적 검증.",
            "Google Books 서지", isbn="1900747189"),
    ],
    "gb-lner-a4-mallard": [
        _RCTS_LNER,
        ref("book", "Mallard: How the Blue Streak Broke the World Steam Speed Record", "Don Hale", "Aurum Press, London", 2005, "en",
            "1938년 기록 주행의 전말(x+181쪽).", "Stanford SearchWorks 서지", isbn="9781854109392"),
    ],
    "gb-lner-a3-flyingscotsman": [_RCTS_LNER,
        ref("book", "The Book of the A3 Pacifics", "(Irwell Press)", "Irwell Press", None, "en",
            "A3 개체별 이력. 발행연도 미확인.", "britishrailwaybooks.co.uk 목록", isbn="9781903266397")],
    "gb-a1-tornado": [_RCTS_LNER],
    "gb-gwr-king": [_RCTS_GWR,
        ref("book", "Peto's Register of GWR Locomotives, Volume 1: King 4-6-0s", "(Irwell Press)", "Irwell Press", None, "en",
            "킹급 개체별 등록부. 발행연도 미확인.", "britishrailwaybooks.co.uk 목록", isbn="9781871608502")],
    "gb-lms-duchess": [
        ref("book", "The Book of the Coronation Pacifics", "Ian Sixsmith", "Irwell Press", 1998, "en",
            "프린세스 코로네이션급 개체별 이력.", "AbeBooks 서지", isbn="1871608945"),
    ],
    # 미국
    "us-up-bigboy-4014": [
        ref("book", "Big Boy", "William W. Kratville", "Kratville Publications, Omaha", 1972, "en",
            "빅보이 형식의 표준 단행본.", "utahrails.net UP 증기 문헌목록"),
        COUNTRY_REFS["US"][2],
    ],
    "us-up-844": [
        ref("book", "Union Pacific 8444", "R. H. Kindig", "Obenchain Publications", 1978, "en",
            "844(당시 8444)호 소책자(64쪽).", "utahrails.net UP 증기 문헌목록"),
        COUNTRY_REFS["US"][2],
    ],
    "us-co-allegheny": [
        ref("book", "The Allegheny: Lima's Finest", "Eugene L. Huddleston, Thomas W. Dixon Jr.", "Hundman Publishing", 1984, "en",
            "H-8 앨러게이니의 표준 단행본(245쪽) — 출력·중량 논쟁의 출전.", "AbeBooks 서지", isbn="0945434030"),
    ],
    "us-nw-611": [
        ref("book", "Norfolk and Western Class J: The Finest Steam Passenger Locomotive", "Kenneth L. Miller",
            "Roanoke Chapter, National Railway Historical Society", 2000, "en", "J형 611 의 표준 단행본.",
            "en.wikipedia 문헌목록", isbn="0-615-11664-7"),
        ref("book", "N&W: Giant of Steam (Revised Edition)", "Lewis Jeffries", "Norfolk and Western Historical Society", 2005, "en",
            "N&W 증기 전반(J·A·Y6).", "en.wikipedia 문헌목록", isbn="0-9704794-5-X"),
    ],
    "us-nw-y6b": [
        ref("book", "N&W: Giant of Steam (Revised Edition)", "Lewis Jeffries", "Norfolk and Western Historical Society", 2005, "en",
            "N&W 증기 전반(J·A·Y6).", "en.wikipedia 문헌목록", isbn="0-9704794-5-X"),
        ref("book", "Norfolk & Western Steam (The Last 25 Years)", "Ron Rosenburg, Eric H. Archer", "Quadrant Press", 1973, "en",
            "", "en.wikipedia 문헌목록", isbn="0-915276-00-3"),
    ],
    "us-nyc-hudson": [
        ref("book", "Thoroughbreds: New York Central's 4-6-4 Hudson", "Alvin F. Staufer, Edward L. May", "A. F. Staufer, Medina OH", 1974, "en",
            "허드슨형 단행본 — J-1·J-3a·드레이퍼스 유선형 10량.", "en.wikipedia 'New York Central Hudson' 문헌목록", isbn="978-0944513033"),
        ref("book", "Steam Power of the New York Central System, Volume 1: Modern Power 1915–1955", "Alvin F. Staufer", "Standard Print & Publishing", 1961, "en",
            "", "en.wikipedia 문헌목록"),
    ],
    "us-prr-k4": [
        ref("book", "Pennsy Power: Steam and Electric Locomotives of the Pennsylvania Railroad, 1900–1957", "Alvin F. Staufer", "Standard Print & Publishing", 1962, "en",
            "PRR 동력차의 고전(LCCN 62-20878).", "en.wikipedia 'PRR class K4' 문헌목록"),
        ref("book", "The Many Faces of the Pennsy K-4", "Bert Pennypacker, Alvin F. Staufer", "N.J. International", 1984, "en",
            "", "en.wikipedia 문헌목록", isbn="0-934088-13-6"),
    ],
    "us-sp-4449": [
        ref("book", "Southern Pacific Daylight Locomotives", "Robert J. Church", "Signature Press", 2004, "en",
            "GS 계열 데이라이트 기관차.", "en.wikipedia 'SP GS-4 class' 문헌목록", isbn="1-930013-11-6"),
        ref("book", "Southern Pacific Company Steam Locomotive Compendium", "Timothy S. Diebert, Joseph A. Strapac", "Shade Tree Books", 1987, "en",
            "SP 증기 전 형식 편람.", "en.wikipedia 문헌목록", isbn="0-930742-12-5"),
        ref("book", "4449: The Queen of Steam", "Henry Brueckman, Jeffrey Moreau", "Carbarn Press", 1984, "en",
            "", "en.wikipedia 'Southern Pacific 4449' 문헌목록", isbn="0-934406-01-4"),
    ],
    "us-milw-classa": [
        ref("book", "The Hiawatha Story", "Jim Scribbins", "Kalmbach Publishing, Milwaukee", 1970, "en",
            "하이어워사 열차와 A형 아틀란틱(1934~1970). 2007 University of Minnesota Press 재판.",
            "en.wikipedia 'The Hiawatha Story'"),
    ],
    # 독일
    "de-adler": [
        ref("book", "Der Adler – Deutschlands berühmteste Lokomotive (Objektgeschichten aus dem DB Museum, Band 2)",
            "DB Museum Nürnberg, Jürgen Franzke (Hrsg.)", "Tümmel, Nürnberg", 2011, "de",
            "소장 박물관의 공식 객체사.", "de.wikipedia 문헌목록", isbn="978-3-940594-23-5"),
        ref("book", "Stephenson's Locomotive auf der Ludwigs-Eisenbahn von Nuernberg nach Fuerth", "Georg Rebenstein", "Nürnberg", 1836, "de",
            "동시대 1차 사료.", "de.wikipedia 문헌목록"),
        ref("book", "Deutschlands erste Eisenbahn mit Dampfkraft. Die kgl. priv. Ludwigseisenbahn zwischen Nürnberg und Fürth",
            "Wolfgang Mück", "Fürth (2. Aufl.)", 1985, "de", "루트비히 철도사.", "de.wikipedia 문헌목록"),
    ],
    "de-drg-01": [
        ref("book", "Die Baureihe 01", "Hansjürgen Wenzel", "Eisenbahn-Kurier Verlag, Freiburg", 1980, "de",
            "01형 표준 단행본.", "de.wikipedia 문헌목록", isbn="3-88255-101-1"),
        ref("book", "Baureihe 01 (3. Aufl.)", "Manfred Weisbrod, Wolfgang Petznick", "transpress, Berlin", 1993, "de",
            "동독 시각의 01형(Reko 포함).", "de.wikipedia 문헌목록", isbn="3-344-70769-8"),
    ],
    "de-drg-05": [
        ref("book", "Baureihe 05 – schnellste Dampflok der Welt. Die Geschichte einer Stromlinienlokomotive der dreißiger Jahre",
            "Alfred B. Gottwaldt (mit Eduard Bündgen)", "Franckh, Stuttgart", 1981, "de",
            "05형과 1936년 200.4km/h 기록.", "de.wikipedia 문헌목록", isbn="3-440-04967-1"),
        ref("book", "Die Baureihe 05 (Deutsche Dampflokomotiven Bd. 12)", "Jürgen Quellmalz", "Eisenbahn-Kurier Verlag, Freiburg", 1978, "de",
            "", "de.wikipedia 문헌목록", isbn="3-88255-105-4"),
    ],
    "de-drg-52": [
        ref("book", "Deutsche Kriegslokomotiven 1939–1945", "Alfred B. Gottwaldt", "transpress, Stuttgart", 1996, "de",
            "전시표준형(52·42) 개발사.", "de.wikipedia 문헌목록", isbn="3-344-71032-X"),
        ref("book", "Geschichte der Kriegslokomotiven. Reihe 52 und Reihe 42", "Helmut Griebl, Hansjürgen Wenzel", "J. O. Slezak, Wien", 1971, "de",
            "", "de.wikipedia 문헌목록", isbn="3-900134-03-0"),
        ref("book", "Die Lokomotiven der Baureihe 52", "Michael Reimer", "Lokrundschau-Verlag, Gülzow", 1996, "de",
            "", "de.wikipedia 문헌목록", isbn="3-931647-03-X"),
    ],
    "de-drg-44": [
        ref("book", "Die Baureihe 44", "Peter Konzelmann", "EK-Verlag, Freiburg", 1981, "de", "", "de.wikipedia 문헌목록", isbn="3-88255-144-5"),
        ref("book", "Die Baureihe 44", "Manfred Weisbrod", "Hermann Merker Verlag, Fürstenfeldbruck", 1994, "de", "", "de.wikipedia 문헌목록", isbn="3-922404-55-3"),
    ],
    "de-drg-0310": [
        ref("book", "Die Baureihe 03.10 der Deutschen Reichsbahn. Geschichte einer eleganten Schnellzug-Lokomotive", "Robin Garn", "Berlin", 2005, "de",
            "유선형 외장 철거·Reko 까지.", "de.wikipedia 문헌목록", isbn="3-935909-23-3"),
    ],
    "de-dr-18201": [
        ref("article", "legendäre 18 201 (EK-Special 38)", "Jürgen U. Ebel", "EK-Verlag, Freiburg", 1995, "de", "", "de.wikipedia 문헌목록"),
        ref("book", "Legende 18 201. Schnellste Dampflok der Welt", "Axel Zwingenberger", "Selbstverlag", 2006, "de", "", "de.wikipedia 문헌목록"),
    ],
    "de-br-10": [
        ref("book", "Die Baureihe 10", "Jürgen-Ulrich Ebel", "EK-Verlag, Freiburg", 1998, "de", "", "de.wikipedia 문헌목록", isbn="978-3-88255-101-3"),
        ref("book", "Wittes Neubaulokomotiven. Die letzten Dampfloks der Deutschen Bundesbahn und ihre Schöpfer 1949 bis 1977",
            "Alfred Gottwaldt", "EK-Verlag, Freiburg", 2014, "de", "DB 신제 증기기관차(10형 포함)의 배경.", "de.wikipedia 문헌목록", isbn="978-3-88255-772-5"),
    ],
    # 프랑스
    "fr-crampton": [
        ref("book", "La Locomotive Crampton (Les Carnets du Musée des arts et métiers)", "Clive Lamming (rédaction)", "Musée des arts et métiers (CNAM), Paris", None, "fr",
            "박물관 소장 크램프턴(동부철도 80호)의 해설 소책자(8쪽). 발행연도 미표기.",
            "fr.wikipedia 문헌목록 / 박물관 PDF(carnet_crampton.pdf) 표지·서지", isbn="2908207427",
            url="http://www.arts-et-metiers.net/sites/arts-et-metiers.net/files/asset/document/carnet_crampton.pdf"),
        _TNS_CRAMPTON1, _TNS_CRAMPTON2,
    ],
    "us-atsf-3751": [
        ref("book", "Iron Horses of the Santa Fe Trail: A Definitive History, in Fact and Photograph, of the Motive Power of One of America's Great Railroads",
            "E. D. Worley", "Southwest Railroad Historical Society, Dallas", 1965, "en",
            "산타페 철도 동력차 전사(480쪽 + 도면 128쪽) — 3751급 4-8-4 수록.", "AbeBooks 서지(초판 목록)"),
    ],
    "fr-242a1": [_CHAPELON, _ROGERS, _TNS_CARPENTER, _TNS_COMPOUND3,
        ref("book", "Les locomotives à vapeur unifiées (2) : 232 R, S, U, 151 TQ, 050 TQ et les prototypes",
            "Bernard Collardey, André Rasserie", "Éditions La Vie du Rail, Paris", 2002, "fr",
            "SNCF 통일형·시제기 — 242 A 1 수록.", "fr.wikipedia '242 A 1' 문헌목록", isbn="2-902808-02-X")],
    "fr-241p": [_TNS_COMPOUND3,
        ref("book", "Les locomotives à vapeur unifiées : 241 P, 240 P, 150 P", "Bernard Collardey, André Rasserie",
            "Éditions La Vie du Rail, Paris", None, "fr", "241 P 형식 단행본(199쪽). 발행연도 미확인.",
            "fr.wikipedia '241 P' 문헌목록", isbn="978-2-902808-93-9"),
    ],
    "fr-231e": [_CHAPELON, _ROGERS, _TNS_CARPENTER, _TNS_COMPOUND3, COUNTRY_REFS["FR"][0]],
    # 폴란드
    "pl-ol49": [_POKROP], "pl-ty51": [_POKROP],
    "pl-pm36": [_POKROP,
        ref("article", "„Piękna Helena” i nie tylko ten parowóz", "(Problemy Kolejnictwa)", "Problemy Kolejnictwa, z. 202", 2024, "pl",
            "Pm36-2 를 다룬 학술지 논문.", "BazTech(ICM) 서지",
            url="http://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-9958b6f5-7f52-463c-b07a-e03b3e219627")],
    # 러시아
    "ru-class-p36": [_RAKOV], "ru-class-l": [_RAKOV], "ru-class-e": [_RAKOV],
    "ru-aa20": [_RAKOV, COUNTRY_REFS["RU"][2]],
    # 중국
    "cn-km": [
        ref("catalog", "Chinese Government Railways steam locomotive 4-8-4 KF class No 7 (Science Museum Group Collection)",
            "Science Museum Group", "collection.sciencemuseumgroup.org.uk", None, "en",
            "요크 국립철도박물관 소장 KF7 의 공식 소장품 기록.", "Science Museum Group Collection",
            url="https://collection.sciencemuseumgroup.org.uk/objects/co205814/chinese-government-railways-steam-locomotive-4-8-4-kf-class-no-7"),
    ],
    # 인도
    "in-fairyqueen": [_HUGHES1], "in-wp": [_HUGHES4], "in-wg": [_HUGHES4],
    "in-dhr-b": [_HUGHES3,
        ref("book", "Halfway to Heaven: Darjeeling and Its Remarkable Railway", "Terry Martin", "RailRomances Publishing", 2000, "en",
            "DHR 1879~2000 통사.", "AbeBooks/Biblio 서지", isbn="9781900622035")],
    # 남아프리카
    "za-class25nc": [_HOLLAND2], "za-class15f": [_HOLLAND2],
    "za-classgl": [_HOLLAND2, _DURRANT_G],
    "za-class26": [_WARDALE],
    # 호주
    "au-c38-3801": [
        ref("book", "3801: A Legend in Steam", "Ron G. Preston", "3801 Limited", 1992, "en", "3801호 단행본.", "en.wikipedia 문헌목록", isbn="0-646-11931-1"),
        ref("book", "A Compendium of New South Wales Steam Locomotives", "Alex Grunbach", "Australian Railway Historical Society, NSW Division", 1989, "en",
            "NSW 증기기관차 전 형식 편람.", "en.wikipedia 문헌목록", isbn="0-909650-27-6"),
    ],
    # 캐나다
    "ca-royalhudson": [COUNTRY_REFS["CA"][0]],
    "ca-cn-6060": [COUNTRY_REFS["CA"][1]],
    # 아르헨티나
    "ar-latrochita": COUNTRY_REFS["AR"],
}


def attach(locos, countries):
    """기관차·국가 dict 에 references 를 붙인다. 알 수 없는 id 는 오류."""
    by_id = {l["id"]: l for l in locos}
    unknown = [k for k in LOCO_REFS if k not in by_id]
    if unknown:
        raise ValueError(f"references.py 에 있는데 LOCOS 에 없는 id: {unknown}")
    for l in locos:
        l["references"] = LOCO_REFS.get(l["id"], [])
    for c in countries:
        c["references"] = COUNTRY_REFS.get(c["code"], [])
    return sum(1 for l in locos if l["references"]), sum(len(v) for v in COUNTRY_REFS.values()) + len(GENERAL)
