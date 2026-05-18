# WORK_LOG

Claude Code가 v3 작업을 진행하며 작성·갱신하는 작업 로그.

작성 형식:

```
## [YYYY-MM-DD HH:MM] 작업번호. 작업제목
- 수정 파일: 파일 경로들
- 핵심 변경: 2~3줄 요약
- 검증 결과: 어떻게 확인했는지
- 사용자 확인 필요 사항: 있다면 명시
```

---

## [2026-05-18] A-0. 사전 점검

- 수정 파일: docs/WORK_LOG.md (초기화)
- 핵심 변경: xlsx 파일 위치 확인
- 검증 결과:
  - `uploads/2025학년도 고등학교 입학생 3개년 교육과정 편제표(입력용).xlsx` ✓
  - `uploads/2026학년도 고등학교 입학생 3개년 교육과정 편제표(입력용).xlsx` ✓
- 사용자 확인 필요 사항: 없음

---

## [2026-05-18] A-1. xlsx 시트 구조 파악

- 수정 파일: 없음 (분석만)
- 핵심 발견:

**xlsx 시트 구조 (2026학년도, 7개 시트)**:
| 시트 | 내용 |
|------|------|
| AdminConfig | 관리자 계정 (무관) |
| Schools | 84+1개 학교 메타정보 |
| Data | 학교별 편제표 JSON (94개) ← 핵심 |
| CourseDB | 835개 과목 마스터 |
| Stats | 통계 요약 |
| 특수목적고 | 특목고 목록 |
| 교과구분 | 교과 구분 기준표 |

**창체 데이터**: 별도 시트 없음. 이미 Data 시트의 편제 JSON에 포함.
- 구조: `changche: {"0":[...], "1":[...], "2":[...]}` (키=활동종류 3가지, 값=6학기 시수단위)
- 학점 변환 공식: 각 학기별 3개 값 합계 / 16 = 해당 학기 창체 학점
- 검증: 이순신고 1-1 = (24+16+16)/16 = 3.5학점 ✓, 1-2 = 3.5학점 ✓
- 천안중앙고: 모든 학기 3.0학점, 총 18학점

**평가 처리 유형**: 별도 시트 없음. 과목 객체에 `achievement` 필드 이미 있음.
- 예: `"achievement": "5단계"`, `"rank": "5등급"`

**순증 과목**: `isSoonjeung: true` + `division: '순증'` 그룹으로 이미 식별 가능.

**핵심 결론**: extract_data.py 수정 불필요. 모든 데이터 이미 curriculum JSON에 있음.
A-2 (extract_data.py 창체 추출) 건너뛰고 A-3 (index.html 수정)부터 진행.

- 사용자 확인 필요 사항: 없음 (A-3 이후 통합 테스트에서 확인)

---

## [2026-05-18] A-3. index.html 창체 학점 반영

- 수정 파일: index.html
- 핵심 변경:
  1. `updateCounter()`에 창체 학점 계산 로직 추가 (changche 키 합산 / 16)
  2. progress-bar 아래 `#changche-row` 요소 추가 → 창체 총학점 + 학기별 분포 표시
  3. total >= 192 달성 시 progress-fill 색상 var(--accent) → var(--ok) 전환
- 검증 결과:
  - JS 문법 체크 통과
  - 이순신고 1-1·1-2 각 3.5학점 ✓
  - 천안중앙고 창체 18학점 (3학점 × 6학기) ✓
  - 지정+창체 기본 116학점, 선택과목 선택 시 192 달성 가능
- 사용자 확인 필요 사항: 로컬 서버에서 UI 확인 요청

---

## [2026-05-18] A-4. 중복 이수 방지

- 수정 파일: index.html
- 핵심 변경:
  - `applyPreset()` 알고리즘 교체: activeSems 루프 진입 전 `pickedSis = new Set()` 추가
  - 매 학기마다 이미 선택된 과목(si) 제외 후 우선순위 높은 과목 선택
  - 후보 부족 시 `console.warn` 출력 (학습 진단용)
- 검증 결과:
  - 충남외고 중국어과 + 인문·어문: 14개 선택그룹 전체 중복 없음 ✓
  - 천안중앙고 + 이공·자연: 7개 선택그룹 전체 중복 없음 ✓
  - JS 문법 체크 OK
- 사용자 확인 필요 사항: 로컬 테스트에서 UI 확인 요청

