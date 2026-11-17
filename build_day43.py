#!/usr/bin/env python3
import json, os

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}
def rows(items): return {'t': 'rows', 'items': items}
def row(n, title, detail): return {'n': n, 'title': title, 'detail': detail}
def bullets(items): return {'t': 'bullets', 'items': items}
def closing(html): return {'t': 'closing', 'html': html}

def bars(label, rows_, scale=30, zero=410):
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
            out.append('<rect x="%s" y="%d" width="%s" height="26" fill="#b91c1c" rx="3"/>' % (zero-w, ry, w))
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

NVIR = 'https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-CEO-Transition/'
FOOL = 'https://www.fool.com/coverage/stock-market-today/2026/11/16/stock-market-today-nov-16-nvidia-sinks-as-u-s-tightens-ai-chip-restrictions-and-analysts-slash-price-targets/'
CNBCUS = 'https://www.cnbc.com/2026/11/15/stock-market-today-live-updates.html'
CNBCTY = 'https://www.cnbc.com/2026/11/16/treasury-yields-bonds-inflation.html'
FEDW = 'https://www.federalreserve.gov/newsevents/speech/warsh20261116a.htm'
AXW = 'https://www.axios.com/2026/11/16/fed-warsh-ai-boom-stocks'
BISPR = 'https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology'
BISPDF = 'https://www.bis.gov/media/documents/rin-0694-ak50.pdf'
FRGOV = 'https://www.federalregister.gov/'
BT = 'https://www.businesstimes.com.sg/companies-markets/energy-commodities/oil-settles-lower-recovering-middle-east-exports-bolster-surplus-outlook'
HINDU = 'https://www.thehindu.com/business/Industry/stock-markets-end-higher-on-foreign-fund-inflows-lower-crude-oil-sensex-up-512-points/article71707675.ece'
FE = 'https://www.financialexpress.com/market/fiis-buy-rs-4865-crore-while-diis-sell-3-factors-supporting-market-sentiment-4386302/'
HBLTMPV = 'https://www.thehindubusinessline.com/markets/tata-motors-pv-falls-75-after-lowering-jlr-outlook/article71706761.ece'
HBLBUZZ = 'https://www.thehindubusinessline.com/markets/buzzing-stocks-on-november-16-pricol-ongc-bel-dr-reddys-va-tech-wabag-and-more/article71705452.ece'
PACE = 'https://bazaarwatch.com/announcement/317263/pace-digitek-limited-press-release'
TCOPENAI = 'https://techcrunch.com/2026/11/16/openai-will-embed-apollo-researchers-to-investigate-ai-subversion/'
MINTBS = 'https://www.livemint.com/companies/start-ups/bharat-semi-raises-24-million-seed-funding-info-edge-deeptech-startup-11794722449154.html'
INC42 = 'https://inc42.com/buzz/the-nvidia-fallout-weekly-funding-rundown-more/'
EMT = 'https://inc42.com/buzz/easemytrip-q2-loss-narrows-98-yoy-to-%E2%82%B957-lakh-revenue-up-34/'
CPRD1 = 'https://www.chatprd.ai/how-i-ai/token-fraud-is-eating-ai-margins-here-s-how-claire-vo-is-fighting-it'
CPRD2 = 'https://www.chatprd.ai/how-i-ai/claude-code-and-obsidian-scott-farrar-s-household-brain'
S1 = 'https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm'
GIFT = 'https://giftniftytoday.com/pre-market'
NKE = 'https://indexes.nikkei.co.jp/en/nkave/archives/summary?dt=11162026&idx=nk225'
LRURL = 'https://files.instinct.com/231ec4wm0ci6-the-purchase-manager'

movers = bars('Leaders and laggards, Monday 16 Nov (% vs Friday\'s close), BSE official prints', [
    ('Max Healthcare', 6.9, '+6.9%'), ('Tata Communications', 4.4, '+4.4%'), ('ITC', 3.8, '+3.8%'),
    ('Tata Consumer', 3.4, '+3.4%'), ('Apollo Hospitals', 2.8, '+2.8%'),
    ('Tata Steel', -2.8, '-2.8%'), ('Paytm', -2.9, '-2.9%'), ('Divi\'s Labs', -3.3, '-3.3%'),
    ('SAIL', -4.2, '-4.2%'), ('Tata Motors PV', -8.6, '-8.6%')])

