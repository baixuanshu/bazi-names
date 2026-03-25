from pathlib import Path
s = Path(r'D:\Projects\bazi-portal\base_names_full_from_transcript.html').read_text(encoding='utf-8')
s = s.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
Path(r'D:\Projects\bazi-portal\base_names_full_from_transcript_clean.html').write_text(s, encoding='utf-8')
print('cleaned', len(s))
