from pathlib import Path
import json, re
from collections import defaultdict

DRAFT = Path(r'D:\Projects\bazi-name-options\白姓-2026年9月-六格局名字库-720名字草案-待确认.md')
NAMES_HTML = Path(r'D:\Projects\bazi-portal\names.html')
BAZI_HTML = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')

pattern_order = ['火格','土格','木火格','水火格','火土格','金火格']

def parse_md():
    data = defaultdict(lambda: defaultdict(list))
    gender = None
    pattern = None
    for line in DRAFT.read_text(encoding='utf-8').splitlines():
        if line.startswith('# 男孩名字库'):
            gender = '男'; continue
        if line.startswith('# 女孩名字库'):
            gender = '女'; continue
        m = re.match(r'##\s+\d+\.\s+(.+?)(男孩名|女孩名)', line)
        if m:
            pattern = m.group(1).strip(); continue
        if line.startswith('| ') and not line.startswith('| 序号') and not line.startswith('|---'):
            p = [x.strip() for x in line.strip('|').split('|')]
            if len(p) >= 9 and gender and pattern:
                score = float(p[3])
                row = {
                    'index': int(p[0]),
                    'name': p[1],
                    'pinyin': p[2],
                    'score': score,
                    'wuxing': p[5],
                    'meaning': p[6],
                    'source': p[7],
                    'reason': p[8],
                }
                key = 'boys' if gender == '男' else 'girls'
                data[pattern][key].append(row)
    return {p:{'boys': data[p]['boys'], 'girls': data[p]['girls']} for p in pattern_order}

def replace_names_html(text, payload):
    new_json = json.dumps(payload, ensure_ascii=False)
    text, count = re.subn(r'const topData=\{.*?\};\s*const patternDirection=', f'const topData={new_json}; const patternDirection=', text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError('names.html topData replace failed')
    return text

def replace_bazi_html(text, payload):
    new_json = json.dumps(payload, ensure_ascii=False)
    text, count = re.subn(r'const topData=\{.*?\};\s*const counts=', f'const topData={new_json}; const counts=', text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError('bazi-analysis.html topData replace failed')
    return text

payload = parse_md()

names_text = NAMES_HTML.read_text(encoding='utf-8', errors='ignore')
names_text = replace_names_html(names_text, payload)
NAMES_HTML.write_text(names_text, encoding='utf-8')

bazi_text = BAZI_HTML.read_text(encoding='utf-8', errors='ignore')
bazi_text = replace_bazi_html(bazi_text, payload)
BAZI_HTML.write_text(bazi_text, encoding='utf-8')

print('updated names.html and bazi-analysis.html with 720-name payload')
