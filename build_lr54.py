#!/usr/bin/env python3
"""Add LR54 (TCS) to editions-src/longreads.json."""
import json

def A(url, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)

S1 = A('https://www.tata.com/newsroom/heritage/five-decades-transformation-tcs', "the Tata group's 2021 history of TCS")
S2 = A('https://www.tata.com/newsroom/heritage/fc-kohli-tcs-information-technology', "the Tata group's 2024 profile of Kohli")
S3 = A('https://www.tata.com/newsroom/heritage/tata-consultancy-services-tcs-timeline-1968', "the Tata group's TCS timeline")
S4 = A('https://science.thewire.in/economy/tech/f-c-kohli-india-information-technology-industry-ibm-tcs-burroughs/', "Dinesh C. Sharma's account in The Wire")
S5 = A('https://www.technologyreview.com/2013/01/02/180827/indias-it-guy/', "MIT Technology Review's 2013 profile of Kohli")
S6 = A('https://www.arabnews.com/archive/253471', "Reuters' report on the 2004 offer")
S7 = A('https://www.tcs.com/who-we-are/newsroom/press-release/tcs-financial-results-q2-fy-2027', "TCS's own results release")
S8 = A('https://www.moneycontrol.com/news/business/tcs-payout-to-tata-sons-falls-most-since-covid-even-as-new-business-losses-swell-to-rs-28-823-crore-13985725.html', "Moneycontrol's July report on the payout")
S9 = A('https://www.business-standard.com/article/beyond-business/tcs-the-complete-story-111092100102_1.html', "Business Standard's review of Ramadorai's book")
S10 = A('https://www.etnownews.com/companies/tcs-headcount-in-q2-results-adds-over-4200-as-attrition-holds-steady-at-13-3-ai-revenue-crosses-3-1-billion-article-156297913', "ET Now's results report")
TCSSITE = A('https://www.tcs.com/who-we-are', "TCS's own site")
HT = A('https://www.hindustantimes.com/business/tata-sons-adds-six-month-ipo-timeline-to-board-meet-agenda-101795654777767.html', "Hindustan Times reported")

def p(html):
    return {"t": "p", "html": html}

def fig(img, alt, caption):
    return {"t": "figure", "img": img, "alt": alt, "caption": caption}

