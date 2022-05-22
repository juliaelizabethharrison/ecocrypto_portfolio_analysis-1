import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hvplot.pandas
import holoviews as hv
import panel as pn
from pathlib import Path
from datetime import datetime, timedelta
from bokeh.models import HoverTool
from matplotlib.pyplot import pie, axis, show

def fetch_env_efficiency_data():
    # Read csv file into DataFrame
    env_df = pd.read_csv(Path(f"data/env_efficiency.csv"), parse_dates=False)
    
    # Convert Column names
    # Name	Symbol	Algorithm	Market cap [USD million]	Market cap [%]	Hashes/s (network)	Efficiency (device) [Hashes/s/W]	Rated power (network) [kW]	Rated power (network) [%]
    columns = ["Name", "Symbol", "Algorithm", "MarketCapMill", "MarketCapPct", "Hashes", "Efficiency", "RatedPowerKW", "RatedPowerPct"]
    env_df.columns = columns
    
    # Clean up data
    env_df['MarketCapPct'] = env_df['MarketCapPct'].map(lambda x: x.lstrip('+-').rstrip('%'))
    env_df['RatedPowerPct'] = env_df['RatedPowerPct'].map(lambda x: x.lstrip('+-').rstrip('%'))

    # Surpress scientific notation is an environmental option fyi
    # pd.set_option('display.float_format', lambda x: '%.0f' % x)
    
    # Convert dtypes
    cols = ["MarketCapMill","MarketCapPct","Hashes","Efficiency","RatedPowerKW","RatedPowerPct"]
    env_df[cols] = env_df[cols].astype(np.float64)
    
    # Sort by Market Cap
    df = env_df.sort_values("Hashes")

    return df

def scatter_plot(df):
    
    # Filter the DataFrame
    df = df.filter(["Symbol","Algorithm","Efficiency", "RatedPowerKW"], axis=1).sort_values("RatedPowerKW")
    
    # Define the hovertool
    hover1 = HoverTool(tooltips=[("Algorithm", "@Algorithm"), ("Symbol", "@Symbol")],
                       formatters = {'@eff': 'printf'
                                     # '@pwr': 'printf'
                                    })
    # Create the plot
    plot = df.hvplot.scatter(x="RatedPowerKW", y="Efficiency",tools=[hover1],by="Algorithm")
    
    return plot

def bar_chart(df):
    
    # Filter the DataFrame
    df = df.filter(["Symbol","Algorithm","Efficiency","RatedPowerKW"], axis=1).sort_values("RatedPowerKW")
    
    # Create the bar chart
    bar = df.hvplot.bar(x="Symbol", y="RatedPowerKW", title="Rated Power per Cryptocurrency", hover_cols=["Efficiency","Symbol", "Algorithm"],width=900, height=400)
    
    return bar


def bar_chart_top_five(df):
    """NEED a better formula to quantify this stuff
    """
    
    # Filter the DataFrame
    df = df[:5].filter(["Symbol","Algorithm","Efficiency","RatedPowerKW"], axis=1).sort_values("Efficiency")
    
    # Create the bar chart
    bar = df.hvplot.bar(x="Symbol", y="Efficiency", title="Rated Power per Top-5 PoS Cryptocurrencies", hover_cols=["Efficiency","Symbol", "Algorithm"], width=900, height=400)
 
    return bar

def bar_chart_bottom_five(df):
    
    # Filter the DataFrame
    df = df.filter(["Symbol","Algorithm","Efficiency","RatedPowerKW"], axis=1).sort_values("Efficiency")
    
    # Create the bar chart
    bar = df.hvplot.bar(x="Symbol", y="Efficiency", title="Rated Power per Top-5 PoS Cryptocurrencies", hover_cols=["Efficiency","Symbol", "Algorithm"], width=900, height=400)
 
    return bar

def make_pie(df):
    
    # Assign data and assets
    assets = df["Coin"].tolist()
    data = df["Funds"]

    ## Creating autopct arguments
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d} USD)".format(pct, absolute)

    ## Creating plot
    fig, ax = plt.subplots(figsize =(10, 10))
    wedges, texts, autotexts = ax.pie(data, autopct = lambda pct: func(pct, data), explode = (0.0, 0.0, 0.2, 0.2, 0.2, 0.2), labels = assets, startangle = 90)
    ax.legend(wedges, assets, title ="Assets", loc ="upper right", bbox_to_anchor = (1, 0, 0.25, 1))
    plt.setp(autotexts, size = 12)
    ax.set_title("Portfolio Composition", fontsize=18, weight ="bold")

    return plt.show()


def efficiency_scatter(df):
    
    # Filter the DataFrame
    df = df.filter(["Symbol","Algorithm","Hashes","Efficiency","RatedPowerKW","RatedPowerPct"], axis=1).sort_values("Hashes")
    
    # Create the bar chart
    bar = df.hvplot.scatter(legend='top', x="Hashes", y="Efficiency", by="Algorithm", size=df["RatedPowerKW"]*10, padding=0.6, 
                            title="Top-5 Most Environmentally Efficient PoS Cryptocurrencies", hover_cols=["RatedPowerPct", "Efficiency","Algorithm"], width=800, height=420)
 
    return bar