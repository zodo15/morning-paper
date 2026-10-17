#!/usr/bin/env python3
"""Send the 'edition is live' push for the Morning Paper site.

Usage: python3 scripts/push_edition.py --day N --title "..." --gist "..."
Token comes from PUSH_SEND_TOKEN env or /tmp/wp/sendtoken (never committed).
Honours quiet hours server-side (11 PM-7 AM IST, quiet-toggle subscribers skipped).
"""
import argparse, json, os, sys, urllib.request

BASE = 'https://morning-paper-zodo15s-projects.vercel.app'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--day', required=True, type=int)
    p.add_argument('--title', required=True, help='push title, e.g. "Edition 13 is live: <lead headline>"')
    p.add_argument('--gist', required=True, help='push body, calm news wording, no buy call')
    p.add_argument('--url', default='./', help='tap target; ./ opens Today')
    a = p.parse_args()
    tok = os.environ.get('PUSH_SEND_TOKEN', '')
    if not tok:
        try: tok = open('/tmp/wp/sendtoken').read().strip()
        except OSError: pass
    if not tok:
        sys.exit('no send token (PUSH_SEND_TOKEN or /tmp/wp/sendtoken)')
    payload = {'pushOnly': True, 'pushTitle': a.title, 'pushGist': a.gist,
               'url': a.url, 'tag': 'edition-%d' % a.day}
    req = urllib.request.Request(BASE + '/api/card', data=json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(r.status, r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit('HTTP %d: %s' % (e.code, e.read().decode()))

if __name__ == '__main__':
    main()
