# Ed53 live correction. Edits editions-src/day-53.json (text only).
import json
A1 = "The two largest Tata trusts - the Sir Dorabji Tata Trust and the Sir Ratan Tata Trust, whose trusts together control 66% of Tata Sons - sued"
B1 = "Two of the Tata trusts - the Sir Dorabji Tata Trust and the RD Tata Trust, among the Tata trusts that together control 66% of Tata Sons - sued"
A2 = "The suits' plaintiffs are the Sir Dorabji Tata Trust and the Sir Ratan Tata Trust, named consistently by Bar and Bench's account and The Economic Times' report; a startup roundup's differing name for the second trust is disregarded."
B2 = "Correction: the suits' plaintiffs are the Sir Dorabji Tata Trust and the RD Tata Trust, as named by The Indian Express, LiveLaw and The Hindu. An earlier version of this edition named the second trust as the Sir Ratan Tata Trust and called the plaintiffs the two largest Tata trusts, controlling 66% of Tata Sons. Both were wrong: the 66% stake belongs to the Tata Trusts together."
p='editions-src/day-53.json'
s=open(p).read()
for a,b in [(A1,B1),(A2,B2)]:
    assert s.count(a)==1, a[:40]
    s=s.replace(a,b)
open(p,'w').write(s)
d=json.loads(s); print('ok')
