from pathlib import Path
import re
import json

ROOT = Path(r'D:\Projects\bazi-portal')
md_path = next(Path(r'D:\Projects\bazi-name-options').glob('*.md'))
text = md_path.read_text(encoding='utf-8')

sections = {'男': {}, '女': {}}
gender = None
pattern = None

def normalize_pattern(s: str) -> str:
    s = s.strip()
    s = s.replace('男孩名字', '').replace('女孩名字', '').replace('男孩名', '').replace('女孩名', '')
    s = s.replace('（', '(').replace('）', ')')
    s = re.sub(r'\(.*?\)', '', s).strip()
    return s

for line in text.splitlines():
    line = line.strip()
    if line.startswith('# 男孩名字库'):
        gender = '男'
        continue
    if line.startswith('# 女孩名字库'):
        gender = '女'
        continue
    m = re.match(r'##\s+\d+\.\s+(.+)', line)
    if m and gender:
        pattern = normalize_pattern(m.group(1))
        sections[gender].setdefault(pattern, [])
        continue
    if line.startswith('|') and gender and pattern and not line.startswith('| 序号') and not line.startswith('|---'):
        parts = [p.strip() for p in line.strip('|').split('|')]
        if len(parts) >= 5:
            try:
                idx = int(parts[0])
            except ValueError:
                continue
            sections[gender][pattern].append({
                'index': idx,
                'name': parts[1],
                'pinyin': parts[2],
                'grade': parts[3],
                'note': parts[4],
            })

patterns = ['火格', '土格', '木火格', '水火格', '火土格', '金火格']
directions = {
    '火格': '偏木',
    '土格': '偏木/水',
    '木火格': '偏木/土',
    '水火格': '偏木',
    '火土格': '偏木',
    '金火格': '偏水/木',
}

# Fallback for source titles that may vary slightly
all_patterns = set(sections['男'].keys()) | set(sections['女'].keys())
for p in list(all_patterns):
    if p not in patterns:
        for std in patterns:
            if std.replace('格','') in p.replace('格','') or p.replace('格','') in std.replace('格',''):
                sections['男'][std] = sections['男'].get(std, sections['男'].get(p, []))
                sections['女'][std] = sections['女'].get(std, sections['女'].get(p, []))

