import json
import pathlib
p = pathlib.Path(r'D:\.openclaw\agents\main\sessions\f6c16a4a-9421-4ba1-914c-85ab065700e4.jsonl')
for n, line in enumerate(p.open('r', encoding='utf-8'), 1):
    try:
        obj = json.loads(line)
    except Exception:
        continue
    msg = obj.get('message', {})
    if msg.get('role') != 'toolResult':
        continue
    text = ' '.join(part.get('text', '') for part in msg.get('content', []) if isinstance(part, dict))
    if (text.startswith('<!DOCTYPE html') or '</style></head><body class="names-page' in text) and ('hero-sticky' in text or 'page-sticky' in text):
        print(n, len(text), 'hero-sticky' in text, 'page-sticky' in text, 'genderScrollMemory' in text, 'maleBtnMirror' in text)
