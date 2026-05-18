# 인수인계 문서 — 충남 고교 과목 선택 실습 사이트

> 이 문서는 다른 컴퓨터(회사)에서 작업을 이어받는 Claude Code / Claude Chat에게 전달하는 문서입니다.
> 마지막 업데이트: 2026-05-18

---

## 📌 한눈에 보는 현재 상태

| 항목 | 내용 |
|------|------|
| 배포 URL | https://curricenterhscne.github.io/course_selector_cne/ |
| 가이드 URL | https://curricenterhscne.github.io/course_selector_cne/guide.html |
| GitHub | curricenterhscne/course_selector_cne (main 브랜치) |
| 최신 커밋 | `214c68d` (2026-05-18) |
| 로컬 경로 | `/Users/kimkang106/curricenter.hs.cne/course_selector_cne` |
| 기술 스택 | 순수 정적 HTML + Vanilla JS + CSS (빌드 도구 없음) |
| 로컬 서버 | `python3 -m http.server 8080` → http://localhost:8080 |

---

## ✅ 완료된 작업 전체 이력

### Phase A — 데이터·버그 수정
- schools.json NaN → null 수정
- 중복 이수 방지 로직
- 창의적 체험활동 학점 자동 계산

### Phase B — UX 개선
- JSON / PDF / Excel 저장·불러오기 (`exportToJSON`, `importFromJSON`, `exportToPDF`, `exportToXLSX`)
- URL 공유 (쿼리스트링 직렬화)

### Phase D — 디자인 리뉴얼 (시안 A, Toss/Notion 모던 톤)
- **D-1**: Pretendard 폰트, 보라 brand 토큰(`--brand: #4f46e5`) 교체
- **D-2**: 헤더 전면 교체 — logo-badge, SVG 아이콘 버튼, year-pill, 검색창
- **D-3**: 편제표 카드 — 흰 배경+border-radius, group-mark 박스, type-dot 점
- **D-4**: 우측 패널 — 그라데이션 progress-card (보라→초록 달성 전환)
- **D-5**: 모바일 768px 반응형 — 학년 아코디언, 학기 탭, 하단 도크, 슬라이드 시트
- **D-6**: 커밋·푸시

### 모바일 버그픽스 (D-5 이후 실기기 테스트)
- iOS Safari: `overflow-y:auto` 내 `sticky` 요소 click 불가 → `.sheet-scroll` 래퍼로 해결
- 모바일 독 배경: 흰색 불투명(`#ffffff`)으로 변경
- reco-row "선택비우기" 세로 정렬 → `margin-left: 0`으로 수정

### Phase G — 학생 가이드 통합
- `guide.html` 프로젝트 루트 배치 (시안 A 톤, Pretendard, 동일 디자인 토큰)
- `index.html` 헤더 `.h-actions` 맨 앞에 `📖 사용 설명서` 버튼 추가
- 모바일에서 텍스트 숨김 → 34×34px 아이콘만 표시
- Placeholder에 첫 방문 학생 안내 링크 추가

---

## 🗂️ 핵심 파일 구조

```
.
├── index.html              ← 단일 페이지 앱 (~1780줄, 모든 로직 inline)
├── guide.html              ← 학생용 사용 설명서 (독립 정적 페이지)
├── CLAUDE.md               ← ⭐ Claude Code 지시서 (반드시 먼저 읽기)
├── README.md
├── docs/
│   ├── WORK_LOG.md         ← ⭐ 전체 작업 이력 (현재 상태 파악용)
│   ├── HANDOFF.md          ← 이 파일
│   ├── 03_DESIGN_RENEWAL.md
│   └── 04_STUDENT_GUIDE.md
└── data/
    ├── schools.json        ← 84개 일반고 메타정보
    ├── courseDB.json       ← 834개 과목 마스터
    ├── curriculum_2025/    ← 93개 학교별 편제표 JSON
    └── curriculum_2026/    ← 94개 학교별 편제표 JSON
```