payload = {p: {'boys': sections['男'].get(p, []), 'girls': sections['女'].get(p, [])} for p in patterns}

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>名字推荐</title>
<style>
:root{{--bg:#0f172a;--bg2:#172554;--panel:rgba(255,255,255,.08);--line:rgba(255,255,255,.12);--text:#eff6ff;--muted:#cbd5e1;--male:#60a5fa;--female:#f9a8d4;--shadow:0 18px 40px rgba(0,0,0,.22)}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}body{{font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:linear-gradient(180deg,var(--bg),var(--bg2));color:var(--text)}}
a{{color:inherit;text-decoration:none}}.wrap{{max-width:1200px;margin:0 auto;padding:16px}}
.hero{{position:sticky;top:0;z-index:60;padding:14px 16px 16px;border-radius:24px 24px 0 0;background:rgba(15,23,42,.96);backdrop-filter:blur(16px);box-shadow:var(--shadow);transition:.25s ease all;overflow:hidden}}
.hero.compact{{border-radius:0;margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);width:100vw}}
.hero::before{{content:'';position:absolute;inset:0;background:rgba(15,23,42,.98);z-index:-1}}
.hero h1{{margin:0 0 12px;text-align:center;font-size:24px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.top-actions{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}}
.btn{{display:flex;align-items:center;justify-content:center;padding:10px 6px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.08);font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}}
.btn.active{{background:rgba(255,255,255,.18)}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}}
.card{{background:rgba(255,255,255,.08);border:1px solid var(--line);border-radius:24px;padding:18px;box-shadow:var(--shadow)}}
.pattern-head{{position:relative;display:flex;align-items:center;justify-content:center;min-height:72px;margin-bottom:12px}}
.pattern-title{{font-size:44px;font-weight:900;line-height:1}}
.pattern-left,.pattern-right{{position:absolute;top:0;font-size:12px;color:var(--muted)}}.pattern-left{{left:0}}.pattern-right{{right:0}}
.name-item{{margin-top:12px;padding:14px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}}
.name-top{{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}}.name-main{{font-size:32px;font-weight:800}}.pinyin{{font-size:12px;color:var(--muted);margin-top:4px}}.grade{{font-size:14px;color:#fde68a;font-weight:700}}
.note{{margin-top:8px;font-size:14px;line-height:1.7;color:#e2e8f0}}
body.theme-female{{background:linear-gradient(180deg,#3b0764,#831843)}}
body.theme-female .hero::before{{background:rgba(58,7,100,.98)}}
body.theme-female .btn.active{{background:rgba(255,255,255,.2)}}
body.theme-female .pattern-title, body.theme-female .name-main{{color:#ffe4f1}}
body.theme-male .pattern-title, body.theme-male .name-main{{color:#dbeafe}}
@media (max-width:720px){{.wrap{{padding:10px}}.hero{{padding:12px 10px 14px}}.hero.compact{{padding:12px 8px 14px}}.hero h1{{font-size:20px}}.top-actions{{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}}.btn{{padding:9px 4px;font-size:12px}}.grid{{grid-template-columns:1fr;gap:12px}}.pattern-title{{font-size:40px}}.name-main{{font-size:28px}}}}
</style>
</head>
<body class="theme-male">
<div class="wrap">
  <section class="hero" id="hero">
    <h1>名字推荐</h1>
    <div class="top-actions">
      <button class="btn active" id="maleBtn">男孩</button>
      <button class="btn" id="femaleBtn">女孩</button>
      <a class="btn" href="index.html">返回首页</a>
      <a class="btn" href="bazi-analysis.html">八字分析</a>
    </div>
  </section>
  <section class="grid" id="grid"></section>
</div>
<script>
const DATA = {json.dumps(payload, ensure_ascii=False)};
const DIRECTIONS = {json.dumps(directions, ensure_ascii=False)};
const PATTERNS = {json.dumps(patterns, ensure_ascii=False)};
let currentGender = '男';
const genderScrollMemory = {{ 男: null, 女: null }};
const hero = document.getElementById('hero');
const grid = document.getElementById('grid');
const maleBtn = document.getElementById('maleBtn');
const femaleBtn = document.getElementById('femaleBtn');
function render(){{
  grid.innerHTML = PATTERNS.map(p => {{
    const list = currentGender === '男' ? (DATA[p]?.boys || []) : (DATA[p]?.girls || []);
    return `<article class="card" id="${{p}}">
      <div class="pattern-head">
        <div class="pattern-left">${{DIRECTIONS[p] || ''}}</div>
        <div class="pattern-title">${{p}}</div>
        <div class="pattern-right">${{list.length}}个名字</div>
      </div>
      ${{list.map(r => `<div class="name-item">
        <div class="name-top"><div><div class="name-main">${{r.name}}</div><div class="pinyin">${{r.pinyin}}</div></div><div class="grade">${{r.grade}}</div></div>
        <div class="note">${{r.note}}</div>
      </div>`).join('')}}
    </article>`;
  }}).join('');
}}
function syncButtons(){{
  maleBtn.classList.toggle('active', currentGender === '男');
  femaleBtn.classList.toggle('active', currentGender === '女');
  document.body.className = currentGender === '男' ? 'theme-male' : 'theme-female';
}}
function setGender(nextGender){{
  if (nextGender === currentGender) return;
  genderScrollMemory[currentGender] = window.scrollY;
  currentGender = nextGender;
  syncButtons();
  render();
  requestAnimationFrame(() => window.scrollTo(0, genderScrollMemory[nextGender] ?? 0));
}}
function updateSticky(){{ hero.classList.toggle('compact', window.scrollY > 18); }}
maleBtn.onclick = () => setGender('男');
femaleBtn.onclick = () => setGender('女');
window.addEventListener('scroll', updateSticky, {{passive:true}});
window.addEventListener('resize', updateSticky);
syncButtons(); render(); updateSticky();
</script>
</body>
</html>'''

(ROOT / 'names.html').write_text(html, encoding='utf-8')
print('restored names.html')
