# 꾸꾸클럽 캐릭터 자산

디자이너가 그린 **원본 캐릭터**를 `꾸꾸클럽.ai`(Adobe Illustrator, PDF 1.5 호환)에서
**벡터 그대로** 추출한 자산입니다. 코드로 재현한 것이 아니라 디자이너의 실제 손그림 패스를
보존하고 있습니다.

## 파일 목록

| 파일 | 캐릭터 | 비고 |
|---|---|---|
| `characters/paenkkumi.svg` | 팬꾸미 (곰/판다) | 메인 · 무덤덤·성실형 · 헤더 마스코트 권장 |
| `characters/tokkumi.svg` | 토꾸미 (토끼) | 메인 · 갓생형 · 히어로/빈 상태 권장 |
| `characters/kkumi.svg` | 꾸미 (애벌레) | 서브 · 작은 장식·로딩 |
| `characters/kkukkuk-club-logo.svg` | 단체 + "꾸꾸클럽" 워드마크 | 로고·푸터 |
| `characters/png/*.png` | 위 4종의 1024~1600px 투명 PNG | SVG 못 쓰는 곳(PPT/인쇄/SNS)용 |

모두 **투명 배경**입니다. 흰 바디라 어떤 배경색 위에도 올라갑니다.

> `kkuk-characters-codegen-DEPRECATED.svg` 는 초기에 코드로 재현했던 버전입니다.
> 이제 위 원본을 쓰므로 사용하지 마세요. (참고용으로만 보관)

## 사용법

### 가장 간단한 방법 — img 태그 (대부분의 경우 권장)
```html
<img src="assets/characters/tokkumi.svg" alt="토꾸미" style="height:120px">
```

### 헤더 마스코트
```html
<span class="kk-header__mascot" style="padding:2px;">
  <img src="assets/characters/paenkkumi.svg" alt="팬꾸미" style="width:100%;height:100%;object-fit:contain;">
</span>
```

### 빈 상태
```html
<div class="kk-empty">
  <img src="assets/characters/tokkumi.svg" alt="" style="height:140px">
  <h3 class="kk-empty__title">아직 선택한 과목이 없어요</h3>
  ...
</div>
```

실제 적용 예시는 `characters-guide.html`을 브라우저로 열어 확인하세요.

## 주의사항

- **어두운 배경 주의**: 캐릭터 윤곽선이 검정이라 진블루(`blue-500`)처럼 어두운 배경 위에선
  묻힐 수 있습니다. 어두운 배경엔 라이트블루/크림/흰색 위에 올리거나, 캐릭터를 흰 카드 안에 넣으세요.
- **최소 크기**: 너무 작게(높이 40px 미만) 쓰면 디테일이 뭉갭니다.
- **비율 유지**: `width`/`height` 중 하나만 지정하고 다른 쪽은 auto로 두어 비율을 유지하세요.
- **색 변경**: 이 SVG는 디자이너 원본 색(검정 윤곽 + 블루 도트 코)이 내장되어 있어 `currentColor`로
  통째 색을 바꾸는 방식은 지원하지 않습니다. 색을 바꿔야 하면 디자이너에게 변형본을 요청하세요.

## 더 필요한 자산이 있다면

원본 `.ai`에는 이 외에도 **표정 변형(캐릭터당 3종씩 9개), 턴어라운드(4방향), 활용 포즈,
4컷 만화** 등이 더 있습니다(자료집 PDF 6~18쪽). 필요해지면 같은 방식으로 추출할 수 있으니
요청하세요. 추출 시 페이지 번호와 원하는 표정/포즈를 알려주시면 됩니다.

추출 방법(기록용): `pdftocairo -svg -f <쪽> -l <쪽> 꾸꾸클럽.ai out.svg` 로 벡터 SVG를 뽑은 뒤,
풀페이지 배경 path를 제거하고 캐릭터 영역으로 viewBox를 크롭, 좌표 정밀도를 2자리로 최적화.
