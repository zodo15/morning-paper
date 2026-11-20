#!/usr/bin/env python3
"""Build editions-src/day-46.json - Friday 20 November 2026."""
import json

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}
def rows(items): return {'t': 'rows', 'items': items}
def row(n, title, detail): return {'n': n, 'title': title, 'detail': detail}
def bullets(items): return {'t': 'bullets', 'items': items}
def closing(html): return {'t': 'closing', 'html': html}
def chart(svg): return {'t': 'chart', 'svg': svg}

CNBC_ANT = 'https://www.cnbc.com/2026/11/19/anthropic-ipo-ant-live-updates.html'
AP_ANT = 'https://apnews.com/article/anthropic-ipo-nasdaq-ai-b6a74b8949021207dc162fcc876c4649'
UPI_ANT = 'https://www.upi.com/Top_News/US/2026/11/19/stocks-nasdaq-anthropic-wall-street/3191795106026/'
REUT_WRAP = 'https://www.streetinsider.com/Reuters/Wall+Street+ends+sharply+lower+as%C2%A0Anthropics+debut+fails+to+revive+AI+fervor/27376046.html'
AP_INDEXES = 'https://apnews.com/article/wall-street-stocks-dow-nasdaq-2f178054aea79d282e5ccf8d62f26a28'
DJ_NASDAQ = 'https://www.morningstar.com/news/dow-jones/202611199618/nasdaq-composite-falls-225-to-2387920-data-talk'
BS_CLOSE = 'https://www.business-standard.com/markets/news/nifty-tops-25-500-for-first-time-since-february-sensex-reclaims-83k-126111901140_1.html'
HBL_CLOSE = 'https://www.thehindubusinessline.com/markets/sensex-nifty50-today-stock-market-live-updates-19th-november-2026/article71717151.ece'
FII_TV18 = 'https://www.cnbctv18.com/market/fiis-data-india-draws-over-usd-13-billion-in-inflows-extends-buying-streak-14-sessions-20037950.htm'
FII_FE = 'https://www.financialexpress.com/market/fiis-pump-in-rs-7411cr-diis-offload-rs-1356cr-3-factors-lifting-market-sentiment-4388788/'
RUPEE_MC = 'https://www.moneycontrol.com/news/currency/rupee-hits-7-month-high-on-stock-rally-traders-eye-exporters-for-fresh-fuel-14084810.html'
MARUTI_TV18 = 'https://www.cnbctv18.com/market/maruti-suzuki-india-share-price-top-nifty-auto-gainer-commodity-cost-tailwind-aluminium-copper-buy-sell-returns-20037438.htm'
FR_RULE = 'https://www.federalregister.gov/documents/2026/11/19/2026-23529/addressing-remote-access-to-advanced-semiconductors'
NVDA_REUT = 'https://www.investing.com/news/stock-market-news/nvidia-stops-shipping-usapproved-ai-chips-china-5035204'
AMD_CNBC = 'https://www.cnbc.com/2026/11/19/amd-falls-on-short-seller-report-of-alleged-china-exposure.html'
GOLD_CNBC = 'https://www.cnbc.com/2026/11/19/gold-silver-metals-price-treasury.html'
GOLD_KITCO = 'https://www.kitco.com/news/article/2026-11-19/gold-falls-below-3650-silver-tumbles-fed-rate-concerns-pressure-metals'
OIL_NEWSQUAWK = 'https://www.newsquawk.com/headlines/crude-wrap-wti-f7-settles-usd-005-lower-at-usd-8321bbl-brent-f7-settles-usd-003-higher-at-usd-9198bbl'
OIL_REUT = 'https://www.investing.com/news/commodities-news/oil-prices-steady-as-supply-surplus-softens-sentiment-though-gulf-war-supports-5037604'
MAH_MINT = 'https://www.livemint.com/market/ipo/mahanadi-coalfields-ipo-ipo1422'
MAH_UPSTOX = 'https://upstox.com/news/market-news/ipo/mahanadi-coalfields-ipo-day-1-check-subscription-status-price-band-and-other-details/article-203685/'
MUTHOOT = 'https://scanx.trade/stock-market-news/companies/muthoot-microfin-board-meet-nov-19-consider-restated-financials/56125092'
SEBI_MC = 'https://www.moneycontrol.com/news/business/markets/sebi-yet-to-decide-on-linking-mtf-exposure-limits-to-stock-free-float-chairman-tuhin-kanta-pandey-14083337.html'
ET_CORP = 'https://economictimes.indiatimes.com/markets/stocks/news/stock-splits-dividends-oil-india-cochin-shipyard-mrf-among-31-companies-turning-ex-record-date-this-week/articleshow/135846835.cms'
INPRIME = 'https://economictimes.indiatimes.com/small-biz/entrepreneurship/inprime-finserv-raises-10-7-million-in-series-b-funding-led-by-fmo/articleshow/135989279.cms'
VITUS = 'https://www.business-standard.com/companies/start-ups/healthcare-startup-vituscare-secures-30-crore-in-a-series-b-funding-round-126111801393_1.html'
BOLTZ = 'https://siliconangle.com/2026/11/19/medical-ai-startup-boltz-raises-110m-to-speed-up-small-molecule-research/'
OAI_JAGGED = 'https://openai.com/index/research-acceleration-jagged-frontier'
OAI_FACTORY = 'https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast/'
OAI_CHIP = 'https://openai.com/index/advancing-chip-design-with-our-models/'
OAI_ACCT = 'https://openai.com/business/solutions/accounting/'
TREASURY = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026'

