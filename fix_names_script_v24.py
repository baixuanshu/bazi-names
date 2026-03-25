from pathlib import Path

p = Path(r'D:\Projects\bazi-portal\names.html')
s = p.read_text(encoding='utf-8', errors='ignore')
start = s.find('const patternStyle=')
end = s.rfind('</script>')
if start == -1 or end == -1 or end <= start:
    raise SystemExit('script block not found')
new_script = '''const patternStyle={"火格":"color:#ff9db3;text-shadow:0 2px 14px rgba(255,157,179,.16)","土格":"color:#d9b375;text-shadow:0 2px 12px rgba(217,179,117,.14)","木火格":"background:linear-gradient(135deg,#79d99e 0%,#90d88a 40%,#ff8e7a 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none","水火格":"background:linear-gradient(135deg,#79b7ff 0%,#8eaaff 45%,#ff8b9f 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none","火土格":"background:linear-gradient(135deg,#e25a4b,#e7b066);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none","金火格":"background:linear-gradient(135deg,#eef4ff,#ffb37f);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none"};
let currentGender='男';
const patterns=['火格','土格','木火格','水火格','火土格','金火格'];
const container=document.getElementById('patterns');
const maleBtn=document.getElementById('maleBtn');
const femaleBtn=document.getElementById('femaleBtn');
const heroSection=document.getElementById('heroSection');
const body=document.body;
function render(){
  container.innerHTML = patterns.map(p=>{
    const list=(currentGender==='男'?topData[p].boys:topData[p].girls);
    return `<article class="card pattern-card" id="${p}" style="background-image:${patternBg[p]}"><div class="pattern-main"><div class="pattern-corner pc-tl"><span class="badge">${patternDirection[p]}</span></div><div class="pattern-center" style="${patternStyle[p]}">${p}</div><div class="pattern-corner pc-tr"><span class="badge">10个名字</span></div></div>${list.map(r=>`<div class="name-line"><div class="subline"><div><div class="name-calligraphy" style="${patternStyle[p]}">${r.name}</div><span class="small">${r.pinyin}</span></div><div class="score">${r.score} 分</div></div><div class="note"><b>五行：</b>${r.wuxing}<br><b class="meaning">组合意思：</b><span class="meaning">${r.meaning}</span><br><b>出处：</b>${r.source}<br><span class="reason"><b>评分理由：</b><strong>评分 ${r.score}</strong>，${r.reason.replace(/^评分\s*\d+分/,'')}</span></div></div>`).join('')}</article>`;
  }).join('');
}
function syncGenderButtons(){
  const isMale=currentGender==='男';
  maleBtn.classList.toggle('active',isMale);
  femaleBtn.classList.toggle('active',!isMale);
}
function setGender(g){
  if(g===currentGender) return;
  currentGender=g;
  body.className=`names-page ${g==='男'?'theme-male':'theme-female'}`;
  syncGenderButtons();
  render();
}
function updateStickyState(){
  const compact = window.scrollY > 18;
  heroSection.classList.toggle('compact', compact);
}
[maleBtn,femaleBtn].forEach(btn=>btn.onclick=()=>setGender(btn.textContent.trim()==='男孩'?'男':'女'));
body.className='names-page theme-male';
syncGenderButtons();
render();
window.addEventListener('scroll', updateStickyState, {passive:true});
window.addEventListener('resize', updateStickyState);
updateStickyState();
'''
s = s[:start] + new_script + s[end:]
p.write_text(s, encoding='utf-8')
print('fixed names.html script to stable v24-like state')
