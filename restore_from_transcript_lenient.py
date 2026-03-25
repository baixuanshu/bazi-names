import json
import pathlib

TRANSCRIPT = pathlib.Path(r'D:\.openclaw\agents\main\sessions\f6c16a4a-9421-4ba1-914c-85ab065700e4.jsonl')
ROOT = pathlib.Path(r'D:\Projects\bazi-portal')


def norm(s: str) -> str:
    return s.replace('\r\n', '\n').replace('\r', '\n')


def collect_edits(target_name):
    out = []
    for line in TRANSCRIPT.open('r', encoding='utf-8'):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        msg = obj.get('message', {})
        if msg.get('role') != 'assistant':
            continue
        for c in msg.get('content', []):
            if c.get('type') != 'toolCall' or c.get('name') != 'edit':
                continue
            args = c.get('arguments', {})
            path = (args.get('file_path') or args.get('path') or '').lower()
            if path.endswith(target_name.lower()):
                out.append((norm(args.get('old_string') or args.get('oldText') or ''), norm(args.get('new_string') or args.get('newText') or '')))
    return out

text = norm((ROOT / 'base_names_full_from_transcript_clean.html').read_text(encoding='utf-8'))
applied, skipped = [], []
for idx, (old, new) in enumerate(collect_edits('names.html')[:25], start=1):
    pos = text.find(old)
    if pos >= 0:
        text = text[:pos] + new + text[pos+len(old):]
        applied.append(idx)
    else:
        skipped.append(idx)

(ROOT / 'names.html').write_text(text, encoding='utf-8', newline='\n')
print('applied', applied)
print('skipped', skipped)
