from pathlib import Path
p = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s = p.read_text(encoding='utf-8', errors='ignore')

if 'function wxClass(wx)' not in s:
    idx = s.find('function elementBoxes(r){')
    if idx == -1: raise SystemExit('elementBoxes not found')
    helpers = "function wxClass(wx){ return {'金':'wx-jin','木':'wx-mu','水':'wx-shui','火':'wx-huo','土':'wx-tu'}[wx] || ''; } function wxOfChar(ch){ return (ganMeta[ch]||zhiMeta[ch]||['未知',''])[0]; } function wxSpan(ch){ const wx = wxOfChar(ch); return `<span class=\"${wxClass(wx)}\">${ch}</span>`; } function baziHtml(text){ return text.split(' ').map(p=>`<span class=\"bazi-piece\">${wxSpan(p[0])}${wxSpan(p[1])}</span>`).join(''); } function pillarHtml(label,pillar){ const gan=pillar[0], zhi=pillar[1], g=ganMeta[gan], z=zhiMeta[zhi], c=(hiddenMap[zhi]||[]).map(wxSpan).join('、'); return `<div class=\"pillar\"><h3>${label}：${wxSpan(gan)}${wxSpan(zhi)}</h3><div class=\"meta-line\"><span class=\"label-mini\">天干</span>${wxSpan(gan)}（${g[1]}${g[0]}）</div><div class=\"meta-line\"><span class=\"label-mini\">地支</span>${wxSpan(zhi)}（${z[1]}${z[0]}）</div><div class=\"meta-line\"><span class=\"label-mini\">藏干</span><span class=\"canggan\">${c}</span></div></div>`; } function hiddenSection(r){ return `<div class=\"section-bar\">藏干展开：</div><div class=\"hidden-grid\">${pillarHtml('年柱',r.year)}${pillarHtml('月柱',r.month)}${pillarHtml('日柱',r.day)}${pillarHtml('时柱',r.hour)}</div>`; } "
    s = s[:idx] + helpers + s[idx:]

base = s.find('cards.innerHTML=list.map')
start = s.find('<div class="note"><b>', base)
end = s.find('${elementBoxes(r)}<div class="bottom-actions">', base)
if start == -1 or end == -1:
    raise SystemExit(f'card bounds not found: {start}, {end}')
s = s[:start] + '<div class="bazi-line"><b>八字：</b>${baziHtml(r.bazi)}</div>${elementBoxes(r)}${hiddenSection(r)}' + s[end:]

css_old = '.element-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:16px}.element-box{padding:10px 6px;border-radius:16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);text-align:center}.element-label{font-size:12px;color:var(--muted);margin-bottom:4px}.element-num{font-size:24px;font-weight:700}.element-jin{color:var(--gold)}.element-mu{color:var(--wood)}.element-shui{color:var(--water)}.element-huo{color:var(--fire)}.element-tu{color:var(--earth)}.bottom-actions{display:flex;justify-content:space-between;gap:12px;margin-top:16px}'
css_new = '.element-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:16px}.element-box{padding:10px 6px;border-radius:16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);text-align:center}.element-label{font-size:12px;color:var(--muted);margin-bottom:4px}.element-num{font-size:24px;font-weight:700}.element-jin{color:var(--gold)}.element-mu{color:var(--wood)}.element-shui{color:var(--water)}.element-huo{color:var(--fire)}.element-tu{color:var(--earth)}.bazi-line{margin-top:14px;text-align:center;font-size:22px;font-weight:900;letter-spacing:.8px;line-height:1.4}.bazi-piece{display:inline-block;margin:0 4px}.section-bar{margin-top:14px;text-align:center;font-size:17px;font-weight:900;letter-spacing:.4px}.hidden-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:14px}.pillar{padding:12px 12px 10px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}.pillar h3{margin:0 0 8px;font-size:15px;line-height:1.2;text-align:center;font-weight:900}.meta-line{margin:3px 0;font-size:12px;line-height:1.55;color:#eaf0ff;font-weight:700}.wx-jin{color:#f4cf7b}.wx-mu{color:#8bd5a0}.wx-shui{color:#8ab9ff}.wx-huo{color:#ff9db3}.wx-tu{color:#dcb58e}.canggan{font-weight:900;letter-spacing:.5px}.label-mini{display:inline-block;color:var(--muted);min-width:34px}.bottom-actions{display:flex;justify-content:space-between;gap:12px;margin-top:16px}'
if css_old in s:
    s = s.replace(css_old, css_new, 1)

p.write_text(s, encoding='utf-8')
print('patched by exact bounds')
