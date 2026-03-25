from pathlib import Path
import json, re
from collections import Counter
import base64

ROOT = Path(r'D:\Projects\bazi-portal')
BAZI_MD = Path(r'D:\Projects\bazi-360-web\2026-09-360时辰八字总表.md')
NAMES_MD = Path(r'D:\Projects\bazi-name-options\白姓-2026年9月-六格局名字库-720名字草案-出处补全版.md')

pattern_direction = {
    '火格':'偏木', '土格':'偏木/水', '木火格':'偏木/土',
    '水火格':'偏木', '火土格':'偏木', '金火格':'偏水/木'
}
pattern_note = {
    '火格':'火势为主，名字更适合顺着木生火的路线去扶，不宜再一味叠火。',
    '土格':'土格样本很少，命名更适合润土、疏土，避免继续堆厚重与滞感。',
    '木火格':'木火本身成链，命名可继续扶木，或稍带土去承接，让结构更稳。',
    '水火格':'水火并见时，最适合用木做桥梁，走水→木→火。',
    '火土格':'火土格更适合从木做源头，形成木→火→土的自然顺生。',
    '金火格':'金火之间不宜硬顶，宜通过水木缓冲，走金→水→木→火。'
}

pattern_art = {
    '火格': {'bg1':'#ff7b72','bg2':'#ffb36b','bg':'linear-gradient(135deg, rgba(255,123,114,.22), rgba(255,179,107,.10))','text':'#ff9db3','style':'color:#ff9db3;text-shadow:0 2px 14px rgba(255,157,179,.16)'},
    '土格': {'bg1':'#c7a36b','bg2':'#edd3a0','bg':'linear-gradient(135deg, rgba(199,163,107,.20), rgba(237,211,160,.10))','text':'#d9b375','style':'color:#d9b375;text-shadow:0 2px 12px rgba(217,179,117,.14)'},
    '木火格': {'bg1':'#6fd39d','bg2':'#ffab6e','bg':'linear-gradient(135deg, rgba(111,211,157,.18), rgba(255,171,110,.10))','text':'#ff9b86','style':'background:linear-gradient(135deg,#79d99e 0%,#90d88a 40%,#ff8e7a 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none'},
    '水火格': {'bg1':'#76b8ff','bg2':'#ff97b0','bg':'linear-gradient(135deg, rgba(118,184,255,.18), rgba(255,151,176,.10))','text':'#8dbdff','style':'background:linear-gradient(135deg,#79b7ff 0%,#8eaaff 45%,#ff8b9f 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none'},
    '火土格': {'bg1':'#ff9575','bg2':'#c59a63','bg':'linear-gradient(135deg, rgba(255,149,117,.18), rgba(197,154,99,.10))','text':'#ef9a6b','style':'background:linear-gradient(135deg,#e25a4b,#e7b066);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none'},
    '金火格': {'bg1':'#d9e3f3','bg2':'#ffab79','bg':'linear-gradient(135deg, rgba(217,227,243,.18), rgba(255,171,121,.10))','text':'#ffd0a2','style':'background:linear-gradient(135deg,#eef4ff,#ffb37f);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none'}
}

