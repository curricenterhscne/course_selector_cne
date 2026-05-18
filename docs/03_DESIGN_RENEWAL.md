# 03. 디자인 리뉴얼 작업 지시서 — 시안 A 적용

> 이 문서는 Claude Code 작업 지시서다. v3 작업이 완료된 상태에서 시작한다.
> ⏸ 마커가 있는 곳에서는 반드시 사용자에게 보고하고 응답을 기다린 후 진행한다.
> 작업 단위 완료마다 `docs/WORK_LOG.md`에 기록한다.

작업 목표: v3 사이트의 디자인을 **시안 A(Toss/Notion 모던 톤)** 으로 전면 교체.
PC와 모바일 모두 자연스럽게 보이는 반응형 단일 페이지로 구현.

---

## 작업 원칙 (반드시 지킬 것)

### 1. JavaScript 로직 절대 변경 금지

다음 함수들은 **이름·시그니처·동작 모두 보존**한다:
- `applyPreset(presetKey)` — 계열 추천 적용
- `updateCounter()` — 학점 집계
- `render()` / `renderGroup()` — 편제표 렌더링
- `exportToJSON()` / `importFromJSON()` / `exportToPDF()` / `exportToXLSX()` — 저장·불러오기
- `state` 객체 구조 (`userSelections`, `selectedCode`, `activePreset` 등)
- URL 직렬화 함수들

수정 대상: **CSS, 일부 HTML 마크업, 렌더링 시 생성되는 className**.

### 2. 단계적 머지

한 번에 다 갈아엎지 말고 5단계로 나눈다. 각 단계 끝에서 사용자 확인.

### 3. 시안 파일은 참조 전용

`mockup_a_desktop.html`, `mockup_a_mobile.html`은 **참조**다. 그대로 복사하면
실데이터 연결이 깨진다. 시안에서 색상·간격·컴포넌트 스타일만 추출해 본 사이트에
이식한다.

### 4. 반응형 단일 페이지

PC와 모바일 둘을 별도 파일로 만들지 않는다. 하나의 `index.html`이 화면 폭에 따라
자동 분기되도록 미디어 쿼리로 구현. 분기 기준: **768px**.

---

## D-0. 사전 점검

수행할 작업:

1. v3 작업 완료 확인 — `docs/WORK_LOG.md`에 Phase A·B 완료 기록이 있는지.
2. `mockup_a_desktop.html`, `mockup_a_mobile.html`이 프로젝트 루트에 있는지 확인.
   없으면 사용자에게 위치 묻고 멈춤.
3. 두 시안 파일을 view로 열어서 디자인 토큰(CSS 변수)·컴포넌트 구조 파악.
4. 현재 `index.html`의 `<style>` 블록 구조 파악:
   - CSS 변수 정의 위치
   - 각 컴포넌트 클래스 (header, group-card, sem-cell 등)
   - 미디어 쿼리 현황

⏸ **사용자 확인 필요**: 점검 결과 보고 후 "D-1 진행해줘" 응답 받으면 시작.

---

## D-1. 디자인 토큰 교체 (Step 1/5)

목적: 색상·폰트·간격·모서리·그림자의 기본 변수만 교체. 컴포넌트 구조는 그대로.
이 단계만 끝나도 사이트 분위기가 크게 바뀐다.

수행할 작업:

1. `index.html`의 `<style>` 최상단 `:root` 블록을 시안 A의 토큰으로 교체:

   ```css
   :root {
     --bg: #fafafa;
     --bg-2: #f1f5f9;
     --panel: #ffffff;
     --ink: #0f172a;
     --ink-2: #334155;
     --ink-3: #64748b;
     --ink-4: #94a3b8;
     --line: #e2e8f0;
     --line-soft: #f1f5f9;

     --brand: #4f46e5;
     --brand-2: #6366f1;
     --brand-3: #818cf8;
     --brand-soft: #eef2ff;
     --brand-softer: #f5f3ff;

     --ok: #059669;
     --ok-soft: #d1fae5;
     --warn: #d97706;
     --warn-soft: #fef3c7;
     --danger: #dc2626;
     --danger-soft: #fee2e2;

     --r-sm: 6px;
     --r: 10px;
     --r-lg: 14px;
     --r-xl: 20px;

     --shadow-sm: 0 1px 2px rgba(15,23,42,.04);
     --shadow: 0 1px 3px rgba(15,23,42,.06), 0 1px 2px rgba(15,23,42,.04);
     --shadow-lg: 0 10px 30px -10px rgba(15,23,42,.12);
     --shadow-up: 0 -8px 24px -6px rgba(15,23,42,.10);
     --shadow-brand: 0 8px 24px -8px rgba(79,70,229,.4);

     --safe-bottom: env(safe-area-inset-bottom, 0px);
   }
   ```

