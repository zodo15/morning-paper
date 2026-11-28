#!/usr/bin/env python3
"""Build editions-src/day-54.json for Saturday 28 November 2026, mirroring Ed53's 13-group shape (section pause in force)."""
import json, datetime

for y, m, dd, wd in [(2026, 11, 27, 'Friday'), (2026, 11, 28, 'Saturday'), (2026, 11, 29, 'Sunday'), (2026, 11, 30, 'Monday'),
                     (2026, 12, 1, 'Tuesday'), (2026, 12, 2, 'Wednesday'), (2026, 12, 3, 'Thursday'), (2026, 12, 4, 'Friday')]:
    assert datetime.date(y, m, dd).strftime('%A') == wd, (y, m, dd)

def p(html):
    return {"t": "p", "html": html}

def A(url, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)

A_HIND = A('https://www.thehindu.com/business/markets/stock-markets-snap-two-day-rally-sensex-tanks-989-points-amid-profit-booking/article71750358.ece', "The Hindu's close report")
A_HBL = A('https://www.thehindubusinessline.com/markets/sensex-sheds-989-points-as-crude-rupee-end-four-week-nifty-rally/article71750532.ece', "Hindu BusinessLine's close report")
A_ETW = A('https://economictimes.indiatimes.com/markets/stocks/news/market-wrap-bel-jsw-steel-shriram-finance-bajaj-auto-top-gainers-and-losers-on-nifty-and-sensex-on-friday/articleshow/136221692.cms', "the Economic Times market wrap")
A_BSE = A('https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_20261127_F_0000.CSV', "BSE's official bhavcopy")
A_TV18 = A('https://www.cnbctv18.com/market/fiis-infuse-nearly-%E2%82%B917630-crore-in-4-days-even-as-nifty-snaps-four-week-rally-20043283.htm', "CNBC-TV18's provisional tally")
A_MAHA = A('https://www.cnbctv18.com/market/mahanadi-coalfields-mcl-coal-india-subsidiary-listing-ipo-subscription-financials-production-offtake-dividends-share-price-20042647.htm', "CNBC-TV18's listing report")
A_THEHINDU_HC = A('https://www.thehindu.com/business/bombay-high-court-gives-go-ahead-for-tata-sons-board-meeting-on-november-30/article71752235.ece', "The Hindu's court report")
A_BB = A('https://www.barandbench.com/news/no-relief-for-tata-trusts-as-bombay-high-court-refuses-to-halt-tata-sons-november-30-board-meeting', "Bar and Bench's hearing report")
A_LL = A('https://www.livelawbiz.com/company-law/high-court/bombay-high-court-denies-interim-relief-to-tata-trusts-allows-november-30-tata-sons-board-meeting-560330', "LiveLaw's hearing report")
A_IE = A('https://indianexpress.com/article/business/tata-trusts-seek-65-crore-damages-tata-sons-10979529/', "The Indian Express")
A_NDTV = A('https://www.ndtvprofit.com/business/tata-trust-vs-tata-trust-tata-sons-says-deferring-nov-30-meet-will-breach-dec-10-rbi-listing-deadline-12385449', "NDTV Profit")
A_HT = A('https://www.hindustantimes.com/business/tata-sons-adds-six-month-ipo-timeline-to-board-meet-agenda-101795654777767.html', "Hindustan Times reported")
A_LAT = A('https://www.latimes.com/business/story/2026-11-27/stocks-jump-to-close-out-erratic-week-that-was-also-wall-streets-best-in-more-than-year', "the Los Angeles Times' close report")
A_AP = A('https://apnews.com/article/wall-street-stocks-dow-nasdaq-04dab6079cf7f3dfe7285a3cc1f240a2', "AP's close report")
A_BLOOM = A('https://www.bloomberg.com/news/articles/2026-11-27/anthropic-shares-jump-after-volatile-first-week-since-record-ipo', "Bloomberg")
A_SA = A('https://stockanalysis.com/news/anthropic-jumps-11-percent-back-above-ipo-price/', "stockanalysis.com's close report")
A_CNA = A('https://www.channelnewsasia.com/business/oil-notches-first-weekly-gain-in-november-supply-fears-6586546', "Reuters' settlement report")
A_MORN = A('https://www.morningstar.com/news/dow-jones/202611274508/comex-gold-ends-the-week-353-higher-at-363960-data-talk', "Dow Jones' Comex settlement report")
A_RTHK = A('https://news.rthk.hk/rthk/en/component/k2/1879502-20261127.htm', "RTHK's close report")
A_KAB = A('https://en.kabutan.com/jp/news/n202611270807', "Kabutan's Tokyo close report")
A_YNA = A('https://en.yna.co.kr/view/AEN20261127004852320', "Yonhap's Seoul close report")
A_INV = A('https://www.investing.com/news/stock-market-news/european-stocks-extend-recovery-as-tech-miners-advance-5053129', "Investing.com's European close report")
A_PIB = A('https://www.pib.gov.in/MediaInvitationDetail.aspx?InvitationID=159438&lang=1&reg=3', "PIB's media invitation")
A_CM = A('https://www.capitalmarket.com/markets/news/live-news/week-ahead-rbi-decision-us-jobs-data-in-focus/1752383', "Capital Market's week-ahead note")
A_TM = A('https://exchangecirculars.com/circulars/bse/2026/bse-2026-11-26-c041fb4df84358f2-bonus-issue-of-tech-mahindra-limited-scrip-code-532755/', "the BSE circular")
A_TMET = A('https://economictimes.indiatimes.com/markets/stocks/news/tech-mahindra-announces-record-date-for-11-bonus-issue-check-details/articleshow/136097664.cms', "the Economic Times")
A_RBI = A('https://www.rbi.org.in/scripts/bs_pressreleasedisplay.aspx/BS_PressReleaseDisplay.aspx?prid=63742', "the RBI's own policy statement")
A_RBIS = A('https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2752', "the RBI's published meeting schedule")
A_UPS = A('https://upstox.com/news/market-news/ipo/matangi-rubber-ipo-opens-dec-1-check-price-band-lot-size-and-key-dates/article-203857/', "Upstox")
A_MCSW = A('https://www.moneycontrol.com/news/business/ipo/diaper-maker-swara-baby-products-to-open-rs-800-crore-ipo-on-dec-2-sets-price-band-at-rs-105-111-14089909.html', "Moneycontrol's report on Swara Baby Products")
A_MCMO = A('https://www.moneycontrol.com/news/business/ipo/monomark-engineering-sets-ipo-price-band-at-rs-60-65-rs-175-5-crore-issue-to-open-on-december-2-14088405.html', "Moneycontrol's report on Monomark Engineering")
A_FCC = A('https://docs.fcc.gov/public/attachments/DA-26-1273A1.txt', "the FCC's own order")
A_CNBCSX = A('https://www.cnbc.com/2026/11/25/spacex-fcc-satellite-approval.html', "CNBC")
A_NV = A('https://techcrunch.com/2026/11/26/nvidia-hits-pause-on-chip-shipments-to-southeast-asia/', "TechCrunch, citing the Wall Street Journal,")
A_CAI = A('https://oag.ca.gov/news/press-releases/attorney-general-bonta-opposes-asset-sale-characterai-amid-child-safety-concerns', "California Attorney General's release")
A_YS = A('https://yourstory.com/2026/11/weekly-funding-roundup-nov-21-27-vc-inflow-dips-on-modest-deal-activity', "YourStory's weekly roundup")
A_CNBCG = A('https://www.cnbc.com/2026/11/27/gold-metals-silver-markets-federal-reserve.html', "CNBC")
A_DARDEN = A('https://www.darden.virginia.edu/effectuation', "UVA Darden")
A_SARA = A('https://cdn.mises.org/sarasvathy_2001_causation_and_effectuation.pdf', "Saras Sarasvathy's 2001 paper in the Academy of Management Review")
A_TCS = A('https://www.tcs.com/who-we-are', "TCS's own site")