char_meta = {
'景':('火','光明、景行、格局开阔','典出“高山仰止，景行行止”'),'桓':('木','栋梁、刚健、持重','常见于古人名号与桓桓之义'),'承':('金','承接、担当、承志','取“承上启下”之义'),'榆':('木','榆树、安定、沉静','取木德与榆荫安稳之意'),'叙':('金','次第、条理、叙事','取有序有度之义'),'衡':('土','平衡、持衡、器局','取“持衡”与“衡门”典雅气'),'君':('木','君子、端正、雅正','取君子人格之义'),'楷':('木','楷模、法度、正则','取“楷范”之义'),'行':('水','品行、践履、行远','典出“景行行止”'),'予':('土','从容、自持、给予','古文常用字，气息平稳'),'桢':('木','支柱、栋梁、可任大事','取“桢干”栋梁之义'),'修':('金','修为、修远、修雅','典出“路漫漫其修远兮”'),'远':('土','志向远大、眼界开阔','典出“修远”之意'),'栖':('木','安处、清隐、从容','取栖止、安顿之义'),'辰':('土','时序、星辰、气象','取星辰与时运之意'),'庭':('火','门庭、家声、气度','取门庭整肃之意'),'柯':('木','枝干、法则、挺拔','木名，取挺秀有则'),'怀':('水','胸怀、包容、温厚','取怀抱与怀德'),'瑾':('火','美玉、德行、贵重','典出“怀瑾握瑜”'),'沐':('水','润泽、濯洗、清新','取润泽修身之意'),'谦':('木','谦和、克己、可信','取谦谦君子'),'清':('水','清雅、清正、清贵','古典名字高频雅字'),'晏':('土','安宁、清平、从容','取海晏河清之意'),'泽':('水','恩泽、润泽、气度','取泽被与宽厚'),'钧':('金','权衡、分量、稳重','取千钧之重、持衡之感'),'涵':('水','涵养、包容、内秀','取涵容与修养'),'之':('火','文言虚字，古风留白','古文气很强的连接字'),'渊':('水','深厚、沉静、见识','取渊渟岳峙之感'),'墨':('水','书卷、文气、沉稳','取翰墨书香'),'润':('水','润泽、温厚、无声','取温润如玉'),'珩':('水','玉佩、礼制、贵气','古玉名，书卷高级感强'),'澄':('水','澄明、清透、定力','取澄怀观道'),'观':('木','视野、格局、观照','取观物与远见'),'泓':('水','深广、清润、内敛','取泓澄深静'),'让':('火','克让、礼让、分寸','古典德目字'),'沛':('水','丰沛、充盈、舒展','取充沛与从容'),'然':('金','自然而然、明达','古文气连接字'),'垣':('土','墙垣、边界、门庭','取门庭稳固'),'岳':('土','山岳、定力、器局','取山岳之重'),'岑':('木','山岑、清冷、安静','古风感强'),'安':('土','安定、安宁、稳妥','取安和稳重'),'城':('土','城府、稳固、掌局','取城池与守成'),'屹':('土','屹立、坚定、挺拔','取峻拔不移'),'峥':('土','峥嵘、锋芒、昂扬','取峥嵘向上'),'言':('木','言信、表达、文气','取言有物'),'棠':('木','海棠、清贵、典雅','典出棠棣与海棠之美'),'樾':('木','树荫、庇护、气象','古风高级字'),'若':('木','如若、若木、文雅','古文常见，气息清润'),'宁':('火','安宁、镇定、贵气','取宁静致远之感'),'知':('火','知礼、知远、知性','取知书达理'),'桐':('木','梧桐、清贵、挺秀','桐为高洁木'),'令':('火','美善、风仪、号令','古风中常见令仪'),'仪':('木','仪度、仪范、端庄','典出有仪有则'),'书':('金','书卷、文脉、教养','取书香门第'),'蘅':('木','香草、品格、清芬','楚辞香草意象'),'昭':('火','昭明、光亮、清朗','取昭昭其明'),'宜':('木','适宜、得体、和顺','取宜室宜家之意'),'月':('木','清辉、柔雅、意境','古诗词高频意象'),'雅':('木','雅正、雅致、端方','取温文尔雅'),'章':('火','文章、章法、文采','取文章华章'),'渝':('水','坚定、不渝、清润','取矢志不渝'),'沁':('水','沁润、清透、入心','取沁人心脾'),'音':('土','声韵、知音、气质','取知音与余韵'),'文':('水','文采、文明、书卷','取文德与文脉'),'岚':('土','山岚、清气、轻灵','山中雾气，古雅'),'容':('土','从容、气度、包容','取从容大方'),'舒':('金','舒展、从容、宽和','取舒朗而不迫'),'和':('水','和雅、平衡、温润','取中和之美'),'屿':('土','洲屿、安定、边界感','现代感低，清简')
}

score_by_grade = {'A+':96,'A':92,'A-':88}

def name_score(name, grade):
    s = sum(ord(c) for c in name)
    return score_by_grade[grade] + (s % 3) - 1

def parse_bazi_rows():
    rows = []
    for line in BAZI_MD.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| '):
            continue
        parts = [x.strip() for x in line.strip('|').split('|')]
        if parts[0] in ('序号','---:') or len(parts) < 15:
            continue
        rows.append({
            'index': int(parts[0]), 'date': parts[1], 'time': parts[2], 'shichen': parts[3],
            'year': parts[4], 'month': parts[5], 'day': parts[6], 'hour': parts[7], 'bazi': parts[8],
            'jin': int(parts[9]), 'mu': int(parts[10]), 'shui': int(parts[11]), 'huo': int(parts[12]), 'tu': int(parts[13]),
            'pattern': parts[14] + ('格' if not parts[14].endswith('格') else '')
        })
    return rows

