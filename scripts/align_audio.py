#!/usr/bin/env python3
"""Derive sentence-level highlight timings for the recorded full read.

Pipeline: ffmpeg silencedetect finds narration pauses -> script sentences are
placed across real speech time proportionally by word count, with boundaries
snapped to detected pauses -> script sentences are matched to the edition's
page blocks (paragraphs + bullets, in reading order) so the site can highlight
the sentence being read. Output is real audio-derived sync, not a guess: the
total speech timeline and every pause comes from the audio file itself.

usage: align_audio.py AUDIO SCRIPT_TXT DAY_SRC_JSON OUT_JSON
"""
import json, re, subprocess, sys, difflib

def ffprobe_duration(path):
    out = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                          '-of','csv=p=0', path], capture_output=True, text=True)
    return float(out.stdout.strip())

def silences(path, noise='-35dB', mind=0.30):
    p = subprocess.run(['ffmpeg','-hide_banner','-i',path,'-af',
                        f'silencedetect=noise={noise}:d={mind}','-f','null','-'],
                       capture_output=True, text=True)
    starts = [float(m.group(1)) for m in re.finditer(r'silence_start: ([\d.]+)', p.stderr)]
    ends   = [float(m.group(1)) for m in re.finditer(r'silence_end: ([\d.]+)', p.stderr)]
    return list(zip(starts, ends))

def speech_intervals(sils, dur):
    out, cur = [], 0.0
    for s, e in sils:
        if s > cur: out.append((cur, s))
        cur = max(cur, e)
    if cur < dur: out.append((cur, dur))
    return out

def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+|\n+', text.strip())
    return [p.strip() for p in parts if p and p.strip()]

def words(t): return len(re.findall(r"\S+", t))

def place_sentences(sents, intervals):
    total_w = sum(words(s) for s in sents) or 1
    total_t = sum(e - s for s, e in intervals)
    # cursor over speech intervals
    iv, off = 0, intervals[0][0] if intervals else 0.0
    def advance(share):
        nonlocal iv, off
        need = share
        while iv < len(intervals):
            s, e = intervals[iv]
            avail = e - off
            if need <= avail:
                off += need
                return
            need -= avail
            iv += 1
            if iv < len(intervals): off = intervals[iv][0]
    out = []
    for stext in sents:
        start = off
        advance(words(stext) / total_w * total_t)
        out.append([start, off, stext])
    return out

def snap(placed, sils, window=0.9):
    mids = [(s + e) / 2 for s, e in sils]
    for i in range(1, len(placed)):
        b = placed[i][0]
        best = None
        for m in mids:
            if abs(m - b) <= window and (best is None or abs(m - b) < abs(best - b)):
                best = m
        if best is not None:
            placed[i][0] = placed[i-1][1] = best
    return placed

TOKEN = re.compile(r"[a-z]+|\d+\.\d+|\d+")
ONES = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,
        'nine':9,'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,
        'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19}
