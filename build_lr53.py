#!/usr/bin/env python3
"""Add LR53 (Asian Paints) to editions-src/longreads.json."""
import json

A_COMP = '<a href="https://www.asianpaints.com/about-us.html" target="_blank" rel="noopener">the company\'s own profile</a>'
A_HBL = '<a href="https://www.thehindubusinessline.com/books/book-review-the-rise-of-asian-paints-champaklal-choksey-a-doyen-of-the-indian-paints-industry/article68505518.ece" target="_blank" rel="noopener">Anupam Gupta\'s biography of Champaklal Choksey</a>'
A_FORBES = '<a href="https://www.forbes.com/sites/forbesasia/2013/08/28/asian-paints-brightens-up-indias-growing-middle-class/" target="_blank" rel="noopener">Forbes Asia\'s 2013 profile</a>'
A_IT = '<a href="https://www.indiatoday.in/magazine/economy/story/19970908-british-major-icis-acquisition-of-91percent-stake-in-asian-paints-raises-spectre-of-takeover-830509-1997-09-07" target="_blank" rel="noopener">India Today reported in September 1997</a>'
A_BS = '<a href="https://www.business-standard.com/article/specials/icis-9-1-stake-in-asian-paints-the-facts-behind-the-case-197082201109_1.html" target="_blank" rel="noopener">ICI\'s own statement of the facts</a>'
A_TBI = '<a href="https://thebetterindia.com/235561/independence-day-quit-india-asian-paints-garage-success-story-swadeshi-brand-india-gop94/" target="_blank" rel="noopener">as The Better India recounts it</a>'
A_MC = '<a href="https://www.moneycontrol.com/news/business/earnings/asian-paints-q2-results-net-profit-rises-7-5-to-rs-1-068-crore-revenue-jumps-17-14063439.html" target="_blank" rel="noopener">its September-quarter results</a>'
A_GRASIM = '<a href="https://www.grasim.com/media/press-releases/aditya-birla-group-set-disrupt-paint-industry-40-percent-addition-industry-capacity-birla-opus" target="_blank" rel="noopener">Grasim\'s own launch announcement</a>'

def p(html):
    return {"t": "p", "html": html}

def fig(img, alt, caption):
    return {"t": "figure", "img": img, "alt": alt, "caption": caption}