def movers_chart():
    # Tracked large names, Thursday 19 Nov % vs Wednesday, BSE official prints (series A)
    data = [
        ('Eicher Motors', 4.73), ('Ashok Leyland', 2.37), ('Oil India', 0.46),
        ('Adani Enterprises', 0.42), ('Oberoi Realty', 0.39), ('Godrej Properties', 0.37),
        ('Prestige Estates', -0.23), ('Wipro', -0.59), ('Tata Communications', -0.93),
        ('HCL Tech', -1.10),
    ]
    n = len(data); h = 30 + 48*n
    scale = 42; zero = 300
    out = ['<svg viewBox="0 0 760 %d" role="img" aria-label="Leaders and laggards among the large names this paper tracks, Thursday 19 Nov (%% vs Wednesday close), BSE official prints">' % h]
    for i, (name, val) in enumerate(data):
        ty = 47 + 48*i; ry = 30 + 48*i
        out.append('<text x="8" y="%d" font-size="21" fill="#334155">%s</text>' % (ty, name))
        w = abs(val)*scale
        lab = '%+.2f%%' % val
        if val >= 0:
            out.append('<rect x="%d" y="%d" width="%s" height="26" fill="#15803d" rx="3"/>' % (zero, ry, round(w,1)))
            out.append('<text x="%s" y="%d" text-anchor="start" font-size="20" fill="#15803d">%s</text>' % (round(zero+w+8,1), ty+2, lab))
        else:
            out.append('<rect x="%s" y="%d" width="%s" height="26" fill="#b91c1c" rx="3"/>' % (round(zero-w,1), ry, round(w,1)))
            out.append('<text x="%s" y="%d" text-anchor="end" font-size="20" fill="#b91c1c">%s</text>' % (round(zero-w-8,1), ty+2, lab))
    out.append('</svg><p style="font-size:13px;color:#64748b;line-height:1.5">Leaders and laggards among the large names this paper tracks, Thursday 19 Nov (% vs Wednesday\'s close), BSE official prints.</p>')
    return ''.join(out)

def ongc_chart():
    lo, hi, now = 218.50, 238.75, 224.50
    scale = (591.29-204.52)/(hi-lo)
    x0 = 204.52 - lo*scale
    xl, xn, xh = x0+lo*scale, x0+now*scale, x0+hi*scale
    return ('<svg viewBox="0 0 760 125" role="img" aria-label="ONGC: coil floor to coil top, Thursday close marked">'
            '<text x="8" y="44" font-size="23">ONGC</text>'
            '<line x1="%s" x2="%s" y1="38" y2="38" stroke="#15803d" stroke-width="10"/>'
            '<circle cx="%s" cy="38" r="10" fill="#172b3c"/>'
            '<text x="%s" y="82" font-size="19" text-anchor="middle">218.50</text>'
            '<text x="%s" y="16" font-size="19" text-anchor="middle">224.50</text>'
            '<text x="%s" y="82" font-size="19" text-anchor="middle">238.75</text></svg>'
            '<p style="font-size:13px;color:#64748b">ONGC\'s coil: floor 218.50, top 238.75; Thursday\'s close 224.50, sixth session under the 228 breakout line.</p>') % (round(xl,1), round(xh,1), round(xn,1), round(xl,1), round(xn,1), round(xh,1))

