#!/usr/bin/env python3
"""Generate the paper File's App.tsx from day-38.json, mirroring Ed37's component shape."""
import json, re, html, sys

d = json.load(open('/downloads/morning-paper/editions-src/day-38.json'))
ed = d['edition']

# collect link consts
consts = {}
def const_name(url):
    if url in consts: return consts[url]
    n = 'U%d' % (len(consts)+1)
    consts[url] = n
    return n

def links_to_jsx(h):
    """Convert raw anchors to TextLink JSX with const table."""
    def rep(m):
        url, txt = m.group(1), m.group(2)
        return '<TextLink href={%s}>%s</TextLink>' % (const_name(url), txt)
    return re.sub(r'<a href="([^"]+)" target="_blank" rel="noopener">([^<]+)</a>', rep, h)

def esc_jsx_text(s):
    # JSX: escape { } in text nodes
    return s.replace('{', '&#123;').replace('}', '&#125;')

ANCHORS = {0: ['s-route'], 2: ['s-markets'], 3: ['s-ipo'], 4: ['s-movers'], 5: ['s-corp'], 6: ['s-gold'], 7: ['s-startup'], 8: ['s-ai'], 9: ['s-vibe'], 10: ['s-try'], 11: ['s-concept'], 12: ['s-term'], 13: ['s-board'], 15: ['s-read'], 16: ['s-brewing'], 17: ['s-week'], 18: ['s-notes']}
# front-page: anchor before specific story index
FP_ANCHORS = {0: ['s-front','s-reopen'], 1: ['s-tide'], 2: ['s-print'], 3: ['s-nvidia'], 4: ['s-crwv'], 5: ['s-ad']}
DETAIL = {1:'#s-reopen',2:'#s-tide',3:'#s-print',4:'#s-nvidia',5:'#s-crwv',6:'#s-ad',7:'#s-lr'}

def para(h, strong_prefix=False, detail=None):
    h2 = links_to_jsx(h.strip())
    if strong_prefix:
        m = re.match(r'(\s*)(<TextLink[^>]*>)?([^:]+?:)', h2)
        if m and '<TextLink' not in (m.group(3) or ''):
            h2 = m.group(1) + '<strong>' + m.group(3) + '</strong>' + h2[m.end():]
    if detail:
        h2 += ' <a href="%s">Detail</a>.' % detail if not h2.rstrip().endswith('.') else ' <a href="%s">Detail</a>' % detail
    return '                <Paragraph>%s</Paragraph>' % esc_jsx_text(h2).replace('&#123;TextLink href={','{').replace('&#123;','&#123;')

def para_clean(h, strong_prefix=False, detail=None):
    h2 = links_to_jsx(h.strip())
    if strong_prefix:
        m = re.match(r'(\d+\. [^.]+\.)', h2)  # '1. Title.' style
        if not m:
            m = re.match(r'([^:]+?:)', h2)      # 'The session:' style
        if m and '<' not in m.group(1):
            h2 = '<strong>' + m.group(1) + '</strong>' + h2[m.end():]
    if detail:
        h2 = h2 + ' <a href="%s">Detail</a>' % detail
    # protect JSX braces in plain text but keep TextLink jsx
    h2 = h2.replace('{', '\x01').replace('}', '\x02')
    h2 = h2.replace('\x01U', '{U').replace('\x02', '}')
    return '                <Paragraph>%s</Paragraph>' % h2

out = []
out.append("import { Bullets, Callout, Closing, FileCard, Group, Header, Heading, Paragraph, Rows, Row, Text, TextLink, BarChart, Table, RangeChart } from '@instinct/files';")
out.append('')
out.append('function Anchor({ id }: { id: string }) { return <span id={id} />; }')
out.append('')

groups = ed['groups']

# first pass: gather consts from all html
for g in groups:
    for b in g['blocks']:
        if b['t'] == 'p':
            links_to_jsx(b['html'])
        elif b['t'] == 'closing':
            links_to_jsx(b['html'])
links_to_jsx(ed['fact'])
lrurl = consts.get('LR38URL', None)

for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')

out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % "The tide and the boardroom")
fact_jsx = esc_jsx_text(links_to_jsx(ed['fact']))
out.append('            fact={`%s`}' % fact_jsx.replace('`','\\`'))
intro_jsx = esc_jsx_text(ed['intro'])
out.append('            intro="%s" />' % intro_jsx.replace('"','&quot;'))

