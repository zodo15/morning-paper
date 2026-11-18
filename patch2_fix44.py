import sys
def rep(fname, old, new, n=1):
    s = open(fname).read()
    c = s.count(old)
    assert c == n, (fname, c, old[:80])
    open(fname, 'w').write(s.replace(old, new))
    print('patched:', old[:70].replace('\n', ' '))
B = 'build_day44.py'

# --- new constants ---
rep(B, "US10YQ = 'https://www.cnbc.com/quotes/US10Y'",
 "US10YQ = 'https://www.cnbc.com/quotes/US10Y'\nFRPI = 'https://www.federalregister.gov/public-inspection/2026-23529/addressing-remote-access-to-advanced-semiconductors'\nHBLBANK = 'https://www.thehindubusinessline.com/markets/bank-nifty-breaks-into-uncharted-territory-as-fii-billions-back-indias-bull-run/article71711651.ece'\nTAK = 'https://doi.org/10.1016/0010-0285(73)90033-9'")

# --- lead1: after-hours pinning ---
rep(B, "rose about 5% in extended trading (' + a(INVFUT, 'the after-hours read') + ')",
 "rose nearly 5% in extended trading as of 18:52 ET (' + a(INVFUT, 'the after-hours read') + ')")

# --- lead BIS para rewrite ---
rep(B, """p(' The BIS compute rule is still not law. Two days after its release, the Federal Register carries no publication entry for RIN 0694-AK50 - checked again this morning - so every clock in the rule (the effective date, the sixty-day comments, the ninety-day runway) has yet to start (' + a(FRGOV, 'the Register') + '; ' + a(BISPDF, 'the rule text') + '). Until the entry exists, the rule remains released, not operative.'),""",
"""p(' The BIS compute rule is scheduled, not yet law. The remote-access rule - RIN 0694-AK50 - was filed with the Federal Register on Monday and sits on its public-inspection list, scheduled for publication on Thursday 19 November (' + a(FRPI, 'the inspection entry') + '; ' + a(BISPDF, 'the rule text') + '). Every clock keys off that publication: the rule takes effect on its publication date, comments run sixty days from it, and covered cloud providers have ninety days from effectiveness to obtain a license. Until the Thursday issue lands, the rule remains scheduled, not operative.'),""")

# --- lead Mumbai para: Bank Nifty record fix ---
rep(B, "The Nifty Bank hit a record 62,422 intraday; FIIs bought a twelfth straight session",
 "The Bank Nifty scaled a record 62,442.20 intraday and closed at a record 62,273.25 (' + a(HBLBANK, 'the banking report') + '); FIIs bought a twelfth straight session")

# --- front page block2: AH pinning ---
rep(B, "The stock\\'s +5% after-hours answer followed a 24% November slide",
 "The stock\\'s nearly-5% after-hours answer, as of 18:52 ET, followed a 24% November slide")

# --- front page Mumbai para: Bank Nifty + Laurus ---
rep(B, "the Nifty Bank\\'s record 62,422 intraday, closing up 697 points",
 "the Bank Nifty\\'s record 62,442.20 intraday and record close of 62,273.25, up 1.13% (' + a(HBLBANK, 'the banking report') + ')")
rep(B, "Laurus Labs gained over 5% after management ruled out further stake sales",
 "Laurus Labs gained over 5% after management said it had no plans to sell further stake")

# --- Goldmine: AH pinning ---
rep(B, "reported at 1:20 PM Pacific, and rose about 5% in extended trading",
 "reported at 1:20 PM Pacific, and rose nearly 5% in extended trading as of 18:52 ET")

# --- fact line: AH + consensus softening ---
rep(B, "up 103% against the $109.1 billion expected, and a $130 billion guide against the $125.1 billion expected; the stock rose about 5% after hours. '",
 "up 103%, and a $130 billion guide, both well above the LSEG consensus; the stock rose nearly 5% after hours. '")

# --- Goldmine: append the term paragraph (merge Term of the day in) ---
rep(B, """The paper labels each one as-of, and the open decides.'),
]})""",
"""The paper labels each one as-of, and the open decides.'),
 p(' One term worth owning: book building. When CNBC reports that Anthropic\\'s "order books closed" at 4 PM, the term is book building: the issuer\\'s banks collect bids from institutions - how many shares, at what price - before the final offer price is set (' + a(CNBCANT, 'the report') + '). The book is the tally of those bids; closing it ends the auction; pricing is the judgment that follows. An oversubscribed book is why an offering can price above its range: more demand than shares at the top end lets the banks move the clearing price up. The same mechanism runs in Mumbai - Urban Company\\'s Rs 2,500-crore QIP, opened Tuesday with a Rs 161.03 floor, is a book-built offer to institutions under SEBI\\'s rules (' + a(ST, 'the QIP report') + '). Watch for it tonight in the Anthropic print: the price, the multiple of the range, and what the book said.'),
]})""")