ed = {}
ed['fact'] = ("Edition 46. Friday 20 November 2026. This edition runs WORDCOUNT words. The biggest listing in history met Wall Street's worst week since April: Anthropic's ANT opened at $111.50 and closed its first session at $97.17, up 17% on the $83 print, while the S&P 500 fell a sixth straight day and the Dow closed below 50,000. Mumbai went the other way - the Sensex rose 990 points to 83,022, its first close over the mark this week, as foreign investors completed the largest month of buying on record. The BIS remote-access chip rule took effect as preannounced; Nvidia has stopped shipping even its licensed chips to China. The long read: Nasdaq, the market the biggest IPO chose.")
ed['intro'] = ("The 5-minute lead route is first; sections carry the detail. The long read: the biggest listing in history did not happen on a trading floor - it ran on a network built in 1971 because the pink sheets were always stale. Nasdaq, the market that was never a place.")
ed['hero'] = {'img': 'photos/d46-hero.jpg', 'alt': 'Abstract plate: a gavel, a rising staircase of bars, and a ticker ribbon splitting into two directions'}

groups = []

# 0 - The 5-minute lead route
groups.append({'heading': 'The 5-minute lead route', 'blocks': [
    p(" ANT closed its debut up 17%%. The largest listing ever opened at $111.50, touched $115.10 - a valuation above $2 trillion for a moment - and closed at $97.17, seventeen percent over the $83 print, with more than 846 million shares changing hands (%s; %s)." % (a(CNBC_ANT,'CNBC'), a(AP_ANT,'AP'))),
    p(" Wall Street fell anyway. The S&P 500 lost 2.02%% to 7,175.83 - a sixth straight loss, its longest streak since 2024 - the Dow dropped 1,101 points to 49,097.06, below 50,000, and the Nasdaq fell 2.25%% to 23,879.20, now 13.5%% under its October peak (%s). The indexes hit their lows of the session just as ANT began trading; that is a coincidence of timing, not an established cause." % a(AP_INDEXES,'AP')),
    p(" Mumbai rallied through it. The Sensex rose 989.94 points (1.21%%) to 83,021.75 and the Nifty 286.35 (1.14%%) to 25,514.30 - its first close above 25,500 since February 23 - with Bank Nifty posting its third record close of the week at 63,063 (%s)." % a(BS_CLOSE,'Business Standard')),
    p(" Foreign money set a record. FIIs bought a provisional Rs 7,411.41 crore on Thursday - a fourteenth straight buying session - taking November past Rs 1.01 lakh crore, the biggest monthly haul on record; DIIs sold Rs 1,356.57 crore (%s; %s)." % (a(FII_TV18,'CNBC-TV18'), a(FII_FE,'FE'))),
    p(" The chip rule is law, and Nvidia moved first. The BIS remote-access rule took effect Thursday, as preannounced when it was released Monday; hours earlier Reuters reported Nvidia has stopped shipping even its licensed Hopper chips to China, on interim CEO Colette Kress's word (%s; %s)." % (a(FR_RULE,'the rule'), a(NVDA_REUT,'Reuters'))),
    p(" A short seller knocked 8%% off AMD. Hunterbrook published alleged supply-chain ties to blacklisted Chinese firms and disclosed its fund is short the stock; AMD says the claims misrepresent its practices (%s)." % a(AMD_CNBC,'CNBC')),
    p(" Gold broke to a 14-month low. Spot closed at $3,650, December futures settled near $3,651, and the market now fully prices a December rate hike; the ten-year yield still fell to 5.04%% as money hid in bonds (%s)." % a(GOLD_CNBC,'CNBC')),
    p(" The long read: Nasdaq. The biggest IPO in history did not trade on a floor; it traded on a quotation network the SEC asked a trade association to build in 1971, because the pink sheets were always stale. From Trumbull, Connecticut, to the top of the IPO record book - the market that was never a place."),
]})

