#!/usr/bin/env python3
"""Generate the LR50 File App.tsx from longreads.json['50'], mirroring LR49's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['50']

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
out.append("import lr50hero from './photos/lr50-hero.jpg';")
out.append("import lr50int1 from './photos/lr50-int1.jpg';")
out.append("import lr50int2 from './photos/lr50-int2.jpg';")
out.append("import lr50int3 from './photos/lr50-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: born in sin, not the first choice, December 1983, the machine, the state exits, Manesar, and the ledger. The record here is the company's and Suzuki's own pages and releases, its FY2025-26 annual report, Business Standard and Forbes India histories, and the New York Times India blog's 2012 and 2014 accounts.")
out.append('        <Figure src={lr50hero} alt="Abstract plate: a small boxy hatchback at the start of a long road climbing toward a distant skyline of factory chimneys, morning light" caption="Abstract plate for the long read - the small car and the long road." fit="cover" />')

figmap = {'lr50-int1': 'lr50int1', 'lr50-int2': 'lr50int2', 'lr50-int3': 'lr50int3'}
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
out.append("        <Closing>Sources read for this piece: Maruti Suzuki's own business description and its 19 July 2012 Manesar statement; Suzuki Motor's 2011 ten-million and 2018 twenty-million milestone releases; Maruti Suzuki's FY2025-26 Annual Integrated Report for the current Suzuki stake (as of 31 March 2026) and FY26 milestones; Business Standard's 2014 forty-year history; Forbes India's economic-milestone retelling; and the New York Times India blog's 2012 Manesar account and 2014 Maruti 800 farewell. Historical figures carry their dates; quotes are as these sources report them; no scenes or settings are invented. A manufacturing story, not investment advice.</Closing>")
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed50lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