lead = [
 p("China's national team steps in. Mainland stocks had their largest gains in more than two years on Friday after Beijing vowed to strengthen the role of the state-backed \"national team\" in steadying the market: the Shanghai Composite rose 3.73% to 3,606, the Shenzhen Component 7.24% to 10,814 and the ChiNext 11.61% to 2,443, while the Hang Seng gained 2.1% to 22,694 (" + A_RTHK + "). Tokyo and Seoul joined in: the Nikkei rose 2.11% to 58,711.11 (" + A_KAB + ") and the Kospi 4.34% to 4,915.68 (" + A_YNA + ")."),
 p("Wall Street closed a big week higher. In a shortened session that ended at 1 PM ET, the S&P 500 rose 114.71 points (1.6%) to 7,297.49, the Dow 591.99 (1.2%) to 50,774.94 and the Nasdaq 543.70 (2.3%) to 24,129.50; the S&P gained 5.6% on the week, its best since April 2025 (" + A_LAT + "). The 10-year Treasury yield stood at 4.94%."),
 p("Anthropic's best close since debut. The shares closed at $91.88, up about 11%, back above the $83 IPO price and the highest close since the 19 November debut (" + A_BLOOM + "; " + A_SA + ")."),
 p("Mumbai's last session of the week fell. The Sensex dropped 989.33 points (1.17%) to 83,339.26 and the Nifty 277.30 (1.07%) to 25,607.20, ending a four-week rally; for the week the Nifty lost 0.75% and the Sensex 0.69% (" + A_HBL + "). IT, auto and financial services each fell more than 1%, and TCS shed 2.46% on BSE. Foreign investors still bought for a nineteenth straight session, a provisional Rs 1,634.33 crore (" + A_TV18 + ")."),
 p("The court said no. The Bombay High Court refused the Tata trusts interim relief on Friday, so the Tata Sons board meeting on Monday goes ahead; Justice Abhay Ahuja said whatever it decides is \"subject to our final orders\", and ordered replies from Tata Sons and six directors (" + A_THEHINDU_HC + "). The two plaintiffs, the Sir Dorabji Tata Trust and the RD Tata Trust, are asking the court to void the 17 September reappointment of N. Chandrasekaran. The next hearing is in January 2027."),
 p("Mahanadi listed below its price. The Coal India arm opened on BSE at Rs 133.15, hit a high of 137.85 and a low of 130.70, and closed at Rs 132.60 against its Rs 136 issue price, down 2.5% (" + A_BSE + ")."),
 p("Oil and gold. Brent settled at $95.44 a barrel, down $1.13 on the day but up about 3% on the week, its first weekly gain in November (" + A_CNA + "). Comex gold for December settled at $3,639.60, up $103.80 or 2.94%, and finished the week 3.53% higher (" + A_MORN + ")."),
 p("SpaceX's licence, read carefully. The FCC granted SpaceX a licence, in part, for up to one million Starmind data-centre satellites. The grant covers the satellites' backup radio links; disposal plans for anything above 600 km are deferred, and the first satellite is due by 25 November 2033 (" + A_FCC + "). Nothing has launched under it."),
 p("What to watch. There is no Indian session today; the next is Monday. Sunday brings the OPEC+ meeting. Monday brings the Tata Sons board meeting, India's second-quarter GDP print at a 4:30 PM press conference (" + A_PIB + ") and the record date for Tech Mahindra's bonus issue. The Reserve Bank's rate meeting runs 2 to 4 December."),
]

