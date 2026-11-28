#!/usr/bin/env python3
"""Generate the LR54 File App.tsx from longreads.json['54'], mirroring LR52's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['54']

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
out.append("import lr54hero from './photos/lr54-hero.jpg';")
out.append("import lr54int1 from './photos/lr54-int1.jpg';")
out.append("import lr54int2 from './photos/lr54-int2.jpg';")
out.append("import lr54int3 from './photos/lr54-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: the room nobody used, a manager borrowed for a year, no machine in the country, the import bargain, cutting the cord, a sensitive topic, and the company that pays the parent. The record here is the Tata group's own heritage pages, TCS's own site and results release, Dinesh C. Sharma's account in The Wire, MIT Technology Review's profile of F.C. Kohli, Reuters on the 2004 offer, Business Standard's review of Ramadorai's book, and Moneycontrol and ET Now on the latest numbers.")
out.append('        <Figure src={lr54hero} alt="Abstract plate: a large 1970s computer room seen from a doorway, tape reels and cabinets in soft silhouette, one window of morning light falling across an empty desk" caption="Abstract plate for the long read - a computer room, and the daylight that reached it." fit="cover" />')

figmap = {'lr54-int1': 'lr54int1', 'lr54-int2': 'lr54int2', 'lr54-int3': 'lr54int3'}
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
out.append("        <Closing>Sources read for this piece: the Tata group's heritage pages (the 2021 history of TCS, the 2024 profile of F.C. Kohli and the TCS timeline); TCS's own site and its second-quarter results release; Dinesh C. Sharma's account in The Wire Science; MIT Technology Review's 2013 profile of Kohli; Reuters' report on the 2004 offer; Business Standard's review of S. Ramadorai's book; Moneycontrol and ET Now for the latest figures; Hindustan Times for the Tata Sons agenda. Where sources disagree on a date, the date is left out.</Closing>")
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed54lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
