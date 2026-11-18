#!/usr/bin/env python3
import json, os

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}
def rows(items): return {'t': 'rows', 'items': items}
def row(n, title, detail): return {'n': n, 'title': title, 'detail': detail}
def bullets(items): return {'t': 'bullets', 'items': items}
def closing(html): return {'t': 'closing', 'html': html}

def bars(label, rows_, scale=45, zero=410):
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

NVPR = 'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000088/q3fy27pr.htm'
CNBCLIVE = 'https://www.cnbc.com/2026/11/17/nvidia-nvda-earnings-report-q3-2027.html'
POLITICO = 'https://www.politico.com/news/2026/11/17/jensen-huangs-return-is-off-the-table-nvidia-chair-says-01171687'
TC = 'https://techcrunch.com/2026/11/17/nvidia-says-it-doesnt-plan-to-reappoint-jensen-huang-as-ceo/'
XINHUA = 'https://english.news.cn/20261118/0d3c2fee757b445a9d3fb6a93445f323/c.html'
INVFUT = 'https://www.investing.com/news/stock-market-news/us-stock-futures-jump-as-nvidia-earnings-revive-ai-optimism-5034391'
APNSA = 'https://apnews.com/article/nsa-computer-network-down-22dc6be1bf1d1f5f86a7167f016e9526'
CNBCANT = 'https://www.cnbc.com/2026/11/17/anthropic-ipo-price.html'
S1A3 = 'https://www.sec.gov/Archives/edgar/data/2130357/000162828026074338/anthropicpbc-sx1ax3.htm'
SACRM = 'https://seekingalpha.com/news/4673872-salesforce-leads-enterprise-software-stocks-lower-ahead-of-anthropics-ipo'
HBLCLOSE = 'https://www.thehindubusinessline.com/markets/sensex-nifty50-today-stock-market-live-updates-17th-november-2026/article71708442.ece'
CN18 = 'https://www.cnbctv18.com/markets/sensex-nifty-recover-us-iran-war-losses-5-reasons-behind-market-rally-as-nifty-hits-9-month-high-20035910.htm'
FIIS = 'https://www.cnbctv18.com/markets/fpis-extend-buying-streak-to-12-sessions-november-inflows-cross-usd-10-billion-20036086.htm'
MCINR = 'https://www.moneycontrol.com/news/business/banks/rupee-jumps-46-paise-to-93-48-hits-seven-month-high-on-foreign-fund-inflows-lower-crude-14082515.html'
REU = 'https://live.euronext.com/en/financial-news/stocks-fall-nvidia-focus-oil-ticks'
OAI = 'https://openai.com/index/introducing-gpt-6-2-astra-sol/'
MSFT = 'https://microsoft.ai/news/microsoft-ignite-2026/'
ST = 'https://startuptalky.com/news/daily-indian-funding-roundup-key-news-17-november-2026/'
ETW = 'https://www.etnownews.com/markets/q2-results-next-week-sml-mahindra-aye-finance-among-15-companies-to-announce-quarterly-earnings-buyback-issue-in-focus-full-list-article-156511135'
DS = 'https://simonwillison.net/2026/Nov/17/datasette-lite/'
DSLITE = 'https://lite.datasette.io/'
GIFT = 'https://giftniftytoday.com/pre-market'
US10YQ = 'https://www.cnbc.com/quotes/US10Y'
FRPI = 'https://www.federalregister.gov/public-inspection/2026-23529/addressing-remote-access-to-advanced-semiconductors'
HBLBANK = 'https://www.thehindubusinessline.com/markets/bank-nifty-breaks-into-uncharted-territory-as-fii-billions-back-indias-bull-run/article71711651.ece'
TAK = 'https://doi.org/10.1016/0010-0285(73)90033-9'
NKE = 'https://www.nikkei.com/article/DGXZQOFL180JT0Y6A111C2000000/'
FRGOV = 'https://www.federalregister.gov/'
BISPDF = 'https://www.bis.gov/media/documents/rin-0694-ak50.pdf'
FOOL = 'https://www.fool.com/coverage/stock-market-today/2026/11/17/stock-market-today-nov-17-nvidia-slides-ahead-of-earnings-but-soars-in-after-hours-trading/'
LRURL = 'https://files.instinct.com/9rcxw4zz4a9r-the-company-that-only-makes-other'

movers = bars('Leaders and laggards, Tuesday 17 Nov (% vs Monday\'s close), BSE official prints', [
    ('Adani Enterprises', 3.1, '+3.1%'), ('Eicher Motors', 2.9, '+2.9%'), ('Oberoi Realty', 2.8, '+2.8%'),
    ('Godrej Properties', 2.7, '+2.7%'), ('Prestige Estates', 2.4, '+2.4%'),
    ('Oil India', -1.8, '-1.8%'), ('Wipro', -1.8, '-1.8%'), ('HCL Tech', -2.0, '-2.0%'),
    ('Tata Communications', -2.8, '-2.8%'), ('Ashok Leyland', -4.3, '-4.3%')])

