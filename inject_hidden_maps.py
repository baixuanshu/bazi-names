from pathlib import Path
import json
p = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s = p.read_text(encoding='utf-8', errors='ignore')
if 'const hiddenMap=' in s and 'const ganMeta=' in s and 'const zhiMeta=' in s:
    print('already injected')
    raise SystemExit
hidden = {'子':['癸'],'丑':['己','癸','辛'],'寅':['甲','丙','戊'],'卯':['乙'],'辰':['戊','乙','癸'],'巳':['丙','庚','戊'],'午':['丁','己'],'未':['己','丁','乙'],'申':['庚','壬','戊'],'酉':['辛'],'戌':['戊','辛','丁'],'亥':['壬','甲']}
gan = {'甲':['木','阳'],'乙':['木','阴'],'丙':['火','阳'],'丁':['火','阴'],'戊':['土','阳'],'己':['土','阴'],'庚':['金','阳'],'辛':['金','阴'],'壬':['水','阳'],'癸':['水','阴']}
zhi = {'子':['水','阳'],'丑':['土','阴'],'寅':['木','阳'],'卯':['木','阴'],'辰':['土','阳'],'巳':['火','阴'],'午':['火','阳'],'未':['土','阴'],'申':['金','阳'],'酉':['金','阴'],'戌':['土','阳'],'亥':['水','阴']}
anchor = 'const rows='
pos = s.find(anchor)
if pos == -1:
    raise SystemExit('rows anchor not found')
insert = f"const hiddenMap={json.dumps(hidden, ensure_ascii=False)}; const ganMeta={json.dumps(gan, ensure_ascii=False)}; const zhiMeta={json.dumps(zhi, ensure_ascii=False)}; "
s = s[:pos] + insert + s[pos:]
p.write_text(s, encoding='utf-8')
print('injected maps')
