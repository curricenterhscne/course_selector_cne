# 04. 학생용 사용 설명서 통합 작업 지시서

> 이 문서는 Claude Code 작업 지시서다. 디자인 리뉴얼(`03_DESIGN_RENEWAL.md`) 작업이
> 완료된 상태에서 진행한다.
> ⏸ 마커가 있는 곳에서는 반드시 사용자에게 보고하고 응답을 기다린 후 진행한다.
> 작업 단위 완료마다 `docs/WORK_LOG.md`에 기록한다.

작업 목표:
- 학생용 사용 설명서(`guide.html`)를 사이트에 통합한다.
- 본 사이트(`index.html`) 헤더에 "사용 설명서" 진입 메뉴를 추가한다.
- 독립 링크로도 학생에게 바로 공유할 수 있도록 한다.
- PC와 모바일 모두 자연스럽게 작동해야 한다.

---

## G-0. 사전 점검

수행할 작업:

1. 디자인 리뉴얼 완료 확인 — `docs/WORK_LOG.md`에 D-1 ~ D-6 완료 기록 확인.
2. 프로젝트 루트에 `guide.html` 파일이 있는지 확인.
   - 없으면 사용자에게 위치 물어보고 대기.
   - 있으면 view로 열어 디자인 토큰·구조가 본 사이트와 일치하는지 확인.
3. 현재 `index.html`의 헤더 영역 마크업·CSS 파악:
   - 우측 아이콘 버튼들(저장/공유/불러오기)의 위치
   - 헤더 그리드 구조

⏸ **사용자 확인 필요**: 점검 결과 보고 후 "G-1 진행해줘" 받으면 시작.

---

## G-1. guide.html을 사이트에 배치 (Step 1/3)

수행할 작업:

1. `guide.html`을 프로젝트 루트(`index.html`과 같은 위치)에 둔다.
   - 이미 거기 있으면 스킵.
   - 다른 위치에 있으면 루트로 이동.

2. 정적 페이지로 동작하는지 검증:
   - 로컬 서버(`python3 -m http.server 8080`)로 띄움
   - `http://localhost:8080/guide.html` 접속
   - 페이지 정상 로드 확인 (히어로·요약·5단계·FAQ 모두 표시)
   - 모바일 뷰(DevTools 390px)에서도 깨지지 않는지 확인
   - 인쇄 미리보기에서 출력 가능한지 확인

3. `guide.html`에 다음 보조 작업 확인:
   - **본 사이트로 돌아가는 링크 동작 확인**: 상단 네비의 "실습으로 돌아가기"
     버튼과 하단 "과목 선택 실습 시작하기" 버튼이 모두 `./`(또는 `index.html`)을
     향하는지.
   - 작동 안 하면 링크 경로 수정 (`href="./"`, `href="index.html"`, `href="/"` 중
     배포 환경에 맞춰 선택). GitHub Pages 배포라면 `./`가 안전.

⏸ **사용자 확인 필요**: 로컬에서 `guide.html` 단독으로 정상 동작 확인 후
"G-2 진행" 받기.

---

## G-2. 본 사이트 헤더에 "사용 설명서" 진입 메뉴 추가 (Step 2/3)

목적: `index.html`에서 학생이 한 번 클릭으로 사용 설명서에 진입할 수 있어야 한다.

### G-2-1. 데스크탑 헤더에 메뉴 버튼 추가

수행할 작업:

1. `index.html`의 헤더 우측 아이콘 버튼 영역(저장/공유/불러오기)에 **사용 설명서
   아이콘 버튼**을 추가한다.
   - 위치: 다른 아이콘 버튼들 **왼쪽**, 즉 가장 첫 번째 항목으로.
     (학생이 처음 진입 시 가장 먼저 눈에 들어와야 하므로)
   - 아이콘: 책 또는 도움말(?) 아이콘
   - SVG는 Lucide 스타일로 통일 (다른 아이콘 버튼과 일관성 유지):

   ```html
   <a href="guide.html" class="icon-btn" title="사용 설명서" id="guide-link">
     <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2" stroke-linecap="round"
          stroke-linejoin="round">
       <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
       <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
     </svg>
   </a>
   ```

2. 마크업이 `<button>`이 아닌 `<a>`로 들어가므로, `.icon-btn` CSS가 `<a>`에도
   적용되도록 확인. 필요시 셀렉터 보완:

   ```css
   .icon-btn, a.icon-btn { /* 기존 스타일 */ }
   a.icon-btn { text-decoration: none; color: var(--ink-2); }
   a.icon-btn:hover { text-decoration: none; }
   ```

3. 첫 방문 사용자에게 메뉴를 더 강하게 알리고 싶다면, 아이콘 옆에 텍스트도
   같이 노출하는 변형 버튼을 검토:

   ```html
   <a href="guide.html" class="guide-btn">
     <svg>...</svg>
     <span>사용 설명서</span>
   </a>
   ```

   ```css
   .guide-btn {
     display: inline-flex; align-items: center; gap: 6px;
     padding: 7px 12px;
     border: 1px solid var(--brand);
     background: var(--brand-soft);
     color: var(--brand);
     border-radius: var(--r);
     font-size: 13px; font-weight: 600;
     text-decoration: none;
     transition: all .15s;
   }
   .guide-btn:hover {
     background: var(--brand);
     color: #fff;
     text-decoration: none;
   }
   ```

   ⏸ **사용자 확인 필요**: 아이콘 단독 vs 아이콘+텍스트 중 어느 쪽이 좋은지
   미리 물어보고 진행.

