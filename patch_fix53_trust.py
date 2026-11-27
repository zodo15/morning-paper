# Ed53 live correction (PREPARED, NOT APPLIED). Run only on main's explicit go, then rebuild data, re-run wc.py, redeploy, regenerate audio for affected chunks.
import sys
A1 = "The two largest Tata trusts - the Sir Dorabji Tata Trust and the Sir Ratan Tata Trust, whose trusts together control 66% of Tata Sons - sued"
B1 = "Two of the Tata trusts - the Sir Dorabji Tata Trust and the RD Tata Trust, among the Tata trusts that together control 66% of Tata Sons - sued"
A2 = "The suits' plaintiffs are the Sir Dorabji Tata Trust and the Sir Ratan Tata Trust, named consistently by Bar and Bench's account and The Economic Times' report; a startup roundup's differing name for the second trust is disregarded."
B2 = "The suits' plaintiffs are the Sir Dorabji Tata Trust and the RD Tata Trust, as named in The Indian Express, LiveLaw and The Hindu and in the damages figures reported by Bar and Bench; a differing name for the second trust in some reports is disregarded."
import json
for f in ['editions-src/day-53.json']:
    s=open(f).read()
    for a,b in [(A1,B1),(A2,B2.replace("'","\\'") if False else B2)]:
        n=s.count(a.replace("'","\\'")) or s.count(a)
        print(f,'matches',n)
