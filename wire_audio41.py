#!/usr/bin/env python3
"""Wire Ed41 audio into day-41.json + longreads.json, then rebuild editions.js.
Usage: python3 wire_audio41.py '<json durations>' where keys are quick, segment1..9, full, lrfull."""
import json, subprocess, sys, os
ROOT=os.path.dirname(os.path.abspath(__file__))
dur=json.loads(sys.argv[1])
labels=[("segment1","Opening and the five-minute lead route"),
("segment2","Front page: the cause, the catch, and the search"),
("segment3","Front page: the terms, the nods, and the claims"),
("segment4","Markets, IPOs, and the top movers"),
("segment5","Corporate actions, Finance Goldmine, Startup Intelligence"),
("segment6","AI Race, vibe coding, try this, and the Schelling point"),
("segment7","Term of the day and the setup board"),
("segment8","Board scoring, the editor's read, and Brewing"),
("segment9","The week ahead and the notes on this edition")]
p=os.path.join(ROOT,'editions-src','day-41.json')
d=json.load(open(p))
a={'quick':'audio/d41-quick.m4a','durations':{k:v for k,v in dur.items() if k!='lrfull'},
   'segments':[{'key':k,'label':l} for k,l in labels]}
for k,_ in labels: a[k]=f'audio/d41-{k}.m4a'
a['full']='audio/d41-full.m4a'
d['audio']=a; d['times']=None
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
lp=os.path.join(ROOT,'editions-src','longreads.json')
lr=json.load(open(lp))
lr['41']['audio']={'full':'audio/lr41-full.m4a','durations':{'full':dur['lrfull']}}
json.dump(lr,open(lp,'w'),ensure_ascii=False,indent=2)
subprocess.run([sys.executable,os.path.join(ROOT,'scripts','build_data.py')],check=True)
print('wired; editions.js regenerated')
