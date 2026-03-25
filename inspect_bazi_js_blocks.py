from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\bazi-analysis.html').read_text(encoding='utf-8', errors='ignore')
for key in ['function elementBoxes','function renderRows','function renderPatternCards','const rows=','function nameCard','window.openModal=function']:
    i = s.find(key)
    print('\nKEY', key, 'IDX', i)
    if i != -1:
        print(s[i:i+2200])
