#!/usr/bin/env python3
"""Add longreads.json['51'] - Dixon Technologies: the factory behind the brands."""
import json

def a(url, txt):
    return '<a href="' + url + '" target="_blank" rel="noopener">' + txt + '</a>'

def F(template, *args):
    out = template
    for arg in args:
        out = out.replace("%%", arg, 1)
    return out

def p(html):
    return {"t": "p", "html": html}

DRHP = "https://www.sebi.gov.in/sebi_data/attachdocs/may-2017/1495451226044.pdf"
DIXON = "https://dixoninfo.com/"
IBEF = "https://www.ibef.org/industry/electronics-system-design-manufacturing-esdm/showcase/dixon"
COUNTERPOINT = "https://counterpointresearch.com/en/insights/India-Smartphone-Production-up-8-percent-YoY-in-2025-Dixon-Leads-EMS-Rankings-Bhagwati-Enters-Top-5"
ET = "https://economictimes.indiatimes.com/markets/stocks/news/dixon-technologies-shares-gain-11-after-q2-revenue-jumps-47-yoy/articleshow/135449583.cms"
FORBES22 = "https://www.forbesindia.com/article/2022-manufacturing-special/dixon-technologies-from-a-single-factory-in-1993-to-a-rs-10700-crore-electronic-manufacturer-for-the-world/77859/1"
FORBES24 = "https://www.forbesindia.com/article/leadership-awards-2024/sunil-vachani-in-a-relentless-pursuit-of-excellence-for-global-domination/91939/1"
EY = "https://www.ey.com/en_in/entrepreneur-of-the-year/winners-2021/sunil-vachani"

