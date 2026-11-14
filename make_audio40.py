#!/usr/bin/env python3
"""Generate Ed40 audio scripts from day-40.json + longreads 40 with house respelling."""
import json, re, io, html as htmlmod

ONES = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
TENS = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']

def w99(n):
    if n < 20: return ONES[n]
    t, o = divmod(n, 10)
    return TENS[t] + ('-' + ONES[o] if o else '')

def w999(n):
    h, r = divmod(n, 100)
    s = ''
    if h: s += ONES[h] + ' hundred'
    if r: s += (' ' if s else '') + w99(r)
    return s

def windian(n):
    """Indian-system words: lakh, crore, thousand."""
    if n == 0: return 'zero'
    crore, r = divmod(n, 10000000)
    lakh, r2 = divmod(r, 100000)
    thou, rest = divmod(r2, 1000)
    parts = []
    if crore: parts.append(windian(crore) + ' crore')
    if lakh: parts.append(w99(lakh) + ' lakh')
    if thou: parts.append(w99(thou) + ' thousand')
    if rest: parts.append(w999(rest))
    return ' '.join(parts)

def wnum(n):
    return windian(n)

def frac_words(frac):
    # decimal digits spoken individually after 'point'
    return 'point ' + ' '.join(ONES[int(c)] for c in frac)

def speak_number(s):
    """s like 1,25,070.85 or 4.98 or 0.4 -> words."""
    s = s.replace(',', '')
    if '.' in s:
        ip, fp = s.split('.')
        if set(fp) == {'0'}:
            return wnum(int(ip))
        return wnum(int(ip)) + ' ' + frac_words(fp)
    return wnum(int(s))

def year_words(y):
    y = int(y)
    if 2000 <= y <= 2009: return 'two thousand' + (' ' + ONES[y-2000] if y>2000 else '')
    if 2010 <= y <= 2019: return 'twenty ' + ONES[y-2010-10+10] if False else 'twenty ' + (ONES[y-2010+10] if False else ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'][y-2010])
    if 2020 <= y <= 2099:
        r = y - 2020
        return 'twenty twenty' + ('-' + ONES[r] if r else '')
    a, b = divmod(y, 100)
    return ONES[a] + (' thousand' if a<10 else '') if False else (w99(a) + (' ' + w99(b) if b else ' hundred') if b or True else '')

def year_say(y):
    y = int(y)
    if 1900 <= y <= 1999:
        a, b = divmod(y, 100)
        if b == 0: return ONES[a-10+10-10+10] if False else w99(a) + ' hundred'
        return w99(a) + ' ' + (('oh ' + ONES[b]) if b < 10 else w99(b))
    if 2000 <= y <= 2009:
        return 'two thousand' + ((' ' + ONES[y % 10]) if y % 10 else '')
    if 2010 <= y <= 2019:
        return 'twenty ' + ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'][y-2010+0] if False else ('twenty ' + ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'][y-2010])
    if 2020 <= y <= 2029:
        r = y - 2020
        return 'twenty twenty' + ('' if r == 0 else '-' + ONES[r])
    return wnum(y)

ACR = ['CPI','NSDL','SEBI','DRHP','BSE','NSE','PSU','FPI','FII','IPO','WTI','DXY','AP','BBC','CNBC','ET','FE','HN','HCL','IT','AI','RBI','GDP','GIFT','NYT','AFP','IRCTC','NMDC','HAL','PV','ABB','RVNL','LSEG','IST','AM','PM','EAAA','NDTV','MRF','ONGC','KOTAK','CEO','FBI','GPU','AWS','RSI','NRI','IIFL','PAT','MPC','TCS','GTC','VIX','ITC','ICICI','JSW','BS','AMD','ARPU','BFSI','CFO','CNA','HBL','HUL','IRDAI','NVDA','PDF','SBI','SMS','TRAI','US']

