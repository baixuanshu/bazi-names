from pathlib import Path

# ---- names.html ----
np = Path(r'D:\Projects\bazi-portal\names.html')
ns = np.read_bytes().decode('latin1')
ns = ns.replace(
    '.name-line .name-calligraphy{font-size:42px;line-height:1.05;font-weight:800;letter-spacing:1.2px}.name-line .small{display:block;margin-top:8px;color:#c9d3ea;font-size:14px}.name-line .score{font-size:18px;font-weight:800;white-space:nowrap}.name-line .note{margin-top:12px;line-height:1.8;color:#f4f7ff;font-size:14px}.detail-toggle{padding:8px 12px!important;font-size:12px!important;min-width:84px}',
    '.name-main{flex:1 1 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.name-line .name-calligraphy{font-size:42px;line-height:1.05;font-weight:800;letter-spacing:1.2px;text-align:center;width:100%}.name-line .small{display:block;margin-top:8px;color:#c9d3ea;font-size:14px;text-align:center;width:100%}.name-line .score{font-size:18px;font-weight:800;white-space:nowrap}.name-line .note{margin-top:12px;line-height:1.8;color:#f4f7ff;font-size:14px}.detail-toggle{padding:8px 12px!important;font-size:12px!important;min-width:84px}'
)
ns = ns.replace(
    '<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>',
    '<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>'
)
np.write_bytes(ns.encode('latin1'))

# ---- bazi-analysis.html ----
bp = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
bs = bp.read_bytes().decode('latin1')
bs = bs.replace(
    '.name-item{padding:16px 16px 14px;border:1px solid rgba(255,255,255,.08);box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 10px 26px rgba(0,0,0,.08);content-visibility:auto;contain:layout paint style;contain-intrinsic-size:220px}.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}',
    '.name-item{padding:16px 16px 14px;border:1px solid rgba(255,255,255,.08);box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 10px 26px rgba(0,0,0,.08);content-visibility:auto;contain:layout paint style;contain-intrinsic-size:220px}.name-main{flex:1 1 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.name-item .name-calligraphy{text-align:center;width:100%}.name-item .small{display:block;text-align:center;width:100%}.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}'
)
bs = bs.replace(
    '<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>',
    '<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>'
)
bs = bs.replace(
    "function getModalMemory(pattern){ if(!modalScrollMemory[pattern]) modalScrollMemory[pattern] = { 男: null, 女: null }; return modalScrollMemory[pattern]; }\r\nfunction restoreModalScroll(pattern, gender){ const box = getModalBox(); if(!box) return; const y = getModalMemory(pattern)[gender]; box.scrollTop = y == null ? 0 : y; }",
    "function getModalMemory(pattern){ if(!modalScrollMemory[pattern]) modalScrollMemory[pattern] = { 男: null, 女: null, 男Anchor: null, 女Anchor: null }; return modalScrollMemory[pattern]; }\r\nfunction captureModalAnchor(pattern, gender){ const box = getModalBox(); if(!box) return; const items=[...modalBody.querySelectorAll('.name-item')]; const top=box.scrollTop; let hit=items.find(el=>el.offsetTop + el.offsetHeight > top + 4) || items[0] || null; if(!hit) return; getModalMemory(pattern)[gender+'Anchor'] = { name: hit.getAttribute('data-name') || '', delta: top - hit.offsetTop }; }\r\nfunction restoreModalScroll(pattern, gender){ const box = getModalBox(); if(!box) return; const mem = getModalMemory(pattern); const anchor = mem[gender+'Anchor']; if(anchor && anchor.name){ const items=[...modalBody.querySelectorAll('.name-item')]; const hit=items.find(el=>el.getAttribute('data-name')===anchor.name); if(hit){ box.scrollTop = Math.max(0, hit.offsetTop + (anchor.delta||0)); return; } } const y = mem[gender]; box.scrollTop = y == null ? 0 : y; }"
)
bs = bs.replace(
    "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); requestAnimationFrame(()=>{ modalSwitching=false; lockModalGenderButtons(false); }); }",
    "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); requestAnimationFrame(()=>{ const box2=getModalBox(); if(box2 && modalPattern){ getModalMemory(modalPattern)[modalGender] = box2.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalSwitching=false; lockModalGenderButtons(false); }); }"
)
bs = bs.replace(
    "window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };",
    "window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>{ restoreModalScroll(p, modalGender); const box=getModalBox(); if(box){ getModalMemory(p)[modalGender]=box.scrollTop; captureModalAnchor(p, modalGender); } }); };"
)
bp.write_bytes(bs.encode('latin1'))
print('fixed names + modal layout + anchor scroll')