TENS = {'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90}
MULT = {'hundred':100,'thousand':1000}
SKIP = {'percent'}

def norm(t):
    """Normalize for matching: spoken number words become digits on both sides,
    so 'ninety-six point seven three' and '96.73' compare equal."""
    t = re.sub(r'(\d),(\d)', r'\1\2', t)  # 22,520 -> 22520
    toks = TOKEN.findall(t.lower().replace('-', ' '))
    out, i = [], 0
    while i < len(toks):
        w = toks[i]
        if w in SKIP:
            i += 1; continue
        if w in ('a', 'an') and i + 1 < len(toks) and toks[i+1] in MULT:
            toks[i] = 'one'; w = 'one'
        if w in ONES or w in TENS:
            total, cur, j = 0, 0, i
            while j < len(toks) and (toks[j] in ONES or toks[j] in TENS or toks[j] in MULT):
                wj = toks[j]
                if wj in ONES: cur += ONES[wj]
                elif wj in TENS: cur += TENS[wj]
                elif wj == 'hundred': cur = max(cur, 1) * 100
                else:  # thousand and up: close the group
                    total += max(cur, 1) * MULT[wj]; cur = 0
                j += 1
            val = total + cur
            if j + 1 < len(toks) and toks[j] == 'point' and toks[j+1] in ONES:
                j += 1; dec = ''
                while j < len(toks) and toks[j] in ONES:
                    dec += str(ONES[toks[j]]); j += 1
                out.append(f"{val}.{dec}" if dec else str(val))
            else:
                out.append(str(val))
            i = j
        else:
            out.append(w); i += 1
    return ' '.join(out)

def strip_html(h):
    import html as H
    return H.unescape(re.sub(r'<[^>]+>', '', h))

def edition_blocks(day_src):
    """Page blocks in rendered reading order. Must mirror exactly the elements
    the site renders with class .rp (see blockHTML in app.js): paragraphs,
    bullet items, row details, callouts, closings - nothing else."""
    ed = day_src['edition']
    blocks = []
    for g in ed['groups']:
        for b in g['blocks']:
            if b['t'] == 'p':
                blocks.append(strip_html(b['html']))
            elif b['t'] == 'bullets':
                blocks.extend(b['items'])
            elif b['t'] == 'rows':
                blocks.extend(r['detail'] for r in b['items'])
            elif b['t'] in ('callout', 'closing'):
                blocks.append(strip_html(b['html']))
    return blocks

def match_blocks(blocks, placed):
    """Sequentially match each page block to a run of script sentences.
    The script follows paper order but adds glue (greeting, transitions, the
    spoken intro), so search a forward window from the running pointer."""
    res, ptr = [], 0
    ratios = []
    WINDOW = 40
    for btext in blocks:
        bn = norm(btext)
        if not bn:
            res.append(None); continue
        best = None
        hi = min(ptr + WINDOW, len(placed))
        for p0 in range(ptr, hi):
            for m in range(1, 9):
                if p0 + m > len(placed): break
                joined = norm(' '.join(x[2] for x in placed[p0:p0+m]))
                sm = difflib.SequenceMatcher(None, bn, joined)
                if best and sm.real_quick_ratio() < best[0]: continue
                if best and sm.quick_ratio() < best[0]: continue
                r = sm.ratio()
                if best is None or r > best[0]:
                    best = (r, p0, m)
        if best and best[0] >= 0.5:
            r, p0, m = best
            ptr = p0 + m
            ratios.append(r)
            res.append((p0, m))
        else:
            res.append(None)
    return res, ratios

def main():
    audio, script_path, day_path, out_path = sys.argv[1:5]
    dur = ffprobe_duration(audio)
    sils = silences(audio)
    intervals = speech_intervals(sils, dur)
    script = re.sub(r'\[[^\]]*\]', '', open(script_path).read())  # [curious] cues
    sents = split_sentences(script)
    placed = snap(place_sentences(sents, intervals), sils)
    day_src = json.load(open(day_path))
    blocks = edition_blocks(day_src)
    matched, ratios = match_blocks(blocks, placed)

    out_blocks = []
    for btext, mm in zip(blocks, matched):
        if mm is None:
            out_blocks.append(None)
            continue
        p0, m = mm
        bs, be = placed[p0][0], placed[p0+m-1][1]
        bsents = split_sentences(btext)
        if len(bsents) == m:
            sent_entries = [{'t': t, 's': round(placed[p0+i][0],2), 'e': round(placed[p0+i][1],2)}
                            for i, t in enumerate(bsents)]
        else:
            # interpolate inside the block by word share
            tw = sum(words(x) for x in bsents) or 1
            cur, sent_entries = bs, []
            for t in bsents:
                e = cur + words(t)/tw*(be-bs)
                sent_entries.append({'t': t, 's': round(cur,2), 'e': round(e,2)})
                cur = e
        out_blocks.append({'s': round(bs,2), 'e': round(be,2), 'sentences': sent_entries})

    json.dump({'version': 1, 'audio': f'audio/d{day_src["day"]}-full.m4a', 'blocks': out_blocks},
              open(out_path,'w'), ensure_ascii=False)
    cov = sum(1 for x in matched if x)
    # Source lines and Why-it-matters boxes are skipped by the spoken script by design
    readable = [i for i, b in enumerate(blocks)
                if not b.startswith('Source:') and not b.startswith('Why it matters to you:')]
    cov_r = sum(1 for i in readable if matched[i])
    print(f'blocks matched: {cov}/{len(blocks)} total, {cov_r}/{len(readable)} excluding Source lines'
          + (f' | avg ratio {sum(ratios)/len(ratios):.2f}' if ratios else ''))
    if readable and cov_r/len(readable) < 0.9:
        print('WARNING: content coverage below 90% - inspect script vs edition text')
        for i in readable:
            if matched[i] is None:
                print('  unmatched content block', i, ':', blocks[i][:90])

if __name__ == '__main__':
    main()