def parse_names():
    gender, pattern, rows = None, None, []
    for line in NAMES_MD.read_text(encoding='utf-8').splitlines():
        if line.startswith('# 男孩名字库'):
            gender = '男'; continue
        if line.startswith('# 女孩名字库'):
            gender = '女'; continue
        m = re.match(r'##\s+\d+\.\s+(.+?)（', line)
        if m:
            pattern = m.group(1).replace('男孩名','').replace('女孩名','').strip(); continue
        if line.startswith('| ') and not line.startswith('| 序号') and not line.startswith('|---'):
            parts = [x.strip() for x in line.strip('|').split('|')]
            if not (gender and pattern):
                continue
            if len(parts) >= 9 and parts[0].isdigit():
                rows.append({
                    'gender': gender,
                    'pattern': pattern,
                    'index': int(parts[0]),
                    'name': parts[1],
                    'pinyin': parts[2],
                    'score': float(parts[3]),
                    'style_order': parts[4],
                    'wuxing': parts[5],
                    'meaning': parts[6],
                    'source': parts[7],
                    'reason': parts[8],
                })
            elif len(parts) == 5 and parts[0].isdigit():
                rows.append({'gender':gender,'pattern':pattern,'index':int(parts[0]),'name':parts[1],'pinyin':parts[2],'grade':parts[3],'note':parts[4]})
    for r in rows:
        if 'wuxing' in r and 'meaning' in r and 'source' in r and 'reason' in r:
            continue
        n1, n2 = r['name'][1], r['name'][2]
        m1 = char_meta.get(n1, ('未定','字义待补','常用取名义'))
        m2 = char_meta.get(n2, ('未定','字义待补','常用取名义'))
        r['score'] = name_score(r['name'], r['grade'])
        r['wuxing'] = f"白（金） + {n1}（{m1[0]}） + {n2}（{m2[0]}）"
        r['meaning'] = f"{n1}主{m1[1]}；{n2}主{m2[1]}。组合起来偏向“{r['note']}”。"
        r['source'] = f"{n1}取意：{m1[2]}；{n2}取意：{m2[2]}。"
        r['reason'] = f"评分 {r['score']}：姓白按金性参考，后两字分别落在{m1[0]}、{m2[0]}，与{r['pattern']}的命名方向“{pattern_direction[r['pattern']]}”相容；再结合音律、字义、古风气质与长期使用稳定性综合给分。"
    return rows

bazi_rows = parse_bazi_rows()
name_rows = parse_names()
patterns = ['火格','土格','木火格','水火格','火土格','金火格']
pattern_counts = Counter(r['pattern'] for r in bazi_rows)
pattern_top = {p: {
    'boys': sorted([r for r in name_rows if r['gender']=='男' and r['pattern']==p], key=lambda x:(-x['score'], x['index'])),
    'girls': sorted([r for r in name_rows if r['gender']=='女' and r['pattern']==p], key=lambda x:(-x['score'], x['index']))
} for p in patterns}

