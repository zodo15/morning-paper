#!/usr/bin/env python3
"""Chunk Ed53 audio scripts at sentence boundaries, each chunk < 4096 chars.
No chunk ends on a short heading-like sentence when more text follows in the same output
(Kore trailing-heading stutter guard). Writes chunks + manifest.json to /downloads/ed53audio/chunks/.
full.txt is NOT chunked for synthesis: it is the exact concatenation of segments 1-8,
so the manifest maps it onto the segment chunks (synthesize=false)."""
import json, os, re, io

SRC = '/downloads/ed53audio'
OUT = '/downloads/ed53audio/chunks'
LIMIT = 4096
os.makedirs(OUT, exist_ok=True)

def sentences(t):
    parts = re.split(r'(?<=[.!?]) ', t.strip())
    return [p for p in parts if p]

def heading_like(s):
    # short, no comma, ends with period, looks like a title/heading rather than a full sentence
    w = s.split()
    return len(s) < 90 and len(w) <= 9 and ',' not in s

def chunk(name, text):
    sens = sentences(text)
    chunks, cur = [], ''
    for s in sens:
        cand = (cur + ' ' + s).strip()
        if cur and len(cand) > LIMIT:
            chunks.append(cur)
            cur = s
        else:
            cur = cand
    if cur:
        chunks.append(cur)
    # trailing-heading guard: relocate a heading-like trailing sentence to the next chunk's head
    i = 0
    while i < len(chunks) - 1:
        c = chunks[i]
        cs = sentences(c)
        if len(cs) > 1 and heading_like(cs[-1]):
            moved = cs[-1]
            chunks[i] = ' '.join(cs[:-1])
            chunks[i+1] = (moved + ' ' + chunks[i+1]).strip()
        else:
            i += 1
    files = []
    for n, c in enumerate(chunks, start=1):
        fn = f'{name}-c{n:02d}.txt'
        with io.open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
            f.write(c + '\n')
        files.append(fn)
    return files

labels = {e['key']: e['label'] for e in json.load(open(os.path.join(SRC, 'labels.json')))}
manifest = {'edition': 53, 'limit_chars': LIMIT, 'rule': 'sentence boundaries; no trailing heading sentences; full = exact concatenation of segments 1-8, do not synthesize separately',
            'outputs': {}}
seg_chunk_lists = []
for n in range(1, 9):
    key = f'segment{n}'
    text = io.open(os.path.join(SRC, key + '.txt'), encoding='utf-8').read()
    files = chunk(key, text)
    manifest['outputs'][key] = {'label': labels.get(key, ''), 'chunks': files}
    seg_chunk_lists += files

for key in ('quick', 'lr-full'):
    text = io.open(os.path.join(SRC, key + '.txt'), encoding='utf-8').read()
    files = chunk(key, text)
    manifest['outputs'][key] = {'label': 'Quick read' if key == 'quick' else 'Long read', 'chunks': files}

full_text = io.open(os.path.join(SRC, 'full.txt'), encoding='utf-8').read()
concat = ' '.join(io.open(os.path.join(SRC, f'segment{n}.txt'), encoding='utf-8').read().strip() for n in range(1, 9))
assert full_text.strip() == concat.strip(), 'full != segments concatenation'
manifest['outputs']['full'] = {'label': 'Full edition', 'synthesize': False, 'concat_of': [f'segment{n}' for n in range(1, 9)], 'chunks': seg_chunk_lists}

with io.open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=1)

for k, v in manifest['outputs'].items():
    print(k, len(v['chunks']), 'chunks', '(no synth)' if v.get('synthesize') is False else '')
mx = max(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith('.txt'))
print('largest chunk bytes:', mx)