2. 폰트 변경:
   - `<head>` 안에 Pretendard CDN 추가:
     ```html
     <link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
     ```
   - 기존 Noto Serif KR 관련 link 제거.
   - body의 `font-family`를 `'Pretendard', -apple-system, system-ui, sans-serif`로.

3. 기존 코드에서 v2 시절 색상 변수(`--accent`, `--accent-soft`,
   `--type-gongtong` 등)가 이름이 달라졌다면 매핑:
   - `--accent` → `--brand`
   - `--accent-soft` → `--brand-soft`
   - 그 외 직접 색상값(`#b8341e` 같은 v2 적색)이 박혀있으면 `--brand`로 교체.

4. 숫자 표시(`.num` 클래스)에 tabular-nums 적용:
   ```css
   .num { font-feature-settings: 'tnum'; font-variant-numeric: tabular-nums; }
   ```

검증 단계:

1. 로컬 서버로 띄워서 페이지 로드.
2. 색상이 모던 보라 톤으로 바뀌었는지 확인.
3. **기능은 모두 정상 동작해야 함** — 학교 선택, 추천 적용, 저장/불러오기 등
   v3 자가 테스트 체크리스트 항목 모두 통과.
4. 텍스트가 Pretendard로 렌더링되는지 (Noto Serif KR 흔적 없는지).

⏸ **사용자 확인 필요**: 토큰 교체 결과 보고 후 "D-2 진행" 받으면 다음 단계.
색상이 너무 강하거나 약하면 D-1에서 수정.

---

## D-2. 헤더 + 추천 버튼 영역 (Step 2/5)

수행할 작업:

1. 헤더 마크업 구조를 시안 A에 맞춰 정리:
   - **상단 줄**: 로고 + "고교학점제" 배지 + subtitle + 우측 아이콘 버튼들(저장/공유)
   - **두 번째 줄**: 학년도 pill + 검색 입력 + 학교 칩
   - **세 번째 줄**: 계열 추천 버튼들 + 우측 도구

2. 헤더 CSS를 시안 A 스타일로:
   ```css
   header {
     background: rgba(255,255,255,0.85);
     backdrop-filter: blur(10px);
     border-bottom: 1px solid var(--line);
     padding: 14px 28px;
     position: sticky; top: 0; z-index: 50;
   }
   ```

3. 로고 영역:
   - 작은 보라색 "고교학점제" 배지(`background: var(--brand)`, `color: #fff`)
   - 옆에 "과목 선택 실습" 텍스트

4. 학년도 pill 스타일 변경 — 토글 형태 (`year-pills` + `year-pill` 클래스):
   ```css
   .year-pills { display: inline-flex; background: var(--line-soft); padding: 3px; border-radius: 99px; }
   .year-pill { padding: 6px 14px; border-radius: 99px; border: 0; background: transparent; ... }
   .year-pill.active { background: var(--panel); color: var(--ink); box-shadow: var(--shadow-sm); }
   ```

5. 검색 입력 스타일:
   - 좌측에 검색 아이콘 (SVG)
   - 포커스 시 `border-color: var(--brand)` + `box-shadow: 0 0 0 3px var(--brand-soft)`

6. 추천 버튼:
   - 평소: 흰 배경 + 회색 테두리 + pill 모양
   - 호버: 보라색 테두리·텍스트
   - 활성: 보라색 배경 + 흰 텍스트 + `box-shadow: 0 4px 12px -4px var(--brand)`
   - 활성 시 앞에 `✓` 마커