board_html = ('<p style="color:#64748b;font-size:13px">Open lines after Tuesday\'s session; prices are BSE official closes, Tuesday 17 November - tonight\'s session is the next scored one</p>'
 + card(1, 'Kotak Mahindra Bank', [('Status','Watchlist - trigger held'),('Entry / trigger','Post-print strength above Rs 437.55 - held above it for a sixteenth session, close Rs 496.65 (+0.70%); touched a 52-week high intraday'),('Stop / invalidation','Below Rs 420 shelves it'),('Target / objective','Structured-setup candidate'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 496.65 (Tue close)')])
 + card(2, 'ONGC', [('Status','Watchlist - inside coil, breakout leg not re-established'),('Entry / trigger','Breakout above 228 with crude holding - close Rs 223.60, fourth session under 228; Brent firmed to $93.26 Tuesday, so the crude leg stabilizes'),('Stop / invalidation','Coil floor Rs 218.50'),('Target / objective','Coil top Rs 238.75'),('R:R at worst fill','1:1.1 - below the screen'),('Reference price','Rs 223.60 (Tue close)')])
 + card(3, 'Infosys', [('Status','Watchlist - below zone, floor watch'),('Entry / trigger','Absorption thesis - trigger zone Rs 1,175, close-based floor Rs 1,120 - close Rs 1,130.00, still below the zone; Tuesday\'s low of Rs 1,126.00 came within six points of the floor'),('Stop / invalidation','A close under 1,120 ends the thesis'),('Target / objective','First checkpoint 1,245 (gap zone)'),('R:R at worst fill','n/a (qualitative)'),('Reference price','Rs 1,130.00 (Tue close)')])
 + card(4, 'JSW Steel', [('Status','Watchlist - fails the screen at Tuesday\'s price'),('Entry / trigger','Hold 1,158.95, then reclaim 1,218.90-1,222.30 - held since; closed Rs 1,336.00'),('Stop / invalidation','Under 1,158.95 breaks the floor'),('Target / objective','5 November swing high near Rs 1,370'),('R:R at worst fill','1:2.3 at the reclaim zone - 1,222.30 fill, 1,158.95 stop, 1,370 target; about 1:0.2 at Tuesday\'s close'),('Reference price','Rs 1,336.00 (Tue close)')])
 + card(5, 'Hindalco', [('Status','Watchlist - candidate'),('Entry / trigger','No entry zone yet - levels to be verified against longer price history; closed Rs 927.70 (+0.29%)'),('Stop / invalidation','n/a until an entry zone exists'),('Target / objective','Momentum plus record quarter as catalyst'),('R:R at worst fill','n/a (not a setup)'),('Reference price','Rs 927.70 (Tue close)')]))

ongc_range = rangec(218.50, 223.60, 238.75, '223.60', "ONGC: coil floor to coil top, marker at Tuesday's close")

G = []

G.append({'heading': 'The 5-minute lead route', 'blocks': [
 p(' Nvidia answered. The first quarter of the post-Huang era came in at $115.8 billion of revenue - up 103% on the year and well above the $109.1 billion analysts expected - with data center at $107.6 billion, up 110%, and a fourth-quarter guide of $130 billion, give or take 3%, against the $125.1 billion expected (' + a(NVPR, 'the company\'s release') + '; ' + a(CNBCLIVE, 'LSEG\'s estimates via CNBC') + '). It was Colette Kress\'s first print as interim CEO and CFO, and the market\'s verdict was immediate: the stock, down 24% in November going in, rose nearly 5% in extended trading Tuesday evening (' + a(INVFUT, 'the after-hours read') + '). The guide\'s fine print: it includes an extra week in the quarter, assumes no China data-center compute revenue, and guides gross margin down to 71-72%.'),
 p(' The leadership file moved twice on the same evening. Jensen Huang issued his first statement since resigning: "If the Board of Directors decides that my return is in the best interest of our shareholders, our employees, the company, and America, I would be honored to answer these calls and return as CEO" (' + a(CNBCLIVE, 'CNBC\'s live report') + '). Board chair Harvey C. Jones closed that door on the call itself: the board "does not intend" to reinstate Huang, having unanimously accepted his resignation - after what the company now describes as disclosure of personal behavior inconsistent with its code of conduct (' + a(POLITICO, 'Politico\'s report') + '; ' + a(TC, 'TechCrunch\'s report') + '). Those are the company\'s words, reported as such; this paper adds nothing to them.'),
 p(' Wall Street had sold the rumor. Tuesday was the S&P 500\'s fourth straight loss - down 1.03% to 7,340.53, its lowest close since July - with the Dow off 848.75 points to 50,759.42 and the Nasdaq down 0.74% to 24,328.38; all eleven sectors fell (' + a(XINHUA, 'the closing wire') + '). Salesforce sank 9% as enterprise software slid ahead of Anthropic\'s debut (' + a(SACRM, 'the software selloff') + '). Then the print landed and futures turned: S&P 500 futures up about 0.7-0.8%, Nasdaq 100 futures up about 1.4-1.6% overnight (' + a(INVFUT, 'the futures board') + '). Separately, the NSA confirmed an outage of an internal classified network after what it called scheduled maintenance; officials said there was no indication of an attack (' + a(APNSA, 'the AP\'s report') + ').'),
 p(' Mumbai, meanwhile, set records. The Sensex rose 427.40 points to 82,532.19 and the Nifty 96.30 to 25,387.40 - both at nine-month highs, having recovered every point lost since 27 February (' + a(HBLCLOSE, 'the BusinessLine close') + '). The Bank Nifty scaled a record 62,442.20 intraday and closed at a record 62,273.25 (' + a(HBLBANK, 'the banking report') + '); FIIs bought a twelfth straight session - a provisional Rs 4,195.38 crore - taking November\'s foreign inflows past $9.5 billion, a record month (' + a(FIIS, 'the flow tally') + '). The rupee joined in: 93.48 to the dollar, its strongest close in seven months (' + a(MCINR, 'the currency report') + '). Falling crude did the lifting for autos, paints and airlines.'),
 p(' Anthropic\'s order books closed at 4 PM in New York on Tuesday, and the offering is likely to price above its $70-78 range, CNBC reports, citing people familiar - an expectation, not an outcome (' + a(CNBCANT, 'the report') + '). Pricing is tonight, New York time; the first trade is Thursday as ANT. The tape it prices into: a software sector it has already marked down, and an AI trade that Nvidia just steadied. The day\'s third gate is the Fed: minutes of the October meeting land today, with futures pricing a December rate rise as near-certain, per CME FedWatch (' + a(INVFUT, 'the rates board') + ').'),
 p(' The BIS compute rule is scheduled, not yet law. The remote-access rule - RIN 0694-AK50 - was filed with the Federal Register on Monday and sits on its public-inspection list, scheduled for publication on Thursday 19 November (' + a(FRPI, 'the inspection entry') + '; ' + a(BISPDF, 'the rule text') + '). Every clock keys off that publication: the rule takes effect on its publication date, comments run sixty days from it, and a data center already providing significant compute, before publication, to customers headquartered - or whose ultimate parent is headquartered - in Macau or Country Group D:5 has ninety days from effectiveness to license that existing service; new activity needs a license without that grace. Until the Thursday issue lands, the rule remains scheduled, not operative.'),
 p(' Overnight markers, as of about 6 AM IST: Brent $93.14; the dollar index at 103.49; gold at $3,841.60, down 0.58%; the US ten-year at 5.115% (' + a(US10YQ, 'CNBC\'s quote boards') + '); the VIX closed Tuesday at 25.46, up 11.13%; GIFT Nifty at 25,358.50, up 0.03%, pointing to a flat open near 25,395 - an indication, not an open (' + a(GIFT, 'the pre-market screen') + '). Tokyo opened higher on the Nvidia print - the Nikkei up about 147 points at the open, gains widening past 400 within minutes (' + a(NKE, 'the Tokyo open') + ').'),
 p(' The long read: the company that only makes other people\'s chips. The chips behind Nvidia\'s record quarter came from one firm in Hsinchu - and Morris Chang was twice sidelined and past fifty when he invented its model. TSMC, the pure-play foundry, as the AI trade\'s quiet landlord (' + a(LRURL, 'read it here') + '). The route ends. The detail begins.'),
]})

G.append({'heading': 'Front page', 'blocks': [
 p(' The print, in full. Revenue of $115.8 billion - up 103% year on year, up 20% on the quarter - with data center at $107.6 billion, up 110% year on year; GAAP gross margin of 74.8%; GAAP earnings of $2.70 a share; net income of $65.3 billion, up 105% (' + a(NVPR, 'the release') + '). Vera Rubin NVL72 systems are shipping - the fastest ramp in the company\'s history, it says - with CoreWeave, Google Cloud, Azure, OCI and Nebius among the first customers. The Hugging Face acquisition remains on track. Four customers made up 47% of the quarter\'s sales - the concentration number to carry into the Concept section below. Kress told the call that Anthropic\'s annualized revenue reached $81 billion at the end of October, and raised the company\'s FY28 growth outlook to 75% from 70% - the company\'s outlook, in its own framing.'),
 p(' What the beat is made of. The $130 billion guide is a real beat - $125.1 billion was the consensus - but it is a constructed one, and the construction is disclosed: the quarter carries an extra week, and the number assumes zero China data-center compute revenue (' + a(NVPR, 'the release') + '). Gross margin is guided down to 71-72% from 74.8% - the cost of the Rubin ramp. And the shareholder returns keep pace: $28.1 billion went out in buybacks and dividends in the quarter, with $227.3 billion of authorization remaining. The stock\'s nearly-5% after-hours answer, by late evening in New York, followed a 24% November slide - six straight weekly drops, the longest such run since 2012 (' + a(CNBCLIVE, 'CNBC\'s live report') + ').'),
 p(' The leadership exchange, on the record. Huang\'s statement Tuesday was his first since the resignation, and it offered a return: "If the Board of Directors decides that my return is in the best interest of our shareholders, our employees, the company, and America, I would be honored to answer these calls and return as CEO" (' + a(CNBCLIVE, 'the statement as reported') + '). Jones, on the call, said the board unanimously accepted the resignation and does not intend to reinstate him - and the company\'s account of the resignation itself has now gained one official sentence: it followed disclosure of personal behavior inconsistent with Nvidia\'s code of conduct, standards and cultural norms (' + a(POLITICO, 'Politico') + '; ' + a(TC, 'TechCrunch') + '). That sentence is the whole of what the company has said on the subject. A search for a permanent chief continues.'),
 p(' The day the print landed into. Tuesday\'s regular session was a selloff: the S&P 500\'s fourth straight loss and lowest close since July, every sector red, financials the worst at -1.87% (' + a(XINHUA, 'the closing wire') + '). The AI complex\'s own anxiety showed in software, where Salesforce\'s 9% fall led the S&P\'s decliners as Anthropic\'s IPO approached - investors are repricing the application layer the new models aim at (' + a(SACRM, 'the software read') + '). Nvidia closed the regular session at $155.46, down 0.44%, before the numbers changed the conversation (' + a(FOOL, 'the session recap') + '). One session of futures is not a recovery; it is a repricing of the print.'),
 p(' Mumbai\'s record day, in full. The Nifty\'s close at 25,387.40 completes the recovery from 27 February - the day the US-Iran war losses began - with 22 constituents now above their levels of that date; Eternal, Kotak Mahindra Bank and ICICI Bank touched 52-week highs (' + a(CN18, 'the session\'s anatomy') + '). Banks did the heavy lifting - the Bank Nifty\'s record 62,442.20 intraday and record close of 62,273.25, up 1.13% (' + a(HBLBANK, 'the banking report') + ') - while cheaper crude lifted Eicher, M&M, Asian Paints and InterGlobe, and Reliance rose 2% to a six-month high as the index\'s biggest contributor. The tell that it was a large-cap day: the advance-decline ratio was flat at 1:1, and small-caps slipped 0.2%. UPL faded from its high on reports its restructuring may be revised; KEI fell 4% on price-cut reports; Ashok Leyland spiked, then closed 8% below its day\'s high; Laurus Labs gained over 5% after management said it had no plans to sell further stake.'),
 p(' The debut that prices tonight. Anthropic\'s books closed Tuesday afternoon in New York, with the offering likely to price above the $70-78 range, per CNBC\'s sourcing - reported here as an expectation, not a result (' + a(CNBCANT, 'the report') + '). The third amended filing landed the same day (' + a(S1A3, 'the S-1/A-3') + '). Nine-month revenue of $33.24 billion, up roughly twelvefold, against a nine-month net loss of $104 billion - most of it the fair-value accounting of convertible notes. The concurrent $26 billion supplier placement closes immediately after the offering. First trade: Thursday, as ANT.'),
]})

G.append({'heading': 'Markets', 'blocks': [
 p(' Tuesday\'s marks, then this morning\'s markers. Mumbai: Sensex 82,532.19, up 427.40 (0.52%); Nifty 25,387.40, up 96.30 (0.38%) - both nine-month highs (' + a(HBLCLOSE, 'the close') + '). New York: S&P 500 7,340.53, down 1.03%; Nasdaq 24,328.38, down 0.74%; Dow 50,759.42, down 1.64%; VIX 25.46, up 11.13% (' + a(XINHUA, 'the wire') + '; ' + a(GIFT, 'the board') + '). This morning, as of about 6 AM IST: S&P 500 futures up 0.8% at 7,418.25 and Nasdaq 100 futures up 1.6% at 27,497.75 (' + a(INVFUT, 'the futures report, timestamped 5:22 AM IST') + '); Brent $93.14; gold $3,841.60, down 0.58%; the dollar index 103.49; the US ten-year at 5.115% (' + a(US10YQ, 'CNBC\'s quote boards') + '); GIFT Nifty at 25,358.50, up 0.03% - a flat indication, not an open (' + a(GIFT, 'the pre-market screen') + '). Tokyo opened up 147 points at 59,007.40 and widened gains past 400 early (' + a(NKE, 'the open') + '). The day\'s schedule: the Fed\'s October minutes this evening; Anthropic prices tonight New York time.'),
]})

G.append({'heading': 'IPOs', 'blocks': [
 p(' The largest AI listing ever attempted gets its price tonight. Anthropic\'s 825 million Class A shares at $70 to $78 price Wednesday evening in New York - the third amended filing is in, the books are closed, and CNBC\'s sources say the price is likely to land above the range; treat that as reported expectation until the print (' + a(S1A3, 'the filing') + '; ' + a(CNBCANT, 'the pricing report') + '). The valuation sought runs to roughly $1.4 trillion, and the sector it lands in has already been repriced: Salesforce, ServiceNow, Workday and Adobe all fell Tuesday as investors weighed what the new models do to the application layer (' + a(SACRM, 'the software slide') + '). In Mumbai, Urban Company opened a Rs 2,500-crore QIP with a floor of Rs 161.03 per share - up to a 5% discount permitted - and Rediff filed updated IPO papers (' + a(ST, 'the startup wire') + ').'),
]})

G.append({'heading': 'Top movers - Tuesday\'s verdicts', 'blocks': [
 p(' Tuesday\'s board - the large names this paper tracks, from best to worst (percentages computed from BSE\'s official closes against Monday):'),
 {'t': 'chart', 'svg': movers},
 p(' Realty carried the day: Oberoi, Godrej Properties and Prestige all gained more than 2.4%, with Adani Enterprises the board\'s leader at +3.12% (' + a(CN18, 'the session report') + '). The two extremes are both reversals: Ashok Leyland closed at Rs 160.65, down 4.26% - and 8% below its own day\'s high - giving back Monday\'s post-print gain, while Tata Communications shed 2.82% after leading Monday\'s board. Tata Motors PV steadied at Rs 259.55, down 1.01% after Monday\'s 8.64% verdict. Carried closes for the ledger: ONGC Rs 223.60, Tata Steel Rs 181.55, SAIL Rs 171.20, ITC Rs 293.00.'),
]})

G.append({'heading': 'Corporate actions', 'blocks': [
 p(' Wednesday\'s board is thin - a small-cap day (' + a(ETW, 'the week\'s calendar') + '). Ansal Properties, BLS Polymers and GVP Infotech feature in the results lane; Aye Finance has an NCD raise; Bonlon Industries prices its rights issue. Thursday is busier: Muthoot Microfin reports, and Natco Pharma\'s dividend record date arrives. Friday carries the twin record dates for Ashok Leyland\'s Re 1 interim and Oil India\'s dividend - both names on today\'s movers board, for different reasons.'),
]})

G.append({'heading': 'Finance Goldmine', 'blocks': [
 p(' What after-hours actually tells you. Nvidia fell 0.44% in Tuesday\'s regular session, reported at 1:20 PM Pacific, and rose nearly 5% in extended trading by late evening - three prices for one stock in one day, and only the first is the deep market (' + a(FOOL, 'the session recap') + '; ' + a(INVFUT, 'the extended session') + '). The mechanics matter: after-hours trading runs on thin volume, wide spreads and retail-heavy flow, so an extended-session move is a first vote, not a verdict - the regular open re-prices it with full participation. The useful habit is to treat the overnight number as information about direction and surprise, not about level: it tells you the print beat or missed the whisper, not where the stock will trade at the close. The same logic applies to this morning\'s GIFT Nifty line, to futures up on the Nvidia print, and to Anthropic\'s price tonight: indications are inputs, not outcomes. The paper labels each one as-of, and the open decides.'),
 p(' One term worth owning: book building. When CNBC reports that Anthropic\'s "order books closed" at 4 PM, the term is book building: the issuer\'s banks collect bids from institutions - how many shares, at what price - before the final offer price is set (' + a(CNBCANT, 'the report') + '). The book is the tally of those bids; closing it ends the auction; pricing is the judgment that follows. An oversubscribed book is why an offering can price above its range: more demand than shares at the top end lets the banks move the clearing price up. The same mechanism runs in Mumbai - Urban Company\'s Rs 2,500-crore QIP, opened Tuesday with a Rs 161.03 floor, is a book-built offer to institutions under SEBI\'s rules (' + a(ST, 'the QIP report') + '). Watch for it tonight in the Anthropic print: the price, the multiple of the range, and what the book said.'),
]})

G.append({'heading': 'Startup Intelligence', 'blocks': [
 p(' Tuesday\'s cheques, largest first (' + a(ST, 'the daily roundup') + '). Dreamteam raised $53 million from Together Fund, Accel and Premji Invest - founded in 2025 by three ex-Freshworks executives (Anand Venkatraman, Ramesh Parthasarathy, Senthil Kanthaswamy), it is building an AI-first CRM, with InVideo and Plex as customers. CountAI took a Rs 10-crore seed from Equirus InnovateX for its Knit-I fabric-defect cameras - KPR and Indorama are customers. finny.club raised Rs 5.3 crore in an angel round that included Juspay\'s Ramanathan RV - it is SEBI-registered. JohnAIC raised $1.9 million pre-seed from Crane Venture Partners for on-premise AI servers, and Lemonpeel $1 million pre-seed from Shastra VC for AI video. In the listed lane, Urban Company opened its Rs 2,500-crore QIP (floor Rs 161.03), and Rediff filed updated IPO papers.'),
 p(' Today\'s startup idea: the audit ledger for agentic commerce. The prompt is this week\'s direction of travel - Microsoft shipping agent models, TSMC\'s CEO crediting "agentic AI" for demand, and Anthropic about to list (' + a(MSFT, 'the Ignite lineup') + '). As companies let AI agents browse, negotiate and pay, the question nobody owns yet is bookkeeping: what did the agent see, what did it decide, what did it spend, and who proves it in a dispute? The idea, with its limits stated: a neutral transaction ledger for agent actions - signed records of prompts, prices and payments that finance and legal teams can audit - sold per logged transaction. The limits: there is no settled standard for agent identity or consent, liability frameworks are unwritten, and the payment networks and model providers may bundle this before a startup can price it - in which case the honest pivot is the dispute-evidence layer, where independence is the product. What would make it wrong: agents staying read-only for another year.'),
]})

G.append({'heading': 'AI Race', 'blocks': [
 p(' Two price lists, one direction. OpenAI released GPT-6.2 Astra and Sol: Astra posts a new high on the Agents\' Last Exam - 5.2 points above GPT-6 Astra at less than a third of the cost, and 5.5 above Claude Fable 5.2 at 5% of the cost - with API pricing of $8 per million input tokens ($0.40 cached) and $40 per million output, 20% below its predecessor; on the Harvey legal benchmark it claims more than double Fable 5.2\'s pass rate at about a sixth of the cost (' + a(OAI, 'the release') + '). Microsoft used Ignite to ship seven models of its own - MAI Cyber 2 Flash, Code 2 and Code 2 Flash, Image 2.7, Realtime 1, Transcribe 2 for Dragon Copilot, and Decision 1.1 - and put its Maia 200 accelerator into production at a claimed 1.7x tokens per watt (' + a(MSFT, 'the Ignite announcements') + '). The frame the week has built: the model layer keeps cutting prices and shipping capability, while the silicon layer underneath prints records. Both cannot be a bubble at once - and both claims are now on the tape.'),
]})

G.append({'heading': 'Vibe coding', 'blocks': [
 p(' The browser is becoming the server. Simon Willison has rewritten Datasette Lite so the full Datasette Python application - server, database engine, plugins - runs inside a browser tab on WebAssembly, via service workers and Pyodide, with no install and no backend (' + a(DS, 'his write-up') + '). The builder\'s lesson is not the demo; it is the architecture. A URL can now carry the entire environment: which Datasette version, which plugins from PyPI, which data files - so a bug report or a data demo becomes a link, not a setup guide. When you build a tool, ask what its "lite" version would be: the whole product, minus the server, shipped as a link. The constraint that makes it work is also the lesson: browsers are sandboxed, so state lives with the user and nothing phones home - privacy as a deployment model. The limits are real too: WASM payloads are heavy, large datasets strain a tab, and persistence is yours to arrange.'),
]})

G.append({'heading': 'Try this today (Wednesday)', 'blocks': [
 p(' Run a database in a browser tab. Open ' + a(DSLITE, 'lite.datasette.io') + ' and point it at any public CSV, JSON or SQLite file - the tool loads it client-side and gives you a full queryable, filterable interface (' + a(DS, 'the author\'s examples') + '). Free, on the web, no login; the demo link on the write-up loads a mapping plugin and a sample dataset if you want the guided version. Try it with a file you already know - a portfolio export, a spending CSV - and notice how much more you see in a table you can filter than in the same rows in a spreadsheet. The limits: everything runs in your tab, so very large files will strain it; your data never leaves your machine, which is the point but also means there is nothing to come back to once you close it; and sharing means sending someone the crafted URL, data file included.'),
 p(' Then, a reading habit for tonight: the owning document. When Anthropic prices, the recap will be everywhere - read the filing first. The SEC\'s full-text search (efts.sec.gov/LATEST/search-index?q=%22Anthropic%22 - or the EDGAR full-text page at sec.gov) is free, on the web, no login. Search the company, open the S-1/A, and read the risk factors and the concurrent placement before you read anyone\'s summary of them (' + a(S1A3, 'the current amendment') + '). The limits: EDGAR is a document store, not an explainer - it gives you what the company filed, in the company\'s words, with no one to translate the accounting. That is also its value: every claim in tomorrow\'s coverage traces back to what you can read tonight.'),
]})

G.append({'heading': 'One concept: recency bias', 'blocks': [
 p(' The recency bias, and the engine under it. In 1973, Amos Tversky and Daniel Kahneman described the availability heuristic: people judge how common something is by how easily an example comes to mind. In their best-known test, most people said more English words begin with the letter K than have K in third place - the truth is the reverse, roughly two to one, but K-first words are easier to summon (' + a(TAK, 'the 1973 paper') + '). Recency bias is the same engine with a clock: the freshest, most vivid evidence quietly becomes the base rate. This week wore the pattern. Six straight weekly losses in Nvidia made "the AI trade is over" feel like the base rate - then one strong print and a nearly-5% after-hours move flipped the story before breakfast, and Mumbai\'s record close made the losses of 27 February feel ancient. Neither the despair nor the relief was a statistic; both were the freshest number doing the talking. The habit: when the latest number moves you most, ask what the last ten said. One print is a data point; a trend is a series.'),
]})

G.append({'heading': 'Setup board', 'blocks': [
 p(' Tuesday\'s session is scored. No stop touched, no target taken - but Infosys\'s floor had its closest call: the day\'s low of Rs 1,126.00 came within six points of the 1,120 close-based floor, and the close at Rs 1,130.00 keeps the thesis alive by its own rule. Every price below is a BSE official close from Tuesday\'s tape. The desk\'s rule stands: every published setup stays on the board until it resolves by its own rules.'),
 {'t': 'chart', 'svg': board_html},
 {'t': 'chart', 'svg': ongc_range},
 p(' The resolved line stays in the ledger: HCLTech, filled 28 October at the worst fill of Rs 1,378.00, target Rs 1,466.80 taken out at 1,468.00 - gross +6.53%, net +6.23% after the 0.3% cost convention - closed Tuesday at Rs 1,355.50. Shelved: Voltas stays rejected, closing at Rs 1,147.30; Tech Mahindra stays shelved above the Rs 1,500 cap, closing at Rs 1,758.00.'),
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
 p(' A week of scenarios met a print. Since Monday, the AI trade had been priced as contingency: the Fed chairman\'s downside scenario, target cuts ahead of the numbers, six straight weekly losses in the stock itself, and software names sold against a competitor\'s listing. Tuesday night replaced contingency with arithmetic - $115.8 billion of revenue, a $130 billion guide, margins guided down on purpose - and the after-hours vote reversed the day\'s entire mood in minutes. The honest reading keeps both facts: the print was strong, and one print does not retire the scenario it answered. The same discipline applies to the evening\'s other exchange. Huang said he would be honored to return; the board said it does not intend to ask. Both statements now sit on the record, in the principals\' own words - and the record, not the rumor, is where this story lives until the search for a permanent chief ends. Price the stated stage, not the headline\'s certainty: released is not operative, a guide is not a quarter, and a pricing tonight is not a debut Thursday.'),
 p(' Also brewing - the leadership file. Cause chain: Huang\'s resignation, now officially characterized as following disclosure of conduct inconsistent with the code of conduct; his first statement Tuesday offering to return; Jones\'s on-call answer that the board does not intend to reinstate him; Kress interim CEO and CFO, one strong print delivered. What settles it: the appointment of a permanent chief. Watch: any search announcement, and whether the board\'s position holds under shareholder pressure.'),
 p(' Also brewing - the debut file. Cause chain: three amended filings; books closed Tuesday 4 PM New York; likely above-range pricing per CNBC\'s sourcing; the $26 billion supplier placement closing after; first trade Thursday as ANT. What settles it: tonight\'s price, then Thursday\'s first print. Watch: New York tonight and the opening cross.'),
 p(' Also brewing - the compute-rule file. Cause chain: released Monday as RIN 0694-AK50; filed with the Federal Register the same day and on the public-inspection list since, with publication scheduled for Thursday 19 November (' + a(FRPI, 'the inspection entry') + '). What settles it: the published entry - effectiveness keys to the publication date, comments run sixty days from it, and the ninety-day grace covers only existing service - data centers already providing significant compute, before publication, to customers headquartered, or whose ultimate parent is headquartered, in Macau or Country Group D:5; new activity is licensed without the grace. Watch: Thursday\'s Register issue, then the comment file.'),
]})

G.append({'heading': 'The week ahead', 'blocks': [
 rows([
  row('1', 'Wed 18 Nov (today)', 'Anthropic prices the 825-million-share offering in New York this evening; the Fed publishes minutes of its October meeting.'),
  row('2', 'Thu 19 Nov', 'ANT debuts on the Nasdaq; the $26 billion supplier placement closes after the offering. Muthoot Microfin reports; Natco Pharma dividend record date.'),
  row('3', 'Fri 20 Nov', 'Record date for Ashok Leyland\'s Re 1 interim dividend and Oil India\'s dividend.'),
  row('4', 'Watching', 'Federal Register publication of RIN 0694-AK50 (starts the rule\'s clocks); Nvidia\'s follow-through after the print; the Infosys floor at 1,120 after Tuesday\'s six-point miss; a permanent Nvidia chief.'),
 ]),
]})

G.append({'heading': 'Notes on this edition', 'blocks': [
 bullets([
  'Sources read for this edition: Nvidia\'s own results release and quarterly call coverage; CNBC\'s live earnings blog for the Huang statement and the Jones exchange, cross-checked against Politico and TechCrunch; the closing market wire and Reuters\' market wrap (which settled a conflicting oil figure from another wrap - Brent rose Tuesday; the wrong figure was discarded); the NSA outage confirmed at the agency\'s own statement and the AP; CNBC\'s Anthropic pricing report, kept as attributed expectation; the S-1/A-3 filing; the Hindu BusinessLine and CNBC-TV18 for the Mumbai close and flows; Moneycontrol for the rupee; the Federal Register\'s public-inspection list, checked this morning - the rule was filed Monday and is scheduled to publish Thursday 19 November, so every clock still waits on publication; OpenAI\'s and Microsoft\'s own announcements; StartupTalky\'s funding roundup; Simon Willison\'s Datasette Lite write-up; BSE\'s official bhavcopy for Indian prices; and the GIFT pre-market screen, labeled as-of.',
  'Framing calls this edition: the company\'s outlook (the FY28 growth raise, the Q4 guide) is reported as the company\'s own framing, not as settled outcome; Anthropic\'s above-range pricing is an attributed expectation, not a result; the resignation is described only in the words the company and the principals have used - no allegations beyond the board\'s stated sentence; an aggregator\'s claims of fresh PMI and tax data were checked and dropped as stale; the GIFT Nifty and futures lines are as-of indications, not opens.',
  'Prices are BSE official closes or the named settlement prints; provisional flow figures are labeled provisional. Nothing here is investment advice.',
 ]),
 closing(' The print beat; the board said no; the debut prices tonight. See you tomorrow.'),
]})

fact = ('Edition 44. Wednesday 18 November 2026. This edition runs 4,646 words. '
 'Nvidia\'s first post-Huang quarter beat across the board - $115.8 billion of revenue, up 103%, and a $130 billion guide, both well above the LSEG consensus; the stock rose nearly 5% after hours. '
 'Huang offered to return; the board said it does not intend to ask. Anthropic prices tonight, with CNBC\'s sources pointing above the range; Mumbai set nine-month highs on record foreign buying. '
 'The long read: TSMC - the company that only makes other people\'s chips.')

intro = ('The 5-minute lead route is first; sections carry the detail. The long read: the chips behind Nvidia\'s record quarter came from one firm in Hsinchu - '
 'and Morris Chang was twice sidelined and past fifty when he invented the pure-play foundry. TSMC, the AI trade\'s quiet landlord.')

d = {
 'day': 44,
 'meta': {'date': 'Wednesday 18 November 2026', 'short': 'Wed 18 Nov', 'longread': 44},
 'edition': {'fact': fact, 'intro': intro, 'groups': G, 'hero': {'img': 'photos/d44-hero.jpg', 'alt': 'Abstract plate: a printed sheet, a half-open door, a rising line', 'caption': 'Abstract plate for edition 44 - the print, the door, and the debut.'}},
 'audio': None,
}
json.dump(d, open('editions-src/day-44.json', 'w'), indent=1, ensure_ascii=False)
print('day-44.json written; groups:', len(G))
