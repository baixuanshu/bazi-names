from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\bazi-analysis.html').read_text(encoding='utf-8', errors='ignore')
base = s.find('cards.innerHTML=list.map')
print('base', base)
print('note after', s.find('<div class="note"><b>', base))
print('elem after', s.find('${elementBoxes(r)}<div class="bottom-actions">', base))
print('snippet', repr(s[base:base+1200]))
