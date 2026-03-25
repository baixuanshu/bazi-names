from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\names.html').read_text(encoding='utf-8')
needle = 'return `<article class="card"'
i = s.find(needle)
print(i)
print(s[i:i+1200])
