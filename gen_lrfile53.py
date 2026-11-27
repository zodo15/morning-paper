#!/usr/bin/env python3
"""Generate the LR53 File App.tsx from longreads.json['53'], mirroring LR52's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['53']

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
out.append("import lr53hero from './photos/lr53-hero.jpg';")
out.append("import lr53int1 from './photos/lr53-int1.jpg';")
out.append("import lr53int2 from './photos/lr53-int2.jpg';")
out.append("import lr53int3 from './photos/lr53-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: four friends and a name, the sign-painter's mascot, the vote on Marine Drive, the quiet company, the dealer machine, the challenger at the door, and what the founders left behind. The record here is the company's own history pages, the published biography of the founding partnership, the business press of 1997 and 2013, the challenger's own press release, the latest quarter's results coverage, and BSE's official prints.")
out.append('        <Figure src={lr53hero} alt="Abstract plate: four empty wooden chairs side by side in a bare rented room, each painted a different bright colour, a fifth chair turned toward the window, soft afternoon light" caption="Abstract plate for the long read - four friends took four chairs; the company took the room." fit="cover" />')

figmap = {'lr53-int1': 'lr53int1', 'lr53-int2': 'lr53int2', 'lr53-int3': 'lr53int3'}
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
out.append("        <Closing>Sources read for this piece: Asian Paints' own history and heritage pages for the founding, the names and the early years; Anupam Gupta's published biography and its reviews in the business press for the four-friends partnership and Gattu; India Today's and Business Standard's 1997 reporting for the buy-out vote and ICI's statement; Forbes Asia and Forbes India for the quiet-executive portrait and the dealer machine; Grasim's own press release for the Birla Opus entry and capacity figures; moneycontrol's results coverage for the latest quarter; TheBetterIndia for colour, with one inflated figure set aside as unverifiable; BSE's official prints for the tape. Historical figures carry their dates; no scenes or settings are invented. A business story, not investment advice.</Closing>")
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed53lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
