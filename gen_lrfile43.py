#!/usr/bin/env python3
"""Generate the LR43 File App.tsx from longreads.json['43'], mirroring LR42's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['43']

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
out.append('            intro="%s" />' % "Seven chapters: the counter, the store, the hire, the machine, the sharing, the listing and the discipline. The record here is the company’s own results releases and exchange filings, with Forbes India’s reporting for the build years and The Hindu for the debut.")

for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append('        <Closing>Sources read for this piece: Forbes India’s boardroom account of the DMart model and its profile of Radhakishan Damani - the Apna Bazar apprenticeship, the eight-day payment rule, the operating numbers, the 2009 ESOP and the pre-listing stakes; The Hindu’s market report of the 21 March 2017 debut; the Economic Times’ two profiles for the market years, with their attributed recollections kept attributed; Avenue Supermarts’ own FY26 results release and the Q2 FY27 scorecard for the current numbers; and the NSE exchange filing that fixed the succession dates a year ahead. Quotes are as these sources report them; no scenes or settings are invented.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed43lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
