#!/usr/bin/env python3
"""Generate the LR52 File App.tsx from longreads.json['52'], mirroring LR51's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['52']

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
out.append("import lr52hero from './photos/lr52-hero.jpg';")
out.append("import lr52int1 from './photos/lr52-int1.jpg';")
out.append("import lr52int2 from './photos/lr52-int2.jpg';")
out.append("import lr52int3 from './photos/lr52-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: Bihar Tubes, the son's rewrite, selling pipe like soap, the balance sheet behind the brand, the Sunday boards, the tape votes, and what the pipe carries now. The record here is CARE Ratings' March 2025 credit report, the company's own story page and timeline, its recorded company history, Tata Steel's board-outcome filing and press release, APL Apollo's investor deck, the SEBI open-offer announcement, and CNBC-TV18's deal anatomy.")
out.append('        <Figure src={lr52hero} alt="Abstract plate: a single long steel tube running diagonally across a dark field, its surface wrapped half in plain grey mill finish and half in bright colour-coded branding bands, workshop light from one side" caption="Abstract plate for the long read - one pipe, two prices: by the kilo, and by the brand." fit="cover" />')

figmap = {'lr52-int1': 'lr52int1', 'lr52-int2': 'lr52int2', 'lr52-int3': 'lr52int3'}
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
out.append("        <Closing>Sources read for this piece: CARE Ratings' March 2025 credit report for the founding, family and financial record; the company's own story page and its Journey Through Time timeline for scale and network; the recorded company history for the listing, bonus and acquisition dates; Tata Steel's board-outcome filing and press release for the slump sale, share purchase and business figures; APL Apollo's investor deck for the funding plan, capacity bridge and 2035 ambition; the SEBI open-offer public announcement for the stake math, offer price and conditions; CNBC-TV18's deal anatomy for the market verdict and the on-record conflict question; BSE's official prints for the first-tape prices. Historical figures carry their dates; no scenes or settings are invented. A business story, not investment advice.</Closing>")
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed52lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
