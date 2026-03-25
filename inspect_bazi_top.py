from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\bazi-analysis.html').read_text(encoding='utf-8')
for t in ['<section class="hero', '八字分析', '返回首页', '去名字推荐', 'analysisHero', 'updateAnalysisSticky']:
    i = s.find(t)
    print('TOKEN', t, 'IDX', i)
    if i >= 0:
        print(s[i:i+500])
        print('---')
