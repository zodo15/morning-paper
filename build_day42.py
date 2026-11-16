#!/usr/bin/env python3
import json, os

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

FAAQA = 'https://www.faa.gov/newsroom/nationwide-ground-stop-questions-and-answers'
ABCL = 'https://abcnews.com/US/live-updates/faa-ground-stop-live-updates-hundreds-flights-canceled/?entryId=138160582&id=138125140'
REU = 'https://www.reuters.com/3fec1b0a85a0/business/aerospace-defense/thousands-us-flights-canceled-delayed-air-travel-system-recovers-shutdown-2026-11-14/'
DOT = 'https://www.transportation.gov/briefing-room/icymi-us-transportation-secretary-sean-p-duffy-provides-update-restoration-airspace'
S1 = 'https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm'
ROAD = 'https://www.anthropic.com/news/roadshow-launch'
TC = 'https://techcrunch.com/2026/11/10/anthropic-sets-ipo-price-range-of-70-to-78-per-share-to-reach-an-implied-valuation-of-1-404-trillion/'
CNBC = 'https://www.cnbc.com/2026/11/15/anthropic-ipo-is-make-or-break-for-the-technology-industry.html'
STKA = 'https://stockanalysis.com/news/anthropic-founders-stakes-18-billion-ipo/'
NVN = 'https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/default.aspx'
CNBCNV = 'https://www.cnbc.com/2026/11/13/nvidia-huang-ceo-replacement-search.html'
BSV = 'https://www.business-standard.com/companies/people/sunil-d-souza-s-elevation-as-voltas-chairman-comes-under-the-lens-126111301680_1.html'
PMT = 'https://www.peoplematters.in/news/leadership/noel-tata-steps-down-as-tata-international-chairman-t-v-narendran-takes-over-53327'
MINT = 'https://www.livemint.com/news/wholesale-inflation-india-october-wpi-data-crude-oil-prices-11794572080138.html'
SPAB = 'https://www.space.com/space-exploration/launches-spacecraft/spacex-says-starship-flight-15-booster-aborted-chopsticks-landing-catch-after-launch-due-to-guidance-issue-video'
SPN = 'https://spacenews.com/starship-launches-on-15th-test-calls-off-booster-catch/'
ETFC = 'https://economictimes.indiatimes.com/tech/funding/firstcry-q2-revenue-rises-14-to-rs-2396-crore-net-loss-narrows-75/articleshow/135833246.cms'
FCIR = 'https://cdn.fcglcdn.com/brainbees/firstcry-ir/Investor_Presentation_Q2FY27.pdf'
DEFASG = 'https://asean.org/wp-content/uploads/2026/11/SG-Dr-Kao-Remarks-for-ASEAN-Business-and-Investment-Summit-ABIS-2026-14-November-2026_As-Delivered.pdf'
PNA = 'https://www.pna.gov.ph/article/asean-ministers-ink-framework-deal-to-support-regions-digital-economy'
ST = 'https://www.straitstimes.com/asia/se-asia/asean-states-sign-digital-economy-framework-agreement-which-kicks-in-from-early-2027'
NASS = 'https://nasstatus.faa.gov/'
GIFT = 'https://giftniftytoday.com/pre-market'
PT = 'https://portfolio-terminal.com/blog/stock-market-week-in-review-november-13-2026'
TBT = 'https://tbtflow.com/daily/fii-dii/2026-11-13'
CNBCTV18 = 'https://www.cnbctv18.com/market/sebi-approves-ipo-plans-of-razorpay-sembcorp-green-infra-and-makemytrip-india-20033679.htm'
LRURL = 'https://files.instinct.com/l7mf9f8tds5m-the-lab-that-left-to-be'

movers = bars('Sensex leaders and laggards, Friday 13 Nov (% vs Thursday\'s close), BSE official prints - carried into Monday', [
    ('HUL', 1.2, '+1.2%'), ('Bajaj Finance', 0.4, '+0.4%'), ('ONGC', 0.2, '+0.2%'), ('Eternal', 0.1, '+0.1%'),
    ('ICICI Bank', -0.3, '-0.3%'), ('SBI', -0.4, '-0.4%'), ('Maruti', -0.6, '-0.6%'), ('TCS', -0.8, '-0.8%'),
    ('Bajaj Finserv', -1.0, '-1.0%'), ('BEL', -1.6, '-1.6%')])

