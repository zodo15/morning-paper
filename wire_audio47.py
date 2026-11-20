#!/usr/bin/env python3
"""Wire Ed47 audio into day-47.json + longreads.json, then rebuild editions.js.
Usage: python3 wire_audio47.py '<json durations>' where keys are quick, segment1..9, full, lrfull."""
import json, subprocess, sys, os
ROOT=os.path.dirname(os.path.abspath(__file__))
dur=json.loads(sys.argv[1])
labels=[("segment1","Opening and the five-minute lead route"),
("segment2","Front page: the correction, ANT, and the divergence"),
("segment3","Front page: the flows, gold, and oil"),
("segment4","Markets, IPOs, and the top movers"),
("segment5","Corporate actions, Finance Goldmine, and Startup Intelligence"),
("segment6","AI Race, vibe coding, try this, and one concept"),
("segment7","The setup board and how the board scores"),
("segment8","The editor's read, with the brewing files"),
("segment9","The week ahead and the notes on this edition")]
p=os.path.join(ROOT,'editions-src','day-47.json')
d=json.load(open(p))
a={'quick':'audio/d47-quick.m4a','durations':{k:v for k,v in dur.items() if k!='lrfull'},
   'segments':[{'key':k,'label':l} for k,l in labels]}
for k,_ in labels: a[k]=f'audio/d47-{k}.m4a'
a['full']='audio/d47-full.m4a'
d['audio']=a; d['times']={'full':'audio/d47-full.times.json'}
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
lp=os.path.join(ROOT,'editions-src','longreads.json')
lr=json.load(open(lp))
lr['47']['audio']={'full':'audio/lr47-full.m4a','durations':{'full':dur['lrfull']},'times':{'full':'audio/lr47-full.times.json'}}
json.dump(lr,open(lp,'w'),ensure_ascii=False,indent=2)
open(os.path.join(ROOT,'editions-src','ed47','audio_ready'),'w').write('1')
subprocess.run([sys.executable,os.path.join(ROOT,'scripts','build_data.py')],check=True)
print('wired; editions.js regenerated')