---

## [2026-05-18] A-5. 순증 과목 활성화

- 수정 파일: index.html
- 핵심 변경:
  1. CSS: `.soonjeung`, `.selected-soonjeung` 스타일 추가 (--warn 계열)
  2. renderGroup() 헤더: isSoonjeung 분기 → "순증 — 희망자 수강" pill
  3. renderGroup() 셀: semCredits[i] 기반으로 활성/비활성 판단, (N) 형태 표시
  4. render(): querySelector에 `.soonjeung` 셀 추가
  5. updateCounter(): isSoonjeung 그룹을 soonjeungTotal로 분리, 192 진행률 제외
  6. HTML: #soonjeung-row 요소 추가 (선택 시만 표시)
- 검증 결과:
  - JS 문법 체크 OK
  - 홍성고 순증 그룹 4개, 각 활성 학기 정확히 1개 (2-1, 3-1, 2-2, 3-2) ✓
  - 천안중앙고 순증 그룹 없음 → 안전 폴백 확인 ✓
- 사용자 확인 필요 사항: 로컬 서버에서 순증 셀 클릭 가능 여부 확인

---

## [2026-05-18] A-6. 과학(군) / 정보과학 분리

- 수정 파일: index.html
- 핵심 발견: 데이터는 이미 분리됨 (과학 28개, 정보 5개, 정보·통신 27개) → case (a) UI만 수정
- 핵심 변경:
  1. `ord` 배열에서 `정보`를 `과학` 바로 다음으로 이동 (인접 표시)
  2. `labelMap` 추가: `과학` → `과학(자연)`, `정보` → `정보과학`
- 검증 결과:
  - JS 문법 체크 OK
  - 북일고 지정과목 시뮬: 과학(자연) 10학점 / 정보과학 3학점 인접 표시 ✓
- 사용자 확인 필요 사항: 없음 (A-7로 진행)

---

## [2026-05-18] A-7. 평가 처리 유형 배지 추가

- 수정 파일: index.html
- 핵심 변경:
  1. CSS: `.eval-badge` 스타일 추가 (9px, 회색 배경, 차분한 톤)
  2. renderGroup() 과목명 셀: achievement 값 → 5단/3단/P/F 배지 삽입
  3. achievement 빈값이면 배지 생략
- 검증 결과:
  - JS 문법 체크 OK
  - 천안중앙고: 공통국어1 [5단] 등 정상 렌더
  - 3단계(과학탐구실험, 체육 등), P/F 배지 분포 확인 ✓
  - 빈값(8개) → 배지 미표시 ✓
- 사용자 확인 필요 사항: 없음 (A-8 커밋 준비로 진행)

---

## [2026-05-18] A-8. Phase A 커밋 & 푸시

- 커밋 해시: 5cc6bf3
- 변경 파일: index.html (+117/-11), docs/WORK_LOG.md (신규)
- 푸시 완료: https://github.com/curricenterhscne/course_selector_cne
- 배포 URL: https://curricenterhscne.github.io/course_selector_cne/

---

## [2026-05-18] B-1. 학급수 표시 제거

- 수정 파일: index.html
- 핵심 변경: `render()` 함수의 metaParts에서 1/2/3학년 학급수 조합 부분 제거
- 검증 결과: JS 문법 체크 OK, 학교명·지역만 표시 확인 ✓
- 사용자 확인 필요 사항: 없음

---

## [2026-05-18] B-2. "프리셋" → "추천 과목" 용어 변경

- 수정 파일: index.html
- 핵심 변경:
  1. 버튼·라벨: "계열 프리셋" → "계열별 추천 과목"
  2. 토스트: "추천 과목을 적용했습니다. 직접 수정할 수 있어요"
  3. 코드 식별자(PRESETS, applyPreset 등)는 변경 없음
- 검증 결과: UI 텍스트에 "프리셋" 단어 없음 ✓
- 사용자 확인 필요 사항: 없음

---

## [2026-05-18] B-3. 학교 통합 검색

- 수정 파일: index.html
- 핵심 변경:
  1. #region-sel, #school-sel, #school-search 제거 → #school-finder + #finder-dropdown 추가
  2. SCHOOL_ABBREV 딕셔너리: 외고→외국어고, 과고→과학고 등 6개 약어 확장
  3. getFinderMatches(): prefix → contains → region 우선순위 정렬, 최대 10개
  4. 키보드 ↑↓/Enter/Esc 지원, 학과 있는 학교 ✦ 표시