# 1 - Front page
groups.append({'heading': 'Front page', 'blocks': [
    p(" The debut, in full. Anthropic opened for trading shortly before noon in New York, the Amodeis on the Nasdaq bell podium. The first print was $111.50 - 34%% over the $83 price set Wednesday night - and the stock briefly reached $115.10, a fully diluted value above $2 trillion, before the bid thinned. It closed at $97.17, up 17.07%%, with more than 846 million shares traded - against 522 million on SpaceX's opening day in June - and a fully diluted market value near $1.76 trillion, which CNBC counts as the seventh-most-valuable US company (%s; %s; %s). A 17%% first-day pop on an $81.3 billion book is strong by any historical measure; it is also a long fade from the high, and both halves of that sentence will matter when the greenshoe question arrives." % (a(CNBC_ANT,'CNBC'), a(AP_ANT,'AP'), a(UPI_ANT,'UPI'))),
    p(" The tape it landed into. The S&P 500's sixth straight loss - 2.02%% to 7,175.83 - is its longest streak since 2024 and leaves the index 8.2%% under last month's record; the Dow's 1,101-point fall (2.19%%) closed it at 49,097.06, below 50,000; the Nasdaq lost 2.25%% to 23,879.20, 13.5%% under its October peak (%s; %s). Nvidia fell a sixth straight session; AMD lost 7.7%% on a short seller's report (below); even the Anthropic-adjacent names - Amazon, Alphabet, Broadcom - gave back their premarket gains. The week is on course to be the S&P's worst since April 2025 (%s)." % (a(AP_INDEXES,'AP'), a(DJ_NASDAQ,'Dow Jones'), a(REUT_WRAP,'Reuters'))),
    p(" The divergence, stated carefully. On the same clock, Mumbai had one of its best days of the year: the Sensex's 990-point rise to 83,021.75 and the Nifty's first 25,500 close since February came on record foreign buying, a seven-month-high rupee and an auto sector re-rated on falling input costs (%s). One session's opposite directions do not prove money is rotating from the AI trade to India; the US slide is six sessions old and India's rally has its own fourteen-session logic. Argent Capital's Jed Ellerbroek made the same point from the other side, telling Reuters he would not extrapolate meaning from debut-day trading - portfolio money making room for Anthropic moves prices without saying anything about demand (%s). What is established: the two biggest pools of risk appetite in this paper's readership moved apart on the day they were supposed to be joined at the hip." % (a(BS_CLOSE,'Business Standard'), a(REUT_WRAP,'the interview'))),
    p(" The chip war opened a second front. The Commerce Department's remote-access rule took effect Thursday - 30 pages in the Federal Register, interim final, comments open until 19 January 2027. It restricts exports, re-exports and in-country transfers to overseas data centers that remotely supply significant compute to companies headquartered in Country Group D:5 or Macau, and it puts due-diligence duties on data centers, foundries and exporters; commercial recommender systems are carved out (%s). The rule was released Monday, so none of that is news to a datacenter lawyer. The news is the timing of Reuters' Wednesday scoop: Nvidia has stopped shipping its licensed Hopper chips to China entirely, interim CEO Colette Kress said, after roughly $2.4 billion of quarterly China sales - a company choosing the strictest reading of the room before the room's rules even bite (%s)." % (a(FR_RULE,'the published rule'), a(NVDA_REUT,'Reuters'))),
    p(" The short seller and the chipmaker. Hunterbrook Media alleged AMD firmware keeps appearing at blacklisted Chinese companies, and disclosed that its affiliated fund is short the stock; AMD fell 7.7%%, its worst day of this selloff, and answered that the claims misrepresent its practices (%s). File it correctly: an allegation from an interested party, met by a denial - the truth of it will be settled by export-control lawyers, not by Thursday's tape. But the report landed on the same day the chip-access rule took effect, which is why it found a bid." % a(AMD_CNBC,'CNBC')),
    p(" Gold broke, and told you why. Spot gold closed at $3,650.12, down 2%% and the lowest in fourteen months; December futures settled near $3,651 after touching $3,668.40, and Kitco's afternoon report had spot through $3,650 late in New York (%s; %s). The driver is the rate path: CNBC's markets desk writes that the market now fully prices a hike at the Fed's December meeting, with the dollar index at its highest since April 2025. The ten-year Treasury yield still fell, 5.07%% to 5.04%% on the Treasury's own daily curve - the classic risk-off bid running underneath the repricing (%s). When gold falls and bonds rally on the same day, the market is not pricing growth; it is pricing fear with a rate hike on top." % (a(GOLD_CNBC,'CNBC'), a(GOLD_KITCO,'Kitco'), a(TREASURY,'the curve'))),
]})

# 2 - Markets
groups.append({'heading': 'Markets', 'blocks': [
    p(" Thursday's marks, then this morning's markers. Mumbai: Sensex 83,021.75, up 989.94 (1.21%%); Nifty 25,514.30, up 286.35 (1.14%%), closing at its high after dipping to 25,104.80 in the opening minutes on the Fed-minutes hangover; Bank Nifty 63,063, up 1.65%%, a third record close this week; BSE Bankex 71,035.37, up 1.80%%; PSU banks up 2.43%%; FMCG up 2.09%%; consumer durables up 3.64%%; IT the laggard, down 1.10%% to 30,919.45 (%s). New York: Dow 49,097.06, down 1,101 (2.19%%); S&P 500 7,175.83, down 2.02%%; Nasdaq 23,879.20, down 550.69 (2.25%%) (%s). Rupee 93.29 to the dollar, a seven-month high (%s). Oil settled nearly flat: Brent $91.98, up three cents; WTI $83.21, down five, as Hormuz tanker-disruption reports offset surplus forecasts and rising US inventories (%s; %s). This morning's markers (stamped 5:50-6:00 AM IST): spot gold last quoted near $3,651 after its $3,650.12 close, a 14-month low; the ten-year Treasury printed 5.04%% Thursday against 5.07%% Wednesday; GIFT Nifty's derived quote was 95.50 points (0.37%%) lower at 22:12 IST Thursday, before the US close fully landed - a contested signal for today's open; the Nikkei opened Friday up 0.34%% at 61,348. On MCX, December gold closed at Rs 1,28,868 per ten grams, down 0.73%%, and silver at Rs 1,59,743 a kilo, down 0.62%%." % (a(BS_CLOSE,'the close report'), a(AP_INDEXES,'AP'), a(RUPEE_MC,'moneycontrol'), a(OIL_NEWSQUAWK,'the settle'), a(OIL_REUT,'Reuters'))),
]})

