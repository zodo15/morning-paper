import sys

def rep(fname, old, new):
    s = open(fname).read()
    n = s.count(old)
    assert n == 1, (fname, n, old[:90])
    open(fname, 'w').write(s.replace(old, new))
    print('patched:', fname, '|', old[:60].replace('\n', ' '), '->')

B = 'build_day44.py'; L = 'lr44.py'

rep(B, "GIFT = 'https://giftniftytoday.com/pre-market'",
       "GIFT = 'https://giftniftytoday.com/pre-market'\nUS10YQ = 'https://www.cnbc.com/quotes/US10Y'")

rep(B, r"""up 103% on the year and above every estimate - with data center at $107.6 billion, up 110%, and a fourth-quarter guide of $130 billion, give or take 3%, against a $125.1 billion consensus (' + a(NVPR, 'the company\'s release') + ')""",
       r"""up 103% on the year and well above the $109.1 billion analysts expected - with data center at $107.6 billion, up 110%, and a fourth-quarter guide of $130 billion, give or take 3%, against the $125.1 billion expected (' + a(NVPR, 'the company\'s release') + '; ' + a(CNBCLIVE, 'LSEG\'s estimates via CNBC') + ')""")

rep(B, r"""p(' Overnight markers: GIFT Nifty at 25,358.50, up 0.03%, pointing to a flat open near 25,395 - an indication, not an open; Brent $93.14; gold $3,846.20; the dollar index 103.49; the US ten-year at 5.119%; the VIX at 25.46 after an 11% jump (' + a(GIFT, 'the pre-market screen, as of 5:42 AM IST') + ').""",
       r"""p(' Overnight markers, as of about 6 AM IST: Brent $93.14; the dollar index at 103.49; gold at $3,841.60, down 0.58%; the US ten-year at 5.115% (' + a(US10YQ, 'CNBC\'s quote boards') + '); the VIX closed Tuesday at 25.46, up 11.13%; GIFT Nifty at 25,358.50, up 0.03%, pointing to a flat open near 25,395 - an indication, not an open (' + a(GIFT, 'the pre-market screen') + ').""")

rep(B, r"""This morning, as of about 5:42 AM IST: GIFT Nifty at 25,358.50, up 0.03% - a flat indication, not an open; S&P 500 futures +0.73% at 7,412.75; Nasdaq 100 futures +1.39% at 27,451; Brent $93.14; gold $3,846.20; the dollar index 103.49; USD/INR 93.47; the US ten-year at 5.119% (' + a(GIFT, 'the pre-market screen') + ').""",
       r"""This morning, as of about 6 AM IST: S&P 500 futures up 0.8% at 7,418.25 and Nasdaq 100 futures up 1.6% at 27,497.75 (' + a(INVFUT, 'the futures report, timestamped 5:22 AM IST') + '); Brent $93.14; gold $3,841.60, down 0.58%; the dollar index 103.49; the US ten-year at 5.115% (' + a(US10YQ, 'CNBC\'s quote boards') + '); GIFT Nifty at 25,358.50, up 0.03% - a flat indication, not an open (' + a(GIFT, 'the pre-market screen') + ').""")

rep(B, """fact = ('Edition 44. The print, the door, and the debut. Wednesday 18 November 2026, edition 44. This edition runs 4,419 words. '
 'Nvidia\\'s first post-Huang quarter beat across the board - $115.8 billion of revenue, up 103%, and a $130 billion guide above consensus; the stock rose about 5% after hours. '""",
       """fact = ('Edition 44. Wednesday 18 November 2026. This edition runs WCOUNT words. '
 'Nvidia\\'s first post-Huang quarter beat across the board - $115.8 billion of revenue, up 103% against the $109.1 billion expected, and a $130 billion guide against the $125.1 billion expected; the stock rose about 5% after hours. '""")

rep(B, r"""The long read: every advanced chip in Nvidia\'s record quarter came from one firm in Hsinchu - """,
       r"""The long read: the chips behind Nvidia\'s record quarter came from one firm in Hsinchu - """)

rep(B, r"""Every advanced chip in Nvidia\'s record quarter came from one firm in Hsinchu - and Morris Chang was twice sidelined and past fifty when he invented its model.""",
       r"""The chips behind Nvidia\'s record quarter came from one firm in Hsinchu - and Morris Chang was twice sidelined and past fifty when he invented its model.""")

rep(L, "FOCUS = 'https://focustaiwan.tw/business/202609090025'",
       "FOCUS = 'https://focustaiwan.tw/business/202609090025'\nNVLIVE = 'https://www.cnbc.com/2026/11/17/nvidia-nvda-earnings-report-q3-2027.html'")

rep(L, r"""$115.8 billion of revenue, a forecast above every estimate - and every advanced chip in that number came out of Morris Chang\'s factories.""",
       r"""$115.8 billion of revenue, well above the $109.1 billion analysts expected (' + a(NVLIVE, 'CNBC\'s tally') + ') - and essentially every chip in that number came out of Morris Chang\'s factories, as they have for three decades.""")

rep(L, r"""Every advanced chip in Nvidia\'s record quarter was made by a company that has never sold a chip of its own. """,
       r"""The chips behind Nvidia\'s record quarter were made by a company that, by its own description, manufactures only its customers\' products. """)

print('all patches applied')
