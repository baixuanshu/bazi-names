from pathlib import Path
p = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s = p.read_text(encoding='utf-8', errors='ignore')

# Replace helper block from pillarHtml/hiddenSection/elementBoxes with enhanced versions
start = s.find('function pillarHtml(')
end = s.find('function renderRows(list){', start)
if start == -1 or end == -1:
    raise SystemExit('helper block bounds not found')
new_block = """function pillarHtml(label,pillar){ const gan=pillar[0], zhi=pillar[1], g=ganMeta[gan], z=zhiMeta[zhi], c=(hiddenMap[zhi]||[]).map(wxSpan).join('、'); return `<div class=\"pillar\"><h3>${label}：${wxSpan(gan)}${wxSpan(zhi)}</h3><div class=\"meta-line\"><span class=\"label-mini\">天干</span>${wxSpan(gan)}（${g[1]}${g[0]}）</div><div class=\"meta-line\"><span class=\"label-mini\">地支</span>${wxSpan(zhi)}（${z[1]}${z[0]}）</div><div class=\"meta-line\"><span class=\"label-mini\">藏干</span><span class=\"canggan\">${c}</span></div></div>`; } function hiddenSection(r){ return `<div class=\"section-bar\">藏干展开：</div><div class=\"hidden-grid\">${pillarHtml('年柱',r.year)}${pillarHtml('月柱',r.month)}${pillarHtml('日柱',r.day)}${pillarHtml('时柱',r.hour)}</div>`; } function elementBoxes(r,title='八字五行'){ return `<div class=\"section-bar\">${title}</div><div class=\"element-grid\"><div class=\"element-box\"><div class=\"element-label\">金</div><div class=\"element-num element-jin\">${r.jin}</div></div><div class=\"element-box\"><div class=\"element-label\">木</div><div class=\"element-num element-mu\">${r.mu}</div></div><div class=\"element-box\"><div class=\"element-label\">水</div><div class=\"element-num element-shui\">${r.shui}</div></div><div class=\"element-box\"><div class=\"element-label\">火</div><div class=\"element-num element-huo\">${r.huo}</div></div><div class=\"element-box\"><div class=\"element-label\">土</div><div class=\"element-num element-tu\">${r.tu}</div></div></div>`; } function hiddenFiveCounts(r){ const pillars=[r.year,r.month,r.day,r.hour]; const out={金:0,木:0,水:0,火:0,土:0}; pillars.forEach(p=>{ const zhi=p[1]; (hiddenMap[zhi]||[]).forEach(g=>{ const wx=wxOfChar(g); if(out[wx]!==undefined) out[wx]++; }); }); return out; } function hiddenElementBoxes(r){ const h=hiddenFiveCounts(r); return `<div class=\"section-bar\">藏干五行</div><div class=\"element-grid\"><div class=\"element-box\"><div class=\"element-label\">金</div><div class=\"element-num element-jin\">${h['金']}</div></div><div class=\"element-box\"><div class=\"element-label\">木</div><div class=\"element-num element-mu\">${h['木']}</div></div><div class=\"element-box\"><div class=\"element-label\">水</div><div class=\"element-num element-shui\">${h['水']}</div></div><div class=\"element-box\"><div class=\"element-label\">火</div><div class=\"element-num element-huo\">${h['火']}</div></div><div class=\"element-box\"><div class=\"element-label\">土</div><div class=\"element-num element-tu\">${h['土']}</div></div></div>`; } function totalElementBoxes(r){ const h=hiddenFiveCounts(r); return `<div class=\"section-bar\">总五行</div><div class=\"element-grid\"><div class=\"element-box\"><div class=\"element-label\">金</div><div class=\"element-num element-jin\">${r.jin + h['金']}</div></div><div class=\"element-box\"><div class=\"element-label\">木</div><div class=\"element-num element-mu\">${r.mu + h['木']}</div></div><div class=\"element-box\"><div class=\"element-label\">水</div><div class=\"element-num element-shui\">${r.shui + h['水']}</div></div><div class=\"element-box\"><div class=\"element-label\">火</div><div class=\"element-num element-huo\">${r.huo + h['火']}</div></div><div class=\"element-box\"><div class=\"element-label\">土</div><div class=\"element-num element-tu\">${r.tu + h['土']}</div></div></div>`; } function renderRows(list){"""
s = s[:start] + new_block + s[end+len('function renderRows(list){'):]

# Replace duplicate element boxes sequence in card rendering
old = '${elementBoxes(r)}${hiddenSection(r)}${elementBoxes(r)}<div class="bottom-actions">'
new = '${elementBoxes(r)}${hiddenSection(r)}${hiddenElementBoxes(r)}${totalElementBoxes(r)}<div class="bottom-actions">'
if old not in s:
    raise SystemExit('render card sequence not found')
s = s.replace(old, new, 1)

# Improve CSS for mobile and pillar layout
css_old = '.hidden-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:14px}.pillar{padding:12px 12px 10px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}.pillar h3{margin:0 0 8px;font-size:15px;line-height:1.2;text-align:center;font-weight:900}.meta-line{margin:3px 0;font-size:12px;line-height:1.55;color:#eaf0ff;font-weight:700}.wx-jin{color:#f4cf7b}.wx-mu{color:#8bd5a0}.wx-shui{color:#8ab9ff}.wx-huo{color:#ff9db3}.wx-tu{color:#dcb58e}.canggan{font-weight:900;letter-spacing:.5px}.label-mini{display:inline-block;color:var(--muted);min-width:34px}.bottom-actions{display:flex;justify-content:space-between;gap:12px;margin-top:16px}'
css_new = '.hidden-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:14px}.pillar{padding:12px 12px 10px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}.pillar h3{margin:0 0 10px;font-size:15px;line-height:1.35;text-align:center;font-weight:900}.meta-line{margin:6px 0;font-size:12px;line-height:1.7;color:#eaf0ff;font-weight:700}.wx-jin{color:#f4cf7b}.wx-mu{color:#8bd5a0}.wx-shui{color:#8ab9ff}.wx-huo{color:#ff9db3}.wx-tu{color:#dcb58e}.canggan{font-weight:900;letter-spacing:.5px}.label-mini{display:inline-block;color:var(--muted);min-width:38px}.bottom-actions{display:flex;justify-content:space-between;gap:12px;margin-top:16px}'
if css_old in s:
    s = s.replace(css_old, css_new, 1)

mobile_old = '.bazi-line{font-size:18px}.section-bar{font-size:16px}.hidden-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.pillar{padding:10px}.pillar h3{font-size:14px}.meta-line{font-size:11px}}'
mobile_new = '.bazi-line{font-size:18px}.section-bar{font-size:16px}.hidden-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.pillar{padding:10px 10px 8px}.pillar h3{font-size:14px;line-height:1.4}.meta-line{font-size:11px;line-height:1.8}.label-mini{min-width:32px;display:block;margin-bottom:2px}}'
if mobile_old in s:
    s = s.replace(mobile_old, mobile_new, 1)

p.write_text(s, encoding='utf-8')
print('patched totals and mobile layout')