- 검증 결과:
  - "외고" → 충남외국어고등학교 매칭 ✓
  - "천안" → 천안 지역 학교 목록 ✓
  - 충남디자인예술고 ✦ 표시 ✓
- 사용자 확인 필요 사항: 로컬 서버 UI 확인 요청

---

## [2026-05-18] B-4. 교과군별 필수 이수학점 표시

- 수정 파일: index.html
- 핵심 변경:
  1. 상수 추가: REQUIRED_CREDITS (국어8/수학8/영어8/사회8/한국사6/과학8/체육8/예술6),
     GROUPED_CATEGORY (기술·가정/정보/정보과학/제2외국어/한문/교양/정보·통신 → 12학점)
  2. renderCreditRow(): 충족 ✓ (--ok 초록) / 미달 ✗ (--accent 적색) / 미정의 → 학점만 표시
  3. groupedKeys 집합으로 합산 교과 필터링 후 "기·정·외·한·교" 한 행으로 합산
- 검증 결과:
  - JS 문법 체크 OK
  - GROUPED_CATEGORY 필터 로직 확인: '정보' 원본 키는 groupedKeys에 포함, '과학'은 main 유지 ✓
  - .satisfied/.violated CSS 클래스 기존 정의 활용 ✓
- 사용자 확인 필요 사항: 로컬 서버에서 천안중앙고 + 이공·자연 프리셋 적용 후 ✓/✗ 표시 확인 요청

---

## [2026-05-18] B-5. 저장/불러오기 (JSON/PDF/Excel)

- 수정 파일: index.html
- 핵심 변경:
  1. **UI (B-5-1)**: `.presets` 줄에 `💾 저장 ▾` 드롭다운(JSON/PDF/Excel) + `📂 불러오기` 레이블 버튼 + 숨겨진 파일 input 추가. 드래그앤드롭 지원.
  2. **JSON 저장 (B-5-2)**: `exportToJSON()` — schema/year/schoolCode/selections/preset/summary 포함 JSON Blob 다운로드. 파일명: `과목선택_[학교명]_[YYYYMMDDHHmm].json`
  3. **JSON 불러오기 (B-5-2)**: `importFromJSON(file)` — schema 검증, 학년도 자동 전환, schoolCode로 학교 로드, selections 복원, preset 버튼 상태 복원, 토스트 안내
  4. **PDF 저장 (B-5-3)**: `exportToPDF()` — html2pdf.js CDN 동적 로드, `body.printing` 클래스로 UI 숨김, A4 가로 landscape 출력, 선택 셀 ✓ 표시
  5. **Excel 저장 (B-5-4)**: `exportToXLSX()` — SheetJS CDN 동적 로드, 3개 시트 생성 (편제표/요약/선택그룹)
  6. **공유 헬퍼**: `_buildSummary()` — JSON·Excel 모두에서 재사용하는 총학점+교과군 집계
  7. **인쇄 CSS**: `body.printing` + `@media print` 규칙 추가
- 검증 결과:
  - JS 문법 체크 OK
  - 모든 심볼(ensureLibrary, exportToJSON, importFromJSON, exportToPDF, exportToXLSX, initSaveLoad) 정확한 위치 확인 ✓
  - index.html 총 1340줄 (정상 범위)
- 사용자 확인 필요 사항: ⏸ B-5-5 전체 통합 검증 (JSON 저장→불러오기, PDF, Excel, 오류 케이스) 로컬 서버에서 확인 요청

---

## [2026-05-18] B-6. Phase B 커밋 & 푸시

- 커밋 해시: e35799c
- 변경 파일: index.html (+522/-54), docs/WORK_LOG.md (+81), docs/ 3개 파일 신규
- 푸시 완료: https://github.com/curricenterhscne/course_selector_cne
- 배포 URL: https://curricenterhscne.github.io/course_selector_cne/

---

## [2026-05-18] D-0. 사전 점검

- 수정 파일: 없음 (분석만)
- 핵심 발견:
  - 시안 파일 2개 확인: mockup_a_desktop.html (668줄), mockup_a_mobile.html (970줄)
  - Phase A·B 완료 확인 (커밋 e35799c)
  - 변수 매핑: --accent→--brand, --ink-soft→--ink-3, --line-strong→--ink-2, --row-1/2→--line-soft/--bg-2
  - 타입배지: .type-badge → .type-dot (D-3 적용 예정)
  - 모바일: renderMobile() 신규 작성 필요 (D-5)
