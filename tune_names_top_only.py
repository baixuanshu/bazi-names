from pathlib import Path
p = Path(r'D:\Projects\bazi-portal\names.html')
s = p.read_text(encoding='utf-8')

s = s.replace('.hero-actions{grid-template-columns:repeat(4,minmax(0,1fr));gap:5px}.btn{padding:8px 2px;font-size:11px;min-width:0}.pattern-head{min-height:92px}.pattern-title{font-size:48px}.pattern-left,.pattern-right{top:2px}}', '.hero-actions{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;width:100%}.btn{padding:8px 2px;font-size:11px;min-width:0;width:100%}.pattern-head{display:flex;align-items:center;justify-content:center;position:relative;min-height:92px;margin-bottom:12px}.pattern-title{font-size:48px;font-weight:900;line-height:1;letter-spacing:1px;text-align:center}.pattern-left,.pattern-right{position:absolute;top:2px;font-size:12px;color:var(--muted);display:flex;align-items:center}.pattern-left{left:0}.pattern-right{right:0}}')

s = s.replace('<div class="hero-actions">', '<div class="hero-actions">')
s = s.replace('<div class="pattern-left"><span class="badge">${patternDirection[p]}</span></div><div class="pattern-title" style="${patternStyle[p]}">${p}</div><div class="pattern-right"><span class="badge">10个名字</span></div>', '<div class="pattern-left"><span class="badge">${patternDirection[p]}</span></div><div class="pattern-title" style="${patternStyle[p]}">${p}</div><div class="pattern-right"><span class="badge">10个名字</span></div>')

p.write_text(s, encoding='utf-8')
print('tuned top only')