7. 아이콘 버튼 (저장/공유/불러오기):
   - 36×36 정사각형, 회색 테두리, 호버 시 보라 액센트
   - 이모지 대신 **SVG 아이콘** 사용 (Lucide-style — 시안 A 참조)

⏸ **사용자 확인 필요**: 헤더 디자인 확인 후 다음 단계.

---

## D-3. 편제표 그룹 카드 (Step 3/5)

목적: 가장 큰 시각적 변화. 표 안의 셀까지 모두 모던 톤으로.

수행할 작업:

1. 그룹 카드 컨테이너:
   ```css
   .group-card {
     background: var(--panel);
     border: 1px solid var(--line);
     border-radius: var(--r-lg);
     margin-bottom: 16px;
     overflow: hidden;
     transition: border-color .15s;
   }
   .group-card:hover { border-color: var(--ink-4); }
   .group-card.fixed { background: linear-gradient(180deg, var(--brand-softer) 0%, var(--panel) 60%); }
   ```

2. 그룹 헤더 (현재 검정 배경에서 → 흰 배경 + 마커 박스로):
   ```css
   .group-head {
     padding: 14px 18px;
     display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
     border-bottom: 1px solid var(--line-soft);
   }
   .group-mark {
     width: 28px; height: 28px;
     background: var(--ink); color: #fff;
     border-radius: var(--r);
     /* fixed 그룹은 brand 컬러 */
   }
   ```

3. 칩(pill) 색상 매핑:
   - 평소: `var(--line-soft)` 회색 배경
   - 충족: `var(--ok-soft)` 초록
   - 진행중: `var(--warn-soft)` 노랑
   - 초과: `var(--danger-soft)` 빨강
   - brand: `var(--brand-soft)` 보라

4. 표 셀 스타일:
   ```css
   th { background: var(--line-soft); ... }
   td.sem.has { background: var(--brand-soft); color: var(--brand); font-weight: 700; }
   td.sem.selected { background: var(--brand); color: #fff; font-weight: 700; }
   td.sem.cl:hover { background: var(--brand-softer); }
   td.sem.disabled-sem { background: repeating-linear-gradient(...); }
   ```
   기존 클래스명을 유지하면서 색상만 바꾼다.

5. 과목 타입 배지 → 작은 컬러 점(dot)으로 변경:
   ```css
   .type-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 8px; }
   .type-공통 { background: #475569; }
   .type-일반 { background: #3b82f6; }
   .type-진로 { background: #ec4899; }
   .type-융합 { background: #10b981; }
   ```
   `renderGroup` 함수에서 기존 `.type-badge` HTML 생성 부분을 `.type-dot`으로 변경.
   배지 안의 "공/일/진/융" 한 글자는 제거 (점만으로 의미 전달).

검증 단계:

1. 천안중앙고 선택 → 편제표가 모던 톤으로 표시.
2. 이공·자연 추천 적용 → 선택된 셀이 보라색으로 표시.
3. 그룹 헤더의 충족 배지가 색상별로 정상 표시.
4. 데이터·기능 회귀 없음.

⏸ **사용자 확인 필요**: 편제표 디자인 확인 후 다음 단계.

---

## D-4. 우측 패널 + 진행률 카드 (Step 4/5)

수행할 작업:

1. 우측 패널 위치·구조는 그대로. 내부 디자인만 시안 A로.

2. 최상단 진행률 카드 — 그라데이션 보라 카드로 강조:
   ```html
   <div class="progress-card">
     <div class="pc-label">총 이수학점</div>
     <div class="pc-value">
       <span class="num" id="total-credits">0</span>
       <span class="of">/ 192</span>
     </div>
     <div class="pc-bar"><div id="progress-fill"></div></div>
   </div>
   ```
   ```css
   .progress-card {
     padding: 22px;
     background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%);
     color: #fff;
     border-radius: var(--r-lg);
     position: relative; overflow: hidden;
   }
   .progress-card::after {
     content: ''; position: absolute;
     right: -30px; top: -30px;
     width: 140px; height: 140px;
     background: rgba(255,255,255,0.08);
     border-radius: 50%;
   }
   .pc-value { font-size: 36px; font-weight: 800; letter-spacing: -0.02em; }
   ```