front = [
 p("What the court did, and did not do. Justice Ahuja declined to stop the board meeting but said its outcome is subject to the court's final orders; Tata Sons argued that deferring the meeting would breach a Reserve Bank listing deadline, and reports differ on the date, so none is printed here (" + A_NDTV + "; " + A_BB + "). Salve appeared for Tata Sons and Singhvi for the Sir Dorabji Tata Trust (" + A_LL + "). The trusts claim Rs 65 crore in damages with 18% interest: Rs 50 crore from the Sir Dorabji Tata Trust and Rs 15 crore from the RD Tata Trust (" + A_IE + "). Tata Sons' counsel said a listing could come by autumn 2027 if the case goes smoothly. Hindustan Times reported that Monday's agenda includes a six-month timeline for a Tata Sons public offering and options for the Shapoorji Pallonji group's 18.4% stake (" + A_HT + ")."),
 p("China's rally in detail. RTHK describes the \"national team\" as state-backed investors, usually led by Central Huijin, the domestic unit of the sovereign wealth fund China Investment Corp, who are often buyers at times of market stress. The Hang Seng's turnover was HK$257.14 billion; its tech index jumped 6.5% to 3,637; the Shanghai Composite, which had been lingering near 17-month lows, closed at 3,606 on turnover of 929.77 billion yuan; and the Star semiconductor index jumped by a near-record 19.5% (" + A_RTHK + "). RTHK quotes Bank of America's Winnie Wu saying that with very depressed valuations and consensus bearishness on China tech, it does not take much for a relief rally."),
 p("Wall Street's week. The Nasdaq gained 2.3% in the half session, with Broadcom up 3.8%, Amazon up 4% and Nvidia up 0.8%. The 10-year yield was 4.94%, against 4.85% on Wednesday (" + A_AP + "). The S&P's 5.6% weekly gain was its best since April 2025."),
 p("Anthropic's week. Bloomberg reports the shares rose nearly 11% to $91.88 after two straight closes below $83. stockanalysis.com records a Wednesday close of $82.79 after an intraday low of $73.85, and a debut-day close of $97.17 on 19 November (" + A_BLOOM + "; " + A_SA + ")."),
 p("Inside the Indian fall. Midcaps and smallcaps held up: the Nifty Midcap 100 rose 0.10% and the Smallcap 100 0.56%, while Nifty Metal gained 1.40% (" + A_HBL + "). The Bank Nifty slipped 494.40 points (0.78%) to 63,040.90. On NSE, 2,119 stocks advanced and 1,514 declined (" + A_ETW + "). One broker's technical note, attributed to HST Wealth, says the Nifty broke below Thursday's doji low after repeated rejection near 26,000, with support at 25,400 and resistance at 25,750; those are that analyst's levels, not this paper's."),
 p("Mahanadi's mechanics. The listing sold shares held by Coal India: an offer for sale of 66.18 crore shares at Rs 136, or Rs 9,000 crore, subscribed 1.52 times, with Coal India selling 10%. At Rs 136 the company's 6,618,363,000 shares come to about Rs 90,000 crore. Financial year 2026 revenue was Rs 29,854 crore and earnings per share Rs 16.13, so the issue price is about 8.4 times earnings (" + A_MAHA + "). BSE volume on debut day was 8,316,367 shares. One outlet's report of a 2% premium is wrong; BSE's own prints show a discount."),
 p("Oil's reasons and OPEC+'s date. Reuters attributes the week's gain to tanker attacks in the Strait of Hormuz and a partly halted Jazan refinery in Saudi Arabia; OPEC+ meets on Sunday and is expected to hold its first-quarter 2027 targets, an expectation, not a decision (" + A_CNA + ")."),
 p("Gold's reversal. Spot gold dipped under $3,500 on Wednesday for the first time since September 2025 (" + A_CNBCG + "), and Comex gold's Friday settlement of $3,639.60 is $103.80 higher on the day (" + A_MORN + ")."),
 p("Europe's gain. The STOXX 600 rose about 1% to 643.85 and was up roughly 3% on the week (" + A_INV + ")."),
]

