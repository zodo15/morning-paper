#!/usr/bin/env python3
"""Generate the LR38 File App.tsx from longreads.json['38'], mirroring LR37's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['39']

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
out.append('            intro="%s" />' % "Seven chapters: the dishwasher, the booth, the mistake, the bet, the earthquake, the summit and the Thursday. The record here runs through Stephen Witt’s New Yorker profile and his authorised biography, Nvidia’s own timeline, blog and resignation release, the Wall Street Journal, Axios, Inc. and Reuters; all prices are the official closes named in the text.")

for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append('        <Closing>Sources read for this piece: Stephen Witt’s New Yorker profile of Jensen Huang (childhood, Denny’s, the founding, the quadrilateral failure, CUDA, the AI bet and the 2023 re-rating) and the Taipei Times interview on his authorised biography; Nvidia’s own corporate timeline, Denny’s blog post and Thursday’s resignation release; Inc. on the RIVA 128 and the thirty-days motto; the Wall Street Journal’s resignation report; Axios for Kress’s staff note; Reuters (via Business Times) for the market’s verdict; Yahoo Finance’s historical table for the official close. The share prices are the official closes named in the text. Nvidia has given no reason for the resignation; the reported investigation is carried once, attributed, without detail.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed39lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines')
