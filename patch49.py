#!/usr/bin/env python3
"""Apply Ed49 review fixes to editions-src/day-49.json. Fails loudly on any miss."""
import json, sys

P = '/downloads/morning-paper/editions-src/day-49.json'
d = json.load(open(P))
g = d['edition']['groups']

def repl(block, old, new, where):
    h = block['html']
    assert old in h, f'MISS in {where}: {old[:60]}'
    block['html'] = h.replace(old, new)

MINT = 'https://www.livemint.com/market/ipo/mahanadi-coalfields-ipo-gmp-check-down-92-from-rs-9-25-to-rs-0-7-issue-struggles-to-attract-bids-subscribe-or-avoid-11795252154826.html'
BL = 'https://www.thehindubusinessline.com/markets/gift-nifty-signals-175-point-gap-up-open-for-indian-markets-despite-weak-global-cues/article71733203.ece'
ETFIX = 'https://economictimes.indiatimes.com/markets/stocks/news/fiis-go-big-on-indian-equities-pump-over-rs-1-10-lakh-crore-in-november-what-comes-next/articleshow/136048685.cms'
def a(url, label): return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'

# [0] lead route
b = g[0]['blocks']
repl(b[0], "Nasdaq 100 futures up about 3.1% in early Asian trade", "Nasdaq 100 futures up about 2.8% in early Asian trade", 'lead0')
repl(b[0], "the region's only major cash market open at dawn kept falling", "the region's biggest cash market open at dawn kept falling", 'lead0')
repl(b[4], "and was at about 25,963, up 0.4%, by 6:40 am (" + a('https://www.moneycontrol.com/news/business/markets/trade-setup-for-november-23-top-15-things-to-know-before-the-opening-bell-ahead-of-f-o-expiry-14086687.html', 'the levels') + ")",
     "and was holding a gap-up of about 175 points near 25,975 by 7:15 (" + a(BL, 'the levels') + ")", 'lead4')
repl(b[5], "the grey-market premium had thinned to a rupee or two by Friday evening.", "the grey-market premium is down to Rs 0.70, from Rs 9.25 a week earlier.", 'lead5')

# [1] front page
b = g[1]['blocks']
repl(b[0], "Nasdaq 100 futures up 3.1%", "Nasdaq 100 futures up 2.8%", 'fp0')
repl(b[0], "Nikkei December futures up 3.2% at about 56,140", "Nikkei December futures up 3.2% at about 56,180", 'fp0')
repl(b[1], "Nvidia -13.8%", "Nvidia -14.0%", 'fp1')
repl(b[4], "and the grey-market premium thinned to Rs 1-2 by Friday evening (" + a('https://hdfcsky.com/news/mahanadi-coalfields-ipo-subscription-status-day-2', 'the day-two tally') + ").",
     "(" + a('https://hdfcsky.com/news/mahanadi-coalfields-ipo-subscription-status-day-2', 'the day-two tally') + "), and the grey-market premium fell to Rs 0.70 by the weekend, from Rs 9.25 a week earlier (" + a(MINT, 'Mint') + ").", 'fp4')

# [2] markets
b = g[2]['blocks']
repl(b[1], "the S&P's RSI under 30, the index 11.6% under its October record with tech down 24.7% in the span.",
     "the S&P's RSI under 30, the index 11.6% under its 6 October record, and the Nasdaq Composite's gain for the year erased.", 'mk1')
b[3]['html'] = (" The commodity tape at the open. Gold's December contract traded at $3,603, up 2.5% - the haven bid strengthening through the rebound; silver added 2.3% to $42.03. "
    "Oil steadied: WTI's January contract at $83.26, down 0.2%, and Brent at $89.79, down 0.2% - investing.com's quote has rolled to the February contract, against Friday's $92.57 December settle, so the two prints are not directly comparable. "
    "Natural gas fell 3.5%. All quotes are ten-minute-delayed indications, not settles.")

# [3] IPOs
b = g[3]['blocks']
repl(b[0], "- with the grey-market premium down to a rupee or two (" + a('https://hdfcsky.com/news/mahanadi-coalfields-ipo-subscription-status-day-2', 'HDFC Sky') + ").",
     "(" + a('https://hdfcsky.com/news/mahanadi-coalfields-ipo-subscription-status-day-2', 'HDFC Sky') + ") - with the grey-market premium down to Rs 0.70, from Rs 9.25 a week earlier (" + a(MINT, 'Mint') + ").", 'ipo0')

