from pathlib import Path

# names.html
np = Path(r'D:\Projects\bazi-portal\names.html')
nb = np.read_bytes()
nb = nb.replace(
    b'.name-line .score{font-size:18px;font-weight:800;white-space:nowrap}.name-line .note{margin-top:12px;line-height:1.8;color:#f4f7ff;font-size:14px}.detail-toggle{padding:8px 12px!important;font-size:12px!important;min-width:84px}',
    b'.name-line .score{font-size:18px;font-weight:800;white-space:nowrap}.name-line .note{margin-top:12px;line-height:1.8;color:#f4f7ff;font-size:14px}.name-line .source-detail,.name-line .source-detail *{font-weight:800!important;font-size:15px}.detail-toggle{padding:8px 12px!important;font-size:12px!important;min-width:84px}'
)
nb = nb.replace('<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>'.encode('utf-8'), '<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>'.encode('utf-8'))
nb = nb.replace('<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>'.encode('utf-8'), '<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>'.encode('utf-8'))
np.write_bytes(nb)

# bazi-analysis.html
bp = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
bb = bp.read_bytes()
bb = bb.replace(
    b'.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}',
    b'.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.name-item .source-detail,.name-item .source-detail *{font-weight:800!important;font-size:15px}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}'
)
bb = bb.replace('<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>'.encode('utf-8'), '<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>'.encode('utf-8'))
bb = bb.replace('<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>'.encode('utf-8'), '<span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span>'.encode('utf-8'))
old_open = "window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };\r\n".encode('utf-8')
new_open = "window.openModal=function(p){ if(modalPattern && modalPattern!==p){ modalScrollMemory[p] = { 男: null, 女: null, 男Anchor: null, 女Anchor: null }; } modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender, 'auto')); };\r\n".encode('utf-8')
if old_open in bb:
    bb = bb.replace(old_open, new_open, 1)
else:
    start = bb.find(b'window.openModal=function(p)')
    end = bb.find(b"document.getElementById('closeBtn')", start)
    if start == -1 or end == -1:
        raise SystemExit('openModal boundaries not found')
    bb = bb[:start] + new_open + bb[end:]
bp.write_bytes(bb)
print('fixed via bytes')
