"""
충남 고교 편제표 xlsx → JSON 번들 추출

사용법:
1. 이 스크립트와 같은 폴더에 xlsx 두 파일을 둔다 (또는 uploads/ 폴더에).
2. python3 extract_data.py
3. data/ 폴더가 생성됨. 그대로 git에 커밋하면 됨.

요구 패키지: pandas, openpyxl
  pip install pandas openpyxl
"""
import json
import re
import unicodedata
import pandas as pd
from pathlib import Path
from collections import defaultdict

# 스크립트 위치 기준 상대 경로
HERE = Path(__file__).parent
UPLOADS = HERE / 'uploads' if (HERE / 'uploads').exists() else HERE
OUT = HERE / 'data'
OUT.mkdir(exist_ok=True)


def find_xlsx(year):
    """파일명 NFC/NFD 차이를 흡수해서 xlsx 파일을 찾음 (macOS·Linux 호환)"""
    target = unicodedata.normalize('NFC', f'{year}학년도_고등학교_입학생_3개년_교육과정_편제표_입력용_.xlsx')
    for f in UPLOADS.iterdir():
        if unicodedata.normalize('NFC', f.name) == target:
            return f
    raise FileNotFoundError(
        f"[{year}] 파일을 찾지 못했습니다.\n"
        f"  찾는 곳: {UPLOADS}\n"
        f"  찾는 이름: {target}\n"
        f"xlsx 파일을 이 스크립트와 같은 폴더 또는 uploads/ 폴더에 두세요."
    )


FILES = {'2025': find_xlsx('2025'), '2026': find_xlsx('2026')}

# ---------- Schools ----------
schools_2026 = pd.read_excel(FILES['2026'], sheet_name='Schools', header=0)
schools_2026.columns = [str(c).strip() for c in schools_2026.columns]
# 공개 사이트에 노출 불필요한 '담당자연락처' 필드는 제외
schools = schools_2026[['학교코드', '학교명', '1학년학급수', '2학년학급수', '3학년학급수', '지역']].copy()
schools = schools.dropna(subset=['학교코드', '학교명'])
schools_list = schools.to_dict('records')
(OUT / 'schools.json').write_text(
    json.dumps(schools_list, ensure_ascii=False, indent=2), encoding='utf-8'
)
print(f"schools.json: {len(schools_list)}개교")

# ---------- Curriculum (Data sheet) ----------
school_codes_in_data = {'2025': set(), '2026': set()}
for year, path in FILES.items():
    year_dir = OUT / f'curriculum_{year}'
    year_dir.mkdir(exist_ok=True)
    data_df = pd.read_excel(path, sheet_name='Data', header=0)
    data_df.columns = [str(c).strip() for c in data_df.columns]
    index = {}
    skipped = 0
    for _, row in data_df.iterrows():
        code = row.get('학교코드')
        json_str = row.get('편제표JSON')
        if pd.isna(code) or pd.isna(json_str):
            skipped += 1
            continue
        try:
            data = json.loads(json_str)
            code_str = str(code).strip()
            (year_dir / f'{code_str}.json').write_text(
                json.dumps(data, ensure_ascii=False), encoding='utf-8'
            )
            index[code_str] = {
                'updated': str(row.get('수정일시', '')),
                'size': len(json_str),
            }
            school_codes_in_data[year].add(code_str)
        except json.JSONDecodeError as e:
            print(f"  [{year}] JSON 파싱 실패 {code}: {e}")
            skipped += 1
    (OUT / f'curriculum_{year}_index.json').write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(f"curriculum_{year}/: {len(index)}개교 분리 저장 (skipped {skipped})")

# Schools 시트에 없지만 Data 시트에 있는 학교 확인 (특목고 등)
schools_codes = set(str(c).strip() for c in schools['학교코드'])
extra_2026 = school_codes_in_data['2026'] - schools_codes
print(f"\nSchools 시트에 없지만 2026 Data에 있는 학교: {len(extra_2026)}개")
if extra_2026:
    print(f"  코드 예시: {list(extra_2026)[:5]}")

# ---------- CourseDB ----------
course_df = pd.read_excel(FILES['2026'], sheet_name='CourseDB', header=0)
course_df.columns = [str(c).strip() for c in course_df.columns]
course_df = course_df.dropna(subset=['과목명'])
course_list = course_df.fillna('').to_dict('records')
(OUT / 'courseDB.json').write_text(
    json.dumps(course_list, ensure_ascii=False, indent=2), encoding='utf-8'
)
print(f"courseDB.json: {len(course_list)}개 과목")

# ---------- 학과 인덱스를 schools.json에 추가 ----------
dept_pattern = re.compile(r'^(N\d+)\(([^)]+)\)$')

for year in ['2025', '2026']:
    depts_by_base = defaultdict(list)
    year_dir = OUT / f'curriculum_{year}'
    for p in year_dir.glob('*.json'):
        code = p.stem
        m = dept_pattern.match(code)
        if m:
            base, dept = m.group(1), m.group(2)
            depts_by_base[base].append({'dept': dept, 'code': code})
    for s in schools_list:
        base = s['학교코드']
        depts = depts_by_base.get(base, [])
        s[f'departments_{year}'] = sorted(depts, key=lambda d: d['dept']) if depts else None

# schools.json 갱신본 저장
(OUT / 'schools.json').write_text(
    json.dumps(schools_list, ensure_ascii=False, indent=2), encoding='utf-8'
)
print(f"\nschools.json에 departments_2025/2026 인덱스 부착 완료")

# ---------- 파일 크기 확인 ----------
print("\n--- 파일 크기 ---")
for f in sorted(OUT.glob('*.json')):
    print(f"  {f.name}: {f.stat().st_size/1024:.1f} KB")
