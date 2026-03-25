from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\bazi-analysis.html').read_text(encoding='utf-8', errors='ignore')
start = s.find('cards.innerHTML=list.map')
print(start)
print(repr(s[start:start+1500]))
