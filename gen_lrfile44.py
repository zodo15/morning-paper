#!/usr/bin/env python3
"""Generate the LR43 File App.tsx from longreads.json['44'], mirroring LR42's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['44']

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
out.append("import lr44hero from './photos/lr44-hero.jpg';")
out.append("import lr44int1 from './photos/lr44-int1.jpg';")
out.append("import lr44int2 from './photos/lr44-int2.jpg';")
out.append("import lr44int3 from './photos/lr44-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: the writer, the transistor man, the pricing man, the call, the pure play, the avalanche and the yes. The record here is TSMC’s own company profile and earnings release, the IEEE’s 2011 profile of Morris Chang, Stanford’s and MIT’s accounts of his talks, and TrendForce’s share count via Focus Taiwan.")
out.append('        <Figure src={lr44hero} alt="Abstract plate: a silicon wafer held above a factory roofline" caption="Abstract plate for the long read." fit="cover" />')

figmap = {'lr44-int1': 'lr44int1', 'lr44-int2': 'lr44int2', 'lr44-int3': 'lr44int3'}
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
out.append('        <Closing>Sources read for this piece: the IEEE Spectrum’s 2011 profile of Morris Chang - the founding years, the TI career and the pure-play idea, quoted as reported; Stanford Engineering’s 2014 account of his Engineering Hero talk; MIT News’ 2023 account of his manufacturing lecture; TSMC’s own company profile and its 3Q26 earnings release for the current numbers; TrendForce’s second-quarter 2026 share count via Focus Taiwan; and the quarter’s coverage for the record-profit streak and expansion plans. Quotes are as these sources report them; no scenes or settings are invented.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed44lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