lr = {
    "title": "The factory behind the brands",
    "fact": ("A Slow Burn long read, Wednesday 25 November 2026. In 1993, in a rented 10,000-square-foot shed in "
             "Noida, twenty-three-year-old Sunil Vachani started assembling televisions with Rs 15 lakh borrowed from "
             "his father. Thirty-three years on, his company runs thirty factories, makes phones and televisions for "
             "more than a hundred global brands, and leads India's smartphone contract-manufacturing rankings - on a "
             "3.1% margin. This is how Dixon Technologies got built."),
    "thumb": "photos/lr51-hero.jpg",
    "hero": {"img": "photos/lr51-hero.jpg",
             "alt": "Abstract plate: a long assembly line receding toward a bright doorway, unmarked white boxes on the line, each box faintly reflecting a different coloured logo, early morning light",
             "caption": "Abstract plate for the long read - one line, a hundred brands, no name on the box."},
    "groups": [
        {"heading": "1. Weston's son", "blocks": [
            p(F("The company was incorporated at Alwar, Rajasthan, on 15 January 1993 as Weston Utilities Limited - the father's name inside the son's company. It became Dixon Utilities and Exports that July, Dixon Technologies (India) Private Limited in January 2006, and a public limited company on 2 May 2017 (%%).", a(DRHP, "the draft red herring prospectus"))),
            p(F("Sunil Vachani was 23, back from American College London, with one failure already behind him: a cordless-phone factory in 1989-90 that never took. He trained at his father Sundar Vachani's Weston, which made televisions - a business hit hard by the collapse of the Soviet Union, then a major buyer of Indian electronics (%%; %%).", a(FORBES22, "Forbes India, 2022"), a(FORBES24, "Forbes India, 2024"))),
            p(F("The first Dixon factory: a rented 10,000-square-foot plot in Noida, a few machines, fifteen employees, and Rs 15 lakh borrowed from his father. Atul Lall, a Weston star who had joined in 1986, was sent along as mentor; he stayed as co-founder and vice-chairman (%%).", a(FORBES24, "Forbes India, 2024"))),
        ]},
        {"heading": "2. A dollar fifty a television", "blocks": [
            p(F("The first order came from Lucky-Goldstar - the Korean group not yet renamed LG, then only a representative office in India: a few thousand televisions for export, at a fee of a dollar fifty per set. We were so desperate for business, Vachani told Forbes India in 2024. When LG entered India properly, Dixon made its domestic televisions. Philips followed - durables, DVD players, audio systems, VCRs - and SEGA's gaming consoles (%%).", a(FORBES24, "the 2024 profile"))),
            p("The economics were thin from day one and stayed that way by design. The company was profitable from its first quarter, Vachani says, with a first-year profit of Rs 3 lakh. The fee-per-set model meant the customer owned the brand, the price and the risk; Dixon owned the line."),
            {"t": "figure", "img": "photos/lr51-int1.jpg", "alt": "Abstract plate: a single television chassis on a workbench, a small stack of dollar coins beside it, workshop shadows", "caption": "Abstract plate - a dollar fifty a set, and the line was running."},
        ]},
        {"heading": "3. What not to do", "blocks": [
            p(F("For eight or nine years the company made only CRT televisions; a 1997 shock to the export business taught the concentration lesson. In the early 2000s Dixon tried a brand of its own, and about two and a half years later abandoned the attempt. Sometimes the decisions of what not to do are far more important, Vachani said in 2022. Out of that retreat came the rule he describes as cast in stone: never compete with your customers (%%).", a(FORBES22, "Forbes India, 2022"))),
            p("The establishment was not impressed. Bureaucrats in the early 2000s told him India's future did not lie in electronics hardware - it was software. Funding was rejected repeatedly; one bank lent against secured exports. In three decades, Vachani says, the company has had exactly one loss-making year - an unhedged rupee-dollar position."),
        ]},
        {"heading": "4. The drill", "blocks": [
            p(F("In May 2008, Motilal Oswal Private Equity invested at a valuation under Rs 150 crore and installed the discipline: be the lowest-cost producer, watch return on capital employed, watch working capital, integrate backwards (%%).", a(FORBES22, "Forbes India, 2022"))),
            p("The same year brought the second product line: CFL lighting. Washing machines for Godrej followed. The company that had lived inside the television tube was becoming a platform - a factory for whatever a brand needed made."),
        ]},
        {"heading": "5. The listing", "blocks": [
            p(F("September 2017 brought the IPO - listing approvals on the 15th, trading from the 18th (%%). The trigger, Vachani has said, was an exit for Motilal Oswal. Forbes computed in 2022 that the split-adjusted listing price of Rs 352 had multiplied roughly ten times, to Rs 3,546. Vachani calls it among the most-subscribed EMS IPOs of its time - his claim, kept as his claim.", a(IBEF, "IBEF's milestone record"))),
            p(F("The prospectus preserves the economics at listing (%%): revenue of Rs 767 crore in FY13, Rs 1,389 crore in FY16, Rs 1,845 crore in the first nine months of FY17 - a 34.6% compound annual rate across FY13-16. And the production shares that justified the price, from Frost and Sullivan data in the document, for FY16: 50.4% of India's EMS/ODM flat-panel television production, 42.6% of washing machines, 38.9% of LED and CFL lights.", a(DRHP, "the DRHP"))),
            {"t": "figure", "img": "photos/lr51-int2.jpg", "alt": "Abstract plate: a brass listing bell on a wooden podium, out-of-focus factory lights behind it, morning haze", "caption": "Abstract plate - the bell, September 2017."},
        ]},
        {"heading": "6. The phone pivot", "blocks": [
            p(F("The mobile phone arrived through Padget Electronics, a joint venture making phones from 2016; the Nokia/HMD contract came in 2021. Then the production-linked incentive era: Dixon sits in five PLI schemes - mobile phones, IT hardware, telecom, LED components and AC components. Forbes walked the Padget Noida floor in 2022: the motherboard line running 24x7, automated, 40,000 units a day (%%).", a(FORBES22, "the 2022 profile"))),
            p(F("Xiaomi's smart televisions came from 2018, then its smartphones. Today the company calls itself India's number-one EMS: $5.18 billion of operating revenue, thirty manufacturing facilities, seven R&D centres, more than a hundred global brands (%%). Counterpoint's April 2026 rankings put Dixon on top of India's 2025 smartphone EMS table, production up 89% year on year on Motorola, realme and Xiaomi orders (%%); in the June quarter of 2025 it became India's largest smartphone maker by shipments - up 196%, past Samsung - per IBEF's record.", a(DIXON, "the company's own site"), a(COUNTERPOINT, "Counterpoint"))),
            {"t": "figure", "img": "photos/lr51-int3.jpg", "alt": "Abstract plate: a smartphone motherboard held in gloved hands under a magnifying lamp, circuit traces catching the light", "caption": "Abstract plate - forty thousand motherboards a day."},
        ]},
        {"heading": "7. The ledger", "blocks": [
            p(F("Then look at the margin. Q2 FY27 - July to September 2026, per the exchange filing reported by ET: revenue Rs 21,794 crore, up 46.7%; net profit Rs 343.7 crore, down 48.7%; EBITDA Rs 666 crore, down 37%; margin 3.1% against 7.1% a year earlier. The stock jumped 11% intraday on the day anyway - the market paid for the revenue line (%%).", a(ET, "ET's results report"))),
            p("The half-year softens the cut: H1 FY27 revenue of Rs 37,938 crore, up 35%; profit after tax of Rs 1,007 crore, up 13%. But the mirror is the story. A company can lead the country's smartphone production and keep about three paise of every rupee. The fee-per-set model from 1993 still runs the P&L."),
            p(F("The next integration is already approved: a joint venture with China's Longcheer - Dixon 74%, Longcheer 26% through its Singapore arm - cleared by the Ministry of Electronics and IT, for smartphones, tablets, wearables, AI PCs, automotive and healthcare electronics. FY26 capex of Rs 1,100-1,200 crore goes into displays, camera modules, optical transceivers and enclosures; a Signify OEM lighting joint venture from June 2025 and a Rs 1,000-crore Tamil Nadu laptop facility promising about 5,000 jobs sit alongside (%%).", a(IBEF, "IBEF"))),
            p(F("Vachani's own summary of the method is his father's advice: keep microscopic and telescopic vision at the same time. And the temperament: I am a paranoid entrepreneur - if we don't change with times, we might just be disrupted (%%). Forbes made him a billionaire in 2022, at $1.1 billion. The factory that began in the father's name now sits behind almost every brand name in an Indian electronics store - which is exactly where its founder wants it: visible nowhere, everywhere underneath.", a(EY, "the EY profile"))),
        ]},
    ],
    "audio": {"full": "audio/lr51-full.m4a", "durations": {}, "times": {"full": "audio/lr51-full.times.json"}},
}

path = "/downloads/morning-paper/editions-src/longreads.json"
d = json.load(open(path))
d["51"] = lr
json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
print("longreads['51'] written;", len(lr["groups"]), "groups")
