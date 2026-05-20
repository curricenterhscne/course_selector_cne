# CLAUDE.md — 충남 고교 과목 선택 실습 사이트

## 프로젝트 개요

충청남도교육청 중등교육과(고교학점제 담당)에서 운영할 **고교학점제 과목 선택 시뮬레이션 사이트**.
2025·2026학년도 입학생용 편제표 데이터(187개교 + 학과 분기)를 기반으로 학생·학부모·교사가
직접 과목을 선택해보며 졸업학점·교과군별 이수·선택그룹 충족 여부를 실시간 확인.

벤치마크: 온마당(onmadang.or.kr)의 학교별 편제표 페이지 — 단, 우리 사이트는 **단순 열람이 아니라
체크박스 시뮬레이션**까지 한다는 것이 핵심 차별점.

## 기술 스택

- **순수 정적 사이트**: HTML + Vanilla JS + CSS (빌드 도구·프레임워크·서버 없음)
- **데이터**: JSON 파일들 (`data/` 하위), 학교 선택 시 fetch로 lazy load
- **배포 대상**: GitHub Pages (계정: `curricenterhscne`)
- **로컬 테스트**: `python3 -m http.server 8080` 또는 VS Code Live Server

## 폴더 구조

```
.
├── index.html                       # 단일 페이지 앱 (32KB, 모든 로직 inline)
├── README.md                        # 기능 설명서
├── CLAUDE.md                        # 이 파일
├── .nojekyll                        # GitHub Pages Jekyll 비활성화 (한글 파일명 보호)
├── .gitignore
└── data/
    ├── schools.json                 # 84개 일반고 메타정보 (학과 인덱스 포함)
    ├── courseDB.json                # 834개 과목 마스터
    ├── curriculum_2025_index.json
    ├── curriculum_2025/             # 학교별 편제표 93개 JSON
    │   ├── N100000246.json
    │   ├── N100000262(애니메이션과).json   # 특목고는 학과별 파일
    │   └── ...
    ├── curriculum_2026_index.json
    └── curriculum_2026/             # 94개 JSON
```

특목고/예고/체육중점 등은 같은 base 코드 + `(학과명)` suffix로 분기됨.
예: 충남디자인예고 = N100000262 → `(시각디자인과)`, `(애니메이션과)`, `(패션디자인과)`

## 주요 기능 (완료된 것)

1. **학년도·지역·검색 필터** + 학교 드롭다운
2. **학교 선택 → 3개년 × 6학기 편제표 자동 렌더** (지정/선택 그룹 구분)
3. **체크박스 시뮬레이션**: 선택 그룹의 셀 클릭 → 학점 누적, "학기별 택 N" 조건 검증
4. **계열 프리셋 6종**: 이공·자연 / 공학·IT / 경상·사회 / 인문·어문 / 예술 / 체육
   - 과목명 키워드 매칭으로 학교마다 다른 개설 과목에도 자동 대응
5. **URL 공유**: 모든 상태(`?y=2026&s=...&p=...`)를 쿼리스트링에 직렬화, 클립보드 복사
6. **특목고 학과 통합**: 학교 선택 시 학과 드롭다운 자동 노출
7. **그룹 헤더 충족 배지** 실시간 표시
8. **우측 패널**: 총 이수학점 / 192학점 진행률 / 교과군별 합계 / 선택그룹 충족 현황

## 디자인 톤

- **에디토리얼·차분한 공공 문서 톤** (Noto Serif KR + Pretendard 혼용)
- 메인 컬러: 적색(#b8341e) — 학점 강조·선택 셀
- 흑백 헤더(#1a1815) + 베이지 배경(#f7f5ef)
- 화려한 애니메이션 X, 정보 밀도와 가독성 우선

## 로컬 테스트 방법

`file://`로 직접 열면 fetch가 CORS에 막힙니다. **반드시 로컬 서버**로 띄울 것:

```bash
python3 -m http.server 8080
# → http://localhost:8080
```

또는 VS Code Live Server, `npx serve` 등.

## GitHub Pages 배포 시 주의사항

1. **`.nojekyll` 파일 필수** — 폴더명에 언더스코어가 없어 큰 문제는 없지만, 한글 파일명
   (`N100000262(애니메이션과).json`)이 있어 Jekyll이 무시할 수 있음. 안전을 위해 둠.
2. **한글·괄호 파일명의 URL 인코딩** — `index.html`의 `loadCurriculum`에서 이미
   `encodeURIComponent(code)`로 처리됨. GitHub Pages가 한글 파일명을 자동 인코딩해
   서빙하므로 그대로 동작함.
3. **`main` 브랜치 root에서 서빙** 설정. `docs/` 폴더로 빼지 않음.
4. **CDN 캐싱**: 정적 JSON이라 push 후 즉시 반영 안 될 수 있음. 강력 새로고침(Cmd+Shift+R).

## 데이터 갱신 방법

### 편제표 수정 / 학교 추가

```bash
# 1. uploads/ 에 새 xlsx 파일 놓기 (파일명 형식 유지)
# 2. 변경사항 미리보기
python3 update_data.py --dry-run

# 3. 특정 연도만 갱신
python3 update_data.py --year 2026

# 4. 전체 갱신
python3 update_data.py

# 5. git add data/ && git commit && git push
```

### 신규 학년도 추가 (예: 2027학년도)

```bash
# 1. uploads/ 에 2027학년도 xlsx 추가
# 2. update_data.py 상단 KNOWN_YEARS 에 '2027' 추가
# 3. 실행 (index.html year-pill 자동 패치 포함)
python3 update_data.py --year 2027
# 4. index.html에서 기본 연도(state.year, URL 기본값) 수동 확인
# 5. git add data/ index.html && git commit && git push
```

### xlsx 주의사항
- `uploads/` 폴더는 .gitignore — Schools 시트에 담당자연락처·비밀번호 포함
- 파일명 형식: `{YYYY}학년도 고등학교 입학생 3개년 교육과정 편제표(입력용).xlsx`

## 향후 개선 후보 (작업 우선순위 아님)

- 공동교육과정·충남온라인학교 개설 과목 연계 배지
- 학교 간 편제 비교 (좌우 분할)
- 학년도 비교 (2025 vs 2026 같은 학교 diff)
- 데이터 정리: 2026에 `N10000` 깨진 코드 1건 (Schools에 없어 미사용, 무해)

## 코딩 스타일

- JavaScript는 vanilla, 외부 라이브러리 없음. ES2020+ 문법 OK
- CSS는 단일 `<style>` 블록 inline. CSS 변수(`--accent` 등)로 컬러 관리
- 한글 주석·식별자 OK (도메인 용어는 한국어가 정확함)
- 파일 추가 시 들여쓰기는 2칸 스페이스
