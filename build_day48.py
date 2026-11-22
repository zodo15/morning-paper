#!/usr/bin/env python3
"""Build editions-src/day-48.json - Sunday 22 November 2026."""
import json

def a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)
def p(html): return {'t': 'p', 'html': html}
def rows(items): return {'t': 'rows', 'items': items}
def row(n, title, detail): return {'n': str(n), 'title': title, 'detail': detail}
def bullets(items): return {'t': 'bullets', 'items': items}
def closing(html): return {'t': 'closing', 'html': html}

REUTERS_SEC = 'https://www.reuters.com/3fec1b0a85a0/world/us-secs-nvidia-probe-is-examining-potential-accounting-issues-sources-say-2026-11-20/'
CNBC_SELLOFF = 'https://www.cnbc.com/2026/11/21/anthropic-ipo-tech-selloff.html'
VERGE_NVDA = 'https://www.theverge.com/tech/1039305/nvda-down-sec-investigation-accounting'
CNBC_CALLS = 'https://www.cnbc.com/2026/11/20/fridays-biggest-analyst-calls-like-anthropic.html'
CNBC_WEEK = 'https://www.cnbc.com/2026/11/20/stock-market-next-week-outlook-for-nov-23-27-2026.html'
REUTERS_BF = 'https://www.investing.com/news/stock-market-news/black-friday-brings-consumer-spending-into-focus-for-airocked-market-5041258'
ET_SEBI = 'https://economictimes.indiatimes.com/markets/stocks/news/fpis-may-soon-get-to-onboard-in-5-days-says-tuhin-kanta-pandey-as-sebi-moves-to-reduce-compliance-burden/articleshow/136044698.cms'
REDIFF_SEBI = 'https://www.rediff.com/business/report/sebi-to-develop-domestic-ai-model-for-indian-securities-market-opportunities--risks/20261121.htm'
ET_FLOWS = 'https://economictimes.indiatimes.com/markets/stocks/news/fiis-go-big-on-indian-equities-pump-over-rs-1-10-lakh-crore-in-november-what-comes-next/articleshow/136048685.cms'
MC_IPO = 'https://www.moneycontrol.com/news/business/ipo/pristine-logistics-arohan-financial-services-get-sebi-nod-to-launch-ipos-14085798.html'
HT_RAZOR = 'https://www.hindustantimes.com/business/razorpay-set-to-file-for-india-ipo-next-week-roadshows-to-follow-february-listing-in-sight-101795074649541.html'
INC42 = 'https://inc42.com/buzz/from-dreamteam-to-boba-bhai-indian-startups-raised-over-291-mn-this-week/'
DREAMTEAM = 'https://www.dreamteam.ai/blog/introducing-dreamteam'
BSEMI_TC = 'https://techcrunch.com/2026/11/15/indian-chip-startup-bharat-semi-lands-24m-seed-round-as-it-eyes-global-ai-sensor-market/'
PULL_POST = 'https://thephysicsofstartups.substack.com/p/build-your-pull-lab'
PULL_REPO = 'https://github.com/TalkToHumans/pull-lab'
APPLE_INV = 'https://www.investing.com/news/stock-market-news/apple-developing-ai-agent-that-could-operate-apps-and-browse-the-web--bloomberg-5040175'
APPLE_VERGE = 'https://www.theverge.com/tech/1038227/apple-ai-agent-engineer-job-listing'
OAI_BIZ = 'https://openai.com/index/introducing-businesses-chatgpt'
OAI_HELP = 'https://help.openai.com/en/articles/20001635-setting-up-your-business-on-chatgpt'
CF_SNAP = 'https://developers.cloudflare.com/browser-run/quick-actions/snapshot/'
CF_PRICE = 'https://developers.cloudflare.com/browser-run/pricing/'
CF_CHANGE = 'https://developers.cloudflare.com/changelog/post/2026-11-19-snapshot-all-formats/'
TOI_CHAWDA = 'https://timesofindia.indiatimes.com/business/india-business/companies-are-cautious-on-leverage-jpmorgan/articleshow/135974086.cms'
AP_NPR = 'https://www.npr.org/2026/11/20/g-s1-154797/nasdaq-sp500-stock-market-ai-sink-negative'
MAH_HDFC = 'https://hdfcsky.com/news/mahanadi-coalfields-ipo-subscription-status-day-2'
MAH_GR = 'https://www.goodreturns.in/news/mahanadi-coalfields-ipo-day-2-issue-subscribed-0-42-times-gmp-drops-as-retail-demand-falls-1548473.html'
NEXTWK = 'https://upstox.com/news/market-news/stocks/upcoming-dividend-stock-split-buybacks-next-week-zee-entertainment-vraj-iron-fusion-cx-others-in-focus/article-203772/'
GOLD_DJ = 'https://www.morningstar.com/news/dow-jones/202611206877/comex-gold-ends-the-week-947-lower-at-351230-data-talk'
OIL_NQ = 'https://www.newsquawk.com/headlines/crude-wrap-wti-f7-settles-usd-077-higher-at-usd-8398bbl--brent-f7-settles-usd-059-higher-at-usd-9257bbl'
RUPEE_BL = 'https://www.thehindubusinessline.com/money-and-banking/rupee-soars-to-7-month-high-against-the-dollar-strengthens-below-93-level/article71724707.ece'
BS_WRAP = 'https://www.business-standard.com/markets/news/markets-gain-2-6-on-fpi-inflows-rupee-rally-and-cooling-crude-oil-prices-126112000973_1.html'