- 사용자 확인 필요 사항: 완료

---

## [2026-05-18] D-1. 디자인 토큰 교체

- 수정 파일: index.html
- 핵심 변경:
  1. Pretendard CDN 추가 (viewport-fit=cover도 추가)
  2. `:root` 전체 교체: 시안 A 토큰(brand/ink/line/shadow/radius 변수군) + 호환성 aliases
  3. body: 'Noto Serif KR' → 'Pretendard', font-feature-settings: 'tnum' 추가
  4. `.num` 클래스 tabular-nums 전역 추가
  5. serif 잔재 제거: .division-num, td.sem-cell, .total-row .num, renderGroup 인라인, td.subject-name
  6. .group-header 배경: #1a1815 → var(--ink)
- 검증 결과: JS OK, 구 hex값·serif 잔재 0건 ✓
- 사용자 확인 필요 사항: 로컬 서버에서 보라톤·Pretendard 폰트 적용 확인 요청

---

## [2026-05-18] D-2. 헤더·도구모음 리디자인

- 수정 파일: index.html
- 핵심 변경:
  1. `<header>` HTML 전체 교체: logo-badge 칩, SVG 아이콘 버튼(저장·불러오기·공유), year-pill 토글, 검색창(SVG 아이콘+search-wrap), school-meta 칩(:empty CSS 제어), reco-row
  2. CSS 교체: `.toolbar`/`.presets`/`.preset-btn` 등 → `.h-top`/`.h-toolbar`/`.year-pills`/`.search-wrap`/`.reco-row`/`.reco-btn`/`.icon-btn`/`.tool-btn`
  3. JS: `.preset-btn` → `.reco-btn` 전체 치환, year-sel → year-pill 이벤트/동기화(3곳), `.finder-wrap` → `.search-wrap` (click-outside 핸들러)
  4. print CSS 클래스명 동기화
- 검증 결과: JS 문법 OK, `finder-wrap` 잔재 0건 ✓
- 사용자 확인 필요 사항: 로컬 서버에서 헤더 외관, 검색·년도·저장 동작 확인 요청

---

## [2026-05-18] D-3. 편제표 그룹 카드 리디자인

- 수정 파일: index.html
- 핵심 변경:
  1. `.group-card`: border-radius·overflow·transition 추가, `.group-card.fixed` 그라데이션 배경
  2. `.group-header` → `.group-head`: 흰 배경+border-bottom, `.group-mark` 28×28 박스 (fixed는 brand 색)
  3. 그룹 meta pill 색상: 어두운 다크 → ok-soft/warn-soft/danger-soft 라이트 톤
  4. `th` 배경: `#f3efe4` → `var(--line-soft)`, border-bottom 토큰화
  5. `td.sem-cell.selectable:hover`: `#ede6d4` → `var(--brand-softer)`
  6. `td.sem-cell.disabled-sem` stripe 색: `#e8e2d4` → `var(--line)`
  7. `.type-badge` → `.type-dot`: 6×6 원형 점, 텍스트 제거
  8. renderGroup HTML: `class="group-card"` → fixed 조건부 클래스, `group-header` → `group-head`, `division-num` → `group-mark`, type-badge → type-dot
  9. legend: type-badge → type-dot, sample stripe 색 토큰화
- 검증 결과: JS 문법 OK, group-header/type-badge 잔재 0건 ✓
- 사용자 확인 필요 사항: 로컬 서버에서 편제표 카드 외관, 선택 셀 색상, 타입 점 표시 확인 요청

---

## [2026-05-18] D-4. 우측 패널 + 진행률 카드

- 수정 파일: index.html
- 핵심 변경:
  1. `aside.counter-panel`: border/bg 제거, flex column + gap 12px 레이아웃
  2. `.progress-card`: 그라데이션 보라 카드 (brand→brand-2), 반원 장식 `::after`, `.achieved` 시 초록 전환
  3. `.pc-label/pc-value/pc-bar`: 36px 숫자, 흰 진행 바, 달성 메시지 CSS 제어
  4. `.summary-card` + `.panel-section`: 흰 카드 + 교과군/선택그룹 섹션 분리
  5. `#soonjeung-row/:not(:empty)`, `#changche-row/:not(:empty)`: 카드형 스타일
  6. `.eval-badge` 배경 토큰화
  7. `updateCounter()`에 `progress-card.achieved` 클래스 토글 한 줄 추가