def respell(t):
    # strip tags, decode entities
    t = re.sub(r"<[^>]+>", " ", t)
    t = htmlmod.unescape(t)
    t = t.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c','"').replace('\u201d','"')
    t = t.replace('\u2013','-').replace('\u2014',' - ')
    # R:R label
    t = re.sub(r"\bR:R\b", "risk-reward", t)
    t = re.sub(r"\bn/a\b", "not applicable", t)
    # named tokens with embedded digits
    t = t.replace('CNBC-TV18', 'C N B C T V eighteen')
    t = re.sub(r"\bG7\b", "G seven", t)
    t = t.replace('108EAAAL27', 'one oh eight E A A A L twenty-seven')
    t = t.replace('Inc42', 'Inc forty-two')
    t = t.replace('Storyboard18', 'Storyboard eighteen')
    def decade(m):
        y = m.group(1)
        if y.endswith('0'):
            dw = w99(int(y) % 100)
            dw = dw[:-2] + 'ies' if dw.endswith('ty') else dw + 's'
            return w99(int(y) // 100) + ' ' + dw
        return year_say(y) + 's'
    t = re.sub(r"\b(\d{4})s\b", decade, t)
    # signs attached to numbers
    t = re.sub(r"\+(?=\s*\d)", "plus ", t)
    t = re.sub(r"(?<=[(\s])-(?=\s*\d)", "minus ", t)
    # clock times H:MM AM/PM
    def clock(m):
        h, mi, ap = m.group(1), m.group(2), m.group(3).upper()
        hs = wnum(int(h)); ms = ('oh ' + ONES[int(mi)]) if int(mi) < 10 else w99(int(mi))
        return f"{hs} {ms} {' '.join(ap)}"
    t = re.sub(r"\b(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)\b", clock, t)
    # ratios like 1:1.1, 3:1, 1:5
    def ratio(m):
        a, b = m.group(1), m.group(2)
        sa = speak_number(a) if '.' in a else wnum(int(a))
        sb = speak_number(b) if '.' in b else wnum(int(b))
        return f"{sa} to {sb}"
    t = re.sub(r"\b(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)\b", ratio, t)
    # ranges number-number -> number to number
    def rng(m):
        return speak_number(m.group(1)) + ' to ' + speak_number(m.group(2))
    def rngpct(m):
        return speak_number(m.group(1)) + ' to ' + speak_number(m.group(2)) + ' percent'
    t = re.sub(r"(?<![A-Za-z])(\d[\d,]*(?:\.\d+)?)-(\d[\d,]*(?:\.\d+)?)%", rngpct, t)
    t = re.sub(r"(?<![A-Za-z])(\d[\d,]*(?:\.\d+)?)-(\d[\d,]*(?:\.\d+)?)(?![A-Za-z])", rng, t)
    # 'a Rs 3 dividend' -> 'a 3-rupee dividend'
    t = re.sub(r"\bRs\.?\s*([0-9][0-9,]*) dividend", r"\1-rupee dividend", t)
    # initials like K.M. U.S. C.P.
    t = re.sub(r"\b((?:[A-Z]\.){2,})", lambda m: ' '.join(c for c in m.group(1) if c.isalpha()), t)
    # crore/lakh suffixes hyphenated to numbers
    t = re.sub(r"([0-9])-(crore|lakh)", r"\1 \2", t)
    # $ amounts with scale words
    def usdscale(m):
        return speak_number(m.group(1)) + ' ' + m.group(2) + ' dollars'
    t = re.sub(r"\$\s*([0-9][0-9,]*(?:\.\d+)?)\s*(million|billion|trillion)", usdscale, t)
    # Rs amounts
    def rs(m):
        return 'rupees ' + speak_number(m.group(1))
    t = re.sub(r"\bRs\.?\s*([0-9][0-9,]*(?:\.\d+)?)", rs, t)
    # $ amounts
    def usd(m):
        return speak_number(m.group(1)) + ' dollars'
    t = re.sub(r"\$\s*([0-9][0-9,]*(?:\.\d+)?)", usd, t)
    # percents
    t = re.sub(r"([0-9][0-9,]*(?:\.\d+)?)\s*%", lambda m: speak_number(m.group(1)) + ' percent', t)
    # S&P and L&T
    t = t.replace('S&P', 'S and P').replace('L&T', 'L and T')
    t = t.replace('M&M', 'M and M')
    t = t.replace('RFE/RL', 'R F E R L')
    t = t.replace('IL JIN', 'I L Jin')
    t = t.replace('STOXX', 'Stoxx')
    t = t.replace('E20', 'E twenty')
    t = t.replace('TDB loan', 'T D B loan')
    t = re.sub(r"\bQ([1-4])\b", r"Q \1", t)
    t = t.replace('S-1', 'S one')
    t = t.replace('CUDA', 'Cuda')
    t = re.sub(r'\bRIVA\b', 'Riva', t)
    t = t.replace('HCLTech', 'H C L Tech')
    t = t.replace('KOSPI', 'Kospi')
    t = t.replace('giftniftytoday.com', 'gift nifty today dot com')
    # years first (4-digit 19xx/20xx) before generic numbers
    t = re.sub(r"\b(19\d{2}|20\d{2})\b", lambda m: year_say(m.group(1)), t)
    # ordinals in dates like 9 Nov / 11 November
    MONTHS = {'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July','Aug':'August','Sep':'September','Oct':'October','Nov':'November','Dec':'December'}
    for ab, full in MONTHS.items():
        t = re.sub(rf"\b{ab}\b", full, t)
    ORD = {1:'first',2:'second',3:'third',4:'fourth',5:'fifth',6:'sixth',7:'seventh',8:'eighth',9:'ninth',10:'tenth',11:'eleventh',12:'twelfth',13:'thirteenth',14:'fourteenth',15:'fifteenth',16:'sixteenth',17:'seventeenth',18:'eighteenth',19:'nineteenth',20:'twentieth',21:'twenty-first',22:'twenty-second',23:'twenty-third',24:'twenty-fourth',25:'twenty-fifth',26:'twenty-sixth',27:'twenty-seventh',28:'twenty-eighth',29:'twenty-ninth',30:'thirtieth',31:'thirty-first'}
    t = re.sub(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b",
               lambda m: 'the ' + ORD[int(m.group(1))] + ' of ' + m.group(2), t)
    # remaining numbers -> words
    t = re.sub(r"\b\d[\d,]*(?:\.\d+)?\b", lambda m: speak_number(m.group(0)), t)
    # acronyms spaced
    for a in sorted(ACR, key=len, reverse=True):
        t = re.sub(rf"\b{a}\b", ' '.join(list(a)), t)
    t = re.sub(r"\bvs\.?\b", "versus", t)
    # acronym-letter glued to word via hyphen (A I-infrastructure)
    t = re.sub(r"\b((?:[A-Z] )+[A-Z])-([a-z])", r"\1 \2", t)
    t = re.sub(r"\b(the|its|a|an|this|on|of|for|to|by) the (?=(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty-first|twenty-second|twenty-third|twenty-fourth|twenty-fifth|twenty-sixth|twenty-seventh|twenty-eighth|twenty-ninth|thirtieth|thirty-first) of )", r"\1 ", t)
    t = re.sub(r"\s+([.,;:!?])", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

d = json.load(open('/downloads/morning-paper/editions-src/day-40.json'))
ed = d['edition']
groups = ed['groups']

def block_text(b):
    if b['t'] == 'rows':
        out = []
        for i in b['items']:
            lab = i.get('n','')
            seg = (i.get('title','') + '. ' + i.get('detail','')).strip()
            out.append((lab + '. ' if lab else '') + seg)
        return ' '.join(out)
    if b['t'] == 'bullets':
        return ' '.join(b['items'])
    if b['t'] in ('svg','chart'):
        return ''
    return b.get('html','')

def group_text(g):
    return ' '.join(block_text(b) for b in g['blocks'] if block_text(b))

fact_clean = re.sub(r"This edition runs [0-9,]+ words\.", "", ed['fact'])
fact_clean = re.sub(r"^Edition 40\. [^.]+\. ", "", fact_clean)
fact_clean = re.sub(r"^Saturday 14 November 2026, edition 40\. ", "", fact_clean)
opening = respell("Slow Burn, Saturday the fourteenth of November twenty twenty-six, edition forty. " + fact_clean + " " + ed['intro'])

segs = [
    ("Opening and the five-minute lead route", [0]),
    ("Front page: the breath, the shortlist, and the print", None),  # front page blocks 1-3
    ("Front page: the exchange, the ledger, and the debut", None),  # front page 4-6
    ("Markets, IPOs, and the top movers", [2,3,4]),
    ("Corporate actions, Finance Goldmine, Startup Intelligence", [5,6,7]),
    ("AI Race, vibe coding, try this, and veto power", [8,9,10,11]),
    ("Term of the day and the setup board", [12,13]),
    ("Board scoring, the editor's read, and Brewing", [14,15,16]),
    ("The week ahead and the notes on this edition", [17,18]),
]

texts = {}
texts['segment1'] = opening + " " + respell(group_text(groups[0]))
fp = groups[1]['blocks']
fp_texts = [respell(block_text(b)) for b in fp]
texts['segment2'] = ' '.join(fp_texts[:3])
texts['segment3'] = ' '.join(fp_texts[3:])
for n, (key, idxs) in enumerate(segs[3:], start=4):
    texts[f'segment{n}'] = ' '.join(respell(group_text(groups[i])) for i in idxs)

closing = "That is the paper for Saturday. Nothing on these pages is investment advice. Slow Burn returns tomorrow morning."
texts['full'] = ' '.join(texts[f'segment{i}'] for i in range(1,10)) + ' ' + closing

# quick: compressed brief
quick = """Slow Burn quick read, Saturday the fourteenth of November twenty twenty-six. Mumbai's three-day rally broke on Friday: the Sensex fell three hundred eighteen point five six to eighty-one thousand five hundred ninety-two point four five and the Nifty a hundred fifty-five point oh five to twenty-five thousand one hundred forty-four point three oh, in the first session priced with inflation at six point oh nine percent and Brent above ninety-five dollars; foreigners still bought a provisional rupees five thousand seven hundred thirty-six point five five crore. Nvidia fell two point oh one percent to one hundred sixty-two point eight five dollars, a sixth straight losing week, as the Financial Times reported the board has approached Arm chief executive Rene Haas about the top job; Arm declined comment and Reuters could not independently verify. America's producer prices ran six point five percent on the year, and a December rate hike of at least a quarter point is fully priced. The F A A halted departures nationwide on Friday afternoon over a telecommunications outage, only the second such stop since nine eleven; the stop was lifted at eight fifteen pm Eastern, air traffic control and airline officials told The Air Current. Anthropic's filing sets terms - eight hundred twenty-five million shares at seventy to seventy-eight dollars - with trading reported to begin Thursday. The long read is Arm: the architecture everybody rents. Nothing in this paper is investment advice."""
texts['quick'] = quick

lrs = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = lrs['40']
lr_parts = ["Slow Burn long read. " + lr['title'] + ". " + re.sub(r"^A Slow Burn long read, Saturday 14 November 2026\. ", "", lr['fact'])]
for g in lr['groups']:
    h = re.sub(r"^(\d)\. ", r"Chapter \1. ", g['heading'])
    lr_parts.append(h + '. ' + group_text(g))
texts['lr-full'] = respell(' '.join(lr_parts))

import os
os.makedirs('/downloads/ed40audio', exist_ok=True)
for k, v in texts.items():
    with io.open(f'/downloads/ed40audio/{k}.txt', 'w', encoding='utf-8') as f:
        f.write(v + '\n')
    print(k, len(v.split()), 'words')
with io.open('/downloads/ed40audio/labels.json', 'w', encoding='utf-8') as f:
    json.dump([{'key': f'segment{i+1}', 'label': s[0]} for i, s in enumerate(segs)], f, indent=1)
print('done')