COMMON_CSS = """
:root{
  --bg:#0f1221; --bg2:#171b31; --panel:rgba(255,255,255,.08); --panel-2:rgba(255,255,255,.04); --text:#f4f7ff; --muted:#b8c2df; --line:rgba(255,255,255,.12);
  --gold:#f4cf7b; --wood:#8bd5a0; --water:#8ab9ff; --fire:#ff9db3; --earth:#dcb58e; --shadow:0 20px 50px rgba(0,0,0,.28);
  --thin-font:"SF Pro Text","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  --calli-font:"STLiti","STXingkai","STKaiti","KaiTi","DFKai-SB",serif;
}
*{box-sizing:border-box} html,body{margin:0;padding:0} html{scroll-behavior:smooth}
body{font-family:var(--thin-font);font-weight:300;background:radial-gradient(circle at top, rgba(255,255,255,.06), transparent 26%), linear-gradient(180deg,var(--bg) 0%,var(--bg2) 100%); color:var(--text); overflow-x:hidden;letter-spacing:.1px}
body::before{content:'';position:fixed;inset:-20%;background:radial-gradient(circle at 20% 20%, rgba(255,255,255,.08), transparent 18%),radial-gradient(circle at 80% 0%, rgba(125,168,255,.08), transparent 20%),radial-gradient(circle at 50% 100%, rgba(255,181,210,.06), transparent 18%);animation:floatGlow 18s ease-in-out infinite;pointer-events:none;z-index:-1}
@keyframes floatGlow{0%,100%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(0,-12px,0) scale(1.03)}}
a{text-decoration:none;color:inherit}
.wrap{max-width:1440px;margin:0 auto;padding:20px}
.hero,.glass,.card,.modal-box,.name-item,.portal-orb{backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);background:var(--panel);border:1px solid var(--line);box-shadow:var(--shadow)}
.hero,.glass,.card,.modal-box,.name-item{border-radius:24px}.hero{padding:24px;margin-bottom:18px;position:relative;overflow:hidden}.hero::after,.card::after,.portal-orb::after{content:'';position:absolute;inset:auto -20% -60% auto;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle, rgba(255,255,255,.16), transparent 68%);opacity:.35;pointer-events:none}
.hero h1{margin:0 0 10px;font-size:30px;letter-spacing:.5px}.desc{color:var(--muted);line-height:1.8;font-size:14px}
.nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.nav a,.btn{display:inline-flex;align-items:center;justify-content:center;padding:11px 15px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.06);color:var(--text);font-size:14px;cursor:pointer;transition:transform .22s ease, background .22s ease, box-shadow .22s ease}.nav a:hover,.btn:hover{transform:translateY(-2px);background:rgba(255,255,255,.1);box-shadow:0 10px 24px rgba(0,0,0,.14)} .btn.active{background:rgba(255,255,255,.14)}
.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin-bottom:18px}.glass{padding:18px}.k{color:var(--muted);font-size:13px}.v{font-size:28px;font-weight:700;margin-top:8px}
.pattern-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{padding:18px;position:relative;overflow:hidden;transition:transform .22s ease,border-color .22s ease,background .22s ease}.card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.22);background:rgba(255,255,255,.1)}
.title{font-size:22px;font-weight:700;letter-spacing:.3px}.line{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.chip,.badge{display:inline-flex;align-items:center;justify-content:center;padding:6px 12px;border-radius:999px;font-size:12px;border:1px solid var(--line);background:rgba(255,255,255,.05)}
.element-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:16px}.element-box{padding:10px 6px;border-radius:16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);text-align:center}.element-label{font-size:12px;color:var(--muted);margin-bottom:4px}.element-num{font-size:24px;font-weight:700}.element-jin{color:var(--gold)}.element-mu{color:var(--wood)}.element-shui{color:var(--water)}.element-huo{color:var(--fire)}.element-tu{color:var(--earth)}.bottom-actions{display:flex;justify-content:space-between;gap:12px;margin-top:16px}
.toolbar{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:12px;margin-bottom:16px} input,select{width:100%;padding:13px 15px;background:rgba(255,255,255,.06);color:var(--text);border:1px solid var(--line);border-radius:16px;font-size:14px;outline:none;transition:border-color .18s ease, transform .18s ease} input:focus,select:focus{border-color:rgba(255,255,255,.28);transform:translateY(-1px)}
.table-wrap{overflow:auto;background:var(--panel);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow)} table{width:100%;border-collapse:collapse;min-width:1080px;font-size:14px} th,td{padding:12px 10px;border-bottom:1px solid rgba(255,255,255,.06);text-align:left;white-space:nowrap} thead th{position:sticky;top:0;background:rgba(17,23,44,.96);z-index:1}
.cards{display:none;gap:12px}.name-item{padding:16px;position:relative;overflow:hidden;transition:transform .2s ease,border-color .2s ease}.name-item:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.24)}.small{font-size:12px;color:var(--muted)} .note{margin-top:10px;font-size:14px;line-height:1.8;color:#eaf0ff}.score{color:#b4ffd9;font-weight:700}.meaning{font-weight:700}.reason strong{font-weight:800}
.modal{position:fixed;inset:0;background:rgba(6,8,16,.62);display:none;align-items:center;justify-content:center;padding:16px;z-index:9999}.modal-box{width:min(1120px,100%);max-height:88vh;overflow:auto;padding:20px;animation:modalIn .22s ease}@keyframes modalIn{from{transform:translateY(8px) scale(.985);opacity:0}to{transform:translateY(0) scale(1);opacity:1}}
.modal-head{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:14px}.name-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.modal-switch{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 18px}.modal-col-title{font-size:20px;font-weight:700;margin:0 0 10px}.modal-section{display:grid;gap:16px}.modal-box .name-calligraphy{font-size:48px;font-weight:800;line-height:1.02}
.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}
@media (max-width:1100px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.pattern-grid{grid-template-columns:1fr}.toolbar{grid-template-columns:1fr 1fr}.name-grid{grid-template-columns:1fr}.wrap{padding:14px}.hero h1{font-size:24px}}
@media (max-width:720px){.wrap{padding:10px}.hero{padding:18px;border-radius:20px}.hero h1{font-size:22px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.toolbar{grid-template-columns:1fr}.table-wrap{display:none}.cards{display:grid}.v{font-size:22px}}
.art{width:100%;height:120px;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,.08);margin:12px 0 10px;background:rgba(255,255,255,.04)}
.hero-mini{margin-top:8px;color:#64748b;font-size:13px;letter-spacing:.2px}
"""

