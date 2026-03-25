from pathlib import Path
src = Path(r'D:\Projects\bazi-portal\backup\names.20260323-0514.html')
dst = Path(r'D:\Projects\bazi-portal\names.html')
s = src.read_bytes().decode('latin1')
repls = [
    ("hero::after,.card::after,.portal-orb::after{content:'';position:absolute;inset:auto -20% -60% auto;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle, rgba(255,255,255,.16), transparent 68%);opacity:.35;pointer-events:none}",
     "hero::after,.card::after,.portal-orb::after{display:none!important;content:none!important}"),
    (".name-line::after{content:'';position:absolute;right:-30px;top:-30px;width:100px;height:100px;background:radial-gradient(circle, rgba(255,255,255,.14), transparent 70%);opacity:.35}.pattern-card .title-wrap{display:flex;justify-content:space-between;align-items:center;gap:10px}\n.theme-male .hero::before{content:'';position:absolute;inset:auto -30px -20px auto;width:220px;height:220px;background:radial-gradient(circle, rgba(120,162,255,.16), transparent 68%);filter:blur(2px);animation:bladeGlow 6s ease-in-out infinite}.theme-female .hero::before{content:'';position:absolute;inset:auto -20px -20px auto;width:220px;height:220px;background:radial-gradient(circle, rgba(255,219,234,.24), transparent 68%);animation:petalGlow 7s ease-in-out infinite}.theme-female .card::before{content:'';position:absolute;right:14px;top:14px;width:46px;height:46px;border-radius:50%;background:radial-gradient(circle, rgba(255,227,239,.22), transparent 70%)}",
     ".name-line::after{display:none!important;content:none!important}.pattern-card .title-wrap{display:flex;justify-content:space-between;align-items:center;gap:10px}\n.theme-male .hero::before,.theme-female .hero::before,.theme-female .card::before{display:none!important;content:none!important}"),
    ("@keyframes bladeGlow{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-8px) scale(1.04)}} @keyframes petalGlow{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-10px) rotate(6deg)}}", "")
]
for old,new in repls:
    if old not in s:
        raise SystemExit('missing target block')
    s = s.replace(old,new,1)
dst.write_bytes(s.encode('latin1'))
print('clean glow fix applied')
