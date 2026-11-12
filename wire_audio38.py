#!/usr/bin/env python3
"""Wire Ed38 audio into day-38.json + longreads.json once segment9/full finals arrive.
Usage: python3 wire_audio38.py <segment9_dur> <full_dur>"""
import json, subprocess, sys, os
ROOT=os.path.dirname(os.path.abspath(__file__))
seg9_dur=float(sys.argv[1]); full_dur=float(sys.argv[2])
dur={'quick':101.2,'segment1':228.0,'segment2':314.2,'segment3':289.7,'segment4':255.4,
     'segment5':343.9,'segment6':349.6,'segment7':229.1,'segment8':268.0,
     'segment9':round(seg9_dur,1),'full':round(full_dur,1)}
labels=[("segment1","Opening and the five-minute lead route"),
("segment2","Front page: the sprint, the tide, and the four P M print"),
("segment3","Front page: Jensen Huang, CoreWeave, and Abu Dhabi"),
("segment4","Markets, IPOs, and the top movers"),
("segment5","Corporate actions, Finance Goldmine, Startup Intelligence"),
("segment6","AI Race, vibe coding, try this, and anchoring"),
("segment7","Term of the day and the setup board"),
("segment8","Board scoring, the editor's read, and Brewing"),
("segment9","The week ahead and the notes on this edition")]
p=os.path.join(ROOT,'editions-src','day-38.json')
d=json.load(open(p))
a={'quick':'audio/d38-quick.m4a','durations':dur,
   'segments':[{'key':k,'label':l} for k,l in labels]}
for k,_ in labels: a[k]=f'audio/d38-{k}.m4a'
a['full']='audio/d38-full.m4a'
d['audio']=a; d['times']=None
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
lp=os.path.join(ROOT,'editions-src','longreads.json')
lr=json.load(open(lp))
lr['38']['audio']={'full':'audio/lr38-full.m4a','durations':{'full':698.9}}
json.dump(lr,open(lp,'w'),ensure_ascii=False,indent=2)
subprocess.run([sys.executable,os.path.join(ROOT,'scripts','build_data.py')],check=True)
print('wired; editions.js regenerated')
