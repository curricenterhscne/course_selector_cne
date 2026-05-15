# Claude Code 작업 가이드 — 충남 고교 과목 선택 실습 사이트 배포

이 문서는 시형 님이 **Claude Code에 그대로 복붙해서 사용**할 수 있는 프롬프트 모음입니다.
순서대로 한 단계씩 진행하세요.

---

## 사전 준비 (시형 님이 직접 — Claude Code 작업 전)

### 1) 파일 위치 정리

이 폴더(`transfer_to_claude_code/`) 전체를 작업 공간 적당한 곳에 옮깁니다.
예: `C:\Users\<사용자>\Documents\github\course_selector_cne\`

폴더 이름은 `course_selector_cne`(또는 시형 님 취향대로) 추천. 이 이름이 곧 GitHub 저장소 이름이 됩니다.

### 2) GitHub 저장소 만들기

브라우저에서 `https://github.com/curricenterhscne` 로 이동 → **New repository**
- Repository name: `course_selector_cne` (위 폴더명과 동일하게)
- Public 선택
- README/`.gitignore`/license **추가하지 않음** (이미 로컬에 있음)
- "Create repository" 클릭
- 만들어진 저장소 페이지에 표시되는 URL 메모: `https://github.com/curricenterhscne/course_selector_cne.git`

### 3) Claude Code 실행

VS Code에서 위 폴더를 열고, 통합 터미널(Git Bash 권장) 띄우기.
이전에 사용해보셨던 흐름 그대로 `claude` 명령으로 Claude Code 시작.

---

## STEP 1 — Git 초기화 & 첫 커밋

Claude Code 채팅창에 그대로 붙여넣기:

```
이 폴더에서 Git 저장소를 초기화하고 첫 커밋을 만들어줘.

1. git init
2. git branch -M main
3. 현재 디렉터리의 모든 파일을 스테이징
4. 다음 메시지로 커밋: "feat: 충남 고교 과목 선택 실습 사이트 v2 초기 커밋

- 84개 일반고 + 187개 학교/학과별 편제표 JSON
- 계열 프리셋 6종(이공/공학/경상/인문/예술/체육)
- URL 공유 기능
- 특목고 학과 드롭다운 통합"

커밋 전에 git status를 한번 보여줘서 어떤 파일이 추가되는지 확인할게.
```

---

## STEP 2 — GitHub 원격 저장소 연결 & push

```
방금 만든 GitHub 저장소에 연결하고 push해줘.

저장소 URL: https://github.com/curricenterhscne/course_selector_cne.git

1. git remote add origin https://github.com/curricenterhscne/course_selector_cne.git
2. git remote -v 로 확인
3. git push -u origin main

만약 인증 오류가 나면 멈추고 알려줘. (gh auth login은 VS Code 통합터미널에서 내가 직접 실행해야 하니까.)
```

> **주의**: `gh auth login`이 필요한 경우 Claude Code의 bash 도구로는 실행이 안 됩니다.
> Claude Code가 멈추면, **VS Code 통합 터미널에서 시형 님이 직접** `gh auth login` 실행한 뒤
> 다시 Claude Code에 "다시 push 시도해줘"라고 입력하세요.

---

## STEP 3 — GitHub Pages 활성화 (브라우저에서 직접)

Claude Code가 할 수 없으니 시형 님이 직접 합니다.

1. `https://github.com/curricenterhscne/course_selector_cne` 접속
2. **Settings → Pages**
3. **Source**: "Deploy from a branch"
4. **Branch**: `main` / **Folder**: `/ (root)`
5. **Save**
6. 1~2분 후 페이지 상단에 `Your site is live at https://curricenterhscne.github.io/course_selector_cne/` 표시되는지 확인

배포 URL 형식: `https://curricenterhscne.github.io/course_selector_cne/`

---

## STEP 4 — 배포 직후 테스트 (브라우저에서 직접)

배포 URL을 열고 다음을 차례로 확인:

