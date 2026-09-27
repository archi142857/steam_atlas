# 국기 에셋

`flag-icons` (https://github.com/lipis/flag-icons) 의 4x3 SVG를 사용합니다.
라이선스: MIT — 전문은 같은 폴더의 `LICENSE` 참조. 앱 설정 화면에도 표기해 두었습니다.

파일명은 ISO 3166-1 alpha-2 소문자입니다 (`kr.svg`, `gb.svg` …).
`countries.json` 의 `code` 를 소문자로 바꾸면 그대로 경로가 됩니다.

## 국가를 추가할 때

```bash
npm install flag-icons          # 또는 이미 받아둔 사본에서
cp node_modules/flag-icons/flags/4x3/<code>.svg assets/flags/
python3 tools/build_preview.py  # 프리뷰에 data URL로 다시 인라인
```

## 주의

`RU`는 '러시아·소련'을 함께 묶은 항목이라 현재 러시아 국기를 씁니다.
소련 시기 차량과 러시아 시기 차량을 나눠 표기하려면 국가 코드를 분리해야 합니다.
