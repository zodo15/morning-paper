#!/usr/bin/env python3
"""Generate the LR38 File App.tsx from longreads.json['38'], mirroring LR37's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['41']

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
out.append('            intro="%s" />' % "Seven chapters: the presses, the second company, the contract, the build-out, the fourth leg, the Friday and the podium. The record here runs through the Transportation Department’s Saturday statement, the FAA’s contract description, L3Harris’s own releases and program pages, the 2002 award reporting, the Encyclopedia of Cleveland History, and the weekend’s wire coverage; all prices are the closes named in the text.")

for g in lr['groups']:
    out.append('')
    out.append('        <Heading>%s</Heading>' % g['heading'])
    out.append('        <Text>')
    for b in g['blocks']:
        out.append('            <Paragraph>%s</Paragraph>' % links_to_jsx(b['html'].strip()))
    out.append('        </Text>')

out.append('')
out.append('        <Closing>Sources read for this piece: the Transportation Department’s Saturday statement (the router flood, the copper-to-fiber maintenance, the safe landings, the provisional no-cyber assessment); USA Today’s probe with Reuters’s Arkansas-and-Texas detail and L3Harris’s Saturday statement; Fox Business’s profile of the company and Duffy’s “stuck with L3Harris” line; the FAA’s own contract description via its 2022 extension notice; Washington Technology’s 2002 report of the $1.7 billion FTI award; the Encyclopedia of Cleveland History for the Harris presses-to-electronics years; the corporate record for L-3’s 1997 founding and the 2019 merger; L3Harris’s own history page, its Aerojet Rocketdyne completion release and its 50-percent modernization milestone. The investigation’s central question - installer error or faulty router - was undetermined at press time, and this piece says so rather than guessing.</Closing>')
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed41lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines')