| # | 테스트 | 기대 결과 |
|---|---|---|
| 1 | 페이지 로딩 | 헤더·툴바·플레이스홀더 정상 표시 |
| 2 | 학년도 = 2026, 지역 = 천안, 학교 = 천안중앙고 선택 | 8개 그룹(지정+선택 1~7) 표시, 우측 패널 학점=98 |
| 3 | "이공·자연" 프리셋 버튼 클릭 | 26개 셀 자동 선택, 총 학점 174 표시, "추천 조합 적용" 토스트 |
| 4 | 선택 1의 미적분Ⅰ 셀 하나 클릭 | 프리셋 active 해제, 해당 셀 토글 |
| 5 | "🔗 공유 링크 복사" 버튼 | "복사되었습니다" 토스트, 시크릿 창에서 그 URL 열면 같은 상태 복원 |
| 6 | 학교 = 충남외국어고등학교 선택 | 학과 드롭다운(베트남어과/영어과/일본어과/중국어과) 자동 노출 |
| 7 | 학과 변경 | 편제표 즉시 갱신 |
| 8 | 학년도를 2025로 변경 | 같은 학교의 2025 편제표 로딩 |
| 9 | 모바일(Chrome DevTools 모바일 뷰) | 우측 패널이 아래로 내려가는 1열 레이아웃 |

문제가 발견되면 다음 단계로.

---

## STEP 5 — 문제 발견 시 Claude Code에 요청

### 케이스 A: 한글 파일명이 404 나는 경우

```
배포 사이트에서 충남외국어고를 선택하면 학과 JSON이 404가 나.
URL은 https://curricenterhscne.github.io/course_selector_cne/data/curriculum_2026/N100002532(영어과).json 이런 형태야.

index.html의 fetch 부분이 한글·괄호 파일명을 제대로 인코딩하는지 점검하고,
필요하면 수정해줘. .nojekyll이 root에 있는지도 확인.
```

### 케이스 B: 스타일이 깨져 보일 때

```
배포 사이트의 [구체적 위치]가 [구체적 증상]이야.
스크린샷은 [경로]에 저장했어 (또는: 다음과 같은 증상이야: ...).

index.html의 CSS를 점검해서 수정해줘.
```

### 케이스 C: 데이터가 안 보이는 학교가 있을 때

```
[학교명] 선택했더니 "편제표 데이터를 찾지 못했습니다" 메시지가 나와.
브라우저 콘솔에는 [에러 메시지]가 떠.

data/curriculum_2026/ 안에 그 학교 파일이 있는지 확인하고,
schools.json의 학교코드와 일치하는지 점검해줘.
```

---

## STEP 6 — 수정 후 재배포

```
방금 수정한 내용을 커밋하고 push해줘.

커밋 메시지는 변경 내용에 맞게 작성. 예시:
- "fix: 한글 파일명 fetch 시 URL 인코딩 보완"
- "style: 모바일에서 학교 메타정보 줄바꿈"
- "data: 누락 학교 X고등학교 데이터 추가"

push 후 GitHub Actions가 자동으로 Pages를 재배포해 (1~2분 소요).
```

---

## STEP 7 — 운영 시 알아둘 것

### 데이터 갱신 (학교에서 편제표 수정해서 올렸을 때)

1. 새 xlsx 두 파일을 받아서 시형 님 로컬의 `/uploads/`에 둠
2. 시형 님이 직접(또는 Claude에게) 데이터 추출 스크립트 재실행:
   ```bash
   python3 extract_data.py
   ```
3. 새로 생긴 `data/` 폴더를 저장소의 `data/` 위에 덮어쓰기
4. Claude Code에 다음 요청:
   ```
   data/ 폴더 내용이 갱신됐어. 변경된 파일 확인하고,
   다음 메시지로 커밋·push해줘:
   "data: 2026학년도 편제표 갱신 (YYYY-MM-DD 기준)"
   ```

### 도메인 연결 (선택)

`curricenterhscne.github.io/course_selector_cne/` 대신 깔끔한 주소를 원하면:
- 무료: `course-selector-cne.netlify.app` (Netlify 배포)
- 유료: 별도 도메인 구매 후 GitHub Pages CNAME 설정

---

## 도움 요청 양식

작업 중 막히면 다음 양식으로 Claude(이 채팅 or Claude Code)에 보내주세요:

```
[현재 단계] STEP N
[기대한 동작] ...
[실제 동작] ...
[에러 메시지 / 스크린샷 경로] ...
[이미 시도해본 것] ...
```