# 3 - IPOs
groups.append({'heading': 'IPOs', 'blocks': [
    p(" Mahanadi Coalfields, day one: 38%% booked. The Coal India arm's Rs 9,000.97-crore offer at Rs 129-136 a share (lot of 110) received bids for 0.38 times the shares on offer by 5 PM Thursday (%s). The book runs to Monday 23 November; allotment is slated for the 25th and listing for the 27th, tentative (%s). Day-one subscription in a five-day book tells you little by itself - retail typically arrives late - but a slow open against a red-hot primary market abroad is a contrast worth noting, not a verdict. And tonight in New York: ANT's second session, where the question is whether the 147-million-share greenshoe stays theoretical." % (a(MAH_UPSTOX,'the day-one tally'), a(MAH_MINT,'the calendar'))),
]})

# 4 - Top movers
groups.append({'heading': "Top movers - Thursday's verdicts", 'blocks': [
    p(" Thursday's board - the large names this paper tracks, from best to worst (percentages computed from BSE's official closes against Wednesday):"),
    chart(movers_chart()),
    p(" The verdict is a rotation within India, not a risk-off. The two ends of the board tell it: Eicher (+4.73%%) led the tracked names on the auto trade - Maruti Suzuki, outside this board, rose 7.58%% for its best day in fifteen months, the Nifty Auto index up nearly 4%% with all fifteen members green, as aluminium and copper fell up to 21%% in recent days and the market started pricing the margin relief that should reach the profit line by the fourth quarter (%s). The red end is IT: HCL Tech, Wipro, Tata Communications, and beyond the board TCS (-1.41%%), Tech Mahindra (-1.38%%) and Infosys (-1.66%%), the Nifty IT index down 1.10%% - the read-across from Wall Street's six-day AI selloff, arriving by wire. The realty trio barely moved. Note the honest wrinkle: Ashok Leyland (+2.37%%) and Oil India (+0.46%%) both have dividend record dates today, so part of their bid is positioning, not verdict - the same caveat this paper applied to Wednesday's movers, run the other way." % a(MARUTI_TV18,'CNBC-TV18')),
]})

# 5 - Corporate actions
groups.append({'heading': 'Corporate actions', 'blocks': [
    p(" Record dates today: Ashok Leyland's interim, Oil India's Rs 7, BF Investment's Rs 20 and Venus Pipes' Re 0.50, plus Medi Assist's buyback record date (%s). Muthoot Microfin's board met for ten minutes Thursday and approved audited special-purpose half-year financials - the paperwork that feeds restated consolidated financials for the proposed IPO of its holding company, Muthoot Fincorp; a step in the parent's listing file, not fresh results (%s). And the margin-rule story paused where it started: SEBI chairman Tuhin Kanta Pandey says a committee discussed linking margin-funding limits to free float and took no decision - a report, a meeting, and no rule (%s)." % (a(ET_CORP,"the week's calendar"), a(MUTHOOT,'the outcome'), a(SEBI_MC,'moneycontrol'))),
]})

# 6 - Finance Goldmine
groups.append({'heading': 'Finance Goldmine', 'blocks': [
    p(" Fourteen sessions, one record. Foreign investors bought a provisional Rs 7,411.41 crore of Indian equities on Thursday - bought Rs 20,707 crore, sold Rs 13,296 crore - stretching the buying streak to fourteen sessions and November's haul past Rs 1.01 lakh crore, the biggest month of foreign buying on record, over $13 billion; domestic institutions sold Rs 1,356.57 crore (%s; %s). The handoff this paper flagged Wednesday is now the month's defining fact: foreign money is buying the highs that domestic money sells into. The last time ownership rotated like this, the rupee told you first - it closed at a seven-month high of 93.29 on Thursday (%s)." % (a(FII_TV18,'CNBC-TV18'), a(FII_FE,"FE's flow data"), a(RUPEE_MC,'moneycontrol'))),
    p(" One term worth owning: the greenshoe. When an IPO is heavily oversubscribed, underwriters hold an over-allotment option - Anthropic's is 147 million shares on top of the 980 million sold - letting them sell 15% more stock and buy it back in the market if the price wobbles. The mechanics matter this week: if ANT trades above the $83 print, the banks exercise the option and pocket the spread; if it sags toward $83, they become the buyer of last resort, and their buying is what stabilizes a debut. The option lasts thirty days, which is why the first month of a big listing trades differently from every month after: there is a bidder with a mandate underneath it. Watch where ANT closes its second session tonight - every close above $83 keeps the greenshoe theoretical." ),
]})