3. `updateCounter()` 함수에서 192학점 달성 시:
   - `.progress-card`에 `.achieved` 클래스 추가
   - 추가 메시지 영역 표시 (예: "졸업 학점 달성")
   - 단, 기존 로직은 건드리지 말고 클래스 추가만.

4. 교과군별 / 선택 그룹 / 창체 섹션은 흰 카드(`summary-card`)로 묶기:
   ```css
   .summary-card {
     background: var(--panel);
     border: 1px solid var(--line);
     border-radius: var(--r-lg);
     overflow: hidden;
   }
   .panel-section { padding: 16px 18px; }
   .panel-section + .panel-section { border-top: 1px solid var(--line-soft); }
   ```

5. 통계 행(`.stat-row`) 스타일:
   - 좌측 라벨 + 우측 값
   - 충족 시 초록(`var(--ok)`) + 작은 ✓
   - 미달 시 빨강(`var(--danger)`) + ✗

⏸ **사용자 확인 필요**: 우측 패널 확인 후 다음 단계.

---

## D-5. 모바일 반응형 (Step 5/5) — 가장 중요한 단계

목적: 768px 이하 화면에서 모바일 시안처럼 동작하도록 반응형 구현.
별도 페이지 만들지 않고, 같은 `index.html`이 자동 분기.

### D-5-1. 레이아웃 분기

```css
/* 데스크탑: 우측 패널 sticky */
main { display: grid; grid-template-columns: 1fr 360px; }
aside.counter-panel { position: sticky; top: 130px; }

/* 모바일 */
@media (max-width: 768px) {
  main {
    display: block;
    padding: 14px;
    padding-bottom: 100px; /* 하단 도크 공간 */
  }
  aside.counter-panel {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    top: auto;
    /* 모바일에서는 우측 패널이 하단 도크로 변신 */
    /* 자세한 내용은 D-5-3 */
  }
}
```

### D-5-2. 모바일 헤더 압축

```css
@media (max-width: 768px) {
  header { padding: 12px 14px 10px; }
  .h-toolbar { gap: 8px; }
  /* 학년도 + 검색 + 학교 칩이 한 줄에 들어가지 않으면 줄바꿈 */
  .search-wrap { max-width: 100%; flex: 1 1 100%; }
  /* 추천 버튼은 가로 스크롤 캐러셀로 */
  .reco-row {
    flex-wrap: nowrap;
    overflow-x: auto;
    scrollbar-width: none;
    margin: 0 -14px;
    padding: 10px 14px 4px;
  }
  .reco-row::-webkit-scrollbar { display: none; }
  .reco-btn { flex-shrink: 0; }
  .reco-label { display: none; } /* 모바일에서는 라벨 숨김 */
}
```

### D-5-3. 편제표 → 학년 아코디언 + 학기 탭 변환

⚠ 이 부분이 가장 큰 작업이다. 데이터 구조는 그대로 두고, **렌더 시 마크업만 분기**.

전략:
- `state.isMobile = window.matchMedia('(max-width: 768px)').matches`로 모바일 여부 감지
- `render()` 함수에서 `state.isMobile`이면 `renderMobile()` 호출, 아니면 기존 `renderGroup()` 호출
- 리사이즈 시 다시 렌더

`renderMobile()` 함수 신규 작성:
1. 편제 그룹들을 **학년별로 묶음** (지정 그룹의 1학년 학기는 1학년, 선택 그룹은
   그 그룹이 운영되는 학기로 묶음).
2. 각 학년을 하나의 아코디언 카드로 렌더 (`.grade-card`).
3. 학년 카드 안에 학기 탭(1-1, 1-2 또는 2-1, 2-2).
4. 각 학기 안에 해당 그룹의 과목들을 **카드 리스트** 형태로 렌더 (`.subject-row`).
5. 셀 클릭 → 모바일에서는 행 전체 클릭 → 그 학기의 셀 토글.

