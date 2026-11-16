#!/usr/bin/env python3
"""Generate the LR38 File App.tsx from longreads.json['38'], mirroring LR37's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['42']

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
out.append('            intro="%s" />' % "Seven chapters: the exit, the constitution, the customers, the money, the burn, the guardrails and the pricing room. The record here is Anthropic’s own amended prospectus, with the company’s roadshow post for the offer’s shape and named press for the range, the framing and the founder arithmetic.")

for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append('        <Closing>Sources read for this piece: Anthropic’s S-1/A-2 on EDGAR - the founding and founder biographies, the revenue and loss tables with their own fair-value caveat, the purchase-commitments table, the Amazon and Google agreements, the concurrent private placement, and the trust, founder-share and benefit-fund structure; the company’s roadshow post for the primary-secondary split; TechCrunch for the range and implied valuation; CNBC for the make-or-break framing; stockanalysis for the founder-stakes arithmetic. The six-times-covered book is Bloomberg’s reporting and is attributed as such; the offer prices Wednesday, and this piece does not guess the number.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed42lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines')