markets = [
 p("US, Friday (half session): S&P 500 7,297.49 (+1.6%), Dow 50,774.94 (+1.2%), Nasdaq 24,129.50 (+2.3%); 10-year yield 4.94% (" + A_LAT + ")."),
 p("Asia, Friday: Nikkei 58,711.11 (+2.11%), Kospi 4,915.68 (+4.34%), Hang Seng 22,694 (+2.1%), Shanghai 3,606 (+3.73%), Shenzhen Component 10,814 (+7.24%), ChiNext 2,443 (+11.61%) (" + A_RTHK + "; " + A_KAB + "; " + A_YNA + ")."),
 p("India, Friday: Sensex 83,339.26 (-1.17%), Nifty 25,607.20 (-1.07%), Bank Nifty 63,040.90 (-0.78%). FII net +Rs 1,634.33 crore, a nineteenth straight buying session (bought Rs 14,259.45 crore, sold Rs 12,625.12 crore); DII net -Rs 556.42 crore (" + A_HBL + "; " + A_TV18 + ")."),
 p("Europe, Friday: STOXX 600 643.85 (+1%) (" + A_INV + ")."),
 p("Commodities: Brent $95.44 (-$1.13); WTI $83.08; Comex gold (December) $3,639.60 (+$103.80) (" + A_CNA + "; " + A_MORN + ")."),
]

