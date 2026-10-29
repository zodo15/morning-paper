#!/usr/bin/env python3
"""One story per push. Dry run prints derived payload without sending."""
import argparse,json,urllib.request,os,re
p=argparse.ArgumentParser();p.add_argument('--card-id',required=True);p.add_argument('--dry-run',action='store_true');a=p.parse_args()
base='https://morning-paper-zodo15s-projects.vercel.app'
cards=json.load(urllib.request.urlopen(base+'/api/cards'))['cards'];c=next(x for x in cards if x['id']==a.card_id)
def sentence(t,cap):
 parts=re.split(r'(?<=[.!?])\s+',t)
 out=parts[0]
 if len(out)>cap:raise SystemExit('First sentence exceeds push cap; supply a shorter reviewed sentence in the card before sending')
 return out
payload={'pushOnly':True,'pushTitle':sentence(c['headline'],110),'pushGist':sentence(c['body'],160),'url':'./?c='+c['id'],'tag':c['id']}
if a.dry_run:print(json.dumps(payload,indent=2));raise SystemExit
with open('/tmp/wp/sendtoken') as f:tok=f.read().strip()
req=urllib.request.Request(base+'/api/card',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json'})
print(urllib.request.urlopen(req).read().decode())
