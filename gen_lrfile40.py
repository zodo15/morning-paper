#!/usr/bin/env python3
"""Generate the LR38 File App.tsx from longreads.json['38'], mirroring LR37's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['40']

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
        links_to_jsx(b['html'])

out = []
out.append("import React from 'react';")
out.append("import { Closing, FileCard, Header, Heading, Paragraph, Text, TextLink } from '@instinct/files';")
out.append('')
out.append("import './style.css';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: the acorn, the twelve, the bet, the listing, the suitors, the second listing and the phone call. The record here runs through Arm’s own official history and releases, SoftBank’s completion announcement, Nvidia’s acquisition and termination releases, and the FT’s report carried via Reuters; all prices are the closes named in the text.")

for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append('        <Closing>Sources read for this piece: Arm’s own official history (the Acorn years, the ARM1, the 1990 joint venture and its twelve founders, the Newton, Saxby’s licensing model, the 1998 listing, Warren East, the 350-billion-chip count, the smartphone share and the Arm AGI CPU); Arm’s Rene Haas appointment release and IPO pricing release; SoftBank’s 2016 completion announcement for the 24-billion-pound price; Nvidia and SoftBank’s 2022 termination release for the deal’s death and Jensen Huang’s quotes; the Financial Times’ succession report via Reuters/CNA, carried attributed - Haas one of several candidates, no guarantee, Arm declining comment, Reuters unable to verify independently. The share prices named are official closes.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed40lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines')
