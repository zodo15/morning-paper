#!/usr/bin/env python3
"""Generate the paper File's App.tsx from day-51.json, from day-51.json, mirroring Ed50's 13-group shape."""
import json, re, html, sys

d = json.load(open('/downloads/morning-paper/editions-src/day-51.json'))
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

ANCHORS = {0: ['s-route'], 2: ['s-markets'], 3: ['s-ipo'], 4: ['s-movers'], 5: ['s-corp'], 6: ['s-gold'], 7: ['s-ai'], 8: ['s-concept'], 9: ['s-board'], 11: ['s-week'], 12: ['s-notes']}
# front-page: anchor before specific story index
FP_ANCHORS = {0: ['s-front','s-split'], 1: ['s-earnings'], 2: ['s-anthropic'], 3: ['s-asia'], 4: ['s-tatasteel'], 5: ['s-deadline'], 6: ['s-mahanadi'], 7: ['s-data']}
DETAIL = {0:'#s-split',1:'#s-earnings',2:'#s-anthropic',3:'#s-asia',4:'#s-tatasteel',5:'#s-deadline',6:'#s-mahanadi',7:'#s-data',8:'#s-markets'}

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
out.append("import { Bullets, Callout, Closing, FileCard, Group, Header, Heading, Paragraph, Rows, Row, Text, TextLink, BarChart, Figure, Table, RangeChart } from '@instinct/files';")
out.append("import d51hero from './photos/d51-hero.jpg';")
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
out.append('        <Header title="%s"' % "The split tape and the holiday deal.")
fact_jsx = esc_jsx_text(links_to_jsx(ed['fact']))
out.append('            fact={`%s`}' % fact_jsx.replace('`','\\`'))
intro_jsx = esc_jsx_text(ed['intro'])
out.append('            intro="%s" />' % intro_jsx.replace('"','&quot;'))
out.append('        <Figure src={d51hero} alt="Abstract plate: a brass balance scale at dawn, one pan holding a glowing microchip sitting low, the other pan holding a wheat sheaf and a brick riding high, soft morning light" caption="Abstract plate for edition 51." fit="cover" />')

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
                out.append('''                <BarChart label="Leaders and laggards among the large names this paper tracks, Monday 23 Nov - BSE official prints, reprinted with no Tuesday session" orientation="bars" data={[
                    { label: 'Tech Mahindra', value: 2.1 },
                    { label: 'HCL Tech', value: 1.9 },
                    { label: 'Infosys', value: 0.7 },
                    { label: 'ONGC', value: -0.3 },
                    { label: 'Voltas', value: -0.8 },
                    { label: 'JSW Steel', value: -2.2 },
                    { label: 'Kotak Bank', value: -2.5 },
                    { label: 'Hindalco', value: -3.1 },
                ]} />''')
            elif 'Open lines' in svg:
                out.append('''                <Table
                    caption="Open lines - no session Tuesday; prices are BSE official closes, Monday 23 November"
                    options={[
                        { number: 1, name: 'Kotak Mahindra Bank' },
                        { number: 2, name: 'ONGC' },
                        { number: 3, name: 'JSW Steel' },
                        { number: 4, name: 'Hindalco' },
                    ]}
                    rows={[
                        { label: 'Status', values: ['Watchlist - trigger held', 'Watchlist - inside coil, breakout leg not re-established', 'Watchlist - R:R fails screen', 'Watchlist - candidate, reclaim failed'], best: 0 },
                        { label: 'Entry / trigger', values: ['Post-print strength above Rs 437.55 - held above it for a twentieth session, close Rs 503.00 (-2.52%); day low 501.20 never threatened the line (day high 521.30)', 'Breakout above 228 with crude holding - close Rs 222.90 (-0.27%), an eighth session under the line; day high 224.95 equals Friday high exactly; Brent settled at $89.37 Monday', 'Hold 1,158.95, then reclaim 1,218.90-1,222.30 - close Rs 1,311.00 (-2.16%), the 1,370 target untouched', 'No verified entry zone yet - close Rs 901.20 (-3.13%); Friday 911-912 reclaim failed, dipped to 899.20 (day high 914.55)'], },
                        { label: 'Stop / invalidation', values: ['Below Rs 420 shelves it', 'Coil floor Rs 218.50', 'Under 1,158.95 breaks the floor', 'n/a (not a setup)'], },
                        { label: 'Target / objective', values: ['Structured-setup candidate', 'Coil top Rs 238.75', '5 November swing high near Rs 1,370', 'n/a'], },
                        { label: 'R:R at worst fill', values: ['n/a (not a setup)', 'below the screen', '~0.39 to 1 - fails the screen at current levels', 'n/a'], },
                        { label: 'Reference price', values: ['Rs 503.00 (Mon close)', 'Rs 222.90 (Mon close)', 'Rs 1,311.00 (Mon close)', 'Rs 901.20 (Mon close)'], },
                    ]}
                />''')
            else:
                # ONGC range chart
                out.append('''                <RangeChart
                    label="ONGC in rupees: coil floor to coil top, marker at Monday's close (no session Tuesday)"
                    rows={[
                        { label: 'ONGC', low: 218.50, now: 222.90, high: 238.75, highlight: true },
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
            out.append('                <Closing>%s</Closing>' % esc_jsx_text(links_to_jsx(b['html'])).strip())
    out.append('            </Text>')
    out.append('        </Group>')

out.append('    </FileCard>')
out.append('}')

open('/downloads/ed51paper-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
