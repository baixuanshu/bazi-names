from pathlib import Path
import re

names = Path(r'D:\Projects\bazi-portal\names.html')
text = names.read_text(encoding='utf-8', errors='ignore')

text = text.replace("const genderScrollMemory = { 男: null, 女: null };\n", "")
text = text.replace("const genderScrollMemory = { ��: null, Ů: null };\n", "")
text = re.sub(r"function restoreGenderScroll\(g\)\{.*?\}\n", "", text, flags=re.S)
text = re.sub(r"function setGender\(g\)\{ if\(g===currentGender\) return;.*?requestAnimationFrame\(\(\)=>restoreGenderScroll\(g\)\); \}\n", "function setGender(g){ if(g===currentGender) return; currentGender=g; body.className=`names-page ${g==='男'?'theme-male':'theme-female'}`; syncGenderButtons(); render(); }\n", text, flags=re.S)
text = re.sub(r"function setGender\(nextGender\)\{.*?requestAnimationFrame\(\(\) => window\.scrollTo\(0, genderScrollMemory\[nextGender\] \?\? 0\)\);\n\}\n", "function setGender(nextGender){ if(nextGender===currentGender) return; currentGender=nextGender; syncButtons(); render(); }\n", text, flags=re.S)
text = text.replace("currentGender='��'", "currentGender='男'")
text = text.replace("'Ů'", "'女'")
text = text.replace("'��'", "'男'")
text = text.replace("==='男'", "==='男'")

names.write_text(text, encoding='utf-8')
print('patched names.html toward v24-safe state')
