#!/usr/bin/env python3
import json

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}

CNBC = 'https://www.cnbc.com/2025/03/30/coreweaves-7-year-journey-to-ipo-wound-through-crypto-before-ai.html'
RBV = 'https://www.reuters.com/breakingviews/coreweave-scripts-ais-tinker-bell-moment-2025-03-27/'
S1 = 'https://www.sec.gov/Archives/edgar/data/1769628/000119312525067651/d899798d424b4.htm'
CRWVREL = 'https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/default.aspx'
REUTFACT = 'https://www.investing.com/news/stock-market-news/factboxcoreweaves-ai-contracts-and-the-lenders-financing-its-buildout-4952427'
REUTCS = 'https://www.reuters.com/business/core-scientific-terminates-9-billion-merger-deal-with-coreweave-2025-10-30/'
FOOL = 'https://www.fool.com/coverage/stock-market-today/2026/11/11/stock-market-today-nov-11-coreweave-surges-25-on-beat-and-raise-quarter/'
REUTDAY = 'https://www.investing.com/news/economy-news/ai-cheer-banishes-rate-hike-fear-5019950'
YAHOO = 'https://finance.yahoo.com/news/down-50-highs-analyst-thinks-130612970.html'

lr = {
 'title': 'The cloud that began on a pool table',
 'fact': "A Slow Burn long read, Thursday 12 November 2026. On Wednesday, one company's results steadied the entire AI trade: CoreWeave beat its quarter, raised its year, and jumped 24.71% - and semiconductors, the Nasdaq and a record-setting Europe followed it up. The company behind that print began in 2017 with one graphics card on a pool table in a Wall Street office, bought by two carbon-market traders to mine ethereum. This is how Michael Intrator, Brian Venturo and Brannin McBee turned distressed crypto hardware into the cloud the gold rush rents its picks from - and what it costs to carry about $50 billion of debt while the market decides, quarter by quarter, whether the picks are worth their price.",
 'groups': []
}
G = lr['groups']

G.append({'heading': '1. The carbon desk', 'blocks': [
 p(' Michael Intrator did not come from technology. A political-science graduate from SUNY Binghamton with a public-administration masters from Columbia, he spent about sixteen years at Natsource, a buyer and trader of carbon credits, working the sales of emission credits tied to air pollution; Brian Venturo worked there as an energy trader (' + a(CNBC, 'CNBC\'s founding profile') + '). A portfolio manager who watched them, Alex Baldassano, gave CNBC the line that has followed them since: "They were the Michael Jordan and Scottie Pippen of the carbon markets at the time." Their firm was involved in the first over-the-counter trade in the Regional Greenhouse Gas Initiative, the American cap-and-trade program - pioneers of a market most of the world had not yet noticed.'),
 p(' The skill that market taught them was not code. It was this: find a commodity everyone will need, build the plumbing before the crowd arrives, and carry the balance sheet to hold the position. In 2013 the pair helped start a small natural-gas hedge fund, Hudson Ridge Asset Management. Four years later, with bitcoin and ethereum rising, they joined with a third partner, Brannin McBee, and founded Atlantic Crypto Corp. - to mine ethereum with Nvidia gaming GPUs, chosen because ethereum, unlike bitcoin, needed no specialised hardware, as Venturo explained on a podcast in 2020. They were not miners by conviction. They were commodity traders who had spotted a new commodity.'),
]})

G.append({'heading': '2. The pool table', 'blocks': [
 p(' The first rig was one GPU on a pool table in a Wall Street office. The pool table filled with cards; the overflow moved into Venturo\'s grandfather\'s garage in New Jersey, which became a data center. Then came the crypto winter of 2018 and 2019 - and the traders did what distressed-asset traders do: they bought what the ruined were selling. "One GPU turned into hundreds, then tens of thousands via strategic acquisitions of distressed hardware during the crypto-winter of 2018/2019, and our portfolio of facilities grew to seven," Intrator wrote in a 2021 blog post, quoted by ' + a(CNBC, 'CNBC') + '. While the market marked the cards down as gaming scrap, Atlantic Crypto was assembling, at bankruptcy prices, the largest amateur GPU fleet anyone had thought to build.'),
 p(' The mistake they did not make matters as much as the ones they did. They never fell in love with the coin. The GPUs were always the asset; ethereum was just the first tenant. When the mining economics thinned, the hardware was already pointed at its next use.'),
]})

G.append({'heading': '3. The rename', 'blocks': [
 p(' In 2019, Atlantic Crypto became CoreWeave, and the fleet took on work beyond mining: rendering video for visual-effects studios and training early AI models - any job that was parallel, hungry, and overpriced elsewhere. The pitch was blunt: CoreWeave claimed on its website that it charged 80% less than the traditional cloud providers, whose limited compute options came "at monopolistic prices," as Intrator put it. Andrew Bly, then CEO of the New York effects studio Molecule VFX, paid CoreWeave to run clusters after starting on Amazon\'s cloud; when his West Coast staff hit problems, CoreWeave stood up infrastructure in Nevada in under a month (' + a(CNBC, 'CNBC') + '). The ethereum rigs kept mining in the gaps - the goal, Venturo said, was 100% utilisation - but the company was now, in every way that counted, a cloud.'),
 p(' Then the discipline that built the company produced its luckiest trade. In September 2022, CoreWeave shut the mining unit down entirely. Two months later, OpenAI launched ChatGPT.'),
]})

