#!/usr/bin/env python3
"""Generate the LR43 File App.tsx from longreads.json['46'], mirroring LR44's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['46']

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
out.append("import lr46hero from './photos/lr46-hero.jpg';")
out.append("import lr46int1 from './photos/lr46-int1.jpg';")
out.append("import lr46int2 from './photos/lr46-int2.jpg';")
out.append("import lr46int3 from './photos/lr46-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: the pink sheets, Trumbull, February 8 1971, the crash that made it, the exchange sells itself, the empire and the decision. The record here is the SEC Historical Society’s Nasdaq exhibit and interviews, Nasdaq’s own fifty-year history and investor FAQ, the NASD’s own history, the Congressional Research Service’s 2000-06 account of the spin-off, and the 2007 OMX offer documents.")
out.append('        <Figure src={lr46hero} alt="Abstract plate: a wall of glowing green quote screens where a trading floor should be" caption="Abstract plate for the long read." fit="cover" />')

figmap = {'lr46-int1': 'lr46int1', 'lr46-int2': 'lr46int2', 'lr46-int3': 'lr46int3'}
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
out.append('        <Closing>Sources read for this piece: ASML’s own founding story (April 2024) and company history timeline; Michael A. Cusumano’s “The ASML Monopoly” in the Communications of the ACM (September 2026) for the EUV program’s cost, the 2012 customer co-investment, the machine’s economics and China’s catch-up effort, quoted as reported; MIT Technology Review’s June 2026 High NA feature for Benschop’s machine and its price; and ASML’s Q3 2026 results release for the record quarter and the sold-out-through-2028 statement. Quotes are as these sources report them; no scenes or settings are invented.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed46lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