# --- Concept: replace accounting concept with psychology concept ---
rep(B, """G.append({'heading': 'One concept: customer concentration', 'blocks': [
 p(' Four customers made 47% of Nvidia\\'s $115.8 billion quarter - that single line, from Tuesday\\'s release, is a customer-concentration disclosure, and it is one of the most load-bearing numbers in any filing (' + a(NVPR, 'the release') + '). The concept: US disclosure rules make a company name any customer above 10% of revenue, and the resulting figure measures how much of the business depends on how few decisions. Concentration is not automatically fragility - those four are presumably the largest AI build-outs on earth, and their orders are the boom - but it converts four companies\\' budgets into one company\\'s risk factor. Read it as a dependency map: when a handful of buyers fund the whole build-out, their capex guidance is the supplier\\'s revenue forecast. The habit transfers directly to Indian filings, where the same dependency hides in segment notes: find the line that says how much of revenue the top customers carry, and you have found the company\\'s real sensitivity.'),
]})""",
"""G.append({'heading': 'One concept: recency bias', 'blocks': [
 p(' The recency bias, and the engine under it. In 1973, Amos Tversky and Daniel Kahneman described the availability heuristic: people judge how common something is by how easily an example comes to mind. In their best-known test, most people said more English words begin with the letter K than have K in third place - the truth is the reverse, roughly two to one, but K-first words are easier to summon (' + a(TAK, 'the 1973 paper') + '). Recency bias is the same engine with a clock: the freshest, most vivid evidence quietly becomes the base rate. This week wore the pattern. Six straight weekly losses in Nvidia made "the AI trade is over" feel like the base rate - then one strong print and a nearly-5% after-hours move flipped the story before breakfast, and Mumbai\\'s record close made the losses of 27 February feel ancient. Neither the despair nor the relief was a statistic; both were the freshest number doing the talking. The habit: when the latest number moves you most, ask what the last ten said. One print is a data point; a trend is a series.'),
]})""")

# --- drop the standalone Term group (merged into Goldmine) ---
rep(B, """G.append({'heading': 'Term of the day: book building', 'blocks': [
 p(' When CNBC reports that Anthropic\\'s "order books closed" at 4 PM, the term is book building: the process by which an issuer\\'s banks collect bids from institutions - how many shares, at what price - before setting the final offer price (' + a(CNBCANT, 'the report') + '). The book is the tally of those bids; closing it ends the auction; pricing is the judgment that follows. An oversubscribed book is why an offering can price above its range: more demand than shares at the top end lets the banks move the clearing price up. The same mechanism runs in Mumbai - Urban Company\\'s Rs 2,500-crore QIP, opened Tuesday with a Rs 161.03 floor, is a book-built offer to institutions under SEBI\\'s rules (' + a(ST, 'the QIP report') + '). Watch for it tonight in the Anthropic print: the price, the multiple of the range, and what the book said.'),
]})

""", "")

# --- Editor's read: append the three brewing files (merge Brewing in) ---
rep(B, """a pricing tonight is not a debut Thursday.'),
]})""",
"""a pricing tonight is not a debut Thursday.'),
 p(' Also brewing - the leadership file. Cause chain: Huang\\'s resignation, now officially characterized as following disclosure of conduct inconsistent with the code of conduct; his first statement Tuesday offering to return; Jones\\'s on-call answer that the board does not intend to reinstate him; Kress interim CEO and CFO, one strong print delivered. What settles it: the appointment of a permanent chief. Watch: any search announcement, and whether the board\\'s position holds under shareholder pressure.'),
 p(' Also brewing - the debut file. Cause chain: three amended filings; books closed Tuesday 4 PM New York; likely above-range pricing per CNBC\\'s sourcing; the $26 billion supplier placement closing after; first trade Thursday as ANT. What settles it: tonight\\'s price, then Thursday\\'s first print. Watch: New York tonight and the opening cross.'),
 p(' Also brewing - the compute-rule file. Cause chain: released Monday as RIN 0694-AK50; filed with the Federal Register the same day and on the public-inspection list since, with publication scheduled for Thursday 19 November (' + a(FRPI, 'the inspection entry') + '). What settles it: the published entry - effectiveness keys to the publication date, comments run sixty days from it, and the cloud-services window is ninety days from effectiveness. Watch: Thursday\\'s Register issue, then the comment file.'),
]})""")

# --- drop the standalone Brewing group ---
rep(B, """G.append({'heading': 'Brewing', 'blocks': [
 p(' The leadership file. Cause chain: Huang\\'s resignation, now officially characterized as following disclosure of conduct inconsistent with the code of conduct; his first statement Tuesday offering to return; Jones\\'s on-call answer that the board does not intend to reinstate him; Kress interim CEO and CFO, one strong print delivered. What settles it: the appointment of a permanent chief. Watch: any search announcement, and whether the board\\'s position holds under shareholder pressure.'),
 p(' The debut file. Cause chain: three amended filings; books closed Tuesday 4 PM New York; likely above-range pricing per CNBC\\'s sourcing; the $26 billion supplier placement closing after; first trade Thursday as ANT. What settles it: tonight\\'s price, then Thursday\\'s first print. Watch: New York tonight and the opening cross.'),
 p(' The compute-rule file. Cause chain: released Monday as RIN 0694-AK50; no Federal Register entry as of Wednesday morning; every clock in the rule still waiting on publication. What settles it: the Register entry - its date starts every clock. Watch: federalregister.gov, and the comment file once it opens.'),
]})

""", "")

# --- Notes bullet: FR status ---
rep(B, "a Federal Register API check this morning - no publication entry for RIN 0694-AK50",
 "the Federal Register\\'s public-inspection list, checked this morning - the rule was filed Monday and is scheduled to publish Thursday 19 November, so every clock still waits on publication")

# --- hero wiring ---
rep(B, " 'edition': {'fact': fact, 'intro': intro, 'groups': G},",
 " 'edition': {'fact': fact, 'intro': intro, 'groups': G, 'hero': {'img': 'photos/d44-hero.jpg', 'alt': 'Abstract plate: a printed sheet, a half-open door, a rising line', 'caption': 'Abstract plate for edition 44 - the print, the door, and the debut.'}},")

print('build_day44.py patches done')
