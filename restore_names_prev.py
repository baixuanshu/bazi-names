from pathlib import Path
import re
import json

ROOT = Path(r'D:\Projects\bazi-portal')
md_path = next(Path(r'D:\Projects\bazi-name-options').glob('*.md'))
text = md_path.read_text(encoding='utf-8')

sections = {'男': {}, '女': {}}
gender = None
pattern = None

patterns = ['火格', '土格', '木火格', '水火格', '火土格', '金火格']
directions = {
    '火格': '偏木',
    '土格': '偏木/水',
    '木火格': '偏木/土',
    '水火格': '偏木',
    '火土格': '偏木',
    '金火格': '偏水/木',
}

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

all_patterns = set(sections['男'].keys()) | set(sections['女'].keys())
for p in list(all_patterns):
    if p not in patterns:
        for std in patterns:
            if std.replace('格','') in p.replace('格','') or p.replace('格','') in std.replace('格',''):
                if p in sections['男'] and std not in sections['男']:
                    sections['男'][std] = sections['男'][p]
                if p in sections['女'] and std not in sections['女']:
                    sections['女'][std] = sections['女'][p]

payload = {p: {'boys': sections['男'].get(p, []), 'girls': sections['女'].get(p, [])} for p in patterns}

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>名字推荐</title>
<style>
:root{{--bg:#0f1221;--bg2:#171b31;--text:#f4f7ff;--muted:#b8c2df;--line:rgba(255,255,255,.12);--shadow:0 20px 50px rgba(0,0,0,.28)}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{font-family:"SF Pro Text","PingFang SC","Microsoft YaHei",system-ui,sans-serif;font-weight:300;color:var(--text);overflow-x:hidden;letter-spacing:.1px;transition:background .45s ease,color .35s ease}}
body.theme-male{{background:radial-gradient(circle at top left, rgba(101,144,255,.18), transparent 24%), radial-gradient(circle at top right, rgba(246,203,120,.12), transparent 20%), linear-gradient(180deg,#09111f 0%,#0f1c34 46%,#172743 100%)}}
body.theme-female{{background:radial-gradient(circle at top left, rgba(255,205,226,.22), transparent 22%), radial-gradient(circle at top right, rgba(255,239,246,.18), transparent 22%), linear-gradient(180deg,#3a1830 0%,#5a2748 36%,#7f3e60 100%)}}
.wrap{{max-width:1440px;margin:0 auto;padding:20px}}
a{{text-decoration:none;color:inherit}}
.hero-sticky{{position:sticky;top:0;z-index:60;margin-bottom:14px;padding:20px 0 18px;border-radius:24px 24px 0 0;overflow:hidden;background:linear-gradient(180deg, rgba(33,41,67,.985) 0%, rgba(33,41,67,.965) 78%, rgba(33,41,67,0) 100%);backdrop-filter:blur(18px) saturate(110%);-webkit-backdrop-filter:blur(18px) saturate(110%);transition:padding .28s ease, box-shadow .28s ease, background .28s ease, border-radius .28s ease, margin .28s ease, width .28s ease;box-shadow:0 8px 22px rgba(0,0,0,.10)}}
.theme-female .hero-sticky{{background:linear-gradient(180deg, rgba(88,48,74,.985) 0%, rgba(88,48,74,.965) 78%, rgba(88,48,74,0) 100%)}}
.hero-sticky::before{{content:'';position:absolute;inset:0;background:rgba(28,39,69,.995);z-index:-1;transition:border-radius .28s ease}}
.theme-female .hero-sticky::before{{background:rgba(88,48,74,.995)}}
.hero-sticky.compact{{border-radius:0;padding:12px max(12px, env(safe-area-inset-right)) 14px max(12px, env(safe-area-inset-left));margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);width:100vw;box-shadow:0 8px 22px rgba(0,0,0,.10)}}
.hero-sticky.compact::before{{border-radius:0}}
.hero-topline{{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}}
.hero-topline h1{{margin:0 auto;font-size:24px;line-height:1.15;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}}
.hero-actions{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}}
.btn{{display:flex;align-items:center;justify-content:center;padding:10px 6px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.08);color:var(--text);font-size:13px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:transform .22s ease, background .22s ease, box-shadow .22s ease}}
.btn:hover{{transform:translateY(-2px);background:rgba(255,255,255,.12);box-shadow:0 10px 24px rgba(0,0,0,.14)}}
.btn.active{{background:rgba(255,255,255,.18)}}
.theme-female .btn.active{{background:rgba(255,255,255,.22)}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}}
.card{{padding:18px;position:relative;overflow:hidden;transition:transform .22s ease,border-color .22s ease,background .22s ease;background:rgba(255,255,255,.08);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow)}}
.card:hover{{transform:translateY(-4px);border-color:rgba(255,255,255,.22);background:rgba(255,255,255,.1)}}
.theme-male .card{{background:linear-gradient(180deg, rgba(14,24,44,.72), rgba(18,31,57,.62))}}
.theme-female .card{{background:linear-gradient(180deg, rgba(87,39,70,.50), rgba(126,61,97,.42))}}
.pattern-head{{display:flex;align-items:center;justify-content:center;position:relative;min-height:86px;margin-bottom:12px}}
.pattern-title{{font-size:52px;font-weight:900;line-height:1;letter-spacing:1px;text-align:center}}
.pattern-left,.pattern-right{{position:absolute;top:0;font-size:12px;color:var(--muted)}}
.pattern-left{{left:0}}.pattern-right{{right:0}}
.name-item{{padding:16px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);margin-top:12px;position:relative;overflow:hidden}}
.name-item::after{{content:'';position:absolute;right:-30px;top:-30px;width:100px;height:100px;background:radial-gradient(circle, rgba(255,255,255,.14), transparent 70%);opacity:.35}}
.name-top{{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap}}
.name-main{{font-family:"STXingkai","STLiti","LiSu","STKaiti","KaiTi",cursive,serif;font-size:40px;letter-spacing:1.2px;line-height:1.05;font-weight:800}}
.theme-female .name-main{{color:#fff1f7;text-shadow:0 2px 10px rgba(255,190,220,.22)}}
.theme-male .name-main{{color:#edf5ff;text-shadow:0 2px 12px rgba(120,162,255,.16)}}
.pinyin{{font-size:12px;color:var(--muted);margin-top:4px}}.grade{{font-size:14px;color:#b4ffd9;font-weight:700}}
.theme-female .grade{{color:#ffe2ee}}
.note{{margin-top:8px;font-size:14px;line-height:1.8;color:#eaf0ff}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr}}.wrap{{padding:14px}}.hero-topline h1{{font-size:22px}}}}
@media (max-width:720px){{.wrap{{padding:10px}}.hero-sticky{{padding:12px 0 10px;border-radius:24px 24px 0 0;overflow:hidden}}.hero-sticky.compact{{border-radius:0;padding:12px max(8px, env(safe-area-inset-right)) 14px max(8px, env(safe-area-inset-left));margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);width:100vw}}.hero-topline h1{{font-size:20px}}.hero-actions{{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}}.btn{{padding:9px 4px;font-size:12px;min-width:0}}.pattern-title{{font-size:40px}}.name-main{{font-size:30px}}.grid{{grid-template-columns:1fr;gap:12px}}}}
</style>
</head>
<body class="theme-male">
<div class="wrap">
  <section class="hero-sticky" id="heroSection">
    <div class="hero-topline">
      <h1>名字推荐</h1>
      <div class="hero-actions">
        <button class="btn active" id="maleBtn">男孩</button>
        <button class="btn" id="femaleBtn">女孩</button>
        <a class="btn" href="index.html">返回首页</a>
        <a class="btn" href="bazi-analysis.html">八字分析</a>
      </div>
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
const heroSection = document.getElementById('heroSection');
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
        <div class="pattern-right">10个名字</div>
      </div>
      ${{list.map(r => `<div class="name-item"><div class="name-top"><div><div class="name-main">${{r.name}}</div><div class="pinyin">${{r.pinyin}}</div></div><div class="grade">${{r.grade}}</div></div><div class="note">${{r.note}}</div></div>`).join('')}}
    </article>`;
  }}).join('');
}}
function syncButtons(){{
  const isMale = currentGender === '男';
  maleBtn.classList.toggle('active', isMale);
  femaleBtn.classList.toggle('active', !isMale);
  document.body.className = isMale ? 'theme-male' : 'theme-female';
}}
function restoreGenderScroll(g){{
  const remembered = genderScrollMemory[g];
  window.scrollTo({{ top: remembered == null ? 0 : remembered, behavior: 'auto' }});
}}
function setGender(nextGender){{
  if (nextGender === currentGender) return;
  genderScrollMemory[currentGender] = window.scrollY;
  currentGender = nextGender;
  syncButtons();
  render();
  requestAnimationFrame(() => restoreGenderScroll(nextGender));
}}
function updateStickyState(){{ heroSection.classList.toggle('compact', window.scrollY > 18); }}
maleBtn.onclick = () => setGender('男');
femaleBtn.onclick = () => setGender('女');
window.addEventListener('scroll', updateStickyState, {{ passive: true }});
window.addEventListener('resize', updateStickyState);
syncButtons();
render();
updateStickyState();
</script>
</body>
</html>'''

(ROOT / 'names.html').write_text(html, encoding='utf-8')
print('restored previous-style names.html')
