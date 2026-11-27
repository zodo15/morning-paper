#!/usr/bin/env python3
"""Ed52 correction: segment 8 only. Inputs SYNTH dir with segment8-c01-a/-b audio. Outputs d52-segment8-r2.m4a, d52-full-r2.m4a, d52-full-r2.times.json, durations-r52.json"""
import json,os,re,io,subprocess,sys,html,glob
ROOT='/downloads/morning-paper'; FIX='/downloads/ed52fix'; LIVE='/downloads/live52'
SYNTH=sys.argv[1] if len(sys.argv)>1 else FIX+'/synth'
OUT=sys.argv[2] if len(sys.argv)>2 else ROOT+'/audio'
os.makedirs(OUT,exist_ok=True); os.makedirs(FIX+'/m4a',exist_ok=True)
def sh(*a): subprocess.run(a,check=True)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True,check=True).stdout.strip())
def to_m4a(n):
    s=glob.glob(f'{SYNTH}/*{n}.*'); s=[x for x in s if not x.endswith('.txt')]; assert len(s)==1,(n,s)
    d=f'{FIX}/m4a/{n}.m4a'; sh('ffmpeg','-v','error','-y','-i',s[0],'-ac','1','-ar','24000','-c:a','aac','-b:a','56k',d); return d
def concat(fs,dst):
    open(dst+'.lst','w').write(''.join(f"file '{f}'\n" for f in fs)); sh('ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',dst+'.lst','-c','copy','-movflags','+faststart',dst)
ua,ub=to_m4a('segment8-c01-a'),to_m4a('segment8-c01-b')
concat([ua,ub],f'{OUT}/d52-segment8-r2.m4a')
concat([f'{LIVE}/d52-segment{i}.m4a' for i in range(1,8)]+[f'{OUT}/d52-segment8-r2.m4a'],f'{OUT}/d52-full-r2.m4a')
D={f'segment{i}':round(dur(f'{LIVE}/d52-segment{i}.m4a'),3) for i in range(1,8)}
D['segment8']=round(dur(f'{OUT}/d52-segment8-r2.m4a'),3); D['full']=round(dur(f'{OUT}/d52-full-r2.m4a'),3)
assert abs(D['full']-sum(D[f'segment{i}'] for i in range(1,9)))<0.5,D
json.dump(D,open(f'{OUT}/durations-r52.json','w'),indent=1); print(D)
ns={}; exec(open(ROOT+'/make_audio52.py').read(),ns)
respell,block_text,groups=ns['respell'],ns['block_text'],ns['groups']
def sent_split(t):
    parts=re.split(r'([.!?]["\']?) ',t.strip()); out=[]
    for i in range(0,len(parts)-1,2): out.append(parts[i]+parts[i+1])
    if len(parts)%2: out.append(parts[-1])
    return [p for p in out if p]
def clean(h): return html.unescape(re.sub(r'<[^>]+>','',h)).strip()
T=lambda n: io.open(f'{FIX}/units/{n}.txt',encoding='utf-8').read().strip()
units=[('segment8-c01-a',T('segment8-c01-a'),dur(ua)),('segment8-c01-b',T('segment8-c01-b'),dur(ub))]
base=sum(D[f'segment{i}'] for i in range(1,8))
stream=[];t=base
for n,txt,d in units:
    ss=sent_split(txt); tot=sum(len(s) for s in ss) or 1; acc=0.0
    for s in ss: stream.append({'t':s,'s':t+acc/tot*d,'e':t+(acc+len(s))/tot*d}); acc+=len(s)
    t+=d
pos=0
def consume(n):
    global pos
    p=stream[pos:pos+n]; assert len(p)==n,'exhausted'; pos+=n; return p
# seg8 = groups 11,12; first sentences are the opening "Edition... / title" line produced by make_audio52 segment8 text; consume by matching start
segtxt=T('segment8-c01-a')+' '+T('segment8-c01-b')
seg8_audio_full=ns['texts']['segment8'].strip()
assert segtxt.replace('\n',' ')==seg8_audio_full.replace('\n',' '),'unit text != segment8 script'
blocks=[]
# segment8 text begins with a spoken heading; find how many leading sentences precede first block
first=sent_split(respell(block_text(groups[11]['blocks'][0])))
# locate start: the block text sentences must appear in stream; skip leading until match
def find_start(first_s):
    for k in range(len(stream)):
        if stream[k]['t']==first_s[0]: return k
    raise AssertionError('start not found')
pos=find_start(first)
for g in groups[11:13]:
    for b in g['blocks']:
        bt=b['t']
        if bt=='rows':
            for it in b['items']:
                lab=str(it.get('n','')); at=(lab+'. ' if lab else '')+(it.get('title','')+'. '+it.get('detail','')).strip()
                part=consume(len(sent_split(respell(at))))
                blocks.append({'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2),'sentences':[{'t':clean(it.get('detail','')),'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2)}]})
        elif bt=='bullets':
            for item in b['items']:
                part=consume(len(sent_split(respell(item))))
                blocks.append({'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2),'sentences':[{'t':clean(item),'s':round(part[0]['s'],2),'e':round(part[-1]['e'],2)}]})
        elif bt in ('p','closing'):
            asens=sent_split(respell(block_text(b))); psens=sent_split(clean(block_text(b)))
            part=consume(len(asens))
            ss=[{'t':psens[k] if k<len(psens) else psens[-1],'s':round(a['s'],2),'e':round(a['e'],2)} for k,a in enumerate(part)]
            blocks.append({'s':ss[0]['s'],'e':ss[-1]['e'],'sentences':ss})
assert pos==len(stream),('unconsumed',pos,len(stream))
old=json.load(open(LIVE+'/full.times.json'))['blocks']
# old blocks before segment8
oldseg8_start=base
keep=[b for b in old if b['s']<oldseg8_start-0.3]
oldseg8=[b for b in old if b['s']>=oldseg8_start-0.3]
print('old seg8 blocks',len(oldseg8),'new seg8 blocks',len(blocks),'kept',len(keep))
# same count except +1 correction bullet
assert len(blocks)==len(oldseg8)+1,('block count',len(blocks),len(oldseg8))
allb=keep+blocks
prev=0.0
for b in allb:
    for s in b['sentences']:
        assert s['e']>s['s'] and s['s']>=prev-0.01,('bad',s); prev=s['s']
assert abs(allb[-1]['e']-D['full'])<1.0,(allb[-1]['e'],D['full'])
json.dump({'version':1,'audio':'audio/d52-full-r2.m4a','blocks':allb},open(f'{OUT}/d52-full-r2.times.json','w'),indent=1)
print('ed52 times ok',len(allb),allb[-1]['e'])