ipos = [
 p("Mahanadi Coalfields debuted at a discount. On BSE it opened at Rs 133.15 (-2.1% against the Rs 136 issue price), ranged from 130.70 to 137.85 and closed at Rs 132.60 (-2.5%) on 8,316,367 shares (" + A_BSE + "; " + A_MAHA + ")."),
 p("Next week's issues. Matangi Rubber's Rs 125.16 crore issue runs 1 to 3 December at Rs 163 to 172 a share (" + A_UPS + "). Swara Baby Products' issue of about Rs 800 crore opens 2 December at Rs 105 to 111 (" + A_MCSW + "), and Monomark Engineering's Rs 175.5 crore issue opens the same day at Rs 60 to 65 (" + A_MCMO + ")."),
]

# Friday movers bar chart (BSE bhavcopy % changes). Baseline x=440, 40 px per 1%.
bars = [("BEL", 1.56), ("JSW Steel", 1.30), ("Hindalco", 0.95), ("ONGC", 0.52), ("Kotak Bank", -1.76), ("TCS", -2.46), ("Bajaj Auto", -2.56), ("HCL Tech", -2.81), ("Shriram Finance", -4.00)]
BASE, SC = 440, 40.0
h = 14 + 48 * len(bars) + 10
svg = '<svg viewBox="0 0 760 %d" role="img" aria-label="Leaders and laggards among the large names this paper tracks, Friday 27 Nov (%% vs Thursday close), BSE official prints">' % h
for i, (n, v) in enumerate(bars):
    y = 30 + 48 * i
    w = round(abs(v) * SC, 1)
    col = '#15803d' if v > 0 else '#b91c1c'
    svg += '<text x="8" y="%d" font-size="21" fill="#334155">%s</text>' % (y + 17, n)
    if v > 0:
        svg += '<rect x="%d" y="%d" width="%s" height="26" fill="%s" rx="3"/><text x="%s" y="%d" text-anchor="start" font-size="20" fill="%s">+%.2f%%</text>' % (BASE, y, w, col, round(BASE + w + 0, 1), y + 19, col, v)
    else:
        svg += '<rect x="%s" y="%d" width="%s" height="26" fill="%s" rx="3"/><text x="%s" y="%d" text-anchor="end" font-size="20" fill="%s">%.2f%%</text>' % (round(BASE - w, 1), y, w, col, round(BASE - w - 7, 1), y + 19, col, v)
svg += '<line x1="%d" y1="14" x2="%d" y2="%d" stroke="#94a3b8" stroke-width="1"/></svg>' % (BASE, BASE, h - 20)
movers_chart = {"t": "chart", "svg": svg}

movers = [
 p("Friday's verdicts. The index fell on IT, autos and financials: HCL Technologies -2.81% to 1,423.80, TCS -2.46% to 2,575.00, Bajaj Auto -2.56% to 10,562.00, and Shriram Finance the session's worst at -4.00% to 924.50. Against it, defence and metals: Bharat Electronics +1.56% to 411.10 and JSW Steel +1.30% to 1,322.00, with Titan +0.95% (4,674.80), IndiGo +0.50% (5,655.00), Tata Steel +0.46% (164.10), Power Grid +0.37% (268.00) and Trent +0.23% (3,270.10) all up (" + A_BSE + "; " + A_ETW + ")."),
 movers_chart,
 p("The paper's own names. Hindalco rose 0.95% to 923.75, ONGC 0.52% to 224.20 and Kotak Mahindra Bank fell 1.76% to 500.05; Infosys closed at 1,152.00 (-2.55%), Voltas at 1,191.00 (-2.54%) and Tech Mahindra at 1,815.00 (-2.15%). Asian Paints fell 0.42% to 2,532.25. All are BSE official closes (" + A_BSE + "). TCS, down 2.46% on the day, is today's long read."),
]

