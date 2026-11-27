#!/usr/bin/env python3
"""Ed53 correction: write the unit texts main must synthesize (Kore, same settings as Ed53).
Units: segment1 (3 units), segment8, quick (3 units), closing. Sentence-boundary halves, no trailing heading sentence."""
import re, io, json, os
C='/downloads/ed53audio/chunks'; OUT='/downloads/ed53fix/units'
def sent_split(t):
    parts = re.split(r'([.!?]["\']?) ', t.strip()); out=[]
    for i in range(0,len(parts)-1,2): out.append(parts[i]+parts[i+1])
    if len(parts)%2: out.append(parts[-1])
    return [p for p in out if p]
def heading_like(s):
    w=s.split(); return len(s)<90 and len(w)<=9 and ',' not in s
def halves(text):
    sens=sent_split(text); tot=sum(len(s)+1 for s in sens); cum=0; best=1; be=9e9
    for k in range(1,len(sens)):
        cum+=len(sens[k-1])+1; e=abs(cum/tot-0.5)
        if e<be and not heading_like(sens[k-1]): best,be=k,e
    return ' '.join(sens[:best]), ' '.join(sens[best:])
rd=lambda n: io.open(f'{C}/{n}.txt',encoding='utf-8').read().strip()
units=[]
def add(name,text): 
    io.open(f'{OUT}/{name}.txt','w',encoding='utf-8').write(text+'\n'); units.append({'unit':name,'chars':len(text)})
a,b=halves(rd('segment1-c01')); add('segment1-c01-a',a); add('segment1-c01-b',b); add('segment1-c02',rd('segment1-c02'))
add('segment8-c01',rd('segment8-c01'))
a,b=halves(rd('quick-c01')); add('quick-c01-a',a); add('quick-c01-b',b); add('quick-c02',rd('quick-c02'))
json.dump({'edition':53,'purpose':'correction re-synthesis','units':units},open(OUT+'/units.json','w'),indent=1)
for u in units: print(u)