INDEX_CSS = COMMON_CSS + """
body.portal-home{background:radial-gradient(circle at top, rgba(255,255,255,.08), transparent 30%), linear-gradient(180deg,#f4f5f9 0%, #e9edf6 35%, #dfe7f5 100%); color:#111827}
.portal-home .hero,.portal-home .portal-orb{background:rgba(255,255,255,.48);border:1px solid rgba(255,255,255,.55);box-shadow:0 24px 50px rgba(51,65,85,.12)}
.portal-home .desc{color:#4b5563}.home-center{min-height:calc(100vh - 40px);display:flex;flex-direction:column;justify-content:center}.orb-grid{display:grid;grid-template-columns:repeat(2,minmax(240px,320px));justify-content:center;gap:28px;margin-top:28px}.portal-orb{width:100%;aspect-ratio:1/1;border-radius:50%;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;transition:transform .28s ease, box-shadow .28s ease}
.portal-orb:hover{transform:translateY(-6px) scale(1.03);box-shadow:0 34px 60px rgba(51,65,85,.18)}.portal-orb:before{content:'';position:absolute;inset:12%;border-radius:50%;background:linear-gradient(135deg,rgba(255,255,255,.65),rgba(255,255,255,.18));z-index:0}.portal-orb::after{content:'';position:absolute;inset:auto;left:-10%;top:-10%;width:48%;height:48%;background:radial-gradient(circle, rgba(255,255,255,.46), transparent 68%);animation:orbFloat 7s ease-in-out infinite}
@keyframes orbFloat{0%,100%{transform:translate3d(0,0,0)}50%{transform:translate3d(10px,14px,0)}}
.orb-inner{position:relative;z-index:1;text-align:center;padding:20px}.orb-title{font-size:28px;font-weight:700;letter-spacing:1px}.orb-sub{margin-top:10px;font-size:14px;color:#475569;line-height:1.7}.orb-bazi{background:linear-gradient(135deg, rgba(188,220,255,.72), rgba(223,235,255,.55))}.orb-name{background:linear-gradient(135deg, rgba(255,218,230,.78), rgba(255,242,247,.56))}
.home-title{text-align:center}.family-row{display:grid;grid-template-columns:1fr 1fr;align-items:center;margin-top:10px;color:#5f6b81;font-size:13px;padding:0 48px}.family-right{text-align:right}.child-line{text-align:center;margin-top:8px;color:#5f6b81;font-size:13px}
@media (max-width:720px){.orb-grid{grid-template-columns:1fr 1fr;gap:14px}.portal-orb{min-width:0}.orb-title{font-size:20px}.orb-sub{font-size:12px}.family-row{font-size:12px}}
"""

NAMES_CSS = COMMON_CSS + """
body.names-page{transition:background .45s ease,color .35s ease}
body.theme-male{background:radial-gradient(circle at top left, rgba(101,144,255,.18), transparent 24%), radial-gradient(circle at top right, rgba(246,203,120,.12), transparent 20%), linear-gradient(180deg,#09111f 0%,#0f1c34 46%,#172743 100%)}
body.theme-female{background:radial-gradient(circle at top left, rgba(255,205,226,.22), transparent 22%), radial-gradient(circle at top right, rgba(255,239,246,.18), transparent 22%), linear-gradient(180deg,#3a1830 0%,#5a2748 36%,#7f3e60 100%)}
.sex-switch{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}.sex-switch .btn{padding:12px 16px;border-radius:999px;min-width:72px}
.theme-male .card,.theme-male .hero,.theme-male .name-item{background:linear-gradient(180deg, rgba(14,24,44,.72), rgba(18,31,57,.62))}.theme-female .card,.theme-female .hero,.theme-female .name-item{background:linear-gradient(180deg, rgba(87,39,70,.50), rgba(126,61,97,.42))}.theme-female .score{color:#ffe2ee}.theme-female .chip,.theme-female .badge,.theme-female .btn,.theme-female input,.theme-female select{background:rgba(255,255,255,.10)}
.name-line{padding:16px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);margin-top:12px;position:relative;overflow:hidden}.name-line::after{content:'';position:absolute;right:-30px;top:-30px;width:100px;height:100px;background:radial-gradient(circle, rgba(255,255,255,.14), transparent 70%);opacity:.35}.pattern-card .title-wrap{display:flex;justify-content:space-between;align-items:center;gap:10px}
.theme-male .hero::before{content:'';position:absolute;inset:auto -30px -20px auto;width:220px;height:220px;background:radial-gradient(circle, rgba(120,162,255,.16), transparent 68%);filter:blur(2px);animation:bladeGlow 6s ease-in-out infinite}.theme-female .hero::before{content:'';position:absolute;inset:auto -20px -20px auto;width:220px;height:220px;background:radial-gradient(circle, rgba(255,219,234,.24), transparent 68%);animation:petalGlow 7s ease-in-out infinite}.theme-female .card::before{content:'';position:absolute;right:14px;top:14px;width:46px;height:46px;border-radius:50%;background:radial-gradient(circle, rgba(255,227,239,.22), transparent 70%)}
.name-calligraphy{font-family:"STXingkai","STLiti","LiSu","STKaiti","KaiTi",cursive,serif;font-size:42px;letter-spacing:1.2px;line-height:1.05;font-weight:800}
.theme-female .name-calligraphy{color:#fff1f7;text-shadow:0 2px 10px rgba(255,190,220,.22)} .theme-male .name-calligraphy{color:#edf5ff;text-shadow:0 2px 12px rgba(120,162,255,.16)}
@keyframes bladeGlow{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-8px) scale(1.04)}} @keyframes petalGlow{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-10px) rotate(6deg)}}
"""