# [6] Finance Goldmine: trim Infosys duplication + merge Term of the day
b = g[6]['blocks']
b[1]['html'] = (" Six years later, the fireworks: on 11 March 1999 the same company became the first India-registered firm to list on a US exchange, and Rs 10,000 in that 1993 IPO compounded to about Rs 4 crore by 2018, dividends and bonuses doing the compounding. Today's long read tells the whole arc.")
del b[2]  # 'What that became' paragraph folded into the trimmed line
term = {"t": "p", "html": (" One term worth owning: the grey market premium - GMP - the unofficial price at which IPO shares change hands before listing, quoted as rupees over the issue price. "
    "Nothing about it is regulated: no exchange, no settlement guarantee, no obligation behind the quote, and the premium routinely evaporates between the close of the book and the open of trading. "
    "Its one honest use is as a sentiment thermometer. Mahanadi Coalfields illustrates the reading: a GMP down to Rs 0.70 by the weekend, from Rs 9.25 a week earlier, is the market's way of saying it expects a listing near the Rs 136 cap - a cold reading for a book that was 0.49 times subscribed after two days ("
    + a(MINT, 'Mint') + "; " + a('https://hdfcsky.com/news/mahanadi-coalfields-ipo-subscription-status-day-2', 'the tally') + ").")}
g[6]['blocks'].append(term)

# [11] One concept: replace with psychology/research concept
g[11]['heading'] = 'One concept: the disposition effect'
g[11]['blocks'] = [{"t": "p", "html": (
    " The disposition effect - why we sell winners and keep losers. In 1985 the economists Hersh Shefrin and Meir Statman gave a name to one of the most reliable patterns in investing behaviour: people sell investments that have risen too early and hold on to those that have fallen, waiting to get back to even. "
    "Terrance Odean later confirmed it in the trading records of 10,000 households at a US brokerage: investors sold their winners at a clearly higher rate than their losers, and the winners they sold went on to beat the losers they kept. "
    "The mechanism is not arithmetic but pride and regret - selling a loser means admitting the mistake, so the account keeps the mistake and banks the compliment. "
    "It shows up far beyond stocks: people stay in jobs, and founders in products, long past the evidence, because quitting writes the loss down. "
    "A week like this one makes it concrete - a market that has fallen for weeks tempts every holder to wait for back-to-even instead of asking the cleaner question: would I buy this today? If the answer is no, holding is a fresh decision, not patience. "
    "The fix the research suggests is mechanical: set exit rules before you enter, and review what you hold as if you did not own it.")}]

# [15] editor's read
b = g[15]['blocks']
repl(b[0], "Seoul's cash market, the only major one open at dawn", "Seoul's cash market, the biggest one open at dawn", 'er0')
repl(b[1], "is hedged with a record index-futures short, a posture of renting", "is hedged with an index-futures short that has grown to about 70,450 contracts from 55,900 a week earlier, a posture of renting", 'er1')
assert '136044698' in b[1]['html']; b[1]['html'] = b[1]['html'].replace('136044698', '136048685')
repl(b[2], "Gold added 1.7% overnight even as equity futures rebounded - the insurance bid did not unwind when the rally cry went out.",
     "Gold was up 2.5% at press time even as equity futures rebounded - the insurance bid did not unwind when the rally cry went out.", 'er2')
# merge Brewing as final watch paragraph
brew = g[16]['blocks'][0]['html'].strip()
b.append({"t": "p", "html": " What settles the week: " + brew[0].lower() + brew[1:]})

# [18] notes
nb = g[18]['blocks'][0]['items']
nb[0] = nb[0].replace("HDFC Sky for the Mahanadi tally;", "HDFC Sky for the Mahanadi tally and Mint for its grey-market premium;").replace("moneycontrol's trade setup for the Nifty levels, attributed as analyst views;", "moneycontrol's trade setup for the Nifty levels, attributed as analyst views, and The Hindu BusinessLine for the GIFT Nifty gap-up;")
nb[1] = nb[1].replace("Brent quotes are the February contract, rolled forward from Friday's December print - the two are not directly comparable.", "Brent quotes are the February contract - investing.com's quote has rolled forward from Friday's December print, while ICE keeps the January contract trading until 30 November - so the two prints are not directly comparable.")

# delete standalone Term of the day [12] and Brewing [16] groups
del g[16]
del g[12]
assert len(g) == 17, len(g)
heads = [x.get('heading') for x in g]
print('roster:', ' | '.join(heads))

json.dump(d, open(P, 'w'), ensure_ascii=False, indent=1)
print('PATCHED OK')
