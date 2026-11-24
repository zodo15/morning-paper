import io, json, os, re
SRC='/downloads/ed50audio'; OUT='/downloads/ed50chunks'
os.makedirs(OUT, exist_ok=True)
LIMIT=1800
order=['segment1','segment2','segment3','segment4','segment5','segment6','segment7','segment8','full','quick','lr-full']
def chunk(text):
    text=text.strip()
    if len(text)<=LIMIT: return [text]
    parts=[]; buf=''
    for s in re.split(r'(?<=[.!?]) ', text):
        if buf and len(buf)+1+len(s)>LIMIT:
            parts.append(buf); buf=s
        else:
            buf=(buf+' '+s).strip()
        while len(buf)>LIMIT:  # overlong single sentence: split at comma/semicolon
            cut=max(buf.rfind('; ',0,LIMIT), buf.rfind(', ',0,LIMIT))
            if cut<1000: cut=LIMIT
            parts.append(buf[:cut+1].strip()); buf=buf[cut+1:].strip()
    if buf: parts.append(buf)
    return parts
manifest={'edition':50,'tracks':[]}
for name in order:
    t=io.open(f'{SRC}/{name}.txt',encoding='utf-8').read()
    cs=chunk(t)
    files=[]
    for i,c in enumerate(cs):
        fn=f'{name}-p{i+1:02d}.txt'
        io.open(f'{OUT}/{fn}','w',encoding='utf-8').write(c+'\n')
        files.append(fn)
    manifest['tracks'].append({'track':name,'chunks':files,'chars':sum(len(c) for c in cs)})
json.dump(manifest, open(f'{OUT}/manifest.json','w'), indent=1)
for tr in manifest['tracks']:
    print(tr['track'], len(tr['chunks']), tr['chunks'], tr['chars'])
