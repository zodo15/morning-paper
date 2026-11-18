#!/usr/bin/env python3
import re
src = open('gen_file44.py').read()

# 1. Header title
old = "<Header title=\"%s\"' % \"The print, the rule, and the chairman's scenario.\""
assert old in src, 'title pattern missing'
src = src.replace(old, "<Header title=\"%s\"' % \"The print, the door, and the debut.\"")

# 2. Anchors
old = "FP_ANCHORS = {0: ['s-front','s-breath'], 1: ['s-shortlist'], 2: ['s-print'], 3: ['s-exchange'], 4: ['s-ledger'], 5: ['s-debut']}"
assert old in src, 'fp anchors missing'
src = src.replace(old, "FP_ANCHORS = {0: ['s-front','s-print'], 1: ['s-guide'], 2: ['s-exchange'], 3: ['s-tape'], 4: ['s-mumbai'], 5: ['s-debut']}")
old = "DETAIL = {1:'#s-breath',2:'#s-shortlist',3:'#s-print',4:'#s-exchange',5:'#s-ledger',6:'#s-debut',7:'#s-lr'}"
assert old in src, 'detail missing'
src = src.replace(old, "DETAIL = {1:'#s-exchange',2:'#s-tape',3:'#s-mumbai',4:'#s-debut',5:'#s-notes',6:'#s-markets'}")

# 3. BarChart block: from '<BarChart label' to the closing "]} />''')"
i0 = src.index('<BarChart label="Leaders and laggards')
i1 = src.index("]} />''')", i0) + len("]} />''')")
new_bar = """<BarChart label="Leaders and laggards, Tuesday 17 Nov, percent change vs Monday's close - BSE official prints" orientation="bars" data={[
                    { label: 'Adani Enterprises', value: 3.1 },
                    { label: 'Eicher Motors', value: 2.9 },
                    { label: 'Oberoi Realty', value: 2.8 },
                    { label: 'Godrej Properties', value: 2.7 },
                    { label: 'Prestige Estates', value: 2.4 },
                    { label: 'Oil India', value: -1.8 },
                    { label: 'Wipro', value: -1.8 },
                    { label: 'HCL Tech', value: -2.0 },
                    { label: 'Tata Communications', value: -2.8 },
                    { label: 'Ashok Leyland', value: -4.3 },
                ]} />''')"""
src = src[:i0] + new_bar + src[i1:]

# 4. Table block
i0 = src.index('<Table')
i1 = src.index("/>''')", i0) + len("/>''')")
new_table = """<Table
                    caption="Open lines after Tuesday's session; prices are BSE official closes, Tuesday 17 November"
                    options={[
                        { number: 1, name: 'Kotak Mahindra Bank' },
                        { number: 2, name: 'ONGC' },
                        { number: 3, name: 'Infosys' },
                        { number: 4, name: 'JSW Steel' },
                        { number: 5, name: 'Hindalco' },
                    ]}
                    rows={[
                        { label: 'Status', values: ['Watchlist - trigger held', 'Watchlist - inside coil, breakout leg not re-established', 'Watchlist - below zone, floor watch', 'Watchlist - fails the screen at Tuesday’s price', 'Watchlist - candidate'], best: 0 },
                        { label: 'Entry / trigger', values: ['Post-print strength above Rs 437.55 - held above it for a sixteenth session, close Rs 496.65 (+0.70%); touched a 52-week high intraday', 'Breakout above 228 with crude holding - close Rs 223.60, fourth session under 228; Brent firmed to $93.26 Tuesday, so the crude leg stabilizes', 'Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,130.00, still below the zone; Tuesday’s low of Rs 1,126.00 came within six points of the floor', 'Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,336.00', 'No entry zone yet - levels to be verified against longer price history; closed Rs 927.70 (+0.29%)'], },
                        { label: 'Stop / invalidation', values: ['Below Rs 420 shelves it', 'Coil floor Rs 218.50', 'A close under 1,120 ends the thesis', 'Under 1,158.95 breaks the floor', 'n/a until an entry zone exists'], },
                        { label: 'Target / objective', values: ['Structured-setup candidate', 'Coil top Rs 238.75', 'First checkpoint 1,245 (gap zone)', '5 November swing high near Rs 1,370', 'Momentum plus record quarter as catalyst'], },
                        { label: 'R:R at worst fill', values: ['n/a (not a setup)', '1:1.1 - below the screen', 'n/a (qualitative)', '1:2.3 at the reclaim zone - 1,222.30 fill, 1,158.95 stop, 1,370 target; about 1:0.2 at Tuesday’s close', 'n/a (not a setup)'], },
                        { label: 'Reference price', values: ['Rs 496.65 (Tue close)', 'Rs 223.60 (Tue close)', 'Rs 1,130.00 (Tue close)', 'Rs 1,336.00 (Tue close)', 'Rs 927.70 (Tue close)'], },
                    ]}
                />''')"""
src = src[:i0] + new_table + src[i1:]

# 5. RangeChart marker
old = 'label="ONGC in rupees: coil floor to coil top, marker at Monday\'s close"'
assert old in src, 'range label missing'
src = src.replace(old, 'label="ONGC in rupees: coil floor to coil top, marker at Tuesday\'s close"')
old = "{ label: 'ONGC', low: 218.50, now: 226.70, high: 238.75, highlight: true }"
assert old in src, 'range row missing'
src = src.replace(old, "{ label: 'ONGC', low: 218.50, now: 223.60, high: 238.75, highlight: true }")

open('gen_file44.py', 'w').write(src)
print('patched OK')