corp = [
 p("Tech Mahindra's bonus. The company's 1:1 bonus issue has Monday 30 November as its record date: shareholders on record receive one extra share for each share held (" + A_TM + "; " + A_TMET + ")."),
 p("The week in startup money. YourStory counts $171 million of venture funding across 13 deals this week, down from $255 million the week before. The larger rounds: Finnable raised Rs 405 crore (about $43.7 million), Green Aero $14 million, and Matters.AI about Rs 115 crore ($12 million) (" + A_YS + ")."),
]

gold = [
 p("Term of the day: bonus issue. A company converts part of its reserves into new shares and hands them to existing shareholders free, in a stated ratio. In a 1:1 bonus every holder gets one new share per share held, so the share count doubles; the company's value does not change, so the price per share is adjusted down to match. Nothing is paid and nothing is received that was not already owned; the holder's stake in the company is exactly what it was. Tech Mahindra's record date is Monday (" + A_TM + ")."),
 p("Reading a streak. The foreign-investor streak has now run nineteen sessions. Summed from the daily provisional prints, foreigners bought Rs 17,630 crore over four sessions this week (+5,672.99, +4,479.08, +5,843.33 and +1,634.33 crore), while domestic institutions swung between buying and selling and net-bought about Rs 6,333 crore over the same four days (" + A_TV18 + "). On Friday the two sides split: foreigners bought Rs 1,634.33 crore while domestic institutions sold Rs 556.42 crore, and the Nifty fell 1.07% anyway."),
 p("What a \"national team\" is. In China it is the market's nickname for state-backed investors, usually led by Central Huijin, the domestic unit of the sovereign wealth fund China Investment Corp, who tend to buy when markets are under stress (" + A_RTHK + ")."),
]

ai = [
 p("The licence behind the headline. The FCC's order, adopted and released on 25 November, says it grants authority for radio communications for backup and emergency telemetry, tracking and command for a constellation of up to one million satellites to operate as data centres in space. It does not license the computing. Disposal of satellites above 600 km is deferred, and the first satellite is due by 25 November 2033 (" + A_FCC + "). Amazon, Viasat and AAS had petitioned to deny (" + A_CNBCSX + ")."),
 p("Nvidia's shipping pause. Nvidia told Dell and Super Micro to pause server shipments to Malaysia, Singapore, Thailand and Indonesia for an unspecified period while it checks that its partners meet US export rules (" + A_NV + " reports)."),
 p("Character.AI's auction. The bankrupt chatbot company's platform and its chat records from more than 21 million US accounts go to auction on 1 December; a coalition of 42 state attorneys general has asked the court to block the sale and also opposes a $350,000 breakup fee (" + A_CAI + ")."),
]

concept = [
 p("In a 2001 paper in the Academy of Management Review, Saras Sarasvathy described a way expert entrepreneurs decide that she called effectuation. Instead of picking a goal and then gathering the resources to reach it, an effectual entrepreneur starts from what is already at hand - who they are, what they know and whom they know - and builds toward whatever the available means allow (" + A_SARA + "; " + A_DARDEN + "). One of her principles is the affordable loss: risk only what you can afford to lose. It fits how today's long read starts: TCS began as a shared computing room for Tata companies, and the export business came later."),
]

