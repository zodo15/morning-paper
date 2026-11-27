#!/usr/bin/env python3
"""Build d53-full.times.json + lr53-full.times.json for Ed53.
Unit-anchored: ffmpeg-concat unit boundaries are exact; within a unit, sentences
distribute by respelled-character weight. Split-chunk a/b seam found by best char-fit
against measured unit durations. Emits print-text sentences per Ed52's live schema."""
import json, re, os, subprocess, html, io

ROOT = '/downloads/morning-paper'
UNITS = '/downloads/ed53units/audio'
CHUNKS = '/downloads/ed53audio/chunks'

# --- get respell/block_text/groups/ed/lr/texts/opening by exec'ing the generator ---
ns = {}
exec(open(os.path.join(ROOT, 'make_audio53.py')).read(), ns)
respell, block_text, groups, ed, texts = ns['respell'], ns['block_text'], ns['groups'], ns['ed'], ns['texts']
lr = ns['lr']

def sent_split(t):
    parts = re.split(r'([.!?]["\']?) ', t.strip())
    out = []
    for i in range(0, len(parts) - 1, 2):
        out.append(parts[i] + parts[i + 1])
    if len(parts) % 2:
        out.append(parts[-1])
    return [p for p in out if p]

def dur(path):
    r = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',path],capture_output=True,text=True)
    out = r.stdout.strip()
    if not out:
        print('DUR FAIL path=%r rc=%s err=%s' % (path, r.returncode, r.stderr[:300]))
        raise SystemExit(1)
    return float(out)

retry = json.load(open('/downloads/ed53units/retry-manifest.json'))
manifest = json.load(open(CHUNKS + '/manifest.json'))

def unit_texts(chunkbase):
    """Return [(unit_name, text)] in audio order for a chunk (1 unsplit or a/b halves)."""
    whole = io.open(CHUNKS + '/' + chunkbase + '.txt', encoding='utf-8').read().strip()
    if chunkbase not in retry:
        return [(chunkbase, whole)]
    # find sentence split k by char-fit against measured durations
    sens = sent_split(whole)
    da = dur(f'{UNITS}/{chunkbase}-a.m4a'); db = dur(f'{UNITS}/{chunkbase}-b.m4a')
    ratio = da / (da + db)
    best, besterr = 1, 9e9
    cum = 0; total = sum(len(s) + 1 for s in sens)
    for k in range(1, len(sens)):
        cum += len(sens[k-1]) + 1
        err = abs(cum / total - ratio)
        if err < besterr: best, besterr = k, err
    return [(chunkbase + '-a', ' '.join(sens[:best])), (chunkbase + '-b', ' '.join(sens[best:]))]

def track_units(key):
    out = []
    for ch in manifest['outputs'][key]['chunks']:
        out += unit_texts(ch[:-4])  # strip .txt
    if key == 'full':
        out.append(('closing-c01', 'See you tomorrow.'))  # sign-off unit appended to segment8+full
    return out

def stream_for(key):
    """audio sentence stream: list of (unit_name, sent_idx_in_unit, s, e) after timing."""
    units = track_units(key)
    stream = []
    t = 0.0
    for name, text in units:
        d = dur(f'{UNITS}/{name}.m4a')
        sens = sent_split(text)
        total = sum(len(s) for s in sens) or 1
        acc = 0.0
        for i, s in enumerate(sens):
            frac0, frac1 = acc / total, (acc + len(s)) / total
            stream.append({'unit': name, 't': s, 's': t + frac0 * d, 'e': t + frac1 * d})
            acc += len(s)
        t += d
    return stream, t

def consume(stream, pos, n):
    part = stream[pos:pos+n]
    assert len(part) == n, f'stream exhausted: need {n} at {pos}'
    return part, pos + n

def clean(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h)).strip()

# ---------- FULL ----------
stream, full_dur = stream_for('full')
pos = 0
# opening: respelled opening sentences (not a block)
opening_sens = sent_split(texts['full'])  # sanity only
# consume the opening: it is respell("Slow Burn...edition fifty-three. " + fact_clean + " " + intro)
fact_clean = re.sub(r"This edition runs (?:[0-9,]+|WORDCOUNT) words\.", "", ed['fact'])
fact_clean = re.sub(r"^Edition 53\. [^.]+\. ", "", fact_clean)
opening_audio = respell("Slow Burn, Friday the twenty-seventh of November twenty twenty-six, edition fifty-three. " + fact_clean + " " + ed['intro'])
n_open = len(sent_split(opening_audio))
_, pos = consume(stream, pos, n_open)

