#!/usr/bin/env python3
"""Wire Ed39 audio into day-39.json + longreads.json, then rebuild editions.js."""
import json, subprocess, sys, os
ROOT=os.path.dirname(os.path.abspath(__file__))
dur={'quick':91.5,'segment1':185.0,'segment2':274.1,'segment3':227.4,'segment4':284.1,
     'segment5':369.0,'segment6':330.6,'segment7':235.1,'segment8':248.3,
     'segment9':226.8,'full':2387.9}
labels=[("segment1","Opening and the five-minute lead route"),
("segment2","Front page: the founder leaves, the ceiling gives way, and the session that waited"),
("segment3","Front page: the barrel reprices, the Kremlin meeting, and the results wave"),
("segment4","Markets, IPOs, and the top movers"),
("segment5","Corporate actions, Finance Goldmine, Startup Intelligence"),
("segment6","AI Race, vibe coding, try this, and key person risk"),
("segment7","Term of the day and the setup board"),
("segment8","Board scoring, the editor's read, and Brewing"),
("segment9","The week ahead and the notes on this edition")]
p=os.path.join(ROOT,'editions-src','day-39.json')
d=json.load(open(p))
a={'quick':'audio/d39-quick.m4a','durations':dur,
   'segments':[{'key':k,'label':l} for k,l in labels]}
for k,_ in labels: a[k]=f'audio/d39-{k}.m4a'
a['full']='audio/d39-full.m4a'
d['audio']=a; d['times']=None
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
lp=os.path.join(ROOT,'editions-src','longreads.json')
lr=json.load(open(lp))
lr['39']['audio']={'full':'audio/lr39-full.m4a','durations':{'full':809.5}}
json.dump(lr,open(lp,'w'),ensure_ascii=False,indent=2)
subprocess.run([sys.executable,os.path.join(ROOT,'scripts','build_data.py')],check=True)
print('wired; editions.js regenerated')