prev = json.load(open('editions-src/day-47.json'))
pg = {x['heading']: x for x in prev['edition']['groups']}
movers_chart_47 = pg["Top movers - Friday's verdicts"]['blocks'][1]
setup_chart1 = pg['Setup board']['blocks'][1]
setup_chart2 = pg['Setup board']['blocks'][2]
board_rows = pg['How the board scores']['blocks'][0]

d = {}
d['day'] = 48
d['meta'] = {'date': 'Sunday 22 November 2026', 'short': 'Sun 22 Nov', 'longread': 48}

ed = {}
ed['fact'] = ("Edition 48. Sunday 22 November 2026. This edition runs 4,577 words. "
 "Two regulators spent Saturday at opposite ends of the AI trade: in Washington, the SEC's enforcement staff is examining potential accounting issues at Nvidia, the company at the center of the market's worst week since April; in Mumbai, SEBI's chairman laid out a five-day entry path for the foreign investors already buying Indian equities at a record pace. "
 "The long read: Nvidia - the company that bet on zero-billion-dollar markets.")
ed['intro'] = ("The 5-minute lead route is first; sections carry the detail. "
 "The long read: founded over breakfast at a Denny's in 1993, nearly dead in 1996, the inventor of the GPU and the company the AI decade crowned - now facing its first SEC probe. Thirty-three years of Nvidia.")
ed['hero'] = {'img': 'photos/d48-hero.jpg', 'alt': 'Abstract plate: a magnifying glass held over a glowing ledger, a red ticker ribbon falling behind it'}

groups = []

groups.append({'heading': 'The 5-minute lead route', 'blocks': [
 p(" Two regulators, one weekend. The SEC's enforcement staff is scrutinizing potential accounting issues at Nvidia - what the issues are, and whether they become a case, is unknown - while in Mumbai, SEBI chairman Tuhin Kanta Pandey used a CII summit to promise foreign investors a five-business-day path into the Indian market (%s; %s)." % (a(REUTERS_SEC,'Reuters'), a(ET_SEBI,'ET'))),
 p(" The worst week since April, by the numbers. Nvidia closed Friday at $125.53, down 13.8%% on the day and 23%% on the week - its sharpest weekly pullback in 18 years, a seventh straight weekly drop that has taken 46%% off the price; the Nasdaq fell 10%% on the week, its worst since the Covid crash of 2020, and the S&P 500 closed under its 200-day moving average for the first time since April after a seventh straight loss, the longest streak since 2020 (%s; %s)." % (a(CNBC_SELLOFF,'CNBC'), a(VERGE_NVDA,'The Verge'))),
 p(" The probe, precisely. What is established: enforcement staff are examining potential accounting issues, per two people briefed; the SEC declined comment and Nvidia did not respond. What is not established: when the probe opened, which accounting questions it covers, whether it becomes an enforcement action. Investigations are not evidence of wrongdoing, and many close without action."),
 p(" Mumbai's record month held through the storm. Foreign investors bought all five sessions - about Rs 32,600 crore on the week and Rs 1.12 lakh crore so far in November, roughly two and a half times October's record selling; the Nifty closed above 25,800 for the first time since February (%s)." % a(ET_FLOWS,'ET')),
 p(" ANT, settled. Anthropic's second session closed at $88.91, down 8.5%%, per Nasdaq's official record - the print this paper corrected to on Saturday morning. The first analyst initiations split: Seaport started at neutral, William Blair at outperform (%s)." % a(CNBC_CALLS,'CNBC')),
 p(" SEBI's Saturday slate. Five-day FPI onboarding with a consultation paper to cut compliance; KYC review cycles stretched from one year to two and from three to eight; remote re-KYC for NRIs; a domestically governed AI model for the securities market; a corporate-bond market-making framework with the RBI; about 2,000 more SME listings as the stated goal (%s; %s)." % (a(ET_SEBI,'ET'), a(REDIFF_SEBI,'Rediff'))),
 p(" The week ahead. India: the November F&O expiry Monday, exchanges closed Tuesday for Guru Nanak Jayanti, Mahanadi Coalfields' allotment Wednesday and listing Friday, both tentative. US: October's core PCE Wednesday, Thanksgiving Thursday, a 1 PM close Friday with Black Friday as the consumer test (%s)." % a(CNBC_WEEK,'CNBC')),
 p(" One concept: circular financing - the loop at the heart of the accounting questions, and how to read it without a conspiracy board."),
 p(" The long read: Nvidia - the company that bet on zero-billion-dollar markets. The Denny's founding, the chip that nearly killed it, the GPU, the decade spent seeding CUDA, and the week the SEC came looking."),
]})

