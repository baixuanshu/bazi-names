from pathlib import Path
p=Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s=p.read_bytes().decode('latin1')

# Make source detail body bold in both mobile and desktop card templates
s=s.replace('<b>出处详情：</b>${r.source}<br><span>组合意思：${r.meaning}</span>','<b>出处详情：</b><strong>${r.source}</strong><br><span>组合意思：${r.meaning}</span>')

# Replace anchor capture/restore block with smooth aligned version
old_block = "function captureModalAnchor(pattern, gender){ const box = getModalBox(); if(!box) return; const items=[...modalBody.querySelectorAll('.name-item')]; const top=box.scrollTop; const hit=items.find(el=>el.offsetTop + el.offsetHeight > top + 4) || items[0] || null; if(!hit) return; getModalMemory(pattern)[gender+'Anchor'] = { name: hit.getAttribute('data-name') || '', delta: top - hit.offsetTop }; }\r\nfunction restoreModalScroll(pattern, gender){ const box = getModalBox(); if(!box) return; const mem = getModalMemory(pattern); const anchor = mem[gender+'Anchor']; if(anchor && anchor.name){ const items=[...modalBody.querySelectorAll('.name-item')]; const hit=items.find(el=>el.getAttribute('data-name')===anchor.name); if(hit){ box.scrollTop = Math.max(0, hit.offsetTop + (anchor.delta||0)); return; } } const y = mem[gender]; box.scrollTop = y == null ? 0 : y; }"
new_block = "function captureModalAnchor(pattern, gender){ const box = getModalBox(); if(!box) return; const items=[...modalBody.querySelectorAll('.name-item')]; const top=box.scrollTop; const hit=items.find(el=>el.offsetTop + el.offsetHeight > top + 4) || items[0] || null; if(!hit) return; getModalMemory(pattern)[gender+'Anchor'] = { name: hit.getAttribute('data-name') || '', delta: top - hit.offsetTop }; }\r\nfunction restoreModalScroll(pattern, gender, behavior='auto'){ const box = getModalBox(); if(!box) return; const mem = getModalMemory(pattern); const anchor = mem[gender+'Anchor']; let targetY = null; if(anchor && anchor.name){ const items=[...modalBody.querySelectorAll('.name-item')]; const hit=items.find(el=>el.getAttribute('data-name')===anchor.name); if(hit){ targetY = Math.max(0, hit.offsetTop + (anchor.delta||0)); } } if(targetY == null){ const y = mem[gender]; targetY = y == null ? 0 : y; } try { box.scrollTo({ top: targetY, behavior }); } catch(e) { box.scrollTop = targetY; } }"
if old_block in s:
    s=s.replace(old_block,new_block,1)
else:
    raise SystemExit('old anchor block not found')

old_switch = "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); try { const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); requestAnimationFrame(()=>{ const box2=getModalBox(); if(box2 && modalPattern){ getModalMemory(modalPattern)[modalGender] = box2.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalSwitching=false; lockModalGenderButtons(false); }); } catch (e) { console.error('switchModalGender failed', e); modalSwitching=false; lockModalGenderButtons(false); } }"
new_switch = "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); try { const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender, 'smooth')); requestAnimationFrame(()=>{ const box2=getModalBox(); if(box2 && modalPattern){ getModalMemory(modalPattern)[modalGender] = box2.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalSwitching=false; lockModalGenderButtons(false); }); } catch (e) { console.error('switchModalGender failed', e); modalSwitching=false; lockModalGenderButtons(false); } }"
if old_switch in s:
    s=s.replace(old_switch,new_switch,1)
else:
    raise SystemExit('old switch block not found')

old_open = "window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };"
new_open = "window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender, 'auto')); };"
if old_open in s:
    s=s.replace(old_open,new_open,1)

p.write_bytes(s.encode('latin1'))
print('fixed modal smooth restore + source bold')
