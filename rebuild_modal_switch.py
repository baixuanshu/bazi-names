from pathlib import Path
p=Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s=p.read_bytes().decode('latin1')

# replace memory helpers by slicing
start=s.find('function getModalMemory(pattern){')
end=s.find('function lockModalGenderButtons(locked){', start)
if start==-1 or end==-1:
    raise SystemExit('memory helper boundaries not found')
new_helpers = (
    "function getModalMemory(pattern){ if(!modalScrollMemory[pattern]) modalScrollMemory[pattern] = { \xe7\x94\xb7: 0, \xe5\xa5\xb3: 0 }; return modalScrollMemory[pattern]; }\r\n"
    "function saveModalScroll(pattern, gender){ const box = getModalBox(); if(!box || !pattern || !gender) return; getModalMemory(pattern)[gender] = box.scrollTop || 0; }\r\n"
    "function restoreModalScroll(pattern, gender, behavior='smooth'){ const box = getModalBox(); if(!box) return; const y = getModalMemory(pattern)[gender] || 0; try { box.scrollTo({ top: y, behavior }); } catch(e) { box.scrollTop = y; } }\r\n"
)
new_helpers = new_helpers.encode('latin1').decode('unicode_escape')
s = s[:start] + new_helpers + s[end:]

# replace switch block by boundaries
sw_start=s.find('function switchModalGender(nextGender){')
sw_end=s.find('window.openModal=function(p){', sw_start)
if sw_start==-1 or sw_end==-1:
    raise SystemExit('switch boundaries not found')
new_switch=(
    "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); "
    "saveModalScroll(modalPattern, modalGender); modalGender = nextGender; renderModalNames(modalPattern); "
    "requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender, 'smooth')); "
    "setTimeout(()=>{ modalSwitching=false; lockModalGenderButtons(false); }, 220); }\r\n"
)
s = s[:sw_start] + new_switch + s[sw_end:]

# replace open block by boundaries
op_start=s.find('window.openModal=function(p){')
op_end=s.find("document.getElementById('closeBtn')", op_start)
if op_start==-1 or op_end==-1:
    raise SystemExit('open boundaries not found')
open_slice=s[op_start:op_end]
# preserve existing Chinese text by reconstructing around it minimally
new_open=(
    "window.openModal=function(p){ if(!modalScrollMemory[p]) modalScrollMemory[p] = { \xe7\x94\xb7: 0, \xe5\xa5\xb3: 0 }; modalPattern=p; modalGender='\xe7\x94\xb7'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' \xe6\x8e\xa8\xe8\x8d\x90\xe5\x90\x8d\xe5\xad\x97'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender, 'auto')); };\r\n"
)
new_open = new_open.encode('latin1').decode('unicode_escape')
s = s[:op_start] + new_open + s[op_end:]

# ensure modal scroll is remembered while user manually scrolls
anchor = "function bindModalDetailToggles(){ modalBody.querySelectorAll('[data-detail-toggle]').forEach(btn=>{ btn.onclick=()=>{ const pattern=btn.getAttribute('data-pattern'); const name=btn.getAttribute('data-name'); const item = btn.closest('.name-item'); const body = item && item.querySelector('[data-detail-body]'); if(!body) return; const open = body.style.display !== 'none'; const next = !open; body.style.display = next ? 'block' : 'none'; btn.textContent = next ? '\xe6\x94\xb6\xe8\xb5\xb7\xe8\xaf\xa6\xe6\x83\x85' : '\xe5\xb1\x95\xe5\xbc\x80\xe8\xaf\xa6\xe6\x83\x85'; setModalDetailOpen(pattern, name, next); }; }); }\r\nfunction renderModalNames(p){"
anchor = anchor.encode('latin1').decode('unicode_escape')
replace = anchor.replace("function renderModalNames(p){", "function bindModalScrollMemory(){ const box=getModalBox(); if(!box) return; if(box._memoryHandler) box.removeEventListener('scroll', box._memoryHandler); box._memoryHandler=()=>saveModalScroll(modalPattern, modalGender); box.addEventListener('scroll', box._memoryHandler, {passive:true}); }\r\nfunction renderModalNames(p){")
if anchor in s:
    s=s.replace(anchor, replace, 1)
    s=s.replace("bindModalDetailToggles(); lockModalGenderButtons(modalSwitching); }", "bindModalDetailToggles(); bindModalScrollMemory(); lockModalGenderButtons(modalSwitching); }", 1)
else:
    raise SystemExit('bind detail block not found')

p.write_bytes(s.encode('latin1'))
print('rebuilt modal switch')