groups.append({'heading': 'Front page', 'blocks': [
 p(" The SEC story, exactly as far as it goes. Enforcement staff are scrutinizing potential accounting issues at Nvidia, Reuters reported Friday, citing two people briefed on the matter; the Wall Street Journal had first reported a probe on Tuesday, without the accounting focus. When the examination opened and precisely which issues it covers are undetermined; the SEC declined to comment and Nvidia did not respond to questions. The wire's own caution is the right one: investigations are not evidence of wrongdoing, and many close without action (%s)." % a(REUTERS_SEC,'Reuters')),
 p(" The tape voted before the news. Nvidia's shares were already down more than 6%% on Friday before the Reuters report landed, then extended to close at $125.53, down 13.8%% - after Thursday had printed a 52-week low. The week cost the stock 23%%, its sharpest weekly pullback in 18 years, and the seven-week slide now totals 46%%; the S&P 500's seven straight losses are its longest streak since 2020, the index closed below its 200-day moving average for the first time since April, and the VIX sits above 30 (%s; %s)." % (a(CNBC_SELLOFF,'CNBC'), a(VERGE_NVDA,'The Verge'))),
 p(" Three threads run through the accounting story. First, Singapore: the FT, citing company accounts, reports that after Nvidia switched geographic revenue reporting from billing address to customer headquarters last year - a change that removed Singapore from the breakdown, so that sales routed through the city-state now land in their buyers' home countries - sales booked to Singapore soared to almost half of global revenue in the company accounts the FT examined. Second, circular financing: the SEC's enforcement chief David Woodcock told Reuters last month the agency is examining AI companies' corporate disclosures, alongside a new financial reporting and accounting unit inside enforcement. Third, the deal book: the Justice Department is reviewing the $12.9 billion Hugging Face acquisition and running a broader antitrust review. On the record, interim CEO Colette Kress told Tuesday's earnings call the company is proud of supporting the AI industry and %s about AI financing deals (%s)." % ('"would be far more selective moving forward"', a(REUTERS_SEC,'Reuters'))),
 p(" SEBI's five-day door. Foreign portfolio investors should be onboarded within five business days, chairman Tuhin Kanta Pandey said Friday, with a consultation paper to review compliance requirements and a Sebi-RBI joint working group on a common application form; trusted-jurisdiction FPIs are already inside a five-day window. From 1 December, KYC review cycles stretch from one year to two and from three to eight by category, and NRIs, OCIs and foreign nationals can complete KYC remotely. Also on the slate: a corporate-bond market-making framework with the RBI and the finance ministry, a review of the SME IPO framework and the Innovators Growth Platform - with roughly 2,000 additional SME listings the goal over the next few years - and a single-fine LODR mechanism with no duplicate disclosures (%s)." % a(ET_SEBI,'ET')),
 p(" Friday's provisional flow print held. Foreign investors bought a net Rs 10,308.42 crore on Friday - matching the provisional figure this paper printed Saturday - taking the week to about Rs 32,600 crore with buying in all five sessions, and November to roughly Rs 1,11,900 crore, about two and a half times October's Rs 45,162 crore of selling. Domestic institutions sold for a third straight week, about Rs 12,700 crore, but the selling halved from the prior two weeks; net institutional buying for the week stands near Rs 19,900 crore. One foot is hedged: FII index-futures net shorts have grown to about 70,450 contracts from 55,900 - cash buying with insurance attached. The Nifty gained 2.6%% on the week and is up 14%% in four (%s)." % a(ET_FLOWS,'ET')),
 p(" The ecosystem repriced the week. Anthropic's first initiations split the street: Seaport Research started at neutral with no price target - revenue growth slowed sharply in the third quarter, a buy-later stance - while William Blair opened at outperform, arguing the market risks missing the forest for the trees; Oppenheimer, valuing Amazon's stake at about $339 billion with a 15%% holding-company discount, raised its Amazon target to $310 from $285. Anthropic ended Friday at $1.6 trillion fully diluted - behind only Apple, Microsoft, Alphabet, Nvidia, Amazon and SpaceX - on $141 billion of private capital raised as of September and a third quarter that produced $1.72 of revenue per compute dollar, up from $0.68 a year earlier (%s)." % a(CNBC_CALLS,'CNBC')),
 p(" The venture math behind it. Menlo and Lightspeed each hold roughly $25 billion at the IPO price, Bessemer about $10 billion, and Menlo has already delivered more than $1 billion to at least five of its LPs, Matt Murphy told CNBC's Faber. Jay Ritter's data frames the cycle: VC-backed IPOs raised $73 billion in 2021 against $39 billion total across 2022-25, and 126 tech IPOs priced in 2021 against 34 in 2025; SpaceX's June listing was the largest until this week, and OpenAI is eyeing 2027 (%s)." % a(CNBC_SELLOFF,'CNBC')),
 p(" Where the strategists stand. Positioning is washed out by several measures - the VIX above 30 for the first time since March, the S&P's RSI below 30, the index 11.6%% under its 6 October record with the tech sector down 24.7%% in that span (%s). Goldman's Ben Snider holds an 8,700 target for end-2027, up 17%%, calling this \"the beginning of the middle\"; BofA's Michael Hartnett warns the hard-landing risk grows in 2027 if the Fed turns tough after the midterms; Fairlead's Katie Stockton tells clients not to sell weakness but to use rallies to reduce exposure (%s)." % (a(REUTERS_BF,'Reuters'), a(CNBC_WEEK,'CNBC'))),
]})

