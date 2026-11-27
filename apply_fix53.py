#!/usr/bin/env python3
"""After assemble_fix53.py: wire r2 audio + durations + word count into editions-src/day-53.json. Then run scripts/build_data.py and bump sw.js."""
import json,re,sys,subprocess
D=json.load(open('/downloads/morning-paper/audio/durations-r2.json'))
p='/downloads/morning-paper/editions-src/day-53.json'
d=json.load(open(p))
a=d['audio']
a['quick']='audio/d53-quick-r2.m4a'; a['segment1']='audio/d53-segment1-r2.m4a'; a['segment8']='audio/d53-segment8-r2.m4a'; a['full']='audio/d53-full-r2.m4a'
for k in ('segment1','segment8','quick','full'): a['durations'][k]=D[k]
d['times']={'full':'audio/d53-full-r2.times.json'}
n=int(subprocess.run(['python3','/downloads/morning-paper/wc.py',p],capture_output=True,text=True).stdout.strip())
d['edition']['fact']=re.sub(r'This edition runs [0-9,]+ words\.','This edition runs %d words.'%n,d['edition']['fact'])
json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)
n2=int(subprocess.run(['python3','/downloads/morning-paper/wc.py',p],capture_output=True,text=True).stdout.strip())
print('wordcount',n,n2); assert n==n2