board_html = ('<p style="color:#64748b;font-size:13px">Open lines after Monday\'s session; prices are BSE official closes, Monday 16 November - tonight\'s session is the next scored one</p>'
 + card(1, 'Kotak Mahindra Bank', [('Status','Watchlist - trigger held'),('Entry / trigger','Post-print strength above Rs 437.55 - held above it for a fifteenth session, close Rs 493.20 (+1.15%)'),('Stop / invalidation','Below Rs 420 shelves it'),('Target / objective','Structured-setup candidate'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 493.20 (Mon close)')])
 + card(2, 'ONGC', [('Status','Watchlist - inside coil, breakout leg not re-established'),('Entry / trigger','Breakout above 228 with crude holding - close Rs 226.70, third session under 228; Brent settled at $92.44, down 3.6%, so the crude leg cools'),('Stop / invalidation','Coil floor Rs 218.50'),('Target / objective','Coil top Rs 238.75'),('R:R at worst fill','1:1.1 - below the screen'),('Reference price','Rs 226.70 (Mon close)')])
 + card(3, 'Infosys', [('Status','Watchlist - below zone, flat'),('Entry / trigger','Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,143.70, still below the zone'),('Stop / invalidation','A close under 1,120 ends the thesis'),('Target / objective','First checkpoint 1,245 (gap zone)'),('R:R at worst fill','n/a (qualitative)'),('Reference price','Rs 1,143.70 (Mon close)')])
 + card(4, 'JSW Steel', [('Status','Watchlist - fails the screen at Monday\'s price'),('Entry / trigger','Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,333.00'),('Stop / invalidation','Under 1,158.95 breaks the floor'),('Target / objective','5 November swing high near Rs 1,370'),('R:R at worst fill','1:2.3 at the reclaim zone - 1,222.30 fill, 1,158.95 stop, 1,370 target; about 1:0.2 at Monday\'s close'),('Reference price','Rs 1,333.00 (Mon close)')])
 + card(5, 'Hindalco', [('Status','Watchlist - candidate'),('Entry / trigger','No entry zone yet - levels to be verified against longer price history; closed Rs 925.00, the board\'s weakest name again (-2.05%)'),('Stop / invalidation','n/a until an entry zone exists'),('Target / objective','Momentum plus record quarter as catalyst'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 925.00 (Mon close)')]))

ongc_range = rangec(218.50, 226.70, 238.75, '226.70', "ONGC: coil floor to coil top, marker at Monday's close")

G = []

G.append({'heading': 'The 5-minute lead route', 'blocks': [
 p(' Nvidia reports tonight into a market that has been selling it. Third-quarter numbers land at about 1:20 PM Pacific on Tuesday - roughly 2:50 AM IST on Wednesday - with the call at 2 PM, per the company\'s own schedule; it is the first print since Jensen Huang\'s resignation, and Colette Kress, interim CEO and CFO, takes her first call at the head of the room. Nvidia has given no reason for the resignation (' + a(NVIR, 'the company\'s transition announcement') + '). The setup is hostile: the stock fell another 4.12% Monday to $156.14 on volume roughly 119% above average, and Mizuho and UBS both cut price targets ahead of the print - to 220 from 250, and to 240 from 300, respectively (' + a(FOOL, 'the day\'s tape') + ').'),
 p(' Monday was Wall Street\'s third straight down session, and its broadest. The S&P 500 lost 1.92% to 7,416.59, the Nasdaq 2.49% to 24,509.76, and the Dow 739 points to 51,608.17; the VIX jumped 18.7% to 22.91. Consumer staples was the only green sector; Micron and Intel fell more than 7%, Sandisk about 8%, AMD, Dell and Oracle about 5% (' + a(CNBCUS, 'CNBC\'s live report') + '). The morning\'s only soft data point helped nothing: the NY Fed\'s Empire State index slid to 7.8 from 16.7 expected - still expansion, with employment at its strongest since June 2022. The ten-year yield eased to 5.131% (' + a(CNBCTY, 'CNBC\'s rates report') + '). Bitcoin\'s slide continued: $62,000 late Saturday, its lowest since August, and a sixth straight weekly decline.'),
 p(' The Bureau of Industry and Security released its AI remote-access rule Monday - released, not yet operative. The interim final rule (RIN 0694-AK50) restricts remote access to American advanced-computing capacity for AI training, but its own text leaves the effective date open: it takes effect on publication in the Federal Register, and as of this morning the Register carries no such publication. Comments run sixty days from publication; services already running get a ninety-day runway (' + a(BISPR, 'the BIS announcement') + '; ' + a(BISPDF, 'the rule text') + '). The shape, not a ban on renting: the remote-access limb bites above 12 million aggregate TPP of compute, where the customer or its ultimate parent is headquartered in Macau or a D:5 country, with a conditional exemption for commercial recommender systems filed through BIS, and ninety days from the effective date for services already running to obtain a license. The same document adds a license requirement for advanced semiconductors bound to Indonesia, Malaysia, Singapore, Thailand or Brazil - waived where the company or its ultimate parent is headquartered in the United States, with reporting duties - tightens the presumptions facing chip fabricators and packagers, and formally rescinds the 2025 AI Diffusion Rule.'),
 p(' The Fed\'s chairman framed the whole boom as a scenario problem. Kevin Warsh, opening the Fed\'s Productivity and Jobs Task Force conference Monday, called the technology "super intelligence" - SI - and laid out three paths, the last of which reads like Monday\'s tape: "Or SI could disappoint. After significant capital investment and stock market gains, expected returns could turn down and equity valuations could fall, leading to an economic slowdown and a more notable rise in unemployment." (' + a(FEDW, 'the Fed\'s published text') + '). He added that in time the economy would recover, but without the productivity gains. Read as the chairman\'s scenario, quoted from the owning source - not a forecast.'),
 p(' Mumbai went its own way on Monday. The Sensex rose 512.34 points to 82,104.79, up 0.63%, after touching 82,311.65 intraday, while Tokyo fell 2.42% (' + a(NKE, 'Tokyo\'s official close') + '); the Nifty closed at 25,291.10, up 0.58%. Financials, FMCG and oil-and-gas names led, helped by foreign buying and cheaper crude (' + a(HINDU, 'The Hindu\'s market report') + '). Provisionally, FIIs bought a net Rs 4,864.68 crore while DIIs sold Rs 3,519.05 crore - a second straight session of heavy foreign buying after Friday\'s roughly Rs 5,737 crore (' + a(FE, 'the provisional tally') + ').'),
 p(' The verdict on Tata Motors PV was the day\'s one heavy casualty: down 8.64% to Rs 262.20 in its first full session on JLR\'s lowered outlook. The cut: JLR now guides to a 2-3% core margin for FY27, from about 4%, and expects an outflow of roughly 1.25 billion pounds - about $1.65 billion - this fiscal, on weak China demand and restructuring costs; JLR is about 80% of the PV arm\'s top line (' + a(HBLTMPV, 'the Hindu BusinessLine report') + ').'),
 p(' Oil gave the day its macro relief. Brent settled at $92.44, down 3.6%, and WTI at $85.72, down 3.2%, as flows through the Strait of Hormuz show signs of recovering and the IEA\'s Friday surplus call sinks in; tanker incidents continue to underscore the risk (' + a(BT, 'the settlement report') + '). Gold eased 0.86% to $3,853.00; silver fell 4.60%, the largest metals move. On Wednesday, Anthropic is scheduled to price its 825-million-share offering at $70 to $78, debuting Thursday as ANT (' + a(S1, 'the S-1/A') + ').'),
 p(' The long read: the purchase manager. Radhakishan Damani apprenticed behind the counter of someone else\'s franchise for seven years, then built DMart on an eight-day payment rule, owned floors and ceiling-high racks - the Avenue Supermarts build story, as it changes CEOs without a ripple (' + a(LRURL, 'read it here') + '). The route ends. The detail begins.'),
]})

G.append({'heading': 'Front page', 'blocks': [
 p(' The print and the chair. Tonight\'s Nvidia numbers arrive with the leadership file exactly where the company left it: Kress interim CEO and CFO, Harvey C. Jones as the board\'s first chair, a search for a permanent chief under way, and no reason given for the resignation (' + a(NVIR, 'the announcement') + '). What changes tonight is the demand read: the first quarterly numbers since the transition, delivered by the executive now running both offices. The street\'s positioning into it is visible - two target cuts on Monday, volume at more than double the average, and a stock under pressure into the print (' + a(FOOL, 'the setup') + '). This paper reports the schedule and the state; the numbers speak tonight.'),
 p(' What the BIS rule actually does, in its own text. Three measures plus a rescission, read from the released document (' + a(BISPDF, 'the rule') + '). First, remote access: no providing covered computing power above 12 million aggregate TPP - at one data center or across linked ones - to companies headquartered, or whose ultimate parent is headquartered, in Macau or a Country Group D:5 jurisdiction; the rule\'s notes make clear the law treats awareness of a high probability as knowledge; commercial recommender systems are exempted, conditional on a filing through BIS\'s exclusion-note process; and services already running must obtain a license within ninety days of the effective date. Second, five named countries - Indonesia, Malaysia, Singapore, Thailand and Brazil - get a new license requirement for advanced semiconductors, waived where the company or its ultimate parent is headquartered in the United States, provided reporting requirements are met - India is not among the five. Third, the presumptions facing front-end chip fabricators and packagers exporting advanced-node logic chips are tightened, narrowing the pathways for chip designers in destinations already facing a license requirement. And the 2025 AI Diffusion Rule is formally rescinded. The effective date remains Federal Register publication, pending as of this morning.'),
 p(' Warsh\'s three scenarios, from the Fed\'s own text. The chairman\'s conference remarks put the productivity question in the language of contingency, not conviction: at one end, SI raises productivity and the gains are shared broadly; in the middle, an SI-driven expansion displaces jobs even as GDP rises; at the other end, SI disappoints after significant capital investment and stock market gains, and "expected returns could turn down and equity valuations could fall" (' + a(FEDW, 'the remarks as published') + '). Axios\'s headline compresses that into a bust warning (' + a(AXW, 'their read') + '); the text itself is a range of outcomes with the downside spelled out. The distinction is the paper\'s, and it matters: a central banker pricing scenarios is not a central banker calling a crash.'),
 p(' Inside Monday\'s slide, the details are unusually specific. The selloff concentrated where the AI build-out lives: memory (Micron, Sandisk), chips (Intel, AMD), servers (Dell), enterprise software (Oracle). The breadth tells the same story - staples green, technology and communication services down about 2.7% and 2.6% - and rates offered no relief narrative, with the two-year at 4.834% and the thirty-year at 5.476% (' + a(CNBCTY, 'the rates close') + '). Empire State\'s internals were mixed rather than weak: new orders slowed to 3.0, but employment rose to 18.1, its best since June 2022. None of this settles whether the week is a wobble or a turn; tonight\'s Nvidia print is the first hard input.'),
 p(' Mumbai\'s Monday, in full. The Sensex\'s 512-point gain came with a 82,311.65 intraday high and leadership from financials, FMCG and oil-and-gas; the Nifty\'s close at 25,291.10 sets up a flat open on this morning\'s GIFT screen (' + a(HINDU, 'The Hindu') + '; ' + a(GIFT, 'the pre-market screen') + '). The flow story stayed foreign-led: FIIs net buyers of Rs 4,864.68 crore provisionally, against DII selling of Rs 3,519.05 crore. Max Healthcare (+6.9%, closing at its day high), Tata Communications, ITC and Tata Consumer led the board\'s gainers; Tata Motors PV, SAIL and Divi\'s Labs anchored its losers (chart below).'),
 p(' Crude\'s slide is the one macro input every one of today\'s stories shares. Brent\'s 3.6% drop to $92.44 takes the edge off India\'s import bill, softens the inflation backdrop the Fed is reading, and eases the cost line of the energy-hungry AI build-out - all on the same day the IEA surplus call met recovering Hormuz flows (' + a(BT, 'Reuters via Business Times') + '). One day is not a trend; the settlement table is where the watch continues.'),
]})

G.append({'heading': 'Markets', 'blocks': [
 p(' Monday\'s marks, then this morning\'s markers. Mumbai: Sensex 82,104.79, up 512.34 (0.63%); Nifty 25,291.10, up 0.58%. New York: S&P 500 7,416.59, down 1.92%; Nasdaq 24,509.76, down 2.49%; Dow 51,608.17, down 1.41%; VIX 22.91, up 18.7%; the US ten-year at 5.131% (' + a(CNBCTY, 'CNBC') + '). Tokyo\'s Monday: Nikkei 59,662.02, down 2.42% (' + a(NKE, 'the official close') + '). This morning\'s markers, as of about 5:50 AM IST: GIFT Nifty at 25,336.00, up 0.13% on its own session - pointing to a flat start, an indication, not an open; Dow futures +0.03%, S&P 500 futures -0.01%, Nasdaq 100 futures -0.11%; Brent $91.75; gold $3,855.60; the dollar index 103.55; USD/INR 93.92 (' + a(GIFT, 'the pre-market screen') + '). The day\'s schedule: Nvidia\'s results tonight, Anthropic\'s pricing and the Fed\'s October minutes tomorrow.'),
]})

G.append({'heading': 'IPOs', 'blocks': [
 p(' The largest AI listing ever attempted prices tomorrow. Anthropic\'s 825 million Class A shares at $70 to $78 - a $57.75-to-$64.35-billion raise, up to $1.404 trillion implied - price Wednesday evening, with the first trade Thursday as ANT and the $26 billion concurrent placement from AMD, Broadcom, Google, Micron, Microsoft, Nvidia and TSMC closing immediately after (' + a(S1, 'the S-1/A') + '). The tape it prices into has changed since the range was set: the Nasdaq has fallen three straight sessions and Nvidia, a placement participant, is coming off a 4% day. Whether that moves the price is the bookrunners\' problem tonight and tomorrow; the terms as filed are the facts today. In Mumbai, no new issues priced Monday; last week\'s SEBI clearances continue their preparation phase.'),
]})

G.append({'heading': 'Top movers - Monday\'s verdicts', 'blocks': [
 p(' Monday\'s board - the large names this paper tracks, from best to worst (percentages computed from BSE\'s official closes against Friday):',
 ),
 {'t': 'chart', 'svg': movers},
 p(' The two ends are both stories. Max Healthcare closed at its day high of Rs 1,010.00, up 6.88%, the board\'s leader. Tata Motors PV closed at Rs 262.20, down 8.64%, in its first full session on JLR\'s margin cut - the detail in the lead route (' + a(HBLTMPV, 'the report') + '). Carried closes for the ledger: ONGC Rs 226.70, Tata Steel Rs 181.75, SAIL Rs 169.00, ITC Rs 294.80. Tonight the movers\' conversation moves to New York: Nvidia\'s print lands at about 2:50 AM IST, after this paper\'s Mumbai readers are asleep and before they wake.'),
]})

G.append({'heading': 'Corporate actions', 'blocks': [
 p(' Monday\'s tape carried a heavy filings board (' + a(HBLBUZZ, 'the BusinessLine roundup') + '). The largest: Pace Digitek disclosed a Rs 2,691-crore order from NTPC Green Energy for 600 MW / 1,800 MWh of battery energy storage at Khavda with fifteen years of operations and maintenance, taking its order book to Rs 13,427 crore (' + a(PACE, 'the company\'s press release') + '). Warburg Pincus signed a definitive agreement for the promoters\' entire 38.51% stake in Pricol\'s automotive-technology arm, post-demerger. ONGC disclosed - via quarterly filings - that its takeover of the Cambay CB-OS-02 block was effective 22 July 2026, with Vedanta carrying an impairment of roughly Rs 379 crore. VA Tech Wabag\'s 300-MLD Yanbu tender was cancelled on the customer\'s account; Dr Reddy\'s closed its FTO-3 inspection with a voluntary action indicated; Zydus\'s LiqMeds site drew four observations; Alembic won final approval for Binimetinib; Bharat Electronics booked Rs 619 crore of orders; GAIL and KRIBHCO signed a cooperation MoU. Carried dates: Natco Pharma\'s dividend record date is Thursday 19 November; Ashok Leyland\'s Re 1 interim and Oil India\'s dividend share the Friday 20 November record date.'),
]})

G.append({'heading': 'Finance Goldmine', 'blocks': [
 p(' Released is not effective: how a US rule actually switches on. Monday\'s BIS announcement is a perfect specimen, so read the mechanics once and keep them (' + a(BISPR, 'the release') + '; ' + a(BISPDF, 'the text') + '). An agency finalizes a rule and issues a press release - that is the announcement, the political fact. This rule\'s own effective-date line literally reads "INSERT DATE OF PUBLICATION IN THE FEDERAL REGISTER": for this rule, the operative fact is publication in the Federal Register, the government\'s daily journal - and the legal clock has not started. Three clocks then run from that publication date, not from the press release: the effective date itself, the comment window (sixty days here - an interim final rule takes comments even after it takes effect, and can be revised on them), and any compliance runway (ninety days here for existing services). The practical habit: when a rule matters, track the Register, not the headlines - the Register\'s own search (federalregister.gov) by the rule\'s RIN number turns the political fog into a dated entry. Until that entry exists, every sentence about this rule belongs in the future tense.'),
]})

G.append({'heading': 'Startup Intelligence', 'blocks': [
 p(' Monday\'s cheque, then last week\'s tape. Bharat Semi announced a $24-million seed round on Monday, led by Info Edge, South Park Commons and Indus Bridge Ventures - against an initial $10-to-15-million target - to build radar and sensing chips for surveillance, automotive and drone markets (' + a(MINTBS, 'Mint') + '). The prior week\'s tape was thin: Indian startups disclosed about $25.2 million across nine deals, down roughly 90% week on week, with cleantech the largest pocket at $16.2 million across three (' + a(INC42, 'Inc42\'s roundup') + '). In the listed lane, EaseMyTrip narrowed its consolidated net loss 98.4% to Rs 56.5 lakh, from Rs 36 crore a year ago, as operating revenue rose 33.5% to Rs 157.9 crore (' + a(EMT, 'Inc42\'s results report') + '). And Nexus Venture Partners\' partner Anup Gupta will step down in June 2027 after nearly 16 years - succession announced well ahead, the week\'s second unhurried handover.'),
 p(' Today\'s startup idea: abuse economics, sold as a service. The prompt is Claire Vo\'s account of fighting token fraud at ChatPRD - tens of thousands of dollars of inference losses, self-reported, and about $200,000 of failed attempted card purchases (' + a(CPRD1, 'her piece') + '). The limits belong in the pitch, so here they are: the efficacy claims are founder testimony; the classifier\'s thresholds, evaluation and false-positive rate are unpublished, with at least one false positive acknowledged; and broad geo-blocks also exclude legitimate users. The idea, within those limits: an independent abuse-audit layer for AI API sellers - session-level anomaly scoring, card-attempt telemetry and evidence bundles a finance team can act on - sold on recovered margin, not fear. The wedge is the mid-tier API sellers too small to build detection in-house. What would make it wrong: the model providers bundling abuse tooling into the platform - in which case the honest pivot is the audit trail, where independence is the product.'),
]})

G.append({'heading': 'AI Race', 'blocks': [
 p(' The week the AI trade met its referees. Three moves, one direction. Washington released the remote-access rule that writes a customer screen into the AI compute trade - knowledge-based, thresholded at 12 million aggregate TPP, aimed at Macau and D:5 nexuses, and not yet operative (' + a(BISPDF, 'the rule text') + '). OpenAI said it will embed outside safety groups - Apollo Research, Goodfire, METR and Transluce - to investigate AI subversion risks, an unusually external structure for evaluating its own frontier work (' + a(TCOPENAI, 'TechCrunch') + '). And tonight Nvidia publishes the first demand numbers of the post-Huang era into exactly this policy weather (' + a(NVIR, 'the company') + '). The common fact: the AI trade now waits on three gates at once - the technology\'s capabilities, the regulators\' screens and the market\'s patience. Wednesday\'s Anthropic pricing is the fourth data point in the same week.'),
]})

G.append({'heading': 'Vibe coding', 'blocks': [
 p(' If you sell AI, you sell compute - and compute invites abuse. The ChatPRD account is the cleanest practitioner\'s description of what that means in practice: fraudulent usage is not an edge case at the margins of an AI product; it is a cost-of-goods line that arrives with the first free tier (' + a(CPRD1, 'the piece') + '). The engineering lessons generalize, and they hold even with the piece\'s limits - self-reported figures, an unpublished classifier, acknowledged false positives. Instrument before you scale: if you cannot see usage at session granularity, you are flying the cost line blind. Price the abuse in: a free tier without an abuse budget is not generous, it is unpriced. And design the false-positive path first: the legitimate user you wrongly block writes the review that defines you, so the appeal flow deserves as much craft as the detector. The one-sentence version: treat inference like inventory - counted, costed and watched for shrinkage.'),
]})

G.append({'heading': 'Try this today (Tuesday)', 'blocks': [
 p(' Learn to read the Federal Register before you need to. Open ' + a(FRGOV, 'federalregister.gov') + ' and search the RIN 0694-AK50 - the Regulation Identifier Number of Monday\'s BIS rule. Free, on the web, no login. What you should see this morning is nothing: no publication entry, which is exactly the point - the rule is released but not yet operative. Bookmark the search and check it again next week; when the entry appears, its document page carries the effective date, the comment deadline and the full text, and the site offers email subscriptions so the entry comes to you instead. The limits: the Register publishes on its own schedule, which can lag a press release by days or weeks, and until the entry exists the authoritative text is the PDF on the agency\'s site (' + a(BISPDF, 'the BIS version') + '). The habit this builds - track the register, not the headline - pays off every time a rule moves markets.'),
 p(' Then, a household experiment from the same newsletter stable: the "household brain." Scott Farrar\'s ChatPRD interview describes running household operations through a shared Markdown file that Claude reads and updates - groceries, schedules, the household\'s standing state (' + a(CPRD2, 'the interview') + '). Keep the limits that came with the verification: it is a workflow demonstration, not a validated system, and the humans make the decisions. To try it, you need any Markdown editor - free, no login, on every platform. Create a household.md, give it three sections (this week, the pantry, the calendar), and maintain it by hand for a week before letting any tool touch it; the file\'s value is the discipline of a single source of truth, and that discipline is yours, not the model\'s.'),
]})

G.append({'heading': 'One concept: red flag', 'blocks': [
 p(' In export-control law, a red flag is a circumstance that should make a reasonable person suspect a violation - and the law\'s bite is that it treats awareness of a high probability as knowledge. The BIS rule released Monday states the standard in its own notes: a provider who sees the signs and proceeds anyway cannot claim ignorance (' + a(BISPDF, 'the rule\'s knowledge definition') + '). The concept is broader than compliance. Every profession has its red flags: the audit trail that stops one level early, the counterparty that will not name its parent, the usage pattern that no honest customer generates. The legal doctrine simply writes down what judgment already knows - that deliberate blindness is a choice, and choices have owners. Monday\'s rule makes the doctrine concrete: above 12 million aggregate TPP, with a Macau or D:5 parent in the picture, "we didn\'t ask" stops being a defense once the rule switches on. In your own work, the habit is cheaper than the lesson: when something flags, write down that it flagged, and what you did.'),
]})

G.append({'heading': 'Term of the day: interim final rule', 'blocks': [
 p(' An interim final rule is US administrative law\'s shortcut: a rule that takes effect without the usual propose-comment-finalize cycle, because the agency finds the delay impracticable or contrary to the public interest. Interim is the key word - the rule is final enough to bind, but the agency still takes comments after publication (sixty days, in Monday\'s case) and can revise on them (' + a(BISPDF, 'the rule text') + '). That makes it the opposite of settled law in one direction and stronger than a proposal in the other: it can move markets while remaining technically open to revision. When coverage calls such a rule "out" or "in force," check the stage: issued is the announcement, published in the Federal Register is the operative fact, and the comment window is the possibility of change. Monday\'s BIS rule has cleared the first stage only.'),
]})

G.append({'heading': 'Setup board', 'blocks': [
 p(' Monday\'s session is scored. The board\'s lines held their rules - no stop touched, no target taken - and every price below is a BSE official close from Monday\'s tape. The desk\'s rule stands: every published setup stays on the board until it resolves by its own rules.',
 ),
 {'t': 'chart', 'svg': board_html},
 {'t': 'chart', 'svg': ongc_range},
 p(' The resolved line stays in the ledger: HCLTech, filled 28 October at the worst fill of Rs 1,378.00, target Rs 1,466.80 taken out at 1,468.00 - gross +6.53%, net +6.23% after the 0.3% cost convention - closed Monday at Rs 1,382.40. Shelved: Voltas stays rejected, closing Monday at Rs 1,151.30; Tech Mahindra stays shelved above the Rs 1,500 cap, closing at Rs 1,783.50.'),
]})

G.append({'heading': 'How the board scores', 'blocks': [
 rows([
  row('1', 'No prior-day stop trade', 'A setup activates only if the zone fills before any prior-day trade at or below the stop.'),
  row('2', 'Worst fill in the zone', 'Entry is assumed at the worst price inside the published zone, not the best.'),
  row('3', 'R:R on the worst fill', 'Reward-to-risk is computed from the worst fill to the published stop and target; below the screen, no setup.'),
  row('4', 'Resolution only', 'A line leaves the board only by stop, target or invalidation - never by opinion.'),
 ]),
]})

G.append({'heading': 'The editor\'s read', 'blocks': [
 p(' One day, three kinds of authority. Washington released a rule whose legal clock has not started - and the discipline of saying so is the whole story: a press release moves prices Monday morning, the legal fact waits on a dated entry in a register most people have never opened, and the gap between the two is where bad reporting lives. The Fed\'s chairman chose the same honesty from the other side, laying out his downside scenario in his institution\'s own words - "expected returns could turn down and equity valuations could fall" - and letting the scenario stay a scenario. And tonight, Nvidia reports under interim leadership, the first print of the post-Huang era, into a market that spent Monday cutting exposure. The thread is that authority now flows to whoever states their stage cleanly: the agency that says released-not-operative, the chairman who says could, the company that says no reason given. The market, meanwhile, had its own quiet demonstration in Mumbai - foreign money buying a second straight day as Tokyo fell. Price the stated stage, not the headline\'s certainty.'),
]})

G.append({'heading': 'Brewing', 'blocks': [
 p(' The Nvidia file. Cause chain: Huang\'s resignation with no reason given; Kress interim CEO and CFO; Jones the first chair; two target cuts Monday; a 4.12% drop on double-average volume; Q3 numbers at about 1:20 PM Pacific tonight, call at 2 PM. What settles it: the print itself - the demand numbers, and whatever the company chooses to say about the search. Watch: tonight, and any search-firm announcement.'),
 p(' The compute-rule file. Cause chain: the remote-access rule released Monday as RIN 0694-AK50; effective date left as Federal Register publication; no Register entry as of this morning; sixty-day comments and a ninety-day runway to run from publication; the AI Diffusion Rule rescinded in the same document. What settles it: the Register entry - its date starts every clock. Watch: federalregister.gov, and the comment file once it opens.'),
 p(' The debut file. Cause chain: the S-1/A on 10 November; an 825-million-share offering at $70-78; a $26-billion supplier placement at the IPO price; pricing Wednesday; first trade Thursday as ANT - into a tape that has sold the Nasdaq for three straight sessions. What settles it: the price, then the first print. Watch: Wednesday evening, New York time.'),
]})

G.append({'heading': 'The week ahead', 'blocks': [
 rows([
  row('1', 'Tue 17 Nov (today)', 'Nvidia Q3 FY27 results about 1:20 PM Pacific (roughly 2:50 AM IST Wednesday); call at 2 PM Pacific - Colette Kress\'s first as interim CEO. First print since the CEO transition.'),
  row('2', 'Wed 18 Nov', 'Anthropic prices the 825-million-share offering ($70-78 range). FOMC October minutes.'),
  row('3', 'Thu 19 Nov', 'ANT debuts on the Nasdaq; the $26 billion supplier placement closes after the offering. Natco Pharma dividend record date.'),
  row('4', 'Fri 20 Nov', 'Record date for Ashok Leyland\'s Re 1 interim dividend and Oil India\'s dividend.'),
  row('5', 'Watching', 'Federal Register publication of RIN 0694-AK50 (starts the rule\'s clocks); post-print re-ratings on Tata Motors PV; the FAA-L3Harris lab finding on the El Dorado router (carried).'),
 ]),
]})

G.append({'heading': 'Notes on this edition', 'blocks': [
 bullets([
  'Sources read for this edition: Nvidia\'s own transition announcement and IR schedule; the BIS press release and the full rule text (RIN 0694-AK50), checked against a Federal Register search this morning - no publication entry found; the Fed\'s published text of Chairman Warsh\'s remarks, quoted from the owning source, with Axios\'s headline kept as an attributed compression; CNBC\'s live market report and rates report; the Motley Fool\'s session coverage for Nvidia volume and the Mizuho and UBS target cuts; The Hindu, the Financial Express and the Hindu BusinessLine for the Mumbai close, provisional flows and the JLR outlook; the BusinessLine buzzing-stocks roundup and Pace Digitek\'s own press release for the filings board; Reuters via Business Times and The Edge\'s settlement table for oil and metals; TechCrunch for the OpenAI embeds; Mint and Inc42 for the startup lane; both ChatPRD pieces, verified with their stated limits; BSE\'s official bhavcopy for Indian prices; the official Nikkei close; and the GIFT pre-market screen, labeled as-of.',
  'Framing calls this edition: the BIS rule is reported as released, not operative - the effective date is Federal Register publication, pending as of this morning, and the paper keeps that distinction in every mention; Warsh\'s remarks are quoted from the Fed\'s own text and reported as scenarios, not forecasts; Nvidia has given no reason for the resignation, and this paper repeats exactly that and no more; the Mizuho and UBS target cuts are reported actions, not endorsements; FII/DII figures are provisional, labeled; the ChatPRD material carries its verification limits - founder testimony, unpublished classifier, acknowledged false positives; Anthropic\'s terms are as filed, with pricing still ahead.',
  'Prices are BSE official closes or the named settlement prints; provisional flow figures are labeled provisional; the GIFT Nifty line is an as-of indication, not an open. Nothing here is investment advice.',
 ]),
 closing(' The rule waits on the Register; the chairman priced the downside in his own words; the print lands tonight. See you tomorrow.'),
]})

fact = ('Edition 43. The print, the rule, and the chairman\'s scenario. Tuesday 17 November 2026, edition 43. This edition runs 4,716 words. '
 'Nvidia reports tonight - its first results since Jensen Huang\'s resignation, with Colette Kress interim CEO and CFO; the stock fell 4.12% Monday as Mizuho and UBS cut targets. '
 'Washington released its AI remote-access rule: released, not yet operative, its effective date still awaiting Federal Register publication. Fed chairman Kevin Warsh laid out his disappointment scenario in the Fed\'s own words. Mumbai rose as Tokyo fell: Sensex 82,104.79, up 512 points on foreign buying and cheaper crude; Tata Motors PV fell 8.64% on JLR\'s margin cut. '
 'The long read: DMart - the purchase manager.')

intro = ('The 5-minute lead route is first; sections carry the detail. The long read: Radhakishan Damani apprenticed behind the counter of someone else\'s franchise for seven years, '
 'then built DMart on an eight-day payment rule, owned floors and ceiling-high racks - the Avenue Supermarts build story, as it changes CEOs without a ripple.')

d = {
 'day': 43,
 'meta': {'date': 'Tuesday 17 November 2026', 'short': 'Tue 17 Nov', 'longread': 43},
 'edition': {'fact': fact, 'intro': intro, 'groups': G},
 'audio': ({
   'quick': 'audio/d43-quick.m4a',
   'durations': {},
   'segments': [
     {'key': 'segment1', 'label': 'Opening and the five-minute lead route'},
     {'key': 'segment2', 'label': 'Front page: the print, the rule, the scenarios'},
     {'key': 'segment3', 'label': 'Front page: the slide, Mumbai, and crude'},
     {'key': 'segment4', 'label': 'Markets, IPOs, and the top movers'},
     {'key': 'segment5', 'label': 'Corporate actions, Finance Goldmine, and Startup Intelligence'},
     {'key': 'segment6', 'label': 'AI Race, vibe coding, try this, and the red flag'},
     {'key': 'segment7', 'label': 'Term of the day and the setup board'},
     {'key': 'segment8', 'label': 'Board scoring, the editor\'s read, and Brewing'},
     {'key': 'segment9', 'label': 'The week ahead and the notes on this edition'},
   ],
   'segment1': 'audio/d43-segment1.m4a', 'segment2': 'audio/d43-segment2.m4a', 'segment3': 'audio/d43-segment3.m4a',
   'segment4': 'audio/d43-segment4.m4a', 'segment5': 'audio/d43-segment5.m4a', 'segment6': 'audio/d43-segment6.m4a',
   'segment7': 'audio/d43-segment7.m4a', 'segment8': 'audio/d43-segment8.m4a', 'segment9': 'audio/d43-segment9.m4a',
   'full': 'audio/d43-full.m4a',
 } if os.path.exists('editions-src/ed43/audio_ready') else None),
}
json.dump(d, open('editions-src/day-43.json', 'w'), indent=1, ensure_ascii=False)
print('day-43.json written; groups:', len(G))