groups.append({'heading': 'Markets', 'blocks': [
 p(" The week's final prints, no new session. New York: S&P 500 6,910.39 after Friday's 3.7%% fall - a correction, more than 10%% under the 6 October record, and the worst week since April; the Nasdaq lost 10%% on the week, its worst since 2020; chips led the damage Friday - Micron -13.9%%, Nvidia -13.8%%, AMD -13.3%%, Broadcom -12.1%% (%s; %s; %s). Asia had its worst week since 2020 - the Nikkei fell 5.1%% on Friday alone. Mumbai: Sensex 83,919.71 and Nifty 25,800.60, up 2.9%% and 2.6%% on the week (%s). The rupee closed at a seven-month high of 92.67 (%s). Gold settled the week down 9.47%% at $3,512.30 (%s); WTI settled at $83.41 and Brent at $92.57 on fresh Gulf strikes (%s)." % (a(AP_NPR,'AP'), a(CNBC_SELLOFF,'CNBC'), a(VERGE_NVDA,'The Verge'), a(BS_WRAP,'Business Standard'), a(RUPEE_BL,'BusinessLine'), a(GOLD_DJ,'Dow Jones Data Talk'), a(OIL_NQ,'Newsquawk'))),
 p(" The consumer file going into Black Friday. Oxford Economics expects holiday sales up 4.2%% (2.2%% after inflation); the NRF projects 182.7 million shoppers, down from 186.9 million last year; October retail sales were moderate with the core reading beating; Walmart and Target guided upbeat; gasoline at $3.69 a gallon against $4.28 a month ago and $3.10 a year ago. Dell and Analog Devices, both reporting this week, could sway the AI trade as much as any store tally (%s)." % a(REUTERS_BF,'Reuters')),
]})

