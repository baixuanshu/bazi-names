from pathlib import Path

path = Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
text = path.read_text(encoding='utf-8')
start = text.find('function nameCard(')
end = text.find('document.getElementById(\'closeBtn\').onclick=()=>modal.style.display=\'none\';')
if start == -1 or end == -1 or end <= start:
    raise SystemExit('modal runtime boundary not found')

replacement = r'''function nameCard(r,p){ const mobile = window.innerWidth <= 720; const open = mobile ? isModalDetailOpen(p, r.name) : true; if(mobile){ return `<div class="name-item" data-name="${r.name}"><div class="subline"><div><div class="name-calligraphy" style="${patternStyle[p]}">${r.name}</div><span class="small">${r.pinyin}</span></div><div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px"><div class="score">${r.score} 分</div><button class="btn" type="button" data-detail-toggle="1" data-pattern="${p}" data-name="${r.name}" style="padding:8px 12px;font-size:12px">${open?'收起详情':'展开详情'}</button></div></div><div class="note" data-detail-body="1" style="display:${open?'block':'none'}"><b>五行：</b>${r.wuxing}<br><b class="meaning">组合意思：</b><span class="meaning">${r.meaning}</span><br><b>出处：</b>${r.source}<br><span class="reason"><b>评分理由：</b><strong>评分 ${r.score}</strong>：${r.reason.replace(/^评分\s*\d+[.:分]?/,'')}</span></div></div>`; } return `<div class="name-item"><div class="subline"><div><div class="name-calligraphy" style="${patternStyle[p]}">${r.name}</div><span class="small">${r.pinyin}</span></div><div class="score">${r.score} 分</div></div><div class="note"><b>五行：</b>${r.wuxing}<br><b class="meaning">组合意思：</b><span class="meaning">${r.meaning}</span><br><b>出处：</b>${r.source}<br><span class="reason"><b>评分理由：</b><strong>评分 ${r.score}</strong>：${r.reason.replace(/^评分\s*\d+[.:分]?/,'')}</span></div></div>`; }
let modalGender='男'; let modalPattern=''; const modalScrollMemory = {}; const modalDetailState = {男:{},女:{}}; let modalSwitching = false;
function modalDetailKey(pattern,name){ return `${pattern}__${name}`; }
function isModalDetailOpen(pattern,name){ return !!modalDetailState[modalGender][modalDetailKey(pattern,name)]; }
function setModalDetailOpen(pattern,name,open){ modalDetailState[modalGender][modalDetailKey(pattern,name)] = !!open; }
function getModalBox(){ return modal.querySelector('.modal-box'); }
function getModalMemory(pattern){ if(!modalScrollMemory[pattern]) modalScrollMemory[pattern] = { 男: null, 女: null }; return modalScrollMemory[pattern]; }
function restoreModalScroll(pattern, gender){ const box = getModalBox(); if(!box) return; const y = getModalMemory(pattern)[gender]; box.scrollTop = y == null ? 0 : y; }
function lockModalGenderButtons(locked){ const a=document.getElementById('modalMale'); const b=document.getElementById('modalFemale'); [a,b].forEach(btn=>{ if(!btn) return; btn.disabled=locked; btn.style.pointerEvents=locked?'none':''; btn.style.opacity=locked?'.72':''; }); }
function getModalList(p){ return modalGender==='男' ? topData[p].boys : topData[p].girls; }
function bindModalDetailToggles(){ modalBody.querySelectorAll('[data-detail-toggle]').forEach(btn=>{ btn.onclick=()=>{ const pattern=btn.getAttribute('data-pattern'); const name=btn.getAttribute('data-name'); const item = btn.closest('.name-item'); const body = item && item.querySelector('[data-detail-body]'); if(!body) return; const open = body.style.display !== 'none'; const next = !open; body.style.display = next ? 'block' : 'none'; btn.textContent = next ? '收起详情' : '展开详情'; setModalDetailOpen(pattern, name, next); }; }); }
function renderModalNames(p){ const box = modal.querySelector('.modal-box'); box.classList.toggle('theme-male', modalGender==='男'); box.classList.toggle('theme-female', modalGender==='女'); const list = getModalList(p); modalBody.innerHTML=`<div class="modal-switch"><button class="btn ${modalGender==='男'?'active':''}" id="modalMale">男孩</button><button class="btn ${modalGender==='女'?'active':''}" id="modalFemale">女孩</button></div><div class="modal-section">${list.map(r=>nameCard(r,p)).join('')}</div>`; document.getElementById('modalMale').onclick=()=>switchModalGender('男'); document.getElementById('modalFemale').onclick=()=>switchModalGender('女'); bindModalDetailToggles(); lockModalGenderButtons(modalSwitching); }
function switchModalGender(nextGender){ if(nextGender===modalGender || modalSwitching) return; modalSwitching=true; lockModalGenderButtons(true); const box = getModalBox(); if(box && modalPattern){ getModalMemory(modalPattern)[modalGender] = box.scrollTop; } modalGender = nextGender; renderModalNames(modalPattern); requestAnimationFrame(()=>restoreModalScroll(modalPattern, modalGender)); requestAnimationFrame(()=>{ modalSwitching=false; lockModalGenderButtons(false); }); }
window.openModal=function(p){ modalPattern=p; modalGender='男'; modalSwitching=false; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); requestAnimationFrame(()=>restoreModalScroll(p, modalGender)); };
'''

text = text[:start] + replacement + text[end:]
path.write_text(text, encoding='utf-8')
print('rewrote modal runtime')
