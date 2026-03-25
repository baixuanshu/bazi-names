import json
import pathlib
import subprocess

root = pathlib.Path(r'D:\Projects\bazi-portal')
transcript = pathlib.Path(r'D:\.openclaw\agents\main\sessions\f6c16a4a-9421-4ba1-914c-85ab065700e4.jsonl')

# 1) regenerate the original file base
subprocess.run(['python', str(root / 'build_portal.py')], check=True)

# 2) collect names.html edits from transcript
edits = []
for line in transcript.open('r', encoding='utf-8'):
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
        if path.endswith('names.html'):
            old = args.get('old_string') or args.get('oldText') or ''
            new = args.get('new_string') or args.get('newText') or ''
            edits.append((old, new))

# 3) apply only edits before the bug-introducing one (1..25)
target = root / 'names.html'
text = target.read_text(encoding='utf-8')
for i, (old, new) in enumerate(edits[:25], start=1):
    if old not in text:
        raise SystemExit(f'FAILED at edit #{i}: old text not found')
    text = text.replace(old, new, 1)

target.write_text(text, encoding='utf-8')
print('restored names.html to pre-bug state using transcript edits 1-25')