groups.append({'heading': 'IPOs', 'blocks': [
 p(" Mahanadi Coalfields goes into its final day cold. The Coal India arm's Rs 8,981.12-crore offer (Rs 129-136 a share) closed day two at 0.49 times subscribed - QIBs ex-anchor 1.37 times, retail 0.25, non-institutional 0.18 - and the grey-market premium thinned to a rupee or two by Friday evening (%s; %s). The book closes Monday; allotment is tentatively Wednesday and listing Friday, in a week shortened by Tuesday's Guru Nanak Jayanti closure." % (a(MAH_HDFC,'the day-two tally'), a(MAH_GR,'Goodreturns'))),
 p(" The pipeline widened. SEBI issued observations to Arohan Financial Services - a Rs 600-crore fresh issue including a Rs 120-crore pre-IPO placement plus an offer for sale of 4.04 crore shares, with TIAA, Aavishkaar Goodwell, Tano, Maj Invest, a Danish SDG fund and the Michael & Susan Dell Foundation among the sellers - and to Pristine Logistics & Infraprojects, the rail-focused multimodal operator promoted from Indian Railways and CONCOR that acquired Sical Logistics and filed through the confidential route in June; Advanced Sys-Tek and Assetz were also cleared. Regular-route issuers have twelve months to launch, confidential filers eighteen with an updated DRHP (%s). And Razorpay is expected to file its updated DRHP next week, with roadshows to follow and a February 2027 listing in sight (%s)." % (a(MC_IPO,'moneycontrol'), a(HT_RAZOR,'HT'))),
]})

groups.append({'heading': "Top movers - Friday's board stands", 'blocks': [
 p(" With no weekend session, Friday's verdicts remain the live board going into Monday's expiry session (percentages computed from BSE's official closes against Thursday):"),
 movers_chart_47,
 p(" What moves it next: Monday is the November F&O expiry and Asia's first session digesting the second leg of the US rout; the decoupling that carried this board all week gets its real test at 9:15."),
]})

groups.append({'heading': 'Corporate actions', 'blocks': [
 p(" Next week's calendar, per upstox's compilation: Pashupati Cotspin trades ex-interim on Monday; Wednesday is Zee Entertainment's buyback record date - up to Rs 600 crore at Rs 91 a share - plus rights issues from Bonlon Industries, Indergiri Finance and Vellora Impact; Friday brings Fusion CX's final dividend and Varvee Global's stock split, Rs 5 to Rs 2. The record date is the line that decides whose shares qualify to tender or receive - holders as of Wednesday evening own the Zee entitlement. One caution for the diary: the exchanges are closed Tuesday 24 November for Prakash Gurpurb Sri Guru Nanak Dev - a four-day trading week (%s)." % a(NEXTWK,'upstox')),
]})

groups.append({'heading': 'Finance Goldmine', 'blocks': [
 p(" One term worth owning: the 200-day moving average. It is the mean of the last two hundred daily closes - the market's slowest widely watched trendline - and the S&P 500 closed under it Friday for the first time since April (%s). The line has no magic in it; its power is administrative: systematic strategies cluster their de-risking triggers at the same well-marked levels, so a close through one can force selling that has nothing to do with anyone's view of earnings. Trend-following funds, risk mandates and a generation of chart-watchers treat a close below it as a regime change, so the line tends to matter most exactly where everyone else is already watching - which is what turns a statistic into a level." % a(CNBC_SELLOFF,'CNBC')),
 p(" Buying with one hand, insuring with the other. The same foreign investors who put Rs 1.12 lakh crore into Indian cash equities this month have lifted their index-futures net short to about 70,450 contracts, from 55,900 - a hedge that profits if the market falls, offsetting part of the cash book (%s). Read together, the two positions are not conviction and its opposite; they are one trade sized for a world where the AI selloff has a second leg. JPMorgan India CEO Pranav Chawda made the same point this week: part of the recent inflow is AI-trade hedging, and its durability depends on AI capex turning into actual investment (%s)." % (a(ET_FLOWS,'ET'), a(TOI_CHAWDA,'TOI'))),
]})

