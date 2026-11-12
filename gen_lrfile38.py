#!/usr/bin/env python3
"""Generate the LR38 File App.tsx from longreads.json['38'], mirroring LR37's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['38']

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
out.append('            intro="%s" />' % "Seven chapters: the carbon desk, the pool table, the rename, the earthquake, the listing, the leverage, and the answer. The record here runs through CNBC's founding profile, Reuters' contract factbox and Breakingviews, the IPO prospectus, and the company's own quarterly release; all prices are the official closes named in the text.")

for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append('        <Closing>Sources read for this piece: CNBC\u2019s March 2025 founding profile of CoreWeave (founders, Natsource, the pool table, the rename, the Microsoft and Nvidia relationships); Reuters Breakingviews on the IPO; the final IPO prospectus on SEC EDGAR; Reuters\u2019 October 2026 factbox of the AI contracts and the lenders (OpenAI deals, about $50 billion of debt, default-insurance pricing on LSEG data); Reuters on the terminated Core Scientific merger; the company\u2019s own third-quarter 2026 release; Motley Fool\u2019s close report for 11 November 2026; Reuters\u2019 Trading Day for the market\u2019s reaction; Yahoo Finance\u2019s retrospective for the $187 high of 20 June 2025. The share prices are the official closes named in the text.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed38lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines')