lr = {
 "title": "The Tata computer room that became an export industry",
 "fact": "A Slow Burn long read, Saturday 28 November 2026. TCS dates its founding to 1968. It began as a computing room for Tata companies that barely used it, and it had to find customers outside the group to survive. A manager borrowed for a year, a government that tied a machine import to an export promise, and a software filter shipped across the world on tape turned that room into an export business. TCS, the Tata computer room that became an export industry.",
 "thumb": "photos/lr54-hero.jpg",
 "hero": {
   "img": "photos/lr54-hero.jpg",
   "alt": "Abstract plate: a large 1970s computer room seen from a doorway, tape reels and cabinets in soft silhouette, one window of morning light falling across an empty desk",
   "caption": "Abstract plate for the long read - a computer room, and the daylight that reached it."
 },
 "groups": [
  {"heading": "1. The room nobody used", "blocks": [
    p("TCS dates its founding to 1968 (" + TCSSITE + "). Its roots are a room. The Tata Computer Centre was meant to handle the data-processing work of all the companies in the Tata group, and it sat under-used. The group's headquarters at Bombay House remodelled it into a company: Tata Consultancy Services (" + S1 + "; " + S4 + ")."),
    p("The idea came from three management graduates of MIT - Lalit Kanodia, Nitin Patel and Ashok Malhotra - who had interned with the Tatas and prepared a project report on data centres; they were asked to carry it out. Yashpal Sahni, a postgraduate of the Indian Statistical Institute, was another founding member (" + S4 + ")."),
    p("The environment was hostile to the whole idea. At the time there were only a handful of computers in India. The government imposed severe restrictions and steep tariffs on importing mainframes, which it saw as pointless luxuries that threatened human jobs, and no private company had attempted such a purchase (" + S5 + "). The market itself belonged to two foreign firms, the American IBM and the British ICL, which imported used machines, refurbished them in India and leased them out at what The Wire calls exorbitant prices; an audit by the Comptroller and Auditor General found large-scale malpractice in their invoicing and pricing, and the government handed the problem to its new Department of Electronics (" + S4 + ")."),
  ]},
  {"heading": "2. A manager borrowed for a year", "blocks": [
    p("F.C. Kohli, an MIT master's graduate who had joined Tata Electric in 1951, had in 1968 put a dedicated mainframe in charge of Mumbai's power grid, a purchase that had to be cleared as a research project; MIT Technology Review says that put him ahead of all but a handful of American utilities (" + S5 + "). In late 1969 the group moved him to TCS. \"I was happy in Tata Electric and was reluctant to leave it,\" he told Dinesh C. Sharma in 2006, \"but I was asked to take charge of the new venture for a year.\" J.R.D. Tata had lobbied for him to take the job (" + S4 + "; " + S2 + ")."),
    p("What he found was a company that \"was up, but it wasn't running,\" in his words to MIT Technology Review; it took on management consulting projects to stay afloat (" + S5 + "). Group companies were reluctant to hand over their data-processing, and Kohli soon realised TCS would have to look for business outside the group. Its first outside customer, in 1971, was Bombay Telephones, which wanted to digitise its telephone directory in a World Bank-funded project; the same year came its first overseas assignment, for an electric company in Iran (" + S4 + "; " + S3 + ")."),
    p("The hardware was whatever could be had. TCS's first mainframe was an ICL 1903 that had never been used, bought for a fraction of its price from a government-owned insurance company after a union blocked installation of what it called a \"job-eating monster\". On it and two leased IBM machines, Kohli's programmers - recruited from the computer science graduates of IIT Kanpur - computerised TCS's in-house operations, inter-branch reconciliation for a large nationalised bank, and Mumbai's telephone directory (" + S5 + ")."),
    fig("photos/lr54-int1.jpg", "Abstract plate: a single mainframe cabinet in a bare room, still wrapped in its packing, a union notice pinned to the door in soft light", "An unused machine, bought cheap - the first mainframe, and the first constraint."),
  ]},
  {"heading": "3. No machine in the country", "blocks": [
    p("Kohli decided to work with Burroughs, IBM's closest rival, using his MIT contacts and his connections through the Institute of Electrical and Electronics Engineers. He visited the United States at least nine times between 1972 and 1974, and in 1974 TCS won a contract from the Detroit-based maker (" + S4 + "; " + S5 + ")."),
    p("The trouble, as Kohli later described it: \"We did not have a Burroughs machine in India - importing one would have taken two years. So we developed it on an ICL machine which we had. We designed a very advanced software filter for filtering from ICL to Burroughs machine.\" There were no data links in those years, so the code written in Bombay was shipped to the United States, tested on Burroughs machines there, and it worked (" + S4 + ")."),
    p("\"This convinced Burroughs that we can do something out of the box,\" Kohli said; Burroughs bought the software to migrate ICL machines to Burroughs in the United Kingdom. Contracts started to flow - from the Detroit Police, the City of Detroit, the State University of New York, banks - and Burroughs became TCS's first major steady overseas client. Tata and Burroughs also set up a separate software unit, Tata Burroughs Limited (" + S4 + "; " + S5 + "). The Tata group's timeline adds that in 1974 TCS delivered its first full software life-cycle project, a financial accounting package for building societies in Britain (" + S3 + "; " + S1 + ")."),
  ]},
  {"heading": "4. The import bargain", "blocks": [
    p("To deliver quality work, TCS needed a Burroughs mainframe of its own. The government consented to the import, but Kohli had to commit to exporting twice the machine's value over five years. The machine cost $340,000; with tariffs, TCS paid more than twice that. TCS kept the promise, and its success, MIT Technology Review says, led the government to rethink its position on computers and brought other Indian companies into the field (" + S5 + ")."),
    p("In 1976 TCS crossed $1 million in export revenue and won the top exporter award (" + S1 + "; " + S3 + "). A year earlier, addressing the annual meeting of the Computer Society of India at Ahmedabad, Kohli had said: \"There was an industrial revolution. We missed it due to reasons beyond our control. Today, there is a new revolution - a revolution in information technology... We have the opportunity to participate in this revolution on an equal basis... If we miss this opportunity, those who follow us will not forgive us for tardiness and negligence\" (" + S4 + ")."),
    fig("photos/lr54-int2.jpg", "Abstract plate: a magnetic tape reel and a shipping crate on a dockside table, a ledger page beside them with two columns of figures, hard afternoon light", "A tape, a crate and a ledger - the export bargain in three objects."),
  ]},
  {"heading": "5. Cutting the cord", "blocks": [
    p("In 1978 TCS parted ways with Burroughs and became independent; Tata Burroughs was formed separately (" + S3 + "; " + S4 + "). S. Ramadorai, who later ran TCS, called cutting the cord \"the best thing that happened to us\" (" + S9 + ")."),
    p("The decade after was an accumulation. A New York office on Park Avenue in 1979, and a contract that required 24-hour delivery cycles; in 1981 TRDDC in Pune, which the group's timeline calls India's first software research centre; in 1989 a securities-clearing deal with SEGA that the timeline calls the world's first real-time securities clearing; in 1992 the core platform for the new National Stock Exchange (" + S3 + "). The group's history says about 700 million lines of code were fixed for Y2K (" + S1 + "; " + S2 + ")."),
  ]},
  {"heading": "6. A sensitive topic", "blocks": [
    p("Kohli handed over to Ramadorai in the 1990s; Ramadorai led TCS for 13 years, until N. Chandrasekaran became CEO in 2009. Chandrasekaran became chairman of Tata Sons in 2017, Gopinathan took over as CEO that year, and K. Krithivasan has run TCS since 2023 (" + S3 + ")."),
    p("In 2002 TCS signed a $100 million contract with GE Medical, which the group's timeline calls the largest by an Indian firm at the time; in 2003 it crossed $1 billion in revenue; in 2012, $10 billion (" + S1 + "; " + S3 + ")."),
    p("In August 2004 TCS listed. The offer sold shares at Rs 850, raising Rs 5,420 crore ($1.17 billion) for a 13.3% stake, and Reuters reported the company valued at $8.78 billion (" + S6 + ")."),
    fig("photos/lr54-int3.jpg", "Abstract plate: a boardroom table with one empty chair at its head, a thick bound prospectus on the table and a window onto a harbour, soft evening light", "The decision to list - a sensitive topic at the head of the table."),
  ]},
  {"heading": "7. The company that pays the parent", "blocks": [
    p("TCS reported its September-quarter results on 8 October. Revenue was $7,642 million, up 0.2% on the quarter and 2.4% on the year in dollars, and Rs 73,188 crore, up 11.2% in rupees. The operating margin was 24.0% and the net margin 19.0%. Net profit was Rs 13,884 crore. The company said its AI revenue now runs at $3.1 billion a year, more than a tenth of the total, and total contract value for the quarter was $9.6 billion (" + S7 + "; " + S10 + "). It employs 598,056 people, with attrition at 13.3%, and declared a dividend of Rs 12 a share (" + S10 + "; " + S7 + ")."),
    p("For Tata Sons, TCS is the main recurring source of cash. Moneycontrol reported in July that Tata Sons received Rs 28,291 crore in dividends from TCS in financial year 2026, down 12% from a record Rs 32,184 crore the year before, and that Air India, Tata Digital and Tata Electronics together lost Rs 28,823 crore in 2026, by its calculation (" + S8 + "). On Friday TCS closed at Rs 2,575.00 on BSE, down 2.46%."),
    p("Monday the Tata Sons board meets while two of the Tata trusts are in court over the reappointment of its chairman. Hindustan Times reported that its agenda includes a six-month timeline for a public offering of Tata Sons itself (" + HT + "). In 2004 the same parent had to decide whether to let the company it built from an unused room go public; Business Standard's review of Ramadorai's book records that raising it with Tata Sons was \"a sensitive topic\" (" + S9 + ")."),
  ]},
 ],
}

path = '/downloads/morning-paper/editions-src/longreads.json'
d = json.load(open(path))
d['54'] = lr
json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
print('added LR54; keys now:', sorted(d.keys(), key=int)[-3:])