groups.append({'heading': 'Startup Intelligence', 'blocks': [
 p(" The week's cheques. Indian startups raised $291.3 million across 22 deals between 16 and 20 November - up 1,056%% from the prior week's $25.2 million - with AI taking $114 million across seven deals and Accel the most active investor (%s). The fresh names: Dreamteam raised $53 million for an AI-native CRM built by Freshworks alumni, backed by Together Fund, Accel and Premji Invest (%s); Bharat Semi raised a $24 million seed for AI sensor chips, co-led by Redstart Ventures and Info Edge with South Park Commons and others (%s); Style Union raised $51.8 million, Boba Bhai $18 million, and August AI $12 million. On the funds side, Oister Global set up a Rs 600-crore deeptech Category-II AIF (Rs 400 crore plus a Rs 200-crore greenshoe), and Mufin Green Finance's board approved buying 23%% of BimaPay for Rs 65.8 crore in cash." % (a(INC42,'Inc42'), a(DREAMTEAM,"the company's own post"), a(BSEMI_TC,'TechCrunch'))),
 p(" The week's template: run the company from a repo. Rob Snyder's Physics of Startups handed its pages this week to Robin, founder of TalkToHumans, who open-sourced his PULL lab: every call transcript, customer, outbound attempt and Stripe event lives in plain markdown files an AI can read - the company brain - with the PULL product-market-fit framework encoded as prompts on top, naming the repeatable case study, prepping each sales call, coaching from the live transcript and running a weekly loop that names the bottleneck. His own framing is the lesson: the system keeps catching him doing the comfortable thing instead of the right one. The template is a free GitHub repo (%s; %s)." % (a(PULL_POST,'the post'), a(PULL_REPO,'the repo'))),
 p(" Today's startup idea: FPI onboarding, as a service. SEBI wants foreign investors inside the market within five business days, with remote re-KYC for NRIs and a common application form being drafted with the RBI. Every custodian, broker and law firm that shepherds an FPI through that door now runs the workflow by hand - document collection, KYC category mapping, depository and tax registrations, renewal calendars on the new two- and eight-year cycles. The product is the compliance rail itself: one dashboard that takes a foreign fund from application to trading day, flags what is missing, and wakes up before each re-KYC lapses. The buyer is the custodian's operations head, the wedge is the five-day promise, and the model writes itself: a per-onboarding fee plus a renewal-calendar subscription on the new two- and eight-year cycles. The regulatory clock that creates the market just started (%s)." % a(ET_SEBI,'ET')),
]})

groups.append({'heading': 'AI Race', 'blocks': [
 p(" Apple is building its agent. Apple's own job listings describe a %s: a system that writes code, browses the web, controls applications and navigates devices, with travel, reservations, briefings and software help as the named uses; the listings name OpenAI, Anthropic, Meta and Google as the competitive set, and the timing - as soon as the end of next year - is early-stage and tentative (%s; %s). Every platform company now has an agent project on the board; Apple's entry says the race's next leg is who operates the phone, not who answers the prompt." % ('"proactive, agentic AI assistant"', a(APPLE_INV,'Bloomberg, via investing.com'), a(APPLE_VERGE,'The Verge'))),
 p(" OpenAI opened the storefront wider. Businesses outside the US can now claim their business in ChatGPT and publish agents - the business hub OpenAI launched on 10 November, which lets a company claim its profile, keep its information current, and see how people engage with it inside the assistant - claiming and agent-publishing run on different eligibility terms (%s; %s). Meanwhile in Mumbai, the market's own regulator wants a sovereign model: SEBI is exploring a domestically governed AI model for the securities market, built on digital public infrastructure, with a committee weighing the risks and opportunities, hallucination guardrails included, and the work still at an initial stage; its existing AI tools already watch intermediary ads and compliance reports (%s)." % (a(OAI_BIZ,'OpenAI'), a(OAI_HELP,'the setup guide'), a(REDIFF_SEBI,'Rediff'))),
]})

groups.append({'heading': 'Vibe coding', 'blocks': [
 p(" One call, whole page. Cloudflare's Browser Run added a /snapshot endpoint this week: a single request returns a page as PDF, its links, scraped elements and extracted JSON in one pass - the four artifacts an agent usually stitches together from four tools (%s). Think of the uses: an agent that reads a vendor's documentation as structured JSON, a monitor that captures a pricing page to PDF every morning, a scraper that needs the rendered DOM, not the raw HTML. It is a quick action inside Browser Run, billed as browser hours, and it runs on the free Workers plan (ten minutes of browser time a day, three concurrent browsers) (%s; %s). The same week's changelog also moved two WAF managed rules - phpAfterShell and ruby2shell - onto the free plan. The pattern worth noticing: the scaffolding layer of the agent economy keeps collapsing into single API calls - this week, page capture became one." % (a(CF_CHANGE,'the changelog'), a(CF_SNAP,'the docs'), a(CF_PRICE,'pricing'))),
]})

