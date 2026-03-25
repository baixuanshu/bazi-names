from pathlib import Path
p=Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s=p.read_bytes().decode('latin1')
s=s.replace(
"function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); requestAnimationFrame(()=>{ modalSwitching=false; lockModalGenderButtons(false); }); }",
"function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop || 0; } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); requestAnimationFrame(()=>{ const box2=getModalBox(); if(box2 && modalPattern){ getModalMemory(modalPattern)[modalGender] = box2.scrollTop || 0; } modalSwitching=false; lockModalGenderButtons(false); }); }",
1)
s=s.replace(
"window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };",
"window.openModal=function(p){ if(!modalScrollMemory[p]) modalScrollMemory[p] = { 男: 0, 女: 0 }; modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };",
1)
p.write_bytes(s.encode('latin1'))
print('applied simple modal memory on clean base')