board_html = ('<p style="color:#64748b;font-size:13px">Open lines after Friday\'s session, carried into Monday; prices are BSE official closes, Friday 13 November - tonight\'s session is the next scored one</p>'
 + card(1, 'Kotak Mahindra Bank', [('Status','Watchlist - trigger held'),('Entry / trigger','Post-print strength above Rs 437.55 - held above it for a fourteenth session, close Rs 487.60'),('Stop / invalidation','Below Rs 420 shelves it'),('Target / objective','Structured-setup candidate'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 487.60 (Fri close)')])
 + card(2, 'ONGC', [('Status','Watchlist - inside coil, breakout leg not re-established'),('Entry / trigger','Breakout above 228 with crude holding - close Rs 225.30, second session under 228 (the break was the Rs 8 ex-dividend); Brent settled at $95.84, so the crude leg stays firm'),('Stop / invalidation','Coil floor Rs 218.50'),('Target / objective','Coil top Rs 238.75'),('R:R at worst fill','1:1.1 - below the screen'),('Reference price','Rs 225.30 (Fri close)')])
 + card(3, 'Infosys', [('Status','Watchlist - below zone, flat'),('Entry / trigger','Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,140.00, flat below the zone'),('Stop / invalidation','A close under 1,120 ends the thesis'),('Target / objective','First checkpoint 1,245 (gap zone)'),('R:R at worst fill','n/a (qualitative)'),('Reference price','Rs 1,140.00 (Fri close)')])
 + card(4, 'JSW Steel', [('Status','Watchlist - fails the screen at Friday\'s price'),('Entry / trigger','Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,345.20'),('Stop / invalidation','Under 1,158.95 breaks the floor'),('Target / objective','5 November swing high near Rs 1,370'),('R:R at worst fill','1:2.3 at the reclaim zone - 1,222.30 fill, 1,158.95 stop, 1,370 target; about 1:0.1 at Friday\'s close'),('Reference price','Rs 1,345.20 (Fri close)')])
 + card(5, 'Hindalco', [('Status','Watchlist - candidate'),('Entry / trigger','No entry zone yet - levels to be verified against longer price history; closed Rs 944.40, the board\'s weakest name Friday'),('Stop / invalidation','n/a until an entry zone exists'),('Target / objective','Momentum plus record quarter as catalyst'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 944.40 (Fri close)')]))

ongc_range = rangec(218.50, 225.30, 238.75, '225.30', "ONGC: coil floor to coil top, marker at Friday's close")

G = []

G.append({'heading': 'The 5-minute lead route', 'blocks': [
 p(' The FAA has told its own story. In a Sunday question-and-answer page, the agency laid out Friday\'s nationwide ground stop in its own words: a technical problem at about 3:30 PM Eastern, data flooding the FAA\'s telecommunications network at roughly 1,000 connection attempts every four to five seconds, controller communications and radar feeds degraded, departures held across the country until 8:15 PM. Two locations were identified as potential sources - a radar site in Amarillo, Texas and a radio-communications site in El Dorado, Arkansas, where L3Harris, the network\'s service provider, had been working, including deploying a new router. L3Harris blocked both locations and the network stabilized; the broadcasting function has been disabled on all new routers as a precaution; the instability reached 17 of the 22 en-route centers before it was contained, and roughly 3,500 airborne aircraft landed safely (' + a(FAAQA, 'the FAA\'s own account') + ').'),
 p(' The cause stays open. Administrator Bryan Bedford called the stop "the result of faulty equipment" on Saturday and saw "zero evidence of anything nefarious, and zero evidence of anything AI-related"; the FAA\'s Sunday page says the root cause remains under investigation with L3Harris; the Arkansas router sits in the company\'s Florida lab - the Secretary\'s detail, not the agency\'s page. Those are different levels of confidence, and this paper keeps them distinct (' + a(ABCL, 'ABC News\' live coverage') + '). What is settled: the agency says it has no indication of a cyberattack or an outside actor; the failure sat in the legacy TDM system, not the fiber modernization; and the SMART data aggregator was unrelated. The recovery, as of late Sunday: more than 17,500 flights cancelled since Friday, only about 30 Monday cancellations on the board, and Secretary Duffy forecasting - his word, a forecast - "fully normal" operations Monday (' + a(ABCL, 'the live tally') + '). L3Harris shares closed Friday at $272.35 and slipped about 4% after hours; today\'s open is the tape\'s first verdict.'),
 p(' Anthropic is set to price Wednesday. The largest public offering an AI lab has attempted: 825 million Class A shares - 801,351,354 from the company, 23,648,646 from selling stockholders - at $70 to $78, with a 123.75-million-share greenshoe, listing Thursday on the Nasdaq as ANT (' + a(S1, 'the S-1/A') + '; ' + a(ROAD, 'the company\'s roadshow post') + '). At the range the raise is $57.75 to $64.35 billion, the implied valuation up to $1.404 trillion (' + a(TC, 'TechCrunch') + '); the book is reported about six times covered - a report, not a company figure. Alongside the float, AMD, Broadcom, Google, Micron, Microsoft, Nvidia and TSMC have agreed to buy $26 billion of non-voting Class N stock in a concurrent private placement at the IPO price (' + a(S1, 'the placement terms') + ').'),
 p(' Nvidia reports tomorrow - its first results since Jensen Huang\'s exit. Third-quarter numbers land Tuesday at 2 PM Pacific, with the CFO\'s commentary in writing ahead of the call, per the company\'s own announcement (' + a(NVN, 'the investor notice') + '). The CEO file is exactly where the board left it Friday: in the process of selecting a search firm, no candidate formally engaged. A Friday report that Arm\'s Rene Haas was approached, and weekend reports that some employees want Huang back, are reports - Nvidia has given no reason for the resignation (' + a(CNBCNV, 'CNBC') + '). The stock needs no reminder: down 12.75% last week to $162.85, its worst week since April (' + a(PT, 'the weekly scorecard') + ').'),
 p(' India\'s wholesale inflation prints today. October WPI is due, with fuel at the center: the Indian crude basket averaged roughly $120 a barrel in October, and September\'s print was 11.39% with fuel and power at 25.9%. IDFC First Bank\'s Gaura Sengupta expects 12.1 to 12.2% or higher - an expectation, labeled as one, not a number yet (' + a(MINT, 'Mint\'s preview') + '). The Federal Reserve\'s October minutes follow Wednesday.'),
 p(' A quiet reshuffle at the top of the Tata group turned into a process story. Noel Tata stepped down as chairman of Tata International effective 12 November, becoming chairman emeritus, with T V Narendran taking over - one move in a transition across six group companies (' + a(PMT, 'People Matters') + '). The friction surfaced at Voltas, where Sunil D\'Souza, the Tata Consumer Products chief, was named chairman succeeding Noel Tata: Business Standard reports that N Chandrasekaran - chairman of Tata Consumer, among his group roles - "was not kept informed" of the appointment ("it is learnt"; attributed reporting, not an established fact) and that the matter may come up at a high-level group meeting (' + a(BSV, 'Business Standard') + '). This paper reports the dates and the attribution, and infers no motive.'),
 p(' Two watch lines for the 9:15 open. Tata Motors PV and Eicher Motors filed results Friday at 4:20 PM, after the close - today is their first full trading session on the numbers (both reported in Saturday\'s edition). And ASEAN\'s Digital Economy Framework Agreement was signed Saturday in Manila: eleven economies, the region\'s first region-wide digital-economy agreement, ratification still pending, effect targeted for 2027 - the detail in the front page (' + a(PNA, 'the Philippine News Agency') + ').'),
 p(' The long read: the lab that left to be careful. Seven researchers walked out of OpenAI in one winter, wrote a constitution for a machine, and turned caution into $33.2 billion of nine-month revenue - Anthropic\'s build story, told from its own prospectus, as the book closes (' + a(LRURL, 'read it here') + '). The route ends. The detail begins.'),
]})

G.append({'heading': 'Front page', 'blocks': [
 p(' What the FAA confirmed, in its own words. The flood came over the FTI telecommunications network - the outsourced backbone L3Harris has run for the government for more than twenty years - during routine copper-to-fiber maintenance. At its peak, roughly 1,000 connection attempts every four to five seconds degraded controller communications and radar feeds; the instability reached 17 of the 22 en-route centers and spread to several approach facilities. The agency\'s containment was procedural, not architectural: L3Harris blocked the two suspect locations, and the broadcasting function is now disabled on all new routers until the investigation says otherwise (' + a(FAAQA, 'the Q&A') + '). The agency is explicit about what did not fail: none of the towers upgraded under the modernization\'s first tranche went down, and the SMART data aggregator - which does not feed air-traffic control - was unrelated.'),
 p(' Two accounts of cause, one open file. Bedford\'s Saturday wording - "faulty equipment," "zero evidence of anything nefarious, and zero evidence of anything AI-related" - is firmer than the FAA\'s Sunday wording: root cause under investigation; the El Dorado router sits in L3Harris\'s Florida lab for examination - the Secretary\'s detail, reported on ABC (' + a(ABCL, 'ABC News') + '). What settles it is the lab report. Until then the honest sentence is the long one: a specific new router at a specific Arkansas site is the suspect, the installation was the contractor\'s, and whether the fault was the unit or the work is not yet determined. The Secretary\'s Saturday framing - installer error or faulty router, undetermined - remains the state of knowledge (' + a(DOT, 'the department\'s statement') + ').'),
 p(' The recovery held through Sunday. Friday: 9,200 flights cancelled, 7,500 delayed. Saturday: more than 6,400 cancelled and 8,000 delayed - the longest nationwide halt since 9/11 (' + a(REU, 'Reuters') + '). The combined tally since Friday passed 17,500 on Sunday, with about 30 Monday flights cancelled as of late Sunday morning and airlines targeting a normal Monday; Duffy: "we\'re going to see things come back to normal today, but probably fully normal tomorrow" (' + a(ABCL, 'ABC News') + '). The Friday White House Situation Room meeting and the Secretary\'s $50 billion modernization ask are the political tail of the story. Watch the L3Harris open: $272.35 at Friday\'s close, $261.00 in after-hours.'),
 p(' Anthropic\'s terms, from the issuer. The float is 825 million Class A shares at $70 to $78 - midpoint $74 - of which 801,351,354 are primary and 23,648,646 secondary, the company receiving nothing from the secondary slice (' + a(ROAD, 'the roadshow post') + '). Pricing Wednesday, first trade Thursday as ANT. The concurrent $26 billion placement deserves its own sentence: AMD, Broadcom, Google, Micron, Microsoft, Nvidia and TSMC - the companies selling Anthropic its compute - will buy stock at the IPO price, closing immediately after the offering (' + a(S1, 'the S-1/A') + '). Reports of a six-times-covered book are Bloomberg\'s, attributed; reports of each co-founder holding roughly $18 billion of stock at the top half of the range are stockanalysis\'s arithmetic (' + a(STKA, 'their math') + ').'),
 p(' ASEAN signed its digital rulebook on Saturday. The Digital Economy Framework Agreement - DEFA - was signed at the 28th ASEAN Economic Community Council meeting in Manila, the region\'s first region-wide digital-economy agreement, covering all eleven economies (' + a(PNA, 'the Philippine News Agency') + '). The stage matters: signed is not in force. Ratification is pending; the ASEAN Secretary-General\'s own remarks say the implementation plan is to be ready "by May next year when DEFA goes into effect" - the bloc\'s target, not a settled date (' + a(DEFASG, 'the Secretary-General\'s remarks, as delivered') + '). The Straits Times reports negotiations ran from September 2023, with first projects expected early 2027 (' + a(ST, 'the Straits Times') + '). The prize being chased: a regional digital economy the Philippines frames as growing from $1 trillion toward $2 trillion by 2030.'),
 p(' SpaceX\'s Friday footnote, kept separate from Saturday\'s first. Flight 15 lifted off Friday; minutes later Booster 22 aborted its own catch attempt, steered offshore, and its flight-termination system fired about six and a half minutes after liftoff over the Gulf. The first explanation - a guidance, navigation and control issue detected late in coast - was corrected by SpaceX on Saturday: the GNC system did what it was designed to do and triggered the abort itself; early indications are the booster ended its boostback burn early on a low fuel-mass alarm, and the root cause is still under investigation (' + a(SPAB, 'Space.com') + '; ' + a(SPN, 'SpaceNews') + '). The upper-stage catch on Saturday - the historic one - stands, and the two outcomes are different machines on different days. The program\'s next flight now has two distinct questions to answer.'),
]})

G.append({'heading': 'Markets', 'blocks': [
 p(' Friday\'s marks are the tape until 9:15. Mumbai: Sensex 81,592.45, down 318.56 points (0.39%); Nifty 25,144.30, down 155.05 (0.61%). New York: S&P 500 7,561.67, down 0.40% Friday but up 2.51% on the week; Nasdaq 25,136.27, down 0.91% (+2.27% wk); Dow 52,347.55, up 0.10% (+2.07% wk); VIX 19.30; the US ten-year at 5.154% (' + a(PT, 'the weekly scorecard') + '). Friday\'s flows ran foreign, provisionally: FIIs bought a net Rs 5,737 crore while DIIs sold Rs 2,254 crore (' + a(TBT, 'the provisional tally') + '); one aggregator counts roughly Rs 26,131 crore of FII buying across Wednesday to Friday - attributed, and the confirmed series lags. This morning\'s markers, as of about 6:15 AM IST: GIFT Nifty at 25,258.00, down 0.03% on its own session and about 114 points above Friday\'s Nifty close - an indication, not an open; Dow futures +0.04%, S&P futures +0.19%, Nasdaq 100 futures +0.43%; Nikkei -0.75%, KOSPI -0.36%, Hang Seng yet to trade; Brent $95.42, down 0.44%; gold $3,888.30; dollar index 103.42; USD/INR 94.24 (' + a(GIFT, 'the pre-market screen') + '). The day\'s domestic number is October WPI, due today (preview in the lead route).'),
]})

G.append({'heading': 'IPOs', 'blocks': [
 p(' One offering owns the calendar. Anthropic is scheduled to price Wednesday evening and open Thursday as ANT: 825 million shares at $70 to $78, a $57.75-to-$64.35-billion raise, up to $1.404 trillion implied (' + a(TC, 'TechCrunch') + '). The mechanics to hold: 801.4 million primary shares fund the company; 23.6 million secondary shares cash out existing holders; the greenshoe adds up to 123.75 million; and the $26 billion concurrent placement means seven of the biggest names in chips and cloud take non-voting Class N stock at the same price the public pays (' + a(S1, 'the filing') + '). In Mumbai, last week\'s SEBI clearances - Razorpay, Sembcorp Green Infra and MakeMyTrip India - move from approval to preparation; nothing new priced over the weekend (' + a(CNBCTV18, 'CNBC-TV18') + '). The contrast that frames the week: a nearly six-year-old lab asking for the largest AI valuation ever, pricing two days after America\'s aviation agency explained how one router stopped the country - both are arguments about how much infrastructure a system can concentrate.'),
]})

G.append({'heading': 'Top movers - Friday\'s board stands', 'blocks': [
 p(' No weekend session, so Friday\'s verdicts are still the live board (percentages computed from BSE\'s official closes against Thursday):',
 ),
 {'t': 'chart', 'svg': movers},
 p(' What changes today is not the closes but the information. Ashok Leyland\'s Saturday print - profit up 12.7% on the company\'s own filing, detailed in Saturday\'s edition - gets its first full session. So do Tata Motors PV and Eicher Motors, whose numbers filed at 4:20 PM Friday, too late for Friday\'s tape. Brainbees (FirstCry) reported Saturday as well; the figures are in Corporate actions. On the US side, L3Harris opens with a named-router investigation and a 4% after-hours discount to unwind or extend; Nvidia opens one day before its first post-Huang print. Friday\'s closes, carried: Hindustan Unilever Rs 1,985.00, Bajaj Finance Rs 1,115.20, ONGC Rs 225.30, Eternal Rs 364.50; Bharat Electronics Rs 401, Bajaj Finserv Rs 1,860, TCS Rs 2,410, Maruti Suzuki Rs 12,878, State Bank of India Rs 1,080.50, ICICI Bank Rs 1,584.'),
]})

G.append({'heading': 'Corporate actions', 'blocks': [
 p(' FirstCry\'s parent reported Saturday. Brainbees Solutions, in an exchange filing dated 14 November: Q2 revenue of Rs 2,396 crore, up 14.1% year on year, and a consolidated net loss narrowed 75.1% to Rs 12.6 crore from Rs 50.5 crore a year ago (' + a(ETFC, 'the Economic Times') + '; ' + a(FCIR, 'the company\'s investor presentation') + '). The loss line is the one that matters for a listings-era retailer: a 75% narrowing is a trajectory statement, and today is its first full session on the tape. Carried dates: Natco Pharma\'s dividend record date is Thursday 19 November; Ashok Leyland\'s Re 1 interim and Oil India\'s dividend share the Friday 20 November record date. On the governance file - Noel Tata\'s six-board transition and the Voltas handover - the confirmed facts and the attributed reporting are kept separate in the lead route and front page; nothing further filed over the weekend.'),
]})

G.append({'heading': 'Finance Goldmine', 'blocks': [
 p(' How to read a trillion-dollar filing in four lines. Anthropic\'s S-1/A rewards a specific order of reading, and the order is the lesson (' + a(S1, 'the filing itself') + '). First line: the ramp - revenue of $41 million in 2023, $386 million in 2024, $4.6 billion in 2025, $33.2 billion in the first nine months of 2026. Second line: the loss, with its own footnote - $41.97 billion in 2025 and $104.0 billion for the nine months, figures the company says are inflated by fair-value marks on convertible notes; the pro forma numbers are $32.4 billion and $96.8 billion. When a company tells you its own headline loss overstates the burn, read the pro forma and note the habit. Third line: the commitments - roughly $900.9 billion of purchase obligations, substantially all compute, with $70.7 billion due within twelve months and about $451.6 billion before the end of 2030; a further $150 to 175 billion of estimated payments sits outside the table, of which $125 to 150 billion is additional Google TPU compute, delivery 2028 to 2031. Fourth line: the customers - roughly 40 million on a trailing basis, more than 1,900 paying above $1 million a year, about 250 above $10 million. Ramp, honest loss, obligations, concentration: read any mega-IPO in that order and the valuation headline becomes the least interesting number in the book.'),
]})

G.append({'heading': 'Startup Intelligence', 'blocks': [
 p(' The weekend cards, kept at arm\'s length. Agnikul Cosmos plans a Rs 510-crore facility in Tirupati under a memorandum of understanding with Andhra Pradesh, to build orbital data-centre units - MoU-stage, per the weekend reports. Baaz Bikes raised a Rs 46-crore Series B for its electric two-wheeler fleet play. Atomberg, fresh from its SEBI clearance, is putting Rs 100 crore of IPO proceeds into research and development. And Nexus Venture Partners\' partner Anup Gupta will step down in June 2027 after nearly 17 years - succession announced about seven months ahead. Each item is reported, not yet read against filings; the ones that matter to the tape get verified when they file. The pattern to note: hardware - rockets, bikes, fans - is where the disclosed cheques went this weekend.'),
 p(' Today\'s startup idea: an independent incident observatory for public infrastructure. Friday proved the shape of the gap: America\'s aviation status pages reported a degraded network for hours before any official account existed, and the authoritative explanation arrived two days later as a web page. A service that continuously archives public status surfaces - the FAA\'s NAS Status, grid operators, payment rails, cloud status pages - timestamps what they said and when, and builds a queryable public timeline of every degradation. The wedge is aviation: airlines, insurers, corporate travel desks and airports all reconstruct incidents after the fact, and today they do it from screenshots. Sell the timestamped record and the alerting feed; give the timeline away for credibility. What would make it wrong: the agencies themselves publishing machine-readable history - in which case the honest pivot is the alerting SLA, where being early is the whole product.'),
]})

G.append({'heading': 'AI Race', 'blocks': [
 p(' The whole trade is one company\'s week. CNBC frames Anthropic\'s debut as make-or-break for the technology industry - a framing, attributed (' + a(CNBC, 'the piece') + '). The filing supports at least the size of the claim: a company with $33.2 billion of nine-month revenue carrying $900.9 billion of purchase commitments is not just going public; it is securitizing the sector\'s entire build-out, down to a $110-billion, ten-year, non-cancelable commitment to Amazon (' + a(S1, 'the S-1/A') + '). The placement list makes the loop literal - AMD, Broadcom, Google, Micron, Microsoft, Nvidia and TSMC will hold Anthropic stock from the first trade - non-voting Class N, not the ANT float (' + a(ROAD, 'the company') + '). Into that week lands Nvidia\'s Tuesday print: the first demand read since the stock\'s worst week since April and its first without the CEO who defined it (' + a(NVN, 'the company\'s notice') + '). Two companies, four days, and every portfolio with an AI sleeve is exposed to both.'),
]})

G.append({'heading': 'Vibe coding', 'blocks': [
 p(' Read the FAA\'s Sunday page as a post-incident review, because it is a good one. The mitigations came before the root cause: block the two suspect sites, disable the risky default - broadcasting - on all new routers, and say plainly that the cause is still open (' + a(FAAQA, 'the document') + '). That ordering is the transferable discipline. In a deploy, the precautionary disable is cheaper than the root-cause debate: you can re-enable a feature; you cannot un-degrade a national network. The second lesson is about language: "no indication of a cyberattack" is a statement about evidence reviewed so far, and the page says exactly that - copy that precision into your own incident updates. The third is about age: the component that failed sat in a legacy system mid-migration, maintained by a contractor on a contract older than some of the engineers reading this. Every dependency list has an oldest vendor; Friday is what its failure mode looks like. Audit yours before it files its own Q&A.'),
]})

G.append({'heading': 'Try this today (Monday)', 'blocks': [
 p(' Bookmark the page the FAA itself recommends. The agency\'s Sunday Q&A points travelers to NAS Status - ' + a(NASS, 'nasstatus.faa.gov') + ' - for real-time airport delay and ground-stop information (' + a(FAAQA, 'the recommendation, in context') + '). Free, on the web, no login. How to use it: open the map, find your airport, and read the general delay and ground-stop programs before you leave for the terminal; during irregular operations it updates faster than the evening news. The limits are honest: it covers US airports, and it reports system status rather than your specific flight - pair it with the airline\'s own app for the tail number. With about 30 Monday cancellations on the board as of late Sunday and airlines targeting a normal day, today is exactly the kind of morning this page earns the bookmark (' + a(ABCL, 'the recovery tally') + ').'),
 p(' Then the two primary reads behind this edition\'s lead. The FAA\'s own question-and-answer page - two screens, every operational number in today\'s paper traceable to it (' + a(FAAQA, 'the Q&A') + '). And for the space footnote: Space.com\'s account of Booster 22 declining to be caught - an abort the guidance system called, a divert, and a flight-termination system doing its job (' + a(SPAB, 'the account and video') + ').'),
]})

G.append({'heading': 'One concept: single point of failure', 'blocks': [
 p(' A single point of failure is the component whose failure stops the system - the one part with no understudy. Engineering doctrine hunts them relentlessly, because they convert small faults into total outages: the question is never "will this part fail" but "what stops when it does." Friday gave the concept a national demonstration. One router\'s behavior - flooding a network with connection attempts - degraded 17 of 22 en-route centers, and the mitigation that worked was procedural, not architectural: humans blocking sites and disabling a feature, because the redundancy that should have absorbed the fault was the thing the fault rode in on (' + a(FAAQA, 'the FAA\'s account') + '). That is the concept\'s sharpest lesson: redundancy that shares a failure mode is not redundancy, and the honest audit question is not "do we have a backup" but "does the backup fail the same way." Worth asking of your supply chain, your cloud region, and your Monday morning.'),
]})

G.append({'heading': 'Term of the day: greenshoe', 'blocks': [
 p(' The greenshoe is the underwriters\' overallotment option: the right to sell extra shares - conventionally up to 15% of the base offering - at the offer price, named for the company first granted one. It exists to stabilize a debut: if the stock jumps, the underwriters exercise the option and deliver the extra shares; if it sags, they buy shares in the market to cover their short, which supports the price. Anthropic\'s greenshoe is exactly 15%: 123.75 million shares on top of the 825 million base, which at the $70-78 range adds up to between roughly $8.7 and $9.7 billion of potential stabilization capacity (' + a(S1, 'the filing') + '). When the coverage around the debut says "the underwriters exercised the greenshoe," you will know what actually happened: demand ran hot enough that the stabilizers became sellers.'),
]})

G.append({'heading': 'Setup board', 'blocks': [
 p(' Monday\'s board is a carry-forward: no weekend session, so Friday\'s prices stay the live marks until 9:15, and tonight\'s close is the next scored session. The desk\'s rule stands: every published setup stays on the board until it resolves by its own rules.',
 ),
 {'t': 'chart', 'svg': board_html},
 {'t': 'chart', 'svg': ongc_range},
 p(' The resolved line stays in the ledger: HCLTech, filled 28 October at the worst fill of Rs 1,378.00, target Rs 1,466.80 taken out at 1,468.00 - gross +6.44%, net +6.14% after the 0.3% cost convention - closed Friday at Rs 1,376.60. Shelved: Voltas stays rejected; Tech Mahindra stays shelved above the Rs 1,500 cap.'),
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
 p(' One weekend, three verdicts on how we run the systems we depend on. The FAA narrated its own failure while the cause was still open - two sites named, the contractor named, the precaution disclosed, the unknowns labeled unknown - and turned the usual rhythm of infrastructure failure, a weekend of silence and a month of lawyers, into something closer to a template; whether the lab finding gets published with the same directness is what the template is worth. Anthropic, meanwhile, asks public investors to price a constitution: a trust that can fire the board, founders who cannot be outvoted, five percent bound to the mission - five years of structure meeting a single number on Wednesday, and the market has never priced all three of growth, burn and mission at a trillion dollars in one book. And Nvidia reports into the strangest context of its public life, record franchise and interim leadership at once - a reminder that succession is never just a governance story when the company is the market\'s load-bearing wall. The common thread: resilience is not the absence of failure but the presence of honest accounting - the agency that names its router, the lab that files its guardrails, the board that states its search stage. Price the accounting, not the absence.'),
]})

G.append({'heading': 'Brewing', 'blocks': [
 p(' The root-cause file. Cause chain: a 24-year-old outsourced network; routine copper-to-fiber maintenance at two southern sites; a new router flooding the backbone at 1,000 attempts every four to five seconds; 17 of 22 centers degraded; the contractor blocking its own two locations; broadcasting disabled fleet-wide as a precaution; the suspect unit in a Florida lab. What settles it: the lab finding - unit or install - and whether the FAA publishes it with Sunday\'s directness. Watch: the L3Harris open, and any update to the FAA\'s page.'),
 p(' The debut file. Cause chain: the S-1/A on 10 November; the roadshow launch; a $70-78 range on 825 million shares; a reported six-times-covered book; a $26 billion supplier placement at the IPO price; pricing Wednesday; first trade Thursday as ANT. What settles it: the price, then the first print - in that order, and neither is knowable today. Watch: Wednesday evening.'),
 p(' The succession file. Cause chain: Noel Tata\'s exit across six group boards, effective 12 November; T V Narendran named at Tata International; Sunil D\'Souza named Voltas chairman; Business Standard reporting that Chandrasekaran "was not kept informed" - attributed, not established; a high-level group meeting where the matter may surface. What settles it: whether the process story stays a process story - a statement, a clarification, or silence. Watch: any group communication, and Voltas\'s first session on the narrative.'),
]})

G.append({'heading': 'The week ahead', 'blocks': [
 rows([
  row('1', 'Mon 16 Nov (today)', 'October WPI prints (IDFC First poll: 12.1-12.2%+, expectation; September was 11.39%). First full session on Tata Motors PV, Eicher and the Saturday batch. L3Harris opens. Nvidia Q3 eve.'),
  row('2', 'Tue 17 Nov', 'Nvidia Q3 FY27 results, 2 PM Pacific; CFO commentary in writing ahead of the call. First print since the CEO transition.'),
  row('3', 'Wed 18 Nov', 'Anthropic prices the 825-million-share offering ($70-78 range). FOMC October minutes.'),
  row('4', 'Thu 19 Nov', 'ANT debuts on the Nasdaq; the $26 billion supplier placement closes after the offering. Natco Pharma dividend record date.'),
  row('5', 'Fri 20 Nov', 'Record date for Ashok Leyland\'s Re 1 interim dividend and Oil India\'s dividend.'),
  row('6', 'Watching', 'The FAA-L3Harris lab finding on the El Dorado router; DEFA ratification track (effect targeted 2027); Nvidia\'s search-firm selection; the Tata group\'s next communication.'),
 ]),
]})

G.append({'heading': 'Notes on this edition', 'blocks': [
 bullets([
  'Sources read for this edition: the FAA\'s own Sunday Q&A, ABC News\' live coverage and Reuters for the ground stop and recovery; the Transportation Department\'s Saturday statement; Anthropic\'s S-1/A-2 on EDGAR and its roadshow post, with TechCrunch, CNBC and stockanalysis for range, framing and founder arithmetic; Nvidia\'s own newsroom notice and CNBC for the search stage; Business Standard and People Matters for the Tata file; Mint for the WPI preview; Space.com and SpaceNews for the booster; the Brainbees exchange filing via the Economic Times and the company\'s own investor presentation; the ASEAN Secretary-General\'s published remarks, the Philippine News Agency and the Straits Times for DEFA; BSE\'s official bhavcopy for Indian prices and the portfolio scorecard for the US week; the provisional FII/DII tally, labeled provisional.',
  'Framing calls this edition: the router\'s root cause is open and is reported open - Bedford\'s "faulty equipment" and the FAA\'s "investigation continues" are quoted as the different statements they are; Duffy\'s "fully normal Monday" is a forecast, attributed; the WPI figure is a poll, labeled; the Nvidia search is "in the process of selecting a search firm," exact; the Chandrasekaran line is Business Standard\'s attributed reporting, and no motive is inferred; Anthropic\'s book coverage and founder stakes are reported figures, attributed; weekend startup cards are carried as reported, not filing-verified.',
  'Prices are BSE official closes or the named settlement prints; provisional flow figures are labeled provisional; the GIFT Nifty line is an as-of indication, not an open. Nothing here is investment advice.',
 ]),
 closing(' The router is in a lab in Florida; the book closes Wednesday; the first print lands tomorrow. See you tomorrow.'),
]})

fact = ('Edition 42. The FAA\'s own account, and the trillion-dollar week. Monday 16 November 2026, edition 42. This edition runs 4,819 words. '
 'The FAA has published its own account of Friday\'s nationwide ground stop: two sites, one new router, a contractor blocking its own locations - and a root cause still open. '
 'Anthropic is set to price the largest AI listing ever attempted on Wednesday: 825 million shares at $70 to $78, trading Thursday as ANT. Nvidia reports tomorrow, its first results since Jensen Huang\'s exit. October wholesale inflation prints in Mumbai today, with crude at the center; Friday\'s marks stand: Sensex 81,592.45, Nifty 25,144.30. '
 'The long read: Anthropic - the lab that left to be careful.')

intro = ('The 5-minute lead route is first; sections carry the detail. The long read: seven researchers left the industry\'s most famous lab in one winter, '
 'wrote a constitution for a machine, and turned caution into 33 billion dollars of nine-month revenue - the Anthropic build story, from its own prospectus, as the book closes.')

d = {
 'day': 42,
 'meta': {'date': 'Monday 16 November 2026', 'short': 'Mon 16 Nov', 'longread': 42},
 'edition': {'fact': fact, 'intro': intro, 'groups': G},
 'audio': ({
   'quick': 'audio/d42-quick.m4a',
   'durations': {},
   'segments': [
     {'key': 'segment1', 'label': 'Opening and the five-minute lead route'},
     {'key': 'segment2', 'label': 'Front page: the account, the cause, the recovery'},
     {'key': 'segment3', 'label': 'Front page: the terms, the agreement, the footnote'},
     {'key': 'segment4', 'label': 'Markets, IPOs, and the top movers'},
     {'key': 'segment5', 'label': 'Corporate actions, Finance Goldmine, and Startup Intelligence'},
     {'key': 'segment6', 'label': 'AI Race, vibe coding, try this, and the single point of failure'},
     {'key': 'segment7', 'label': 'Term of the day and the setup board'},
     {'key': 'segment8', 'label': 'Board scoring, the editor\'s read, and Brewing'},
     {'key': 'segment9', 'label': 'The week ahead and the notes on this edition'},
   ],
   'segment1': 'audio/d42-segment1.m4a', 'segment2': 'audio/d42-segment2.m4a', 'segment3': 'audio/d42-segment3.m4a',
   'segment4': 'audio/d42-segment4.m4a', 'segment5': 'audio/d42-segment5.m4a', 'segment6': 'audio/d42-segment6.m4a',
   'segment7': 'audio/d42-segment7.m4a', 'segment8': 'audio/d42-segment8.m4a', 'segment9': 'audio/d42-segment9.m4a',
   'full': 'audio/d42-full.m4a',
 } if os.path.exists('editions-src/ed42/audio_ready') else None),
}
json.dump(d, open('editions-src/day-42.json', 'w'), indent=1, ensure_ascii=False)
print('day-42.json written; groups:', len(G))