# 7 - Startup Intelligence
groups.append({'heading': 'Startup Intelligence', 'blocks': [
    p(" Thursday's cheques. InPrime Finserv raised $10.7 million in a Series B led by FMO, the Dutch development bank, to keep lending to India's informal micro-entrepreneurs (%s). VitusCare raised Rs 30 crore in a Series B to expand its dialysis-centre network and build AI-assisted care tooling (%s). From Wednesday's global file, now verified: Boltz, the Boston molecular-design lab, raised $110 million to speed small-molecule drug work with its open-source structure-prediction models (%s). The pattern across the three: picks-and-shovels cheques - credit rails, clinics, and drug-design infrastructure - while the application layer hogs the headlines." % (a(INPRIME,'ET'), a(VITUS,'Business Standard'), a(BOLTZ,'SiliconANGLE'))),
    p(" Today's startup idea: the free-float leverage map. SEBI's committee has now admitted it is debating a cap on margin funding tied to each stock's free float - and taken no decision. Whoever builds the map first owns the conversation: a public dashboard that takes BSE's daily bhavcopy and shareholding patterns, estimates each stock's margin-funded book against its free float, and flags the fifty names where a 5-10% cap would force the most unwinding. The data is free but incomplete - no consolidated margin book is public, so the product is an honest estimate with the methodology printed, not a false precision machine. The buyers are the brokers themselves, who will need the analysis the day a consultation paper drops, and the financial press, who will cite the map either way. Distribution first, subscription second." ),
]})

# 8 - AI Race
groups.append({'heading': 'AI Race', 'blocks': [
    p(" OpenAI published its own telemetry. Two progress reports this week, both on its own blog. First: internal agents now complete 46%% of research tasks estimated at two-to-four hours of human work, up from 23%% in March - and 35%% of four-to-eight-hour tasks, up from 13%% - with the success rate wildly uneven by task type: 79%% for monitoring training runs, 35%% for launching them, 25%% for writing inference code. The median researcher's daily agent usage hit $2,400 at list prices in October, up 62%% in a month; asked what they would trade to keep frontier coding agents for three months, researchers offered a median 30%% of team compute or 40%% of team headcount (%s). Second: the models are now measurably improving the chips they run on - one multiplier redesign on the in-house Jalapeño inference chip used about 15%% less silicon area and cut latency from two clock cycles to one, with the same method now being applied to AMD hardware and folded into Synopsys's design tools (%s). Read the two together: the users automating the most are the people building the thing itself, and they are paying list price to do it. That is either what a productivity tool looks like on the inside, or what a bubble's engine room looks like - the telemetry does not say, and neither does this paper." % (a(OAI_JAGGED,'the autonomy post'), a(OAI_CHIP,'the chip post'))),
]})

# 9 - Vibe coding
groups.append({'heading': 'Vibe coding', 'blocks': [
    p(" The factory is the unit now. OpenAI's third engineering post of the week describes the Performance Factory, the Codex-powered system that keeps ChatGPT fast: an alert fires, an agent investigates, records findings, proposes a fix for human review, and a second agent verifies the recovery after deployment. In just over three months the first workflow ran more than 1,700 investigations and root-caused over 600 regressions - seventeen automated investigations a day, with engineers reviewing fixes rather than hunting them (%s). The post's honest progression is the lesson: manual debugging, then Codex as a partner, then a shared investigation skill, then a human copying alerts into the agent, then no human in the loop at all. The skill that survives automation is writing the workflow and reviewing its output - the engineers in this story did not become faster debuggers; they became editors of a debugging machine. That is the career move hiding in every 'agents are coming' headline this week." % a(OAI_FACTORY,'the post')),
]})