setup_lines = """<p style="color:#64748b;font-size:13px">Open lines, BSE official closes, Friday 27 November: <b>Kotak Mahindra Bank</b> 500.05 (-1.76%) - trigger holds, twenty-third session above 437.55 (day's low 499.80); stop far away at 420. <b>ONGC</b> 224.20 (+0.52%) - eleventh session below the 228 breakout line (high 224.90); coil floor 218.50 intact (low 222.65). <b>JSW Steel</b> 1,322.00 (+1.30%) - target 1,370 untouched (high 1,329.50); reward-to-risk at the worst fill versus the 1,158.95 floor is about 0.29 to 1, still failing the screen. <b>Hindalco</b> 923.75 (+0.95%) - a second straight close above the 911-912 zone (low 913.45), the first time the reclaim has held into the next session; the candidate case strengthens, still no verified entry zone. Ledger: <b>HCLTech</b> 1,423.80 (-2.81%), resolved earlier at the 1,468.00 exit; <b>Infosys</b> 1,152.00 (-2.55%). Shelved: <b>Voltas</b> 1,191.00 (-2.54%); <b>Tech Mahindra</b> 1,815.00 (-2.15%), above the Rs 1,500 cap.</p>"""

def px(v):
    return round(204.5 + (v - 218.5) / (238.75 - 218.5) * (591.3 - 204.5), 1)

setup_chart2 = {"t": "chart", "svg": '<svg viewBox="0 0 760 125" role="img" aria-label="ONGC: coil floor to coil top, Friday close marked"><text x="8" y="44" font-size="23">ONGC</text><line x1="204.5" x2="591.3" y1="38" y2="38" stroke="#15803d" stroke-width="10"/><circle cx="%s" cy="38" r="10" fill="#172b3c"/><text x="204.5" y="82" font-size="19" text-anchor="middle">floor 218.50</text><text x="591.3" y="82" font-size="19" text-anchor="middle">coil top 238.75</text><text x="%s" y="18" font-size="19" text-anchor="middle">Fri close 224.20</text><text x="%s" y="82" font-size="19" text-anchor="middle" fill="#64748b">breakout line 228</text></svg>' % (px(224.20), px(224.20), px(228.0))}

setup = [
 p("Nothing resolved, nothing new. Friday's broad selloff in IT and financials hit the ledger and shelved names hardest - Infosys -2.55%, Voltas -2.54%, Tech Mahindra -2.15% - while the live watchlist was mixed: Kotak -1.76%, JSW Steel +1.30%, Hindalco +0.95%, ONGC +0.52%. Four watchlist lines carry into Monday unchanged. Mahanadi's debut below its issue price adds no line to the board; the print is stated without inference."),
 p("The line to watch is Hindalco's. It closed above the 911-912 zone for a second straight session, and unlike the previous reclaim, which failed the next day, this one held. That strengthens the candidate case. It is still not a setup: there is no verified entry zone against longer history. ONGC's coil floor at 218.50 held an eleventh session. Cash-only swing setups under Rs 1,500 a share; research, not advice."),
 {"t": "chart", "svg": setup_lines},
 setup_chart2,
]

rules = {"t": "rows", "items": [
 {"n": "1", "title": "No prior-day stop trade", "detail": "A setup activates only if the zone fills before any prior-day trade at or below the stop; a stop touched first kills the line before entry."},
 {"n": "2", "title": "Worst fill in the zone", "detail": "Entry is assumed at the worst price inside the published zone, not the best."},
 {"n": "3", "title": "R:R on the worst fill", "detail": "Reward-to-risk is computed from the worst fill to the published stop and target; lines that fail stay on the watchlist, not the board."},
 {"n": "4", "title": "Resolution only", "detail": "Every published setup stays on the board until its target or its stop resolves it; resolved lines move to the ledger with gross and net (0.3% cost convention)."},
]}

week = {"t": "rows", "items": [
 {"n": "1", "title": "Sun 29 Nov", "detail": "OPEC+ meets; the expectation reported by Reuters is that it holds its first-quarter 2027 output targets. That is an expectation, not a decision."},
 {"n": "2", "title": "Mon 30 Nov", "detail": "Tata Sons board meeting, with the court's final orders still to come. India's second-quarter GDP print arrives at the statistics ministry's 4:30 PM press conference, alongside October industrial output; one forecast cited by Capital Market is about 7.6% against 7.8% in the previous quarter. Tech Mahindra's 1:1 bonus record date."},
 {"n": "3", "title": "Tue 1 Dec", "detail": "Character.AI's platform and chat records go to auction. Matangi Rubber's Rs 125.16 crore issue opens and runs to Thursday 3 December."},
 {"n": "4", "title": "Wed 2 to Fri 4 Dec", "detail": "Swara Baby Products and Monomark Engineering open their issues on Wednesday. The Reserve Bank's rate meeting runs 2 to 4 December; the repo rate stands at 5.50%, as set at the 7 October meeting. US jobs data comes Friday."},
]}

