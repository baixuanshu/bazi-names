from pathlib import Path
p=Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
raw=p.read_bytes()
s=raw.decode('latin1')
start=s.find('function getModalMemory(pattern){')
mid=s.find('function lockModalGenderButtons(locked){', start)
if start==-1 or mid==-1:
    raise SystemExit('memory block boundaries not found')
new_block = "function getModalMemory(pattern){ if(!modalScrollMemory[pattern]) modalScrollMemory[pattern] = { 男: 0, 女: 0 }; return modalScrollMemory[pattern]; }\r\nfunction captureModalScroll(pattern, gender){ const box = getModalBox(); if(!box) return; getModalMemory(pattern)[gender] = box.scrollTop || 0; }\r\nfunction restoreModalScroll(pattern, gender, behavior='auto'){ const box = getModalBox(); if(!box) return; const y = getModalMemory(pattern)[gender] || 0; try { box.scrollTo({ top: y, behavior }); } catch(e) { box.scrollTop = y; } }\r\n"
s = s[:start] + new_block + s[mid:]
old_switch = "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); try { const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender, 'smooth')); requestAnimationFrame(()=>{ const box2=getModalBox(); if(box2 && modalPattern){ getModalMemory(modalPattern)[modalGender] = box2.scrollTop; captureModalAnchor(modalPattern, modalGender); } modalSwitching=false; lockModalGenderButtons(false); }); } catch (e) { console.error('switchModalGender failed', e); modalSwitching=false; lockModalGenderButtons(false); } }"
new_switch = "function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); try { captureModalScroll(modalPattern, modalGender); modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender, 'auto')); requestAnimationFrame(()=>{ captureModalScroll(modalPattern, modalGender); modalSwitching=false; lockModalGenderButtons(false); }); } catch (e) { console.error('switchModalGender failed', e); modalSwitching=false; lockModalGenderButtons(false); } }"
if old_switch not in s:
    raise SystemExit('old switch block not found')
s=s.replace(old_switch,new_switch,1)
open_start=s.find('window.openModal=function(p){')
open_end=s.find("document.getElementById('closeBtn')", open_start)
if open_start==-1 or open_end==-1:
    raise SystemExit('open block boundaries not found')
new_open = "window.openModal=function(p){ if(!modalScrollMemory[p]) modalScrollMemory[p] = { 男: 0, 女: 0 }; modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender, 'auto')); };\r\n"
s = s[:open_start] + new_open + s[open_end:]
p.write_text(s, encoding='utf-8')
print('final simple modal scroll fix applied utf8')
