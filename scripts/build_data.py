#!/usr/bin/env python3
"""Regenerate data/editions.js from editions-src/. Source of truth is the
per-day JSON files; never edit data/editions.js by hand."""
import json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load():
    days = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'editions-src', 'day-*.json')),
                       key=lambda p: int(p.split('day-')[1].split('.')[0])):
        with open(path) as f:
            src = json.load(f)
        days[str(src['day'])] = src
    with open(os.path.join(ROOT, 'editions-src', 'longreads.json')) as f:
        longreads = json.load(f)
    return days, longreads

def build():
    days, longreads = load()
    today = max(int(d) for d in days)
    data = {
        'today': today,
        'meta': {d: s['meta'] for d, s in days.items()},
        'editions': {d: s['edition'] for d, s in days.items()},
        'longreads': longreads,
        'audio': {d: s.get('audio') for d, s in days.items()},
    }
    # fold per-day highlight timing refs into audio records
    for d, s in days.items():
        t = s.get('times')
        if t:
            if data['audio'][d] is None:
                data['audio'][d] = {}
            data['audio'][d]['times'] = t
    out = 'window.PAPER_DATA=' + json.dumps(data, ensure_ascii=False) + ';\n'
    path = os.path.join(ROOT, 'data', 'editions.js')
    with open(path, 'w') as f:
        f.write(out)
    print(f'wrote {path} ({len(out)//1024} KB), today={today}')

if __name__ == '__main__':
    build()