- 검증 결과: JS 문법 OK, total-row/progress-bar 잔재 0건 ✓
- 사용자 확인 필요 사항: 로컬 서버에서 우측 패널(그라데이션 카드·교과군·선택그룹), 192학점 달성 시 녹색 전환 확인 요청

---

## [2026-05-18] D-5. 모바일 반응형

- 수정 파일: index.html
- 핵심 변경:
  1. main: 1fr 360px 그리드, 768px 이하 display:block, padding-bottom:88px
  2. @media 768px: header 압축, reco-row 가로 스크롤 캐러셀, legend 숨김
  3. aside: 768px에서 fixed 하단 도크(62px), .sheet-open 시 78vh 슬라이드 업
  4. .mobile-dock: 하단 바 — "이수학점 N / 192" + "상세 ▴", 탭으로 시트 토글
  5. .sheet-backdrop: 반투명 오버레이
  6. renderMobile(): 창체 카드 + 1·2·3학년 아코디언 + 학기 탭 + subject-row 카드 목록
  7. renderMobileSem(): 학기별 과목 행 렌더링
  8. toggleGrade() / switchSem(): 아코디언·탭 DOM 조작
  9. onMobileRowClick(): 모바일 과목 행 클릭 → state 토글 → render() → pushUrl()
  10. toggleSheet(): 도크 탭 → counter-panel 슬라이드 업/다운 + backdrop
  11. state.isMobile + matchMedia resize 리스너
  12. updateCounter() 끝에 m-total 갱신 한 줄 추가
- 검증 결과: JS 문법 OK, 6개 모바일 함수 정의 확인 ✓
- 사용자 확인 필요 사항:
  - Chrome DevTools 모바일 뷰(390×844)로 천안중앙고 선택 후 아코디언·탭·과목 선택 동작 확인
  - 하단 도크 탭 → 시트 슬라이드 업 확인
  - 데스크탑(1280px↑)에서 회귀 없음 확인

---

## [2026-05-18] D-6. 최종 커밋 & 푸시

- 수정 파일: index.html, docs/WORK_LOG.md (+ docs/03_DESIGN_RENEWAL.md, mockup_a_*.html 추가)
- 커밋 해시: ac55ebd
- 커밋 메시지: feat: 디자인 리뉴얼 — 시안 A 적용 (Toss/Notion 모던 톤)
- 배포 URL: https://curricenterhscne.github.io/course_selector_cne/
- 검증 결과: JS 문법 OK, push 성공 ✓

---

## [2026-05-18] G-0. 학생 가이드 통합 — 사전 점검

- 수정 파일: 없음 (확인만)
- 확인 결과:
  - D-1~D-6 완료 기록 확인 ✓
  - guide.html 프로젝트 루트 존재 ✓
  - 디자인 토큰(--brand, Pretendard) 본 사이트와 동일 ✓
  - "실습으로 돌아가기" 링크 href="./" ✓
- 사용자 선택: 헤더 버튼=아이콘+텍스트, placeholder 안내 링크=추가

---

## [2026-05-18] G-1. guide.html 배치 확인

- 수정 파일: 없음
- 확인 결과: 이미 루트에 위치, 링크 경로 정상 ✓

---

## [2026-05-18] G-2. index.html 헤더에 사용 설명서 진입 버튼 추가

- 수정 파일: index.html
- 핵심 변경:
  1. `.guide-btn` CSS: 보라 테두리+배경 버튼, 호버 시 보라 채움
  2. `a.icon-btn` CSS: 링크 요소에도 아이콘 버튼 스타일 적용
  3. `.placeholder-guide-link` CSS: 진입 유도 버튼
  4. 헤더 `.h-actions` 맨 앞에 `<a class="guide-btn">` 추가 (책 아이콘 + "사용 설명서")
  5. 모바일 768px: `.guide-btn span { display: none }`, 버튼 34×34px로 압축
  6. placeholder에 "처음 사용하신다면 사용 설명서를 먼저 읽어 보세요 →" 링크 추가
- 검증 결과: JS 문법 OK ✓
