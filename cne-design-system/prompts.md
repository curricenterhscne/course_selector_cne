# Claude Code 프롬프트 템플릿 — 꾸꾸클럽 디자인 시스템 적용

이 디자인 시스템을 실제 웹앱에 적용하거나 새 모듈을 만들 때, 아래 템플릿을
Claude Code(터미널)에 그대로 붙여 쓰세요. `<...>` 부분만 채우면 됩니다.

전제: 작업 대상 레포에서 디자인 시스템을 참조할 수 있어야 합니다. 권장 방식 중 하나:
- (A) `cne-design-system`을 git submodule로 추가, 또는
- (B) GitHub Pages/CDN에 올린 CSS를 `<link>`로 참조, 또는
- (C) `tokens/`·`components/`·`assets/`만 대상 레포에 복사.

---

## 템플릿 1 — 기존 사이트에 토큰부터 점진 적용

```
이 레포는 충남 고교학점제 가족 사이트 중 하나야(<레포 설명: 예 course_selector_cne — 학교별 시간표 시뮬레이션>).
꾸꾸클럽 디자인 시스템 v1.0을 점진 적용하려고 해. 한 번에 다 바꾸지 말고 아래 순서로:

1) cne-design-system/tokens/design-tokens.css 를 먼저 import 하고,
   기존 색·서체·간격을 디자인 토큰(--color-*, --text-*, --space-*)으로 치환해.
   - 기존 적색/베이지 톤은 폐기. 배경은 --color-bg(라이트블루), 강조는 --color-brand(진블루),
     '권장/행운'은 --color-accent(그린)으로 매핑.
2) 토큰만으로 전체가 가족 톤으로 보이는지 먼저 확인하고 멈춰. 컴포넌트 교체는 그 다음 단계에서.

기존 기능(187개교 데이터, 6개 계열 프리셋, URL 공유, 그룹 충족 배지)은 절대 깨지면 안 돼.
변경 전후로 동작을 확인하고, diff를 작게 유지해.
```

## 템플릿 2 — 컴포넌트를 kk- 클래스로 교체

```
디자인 토큰 적용은 끝났어. 이제 화면 단위로 컴포넌트를 components/components.css 의
kk- 클래스로 교체하자. 이번엔 <대상 화면/영역: 예 과목 편제표 카드>만.

- 카드는 .kk-card / 과목 카드는 .kk-card--course
- 권장 표시(★)는 .kk-badge--recommend, 핵심(◆)은 .kk-badge--core, 온라인 개설은 .kk-badge--online
- 버튼은 .kk-btn--primary / --secondary
원래 마크업 구조와 데이터 바인딩은 유지하고, 클래스와 스타일만 교체해.
한 화면 끝나면 멈추고 스크린샷으로 확인하자.
```

## 템플릿 3 — bridge 연동 표시를 배지로 통일

```
majors ↔ selector bridge 연동에서 ★(권장)·◆(핵심) 표시를 디자인 시스템 배지로 통일해줘.
- core = 진로선택 → .kk-badge--core (◆)
- want = 일반선택 + 융합선택 → .kk-badge--recommend (★, 그린)
- 미개설 과목 사이드바 안내에는 .kk-badge--online + 안내 문구
URL 파라미터 분류 규칙(core=진로선택만 / want=일반+융합)은 그대로 유지해.
```

## 템플릿 4 — 새 모듈 정적 사이트 골격 생성

```
꾸꾸클럽 디자인 시스템 v1.0으로 새 정적 사이트(vanilla HTML/CSS/JS)를 만들어줘.
모듈: <예: 모듈 1 자기이해 — 흥미·적성·가치관 검사 결과 입력, 강점 카드, 종합 점검표>

요구사항:
- cne-design-system/tokens/design-tokens.css + components/components.css 를 import
- 헤더는 .kk-header (마스코트는 assets/kkuk-characters.svg 의 #kkuk-paenkkumi)
- 이 모듈 대표 캐릭터는 <예: 토꾸미 #kkuk-tokkumi> (DESIGN-GUIDE 모듈별 배정 참고)
- 빈 상태/로딩에 .kk-empty + 캐릭터 활용
- 데이터는 localStorage에 저장(키 접두사: kkuk:module1:)해서 다른 모듈과 공유 가능하게
- 학생용 톤. 행정 화면 아님(.surface-admin 쓰지 말 것)
- 반응형(모바일 우선). 한글 본문 가독성 최우선.
먼저 페이지 골격과 섹션 구조만 만들고 확인받은 뒤 기능을 채우자.
```

## 템플릿 5 — 행정/교사 화면

```
이 화면은 교사·실무자용 행정 화면이야(<예: 187개교 개설 현황 대시보드>).
컨테이너에 .surface-admin 을 적용해서 학생 화면과 차분하게 분기시켜.
- 표는 .kk-table (.kk-table-wrap 으로 감싸 가로 스크롤), 숫자는 .num / 강조는 .num--emph
- 캐릭터는 헤더 마스코트 정도만, 본문엔 절제
- 상태 배지는 .kk-badge--recommend(확정)/--online(검토)/--neutral(미달)
데이터 정확성과 표 정렬(등폭 숫자)이 최우선이야.
```

---

## 공통 주의사항 (모든 프롬프트에 적용)

- **디자인 토큰을 직접 수정하지 말 것.** 색이 안 맞으면 의미 토큰(`--color-*`) 매핑을
  조정하거나, 정말 필요한 신규 토큰은 디자인 시스템 레포에 별도 PR로 추가.
- **원시 색(`--kkuk-blue-500`) 직접 사용 금지**, 의미 토큰 우선.
- **캐릭터는 40px 미만으로 쓰지 말 것**, 코 도트는 항상 진블루(#4F6EBE) 고정.
- **그린 액센트 남용 금지** — "권장/행운/성공" 의미일 때만.
- 변경은 작은 diff로, 화면 단위로 확인하며 진행.
