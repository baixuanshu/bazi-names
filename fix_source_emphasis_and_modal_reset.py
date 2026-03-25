from pathlib import Path

# names.html
np = Path(r'D:\Projects\bazi-portal\names.html')
ns = np.read_bytes().decode('latin1')
ns = ns.replace('.name-line .score{font-size:18px;font-weight:800;white-space:nowrap}.name-line .note{margin-top:12px;line-height:1.8;color:#f4f7ff;font-size:14px}.detail-toggle{padding:8px 12px!important;font-size:12px!important;min-width:84px}', '.name-line .score{font-size:18px;font-weight:800;white-space:nowrap}.name-line .note{margin-top:12px;line-height:1.8;color:#f4f7ff;font-size:14px}.name-line .source-detail,.name-line .source-detail *{font-weight:800!important;font-size:15px}.detail-toggle{padding:8px 12px!important;font-size:12px!important;min-width:84px}')
ns = ns.replace('<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>','<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>')
ns = ns.replace('<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>','<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>')
np.write_bytes(ns.encode('latin1'))

# bazi-analysis.html
bp = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
bs = bp.read_bytes().decode('latin1')
bs = bs.replace('.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}', '.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.name-item .source-detail,.name-item .source-detail *{font-weight:800!important;font-size:15px}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}')
bs = bs.replace('<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>','<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>')
bs = bs.replace('<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>','<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>')
start = bs.find('window.openModal=function(p)')
end = bs.find("document.getElementById('closeBtn')", start)
if start == -1 or end == -1:
    raise SystemExit('openModal boundaries not found')
new_open = "window.openModal=function(p){ if(modalPattern && modalPattern!==p){ modalScrollMemory[p] = { 男: null, 女: null, 男Anchor: null, 女Anchor: null }; } modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender, 'auto')); };\r\n"
bs = bs[:start] + new_open + bs[end:]
bp.write_bytes(bs.encode('latin1'))
print('fixed source emphasis + modal per-pattern reset')