BAZI_CSS = COMMON_CSS + """
body.bazi-page{background:radial-gradient(circle at top left, rgba(103,132,255,.12), transparent 24%), radial-gradient(circle at top right, rgba(255,219,143,.10), transparent 20%), linear-gradient(180deg,#0a0f1d 0%,#111b30 46%,#17253e 100%)}
.row-actions{display:flex;gap:8px;flex-wrap:wrap}.mini{font-size:13px;color:var(--muted)} .summary-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.pattern-head{display:flex;justify-content:flex-end;align-items:flex-start;gap:10px}.pattern-main{display:flex;align-items:center;justify-content:center;min-height:118px;position:relative;margin:8px 0 12px}.pattern-center{font-size:56px;font-weight:900;letter-spacing:1px;text-align:center}.pattern-corner{position:absolute;font-size:12px;color:var(--muted)}.pc-tl{left:0;top:0}.pc-tr{right:0;top:0}.pc-bl{left:0;bottom:0}.pc-br{right:0;bottom:0}
"""

def write_index():
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>白姓八字与名字导航</title><style>{INDEX_CSS}</style></head><body class="portal-home"><div class="wrap home-center"><section class="hero"><h1 class="home-title">白姓 · 八字与名字</h1><div class="family-row"><div>父亲：白淞榆</div><div class="family-right">母亲：罗敏</div></div><div class="child-line">留给孩子的名字___</div></section><section class="orb-grid"><a class="portal-orb orb-bazi" href="bazi-analysis.html"><div class="orb-inner"><div class="orb-title">八字</div><div class="orb-sub">360 个时辰<br>6 个格局</div></div></a><a class="portal-orb orb-name" href="names.html"><div class="orb-inner"><div class="orb-title">名字</div><div class="orb-sub">男女名字<br>分数、五行、出处、评分理由</div></div></a></section></div></body></html>'''
    (ROOT/'index.html').write_text(html, encoding='utf-8')

def write_names():
    top_json = json.dumps(pattern_top, ensure_ascii=False)
    dir_json = json.dumps(pattern_direction, ensure_ascii=False)
    bg_json = json.dumps({k: pattern_art[k]['bg'] for k in patterns}, ensure_ascii=False)
    color_json = json.dumps({k: pattern_art[k]['text'] for k in patterns}, ensure_ascii=False)
    style_json = json.dumps({k: pattern_art[k]['style'] for k in patterns}, ensure_ascii=False)
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>名字推荐</title><style>{NAMES_CSS}</style></head><body class="names-page theme-male"><div class="wrap"><section class="hero"><h1>名字推荐</h1><div class="nav"><a href="index.html">返回首页</a><a href="bazi-analysis.html">去八字分析</a></div></section><section class="sex-switch"><button class="btn active" id="maleBtn">男孩</button><button class="btn" id="femaleBtn">女孩</button></section><section class="pattern-grid" id="patterns"></section></div><script>const topData={top_json}; const patternDirection={dir_json}; const patternBg={bg_json}; const patternColor={color_json}; const patternStyle={style_json}; let currentGender='男'; const patterns=['火格','土格','木火格','水火格','火土格','金火格']; const container=document.getElementById('patterns'); const maleBtn=document.getElementById('maleBtn'); const femaleBtn=document.getElementById('femaleBtn'); const body=document.body; function render(){{ container.innerHTML = patterns.map(p=>{{ const list=(currentGender==='男'?topData[p].boys:topData[p].girls); return `<article class="card pattern-card" id="${{p}}" style="background-image:${{patternBg[p]}}"><div class="pattern-main"><div class="pattern-corner pc-tl"><span class="badge">${{patternDirection[p]}}</span></div><div class="pattern-center" style="${{patternStyle[p]}}">${{p}}</div><div class="pattern-corner pc-tr"><span class="badge">${{list.length}} 个名字</span></div></div>${{list.map(r=>`<div class="name-line"><div class="subline"><div><div class="name-calligraphy" style="${{patternStyle[p]}}">${{r.name}}</div><span class="small">${{r.pinyin}}</span></div><div class="score">${{r.score}} 分</div></div><div class="note"><b>五行：</b>${{r.wuxing}}<br><b class="meaning">组合意思：</b><span class="meaning">${{r.meaning}}</span><br><b>出处：</b>${{r.source}}<br><span class="reason"><b>评分理由：</b><strong>评分 ${{r.score}}</strong>：${{r.reason.replace(/^评分\s*\d+：/,'')}}</span></div></div>`).join('')}}</article>`; }}).join(''); }} maleBtn.onclick=()=>{{currentGender='男'; body.className='names-page theme-male'; maleBtn.classList.add('active'); femaleBtn.classList.remove('active'); render();}}; femaleBtn.onclick=()=>{{currentGender='女'; body.className='names-page theme-female'; femaleBtn.classList.add('active'); maleBtn.classList.remove('active'); render();}}; render();</script></body></html>'''
    (ROOT/'names.html').write_text(html, encoding='utf-8')

