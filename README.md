Trader Performance vs Market Sentiment

A data-driven analysis exploring how market sentiment influences trader behavior, profitability, and risk exposure.

This project combines historical trading activity with the Crypto Fear & Greed Index to understand how traders behave during fear-driven markets vs greed-driven markets, and what strategic insights emerge from those patterns.

Problem Statement

Financial markets are strongly influenced by investor psychology. Periods of fear often bring high volatility and rapid price movements, while greed-driven markets tend to exhibit strong directional momentum.

This project investigates:

Does market sentiment affect trader profitability?

How does trader behavior change during fear vs greed periods?

Can sentiment signals help improve trading strategies?

Dataset

Two datasets were used for the analysis.

Historical Trading Data

Execution-level trading records including:

trade size

realized profit and loss

trading fees

execution price

account identifiers

timestamps

Fear & Greed Index

A sentiment indicator ranging from 0 to 100, reflecting market emotions.

Score Range	Market State
0–40	Fear
40–60	Neutral
60–100	Greed
Methodology

The project follows a structured analysis pipeline.

1. Data Preparation

cleaned trading data

normalized timestamps

aggregated trades to daily metrics

merged trading data with sentiment index

2. Feature Engineering

Key trading behavior indicators were constructed, including:

net trader profitability

trading volume

trade frequency

average trade size

directional order flow

position size proxies

These metrics allow analysis of trading intensity, directional bias, and exposure levels.

3. Market-Level Analysis

Trader metrics were aggregated to produce market-wide indicators such as:

total market trading volume

number of active traders

normalized trader profitability

order flow imbalance

This allows comparison between individual trader behavior and overall market activity.

4. Risk Analysis

To measure trading risk, the analysis evaluates:

cumulative trader profitability

drawdown behavior

distribution of trader returns

This helps identify how different trader groups manage risk.

Key Findings
1. Trading activity increases during fear regimes

Markets experiencing strong negative sentiment tend to exhibit:

higher trading frequency

larger position sizes

increased volatility

2. Trader profitability is higher during fear periods

Average profit per trader:

Fear regime   ≈ 2790 USD
Greed regime  ≈ 2108 USD

This suggests volatile market conditions create more opportunities for profitable trades.

3. Traders take larger positions during fear regimes

Upper tail position sizes:

Fear regime   ≈ 9.1e5
Greed regime  ≈ 3.6e5

Traders appear to increase exposure during periods of high volatility.

4. Trader behavior varies significantly across segments

Three distinct trader profiles emerged:

Segment	Characteristics
High Position Traders	Highest drawdowns
Frequent Traders	Higher total profits but higher volatility
Consistent Traders	Most stable risk-adjusted performance

Drawdown comparison:

High position traders ≈ -83.8k
Low position traders  ≈ -7.9k
Strategy Insights

The results suggest that sentiment-aware trading strategies may improve performance.

Fear Regime

exploit high volatility

control position sizing to limit drawdowns

Greed Regime

reduce leverage

focus on selective trading opportunities

Combining market sentiment signals with trader segmentation can improve risk-adjusted performance.

Project Structure
trader-sentiment-analysis
│
├── data
│   ├── historical_data.csv
│   └── fear_greed_index.csv
│
├── notebooks
│   └── Sentiment_Analysis.ipynb
│
├── reports
│   ├── chart1_pnl_per_trader_box.png
│   ├── chart2_behavior_bars.png
│   └── chart3_segment_frequency_pnl.png
│
└── README.md
Technologies Used

Python

Pandas

NumPy

Matplotlib

Seaborn

Jupyter Notebook

Future Work

Potential extensions include:

predictive sentiment models

volatility forecasting

regime-switching trading strategies

machine learning models for trader segmentation

Author

Nirvan Jha
