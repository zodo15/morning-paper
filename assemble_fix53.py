#!/usr/bin/env python3
"""Ed53 correction assembler. Inputs: synthesized unit audio in SYNTH (wav/m4a/mp3, names = units in units.json),
old live tracks in LIVE (d53-segment2..7.m4a, full.times.json). Outputs (suffix -r2) to OUT:
 d53-segment1-r2.m4a, d53-segment8-r2.m4a, d53-quick-r2.m4a, d53-full-r2.m4a, d53-full-r2.times.json, durations.json
Unchanged tracks (segment2..7, lr53) keep their live names."""
import json, os, re, io, subprocess, sys, html, glob
ROOT='/downloads/morning-paper'; FIX='/downloads/ed53fix'; UNITS=FIX+'/units'
SYNTH=sys.argv[1] if len(sys.argv)>1 else FIX+'/synth'
OUT=sys.argv[2] if len(sys.argv)>2 else ROOT+'/audio'
LIVE='/downloads/live53'
os.makedirs(OUT,exist_ok=True); os.makedirs(FIX+'/m4a',exist_ok=True)
def sh(*a): subprocess.run(a,check=True)
def dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True,check=True).stdout.strip())
def to_m4a(name):
    src=[f for f in glob.glob(f'{SYNTH}/{name}.*')]
    assert len(src)==1,(name,src)
    dst=f'{FIX}/m4a/{name}.m4a'
    sh('ffmpeg','-v','error','-y','-i',src[0],'-ac','1','-ar','24000','-c:a','aac','-b:a','56k',dst)
    return dst
def concat(files,dst):
    lst=dst+'.lst'
    open(lst,'w').write(''.join(f"file '{f}'\n" for f in files))
    sh('ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy','-movflags','+faststart',dst)
txt=lambda n: io.open(f'{UNITS}/{n}.txt',encoding='utf-8').read().strip()
U={n:to_m4a(n) for n in ['segment1-c01-a','segment1-c01-b','segment1-c02','segment8-c01','quick-c01-a','quick-c01-b','quick-c02']}
seg1=[U['segment1-c01-a'],U['segment1-c01-b'],U['segment1-c02']]
quick=[U['quick-c01-a'],U['quick-c01-b'],U['quick-c02']]
concat(seg1,f'{OUT}/d53-segment1-r2.m4a'); concat([U['segment8-c01']],f'{OUT}/d53-segment8-r2.m4a'); concat(quick,f'{OUT}/d53-quick-r2.m4a')
old=[f'{LIVE}/d53-segment{i}.m4a' for i in range(2,8)]
concat([f'{OUT}/d53-segment1-r2.m4a']+old+[f'{OUT}/d53-segment8-r2.m4a'],f'{OUT}/d53-full-r2.m4a')
D={'segment1':dur(f'{OUT}/d53-segment1-r2.m4a'),'segment8':dur(f'{OUT}/d53-segment8-r2.m4a'),'quick':dur(f'{OUT}/d53-quick-r2.m4a'),'full':dur(f'{OUT}/d53-full-r2.m4a')}
for i in range(2,8): D[f'segment{i}']=dur(f'{LIVE}/d53-segment{i}.m4a')
D={k:round(v,3) for k,v in D.items()}
assert abs(D['full']-sum(D[f'segment{i}'] for i in range(1,9)))<0.5,('full!=sum',D)
json.dump(D,open(f'{OUT}/durations-r2.json','w'),indent=1); print('durations',D)

# ---- times ----
ns={}; exec(open(ROOT+'/make_audio53.py').read(),ns)
respell,block_text,groups,ed,texts=ns['respell'],ns['block_text'],ns['groups'],ns['ed'],ns['texts']
def sent_split(t):
    parts=re.split(r'([.!?]["\']?) ',t.strip()); out=[]
    for i in range(0,len(parts)-1,2): out.append(parts[i]+parts[i+1])
    if len(parts)%2: out.append(parts[-1])
    return [p for p in out if p]
