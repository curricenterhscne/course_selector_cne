# cne-design-system

**충남 고교학점제 종합지원 온마당 디자인 시스템 v1.0**
참학력 온라인 공동교육과정 멤버쉽 캐릭터 **꾸꾸클럽** 기반 · C-1 라이트 도미넌트

충남 고교학점제 가족 사이트(신규 온마당 + 모든 하위 모듈·웹앱)가 한눈에 같은 가족으로
인식되도록 하는 **단일 진실원**입니다. 모든 사이트는 이 레포의 CSS를 참조합니다.

---

## 빠른 시작

```html
<head>
  <!-- 1. 본문 폰트 -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
  <!-- 2. 디자인 토큰 (필수, 먼저) -->
  <link rel="stylesheet" href="tokens/design-tokens.css">
  <!-- 3. 컴포넌트 (선택) -->
  <link rel="stylesheet" href="components/components.css">
</head>
```

캐릭터를 쓰려면 `assets/characters/`의 SVG를 `<img>`로 삽입합니다:
`<img src="assets/characters/paenkkumi.svg" alt="팬꾸미" style="height:120px">`
(디자이너 원본 벡터, 투명 배경. 자세한 사용법은 `assets/README.md` 참조.)

**라이브 프리뷰 / 레퍼런스**: `templates/preview.html`을 브라우저로 열어보세요.
모든 색·서체·컴포넌트·캐릭터가 실제 적용된 모습을 한 화면에서 볼 수 있습니다.

---

## 파일 구조

```
cne-design-system/
├─ README.md              ← 지금 이 파일
├─ DESIGN-GUIDE.md        ← 사람이 읽는 상세 가이드 (색·서체·캐릭터 활용·분기 원칙)
├─ prompts.md             ← Claude Code 적용 프롬프트 템플릿
├─ tokens/
│  └─ design-tokens.css   ← 색·서체·간격·반경·그림자 변수 (단일 진실원)
├─ components/
│  └─ components.css       ← 핵심 컴포넌트 5 + 배지·빈상태·관리자 표면
├─ assets/
│  ├─ README.md           ← 캐릭터 자산 사용법
│  ├─ characters/         ← 디자이너 원본 캐릭터 (꾸꾸클럽.ai에서 벡터 추출)
│  │  ├─ paenkkumi.svg · tokkumi.svg · kkumi.svg · kkukkuk-club-logo.svg
│  │  └─ png/             ← 동일 캐릭터 고해상도 투명 PNG (PPT/인쇄용)
│  └─ characters-guide.html ← 캐릭터 적용 예시 페이지
└─ templates/
   └─ preview.html        ← 라이브 프리뷰 / 스타일 가이드 데모
```

---

## 핵심 규칙 (자세한 내용은 DESIGN-GUIDE.md)

- **색**: 배경=라이트블루(`#DAF2FC`), 브랜드=진블루(`#4F6EBE`), 액센트=그린(`#7BCE7C`, 네잎클로버=권장/행운). 모두 꾸꾸클럽 PDF에서 추출.
- **의미 토큰 우선**: `--color-brand`를 쓰고 `--kkuk-blue-500`을 직접 쓰지 않기.
- **서체**: 본문 Pretendard, 한글 가독성 최우선.
- **캐릭터**: 학생 화면에 적극, 행정 화면(`.surface-admin`)엔 절제.
- **배지 의미 통일**: ★권장=그린 / ◆핵심=진블루 / 온라인=라이트블루.

---

## 버전

- **v1.0** (2026-05): 색·서체·간격·핵심 컴포넌트 5·배지·캐릭터 자산·빈 상태·관리자 표면.
- 모달·탭·차트 등은 실제 모듈을 만들며 같은 토큰 위에서 확장 예정.
