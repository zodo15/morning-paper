#!/usr/bin/env python3
"""Wire Ed49 audio into day-49.json + longreads.json, then rebuild editions.js."""
import json, subprocess, sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
dur = json.loads(sys.argv[1])
labels = [("segment1", "Opening and the five-minute lead route"),
("segment2", "Front page: the split open, Friday's settles, and Bessent"),
("segment3", "Front page: the decoupling's test, Mahanadi, Neon, and the cheques"),
("segment4", "Markets, IPOs, and the top movers"),
("segment5", "Corporate actions, Finance Goldmine, and Startup Intelligence"),
("segment6", "AI Race, vibe coding, try this, one concept, and the term of the day"),
("segment7", "The setup board and how the board scores"),
("segment8", "The editor's read and brewing"),
("segment9", "The week ahead and the notes on this edition")]
p = os.path.join(ROOT, 'editions-src', 'day-49.json')
d = json.load(open(p))
a = {'quick': 'audio/d49-quick.m4a', 'durations': {k: v for k, v in dur.items() if k != 'lrfull'},
     'segments': [{'key': k, 'label': l} for k, l in labels]}
for k, _ in labels:
    a[k] = 'audio/d49-%s.m4a' % k
a['full'] = 'audio/d49-full.m4a'
d['audio'] = a
d['times'] = {'full': 'audio/d49-full.times.json'}
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)
lp = os.path.join(ROOT, 'editions-src', 'longreads.json')
lr = json.load(open(lp))
lr['49']['audio'] = {'full': 'audio/lr49-full.m4a', 'durations': {'full': dur['lrfull']}, 'times': {'full': 'audio/lr49-full.times.json'}}
json.dump(lr, open(lp, 'w'), ensure_ascii=False, indent=2)
subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'build_data.py')], check=True)
print('wired; editions.js regenerated')
