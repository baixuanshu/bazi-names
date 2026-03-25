from pathlib import Path
bp=Path(r'D:\Projects\bazi-portal\bazi-analysis.html')
raw=bp.read_bytes()
bs=raw.decode('latin1')
start=bs.find('function nameCard(r,p){')
end=bs.find('let modalGender=', start)
if start==-1 or end==-1:
    raise SystemExit('nameCard boundaries not found')
new_func='''function nameCard(r,p){ const mobile = window.innerWidth <= 720; const open = mobile ? isModalDetailOpen(p, r.name) : true; if(mobile){ return `<div class="name-item" data-name="${r.name}"><div class="subline"><div class="name-main"><div class="name-calligraphy" style="${patternStyle[p]}">${r.name}</div><span class="small">${r.pinyin}</span></div><div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px"><div class="score">${r.score} 分</div><button class="btn" type="button" data-detail-toggle="1" data-pattern="${p}" data-name="${r.name}" style="padding:8px 12px;font-size:12px">${open?'收起详情':'展开详情'}</button></div></div><div class="note" data-detail-body="1" style="display:${open?'block':'none'}"><b>五行：</b>${r.wuxing}<br><span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span><br><span class="reason"><b>评分理由：</b><strong>评分 ${r.score}</strong>：${r.reason.replace(/^评分\s*\d+[.:分]?/,'')}</span></div></div>`; } return `<div class="name-item"><div class="subline"><div class="name-main"><div class="name-calligraphy" style="${patternStyle[p]}">${r.name}</div><span class="small">${r.pinyin}</span></div><div class="score">${r.score} 分</div></div><div class="note"><b>五行：</b>${r.wuxing}<br><span class="source-detail"><b>出处详情：</b>${r.source}</span><br><span>组合意思：${r.meaning}</span><br><span class="reason"><b>评分理由：</b><strong>评分 ${r.score}</strong>：${r.reason.replace(/^评分\s*\d+[.:分]?/,'')}</span></div></div>`; }
'''
bs=bs[:start]+new_func+bs[end:]
old_css='.name-item{padding:16px 16px 14px;border:1px solid rgba(255,255,255,.08);box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 10px 26px rgba(0,0,0,.08);content-visibility:auto;contain:layout paint style;contain-intrinsic-size:220px}.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}'
new_css='.name-item{padding:16px 16px 14px;border:1px solid rgba(255,255,255,.08);box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 10px 26px rgba(0,0,0,.08);content-visibility:auto;contain:layout paint style;contain-intrinsic-size:220px}.name-main{flex:1 1 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.name-item .name-calligraphy{text-align:center;width:100%;font-size:42px;line-height:1.05;font-weight:800;letter-spacing:1.2px}.name-item .small{display:block;text-align:center;width:100%;margin-top:8px;color:#c9d3ea;font-size:14px}.name-item .note{margin-top:12px;padding-top:12px;border-top:1px dashed rgba(255,255,255,.08);line-height:1.78}.name-item .source-detail,.name-item .source-detail *{font-weight:800!important}.subline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.section-gap{margin-top:20px}'
if old_css not in bs:
    raise SystemExit('old css not found')
bs=bs.replace(old_css,new_css,1)
bp.write_text(bs, encoding='utf-8')
print('synced modal template from names utf8')