### G-2-2. 모바일 헤더 대응

수행할 작업:

1. 모바일 뷰(≤768px)에서는 헤더가 압축되어 있으므로, 텍스트 라벨이 길면
   잘릴 수 있다. 대응:
   - 모바일에서는 **아이콘만** 표시되도록 미디어 쿼리 처리:

   ```css
   @media (max-width: 768px) {
     .guide-btn span { display: none; }
     .guide-btn { padding: 7px; }
   }
   ```

2. 모바일에서 다른 아이콘 버튼들(저장/공유)과 동일한 36×36 정사각형이 되도록
   확인.

### G-2-3. 첫 방문 학생 안내 (선택, 시형 님 판단)

수행할 작업 (이건 사용자에게 진행 여부 먼저 물어볼 것):

1. 학교 선택 전 상태(placeholder 영역)에 사용 설명서로 안내하는 카드 추가:

   ```html
   <div class="placeholder" id="placeholder">
     좌측 상단에서 학교를 선택하면 3개년 교육과정 편제표가 표시됩니다.
     <br>
     <a href="guide.html" class="placeholder-guide-link">
       처음 사용하신다면 사용 설명서를 먼저 읽어 보세요 →
     </a>
   </div>
   ```

   ```css
   .placeholder-guide-link {
     display: inline-block;
     margin-top: 14px;
     padding: 10px 18px;
     background: var(--brand);
     color: #fff;
     border-radius: var(--r);
     font-size: 13.5px;
     font-weight: 600;
     text-decoration: none;
     box-shadow: var(--shadow-brand);
     transition: transform .15s;
   }
   .placeholder-guide-link:hover {
     transform: translateY(-1px);
     text-decoration: none;
   }
   ```

   ⏸ **사용자 확인 필요**: 이 placeholder 카드 안내를 추가할지 여부를 사용자에게
   물어보고 진행.

검증 단계:

1. 데스크탑 헤더에서 사용 설명서 버튼이 정상 표시되는지.
2. 클릭 시 `guide.html`로 이동하는지.
3. `guide.html`에서 "실습으로 돌아가기" 클릭 시 다시 본 사이트로 돌아오는지.
4. 모바일 뷰에서도 메뉴가 깨지지 않는지.
5. 기존 기능(저장/공유/추천 등) 회귀 없는지.

⏸ **사용자 확인 필요**: 결과 보고 후 "G-3 진행" 받으면 마무리.

---

## G-3. 마무리 — 커밋 & 푸시 (Step 3/3)

⏸ **사용자 승인 필요**: 다음 보고 후 응답 받기:

1. 변경된 파일 목록 (`git status`)
2. G-1 ~ G-2 작업 요약
3. 검증 결과
4. 커밋 메시지 제안:

   ```
   feat: 학생용 사용 설명서 추가 (guide.html)

   - 시안 A 톤(Toss/Notion 모던)으로 통일된 정중한 어투의 가이드 페이지
   - 본 사이트 헤더에 "사용 설명서" 진입 버튼 추가
   - PC·모바일 반응형 + 인쇄 출력 대응
   - 독립 링크로 학생들에게 직접 공유 가능
   ```

사용자 승인 시:

1. `git add -A && git commit -m "..." && git push origin main`
2. WORK_LOG.md에 푸시 시각·커밋 해시 기록
3. 사용자에게 다음 안내:
   - 본 사이트 URL: `https://curricenterhscne.github.io/course_selector_cne/`
   - 가이드 직접 링크: `https://curricenterhscne.github.io/course_selector_cne/guide.html`
   - 1~2분 후 배포 반영
   - 아래 자가 테스트 체크리스트 제시

---

## 자가 테스트 체크리스트 (사용자가 직접)

배포 사이트에서 다음 확인:

### 데스크탑
- [ ] 본 사이트 헤더에 사용 설명서 진입 버튼이 잘 보임
- [ ] 버튼 클릭 시 `guide.html`로 이동
- [ ] 가이드 페이지 디자인이 본 사이트와 일관됨 (보라색·Pretendard·모던 톤)
- [ ] FAQ 클릭 시 답변 펼침/접힘 정상
- [ ] "실습으로 돌아가기" 버튼 동작
- [ ] "과목 선택 실습 시작하기" CTA 버튼 동작

### 모바일
- [ ] 헤더에 사용 설명서 아이콘이 다른 아이콘들과 자연스럽게 배치
- [ ] 가이드 페이지가 모바일에서 깨지지 않고 읽기 좋음
- [ ] FAQ 펼침/접힘 정상

### 독립 링크
- [ ] `https://curricenterhscne.github.io/course_selector_cne/guide.html` 직접
  접속 시 정상 로드
- [ ] 학생에게 카톡 등으로 보낼 때 미리보기 정상 (description 메타 태그 작동)

### 인쇄
- [ ] PDF 출력 미리보기에서 깔끔하게 보임 (FAQ 모두 펼쳐진 상태로 출력)
- [ ] 상단 네비·하단 CTA는 인쇄에서 숨겨짐

⏸ **사용자 확인 필요**: 모두 통과해야 작업 완료. 문제 있으면 해당 단계로 돌아가
수정.