마크업 예시 (`renderMobile()`이 만들 HTML):

```html
<div class="changche-card">
  <div class="changche-icon">⭐</div>
  <div class="changche-main">
    <div class="changche-title">창의적 체험활동</div>
    <div class="changche-detail">
      <span class="changche-num num">18학점</span>
      <span class="changche-sub">학기별 3씩 자동</span>
    </div>
  </div>
</div>

<div class="grade-card">
  <div class="grade-head open" onclick="toggleGrade(1)">
    <span class="grade-num">1</span>
    <div class="grade-title-block">
      <div class="grade-title">1학년</div>
      <div class="grade-sub">공통 과목 · 자동 이수</div>
    </div>
    <div class="grade-status">
      <span class="grade-credit num">38<span class="unit">학점</span></span>
      <svg class="chevron">...</svg>
    </div>
  </div>
  <div id="g1-body">
    <div class="sem-tabs">
      <button class="sem-tab active" onclick="switchSem(1, '1-1')">1학기<span class="sub">1-1</span></button>
      <button class="sem-tab" onclick="switchSem(1, '1-2')">2학기<span class="sub">1-2</span></button>
    </div>
    <div class="grade-body" id="g1-content">
      <!-- 학기별 과목 카드들 -->
    </div>
  </div>
</div>
```

### D-5-4. 모바일 하단 진행률 도크

데스크탑의 우측 진행률 카드가 모바일에서는 하단 고정 도크로 변신:

```css
@media (max-width: 768px) {
  aside.counter-panel {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    top: auto;
    width: 100%;
    max-height: none;
    background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%);
    color: #fff;
    padding: 12px 16px calc(12px + var(--safe-bottom));
    box-shadow: var(--shadow-up);
    z-index: 90;
    border-radius: 0;
    /* 평소엔 미니바, 탭하면 Bottom Sheet 전체 펼침 */
  }
  /* 모바일에서는 우측 패널 내부 섹션 숨기고 미니 표시만 */
  .counter-panel .panel-section,
  .counter-panel h3 { display: none; }
  /* 모바일에서만 보일 mini-dock 영역 */
  .counter-panel .mobile-dock { display: flex; }
}
.counter-panel .mobile-dock { display: none; }
```

`.mobile-dock` HTML 마크업을 우측 패널 안에 추가:
```html
<div class="mobile-dock" onclick="openSheet()">
  <div class="md-text">
    <div class="md-label">총 이수학점</div>
    <div class="md-value"><span id="m-total">192</span> / 192</div>
  </div>
  <span class="md-arrow">상세 ▴</span>
</div>
```

### D-5-5. Bottom Sheet (상세 충족 현황)

모바일 도크 탭 시 슬라이드 업으로 전체 충족 현황 노출:

```html
<!-- body 끝 부분에 추가 -->
<div class="sheet-backdrop" id="sheet-bg" onclick="closeSheet()"></div>
<div class="bottom-sheet" id="sheet">
  <div class="sheet-handle"></div>
  <div class="sheet-head">
    <h2>이수 학점 현황</h2>
    <button class="close-x" onclick="closeSheet()">✕</button>
  </div>
  <!-- 우측 패널 내용 복제 (창체, 진행률 카드, 교과군, 선택 그룹) -->
  <!-- updateCounter()가 이 영역도 갱신하도록 ID 추가 -->
</div>
```

```css
.bottom-sheet {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: var(--panel);
  border-radius: 22px 22px 0 0;
  z-index: 96;
  transform: translateY(100%);
  transition: transform .28s cubic-bezier(.22,.6,.32,1);
  max-height: 78vh;
  overflow-y: auto;
  padding-bottom: calc(20px + var(--safe-bottom));
}
.bottom-sheet.show { transform: translateY(0); }
.sheet-backdrop { /* 배경 흐림 */ }
```

`updateCounter()` 함수가 우측 패널 + 시트 양쪽 모두 갱신하도록 셀렉터 추가.
기존 ID 두 곳에 같은 값 표시: 데스크탑은 우측 패널 보이고 시트는 숨겨짐,
모바일은 반대.

