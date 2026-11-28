#!/usr/bin/env python3
"""Wire Ed54 audio into day-54.json + longreads.json. Does NOT run build_data.py (deploy-time only, on main's go)."""
import json, sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
dur = json.loads(sys.argv[1])
labels = [('segment1', 'Opening and the five-minute lead route'),('segment2', "Front page: the court, China's rally, Wall Street and Anthropic"),('segment3', 'Front page: the Indian fall, Mahanadi, oil, gold and Europe'),('segment4', 'Markets, IPOs, and the top movers'),('segment5', 'Corporate actions and Finance Goldmine'),('segment6', 'AI Race and one concept'),('segment7', 'The setup board and how the board scores'),('segment8', 'The week ahead and the notes on this edition')]
p = os.path.join(ROOT, 'editions-src', 'day-54.json')
d = json.load(open(p))
a = {'quick': 'audio/d54-quick.m4a', 'durations': {k: v for k, v in dur.items() if k != 'lrfull'},
     'segments': [{'key': k, 'label': l} for k, l in labels]}
for k, _ in labels:
    a[k] = 'audio/d54-%s.m4a' % k
a['full'] = 'audio/d54-full.m4a'
d['audio'] = a
d['times'] = {'full': 'audio/d54-full.times.json'}
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)
lp = os.path.join(ROOT, 'editions-src', 'longreads.json')
lr = json.load(open(lp))
lr['54']['audio'] = {'full': 'audio/lr54-full.m4a', 'durations': {'full': dur['lrfull']}, 'times': {'full': 'audio/lr54-full.times.json'}}
json.dump(lr, open(lp, 'w'), ensure_ascii=False, indent=2)
print('wired day-54.json + longreads.json (editions.js NOT regenerated - build_data.py runs only at deploy go)')