blocks_out = []
mismatches = []
for gi, g in enumerate(groups):
    for b in g['blocks']:
        bt = b['t']
        if bt in ('svg', 'chart', 'figure'):
            continue
        if bt == 'rows':
            for it in b['items']:
                lab = str(it.get('n', ''))
                atext = (lab + '. ' if lab else '') + (it.get('title', '') + '. ' + it.get('detail', '')).strip()
                n = len(sent_split(respell(atext)))
                part, pos = consume(stream, pos, n)
                blocks_out.append({'s': round(part[0]['s'], 2), 'e': round(part[-1]['e'], 2),
                                   'sentences': [{'t': clean(it.get('detail', '')), 's': round(part[0]['s'], 2), 'e': round(part[-1]['e'], 2)}]})
        elif bt == 'bullets':
            for item in b['items']:
                n = len(sent_split(respell(item)))
                part, pos = consume(stream, pos, n)
                blocks_out.append({'s': round(part[0]['s'], 2), 'e': round(part[-1]['e'], 2),
                                   'sentences': [{'t': clean(item), 's': round(part[0]['s'], 2), 'e': round(part[-1]['e'], 2)}]})
        elif bt in ('p', 'closing'):
            audio_txt = respell(block_text(b))
            asens = sent_split(audio_txt)
            psens = sent_split(clean(block_text(b)))
            if bt == 'closing' and pos + len(asens) > len(stream):
                print('WARN: closing not spoken in audio; omitting closing block from times')
                continue
            part, pos = consume(stream, pos, len(asens))
            if len(psens) != len(asens):
                mismatches.append((gi, bt, len(psens), len(asens), clean(block_text(b))[:60]))
                # fallback: zip by min length
            sents = []
            for k, a in enumerate(part):
                t_txt = psens[k] if k < len(psens) else psens[-1]
                sents.append({'t': t_txt, 's': round(a['s'], 2), 'e': round(a['e'], 2)})
            blocks_out.append({'s': sents[0]['s'], 'e': sents[-1]['e'], 'sentences': sents})
print('full: stream sentences', len(stream), 'consumed', pos, 'duration', round(full_dur, 2))
print('full mismatches:', mismatches)

times = {'version': 1, 'audio': 'audio/d53-full.m4a', 'blocks': blocks_out}
# checks: zero nulls, monotonic, span
prev = 0.0; ok = True
for b in times['blocks']:
    for s in b['sentences']:
        if s['s'] is None or s['e'] is None or s['e'] <= s['s'] or s['s'] < prev - 0.01: ok = False; print('BAD', s)
        prev = s['s']
assert abs(blocks_out[-1]['e'] - full_dur) < 1.0, ('end mismatch', blocks_out[-1]['e'], full_dur)
assert pos == len(stream)
json.dump(times, open(ROOT + '/audio/d53-full.times.json', 'w'), indent=1)
print('full times ok:', ok, 'blocks:', len(blocks_out), 'end', blocks_out[-1]['e'])

# ---------- LR ----------
def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', '', s.lower())).strip()

def consume_text(stream, pos, text):
    """Consume stream sentences whose joined normalized text equals norm(text); tolerates merge/split drift."""
    target = norm(text)
    acc = ''
    k = pos
    while k < len(stream):
        acc = (acc + ' ' + norm(stream[k]['t'])).strip()
        k += 1
        if acc == target:
            return stream[pos:k], k
        if len(acc) > len(target) or acc != target[:len(acc)]:
            break
    raise AssertionError('LR no match at pos %d: %r vs stream %r' % (pos, text[:80], stream[pos]['t'][:80] if pos < len(stream) else '<eof>'))

stream, lr_dur = stream_for('lr-full')
pos = 0
lr_open = re.sub(r"^A Slow Burn long read, Friday 27 November 2026\. ", "", lr['fact'])
opening_audio = respell("Slow Burn long read. " + lr['title'] + ". " + lr_open)
_, pos = consume_text(stream, pos, opening_audio)
blocks_out = []
mismatches = []
for g in lr['groups']:
    h = re.sub(r"^(\d)\. ", r"Chapter \1. ", g['heading'])
    _, pos = consume_text(stream, pos, respell(h))
    for b in g['blocks']:
        if b.get('t') == 'figure':
            continue
        audio_txt = respell(b['html'])
        asens = sent_split(audio_txt)
        psens = sent_split(clean(b['html']))
        part, pos = consume_text(stream, pos, audio_txt)
        if len(psens) != len(part):
            mismatches.append((g['heading'], len(psens), len(part), clean(b['html'])[:60]))
        if len(psens) == len(part):
            sents = [{'t': psens[k], 's': round(part[k]['s'], 2), 'e': round(part[k]['e'], 2)} for k in range(len(part))]
        else:
            # char-weighted distribution of print sentences over the consumed span
            span0, span1 = part[0]['s'], part[-1]['e']
            tot = sum(len(p) for p in psens) or 1
            acc = 0.0
            sents = []
            for p in psens:
                f0, f1 = acc / tot, (acc + len(p)) / tot
                sents.append({'t': p, 's': round(span0 + f0 * (span1 - span0), 2), 'e': round(span0 + f1 * (span1 - span0), 2)})
                acc += len(p)
        blocks_out.append({'s': sents[0]['s'], 'e': sents[-1]['e'], 'sentences': sents})
print('lr: stream sentences', len(stream), 'consumed', pos, 'duration', round(lr_dur, 2))
print('lr mismatches:', mismatches)
times = {'version': 1, 'audio': 'audio/lr53-full.m4a', 'blocks': blocks_out}
prev = 0.0; ok = True
for b in times['blocks']:
    for s in b['sentences']:
        if s['s'] is None or s['e'] is None or s['e'] <= s['s'] or s['s'] < prev - 0.01: ok = False; print('BAD', s)
        prev = s['s']
assert abs(blocks_out[-1]['e'] - lr_dur) < 1.0, ('end mismatch', blocks_out[-1]['e'], lr_dur)
assert pos == len(stream)
json.dump(times, open(ROOT + '/audio/lr53-full.times.json', 'w'), indent=1)
print('lr times ok:', ok, 'blocks:', len(blocks_out), 'end', blocks_out[-1]['e'])
