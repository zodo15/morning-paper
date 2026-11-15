#!/usr/bin/env python3
import json

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}
def rows(items): return {'t': 'rows', 'items': items}
def row(n, title, detail): return {'n': n, 'title': title, 'detail': detail}
def bullets(items): return {'t': 'bullets', 'items': items}
def closing(html): return {'t': 'closing', 'html': html}

def bars(label, rows_, scale=7.758064516129032, zero=410):
    n = len(rows_); h = 30 + 48*n
    out = ['<svg viewBox="0 0 760 %d" role="img" aria-label="%s">' % (h, label)]
    for i, (name, val, vlabel) in enumerate(rows_):
        ty = 47 + 48*i; ry = 30 + 48*i
        out.append('<text x="8" y="%d" font-size="21" fill="#334155">%s</text>' % (ty, name))
        w = abs(val)*scale
        if val >= 0:
            out.append('<rect x="%d" y="%d" width="%s" height="26" fill="#15803d" rx="3"/>' % (zero, ry, w))
            out.append('<text x="%s" y="%d" text-anchor="start" font-size="20" fill="#15803d">%s</text>' % (zero+w+8, ty+2, vlabel))
        else:
            out.append('<rect x="%s" y="%d" width="%s" height="26" fill="#b91c1c" rx="3"/>' % (zero-w, ry, vlabel and w or w))
            out.append('<text x="%s" y="%d" text-anchor="end" font-size="20" fill="#b91c1c">%s</text>' % (zero-w-8, ty+2, vlabel))
    out.append('</svg><p style="font-size:13px;color:#64748b;line-height:1.5">%s</p>' % label)
    return ''.join(out)

def card(num, name, rws):
    s = '<div style="border:1px solid #d9d1c4;border-radius:8px;padding:14px;margin:12px 0"><strong>%d. %s</strong>' % (num, name)
    for k, v in rws:
        s += '<p style="margin:10px 0;font-size:15px"><b>%s: </b>%s</p>' % (k, v)
    return s + '</div>'

def rangec(low, now, high, nowlabel, caption):
    lo, hi = 218.50, 238.75
    scale = (591.290322580645-204.51612903225836)/(238.75-218.50)
    x0 = 204.51612903225836 - 218.50*scale
    xl, xn, xh = x0+low*scale, x0+now*scale, x0+high*scale
    return ('<svg viewBox="0 0 760 125" role="img" aria-label="%s">'
            '<text x="8" y="44" font-size="23">ONGC</text>'
            '<line x1="%s" x2="%s" y1="38" y2="38" stroke="#15803d" stroke-width="10"/>'
            '<circle cx="%s" cy="38" r="10" fill="#172b3c"/>'
            '<text x="%s" y="82" font-size="19" text-anchor="middle">218.50</text>'
            '<text x="%s" y="16" font-size="19" text-anchor="middle">%s</text>'
            '<text x="%s" y="82" font-size="19" text-anchor="middle">238.75</text></svg>'
            '<p style="font-size:13px;color:#64748b">%s</p>') % (caption, xl, xh, xn, xl, xn, nowlabel, xh, caption)

DOT = 'https://www.transportation.gov/briefing-room/icymi-us-transportation-secretary-sean-p-duffy-provides-update-restoration-airspace'
USAT = 'https://www.usatoday.com/story/news/nation/2026/11/14/faa-ground-stop-probe-l3harris/92780406007/'
FOX = 'https://www.foxbusiness.com/fox-news-air-space/who-l3harris-federal-contractor-sec-duffy-says-may-have-caused-faa-outage'
SPACE = 'https://www.space.com/space-exploration/launches-spacecraft/spacex-chopsticks-catch-starship-upper-stage-flight-14'
NPR = 'https://www.npr.org/2026/11/14/g-s1-153786/spacex-successfully-catches-starship-and-makes-history'
SPN = 'https://spacenews.com/starship-launches-on-15th-test-calls-off-booster-catch/'
CNBCNV = 'https://www.cnbc.com/2026/11/13/nvidia-huang-ceo-replacement-search.html'
NVREL = 'https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition'
YAHOO = 'https://finance.yahoo.com/technology/article/anthropic-sets-ipo-date-for-thursday-nov-19-173011206.html'
S1A = 'https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm'
INV = 'https://www.investing.com/news/stock-market-news/anthropics-ipo-is-about-six-times-oversubscribed-bloomberg-news-reports-5023345'
CNBCTV18 = 'https://www.cnbctv18.com/market/sebi-approves-ipo-plans-of-razorpay-sembcorp-green-infra-and-makemytrip-india-20033679.htm'
HINDUMCL = 'https://www.thehindu.com/business/markets/mahanadi-coalfields-files-rhp-for-proposed-ipo-worth-nearly-9500-crore/article71702765.ece'
BSEAL = 'https://www.bseindia.com/xml-data/corpfiling/AttachLive/3e6ba97b-b37f-4229-bec5-d7f4a78355c0.pdf'
TOIPAYTM = 'https://timesofindia.indiatimes.com/business/india-business/paytm-gets-rbi-prelim-authorisation-to-operate-wallets-shares-surge-to-52-week-high/articleshow/135798025.cms'
MINTMDR = 'https://www.livemint.com/market/stock-market-news/upi-mdr-rollout-after-diwali-what-it-means-for-paytm-mobikwik-and-pine-labs-what-investors-should-know-11794477959612.html'
BSA2B = 'https://www.business-standard.com/companies/news/adyar-ananda-bhavan-sells-majority-stake-to-bodhi-tree-for-180-million-126111201795_1.html'
ENT = 'https://entrackr.com/report/funding-and-acquisitions-in-indian-startups-this-week-nov-09-nov-14-12808553'
GTEAM = 'https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature/'
FORTUNE = 'https://fortune.com/2026/11/13/openai-disbands-robotics-team-as-its-general-models-start-running-robots/'
SIERRA = 'https://sierra.ai/blog/releasing-poppy'
CURSOR = 'https://cursor.com/blog/security-incident-update'
SCH = 'https://schelling-atlas.com/'
SLOP = 'https://www.slopmanifesto.com/'
PT = 'https://portfolio-terminal.com/blog/stock-market-week-in-review-november-13-2026'
MCWEEK = 'https://www.moneycontrol.com/news/business/ipo/business-in-the-week-ahead-november-16-20-2026-14079544.html'
FEFII = 'https://www.financialexpress.com/market/fiis-pour-in-rs-5736-crore-but-nifty-slips-what-is-keeping-investors-cautious-4383868/'
XINHUA = 'https://english.news.cn/20261113/f3639000249a45b295f889e38266c7bd/c.html'
LRURL = 'https://files.instinct.com/5bywoe9rouad-the-network-america-flies-on'
LEDGER = 'https://files.instinct.com/gqn467t8lax3-the-exchange-under-the-banyan-tree'