for gi, g in enumerate(groups):
    out.append('')
    out.append('        <Group label="%s" heading>' % g['heading'].replace('"','&quot;'))
    out.append('            <Text>')
    for aid in ANCHORS.get(gi, []):
        out.append('                <Anchor id="%s" />' % aid)
    for bi, b in enumerate(g['blocks']):
        t = b['t']
        if gi == 1 and bi in FP_ANCHORS:
            for aid in FP_ANCHORS[bi]:
                out.append('                <Anchor id="%s" />' % aid)
        if t == 'p':
            strong = gi in (0, 1)
            detail = DETAIL.get(bi) if gi == 0 else None
            out.append(para_clean(b['html'], strong_prefix=strong, detail=detail))
        elif t == 'chart':
            svg = b['svg']
            if svg == 'BARCHART_MOVERS':
                out.append('''                <BarChart label="Sensex leaders and laggards, Wednesday 11 Nov (% vs Monday's close), BSE official prints" orientation="bars" data={[
                    { label: 'M&M', value: 5.3 },
                    { label: 'IndiGo', value: 4.4 },
                    { label: 'Trent', value: 3.0 },
                    { label: 'Tata Steel', value: 2.2 },
                    { label: 'ITC', value: 2.2 },
                    { label: 'Axis Bank', value: 2.1 },
                    { label: 'Tech Mahindra', value: -1.3 },
                    { label: 'Nestle India', value: -1.0 },
                    { label: 'ICICI Bank', value: -1.0 },
                    { label: 'HCL Tech', value: -1.0 },
                ]} />''')
            elif svg == 'BOARD_TABLE':
                out.append('''                <Table
                    caption="Open lines after Wednesday's session; prices are BSE official closes, Wednesday 11 November"
                    options={[
                        { number: 1, name: 'Kotak Mahindra Bank' },
                        { number: 2, name: 'ONGC' },
                        { number: 3, name: 'Infosys' },
                        { number: 4, name: 'JSW Steel' },
                        { number: 5, name: 'Hindalco' },
                    ]}
                    rows={[
                        { label: 'Status', values: ['Watchlist - trigger held', 'Watchlist - inside coil, crude leg firming', 'Watchlist - below zone, flat', 'Watchlist - R:R fails screen', 'Watchlist - candidate'], best: 0 },
                        { label: 'Entry / trigger', values: ['Post-print strength above Rs 437.55 - held above it for a twelfth session, close Rs 488.00', 'Breakout above 228 with crude holding - close Rs 235.00, six sessions above 228 inside the coil; Brent settled at $92.76, so the crude condition firmed for the first time in days; Rs 8 dividend declared', 'Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,153.00, flat below the zone; the Rs 26 dividend is paid', 'Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,352.00', 'No entry zone yet - levels to be verified against longer price history; closed Rs 960.00'], },
                        { label: 'Stop / invalidation', values: ['Below Rs 420 shelves it', 'Coil floor Rs 218.50', 'A close under 1,120 ends the thesis', 'Under 1,158.95 breaks the floor', 'n/a until an entry zone exists'], },
                        { label: 'Target / objective', values: ['Structured-setup candidate', 'Coil top Rs 238.75', 'First checkpoint 1,245 (gap zone)', '5 November swing high near Rs 1,370', 'Momentum plus record quarter as catalyst'], },
                        { label: 'R:R at worst fill', values: ['n/a (not a setup)', '1:1.1 - below the screen', 'n/a (qualitative)', '1:1.2 - failed the screen', 'n/a (not a setup)'], },
                        { label: 'Reference price', values: ['Rs 488.00 (Wed close)', 'Rs 235.00 (Wed close)', 'Rs 1,153.00 (Wed close)', 'Rs 1,352.00 (Wed close)', 'Rs 960.00 (Wed close)'], },
                    ]}
                />''')
            else:
                # ONGC range chart
                out.append('''                <RangeChart
                    label="ONGC: coil floor to coil top, marker at Wednesday's close"
                    rows={[
                        { label: 'ONGC', low: 218.50, now: 235.00, high: 238.75, highlight: true },
                    ]}
                    range={[210, 245]}
                    scaleLabels={['210', '245']}
                />''')
        elif t == 'rows':
            out.append('                <Rows>')
            for it in b['items']:
                out.append('                    <Row n="%s" title="%s" detail="%s" />' % (it['n'], esc_jsx_text(it['title']).replace('"','&quot;'), esc_jsx_text(it['detail']).replace('"','&quot;')))
            out.append('                </Rows>')
        elif t == 'bullets':
            out.append('                <Bullets items={[')
            for it in b['items']:
                j = links_to_jsx(it).replace('"','\\"')
                out.append('                    "%s",' % j)
            out.append('                ]} />')
        elif t == 'closing':
            out.append('                <Closing>%s</Closing>' % esc_jsx_text(links_to_jsx(b['html'])).strip())
    out.append('            </Text>')
    out.append('        </Group>')

out.append('    </FileCard>')
out.append('}')

open('/downloads/ed38paper-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