notes = [
 {"t": "bullets", "items": [
   "Sources read for this edition: BSE's bhavcopy for every Indian price; Hindu BusinessLine, The Hindu and the Economic Times for the Indian close; CNBC-TV18 for provisional flows and the Mahanadi listing; RTHK, Kabutan and Yonhap for Asia; the Los Angeles Times and AP for Wall Street; Bloomberg and stockanalysis.com for Anthropic; Reuters and Dow Jones for oil and gold; The Hindu, Bar and Bench, LiveLaw and The Indian Express for the Tata hearing; the FCC's own order for the SpaceX licence; PIB, the RBI's own pages and Capital Market for the week ahead; the California Attorney General's release for Character.AI; Sarasvathy's 2001 paper and UVA Darden for effectuation.",
   "Prices: every India price is a BSE official print; flows are provisional exchange data as reported by CNBC-TV18. Sources differ on the next hearing date in the Tata case and on the Reserve Bank's listing deadline, so neither is printed.",
   "Correction: Edition 53 named the second plaintiff in the Tata suits as the Sir Ratan Tata Trust and called the plaintiffs the two largest trusts controlling 66% of Tata Sons. The second plaintiff is the RD Tata Trust, and the 66% belongs to the Tata Trusts together. Editions 52 and 53 also dated Monday's events as Sunday 30 November; 30 November 2026 is a Monday. Both are corrected on the site.",
 ]},
 {"t": "closing", "text": "See you tomorrow."},
]

LR_INTRO = "The 5-minute lead route is first; sections carry the detail. The long read: a computing room that Tata companies were barely using, a manager borrowed for a year who stayed, an export promise the government attached to a mainframe, and a software filter shipped to the United States on tape. TCS, the Tata computer room that became an export industry."

day54 = {
 "day": 54,
 "meta": {"date": "Saturday 28 November 2026", "short": "Sat 28 Nov", "longread": 54},
 "edition": {
  "fact": "Edition 54. Saturday 28 November 2026. This edition runs 3016 words. China's state-backed national team lifted mainland stocks to their biggest gain in over two years; Wall Street ended its best week since April 2025; the Bombay High Court let Monday's Tata Sons board meeting go ahead; and Mahanadi Coalfields listed at Rs 132.60 against its Rs 136 issue price.",
  "intro": LR_INTRO,
  "hero": {"img": "photos/d54-hero.jpg", "alt": "Abstract plate: a quiet Saturday desk with a weekly ledger, a courthouse bench and a tall window, the faint outline of an old mainframe room behind it, soft first light"},
  "groups": [
   {"heading": "The 5-minute lead route", "blocks": lead},
   {"heading": "Front page", "blocks": front},
   {"heading": "Markets", "blocks": markets},
   {"heading": "IPOs", "blocks": ipos},
   {"heading": "Top movers - Friday's verdicts", "blocks": movers},
   {"heading": "Corporate actions", "blocks": corp},
   {"heading": "Finance Goldmine", "blocks": gold},
   {"heading": "AI Race", "blocks": ai},
   {"heading": "One concept: effectuation", "blocks": concept},
   {"heading": "Setup board", "blocks": setup},
   {"heading": "How the board scores", "blocks": [rules]},
   {"heading": "The week ahead", "blocks": [week]},
   {"heading": "Notes on this edition", "blocks": notes},
  ],
 },
}

json.dump(day54, open('/downloads/morning-paper/editions-src/day-54.json', 'w'), ensure_ascii=False, indent=1)
print('wrote day-54.json')
