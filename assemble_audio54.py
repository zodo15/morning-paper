#!/usr/bin/env python3
"""Ed54: synth dir (ed54_<unit>.*) -> /downloads/ed54units/audio/<unit>.m4a, then segment/quick/lr/full tracks into audio/."""
import os, glob, subprocess, json, sys
SYNTH = sys.argv[1]; U = '/downloads/ed54units/audio'; OUT = '/downloads/morning-paper/audio'
os.makedirs(U, exist_ok=True); os.makedirs(OUT, exist_ok=True)
man = json.load(open('/downloads/ed54audio/chunks/manifest.json'))['outputs']
sh = lambda *a: subprocess.run(a, check=True)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True,check=True).stdout.strip())
def units_for(n):
    if glob.glob(f'{SYNTH}/ed54_{n}.*') or glob.glob(f'{SYNTH}/{n}.*'): return [unit(n)]
    return [unit(n+'-p1'), unit(n+'-p2')]
def unit(n):
    src = glob.glob(f'{SYNTH}/ed54_{n}.*') + glob.glob(f'{SYNTH}/{n}.*'); assert len(src)==1, (n, src)
    dst = f'{U}/{n}.m4a'
    sh('ffmpeg','-v','error','-y','-i',src[0],'-ac','1','-ar','24000','-c:a','aac','-b:a','56k',dst); return dst
def concat(files, dst):
    lst = '/tmp/' + os.path.basename(dst) + '.lst'; open(lst,'w').write(''.join(f"file '{f}'\n" for f in files))
    sh('ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy','-movflags','+faststart',dst)
D = {}; seg_files = []
for k in [f'segment{i}' for i in range(1,9)]:
    fs = [u for c in man[k]['chunks'] for u in units_for(c[:-4])]
    concat(fs, f'{OUT}/d54-{k}.m4a'); seg_files.append(f'{OUT}/d54-{k}.m4a'); D[k] = round(dur(f'{OUT}/d54-{k}.m4a'),3)
concat(seg_files, f'{OUT}/d54-full.m4a'); D['full'] = round(dur(f'{OUT}/d54-full.m4a'),3)
if glob.glob(f'{SYNTH}/ed54_quick*'):
  concat([u for c in man['quick']['chunks'] for u in units_for(c[:-4])], f'{OUT}/d54-quick.m4a'); D['quick'] = round(dur(f'{OUT}/d54-quick.m4a'),3)
if glob.glob(f'{SYNTH}/ed54_lr-full*'):
  concat([u for c in man['lr-full']['chunks'] for u in units_for(c[:-4])], f'{OUT}/lr54-full.m4a'); D['lrfull'] = round(dur(f'{OUT}/lr54-full.m4a'),3)
assert abs(D['full']-sum(D[f'segment{i}'] for i in range(1,9)))<0.5
json.dump(D, open('/downloads/ed54units/durations.json','w'), indent=1); print(json.dumps(D))
