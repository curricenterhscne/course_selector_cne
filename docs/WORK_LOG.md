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
