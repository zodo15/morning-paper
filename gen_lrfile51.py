#!/usr/bin/env python3
"""Generate the LR50 File App.tsx from longreads.json['50'], mirroring LR50's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['51']

consts = {}
def const_name(url):
    if url in consts: return consts[url]
    n = 'U%d' % (len(consts)+1)
    consts[url] = n
    return n

def links_to_jsx(h):
    def rep(m):
        return '<TextLink href={%s}>%s</TextLink>' % (const_name(m.group(1)), m.group(2))
    return re.sub(r'<a href="([^"]+)" target="_blank" rel="noopener">([^<]+)</a>', rep, h)

for g in lr['groups']:
    for b in g['blocks']:
        if b.get('t') == 'p':
            links_to_jsx(b['html'])

out = []
out.append("import React from 'react';")
out.append("import { Closing, FileCard, Header, Heading, Figure, Paragraph, Text, TextLink } from '@instinct/files';")
out.append('')
out.append("import './style.css';")
out.append("import lr51hero from './photos/lr51-hero.jpg';")
out.append("import lr51int1 from './photos/lr51-int1.jpg';")
out.append("import lr51int2 from './photos/lr51-int2.jpg';")
out.append("import lr51int3 from './photos/lr51-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: Weston\'s son, a dollar fifty a television, what not to do, the drill, the listing, the phone pivot, and the ledger. The record here is the company\'s draft red herring prospectus filed with SEBI, its own site, IBEF\'s milestone record, Counterpoint\'s rankings, ET\'s results report, two Forbes India profiles and EY\'s entrepreneur profile.")
out.append('        <Figure src={lr51hero} alt="Abstract plate: a long assembly line receding toward a bright doorway, unmarked white boxes on the line, each box faintly reflecting a different coloured light, early morning haze" caption="Abstract plate for the long read - one line, a hundred brands, no name on the box." fit="cover" />')

figmap = {'lr51-int1': 'lr51int1', 'lr51-int2': 'lr51int2', 'lr51-int3': 'lr51int3'}
for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        if b.get('t') == 'figure':
            key = b['img'].split('/')[-1].replace('.jpg','')
            out.append('        </Text>')
            out.append('        <Figure src={%s} alt="%s" caption="%s" />' % (figmap[key], b['alt'].replace('"','&quot;'), b['caption'].replace('"','&quot;')))
            out.append('        <Text>')
        else:
            out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append("        <Closing>Sources read for this piece: Dixon Technologies' draft red herring prospectus filed with SEBI (May 2017) for the incorporation history, listing economics and FY16 production shares; the company's own site for current scale; IBEF's milestone record for the listing dates, the Longcheer joint venture, capex and facilities; Counterpoint's April 2026 rankings for the 2025 smartphone EMS table; ET's report of the Q2 FY27 exchange filing for results; Forbes India's 2022 and 2024 profiles and EY's entrepreneur profile for the founding story and quotes. Historical figures and quotes carry their dates; the Q2 profit is printed on ET's net-profit convention (Rs 343.7 crore) with margins as reported; no scenes or settings are invented. A manufacturing story, not investment advice.</Closing>")
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed51lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
