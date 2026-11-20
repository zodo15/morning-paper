#!/usr/bin/env python3
"""Write LR46 (Nasdaq) into editions-src/longreads.json."""
import json

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}
def fig(img, alt, caption): return {'t': 'figure', 'img': img, 'alt': alt, 'caption': caption}

NSDQ50 = 'https://www.nasdaq.com/articles/nasdaq%3A-50-years-of-market-innovation-2021-02-11'
SECHIST = 'https://sechistorical.org/exhibition/transformation-regulation-equities-market-structure-1934-to-2018-2/automating-the-exchanges-1976-1995/nasdaq/'
FINRA = 'https://www.finra.org/sites/default/files/Corporate/p009762.pdf'
CRS = 'https://www.congress.gov/crs_external_products/RS/PDF/RS21193/RS21193.6.pdf'
IRFAQ = 'https://ir.nasdaq.com/resources/investor-faqs'
IROMX = 'https://ir.nasdaq.com/news-releases/news-release-details/nasdaq-obtains-clearance-committee-foreign-investment-united'
BDOMX = 'https://www.borsedubai.ae/docs/English%20Offer%20Document.pdf'
TRADERS = 'https://www.tradersmagazine.com/news/nasdaq-a-timeline/'
CNBC_ANT = 'https://www.cnbc.com/2026/11/19/anthropic-ipo-ant-live-updates.html'

