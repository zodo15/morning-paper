#!/usr/bin/env python3
"""Generate the LR48 File App.tsx from longreads.json['48'], mirroring LR47's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['48']

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
out.append("import lr48hero from './photos/lr48-hero.jpg';")
out.append("import lr48int1 from './photos/lr48-int1.jpg';")
out.append("import lr48int2 from './photos/lr48-int2.jpg';")
out.append("import lr48int3 from './photos/lr48-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: Denny’s, the octopus, pay us for nothing, one tapeout, the first GPU, the second zero, and a million times. The record here is Sequoia’s Crucible Moments transcript - the founders’ and backers’ own words - Nvidia’s investor FAQ for the listing facts, and Reuters, CNBC and The Verge for the probe week.")
out.append('        <Figure src={lr48hero} alt="Abstract plate: a green circuit trace rising from a roadside diner table into a server hall" caption="Abstract plate for the long read." fit="cover" />')

figmap = {'lr48-int1': 'lr48int1', 'lr48-int2': 'lr48int2', 'lr48-int3': 'lr48int3'}
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
out.append('        <Closing>Sources read for this piece: Sequoia Capital’s Crucible Moments episode on Nvidia - Jensen Huang, Chris Malachowsky, Mark Stevens and Andrew Ng in their own words; Nvidia’s investor FAQ for the IPO and incorporation record; and Reuters, CNBC and The Verge for the week of the SEC examination. Quotes are as these sources report them; no scenes or settings are invented.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed48lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