groups.append({'heading': 'Try this today (Sunday)', 'blocks': [
 p(" Snapshot a page yourself. Create a free Cloudflare account, mint an API token with Browser Run permissions from the dashboard's API-tokens page, and POST one URL to the /snapshot endpoint with the token as a bearer header - you get back a PDF, the link list, the scraped content and structured JSON of the same page in one response (%s). Access and limits, from Cloudflare's own pages: quick actions like /snapshot are billed as browser hours; the Workers Free plan includes ten minutes of browser time per day and three concurrent browsers, so keep tests to a handful of pages; a 429 means the daily budget is spent (%s; %s). One house rule from this desk: only snapshot pages you are allowed to fetch." % (a(CF_SNAP,'the endpoint docs'), a(CF_PRICE,'pricing'), a(CF_CHANGE,'the changelog'))),
 p(" Then run the owning-document drill on the week's biggest story. Read the Reuters probe report once (%s), then read Nvidia's own investor FAQ (%s), and write down three columns: what the wire established, what it could not establish, and what only the company's filings can settle. Ten minutes, and you will read every probe story differently - the gap between column one and column two is where most of the weekend's commentary lives." % (a(REUTERS_SEC,'the story'), a('https://investor.nvidia.com/investor-resources/faqs/','the FAQ'))),
]})

groups.append({'heading': 'One concept: circular financing', 'blocks': [
 p(" Circular financing - the loop the SEC is now staring into. The mechanics: a supplier invests in its own customer, the customer spends the investment on the supplier's product, and the supplier books the spending as revenue - money making a round trip that leaves a sale behind. The practice has a pedigree: in the late-1990s telecom bubble, equipment makers like Lucent and Nortel lent carriers the money to buy their own gear, and when the carriers defaulted, the revenue proved to have been borrowed from the future. Nothing about the loop is illegal by itself - companies may invest in customers, and customers may buy - which is exactly why the accounting questions matter: whether the revenue is real demand or financed demand, and whether the disclosures let an investor tell the difference. That distinction, not the existence of the deals, is what an examination like this week's exists to test. For the reader, the tell to watch in any filing season is the gap between revenue growth and cash collection - financed demand spends slower than it books (%s)." % a(REUTERS_SEC,'Reuters')),
]})

groups.append({'heading': 'Setup board', 'blocks': [
 p(" Sunday's board is a carry-forward: no weekend session, so Friday's prices stay the live marks and Monday's expiry session is the next scored day. Friday left the long side's best session of the week on the tape - Kotak +3.08%% near the day's high, Hindalco +2.34%% reclaiming its zone, JSW Steel at its high for a second straight session - with no stop, no target, no invalidation, and no watchlist name newly clearing the published screen. Monday is the F&O expiry and the Mahanadi close; the desk's rule stands: every published setup stays on the board until it completes (target hit) or fails (stop hit). Per-share prices on every line; the Rs 1,500 price cap screens what qualifies as a setup."),
 setup_chart1,
 setup_chart2,
 p(" The ledger is unchanged: HCLTech, filled 28 October at the worst fill of Rs 1,378.00, target Rs 1,466.80 taken out at 1,468.00 - gross +6.53%%, net +6.23%% after the 0.3%% cost convention - closed Friday at Rs 1,337.00. Infosys, resolved Wednesday by invalidation, no trade, no P&L, closed at Rs 1,096.40 (+0.54%%), holding above the 1,072.60 low it printed on the way down. Research, not advice; cash-only swing setups under Rs 1,500 a share; BSE official prints are the standard."),
]})

groups.append({'heading': 'How the board scores', 'blocks': [board_rows]})

