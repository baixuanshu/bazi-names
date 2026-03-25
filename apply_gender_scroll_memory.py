from pathlib import Path
import re

# names.html
names = Path(r'D:\Projects\bazi-portal\names.html')
s = names.read_text(encoding='utf-8', errors='ignore')
pat = re.compile(r"function syncGenderButtons\(\)\{.*?</script></body></html>", re.S)
repl = """function syncGenderButtons(){ const isMale=currentGender==='男'; maleBtn.classList.toggle('active',isMale); femaleBtn.classList.toggle('active',!isMale); }
const genderScrollMemory = { 男: null, 女: null };
function restoreGenderScroll(g){ const y = genderScrollMemory[g]; window.scrollTo({ top: y == null ? 0 : y, behavior: 'auto' }); }
function setGender(g){ if(g===currentGender) return; genderScrollMemory[currentGender] = window.scrollY; currentGender=g; body.className=`names-page ${g==='男'?'theme-male':'theme-female'}`; syncGenderButtons(); render(); requestAnimationFrame(()=>restoreGenderScroll(g)); }
function updateStickyState(){ if(heroSection) heroSection.classList.toggle('compact', window.scrollY > 18); }
maleBtn.onclick=()=>setGender('男');
femaleBtn.onclick=()=>setGender('女');
body.className='names-page theme-male';
syncGenderButtons();
render();
window.addEventListener('scroll', updateStickyState, {passive:true});
window.addEventListener('resize', updateStickyState);
updateStickyState();</script></body></html>"""
ns, count = pat.subn(repl, s, count=1)
if count != 1:
    raise SystemExit('names.html patch failed')
names.write_text(ns, encoding='utf-8')

# bazi-analysis.html modal
bazi = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
s = bazi.read_text(encoding='utf-8', errors='ignore')
pat = re.compile(r"modalGender=.*?window\.openModal=function\(p\)\{.*?modal\.addEventListener\('click',e=>\{ if\(e\.target===modal\) modal\.style\.display='none'; \}\);", re.S)
repl = """modalGender='男'; let modalPattern=''; const modalScrollMemory = {};
function getModalBox(){ return modal.querySelector('.modal-box'); }
function getModalMemory(pattern){ if(!modalScrollMemory[pattern]) modalScrollMemory[pattern] = { 男: null, 女: null }; return modalScrollMemory[pattern]; }
function restoreModalScroll(pattern, gender){ const box = getModalBox(); if(!box) return; const y = getModalMemory(pattern)[gender]; box.scrollTop = y == null ? 0 : y; }
function renderModalNames(p){ const list = modalGender==='男' ? topData[p].boys : topData[p].girls; modalBody.innerHTML=`<div class="modal-switch"><button class="btn ${modalGender==='男'?'active':''}" id="modalMale">男孩</button><button class="btn ${modalGender==='女'?'active':''}" id="modalFemale">女孩</button><button class="btn" id="modalClose">关闭</button></div><div class="modal-section">${list.map(r=>nameCard(r,p)).join('')}</div>`; document.getElementById('modalMale').onclick=()=>switchModalGender('男'); document.getElementById('modalFemale').onclick=()=>switchModalGender('女'); document.getElementById('modalClose').onclick=()=>{modal.style.display='none';}; }
function switchModalGender(nextGender){ if(nextGender===modalGender) return; const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); }
window.openModal=function(p){ modalPattern=p; modalGender='男'; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };
document.getElementById('closeBtn').onclick=()=>modal.style.display='none'; modal.addEventListener('click',e=>{ if(e.target===modal) modal.style.display='none'; });"""
ns, count = pat.subn(repl, s, count=1)
if count != 1:
    raise SystemExit('bazi-analysis.html modal patch failed')
bazi.write_text(ns, encoding='utf-8')
print('applied gender scroll memory to names page and modal')
