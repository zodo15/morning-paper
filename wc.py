#!/usr/bin/env python3
"""Standing Slow Burn word counter (validated against Ed36 = 4,824).
Counts: fact (excluding the "This edition runs N words." sentence) + intro
+ p/closing html + rows title+detail + bullets items. Charts and headings excluded.
Splits on whitespace and dashes."""
import json, re, sys
def strip(h):
    h = re.sub(r"<[^>]+>", " ", h or "")
    for a,b in [("&amp;","&"),("&nbsp;"," "),("&#39;","'"),("&quot;",'"'),("&rsquo;","'"),("&ndash;","-"),("&mdash;","-"),("&lt;","<"),("&gt;",">"),("&hellip;","...")]:
        h = h.replace(a,b)
    return h
def wc(t): return len([w for w in re.split(r"[\s\u2013\u2014-]+", strip(t)) if w])
def bw(b):
    if b["t"]=="rows": return sum(wc(i.get("title",""))+wc(i.get("detail","")) for i in b.get("items",[]))
    if b["t"]=="bullets": return sum(wc(x) for x in b.get("items",[]))
    if b["t"]=="chart": return 0
    return wc(b.get("html",""))
d = json.load(open(sys.argv[1]))
ed = d["edition"]
fact = re.sub(r"This edition runs [0-9,]+ words\.", "", ed["fact"])
print(wc(fact) + wc(ed["intro"]) + sum(bw(b) for g in ed["groups"] for b in g["blocks"]))