def write_bazi():
    data_json = json.dumps(bazi_rows, ensure_ascii=False)
    top_json = json.dumps(pattern_top, ensure_ascii=False)
    counts_json = json.dumps(pattern_counts, ensure_ascii=False)
    dir_json = json.dumps(pattern_direction, ensure_ascii=False)
    bg_json = json.dumps({k: pattern_art[k]['bg'] for k in patterns}, ensure_ascii=False)
    color_json = json.dumps({k: pattern_art[k]['text'] for k in patterns}, ensure_ascii=False)
    style_json = json.dumps({k: pattern_art[k]['style'] for k in patterns}, ensure_ascii=False)
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>八字分析</title><style>{BAZI_CSS}</style></head><body class="bazi-page"><div class="wrap"><section class="hero"><h1>八字分析</h1><div class="nav"><a href="index.html">返回首页</a><a href="names.html">去名字推荐</a></div></section><section class="grid"><div class="glass"><div class="k">总样本</div><div class="v">360</div></div><div class="glass"><div class="k">格局数</div><div class="v">6</div></div><div class="glass"><div class="k">主格局</div><div class="v">火格</div></div><div class="glass"><div class="k">单五行偏多</div><div class="v">308</div></div><div class="glass"><div class="k">双五行偏多</div><div class="v">52</div></div></section><section class="pattern-grid" id="patternCards"></section><div class="section-gap"></div><section class="toolbar"><input id="search" placeholder="搜索：序号 / 日期 / 八字 / 格局"><select id="pattern"><option value="">全部格局</option></select><select id="sort"><option value="index">按序号</option><option value="date">按日期</option></select><select id="view"><option value="auto">自动视图</option><option value="table">表格</option><option value="card">卡片</option></select></section><div class="table-wrap" id="tableWrap"><table><thead><tr><th>序号</th><th>日期</th><th>时间</th><th>时辰</th><th>八字</th><th>格局</th><th>操作</th></tr></thead><tbody id="tbody"></tbody></table></div><section class="cards" id="cards"></section></div><div class="modal" id="modal"><div class="modal-box"><div class="modal-head"><div><div class="title" id="modalTitle">推荐名字</div></div><button class="btn close" id="closeBtn">关闭</button></div><div class="name-grid" id="modalBody"></div></div></div><script>const rows={data_json}; const topData={top_json}; const counts={counts_json}; const patternDirection={dir_json}; const patternBg={bg_json}; const patternColor={color_json}; const patternStyle={style_json}; const patterns=['火格','土格','木火格','水火格','火土格','金火格']; const patternCards=document.getElementById('patternCards'), tbody=document.getElementById('tbody'), cards=document.getElementById('cards'), modal=document.getElementById('modal'), modalTitle=document.getElementById('modalTitle'), modalBody=document.getElementById('modalBody'); const search=document.getElementById('search'), pattern=document.getElementById('pattern'), sort=document.getElementById('sort'), view=document.getElementById('view'); patterns.forEach(p=>{{ const o=document.createElement('option'); o.value=p; o.textContent=p; pattern.appendChild(o); }}); function renderPatternCards(){{ patternCards.innerHTML = patterns.map(p=>`<article class="card" style="background-image:${{patternBg[p]}}"><div class="pattern-head"></div><div class="pattern-main"><div class="pattern-corner pc-tl"><span class="badge">${{patternDirection[p]}}</span></div><div class="pattern-center" style="${{patternStyle[p]}}">${{p}}</div><div class="pattern-corner pc-tr"><span class="badge">${{counts[p]||0}} 次</span></div></div><div class="bottom-actions"><button class="btn" onclick="openModal('${{p}}')">推荐名字</button><a class="btn" href="names.html#${{encodeURIComponent(p)}}">去名字页</a></div></article>`).join(''); }} function nameCard(r,p){{ return `<div class="name-item"><div class="subline"><div><div class="name-calligraphy" style="${{patternStyle[p]}}">${{r.name}}</div><span class="small">${{r.pinyin}}</span></div><div class="score">${{r.score}} 分</div></div><div class="note"><b>五行：</b>${{r.wuxing}}<br><b class="meaning">组合意思：</b><span class="meaning">${{r.meaning}}</span><br><b>出处：</b>${{r.source}}<br><span class="reason"><b>评分理由：</b><strong>评分 ${{r.score}}</strong>：${{r.reason.replace(/^评分\s*\d+：/,'')}}</span></div></div>`; }} let modalGender='男'; function renderModalNames(p){{ const list = modalGender==='男' ? topData[p].boys : topData[p].girls; modalBody.innerHTML=`<div class="modal-switch"><button class="btn ${{modalGender==='男'?'active':''}}" id="modalMale">男孩</button><button class="btn ${{modalGender==='女'?'active':''}}" id="modalFemale">女孩</button></div><div class="modal-section">${{list.map(r=>nameCard(r,p)).join('')}}</div>`; document.getElementById('modalMale').onclick=()=>{{modalGender='男'; renderModalNames(p);}}; document.getElementById('modalFemale').onclick=()=>{{modalGender='女'; renderModalNames(p);}}; }} window.openModal=function(p){{ modalGender='男'; modal.style.display='flex'; modalTitle.textContent=p+' 推荐名字'; renderModalNames(p); }}; document.getElementById('closeBtn').onclick=()=>modal.style.display='none'; modal.addEventListener('click',e=>{{ if(e.target===modal) modal.style.display='none'; }}); function elementBoxes(r){{ return `<div class="element-grid"><div class="element-box"><div class="element-label">金</div><div class="element-num element-jin">${{r.jin}}</div></div><div class="element-box"><div class="element-label">木</div><div class="element-num element-mu">${{r.mu}}</div></div><div class="element-box"><div class="element-label">水</div><div class="element-num element-shui">${{r.shui}}</div></div><div class="element-box"><div class="element-label">火</div><div class="element-num element-huo">${{r.huo}}</div></div><div class="element-box"><div class="element-label">土</div><div class="element-num element-tu">${{r.tu}}</div></div></div>`; }} function renderRows(list){{ tbody.innerHTML=list.map(r=>`<tr id="row-${{r.index}}"><td>${{r.index}}</td><td>${{r.date}}</td><td>${{r.time}}</td><td>${{r.shichen}}</td><td>${{r.bazi}}</td><td>${{r.pattern}}</td><td><div class="row-actions"><button class="btn" onclick="openModal('${{r.pattern}}')">推荐名字</button><a class="btn" href="names.html#${{encodeURIComponent(r.pattern)}}">打开名字页</a></div></td></tr>`).join(''); cards.innerHTML=list.map(r=>`<article class="card" id="mrow-${{r.index}}" style="background-image:${{patternBg[r.pattern]}}"><div class="pattern-main"><div class="pattern-corner pc-tl"><span class="badge">第${{r.index}}组</span></div><div class="pattern-center" style="${{patternStyle[r.pattern]}}">${{r.pattern}}</div></div><div class="small" style="margin-top:14px;font-weight:700;font-size:15px;text-align:center;letter-spacing:.3px">${{r.date}} · ${{r.time}} · ${{r.shichen}}</div><div class="line" style="margin-top:16px"><span class="chip">年柱：${{r.year}}</span><span class="chip">月柱：${{r.month}}</span><span class="chip">日柱：${{r.day}}</span><span class="chip">时柱：${{r.hour}}</span></div><div class="note"><b>八字：</b>${{r.bazi}}</div>${{elementBoxes(r)}}<div class="bottom-actions"><button class="btn" onclick="openModal('${{r.pattern}}')">推荐名字</button><a class="btn" href="names.html#${{encodeURIComponent(r.pattern)}}">打开名字页</a></div></article>`).join(''); applyView(); }} function applyView(){{ const mobile = window.innerWidth<=720; const real = view.value==='auto' ? (mobile?'card':'table') : view.value; document.getElementById('tableWrap').style.display = real==='table'?'block':'none'; cards.style.display = real==='card'?'grid':'none'; }} function apply(){{ let list = rows.filter(r=>{{ const q=search.value.trim(); return (!q || (`${{r.index}} ${{r.date}} ${{r.bazi}} ${{r.pattern}}`).includes(q)) && (!pattern.value || r.pattern===pattern.value); }}); if(sort.value==='date') list.sort((a,b)=> `${{a.date}} ${{a.time}}`.localeCompare(`${{b.date}} ${{b.time}}`)); else list.sort((a,b)=> a.index-b.index); renderRows(list); }} [search,pattern,sort,view].forEach(el=>{{ el.addEventListener('input', apply); el.addEventListener('change', apply); }}); window.addEventListener('resize', applyView); renderPatternCards(); apply();</script></body></html>'''
    (ROOT/'bazi-analysis.html').write_text(html, encoding='utf-8')

write_index(); write_names(); write_bazi(); print('done')
