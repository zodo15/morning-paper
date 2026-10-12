#!/usr/bin/env python3
"""Publish one morning's edition into the static bundle.

usage: publish_day.py DAY_SRC_JSON [--full FULL_AUDIO] [--quick QUICK_AUDIO]
                      [--script-full TXT]

- validates the day's source JSON (schema + concept + day sequence)
- converts audio to AAC m4a 64k mono under audio/
- if the full-read script is given, derives sentence-sync timings
- writes editions-src/day-N.json and regenerates data/editions.js
- prints the file list to push to GitHub
"""
import argparse, json, os, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fail(msg): print('ERROR: ' + msg); sys.exit(1)

def convert(src, dst):
    subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-c:a','aac','-b:a','64k','-ac','1',dst], check=True)
    out = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',dst],
                         capture_output=True, text=True)
    return float(out.stdout.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('day_json')
    ap.add_argument('--full'); ap.add_argument('--quick'); ap.add_argument('--script-full')
    a = ap.parse_args()

    src = json.load(open(a.day_json))
    for k in ('day','meta','edition'):
        if k not in src: fail(f'missing {k}')
    ed = src['edition']
    for k in ('fact','intro','groups'):
        if k not in ed: fail(f'edition missing {k}')
    if not ed.get('concept') or not ed['concept'].get('name'):
        fail('edition missing concept {label,name,line} (One Concept a Day)')
    if not src['meta'].get('date') or not src['meta'].get('short'):
        fail('meta missing date/short')

    existing = sorted(int(os.path.basename(p).split('-')[1].split('.')[0])
                      for p in glob.glob(os.path.join(ROOT,'editions-src','day-*.json')))
    if existing and src['day'] != existing[-1] + 1:
        fail(f'day {src["day"]} is not next in sequence (have through {existing[-1]})')

    audio = {'full': None, 'quick': None}
    times = None
    n = src['day']
    if a.full:
        dst = os.path.join(ROOT,'audio',f'd{n}-full.m4a')
        d = convert(a.full, dst); audio['full'] = f'audio/d{n}-full.m4a'
        print(f'full read: {d/60:.1f} min -> {dst}')
    if a.quick:
        dst = os.path.join(ROOT,'audio',f'd{n}-quick.m4a')
        d = convert(a.quick, dst); audio['quick'] = f'audio/d{n}-quick.m4a'
        print(f'quick listen: {d/60:.1f} min -> {dst}')
    src['audio'] = audio if (audio['full'] or audio['quick']) else None

    if a.full and a.script_full:
        times_rel = f'audio/d{n}-full.times.json'
        subprocess.run([sys.executable, os.path.join(ROOT,'scripts','align_audio.py'),
                        os.path.join(ROOT,'audio',f'd{n}-full.m4a'), a.script_full,
                        a.day_json, os.path.join(ROOT, times_rel)], check=True)
        times = {'full': times_rel}
    src['times'] = times

    with open(os.path.join(ROOT,'editions-src',f'day-{n}.json'),'w') as f:
        json.dump(src, f, ensure_ascii=False, indent=2)
    subprocess.run([sys.executable, os.path.join(ROOT,'scripts','build_data.py')], check=True)

    changed = [f'editions-src/day-{n}.json', 'data/editions.js']
    if audio['full']: changed.append(f'audio/d{n}-full.m4a')
    if audio['quick']: changed.append(f'audio/d{n}-quick.m4a')
    if times: changed.append(times['full'])
    print('push these files:'); [print('  ' + c) for c in changed]

if __name__ == '__main__':
    main()