---

## 🔧 index.html 구조 (핵심 요소)

```
<head>
  Pretendard CDN
  <style>  ← CSS 전체 (CSS 변수, 컴포넌트, 미디어 쿼리)
</head>
<body>
  <header>
    .h-top     → 로고 | subtitle | .h-actions(guide-btn, 저장, 불러오기, 공유)
    .h-toolbar → year-pills | 검색창 | school-meta 칩 | dept-sel
    .reco-row  → 계열 추천 버튼 6개 | 선택비우기
  </header>
  <main>
    <section#curriculum-area>  ← 편제표 렌더링 영역
    <aside.counter-panel>      ← 이수학점 패널
      .mobile-dock             ← 모바일 하단 도크 (스크롤 영역 밖)
      .sheet-scroll            ← 모바일 스크롤 영역
        .progress-card
        #soonjeung-row, #changche-row
        .summary-card (교과군별, 선택그룹)
  </main>
  .sheet-backdrop  ← 모바일 시트 오버레이
  <script>  ← 모든 JS 인라인
</script>
```

### 보호된 JS 함수 (수정 금지)
- `applyPreset(presetKey)` — 계열 추천
- `updateCounter()` — 학점 집계
- `render()` / `renderGroup()` — 편제표 렌더링
- `renderMobile()` / `renderMobileSem()` — 모바일 렌더링
- `exportToJSON()` / `importFromJSON()` / `exportToPDF()` / `exportToXLSX()`
- `state` 객체 구조, URL 직렬화 함수들

---

## 🎨 디자인 토큰 (CSS 변수)

```css
--brand: #4f46e5;   /* 메인 보라 */
--brand-2: #6366f1;
--brand-soft: #eef2ff;
--ink: #0f172a;     /* 본문 검정 */
--ink-3: #64748b;   /* 서브 텍스트 */
--line: #e2e8f0;    /* 테두리 */
--bg: #fafafa;      /* 배경 */
--panel: #ffffff;   /* 카드 배경 */
--ok: #059669;      /* 충족 */
--warn: #d97706;    /* 경고 */
--danger: #dc2626;  /* 초과 */
```

---

## 🚀 다음 세션에서 할 일

1. **디테일 수정** — 회사 컴퓨터에서 재확인 후 발견되는 UI/UX 이슈
2. **최종 검증** — 충남 전체 187개교 편제표 로드 이상 없음 확인
3. **충남 전체 학생 안내 배포** — 공식 URL 공유 및 홍보

---

## 💡 새 세션 시작 방법

### Claude Code (터미널)
```bash
cd /path/to/course_selector_cne   # 또는 git clone 후
cat CLAUDE.md                      # 프로젝트 지시서 먼저 읽기
cat docs/WORK_LOG.md               # 작업 이력 확인
python3 -m http.server 8080        # 로컬 서버 실행
```

### Claude Chat (브라우저)
이 HANDOFF.md 파일을 첨부하거나 내용을 붙여넣어 컨텍스트 제공.

---

## ⚠️ 주의사항

1. **JS 로직 절대 변경 금지** — 위 "보호된 JS 함수" 목록 참조
2. **로컬 서버 필수** — `file://` 직접 열면 fetch CORS 오류
3. **변경 후 JS 문법 검증**:
   ```bash
   node -e "const fs=require('fs');const html=fs.readFileSync('index.html','utf8');const m=html.match(/<script>([\s\S]*?)<\/script>/);try{new Function(m[1]);console.log('JS OK')}catch(e){console.error(e.message)}"
   ```
4. **push 전 사용자 승인 필수** — 반드시 확인 후 push
5. **GitHub Pages**: push 후 1~2분 대기, 강력 새로고침(Cmd+Shift+R)

---

*이 문서는 Claude Code가 자동 생성했습니다. 최신 상태는 `docs/WORK_LOG.md`를 참조하세요.*
