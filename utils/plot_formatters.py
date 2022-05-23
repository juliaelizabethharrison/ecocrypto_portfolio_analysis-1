# import necessary classes/libraries
from bokeh.models.formatters import DatetimeTickFormatter, NumeralTickFormatter

# HVPlot Properties & Formatters
formatter_dt = DatetimeTickFormatter(days='%m/%d\n(%Y)', months='%m/%Y', years='%Y')
formatter_usd_b = NumeralTickFormatter(format="0,0{\n(billion USD $)}")
formatter_usd_m = NumeralTickFormatter(format="0,0{\n(million USD $)}")
formatter_usd_k = NumeralTickFormatter(format="{\u0024}0.0")
formatter_usd = NumeralTickFormatter(format="$0,0")
formatter_usd_sm = NumeralTickFormatter(format="$0.0000000")
formatter_pct = NumeralTickFormatter(format="0.0%")
formatter_eth = NumeralTickFormatter(format="0,0{\n(ETH \u039E)}")
formatter_btc_m = NumeralTickFormatter(format="0,0{\n(million BTC \u20BF)}")
formatter_btc = NumeralTickFormatter(format="0,0{\n(BTC \u20BF)}")

font_sizes = {'title': '14pt', 'xlabel': '10pt', 'ylabel': '10pt'}