### D-5-6. 모바일 터치 타깃 검증

- 모든 클릭/탭 가능 요소가 최소 44px 높이인지 확인 (Apple HIG)
- 검색 입력 → 40px 이상
- 추천 버튼 → 36px 이상이지만 좌우 패딩으로 손가락 접근성 확보
- 과목 행 → 52px 이상

검증 단계:

1. Chrome DevTools 모바일 뷰(390×844, iPhone 14)로 천안중앙고 선택.
2. 학년 아코디언 펼침/접힘 정상.
3. 학기 탭 전환 시 해당 학기 과목만 표시.
4. 과목 행 탭 → 선택 토글 + 우측 데스크탑 patch 동기화 확인.
5. 하단 도크 탭 → Bottom Sheet 열림.
6. 시트 안 충족 현황 모두 정상 표시.
7. 가로 회전(landscape) 시 깨지지 않음.

⏸ **사용자 확인 필요**: 모바일 동작 결과 보고. 실제 휴대폰에서도 테스트
권장 (배포 후).

---

## D-6. 마무리 — 커밋 & 푸시

⏸ **사용자 승인 필요**: 다음을 보고:

1. 변경된 파일 목록.
2. D-1 ~ D-5 작업 요약.
3. 기능 회귀 없음 검증 결과.
4. 커밋 메시지 제안:
   ```
   feat: 디자인 리뉴얼 — 시안 A 적용 (Toss/Notion 모던 톤)

   - 디자인 토큰 교체 (Pretendard, 보라 메인, 모던 그림자)
   - 헤더·추천버튼·편제표·우측패널 전면 리뉴얼
   - 모바일 반응형 (768px 분기): 학년 아코디언 + 학기 탭 + 하단 도크 + Bottom Sheet
   ```

사용자 승인 시:
1. `git add -A && git commit -m "..." && git push origin main`
2. WORK_LOG.md에 푸시 시각·커밋 해시 기록.
3. 사용자에게 배포 URL 안내 (1~2분 후 반영).

---

## 디자인 리뉴얼 자가 테스트 체크리스트

배포 후 사용자가 직접 확인:

### 데스크탑 (1280px 이상)
- [ ] 헤더가 모던 톤(반투명, 보라 배지)으로 표시
- [ ] 학년도 pill, 검색 입력, 학교 칩, 추천 버튼이 시안 A처럼 보임
- [ ] 편제표 카드가 깔끔하게 분리되어 표시
- [ ] 과목 타입이 작은 색깔 점으로 표시
- [ ] 우측 진행률 카드가 그라데이션 보라색으로 표시
- [ ] 192학점 달성 시 시각적 강조 (있다면)

### 모바일 (≤ 768px, 실제 휴대폰 권장)
- [ ] 헤더가 압축되어 표시
- [ ] 추천 버튼이 가로 스크롤 캐러셀
- [ ] 편제표가 학년 아코디언으로 변환
- [ ] 학기 탭 전환 정상
- [ ] 과목 행이 카드 리스트 형태
- [ ] 하단에 진행률 도크 고정
- [ ] 도크 탭 시 Bottom Sheet 열림
- [ ] 시트에 교과군·선택 그룹 충족 현황 모두 표시
- [ ] 가로 회전 시 깨지지 않음

### 기능 회귀 확인 (반드시)
- [ ] 학교 선택 정상
- [ ] 학과 선택 정상 (충남외고 등)
- [ ] 추천 적용 정상 (이공·자연 등)
- [ ] 중복 이수 방지 정상 (Phase A 검증)
- [ ] 창체 학점 192학점 정상 표시
- [ ] 저장 (JSON/PDF/Excel) 정상
- [ ] 불러오기 (JSON) 정상
- [ ] 공유 링크 정상
- [ ] URL 직접 진입 정상

⏸ **사용자 확인 필요**: 모두 통과해야 디자인 리뉴얼 완료.
문제 있으면 해당 단계로 돌아가 수정.
