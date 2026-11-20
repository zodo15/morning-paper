#!/usr/bin/env python3
"""Generate the LR47 File App.tsx from longreads.json['46'], mirroring LR46's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['47']

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
out.append("import lr47hero from './photos/lr47-hero.jpg';")
out.append("import lr47int1 from './photos/lr47-int1.jpg';")
out.append("import lr47int2 from './photos/lr47-int2.jpg';")
out.append("import lr47int3 from './photos/lr47-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: the banyan tree, one rupee each, corners and committees, the tower, the bomb and the scam, the brokers lose their club, and the venue. The record here is Business Standard’s and Fortune India’s 150-year histories, India Today’s and News18’s founding accounts, the Indian Express archive on demutualisation, the SEBI chairman’s own anniversary address, and FE’s flow record.")
out.append('        <Figure src={lr47hero} alt="Abstract plate: a wall of glowing green quote screens where a trading floor should be" caption="Abstract plate for the long read." fit="cover" />')

figmap = {'lr47-int1': 'lr47int1', 'lr47-int2': 'lr47int2', 'lr47-int3': 'lr47int3'}
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
out.append('        <Closing>Sources read for this piece: Fortune India’s and Business Standard’s 150-year histories of the BSE; India Today’s and News18’s founding accounts; the Indian Express archive on demutualisation; SEBI chairman Tuhin Kanta Pandey’s anniversary address (sebi.gov.in); CNBC-TV18’s evolution timeline; and FE’s record of November’s foreign flows. Quotes are as these sources report them; no scenes or settings are invented.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed47lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