lr = {
 "title": "The company that outlasted its founders",
 "fact": "A Slow Burn long read, Friday 27 November 2026. In 1942, with wartime Britain choking off paint imports, four friends started making paint in a South Bombay garage. Twenty-five years later their company was India's largest paintmaker. Thirty years after that, the family of the man who built it sold every share - and the company they left behind kept right on growing. Asian Paints, the company that outlasted its founders.",
 "thumb": "photos/lr53-hero.jpg",
 "hero": {
   "img": "photos/lr53-hero.jpg",
   "alt": "Abstract plate: a row of four empty chairs at a long table, behind them a wall of paint swatches in daffodil and aquamarine, one swatch brighter than the rest, morning light",
   "caption": "Abstract plate for the long read - four chairs, one wall, and a company that kept its seat at the top."
 },
 "groups": [
  {"heading": "1. The boycott year's garage", "blocks": [
    p("In the August of 1942, as the Quit India movement filled Bombay's streets, the British government slapped a temporary ban on paint imports to save shipping for the war. India's walls suddenly had two options: Shalimar Paints, or expensive foreign brands. Four friends saw the gap. Champaklal Choksey, Chimanlal Choksi, Suryakant Dani and Arvind Vakil - two of them already paint dealers, Dani and Vakil related by marriage - set up a partnership in a tiny garage in South Bombay and called it, with a shrug that has outlived them all, something they reportedly found in a telephone directory: the Asian Oil and Paint Company (" + A_TBI + "; " + A_HBL + ", reviewed by Hindu BusinessLine)."),
    p("Their edge was not chemistry; it was arithmetic and nerve. In 1945 they abandoned the industry's giant tins for tiny paint packets that any small shop could stock and any household could afford, and they tied up with small distributors in every corner they could reach. That first recorded year the company did Rs 3.5 lakh of business in five colours - black, white, red, blue and yellow (" + A_TBI + "). The giants they were up against, Goodlass Nerolac and the British incumbents, were fighting for the cities. The four friends went where the giants were not."),
    p("Champaklal Hiralal Choksey - Champak Seth to the company, Champakbhai to the industry - was the first among equals. He had fallen out bitterly with his own father in 1936 and been tided over by Dani; he brought to the partnership a ferocious energy, an organiser's instinct for the whole industry, and one fixed idea that would outlive him: the company is bigger than anyone in it (" + A_HBL + ")."),
  ]},
  {"heading": "2. Gattu goes to the village", "blocks": [
    p("While the foreign brands fought over Bombay and Calcutta, Asian Paints wooed the small shopkeepers of villages and tiny towns - even the colours were a nod to what rural India wanted, dark aquamarine and deep daffodil, because dark shades were considered powerful, as a past president of the Indian Paint Association told " + A_FORBES + ". The bet was that a country of first-time painters did not need convincing to paint; it needed paint it could reach."),
    p("In 1954 the company commissioned the cartoonist R.K. Laxman to draw a mascot. He produced a mischievous boy standing by a paint can, brush in hand, hair a mess - and Asian Paints ran a public contest to name him. Of 47,000 entries, two people from Bombay sent the winning name: Gattu (" + A_TBI + "). Gattu became the face of Tractor Distemper and its tagline - \"Don't lose your temper, use Tractor Distemper\" - reframed paint from repair to lifestyle: you did not wait for the walls to peel."),
    p("The campaign worked beyond its authors' hopes: sales rose tenfold over the next four years, and the surge paid for the company's first real plant, at Bhandup on Bombay's edge. Through the late 1950s and 1960s the company added corporate clients like Balmer Lawrie and began to look like what it was becoming (" + A_TBI + ")."),
    fig("photos/lr53-int1.jpg", "Abstract plate: a 1950s village shop shelf with tiny paint packets in five plain colours, a hand-painted sign of a mischievous boy with a brush above", "The packet, the mascot and the village shelf - the three moves that built the base."),
  ]},
  {"heading": "3. Number one, and the rules that kept it", "blocks": [
    p("In 1967, twenty-five years after the garage, Asian Paints became India's largest paint company, ahead of every multinational in the market. It has held that position every year since - fifty-nine years and counting, by " + A_COMP + "'s own telling."),
    p("Two decisions explain the durability better than any campaign. The first was a private compact: as far back as 1950, the four families had an agreement on how board representation would work among them - equal, balanced, and not up for renegotiation by any one family. The second came out of grief. When Arvind Vakil died in 1960, the founders faced the fact that families are mortal and companies need not be: Asian Paints began hiring professional managers from the best institutions in the country, decades before that was fashionable in Indian business. By 1968 the intake from premier engineering and business schools had turned the company into what " + A_HBL + " calls a veritable CEO factory; P.M. Murty would become the first non-family managing director."),
    p("The families kept a strict line between affection and commerce. The review of Gupta's book tells of Atul Choksey - the founder's son, then MD - visiting a depot and flatly telling dealers who knew his family personally that discounts and commissions were to be discussed with the depot executive, not with him. Personal relationships and commercial considerations, the founders insisted, were to be kept miles apart."),
  ]},
  {"heading": "4. The computer in the paint shop", "blocks": [
    p("In 1969, when computing in India meant a handful of government installations, V. Veeraraghavan's team at Asian Paints put a computer to work on inventory. By the 1970s the company had bought its first mainframe - at a time when computers were virtually unheard of in Indian business, " + A_FORBES + " notes - and aimed it at the problem that decides paint: demand forecasting. Paint is thousands of SKUs going stale on shelves; know what sells where, and you can make to demand instead of to stock."),
    p("The distribution model matched the math. Where the industry sold through wholesale distributors and clearing agents, Asian Paints went direct to the neighbourhood dealer and made itself the dealer's warehouse - frequent replenishment runs meant the shopkeeper needed almost no stockroom. Computerised colour-matching arrived in the mid-1970s, PCs in branches by the early 1980s, the first TV commercial in 1984, a customer helpline and a website by 1998-99 (" + A_TBI + ")."),
    p("The tinting machine completed the trap, in the best sense. Instead of stocking hundreds of pre-mixed shades, a dealer stocked white base paint and let a computerised machine inject colourants to order - over a thousand shades from a shelf's worth of inventory. Dealers bought the machines with their own money, and a small Indian paint shop has room for exactly one. Whoever's machine sits in the corner owns the shop's walls (" + A_HBL + ")."),
  ]},
  {"heading": "5. The last day of July", "blocks": [
    p("By the mid-1990s Champaklal Choksey was an old man estranged from his own creation. The disputes - over expansion financing, and over his son Atul's demand for greater board representation than the families' 1950 compact allowed - had worn everyone down. In April 1997, the Chokseys quietly approached British paint major ICI about buying their block of roughly 9.5% (" + A_IT + "; " + A_BS + ")."),
    p("Then came 31 July 1997. That day, through DSP Merrill Lynch, the Chokseys sold 8% of Asian Paints to two foreign institutional investors for about Rs 130 crore. That same day, in Pune, Champaklal Choksey died. Within weeks the deal collapsed - the FIIs said material information had been withheld from them, namely who the sellers were - and on 13 August the Chokseys revoked it (" + A_BS + ")."),
    p("Kotak Mahindra Capital then bought the family's 9.1% block, and on 18 August, with RBI permission for the foreign exchange, ICI agreed to buy it from Kotak at Rs 351 a share, about Rs 128.7 crore in all. The other three families wanted none of it: they refused to bless the transaction, and in the end a mutual fund took roughly half the shares and the Dani, Choksi and Vakil families took the rest (" + A_FORBES + "). The Chokseys were out of Asian Paints entirely. The founder's family had exited; the founder's company did not miss a step."),
    fig("photos/lr53-int2.jpg", "Abstract plate: a share certificate torn in two on a desk, one half stamped 31 July 1997, a telephone off the hook beside it, hard afternoon light", "31 July 1997 - the sale, and the same day, the death."),
  ]},
  {"heading": "6. The institution without its first family", "blocks": [
    p("Here is the part that makes Asian Paints a case study rather than a family saga. The exit of its primary visionary's family had no material impact on the company. Three families and a professional management ran it exactly as before, because that was the design: Champaklal himself had spent decades building an institution that would outlast its founders - and then tested it in the harshest way possible (" + A_HBL + ")."),
    p("The numbers he left running are the legend. The company listed in 1982; by the reckoning in " + A_HBL + ", the share has compounded over 20,000 times since, and Rs 10,000 invested in 1990 was worth about Rs 1.03 crore by 2024 - a 22.6% annual return sustained across thirty-four years. A mutual fund that bought the unwanted Choksey block in 1997 was holding one of the great positions in Indian market history."),
    p("The playbook kept evolving: joint ventures with America's PPG for automotive and industrial coatings in 1997 and 2012, a move into modular kitchens with Sleek in 2013, the slow build of a home-decor business, backward integration into raw materials decades after the first plant. When someone from a rival paint company asked Choksey how to create a successful company, " + A_HBL + " records his answer: \"You have to decide whether you want to do well, or you want the company to do well.\""),
  ]},
  {"heading": "7. The paint war", "blocks": [
    p("The company those decisions built is, by " + A_COMP + ": India's leading paint and decor company, second in Asia and eighth in the world in coatings, Rs 354 billion in consolidated turnover, twenty-seven plants across fifteen countries serving sixty. In February 2024 it got its first existential challenger in decades: the Aditya Birla Group's Grasim launched Birla Opus with Rs 10,000 crore upfront, a 40% addition to the entire industry's capacity, and a target of Rs 10,000 crore revenue in three years (" + A_GRASIM + ")."),
    p("The war is being fought exactly where the 1942 playbook says it should be: in the dealer's shop. Opus's capital buys plants and dealer incentives; Asian Paints' defence is the tinting machine in the corner, the delivery van that comes several times a day, and the painter who recommends the brand by habit. The cost of the fight is visible: " + A_MC + " showed profit up 7.5% to Rs 1,067.6 crore on revenue up 16.9% - but the operating margin shrank 202 basis points to 15.6% as the company absorbed raw-material inflation to protect demand."),
    p("And this week, with Brent settling at $96.57 a barrel - crude is the paint industry's cost line - the stock fell 2.89% on Thursday to Rs 2,543.00, closing at its day low (BSE official print). The market is repricing the moat in real time. The garage company has been counted out before: by the British brands in 1942, by the sceptics in 1997, by every bear who ever called its valuation impossible. The four chairs are long empty; the wall they painted still has not peeled."),
    fig("photos/lr53-int3.jpg", "Abstract plate: two paint tins facing each other on a shelf, one old and dented in daffodil yellow, one new and glossy, price tags dangling", "The incumbent and the challenger - the paint war comes to the dealer's shelf."),
  ]},
 ],
}

path = '/downloads/morning-paper/editions-src/longreads.json'
d = json.load(open(path))
d['53'] = lr
json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
print('added LR53; keys now:', sorted(d.keys(), key=int)[-3:])
