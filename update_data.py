#!/usr/bin/env python3
"""
편제표 데이터 갱신 스크립트 (extract_data.py 대체)

사용법:
  python3 update_data.py                   # 알려진 모든 연도 갱신
  python3 update_data.py --year 2026       # 특정 연도만 갱신
  python3 update_data.py --year 2027       # 신규 연도 추가 (index.html 자동 패치)
  python3 update_data.py --dry-run         # 변경사항 미리보기만 (파일 쓰기 없음)
  python3 update_data.py --year 2026 --dry-run

요구 패키지:
  pip install pandas openpyxl
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = Path(__file__).parent
UPLOADS = HERE / 'uploads' if (HERE / 'uploads').exists() else HERE
OUT = HERE / 'data'

# ── 알려진 연도 목록 (신규 연도 추가 시 자동 감지됨) ──────────────────────
KNOWN_YEARS = ['2025', '2026']

# ─────────────────────────────────────────────────────────────────────────────
# 유틸
# ─────────────────────────────────────────────────────────────────────────────

def find_xlsx(year: str) -> Path:
    """파일명 NFC/NFD 차이를 흡수해서 xlsx 파일을 찾음"""
    patterns = [
        f'{year}학년도 고등학교 입학생 3개년 교육과정 편제표(입력용).xlsx',
        f'{year}학년도_고등학교_입학생_3개년_교육과정_편제표_입력용_.xlsx',
    ]
    for f in UPLOADS.iterdir():
        fname_nfc = unicodedata.normalize('NFC', f.name)
        for pat in patterns:
            if fname_nfc == unicodedata.normalize('NFC', pat):
                return f
    raise FileNotFoundError(
        f"[{year}] xlsx 파일을 찾지 못했습니다.\n"
        f"  찾는 곳: {UPLOADS}\n"
        f"  파일명 예시: {patterns[0]}"
    )


def load_existing_json(year_dir: Path) -> dict:
    """기존 data/curriculum_YYYY/*.json 을 {코드: data} 로 로드"""
    result = {}
    if not year_dir.exists():
        return result
    for f in year_dir.glob('*.json'):
        try:
            result[f.stem] = json.loads(f.read_text(encoding='utf-8'))
        except Exception:
            pass
    return result


def jsondiff_summary(old: dict, new: dict) -> str:
    """두 dict가 다르면 차이 요약 문자열 반환"""
    old_groups = len(old.get('groups', []))
    new_groups = len(new.get('groups', []))
    if old_groups != new_groups:
        return f"groups {old_groups}→{new_groups}개"
    old_subj = sum(len(g.get('subjects', [])) for g in old.get('groups', []))
    new_subj = sum(len(g.get('subjects', [])) for g in new.get('groups', []))
    if old_subj != new_subj:
        return f"subjects {old_subj}→{new_subj}개"
    return "내용 변경"


def validate_curriculum(code: str, data: dict) -> list:
    """편제표 데이터 구조 검증. 문제 목록 반환 (빈 리스트 = 정상)"""
    issues = []
    if not isinstance(data.get('groups'), list):
        issues.append('groups 배열 없음')
        return issues
    for gi, g in enumerate(data['groups']):
        if not isinstance(g.get('subjects'), list):
            issues.append(f'groups[{gi}] subjects 없음')
            continue
        for si, s in enumerate(g['subjects']):
            if not s.get('name'):
                issues.append(f'groups[{gi}].subjects[{si}] 이름 공백')
            has_credits = (
                (isinstance(s.get('semCredits'), list) and len(s['semCredits']) == 6)
                or s.get('opCredit') or g.get('groupCredit') or s.get('basic')
            )
            if not has_credits:
                issues.append(f'groups[{gi}].subjects[{si}] ({s.get("name","?")}) 학점 정보 없음')
    return issues


# ─────────────────────────────────────────────────────────────────────────────
# 핵심 추출 함수
# ─────────────────────────────────────────────────────────────────────────────

def extract_year(year: str, xlsx_path: Path, dry_run: bool) -> dict:
    """
    단일 연도 추출. 반환: {
      'added': [...코드],
      'changed': [...(코드, 요약)],
      'removed': [...코드],
      'unchanged': int,
      'errors': [...(코드, 에러)],
      'validation_issues': {...코드: [이슈]},
    }
    """
    year_dir = OUT / f'curriculum_{year}'
    existing = load_existing_json(year_dir)

    print(f"\n  xlsx 읽는 중... ({xlsx_path.name})")
    data_df = pd.read_excel(xlsx_path, sheet_name='Data', header=0)
    data_df.columns = [str(c).strip() for c in data_df.columns]

    new_data = {}   # {코드: parsed_json}
    parse_errors = []

    for _, row in data_df.iterrows():
        code = row.get('학교코드')
        json_str = row.get('편제표JSON')
        if pd.isna(code) or pd.isna(json_str):
            continue
        code_str = str(code).strip()
        try:
            new_data[code_str] = json.loads(json_str)
        except json.JSONDecodeError as e:
            parse_errors.append((code_str, str(e)))

    # ── diff 계산 ──
    existing_codes = set(existing.keys())
    new_codes = set(new_data.keys())

    added = sorted(new_codes - existing_codes)
    removed = sorted(existing_codes - new_codes)
    changed = []
    unchanged = 0

    for code in sorted(new_codes & existing_codes):
        if json.dumps(new_data[code], sort_keys=True) != json.dumps(existing[code], sort_keys=True):
            changed.append((code, jsondiff_summary(existing[code], new_data[code])))
        else:
            unchanged += 1

    # ── 검증 ──
    validation_issues = {}
    for code, data in new_data.items():
        issues = validate_curriculum(code, data)
        if issues:
            validation_issues[code] = issues

    # ── 파일 쓰기 ──
    if not dry_run:
        year_dir.mkdir(exist_ok=True)
        # 추가/변경만 씀 (제거된 파일은 수동 확인 후 삭제)
        for code in added + [c for c, _ in changed]:
            path = year_dir / f'{code}.json'
            path.write_text(json.dumps(new_data[code], ensure_ascii=False), encoding='utf-8')
        # 인덱스 갱신
        index = {}
        for _, row in data_df.iterrows():
            code = row.get('학교코드')
            json_str = row.get('편제표JSON')
            if pd.isna(code) or pd.isna(json_str):
                continue
            code_str = str(code).strip()
            if code_str in new_data:
                index[code_str] = {'updated': str(row.get('수정일시', '')), 'size': len(str(json_str))}
        (OUT / f'curriculum_{year}_index.json').write_text(
            json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8'
        )

    return {
        'added': added,
        'changed': changed,
        'removed': removed,
        'unchanged': unchanged,
        'errors': parse_errors,
        'validation_issues': validation_issues,
        'new_data': new_data,  # schools.json 갱신용
    }


def extract_schools_and_coursedb(xlsx_path: Path, dry_run: bool, all_years_data: dict):
    """
    schools.json + courseDB.json 갱신.
    all_years_data: {year: extract_year 결과}
    """
    print(f"\n  Schools / CourseDB 읽는 중...")

    # Schools (2026 기준)
    schools_df = pd.read_excel(xlsx_path, sheet_name='Schools', header=0)
    schools_df.columns = [str(c).strip() for c in schools_df.columns]
    schools = schools_df[['학교코드', '학교명', '1학년학급수', '2학년학급수', '3학년학급수', '지역']].copy()
    schools = schools.dropna(subset=['학교코드', '학교명'])
    schools_list = schools.to_dict('records')

    # departments 인덱스 부착
    dept_pattern = re.compile(r'^(N\d+)\(([^)]+)\)$')
    for year in all_years_data:
        year_dir = OUT / f'curriculum_{year}'
        depts_by_base = defaultdict(list)
        if year_dir.exists():
            for p in year_dir.glob('*.json'):
                m = dept_pattern.match(p.stem)
                if m:
                    depts_by_base[m.group(1)].append({'dept': m.group(2), 'code': p.stem})
        # 신규 추출 데이터에서도 반영
        result = all_years_data[year]
        for code in result.get('new_data', {}):
            m = dept_pattern.match(code)
            if m:
                base, dept = m.group(1), m.group(2)
                existing_depts = [d['code'] for d in depts_by_base[base]]
                if code not in existing_depts:
                    depts_by_base[base].append({'dept': dept, 'code': code})
        for s in schools_list:
            base = s['학교코드']
            depts = depts_by_base.get(base, [])
            s[f'departments_{year}'] = sorted(depts, key=lambda d: d['dept']) if depts else None

    # CourseDB
    course_df = pd.read_excel(xlsx_path, sheet_name='CourseDB', header=0)
    course_df.columns = [str(c).strip() for c in course_df.columns]
    course_df = course_df.dropna(subset=['과목명'])
    course_list = course_df.fillna('').to_dict('records')

    if not dry_run:
        (OUT / 'schools.json').write_text(
            json.dumps(schools_list, ensure_ascii=False, indent=2), encoding='utf-8'
        )
        (OUT / 'courseDB.json').write_text(
            json.dumps(course_list, ensure_ascii=False, indent=2), encoding='utf-8'
        )

    return len(schools_list), len(course_list)


# ─────────────────────────────────────────────────────────────────────────────
# index.html 패치 (신규 연도 추가 시)
# ─────────────────────────────────────────────────────────────────────────────

def patch_index_html(new_year: str, dry_run: bool) -> bool:
    """
    index.html에 신규 연도 year-pill 버튼 추가.
    반환: True = 패치 성공, False = 이미 존재하거나 실패
    """
    html_path = HERE / 'index.html'
    html = html_path.read_text(encoding='utf-8')

    # 이미 있으면 스킵
    if f'data-year="{new_year}"' in html:
        print(f"\n  index.html: {new_year} 버튼 이미 존재, 스킵")
        return False

    # 마지막 year-pill 버튼 뒤에 새 버튼 삽입
    pattern = r'(<button class="year-pill(?:\s+active)?" data-year="\d{4}">\d{4}</button>)(?=\s*</div>)'
    last_pill = None
    for m in re.finditer(r'<button class="year-pill(?:\s+active)?" data-year="\d{4}">\d{4}</button>', html):
        last_pill = m

    if not last_pill:
        print(f"\n  ⚠ index.html: year-pill 버튼을 찾지 못했습니다. 수동으로 추가하세요.")
        print(f'  추가할 내용: <button class="year-pill" data-year="{new_year}">{new_year}</button>')
        return False

    insert_pos = last_pill.end()
    new_button = f'\n    <button class="year-pill" data-year="{new_year}">{new_year}</button>'
    patched = html[:insert_pos] + new_button + html[insert_pos:]

    if not dry_run:
        html_path.write_text(patched, encoding='utf-8')
        print(f"\n  index.html: {new_year} 버튼 추가 완료 (기존 마지막 pill 뒤)")
    else:
        print(f"\n  [dry-run] index.html에 추가될 버튼: {new_button.strip()}")

    return True


# ─────────────────────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='편제표 데이터 갱신 스크립트')
    parser.add_argument('--year', metavar='YYYY', help='처리할 연도 (생략 시 전체 연도)')
    parser.add_argument('--dry-run', action='store_true', help='변경사항 미리보기만 (파일 쓰기 없음)')
    args = parser.parse_args()

    dry_run = args.dry_run
    if dry_run:
        print("── DRY-RUN 모드: 파일을 실제로 쓰지 않습니다 ──")

    OUT.mkdir(exist_ok=True)

    # 처리 연도 결정
    if args.year:
        target_years = [args.year]
        is_new_year = args.year not in KNOWN_YEARS
        if is_new_year:
            print(f"\n★ 신규 연도 감지: {args.year}")
    else:
        target_years = KNOWN_YEARS
        is_new_year = False

    # xlsx 파일 탐색
    xlsx_files = {}
    missing = []
    for year in target_years:
        try:
            xlsx_files[year] = find_xlsx(year)
            print(f"  [{year}] xlsx 확인: {xlsx_files[year].name}")
        except FileNotFoundError as e:
            print(f"  [{year}] ✗ {e}")
            missing.append(year)

    if missing:
        sys.exit(1)

    # 연도별 추출
    all_results = {}
    for year in target_years:
        print(f"\n{'─'*50}")
        print(f"  {year}학년도 처리 중")
        print(f"{'─'*50}")
        result = extract_year(year, xlsx_files[year], dry_run)
        all_results[year] = result

        # 결과 출력
        added = result['added']
        changed = result['changed']
        removed = result['removed']
        unchanged = result['unchanged']
        errors = result['errors']
        issues = result['validation_issues']

        print(f"\n  변경 요약:")
        print(f"    신규: {len(added)}개  |  변경: {len(changed)}개  |"
              f"  삭제: {len(removed)}개  |  동일: {unchanged}개")

        if added:
            print(f"\n  [신규 학교]")
            for c in added:
                print(f"    + {c}")

        if changed:
            print(f"\n  [변경된 학교]")
            for c, summary in changed:
                print(f"    ~ {c}  ({summary})")

        if removed:
            print(f"\n  [xlsx에서 사라진 학교] ← 수동 확인 필요, 파일 자동 삭제 안 함")
            for c in removed:
                print(f"    - {c}")

        if errors:
            print(f"\n  [JSON 파싱 오류]")
            for c, e in errors:
                print(f"    ✗ {c}: {e}")

        if issues:
            print(f"\n  [데이터 품질 경고]")
            for c, iss in issues.items():
                for i in iss:
                    print(f"    [!] {c}: {i}")

    # schools.json / courseDB.json 갱신 (가장 최신 연도의 xlsx 기준)
    latest_year = max(target_years)
    print(f"\n{'─'*50}")
    print(f"  schools.json / courseDB.json 갱신 ({latest_year} 기준)")
    print(f"{'─'*50}")
    n_schools, n_courses = extract_schools_and_coursedb(
        xlsx_files[latest_year], dry_run, all_results
    )
    if not dry_run:
        print(f"  schools.json: {n_schools}개교")
        print(f"  courseDB.json: {n_courses}개 과목")

    # 신규 연도 index.html 패치
    if is_new_year and args.year:
        print(f"\n{'─'*50}")
        print(f"  index.html 패치")
        print(f"{'─'*50}")
        patch_index_html(args.year, dry_run)

    # 최종 요약
    print(f"\n{'='*50}")
    print(f"  완료")
    print(f"{'='*50}")

    total_changed = sum(
        len(r['added']) + len(r['changed']) for r in all_results.values()
    )

    if dry_run:
        print(f"\n  [dry-run] 실제 적용하려면 --dry-run 없이 다시 실행하세요.")
    elif total_changed == 0 and not is_new_year:
        print(f"\n  변경 없음. 커밋할 필요 없습니다.")
    else:
        print(f"\n  다음 단계:")
        changed_files = []
        for year in target_years:
            r = all_results[year]
            for c in r['added'] + [c for c, _ in r['changed']]:
                changed_files.append(f"data/curriculum_{year}/{c}.json")
        changed_files += ['data/schools.json', 'data/courseDB.json']
        for year in target_years:
            changed_files.append(f"data/curriculum_{year}_index.json")
        if is_new_year:
            changed_files.append('index.html')

        print(f"\n  git add {' '.join(changed_files[:3])}{'  ...' if len(changed_files) > 3 else ''}")
        print(f"  또는: git add data/ {'index.html' if is_new_year else ''}")
        commit_year = args.year or '+'.join(target_years)
        print(f"  git commit -m \"data: {commit_year}학년도 편제표 갱신\"")
        print(f"  git push origin main")


if __name__ == '__main__':
    main()
