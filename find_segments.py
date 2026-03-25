from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\bazi-analysis.html').read_text(encoding='utf-8', errors='ignore')
for needle in [
    '<div class="note"><b>',
    '${elementBoxes(r)}<div class="bottom-actions">',
    'function applyView(){',
    'cards.innerHTML=list.map(r=>`<article class="card"'
]:
    print(needle, s.find(needle))
