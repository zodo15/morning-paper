#!/usr/bin/env python3
"""Generate the LR49 File App.tsx from longreads.json['49'], mirroring LR48's shape."""
import json, re

d = json.load(open('/downloads/morning-paper/editions-src/longreads.json'))
lr = d['49']

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
out.append("import lr49hero from './photos/lr49-hero.jpg';")
out.append("import lr48int1 from './photos/lr49-int1.jpg';")
out.append("import lr48int2 from './photos/lr49-int2.jpg';")
out.append("import lr48int3 from './photos/lr49-int3.jpg';")
out.append('')
for url, name in consts.items():
    out.append("const %s = '%s';" % (name, url))
out.append('')
out.append('export function App() {')
out.append('    return <FileCard>')
out.append('        <Header title="%s"' % lr['title'])
out.append('            fact={`%s`}' % lr['fact'].replace('`', '\\`'))
out.append('            intro="%s" />' % "Seven chapters: Deccan Gymkhana, disks in the mail, the door marked no, the IPO almost nobody wanted, a small step for Nasdaq, twenty-three months, and the ledger. The record here is the company's own history and founders' pages, the Murthys' on-record interviews, the 1999 listing accounts and the 1993 backstory.")
out.append('        <Figure src={lr49hero} alt="Abstract plate: seven small lamps on a windowsill above a quiet street, their light pooling into a rising grid" caption="Abstract plate for the long read - seven lamps in a Pune window." fit="cover" />')

figmap = {'lr49-int1': 'lr48int1', 'lr49-int2': 'lr48int2', 'lr49-int3': 'lr48int3'}
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
out.append("        <Closing>Sources read for this piece: Infosys's own history, milestones and founders pages; Sudha Murty's interviews with moneycontrol and The Week and the NDTV Dialogues transcript; Kris Gopalakrishnan's recollections in The Week; the Reuters listing-day account carried by WIRED and the company's own 11 March 1999 release; CNBC-TV18's 1993 IPO backstory and arithmetic; and Mint's 2018 retrospective with T.V. Mohandas Pai. Quotes are as these sources report them; no scenes or settings are invented.</Closing>")
out.append('    </FileCard>;')
out.append('}')

open('/downloads/ed49lr-src-App.tsx', 'w').write('\n'.join(out) + '\n')
print('LR App.tsx generated:', len(out), 'lines;', len(consts), 'link consts')