groups.append({'heading': "The editor's read", 'blocks': [
 p(" Two regulators, one weekend, one trade. In Washington, the agency that polices disclosure is examining the books of the company the AI decade was built on. In Mumbai, the agency that polices India's markets is widening the door for the foreign money already arriving at a record pace - money that is, in part, the same trade seen from the other end. The correction and the record month are not two stories; they are one repricing with two addresses."),
 p(" Keep the probe in its box. The stock fell more than 6%% before the Reuters story existed - the tape's verdict on the week was already in - and everything established so far fits in one sentence: enforcement staff are looking at potential accounting issues. No charges, no findings, no named issues. The honest way to hold the story is the way this paper holds every early file: the probe is a question, and questions about accounting at the market's most important company are worth front-page space without being worth a verdict."),
 p(" The hedge is the tell. Foreign investors are buying Indian equities at a record pace and shorting index futures at the fastest rate in months - Rs 1.12 lakh crore of cash buying wrapped in 70,450 contracts of insurance. That is not the posture of money that believes the decoupling is permanent; it is the posture of money renting it. Monday's expiry session, after Asia's worst week since 2020, is the first honest test of how long the rental runs."),
 p(" What settles it: Wednesday's core PCE print for the inflation file, Friday's Black Friday tape for the consumer file, and the December calendar - the Fed on the 9th, the RBI on the 4th, Q2 GDP on the 30th - for the rate file. And for the probe file: nothing on a schedule, which is its own lesson. Filings, not headlines, will answer it."),
]})

groups.append({'heading': 'The week ahead', 'blocks': [rows([
 row(1, 'Sun 22 Nov', 'No trading. The paper runs as usual.'),
 row(2, 'Mon 23 Nov', 'November F&O monthly expiry; Mahanadi Coalfields\' book closes (0.49 times after day two); ANT\'s third session after a -8.5% second day; S&P Global flash PMIs; HPE and Agilent report in the US.'),
 row(3, 'Tue 24 Nov', 'Indian exchanges closed for Prakash Gurpurb Sri Guru Nanak Dev. US: ADP weekly, Consumer Confidence, FHFA house prices; Dell, HP, Workday, Best Buy and Analog Devices report.'),
 row(4, 'Wed 25 Nov', 'October core PCE, personal income, Q3 GDP second estimate, durables and claims in the US; Mahanadi allotment (tentative); Zee\'s Rs 600-crore buyback record date.'),
 row(5, 'Thu 26 - Fri 27 Nov', 'NYSE closed Thursday for Thanksgiving; Friday is a 1:00 PM ET close with Black Friday as the consumer test - Oxford Economics sees holiday sales up 4.2%; Mahanadi lists Friday (tentative).'),
 row(6, 'Watching', 'Q2 GDP on 30 November; the RBI\'s MPC on 4 December with a hike in play if inflation stays above tolerance (Geojit\'s Nair); the Fed on 9 December; Nvidia\'s next filing for what the probe-era disclosures say.'),
])]})

groups.append({'heading': 'Notes on this edition', 'blocks': [
 bullets([
  "Sources read for this edition: Reuters' exclusive on the SEC's Nvidia examination; CNBC for the week's tape, the analyst initiations and the US calendar; The Verge for the 52-week low and the seven-week slide; the FT's Singapore reporting as cited by Reuters; ET for the SEBI slate and the week's flows; Rediff for SEBI's AI model; TOI for the JPMorgan India interview; Business Standard for the Mumbai close; moneycontrol for the SEBI IPO observations; HT for Razorpay; Inc42, the companies' own posts and TechCrunch for the startup tally, with the PULL lab template from Rob Snyder's Physics of Startups and its GitHub repo; Bloomberg via investing.com and The Verge for Apple's agent; OpenAI's own post and help center for Businesses in ChatGPT; Cloudflare's changelog, docs and pricing pages for /snapshot; HDFC Sky and Goodreturns for the Mahanadi book; upstox for the corporate-actions calendar; AP's final close wire (via NPR), Dow Jones Data Talk (via Morningstar), Newsquawk and BusinessLine for Friday's prints. Research, not advice.",
  "ANT's close is stated at $88.91, down 8.5%, per Nasdaq's official record - the print Ed47 was corrected to on Saturday morning; an earlier AP wire carried a preliminary $88.30.",
  "No US close table in this edition: there has been no new session since Friday's final prints, which Ed47 carried in full on Saturday.",
 ]),
 closing(" That's the paper for Sunday. Monday brings the expiry, the Mahanadi close, and the decoupling's first real test. See you tomorrow."),
]})

ed['groups'] = groups
d['edition'] = ed
json.dump(d, open('editions-src/day-48.json', 'w'), indent=2, ensure_ascii=False)
print('wrote editions-src/day-48.json:', len(groups), 'groups')