movers = bars('Sensex leaders and laggards, Friday 13 Nov (% vs Thursday\'s close), BSE official prints - carried into Sunday', [
    ('HUL', 1.2, '+1.2%'), ('Bajaj Finance', 0.4, '+0.4%'), ('ONGC', 0.2, '+0.2%'), ('Eternal', 0.1, '+0.1%'),
    ('ICICI Bank', -0.3, '-0.3%'), ('SBI', -0.4, '-0.4%'), ('Maruti', -0.6, '-0.6%'), ('TCS', -0.8, '-0.8%'),
    ('Bajaj Finserv', -1.0, '-1.0%'), ('BEL', -1.6, '-1.6%')])

board_html = ('<p style="color:#64748b;font-size:13px">Open lines after Friday\'s session, carried into Sunday; prices are BSE official closes, Friday 13 November</p>'
 + card(1, 'Kotak Mahindra Bank', [('Status','Watchlist - trigger held'),('Entry / trigger','Post-print strength above Rs 437.55 - held above it for a fourteenth session, close Rs 487.60'),('Stop / invalidation','Below Rs 420 shelves it'),('Target / objective','Structured-setup candidate'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 487.60 (Fri close)')])
 + card(2, 'ONGC', [('Status','Watchlist - inside coil, breakout leg not re-established'),('Entry / trigger','Breakout above 228 with crude holding - close Rs 225.30, second session under 228 (the break was the Rs 8 ex-dividend); Brent settled at $95.84, so the crude leg stays firm'),('Stop / invalidation','Coil floor Rs 218.50'),('Target / objective','Coil top Rs 238.75'),('R:R at worst fill','1:1.1 - below the screen'),('Reference price','Rs 225.30 (Fri close)')])
 + card(3, 'Infosys', [('Status','Watchlist - below zone, flat'),('Entry / trigger','Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,140.00, flat below the zone'),('Stop / invalidation','A close under 1,120 ends the thesis'),('Target / objective','First checkpoint 1,245 (gap zone)'),('R:R at worst fill','n/a (qualitative)'),('Reference price','Rs 1,140.00 (Fri close)')])
 + card(4, 'JSW Steel', [('Status','Watchlist - R:R fails screen'),('Entry / trigger','Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,345.20'),('Stop / invalidation','Under 1,158.95 breaks the floor'),('Target / objective','5 November swing high near Rs 1,370'),('R:R at worst fill','1:1.2 - failed the screen'),('Reference price','Rs 1,345.20 (Fri close)')])
 + card(5, 'Hindalco', [('Status','Watchlist - candidate'),('Entry / trigger','No entry zone yet - levels to be verified against longer price history; closed Rs 944.40, the board\'s weakest name Friday'),('Stop / invalidation','n/a until an entry zone exists'),('Target / objective','Momentum plus record quarter as catalyst'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 944.40 (Fri close)')]))

ongc_range = rangec(218.50, 225.30, 238.75, '225.30', "ONGC: coil floor to coil top, marker at Friday's close")

G = []

G.append({'heading': 'The 5-minute lead route', 'blocks': [
 p(' Today\'s long read: The network America flies on - how a printing-press shop founded in 1895 became the contractor running the network beneath 45,000 daily US flights, and what one router did to it on Friday. ' + a(LRURL, 'Read it here') + '.'),
 p(' The cause: the Transportation Secretary names it - a contractor crew swapping copper for fiber at a remote FAA site installed a router that flooded the network with more than 1,000 connection attempts every four to five seconds; installer error or faulty unit, still undetermined.'),
 p(' The catch: hours later, SpaceX caught a Starship upper stage returning from orbit - the first ever - while its booster, short of fuel, ditched itself in the Gulf. Two engineering stories, one weekend, opposite directions.'),
 p(' The search: Nvidia\'s board is selecting a search firm for the top job and has formally engaged no candidate; Colette Kress presents her first quarter as interim chief on Tuesday.'),
 p(' The terms: Anthropic prices its IPO on Wednesday and begins trading Thursday as ANT - 825 million shares at $70 to $78, an order book reported six times covered.'),
 p(' The nods: SEBI clears the IPO plans of Razorpay, Sembcorp Green Infra and MakeMyTrip\'s India arm; Coal India\'s MCL files its Rs 9,500-crore RHP.'),
 p(' The ledger: Ashok Leyland\'s Saturday print - standalone profit up 12.7% to Rs 869.02 crore, a Re 1 dividend, and an auditors\' review-scope disclaimer to read carefully; Paytm gets RBI\'s in-principle nod to run wallets again.'),
 p(' The week: WPI on Monday, Fed minutes and Anthropic\'s pricing on Wednesday, ANT\'s debut on Thursday - and Mumbai\'s first session since the inflation print.'),
]})

G.append({'heading': 'Front page', 'blocks': [
 p(' The cause. America\'s worst aviation outage in years has a named suspect, and it is a box. Transportation Secretary Sean Duffy, in Saturday\'s statement: at least one remote FAA location, a contractor crew doing routine maintenance - switching telecommunication lines from old copper wire to fiber - and the router it installed began flooding the air-traffic network with more than 1,000 connection attempts every four to five seconds, degrading controller communications and radar feeds nationwide (' + a(DOT, 'the department\'s statement') + '). The contractor is L3Harris Technologies, the FAA\'s telecom provider for more than twenty years. What remains unknown is the only thing that matters legally: "was it user error or installer error from L3Harris, or did they install a faulty router? We haven\'t determined what the fault was" (' + a(FOX, 'Fox Business') + '). Friday\'s five-hour ground stop cancelled roughly 10,000 flights and delayed more than 7,000; some 3,500 airborne aircraft landed safely, and the system was back at full operations by Saturday morning (' + a(USAT, 'USA Today') + '). "We don\'t believe this was cyber," Duffy said - provisional, and his words. Officials told Reuters the suspect routers may have sat at sites in both Arkansas and Texas. <em>Editor\'s takeaway: the FAA outsourced its nervous system in 2002 and cannot fly without it; watch who pays for the answer - the installer, the router, or the contract.</em>'),
 p(' The catch. Hours after the ground stop lifted, SpaceX completed the harder half of the most ambitious Starship test yet: Ship 42, the upper stage, returned from orbit and was caught by the launch tower\'s chopstick arms at Starbase, Texas, at 4:20 PM Eastern Saturday - the first catch of a Starship returning from space, about 22.5 hours after Friday evening\'s liftoff (' + a(SPACE, 'Space.com\'s account') + '; ' + a(NPR, 'AP') + '). The other half failed cleanly: the Super Heavy booster\'s engines stopped firing too early on descent after a low-fuel alarm, its guidance sensed it was off profile, and it diverted itself to the Gulf of Mexico and self-destructed before splashdown - SpaceX\'s Kate Tice on the webcast (' + a(NPR, 'AP') + '; ' + a(SPN, 'SpaceNews') + '). In between, the ship deployed 26 Starlink V3 satellites and circled Earth fourteen times. "That was the holy grail of spaceflight," said SpaceX\'s Dan Huot. "We caught a Starship, and now everything changes." <em>Editor\'s takeaway: full reusability is now half-proven in one flight - and the half that failed has already been proven three times; the next flight is the one to watch.</em>'),
 p(' The search. Nvidia\'s board has begun the formal hunt: it is "in the process of selecting a search firm," has "not formally engaged any potential candidates," and calls speculation about individual names premature, the board said in a statement (' + a(CNBCNV, 'CNBC') + '). Interim chief executive Colette Kress chaired the first board meeting of the new structure on Thursday and presents third-quarter results on Tuesday - the first print since the resignation, for which Nvidia has given no reason (' + a(NVREL, 'the transition release') + '). In Washington, two House committees want Jensen Huang to testify, and the Senate Banking Committee wants Huang and Commerce Secretary Lutnick. <em>Editor\'s takeaway: the process answer replaces the name answer - the stock now trades the calendar: Tuesday\'s call, then a search firm, then a shortlist.</em>'),
 p(' The terms. Anthropic will price its initial public offering on Wednesday, 18 November, and begin trading on Thursday the 19th under the ticker ANT, the company announced (' + a(YAHOO, 'Yahoo Finance') + '). The amended filing sets 825 million Class A shares at an expected $70 to $78 - a $57.75 to $64.35 billion raise at the range - for a reported valuation of $1.3 to $1.45 trillion (' + a(S1A, 'the S-1/A') + '). Bloomberg reports the book is roughly six times covered (' + a(INV, 'Investing.com carries it') + '). It is the largest test the AI trade has faced, and the template OpenAI\'s expected 2027 debut will be measured against. <em>Editor\'s takeaway: a six-times-covered book means the pricing tells you little - the first hour of trading tells you everything about what public money will pay for frontier AI.</em>'),
 p(' The nods. SEBI cleared three IPO plans in one sweep, per the regulator\'s site: Razorpay - final observations issued 3 November, an estimated Rs 5,000-6,000 crore; Sembcorp Green Infra - a Rs 3,750-crore all-fresh issue, 3.6 GW operational and 4 GW under construction; and MakeMyTrip\'s Indian subsidiary - an offer-for-sale by the Nasdaq-listed parent and its Singapore unit, approved 6 November (' + a(CNBCTV18, 'CNBC-TV18') + '). And Coal India\'s Mahanadi Coalfields filed its RHP dated 13 November: an offer for sale of up to 66.18 crore shares, 10% of the parent\'s stake, estimated at Rs 9,500 crore (' + a(HINDUMCL, 'The Hindu') + '). <em>Editor\'s takeaway: the primary market\'s next quarter is fintech, green power, travel and coal - the pipeline is pricing risk appetites the indices do not show.</em>'),
 p(' The claims. Yemen\'s Houthi movement claimed a wave of strikes on Saudi Arabia - drones on an Aramco refinery in Riyadh and on Pumping Station 7 of the East-West pipeline, ballistic missiles toward Yanbu, Sharurah and the King Khalid air base; Saudi Arabia said it intercepted two ballistic missiles and four drones and has confirmed no damage, and none of the claims is independently verified (' + a(XINHUA, 'Xinhua') + '). Egypt and the Arab League condemned the attacks; fighting flared in Lahj, near the Bab al-Mandab. The market\'s verdict on the claims, for now: Brent settled the week down 2.5% at $95.84. <em>Editor\'s takeaway: unverified claims against oil infrastructure are now a weekly feature - the tape only moves when Saudi Arabia confirms damage, which it has not.</em>'),
]})

G.append({'heading': 'Markets', 'blocks': [
 p(' No session Saturday; Friday\'s finals are the tape. Mumbai: Sensex 81,592.45, down 318.56 points (0.39%); Nifty 25,144.30, down 155.05 (0.61%) - the three-day rally snapped in the first session priced with 6.09% inflation and a $95 barrel, with cement, realty and autos the worst sectors and every index red. The flows underneath still ran foreign: FIIs bought a provisional Rs 5,736.55 crore while domestic institutions sold Rs 2,253.58 crore (' + a(FEFII, 'NSDL and BSE figures via FE') + '). New York: the S&P 500 closed 7,561.67, down 0.40% Friday but up 2.51% on the week - its best since August; the Nasdaq 25,136.27 (+2.27% on the week), the Dow 52,347.55 (+2.07%); the ten-year Treasury yield ended at 5.154%, its highest close in a month; Brent settled $95.84 (-2.52% on the week), gold $3,879.70 (-4.6%), the dollar index 103.41 (' + a(PT, 'the week\'s closing tables') + '). The week\'s split personality in one pair: Nvidia fell 12.75% while the Philadelphia semiconductor index rose 8.05%.'),
]})

G.append({'heading': 'IPOs', 'blocks': [
 p(' Anthropic owns the week. The issuer\'s own numbers: 825 million Class A shares - 801.4 million primary, the rest selling stockholders - at an expected $70 to $78, an application to list on the Nasdaq as ANT, 123.75 million more on the underwriters\' option, and roughly $451.6 billion of compute commitments through 2030 in the risk factors (' + a(S1A, 'the S-1/A') + '). The company-announced dates: pricing Wednesday, first trade Thursday (' + a(YAHOO, 'Yahoo Finance') + '). At the range the raise is $57.75 to $64.35 billion; reports put the valuation at $1.3 to $1.45 trillion and the book six times covered - reported figures, attributed (' + a(INV, 'Bloomberg via Investing.com') + '). In Mumbai, the pipeline thickened: SEBI\'s nod to Razorpay (estimated Rs 5,000-6,000 crore), Sembcorp Green Infra (Rs 3,750 crore, all fresh issue) and MakeMyTrip India (OFS-only) (' + a(CNBCTV18, 'CNBC-TV18') + '), and Mahanadi Coalfields\' RHP for a roughly Rs 9,500-crore offer-for-sale, dated 13 November (' + a(HINDUMCL, 'The Hindu') + '). The contrast to hold: America\'s biggest-ever AI float prices the same week India\'s biggest coal arm goes to market - two very different bets on what the next decade runs on.'),
]})

G.append({'heading': 'Top movers - Friday\'s board stands', 'blocks': [
 p(' With no weekend session, Friday\'s verdicts remain the live board going into Monday (percentages computed from BSE\'s official closes against Thursday):',
 ),
 {'t': 'chart', 'svg': movers},
 p(' Closes, carried: Hindustan Unilever Rs 1,985.00, Bajaj Finance Rs 1,115.20, ONGC Rs 225.30, Eternal Rs 364.50; on the other side Bharat Electronics Rs 401, Bajaj Finserv Rs 1,860, TCS Rs 2,410, Maruti Suzuki Rs 12,878, State Bank of India Rs 1,080.50, ICICI Bank Rs 1,584. Saturday\'s results add fresh names to Monday\'s open: Ashok Leyland reported after Friday\'s close (numbers in Corporate actions), with Patanjali Foods, Brainbees, PTC Industries, Kaynes and Sammaan Capital also on the Saturday board.'),
]})

G.append({'heading': 'Corporate actions', 'blocks': [
 p(' Ashok Leyland\'s Saturday print, on the company\'s own filing: standalone net profit of Rs 869.02 crore against Rs 771.06 crore a year ago, up 12.7%, on revenue of Rs 13,364.28 crore, up 39.4%; the board declared an interim dividend of Re 1 per share (' + a(BSEAL, 'the BSE filing') + '). One line deserves care: the auditors\' consolidated review carries a disclaimer tied to a loan-balance and system review at subsidiary Hinduja Leyland Finance - a scope disclaimer with impact undetermined, not a fraud finding or a quantified loss, and this paper reports it as exactly that. Elsewhere on the weekend wire: Adyar Ananda Bhavan, the Chennai vegetarian chain, sold a majority stake to Bodhi Tree Systems - the Murdoch-Uday Shankar venture - for $180 million (' + a(BSA2B, 'Business Standard') + '); Unacademy moved founder Gaurav Munjal to executive chairman and named Akhilendra Kumar chief executive; and Paytm won RBI\'s in-principle authorisation to operate wallets again - the stock closed at a 52-week-high Rs 1,939.70, still 9.8% below its Rs 2,150 issue price (' + a(TOIPAYTM, 'Times of India') + '). The MDR piece of the Paytm story is expectation, not policy: a post-Diwali merchant-fee rollout is reported as coming, not notified (' + a(MINTMDR, 'Mint\'s explainer') + '). Carried dates: Oil India\'s dividend record date is Friday 20 November; Natco\'s was Thursday 19 November.'),
]})

G.append({'heading': 'Finance Goldmine', 'blocks': [
 p(' The week one stock masked four hundred. Read the closing table twice: the S&P 500 rose 2.51% - its best week since August - while its largest member fell 12.75%. Strip Nvidia out and the index would have risen about 3.7%; the equal-weight index, where Nvidia counts the same as the smallest member, rose 2.32%; 401 of the index\'s 502 stocks gained (' + a(PT, 'the weekly scorecard') + '). The money did not leave chips: AMD rose 18.93%, its best week since May, and Broadcom 18.16%, its best in a year - the pair\'s gain against Nvidia was the largest weekly swing between them since Broadcom listed. The pattern has a name worth keeping: cap-weighted indices let one company\'s grief impersonate a market verdict, and this week it nearly did. The personal-money translation: when a headline says "tech fell," ask which index, which weighting, and which five names - the average stock and the average index point often live in different countries. The same arithmetic runs in Mumbai, where a handful of banks and Reliance can move the Sensex while most members go the other way; the breadth line, not the index, is the honest tape.'),
]})

G.append({'heading': 'Startup Intelligence', 'blocks': [
 p(' A thin week, counted two ways. Indian startups disclosed about $31.3 million across 12 rounds in the week of 9-14 November, down 88% from the prior week\'s $258.1 million and far under the eight-week average of $194.3 million (' + a(ENT, 'entrackr\'s weekly table') + '); a rival tally counts $25.2 million across nine deals for 9-13 November - the trackers window and count differently, so the window and the source are stated. The real signals were in the smaller print: Greenjoules\' Rs 150-crore Series B for waste-to-biocrude fuel; Froncort.AI\'s $2.3 million from Google.org; Rigi\'s Rs 10 crore from Google; and the week\'s biggest deal being a consumer-brand buyout, not a venture round - Bodhi Tree\'s $180 million for control of A2B. Around the table: Norwest closed its eighteenth fund at $4 billion; Sarvam named a president; and MeitY questioned Pronto, Snabbit and Urban Company over gig-worker video data (' + a(ENT, 'the news-flash file') + ').'),
 p(' Today\'s startup idea: provenance-as-a-service for the tools developers trust. The Cursor incident\'s quiet lesson is that one leaked vendor key put a backdoored extension on a marketplace cache for eleven hours, and at most 5,000 developers installed it before anyone knew. Somebody has to watch the watchers: a service that continuously fingerprints what registries, marketplaces and CDNs actually serve - extension builds, package tarballs, container images - and compares it byte-for-byte against what the publisher signed, alerting within minutes when the served artifact diverges. The buyer is any enterprise with a developer fleet, and the wedge is narrow: start with the top hundred VS Code extensions, publish a free public dashboard, sell the private feed and the incident SLA. What would make it wrong: marketplaces adopting mandatory signed provenance faster than a startup can sell around it - in which case the honest pivot is compliance evidence, not detection.'),
]})

G.append({'heading': 'AI Race', 'blocks': [
 p(' Google\'s agent teams start collecting proofs - and OpenAI folds a team into the model. Google Research\'s weekend post is a results sheet for Antigravity\'s /teamwork multi-agent workflows paired with Gemini 4: information theory\'s Courtade-Kumar conjecture, open since 2013, proven in full generality and formalized in roughly 50 million lines of Lean 4; the Weil conjectures formalized end-to-end across 28,800 subagent invocations; a two-week campaign that rewrote the Zircon microkernel\'s remaining C++ into about 800,000 lines of Rust that pass the original test suite; and a libgav1 port that ended 20-30% faster than the hand-optimized original (' + a(GTEAM, 'Google Research\'s post') + '). The tools open to outside researchers and developers now, with ten thousand academic seats free for six months. OpenAI, meanwhile, disbanded its stand-alone robotics team, folding researchers into core research and applied hardware - the bet, the company told Fortune, is that general models like GPT-6 Astra run robots directly, no specialized brain required (' + a(FORTUNE, 'Fortune\'s exclusive') + '). And Sierra shipped v1.0 of Poppy, the protocol for personal agents to talk to businesses: Shopify now publishes a Poppy file for every merchant, Meta\'s Muse looks for it on every site, and the design-partner list passed a hundred (' + a(SIERRA, 'Sierra\'s release') + '). One more artifact of the week, carried with care: a "No AI Slop Manifesto" circulating since the AI Engineer Code Summit - five values, 22 resolutions, undated on its own page, which describes itself as written by the conference\'s speakers and attendees (' + a(SLOP, 'the site itself') + '); this paper notes it as a sentiment marker, not an event.'),
]})

G.append({'heading': 'Vibe coding', 'blocks': [
 p(' The breach every builder should read end-to-end. Cursor\'s own post-mortem is unusually complete: an attacker obtained an access key Cursor had issued to Fireworks - exposed by Fireworks - and used it to copy a read-only training-data bucket of coding-agent traces; a few traces held unredacted credentials; those opened Cursor\'s SaaS tools, archived source and support mail; and on 29 October the attacker placed a malicious copy of Anthropic\'s Claude Code extension on Cursor\'s marketplace cache, where at most 5,000 users pulled it over roughly eleven hours (' + a(CURSOR, 'Cursor\'s update') + '). Not an Anthropic vulnerability; not the production signing keys; last attacker activity blocked 1 November. The builder\'s checklist writes itself: vendor keys are your keys; training buckets are attack surface; anything your users install needs provenance you verify, not provenance you assume. Then, for the weekend\'s stranger read: researchers at ELLIS T\u00fcbingen turned pairs of AI agents loose on the web with one instruction - find each other - and 21 of 40 pairs did, all converging on the same meet-up spot, ntfy.sh, reached from memory rather than search (' + a(SCH, 'the Schelling Atlas') + '). When the researchers blocked it, the agents scattered to maps, shops and dead domains an attacker could register. The agents are developing habits; the habits are becoming infrastructure; and nobody is signing any of it.'),
]})

G.append({'heading': 'Try this today (Sunday)', 'blocks': [
 p(' Put your own words through Deep Review. The same engine behind Google\'s proof-checking week reviews drafts: in Antigravity, two Deep Review calls a week are free, and its authors report that on 578 opted-in conference submissions, over 30% of authors said it caught substantive proof bugs or significant typos (' + a(GTEAM, 'the Google Research post') + '). How to try it: open Antigravity, start Deep Review, and paste the document you most cannot afford to be wrong in - a proposal, a proof, a contract summary. The limits are honest: it is built for research-shaped documents, the free tier is two calls a week, and its findings are leads to verify, not verdicts to paste. The tools themselves predate this week - what is new is the external opening and the results behind it.'),
 p(' Then one read and one watch, both primary. The read: the Transportation Secretary\'s Saturday statement on the ground stop - two pages, every number in this paper\'s lead traceable to it (' + a(DOT, 'the statement') + '). The watch: Ship 42 threading itself into the chopsticks, on Space.com\'s capture of the 4:20 PM catch (' + a(SPACE, 'the video') + ') - then note the date, because the next attempt at catching both halves is the flight that changes the economics.'),
]})

G.append({'heading': 'One concept: the Schelling point', 'blocks': [
 p(' How do people coordinate when they cannot talk? In 1960 the economist Thomas Schelling answered: they meet at the option that stands out - the focal point each expects the other to expect. His classic setup: two people told to meet in New York City on a given day, no communication, no named place; most, he found, picked noon at Grand Central Station - not because it was best, but because it was salient, the answer that felt like the answer. The concept earned him a Nobel and a name: the Schelling point. This week gave the idea its strangest demonstration yet. Researchers turned pairs of AI agents loose on the open web with tokens to exchange and no agreed meeting place - and the agents converged, from memory, on one obscure pub-sub site, ntfy.sh: 42 of 130 opened with a request to it before searching anything, and every successful pair met there (' + a(SCH, 'the study') + '). Asked the puzzle directly, models named Wikipedia - a site none of their agents actually visited. What agents say and what agents do are different datasets, and the doing just inherited Schelling. The uses are practical: standards are Schelling points - the protocol that feels inevitable collects the votes, which is why Shopify and Meta moving on the same week matters more than either feature list; and in any negotiation, the option that feels like the default is a position somebody staked out early. <em>60-second recall, closed book: (1) What did Schelling\'s strangers pick, and why? (2) Where did the agents meet, reached how? (3) What did the models say when asked - and what is the lesson? Answers: noon at Grand Central, because salience beats optimality; ntfy.sh, from memory; Wikipedia - say and do are different datasets.</em>'),
]})

G.append({'heading': 'Term of the day: ground stop', 'blocks': [
 p(' A ground stop is the aviation system\'s hand brake: an order that holds aircraft at their departure airports - wheels down, wherever they are - while planes already flying continue to their destinations. It is the most severe tool in the FAA\'s traffic-management kit, above ground delays and miles-in-trail restrictions, and it is issued for runways, airports, regions or - rarely - the whole country. Friday\'s was the rare kind: departures halted nationwide for about five hours after a router flood degraded controller communications and radar feeds, only the second such nationwide stop since 9/11, per the Associated Press; roughly 10,000 flights cancelled, more than 7,000 delayed, and some 3,500 aircraft already aloft landed safely before the stop lifted at about 8:15 PM Eastern (' + a(DOT, 'the department\'s statement') + '; ' + a(USAT, 'USA Today') + '). The details that define the term: a ground stop does not ground the sky - it freezes the ground and lets the sky drain, which is why the safety numbers look the way they do. And the effects outlive the order: aircraft and crews land in the wrong cities, and the schedule takes days to unknot, which airlines warn is still working itself out this weekend.'),
]})

G.append({'heading': 'Setup board', 'blocks': [
 p(' Sunday\'s board is a carry-forward: no weekend session, so Friday\'s prices stay the live marks and Monday is the next scored session. The desk\'s rule stands: every published setup stays on the board until it completes (target hit) or fails (stop hit). Per-share prices on every line; the Rs 1,500 price cap screens what qualifies as a setup. Ledger: ' + a(LEDGER, 'Slow Burn swing research, 24 Oct') + '.'),
 {'t': 'chart', 'svg': board_html},
 {'t': 'chart', 'svg': ongc_range},
 p(' The resolved line stays in the ledger: HCLTech, filled 28 October at the worst fill of Rs 1,378.00, target Rs 1,466.80 taken out at 1,468.00 - gross +6.44%, net +6.14% after the 0.3% cost convention, in seven sessions; the stock closed Friday at Rs 1,376.60, which changes nothing for a line that already paid. Of the open lines: ONGC (Rs 225.30) spent a second session under the 228 breakout line - the break was the Rs 8 ex-dividend adjustment, and Friday\'s low of 224.90 held well above the 218.50 floor while crude settled the week at $95.84; Kotak (Rs 487.60) held its trigger for a fourteenth session; Infosys (Rs 1,140.00) is flat below the zone with the 1,120 floor untouched; JSW Steel (Rs 1,345.20) still fails the risk-reward screen; Hindalco (Rs 944.40) remains a candidate without a verified entry zone. No resolutions, no new setups - and Saturday\'s results give Monday fresh names before any of them can qualify: a setup needs verified levels, not a single strong print.'),
]})

G.append({'heading': 'How the board scores', 'blocks': [
 rows([
  row('1', 'No prior-day stop trade', 'A setup activates only if the zone fills before any prior-day trade at or below the stop.'),
  row('2', 'Same-day zone and stop', 'Unknowable from daily data: conservative scoring assumes the worst fill, then the stop.'),
  row('3', 'Resolutions stay on record', 'A setup leaves the board only when its target or stop resolves it; winners and losers both stay in the ledger.'),
 ]),
]})

G.append({'heading': 'The editor\'s read', 'blocks': [
 p(' One weekend, two machines. On Friday a router the size of a pizza box, swapped in during maintenance nobody schedules coverage for, stopped the largest aviation system on Earth for five hours - and a few hours after it restarted, a stainless-steel spacecraft fell out of orbit, through fire, into a pair of mechanical arms that caught it like a fly ball. The temptation is to grade the two organizations; the honest read is to grade the two problems. The FAA\'s is a legacy problem: a network built when Compaq made servers, maintained under contracts old enough to drink, with a 2027 deadline and a $50 billion ask - and its failure mode is invisible until national. SpaceX\'s is a frontier problem: never been done, on camera, and its failure mode - a booster ditching itself in the Gulf - was designed in advance and executed without a single person at risk. Legacy fails by surprise; frontier fails by rehearsal. The investor\'s version of the distinction is the week\'s real lesson: price the maintenance debt of the systems you depend on - the exchange, the bank, the grid - with the same attention you give the launches you watch. Monday tests both stories: L3Harris opens with the Secretary\'s sentence hanging over it, and SpaceX goes back to work on the half that missed.'),
]})

G.append({'heading': 'Brewing', 'blocks': [
 p(' The router file. Cause chain: twenty-four years of outsourced telecom; a 2002 contract nobody rebid; copper past its replacement date; a Saturday press conference naming L3Harris and a single router - installer error or faulty unit undetermined; a company statement pointing at its own 70% conversion record; and a Secretary who needs $50 billion saying "I\'m stuck with L3Harris" (' + a(DOT, 'DOT') + '; ' + a(FOX, 'Fox Business') + '). Watch next: the FAA\'s additional testing with the company, any determination on the router, LHX\'s Monday open (it fell 4% after hours), and whether the $50 billion ask names who operates what. Proven wrong if: the fault lands on a defective unit alone and the modernization role survives intact.'),
 p(' The succession file. Cause chain: Thursday\'s one-sentence exit, no reason given; Friday\'s FT report naming Arm\'s Rene Haas among approaches; the board\'s own answer - selecting a search firm, no candidate formally engaged, speculation premature; Kress chairing the new structure\'s first meeting; House committees requesting Huang, Senate Banking requesting Huang and Lutnick (' + a(CNBCNV, 'CNBC') + '; ' + a(NVREL, 'Nvidia\'s release') + '). Watch next: Tuesday\'s quarter - the first print of the interim era, with the written commentary at about 1:20 PM Pacific and the call at 2 PM - and any search-firm announcement. Proven wrong if: the board names a permanent chief inside weeks, making the search a formality.'),
 p(' The debut file. Cause chain: the largest AI company yet to test public markets - an S-1/A at 825 million shares, $70 to $78, a reported $1.3-1.45 trillion valuation, a reported six-times-covered book, roughly $451.6 billion of compute commitments disclosed; pricing Wednesday, first trade Thursday as ANT (' + a(S1A, 'the filing') + '; ' + a(YAHOO, 'the company\'s dates') + '). Watch next: whether pricing lands in, above or below the range; the first hour\'s tape; and what a strong or weak debut does to the reported 2027 OpenAI timeline. Proven wrong if: the deal is pulled or delayed - a six-times-covered book says that is not the base case.'),
]})

G.append({'heading': 'The week ahead', 'blocks': [
 rows([
  row('1', 'Sun 15 Nov (today)', 'No session in Mumbai. The FAA investigation and airline recovery continue; the week\'s positioning starts with Friday\'s marks.'),
  row('2', 'Mon 16 Nov', 'Mumbai reopens - the first session to judge Saturday\'s results, Ashok Leyland first; India\'s October WPI expected (moneycontrol\'s planner); L3Harris\'s first session since the naming.'),
  row('3', 'Tue 17 Nov', 'Nvidia\'s third quarter: written CFO commentary about 1:20 PM Pacific, call at 2 PM - Kress\'s first print as interim chief.'),
  row('4', 'Wed 18 Nov', 'Fed minutes. Anthropic prices its IPO after the US close - company-announced.'),
  row('5', 'Thu 19 Nov', 'Anthropic begins trading as ANT on the Nasdaq. Natco\'s dividend record date (carried).'),
  row('6', 'Watching', 'Oil India\'s dividend record date Friday 20 November; MCL RHP pricing steps; Razorpay, Sembcorp and MakeMyTrip India launch timing; any Saudi damage confirmation on the Houthi claims; the FAA\'s router determination; Cult.fit\'s Madras High Court date on 2 December.'),
 ]),
]})

G.append({'heading': 'Notes on this edition', 'blocks': [
 bullets([
  'Sources read for this edition: the Transportation Department\'s Saturday statement, USA Today and Fox Business for the ground stop and L3Harris; Space.com, AP via NPR and SpaceNews for the Starship flight, with event timing from Space.com\'s on-site account; Nvidia\'s own transition release and the board statement via CNBC; Anthropic\'s S-1/A on EDGAR and the company\'s announced dates via Yahoo Finance, with the oversubscription attributed to Bloomberg; Google Research, Fortune, Sierra and Cursor\'s own posts for the AI sections; the Schelling Atlas study site; BSE\'s official bhavcopy for Indian prices and the portfolio scorecard for the US week; the companies\' own BSE filing for Ashok Leyland; SEBI actions via CNBC-TV18; The Hindu for the MCL RHP; entrackr\'s weekly table for startup funding; Xinhua for the Gulf claims.',
  'Framing calls this edition: the router\'s fault is undetermined and is reported as undetermined - installer error or defective unit; the no-cyber assessment is the Secretary\'s provisional words, attributed; the Starship booster loss and the ship\'s catch are reported as separate outcomes, never as a double catch; Anthropic\'s valuation and book coverage are reported figures, attributed; Paytm\'s merchant-fee piece is labeled expectation, not policy; the manifesto is carried as a sentiment marker with its own page\'s claim, not as a dated event; the Saudi-Houthi exchange reports circulating in regional media failed wire verification and were dropped.',
  'Prices are BSE official closes or the named settlement prints; provisional flow figures are labeled provisional. Nothing on this page is investment advice. Verify anything load-bearing against the linked sources.',
 ]),
 closing(' The router failed in public; the catch worked in public; the week prices both. See you tomorrow.'),
]})

fact = ('Edition 41. The cause and the catch. Sunday 15 November 2026, edition 41. This edition runs 0,000 words. '
 'The cause of Friday\'s nationwide ground stop has a name: a router installed during L3Harris\'s copper-to-fiber maintenance flooded the FAA network - installer error or faulty unit undetermined. Hours later SpaceX caught a Starship upper stage returning from orbit, a first, while its booster ditched in the Gulf. '
 'Nvidia\'s board is selecting a search firm; Anthropic prices Wednesday and trades Thursday as ANT - 825 million shares at $70 to $78. SEBI cleared Razorpay, Sembcorp Green Infra and MakeMyTrip India; Coal India\'s MCL filed its RHP; Ashok Leyland grew profit 12.7%; Paytm can run wallets again. '
 'Mumbai\'s Friday marks stand: Sensex 81,592.45, Nifty 25,144.30. The long read: L3Harris - the network America flies on.')

intro = ('The 5-minute lead route is first; sections carry the detail. The long read: two brothers\' sheet feeder in 1895 Ohio, '
 'a radio maker bought for army maps, a 1997 roll-up named for its founders and a bank, a $1.7 billion contract to run America\'s air-traffic network - '
 'and the Saturday press conference that put the contractor on the evening news.')

d = {
 'day': 41,
 'meta': {'date': 'Sunday 15 November 2026', 'short': 'Sun 15 Nov', 'longread': 41},
 'edition': {'fact': fact, 'intro': intro, 'groups': G},
 'audio': {
   'quick': 'audio/d41-quick.m4a',
   'durations': {},
   'segments': [
     {'key': 'segment1', 'label': 'Opening and the five-minute lead route'},
     {'key': 'segment2', 'label': 'Front page: the cause, the catch, the search'},
     {'key': 'segment3', 'label': 'Front page: the terms, the nods, the claims'},
     {'key': 'segment4', 'label': 'Markets, IPOs and the movers'},
     {'key': 'segment5', 'label': 'Corporate actions and the Finance Goldmine'},
     {'key': 'segment6', 'label': 'Startup Intelligence and the AI Race'},
     {'key': 'segment7', 'label': 'Vibe coding and Try this today'},
     {'key': 'segment8', 'label': 'Concept, term and the setup board'},
     {'key': 'segment9', 'label': 'The editor\'s read, brewing and the week ahead'},
   ],
   'segment1': 'audio/d41-segment1.m4a', 'segment2': 'audio/d41-segment2.m4a', 'segment3': 'audio/d41-segment3.m4a',
   'segment4': 'audio/d41-segment4.m4a', 'segment5': 'audio/d41-segment5.m4a', 'segment6': 'audio/d41-segment6.m4a',
   'segment7': 'audio/d41-segment7.m4a', 'segment8': 'audio/d41-segment8.m4a', 'segment9': 'audio/d41-segment9.m4a',
   'full': 'audio/d41-full.m4a',
 },
}
json.dump(d, open('editions-src/day-41.json', 'w'), indent=1, ensure_ascii=False)
print('day-41.json written; groups:', len(G))