G.append({'heading': '4. The earthquake', 'blocks': [
 p(' ChatGPT reached 100 million users in under three months, and the load landed on Microsoft, whose Azure cloud served OpenAI. Microsoft needed GPUs faster than it could build for them - and it began renting from CoreWeave, in a deal worth potentially billions of dollars (' + a(CNBC, 'CNBC') + '). "That\'s the moment where CoreWeave came into the collective consciousness," Michael Kellner, a communications executive who represented the company, told CNBC. Around the same time, Nvidia became both a customer and an investor - a symbiosis Intrator described plainly: "They depend upon us to be able to build and deliver the most performant configuration of their infrastructure in the world." The traders from the carbon desk now sat between the two most important companies in AI, supplying one and supplied by the other.'),
 p(' The contracts that followed made the model concrete: in March 2025, OpenAI signed a deal worth up to $11.9 billion and took $350 million of CoreWeave stock as part of it; in May 2025 it added as much as $4 billion more, payable through 2029 (' + a(REUTFACT, 'Reuters\' factbox of the contracts') + '). Revenue, $1.9 billion in 2024, had grown eightfold in a year (' + a(RBV, 'Reuters Breakingviews') + '). The catch was written in the same filings: Microsoft alone was 62% of 2024 revenue - one customer, one supplier, and a mountain of borrowed money between them.'),
]})

G.append({'heading': '5. The listing', 'blocks': [
 p(' In late March 2025, CoreWeave went public - and the market immediately showed the price of its structure. The offering was cut from a hoped-for $47 to $55 a share down to $40; Nvidia stepped in as an anchor buyer at $40; the valuation target was cut by about 22% to roughly $23 billion (' + a(RBV, 'Reuters Breakingviews') + '; ' + a(S1, 'the final prospectus') + '). Even trimmed, it raised $1.5 billion - the largest American venture-backed tech IPO since 2021 - listing on Nasdaq on 28 March 2025 under the ticker CRWV. The three founders were worth a combined $5.3 billion on paper, over 250,000 Nvidia GPUs humming in 32 data centers (' + a(CNBC, 'CNBC') + ').'),
 p(' Then the crowd forgot the caution it had just shown. Three months later, on 20 June 2025, the stock touched $187 - four and a half times the IPO price (' + a(YAHOO, 'Yahoo Finance\'s retrospective') + '). The whole AI-infrastructure complex was priced for perfection, and CoreWeave was its purest expression: the faster it borrowed, the faster it built, the more the market paid. The unwind came just as fast: by October 2025, the stock had roughly halved, and the company\'s $9 billion all-stock bid for the miner Core Scientific - its route to owned power and data centers - was rejected by Core Scientific\'s own shareholders and terminated on 30 October 2025 (' + a(REUTCS, 'Reuters') + ').'),
]})

G.append({'heading': '6. The leverage', 'blocks': [
 p(' Debt is the fuel for this company, Intrator has said - and by October 2026 the tank held about $50 billion (' + a(REUTFACT, 'Reuters\' factbox') + '). The bond market\'s anxiety had a number: insuring CoreWeave\'s debt against default cost around 1,000 basis points in October, implying - on LSEG\'s data - a market-read five-year default probability near 63%, up from about 30% a year earlier. The whole model is a carry trade on the future of AI compute: borrow against signed contracts, buy GPUs before the money arrives, and trust that the tenants - Microsoft, OpenAI, the frontier labs - keep paying through the decade. The third-quarter filing showed what that machine costs to run even when it works: a net loss of $709 million in a quarter with $3,661 million of revenue, and $846 million of net interest expense in the same three months (' + a(CRWVREL, 'the company\'s own release') + ').'),
 p(' None of this is hidden. It is the bet, stated in the prospectus and renewed every quarter. What Tuesday\'s results changed was the evidence: revenue more than two and a half times the year-ago quarter, an adjusted operating margin of 16% that CEO Intrator called "a quarter ahead of plan," and a contracted revenue backlog of approximately $132.5 billion - the largest single argument that the tenants are real, signed, and waiting.'),
]})

G.append({'heading': '7. The answer, and the question', 'blocks': [
 p(' The market\'s verdict on that evidence was the loudest single-stock statement of the season: up 24.71% on Wednesday, to $60.77 (' + a(FOOL, 'Motley Fool\'s close report') + ') - and the relief spread far beyond one ticker. Semiconductors rose 5.6% as a group, Sandisk 14%, Micron and Dell 12%, the Nasdaq 1.6%, and Europe\'s STOXX 600 closed at a record; Seoul\'s opening dispatch said the print "eased investor concerns over the profitability of massive AI investment" (' + a(REUTDAY, 'Reuters\' Trading Day') + '). The company that began on a pool table had become the AI trade\'s referee: when it answers well, the game continues.'),
 p(' The question it leaves is the one the whole build-out now turns on. A $132.5 billion backlog against about $50 billion of debt is a machine that must keep being right - every quarter, with rates high and the contracts concentrated in a handful of tenants who are also its rivals\' best customers. Intrator and Venturo have survived the carbon markets, a gas fund, a crypto winter, a rejected takeover and a halved stock. Their own history says the edge was never the GPUs. It was knowing that the asset outlives the tenant - and being willing to carry the balance sheet until the next one arrives. Whether that is a moat or a mortgage is now the market\'s daily referendum; Wednesday was one vote, and it was decisive. The recount is every earnings date, starting with the one circled in red across the street at Nvidia, five days from now.'),
]})

p_ = '/downloads/morning-paper/editions-src/longreads.json'
d = json.load(open(p_))
d['38'] = lr
json.dump(d, open(p_, 'w'), indent=1)
print('longreads 38 written; total keys:', len(d))