# 10 - Try this today (Friday)
groups.append({'heading': 'Try this today (Friday)', 'blocks': [
    p(" Hand the books to the machine, carefully. OpenAI launched ChatGPT for Accounting this week: an accounting plugin plus computer use that delegate invoice processing, reconciliation and draft reporting across the tools a finance team already runs, with human review written into the setup (%s). The honest test for a Friday afternoon: take ten invoices or one bank statement and have it draft the reconciliation, then check every line yourself. The point is not whether it saves you an hour; it is learning where your review has to live before you trust it with a quarter. If your workspace has not enabled the plugin, the setup guide on the same page is the read." % a(OAI_ACCT,"OpenAI's page")),
    p(" Then, a spectator skill: read an opening cross. ANT trades its second session tonight. When a big IPO's stock first opens, the opening cross - the auction that matches the overnight orders into one print - tells you who actually showed up: a strong cross with follow-through means real books; a spike that fades in the first hour means the flippers got filled. Thursday's tape was the second kind of open ($111.50 to $97.17) wrapped in the first kind of demand (846 million shares, a record). Both things happened; watch which one repeats tonight. The tape is free on any market site; the vocabulary is above." ),
]})

# 11 - One concept
groups.append({'heading': 'One concept: the winner\u2019s curse', 'blocks': [
    p(" The winner's curse, and why the person who got the biggest allocation should worry. The idea comes from auction theory: when bidders value the same thing differently and nobody knows the true value, the winner is systematically the bidder whose estimate was most optimistic - so winning is itself bad news about your valuation. In IPOs it works through allocation rather than price: in a hot book your order gets rationed to a sliver, but in a cold book you get every share you asked for - which means your fill rate is highest precisely in the deals you least wanted. Rock's 1986 paper built the logic into IPO pricing itself: issuers underprice to keep uninformed investors bidding, because the informed only show up for the discounts. Thursday gave the concept a live specimen. An $81.3 billion book went thirty-something times covered, everyone got rationed, the stock opened 34% up - and then faded all afternoon. The investors celebrating the smallest allocations may have been dealt the kindest hand. The discipline: in a rationed market, treat getting exactly what you asked for as information, not luck." ),
]})

# 12 - Setup board
groups.append({'heading': 'Setup board', 'blocks': [
    p(" Thursday's session is scored, and nothing resolved. The board's four watchlist names all moved with the tape - JSW Steel had the day of the group, up 1.72% to close at its high of 1,334.00 - and not one line changed state: no stop, no target, no invalidation, and no watchlist name newly clears the published screen. The session's lesson arrived elsewhere: Infosys, invalidated Wednesday at the 1,120 close-based floor, kept falling - 1,090.55 at the close after printing 1,072.60 intraday. The rule did exactly what a floor is for."),
    chart('<p style="color:#64748b;font-size:13px">Open lines after Thursday\'s session (BSE official closes): <b>Kotak Mahindra Bank</b> 500.60 (+1.15%) - trigger holds, 18th session above 437.55 (day\'s low 491.90); stop far away at 420. <b>ONGC</b> 224.50 (-0.16%) - sixth session below the 228 breakout line; coil floor 218.50 intact. <b>JSW Steel</b> 1,334.00 (+1.72%, closed at the high) - now ~36 points from the 1,370 target, but the risk-reward at worst fill is still about 0.2 to 1 against the 1,158.95 floor: fails the screen. <b>Hindalco</b> 909.00 (+0.96%) - gap-down open at 881, a 28-point recovery to the underside of the 911-912 zone it broke Wednesday; still no verified entry zone. <b>Shelved:</b> Voltas (rejected) jumped 9.09% to 1,235.00 - a one-day surge changes nothing while the screen has not re-cleared it; Tech Mahindra 1,723.00 stays above the 1,500 cap.</p>'),
    chart(ongc_chart()),
    p(" The ledger is unchanged: HCLTech, filled 28 October at the worst fill of Rs 1,378.00, target Rs 1,466.80 taken out at 1,468.00 - gross +6.53%, net +6.23% after the 0.3% cost convention - closed Thursday at Rs 1,331.60. Infosys sits in the resolved column by invalidation, no trade, no P&L - and two sessions of follow-through say the floor rule earned its place. Research, not advice; cash-only swing setups under Rs 1,500 a share; BSE official prints are the standard."),
]})

# 13 - How the board scores
groups.append({'heading': 'How the board scores', 'blocks': [
    rows([
        row(1, 'No prior-day stop trade', 'A setup activates only if the zone fills before any prior-day trade at or below the stop; a stop touched first kills the line before entry.'),
        row(2, 'Worst fill in the zone', 'Entry is assumed at the worst price inside the published zone, not the best.'),
        row(3, 'R:R on the worst fill', 'Reward-to-risk is computed from the worst fill to the published stop and target; lines that fail stay on the watchlist, not the board.'),
        row(4, 'Resolution only', 'A line leaves the board only by stop, target or invalidation - never by opinion.'),
    ]),
]})

