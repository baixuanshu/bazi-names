from pathlib import Path
for fn, old in [
    (r'D:\Projects\bazi-portal\names.html', b'.name-line .source-detail,.name-line .source-detail *{font-weight:800!important;font-size:15px}'),
    (r'D:\Projects\bazi-portal\bazi-analysis.html', b'.name-item .source-detail,.name-item .source-detail *{font-weight:800!important;font-size:15px}')
]:
    p=Path(fn)
    b=p.read_bytes()
    if old not in b:
        raise SystemExit(f'missing target in {fn}')
    b=b.replace(old, old.replace(b';font-size:15px', b''), 1)
    p.write_bytes(b)
print('source detail now bold only, normal size')
