#!/usr/bin/env python3
"""Generate the paper File's App.tsx from day-53.json, mirroring Ed52's 13-group shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/day-53.json'))
ed = d['edition']

consts = {}
def const_name(url):
    if url in consts: return consts[url]
    n = 'U%d' % (len(consts)+1)
    consts[url] = n
    return n

def links_to_jsx(h):
    def rep(m):
        url, txt = m.group(1), m.group(2)
        return '<TextLink href={%s}>%s</TextLink>' % (const_name(url), txt)
    return re.sub(r'<a href="([^"]+)" target="_blank" rel="noopener">([^<]+)</a>', rep, h)

def esc_jsx_text(s):
    return s.replace('{', '&#123;').replace('}', '&#125;')

ANCHORS = {0: ['s-route'], 2: ['s-markets'], 3: ['s-ipo'], 4: ['s-movers'], 5: ['s-corp'], 6: ['s-gold'], 7: ['s-ai'], 8: ['s-concept'], 9: ['s-board'], 11: ['s-week'], 12: ['s-notes']}
FP_ANCHORS = {0: ['s-front','s-tata'], 1: ['s-us'], 2: ['s-bok'], 3: ['s-asia'], 4: ['s-flows'], 5: ['s-oil'], 6: ['s-mahanadi'], 7: ['s-europe']}
DETAIL = {0:'#s-tata',1:'#s-tata',2:'#s-bok',3:'#s-asia',4:'#s-oil',5:'#s-markets',6:'#s-mahanadi',7:'#s-ai'}

def para_clean(h, strong_prefix=False, detail=None):
    h2 = links_to_jsx(h.strip())
    if strong_prefix:
        m = re.match(r'(\d+\. [^.]+\.)', h2)
        if not m:
            m = re.match(r'([^:]+?:)', h2)
        if m and '<' not in m.group(1):
            h2 = '<strong>' + m.group(1) + '</strong>' + h2[m.end():]
    if detail:
        h2 = h2 + ' <a href="%s">Detail</a>' % detail
    h2 = h2.replace('{', '\x01').replace('}', '\x02')
    h2 = h2.replace('\x01U', '{U').replace('\x02', '}')
    return '                <Paragraph>%s</Paragraph>' % h2

out = []
out.append("import { Bullets, Callout, Closing, FileCard, Group, Header, Heading, Paragraph, Rows, Row, Text, TextLink, BarChart, Figure, Table, RangeChart } from '@instinct/files';")
out.append("import d53hero from './photos/d53-hero.jpg';")
out.append('')
out.append('function Anchor({ id }: { id: string }) { return <span id={id} />; }')
out.append('')

groups = ed['groups']
for g in groups:
    for b in g['blocks']:
        if b['t'] == 'p':
            links_to_jsx(b['html'])
        elif b['t'] == 'closing':
            links_to_jsx(b.get('html', b.get('text','')))
links_to_jsx(ed['fact'])

for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')

out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % "The owners sue the company")
fact_jsx = esc_jsx_text(links_to_jsx(ed['fact']))
out.append('            fact={`%s`}' % fact_jsx.replace('`','\\`'))
intro_jsx = esc_jsx_text(ed['intro'])
out.append('            intro="%s" />' % intro_jsx.replace('"','&quot;'))
out.append('        <Figure src={d53hero} alt="Abstract plate: a courthouse bench silhouette behind a wall of paint swatches in daffodil and aquamarine, one swatch peeling to reveal an old ledger page, soft morning light" caption="Abstract plate for edition 53." fit="cover" />')

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
            if 'eaders and laggards' in svg:
                out.append('''                <BarChart label="Leaders and laggards among the large names this paper tracks, Thursday 26 Nov - % vs Wednesday close, BSE official prints" orientation="bars" data={[
                    { label: 'HCL Tech', value: 6.28 },
                    { label: 'Infosys', value: 4.69 },
                    { label: 'Tech Mahindra', value: 3.33 },
                    { label: 'Hindalco', value: 2.94 },
                    { label: 'ONGC', value: 0.50 },
                    { label: 'JSW Steel', value: 0.31 },
                    { label: 'Kotak Bank', value: 0.10 },
                    { label: 'Voltas', value: -0.65 },
                ]} />''')
            elif 'Open lines' in svg:
                out.append('''                <Table
                    caption="Open lines, BSE official closes, Thursday 26 November"
                    options={[
                        { number: 1, name: 'Kotak Mahindra Bank' },
                        { number: 2, name: 'ONGC' },
                        { number: 3, name: 'JSW Steel' },
                        { number: 4, name: 'Hindalco' },
                    ]}
                    rows={[
                        { label: 'Status', values: ['Watchlist - trigger held', 'Watchlist - inside coil, floor pressure eased', 'Watchlist - R:R fails screen', 'Watchlist - candidate strengthens'], best: 0 },
                        { label: 'Entry / trigger', values: ['Post-print strength above Rs 437.55 - held for a twenty-second session, close Rs 509.00 (+0.10%); day low 504.65 never threatened the line', 'Breakout above 228 with crude holding - close Rs 223.05 (+0.50%), a tenth session under the line; day low 222.10 eased off Wednesday&#39;s tightest test', 'Hold 1,158.95, then reclaim 1,218.90-1,222.30 - close Rs 1,305.00 (+0.31%), the 1,370 target untouched', 'No verified entry zone yet - close Rs 915.10 (+2.94%), back above the 911-912 zone for the first time since Friday&#39;s failed reclaim'], },
                        { label: 'Stop / invalidation', values: ['Below Rs 420 shelves it', 'Coil floor Rs 218.50', 'Under 1,158.95 breaks the floor', 'n/a (not a setup)'], },
                        { label: 'Target / objective', values: ['Structured-setup candidate', 'Coil top Rs 238.75', '5 November swing high near Rs 1,370', 'n/a'], },
                        { label: 'R:R at worst fill', values: ['n/a (not a setup)', 'below the screen', '~0.44 to 1 - fails the screen at current levels', 'n/a'], },
                        { label: 'Reference price', values: ['Rs 509.00 (Thu close)', 'Rs 223.05 (Thu close)', 'Rs 1,305.00 (Thu close)', 'Rs 915.10 (Thu close)'], },
                    ]}
                />''')
            else:
                out.append('''                <RangeChart
                    label="ONGC in rupees: coil floor to coil top, marker at Thursday&#39;s close"
                    rows={[
                        { label: 'ONGC', low: 218.50, now: 223.05, high: 238.75, highlight: true },
                    ]}
                    range={[218.50, 238.75]}
                    scaleLabels={['218.50', '238.75']}
                />''')
        elif t == 'rows':
            out.append('                <Rows>')
            for it in b['items']:
                out.append('                    <Row number="%s" name="%s" detail="%s" />' % (it['n'], esc_jsx_text(it['title']).replace('"','&quot;'), esc_jsx_text(it['detail']).replace('"','&quot;')))
            out.append('                </Rows>')
        elif t == 'bullets':
            out.append('                <Bullets items={[')
            for it in b['items']:
                j = links_to_jsx(it).replace('"','\\"')
                out.append('                    "%s",' % j)
            out.append('                ]} />')
        elif t == 'closing':
            out.append('                <Closing>%s</Closing>' % esc_jsx_text(links_to_jsx(b.get('html', b.get('text','')))).strip())
    out.append('            </Text>')
    out.append('        </Group>')

out.append('    </FileCard>')
out.append('}')

open('/downloads/ed53paper-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