# 14 - Editor's read
groups.append({'heading': "The editor's read", 'blocks': [
    p(" The record book and the losing streak are the same story. It is tempting to pick one: either Anthropic's 17% debut proves the AI trade lives, or the S&P's sixth straight loss proves it is dying. The honest read is that both are the same repricing seen from two sides. Public-market money is not leaving AI - it just paid $97 for something it could have had at $83 twelve hours earlier, while selling the incumbents to make room. That is rotation inside the theme, with the risk budget shrinking as it rotates: Nvidia down six straight sessions, AMD on a short report, the indexes at their lows the moment the new supply opened. Ellerbroek's line deserves the last word on causation: money making room for Anthropic moves prices without saying anything about demand. What the day actually settled is narrower and more useful: the largest listing in history can clear in a falling market. The demand exists. The price of everything else is the argument."),
    p(" Also brewing - the rate file. Cause chain: the October minutes said most participants expect more hikes; the dollar and gold have since voted, gold to a fourteen-month low; markets now fully price a December hike. What settles it: the December meeting itself, and any speaker who blinks first. The ten-year falling to 5.04% on a hike-pricing day is the wrinkle to hold - fear is outbidding the repricing."),
    p(" Also brewing - the chip file. Cause chain: the remote-access rule was released Monday, took effect Thursday, comments open to 19 January; Reuters reported Nvidia had already stopped shipping licensed chips to China; a short seller put AMD's China exposure on the tape the same day. What settles it: whether any of the three - BIS, Nvidia, AMD - puts a revenue number on the halt. Watch Nvidia's next filing for the China line."),
    p(" Also brewing - the divergence file. Cause chain: fourteen straight sessions of foreign buying, a record November, a seven-month-high rupee, and a Sensex within touching distance of its record - while Wall Street posts its worst week since April. What settles it: today's open. GIFT Nifty's derived quote was already 0.37% lower last night; if Mumbai holds its gains through the US hangover, the divergence is a story with legs, not a day."),
]})

# 15 - The week ahead
groups.append({'heading': 'The week ahead', 'blocks': [
    rows([
        row(1, 'Fri 20 Nov (today)', "Record dates: Ashok Leyland's interim, Oil India's Rs 7, BF Investment's Rs 20, Venus Pipes' Re 0.50, plus Medi Assist's buyback record date; Mahanadi Coalfields day two; ANT's second session tonight in New York."),
        row(2, 'Mon 23 - Fri 27 Nov', 'Mahanadi closes Monday, allotment Wednesday, listing Friday (tentative); the BIS rule comment docket (BIS-2026-0628) builds toward its 19 January deadline.'),
        row(3, 'Watching', "Fed speakers into the December meeting with a hike fully priced; Nvidia's next filing for the China revenue line; SEBI's MTF committee after the chairman's no-decision; whether ANT's greenshoe stays theoretical."),
    ]),
]})

# 16 - Notes
groups.append({'heading': 'Notes on this edition', 'blocks': [
    bullets([
        "Sources read for this edition: CNBC, AP, UPI and Reuters for the ANT debut and the US close; Dow Jones' data wire for the Nasdaq level; Business Standard and BusinessLine for the Mumbai close; CNBC-TV18 and FE for flows (provisional, NSE-published figures via the press); moneycontrol for the rupee; the Federal Register's published rule text; Reuters for Nvidia's China halt; CNBC for AMD; CNBC and Kitco for gold; the US Treasury's own daily yield curve; Newsquawk and Reuters for the oil settle; Mint and upstox for the Mahanadi book; OpenAI's own engineering posts; BSE's official bhavcopy for every Indian price. Marker values are as-of their stamps (5:50-6:00 AM IST) and will move before the open.",
        "The claim that ANT is the largest listing ever at pricing and the seventh-most-valuable US company are the wires' and CNBC's framings respectively; the first-day share-volume comparison to SpaceX is CNBC's. Index levels are final closes. The gold figures distinguish Thursday's spot close ($3,650.12) from the December futures settle (near $3,651); intraday prints differ from settles. The S&P's sixth straight loss is its longest streak since 2024 per AP; the weekly-worst-since-April framing is Reuters', stated as on-course, not final. Hunterbrook's AMD claims are allegations by an interested short seller and are reported as such; AMD denies them.",
    ]),
    closing(" The biggest listing in history cleared on the worst week since April; Mumbai bought the divergence. See you tomorrow."),
]})

ed['groups'] = groups
out = {'day': 46, 'meta': {'date': 'Friday 20 November 2026', 'short': 'Fri 20 Nov', 'longread': 46}, 'edition': ed, 'audio': {}, 'times': {}}
json.dump(out, open('/downloads/morning-paper/editions-src/day-46.json','w'), indent=1, ensure_ascii=False)
print('day-46.json written,', len(groups), 'groups')