def clean(h): return html.unescape(re.sub(r'<[^>]+>','',h)).strip()
# new-timeline units: seg1 units, then OLD segments 2-7 as single whole units (replaced later), then seg8 unit
units=[('segment1-c01-a',txt('segment1-c01-a'),dur(U['segment1-c01-a'])),('segment1-c01-b',txt('segment1-c01-b'),dur(U['segment1-c01-b'])),('segment1-c02',txt('segment1-c02'),dur(U['segment1-c02']))]
for i in range(2,8): units.append((f'segment{i}',texts[f'segment{i}'].strip(),D[f'segment{i}']))
units.append(('segment8-c01',txt('segment8-c01'),dur(U['segment8-c01'])))
stream=[];t=0.0
for name,text,d in units:
    sens=sent_split(text); tot=sum(len(s) for s in sens) or 1; acc=0.0
    for s in sens:
        stream.append({'t':s,'s':t+acc/tot*d,'e':t+(acc+len(s))/tot*d,'u':name}); acc+=len(s)
    t+=d
full_dur=t
pos=0
def consume(n):
    global pos
    part=stream[pos:pos+n]; assert len(part)==n,'stream exhausted'; pos+=n; return part
fact_clean=re.sub(r"This edition runs (?:[0-9,]+|WORDCOUNT) words\.","",ed['fact'])
fact_clean=re.sub(r"^Edition 53\. [^.]+\. ","",fact_clean)
opening_audio=respell("Slow Burn, Friday the twenty-seventh of November twenty twenty-six, edition fifty-three. "+fact_clean+" "+ed['intro'])
consume(len(sent_split(opening_audio)))
blocks=[]
for g in groups:
    for b in g['blocks']:
        bt=b['t']
        if bt in ('svg','chart','figure'): continue
        if bt=='rows':
            for it in b['items']:
                lab=str(it.get('n','')); at=(lab+'. ' if lab else '')+(it.get('title','')+'. '+it.get('detail','')).strip()
                part=consume(len(sent_split(respell(at))))
                blocks.append({'u':part[0]['u'],'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2),'sentences':[{'t':clean(it.get('detail','')),'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2)}]})
        elif bt=='bullets':
            for item in b['items']:
                part=consume(len(sent_split(respell(item))))
                blocks.append({'u':part[0]['u'],'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2),'sentences':[{'t':clean(item),'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2)}]})
        elif bt in ('p','closing'):
            asens=sent_split(respell(block_text(b))); psens=sent_split(clean(block_text(b)))
            part=consume(len(asens))
            sents=[{'t':psens[k] if k<len(psens) else psens[-1],'s':round(a['s'],2),'e':round(a['e'],2)} for k,a in enumerate(part)]
            blocks.append({'u':part[0]['u'],'s':sents[0]['s'],'e':sents[-1]['e'],'sentences':sents})
assert pos==len(stream),('unconsumed',pos,len(stream))
# replace segs 2-7 blocks with OLD exact times shifted
oldt=json.load(open(LIVE+'/full.times.json'))['blocks']
OLD_S2=409.483; OLD_S8=OLD_S2+sum(D[f'segment{i}'] for i in range(2,8)); NEW_S2=D['segment1']; delta=NEW_S2-OLD_S2
eps=0.3
oldmid=[b for b in oldt if OLD_S2-eps<=b['s']<OLD_S8-eps]
newidx=[i for i,b in enumerate(blocks) if re.fullmatch(r'segment[2-7]',b['u'])]
assert len(oldmid)==len(newidx),('block count',len(oldmid),len(newidx))
for k,i in enumerate(newidx):
    ob=oldmid[k]
    assert [s['t'] for s in ob['sentences']]==[s['t'] for s in blocks[i]['sentences']] or len(ob['sentences'])==len(blocks[i]['sentences']),('text',k)
    blocks[i]={'s':round(ob['s']+delta,2),'e':round(ob['e']+delta,2),'sentences':[{'t':s['t'],'s':round(s['s']+delta,2),'e':round(s['e']+delta,2)} for s in ob['sentences']]}
for b in blocks: b.pop('u',None)
prev=0.0
for b in blocks:
    for s in b['sentences']:
        assert s['e']>s['s'] and s['s']>=prev-0.01,('bad',s); prev=s['s']
assert abs(blocks[-1]['e']-D['full'])<1.0,('end',blocks[-1]['e'],D['full'])
json.dump({'version':1,'audio':'audio/d53-full-r2.m4a','blocks':blocks},open(f'{OUT}/d53-full-r2.times.json','w'),indent=1)
print('times ok blocks',len(blocks),'end',blocks[-1]['e'],'mid blocks swapped',len(newidx))
