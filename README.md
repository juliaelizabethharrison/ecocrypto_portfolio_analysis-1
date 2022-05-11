# **Cryptocurrency for Energy Conscious Investors** #

## *WorkInProgress* ##

- README change tracking goes here

## Technologies ##

- python
- jupyterlab
- pandas
- numpy
- matplotlib
- hvplot, geoviews

## Background ##

We've been tasked with evaluating some crypto currencies that use blockchains with eco-freindly metrics or low-carbon footprint.

etc..

## Overview ##

etc

### Quantatative Analysis ###

We've created a DataFrame for analysis by importing trade data. Then, we performed our quantitative analysis which includes the following:

- Analyze the data for **Performance** to determine if any of the portfolios outperform the broader stock market, which the S&P 500 represents.

![Cumulative Returns](images/screenshot_cumulative_returns.png)

- **Volatility** of each of the four fund portfolios and of the S&P 500 Index by using box plots:

![Volatility](images/screenshot_fund_volatility_box.png)

- **Risk** profile of each portfolio using the **standard deviation** and **beta**:

![Risk](images/screenshot_fund_risk.png)

- **Risk-Return** profile using sharpe index:

![Sharpe Ratios](images/screenshot_sharpe_ratios_bar.png)

- **Portfolio Diversification**:  For each portfolio, we've calculated the covariance using the 60-day rolling window, the daily return data, and the Eco-Crypto Currency returns. We then calculated the beta of each portfolio by dividing the covariance of the portfolio by the variance of the Eco-Crypto Currencies. Lastly, we calculate the rolling beta of the portfolio using the average value of the 60-day rolling window.

## Conclusion ##

Based on our analysis, we've choosen a few Eco-Crypto Currency Portfolios that we are likely to recommend as investment options:

### *insert here* ###

### 60-Day Rolling Beta Comparison ###

![Rolling Beta](images/screenshot_portfolio_rolling_beta_comparison.png)