lr = {
 'title': 'The market that was never a place',
 'fact': "A Slow Burn long read, Friday 20 November 2026. On Thursday the biggest listing in history - $81.3 billion - opened for trading on a market with no floor, no specialists and no building that matters. Nasdaq was built in 1971 because the pink sheets were always stale. This is how a quotation machine became the venue the AI era chose.",
 'thumb': 'photos/lr46-hero.jpg',
 'hero': {'img': 'photos/lr46-hero.jpg', 'alt': 'Abstract plate: a wall of glowing quote screens where a trading floor should be', 'caption': 'Abstract plate for the long read - the market that was never a place.'},
 'groups': [
  {'heading': '1. The pink sheets', 'blocks': [
    p(" To understand why Nasdaq exists, picture how you bought an unlisted stock in 1965. Your broker did not walk to a floor - there was no floor for this stock. He worked the telephones, calling other dealers one by one, and his map of the market was the pink sheets: a printed list of wholesale quotes, compiled, published and circulated on paper, always stale by the time anyone read it. The SEC Historical Society counts about 5,000 firms in the National Association of Securities Dealers at the time, two-thirds of them working only this over-the-counter market, and describes it as a market that was virtual before the word existed - an invisible network of broker-dealers linked by telephone and a daily printout (%s). The investor paid for the staleness twice: once in the spread, and once in the time lost while a broker looked for a counterparty whose quote had already moved." % a(SECHIST,'the Society\'s exhibit')),
    p(" The fix came from the referee. In 1963 the SEC's Special Study of the Securities Markets said the OTC market needed automation and proposed exactly that: a computerized, real-time substitute for the pink sheets (%s; %s). The NASD's president, Robert Haack, ordered a centralized processing complex built in Trumbull, Connecticut, late that decade. The industry that would one day trade on the machine was in no hurry to build it: smaller brokers feared narrower spreads, and the New York Stock Exchange's members feared for the floor's business. So the design was compromised from birth - no retail interface, and no NYSE-listed stocks allowed. The upstart was permitted to exist on the condition that it stayed small." % (a(TRADERS,'the timeline'), a(SECHIST,'SEC Historical Society'))),
  ]},
  {'heading': '2. Trumbull', 'blocks': [
    p(" The NASD itself was a creature of crisis: organized under the 1938 Maloney Act amendments to the Securities Exchange Act, the industry's answer to the crash-era demand for a referee it would actually obey (%s). Three decades later that association contracted with the Bunker-Ramo Corporation of Trumbull to build the machine - a room of tape drives and monochrome cathode-ray screens where market makers in OTC stocks could update their bid and ask quotes electronically, all of them writing to the same system at once (%s). It was one of the first data centers built for trading, and it inverted the physics of the floor: on a floor, being present is the advantage; on a network, everyone sees the same quote at the same time." % (a(FINRA,'the NASD\'s own history'), a(NSDQ50,'Nasdaq\'s 50-year history'))),
    fig('photos/lr46-int1.jpg', 'Abstract plate: paper quote sheets dissolving into a grid of green terminal lights', 'The trade - paper sheets for a screen, stale prices for live ones.'),
    p(" Consider what that contract really was: a trade association of brokers hiring a defense-electronics firm to replace its own members' telephones. Every exchange before it had been a place you went to. This was a place you dialed into - and the people who paid for it were the people whose spreads it would compress."),
  ]},
  {'heading': '3. February 8, 1971', 'blocks': [
    p(" The National Association of Securities Dealers Automated Quotations - NASDAQ - went live on Monday, February 8, 1971, quoting some 3,000 securities through about 1,000 market makers, with the rest of the OTC market still on paper (%s). It launched with three tiers of service: Level 1 gave the representative quotes newspapers carried; Level 2 showed the wholesale quotes the pink sheets had carried; Level 3 let firms work orders. It did not yet execute anything - matching was still done by telephone - but the transparency alone did what theory said it would: spreads narrowed significantly. By 1980, still banned from NYSE stocks, the upstart was handling 63%% of the NYSE's volume (%s). And the companies that would define the century were choosing it: Apple in 1980, Microsoft in 1986, and with them a generation of technology issuers who, in NASDAQ president Joe Hardiman's later telling, felt comfortable with a screen-based market and knew it was the future rather than a floor (%s)." % (a(SECHIST,'the Society'), a(SECHIST,'the same record'), a(SECHIST,'his interview'))),
    p(" The slogan the market later adopted - the stock market for the next hundred years - was, in 1971, simply a description. Nothing about the system required a century to prove itself; it required only that the telephone keep losing to the screen."),
  ]},
  {'heading': '4. The crash that made it', 'blocks': [
    p(" Execution came late and then all at once. Electronic small-order execution - SOES, for orders under a thousand shares - arrived only in 1984, and was voluntary. Then came October 1987: from the 13th to the 19th the Dow fell 31%%, almost a trillion dollars of value gone, and on the worst of it the Nasdaq market makers simply stopped answering the phone. Quotes locked and crossed; the telephone layer of the market failed exactly when it was needed (%s). The SEC's verdict was that if computers had helped cause the break, more computerization was the way out: in 1988, an improved SOES was made mandatory for all market makers. The day traders who learned to pick off slow quotes on it - the SOES bandits - became the first high-frequency traders in spirit, and Nasdaq's 1990 answer, SelectNet, extended electronic negotiation to large orders. Each scandal of speed produced more speed." % a(SECHIST,'SEC Historical Society')),
    fig('photos/lr46-int2.jpg', 'Abstract plate: telephones hanging off hooks while a terminal glows', 'October 1987 - the day the phones failed and the screen became mandatory.'),
    p(" The pattern is the point of the chapter: Nasdaq's market share was never won in committee. It was won on the days the old system's human links broke - and every break ended with more of the market forced onto the machine."),
  ]},
  {'heading': '5. The exchange sells itself', 'blocks': [
    p(" For thirty years Nasdaq was a utility owned by its referees. In 2000, squeezed by electronic competitors, the NASD membership voted to spin it out as a for-profit, shareholder-owned company - a three-stage uncoupling that the Congressional Research Service documented in real time: private placements of its shares in 2000-01, an application for full exchange status filed in March 2001, and then a public listing (%s). The restricted shares first traded on the OTC Bulletin Board in 2002 - the old pink-sheet market's descendant trading its own stock - and on February 9, 2005, Nasdaq listed its shares on The Nasdaq Stock Market itself, in a $155 million secondary offering priced at $9 a share (%s). On January 13, 2006, the SEC approved it as a registered national securities exchange: the quotation utility was now, formally, an exchange and a listed company on its own board (%s)." % (a(CRS,'the CRS report'), a(IRFAQ,'Nasdaq\'s own FAQ'), a(CRS,'CRS'))),
    p(" There is a sentence worth pausing on in that history: the market built because paper prices were always stale ended up pricing itself, on itself, electronically. The machine had become the merchandise."),
  ]},
  {'heading': '6. The empire', 'blocks': [
    p(" The newly public company went shopping in the middle of a bidding war it nearly lost. In August 2007, Borse Dubai made an all-cash offer for OMX, the Nordic-Baltic exchange group, at SEK 230 a share; by September 20, Nasdaq and Borse Dubai had carved up a joint deal - Dubai would take the shares, Nasdaq would take OMX (%s). On the last day of 2007, Nasdaq formally withdrew its own stand-alone offer and proceeded to buy OMX from Borse Dubai, clearing the US foreign-investment review on the way (%s). The merged Nasdaq OMX put the market that began in a Connecticut data room inside a transatlantic group running exchanges from Stockholm to the Baltics - and selling the one thing its history had taught it to make: market technology, to other people's exchanges." % (a(BDOMX,'the Borse Dubai offer'), a(IROMX,'Nasdaq\'s release'))),
    fig('photos/lr46-int3.jpg', 'Abstract plate: two flags\' colors braided into a single ticker ribbon', 'The OMX deal - a bidding war settled by carving the prize in two.'),
  ]},
  {'heading': '7. The decision', 'blocks': [
    p(" On Thursday, shortly before noon in New York, the largest initial public offering ever priced - $81.3 billion, 980 million shares, Anthropic's ANT - opened for trading on this network. There was no floor to crowd onto and no specialist's post to stand at; there was a bell podium in a Times Square television studio, and behind it the descendant of the Trumbull data center matching 846 million shares in a session (%s). The company that could have listed anywhere chose the market with no address." % a(CNBC_ANT,'the debut')),
    p(" That is the decision this story was always heading to. The SEC asked for a machine to replace stale paper; the brokers who feared it funded it; the crash of 1987 made it mandatory; the dotcoms made it a brand; the 2005 listing made it a company; the OMX deal made it an empire. Each turn rewarded the same bet - that a market is information, not real estate. On Thursday the biggest listing in history paid that bet its largest compliment yet: it never considered needing a floor."),
  ]},
 ],
 'audio': {}, 
}

p_ = '/downloads/morning-paper/editions-src/longreads.json'
d = json.load(open(p_))
d['46'] = lr
json.dump(d, open(p_,'w'), indent=1, ensure_ascii=False)
import re
def strip(h): return re.sub(r'<[^>]+>',' ',h or '')
w = sum(len(strip(b.get('html','')).split()) for g in lr['groups'] for b in g['blocks'] if b.get('t')=='p')
print('LR46 written, chapters:', len(lr['groups']), 'words:', w)
