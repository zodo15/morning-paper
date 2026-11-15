#!/usr/bin/env python3
"""Repair Ed39/Ed40 chart blocks: replace unresolved tokens/raw text with the
inline SVG/HTML the site renders (same helpers as build_day41.py). Content and
session labels preserved (Thursday 12 Nov for Ed39, Friday 13 Nov for Ed40)."""
import json

def bars(label, rows_, scale=7.758064516129032, zero=410):
    n = len(rows_); h = 30 + 48*n
    out = ['<svg viewBox="0 0 760 %d" role="img" aria-label="%s">' % (h, label)]
    for i, (name, val, vlabel) in enumerate(rows_):
        ty = 47 + 48*i; ry = 30 + 48*i
        out.append('<text x="8" y="%d" font-size="21" fill="#334155">%s</text>' % (ty, name))
        w = abs(val)*scale
        if val >= 0:
            out.append('<rect x="%d" y="%d" width="%s" height="26" fill="#15803d" rx="3"/>' % (zero, ry, w))
            out.append('<text x="%s" y="%d" text-anchor="start" font-size="20" fill="#15803d">%s</text>' % (zero+w+8, ty+2, vlabel))
        else:
            out.append('<rect x="%s" y="%d" width="%s" height="26" fill="#b91c1c" rx="3"/>' % (zero-w, ry, w))
            out.append('<text x="%s" y="%d" text-anchor="end" font-size="20" fill="#b91c1c">%s</text>' % (zero-w-8, ty+2, vlabel))
    out.append('</svg><p style="font-size:13px;color:#64748b;line-height:1.5">%s</p>' % label)
    return ''.join(out)

def card(num, name, rws):
    s = '<div style="border:1px solid #d9d1c4;border-radius:8px;padding:14px;margin:12px 0"><strong>%d. %s</strong>' % (num, name)
    for k, v in rws:
        s += '<p style="margin:10px 0;font-size:15px"><b>%s: </b>%s</p>' % (k, v)
    return s + '</div>'

def rangec(low, now, high, nowlabel, caption):
    scale = (591.290322580645-204.51612903225836)/(238.75-218.50)
    x0 = 204.51612903225836 - 218.50*scale
    xl, xn, xh = x0+low*scale, x0+now*scale, x0+high*scale
    return ('<svg viewBox="0 0 760 125" role="img" aria-label="%s">'
            '<text x="8" y="44" font-size="23">ONGC</text>'
            '<line x1="%s" x2="%s" y1="38" y2="38" stroke="#15803d" stroke-width="10"/>'
            '<circle cx="%s" cy="38" r="10" fill="#172b3c"/>'
            '<text x="%s" y="82" font-size="19" text-anchor="middle">218.50</text>'
            '<text x="%s" y="16" font-size="19" text-anchor="middle">%s</text>'
            '<text x="%s" y="82" font-size="19" text-anchor="middle">238.75</text></svg>'
            '<p style="font-size:13px;color:#64748b">%s</p>') % (caption, xl, xh, xn, xl, xn, nowlabel, xh, caption)

def splice(path, movers_svg, board_html, range_svg, old_range_is_token):
    d = json.load(open(path))
    g4 = d['edition']['groups'][4]
    g13 = d['edition']['groups'][13]
    c4 = [b for b in g4['blocks'] if b['t'] == 'chart']
    c13 = [b for b in g13['blocks'] if b['t'] == 'chart']
    assert len(c4) == 1 and len(c13) == 2, (path, len(c4), len(c13))
    c4[0]['svg'] = movers_svg
    c13[0]['svg'] = board_html
    c13[1]['svg'] = range_svg
    json.dump(d, open(path, 'w'), indent=1, ensure_ascii=False)
    print(path, 'spliced')

# ---- Ed40: Friday's data, identical to Ed41's carried board, Friday labels
d41 = json.load(open('editions-src/day-41.json'))
m41 = [b for b in d41['edition']['groups'][4]['blocks'] if b['t'] == 'chart'][0]['svg']
m40 = m41.replace(" - carried into Sunday", "")
b41 = [b for b in d41['edition']['groups'][13]['blocks'] if b['t'] == 'chart']
board40 = b41[0]['svg'].replace("Open lines after Friday's session, carried into Sunday; prices",
                                "Open lines after Friday's session; prices")
range40 = b41[1]['svg']
assert 'carried into Sunday' not in m40 and 'carried into Sunday' not in board40
splice('editions-src/day-40.json', m40, board40, range40, True)

# ---- Ed39: Thursday's data from the edition's own records (gen_file39.py JSX)
movers39 = bars("Sensex leaders and laggards, Thursday 12 Nov (% vs Wednesday's close), BSE official prints", [
    ('Bajaj Finance', 3.3, '+3.3%'), ('SBI', 2.3, '+2.3%'), ('BEL', 2.3, '+2.3%'),
    ('Bajaj Finserv', 1.3, '+1.3%'), ('ICICI Bank', 1.2, '+1.2%'), ('Eternal', 0.9, '+0.9%'),
    ('TCS', -1.6, '-1.6%'), ('Maruti', -1.7, '-1.7%'), ('HUL', -2.9, '-2.9%'), ('ONGC', -4.4, '-4.4%')])

board39 = ('<p style="color:#64748b;font-size:13px">Open lines after Thursday\'s session; prices are BSE official closes, Thursday 12 November</p>'
 + card(1, 'Kotak Mahindra Bank', [('Status','Watchlist - trigger held'),('Entry / trigger','Post-print strength above Rs 437.55 - held above it for a thirteenth session, close Rs 488.70'),('Stop / invalidation','Below Rs 420 shelves it'),('Target / objective','Structured-setup candidate'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 488.70 (Thu close)')])
 + card(2, 'ONGC', [('Status','Watchlist - back under breakout, ex-dividend'),('Entry / trigger','Breakout above 228 with crude holding - close Rs 224.75, back under 228 after six sessions; Thursday was the Rs 8 ex-dividend, and Brent settled at $95.82, so the crude leg firmed again'),('Stop / invalidation','Coil floor Rs 218.50'),('Target / objective','Coil top Rs 238.75'),('R:R at worst fill','1:1.1 - below the screen'),('Reference price','Rs 224.75 (Thu close)')])
 + card(3, 'Infosys', [('Status','Watchlist - below zone, flat'),('Entry / trigger','Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,147.90, flat below the zone'),('Stop / invalidation','A close under 1,120 ends the thesis'),('Target / objective','First checkpoint 1,245 (gap zone)'),('R:R at worst fill','n/a (qualitative)'),('Reference price','Rs 1,147.90 (Thu close)')])
 + card(4, 'JSW Steel', [('Status','Watchlist - R:R fails screen'),('Entry / trigger','Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,354.00'),('Stop / invalidation','Under 1,158.95 breaks the floor'),('Target / objective','5 November swing high near Rs 1,370'),('R:R at worst fill','1:1.2 - failed the screen'),('Reference price','Rs 1,354.00 (Thu close)')])
 + card(5, 'Hindalco', [('Status','Watchlist - candidate'),('Entry / trigger','No entry zone yet - levels to be verified against longer price history; closed Rs 964.20'),('Stop / invalidation','n/a until an entry zone exists'),('Target / objective','Momentum plus record quarter as catalyst'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 964.20 (Thu close)')]))

range39 = rangec(218.50, 224.75, 238.75, '224.75', "ONGC: coil floor to coil top, marker at Thursday's close")
splice('editions-src/day-39.json', movers39, board39, range39, False)
print('done')
