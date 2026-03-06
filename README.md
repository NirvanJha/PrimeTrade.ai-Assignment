
md
# Trader Performance vs Market Sentiment

A data-driven analysis exploring how market sentiment influences trader behavior, profitability, and risk exposure.

This project combines historical trading activity with the Crypto Fear & Greed Index to understand how traders behave during fear-driven markets versus greed-driven markets, and what strategic insights can be extracted to improve trading performance.

## Problem Statement

Financial markets are strongly influenced by investor psychology. Periods of fear often bring high volatility and rapid price movements, while greed-driven markets tend to exhibit strong directional momentum. Understanding how traders respond to these sentiment shifts is critical for developing effective trading strategies.

This project investigates three core questions:

- Does market sentiment affect trader profitability?
- How does trader behavior change during fear versus greed periods?
- Can sentiment signals help improve trading strategies?

## Dataset

Two datasets were used for this analysis:

### Historical Trading Data

Execution-level trading records including:
- Trade size
- Realized profit and loss
- Trading fees
- Execution price
- Account identifiers
- Timestamps

### Fear & Greed Index

A sentiment indicator ranging from 0 to 100, reflecting market emotions.

| Score Range | Market State |
|-------------|--------------|
| 0–40       | Fear         |
| 40–60      | Neutral      |
| 60–100     | Greed        |

## Methodology

The project follows a structured analysis pipeline:

### 1. Data Preparation

- Cleaned trading data and normalized timestamps
- Aggregated trades to daily metrics
- Merged trading data with sentiment index

### 2. Feature Engineering

Key trading behavior indicators were constructed:
- Net trader profitability
- Trading volume
- Trade frequency
- Average trade size
- Directional order flow
- Position size proxies

### 3. Market-Level Analysis

Trader metrics were aggregated to produce market-wide indicators:
- Total market trading volume
- Number of active traders
- Normalized trader profitability
- Order flow imbalance

### 4. Risk Analysis

Risk measurements include:
- Cumulative trader profitability
- Drawdown behavior
- Distribution of trader returns

## Key Findings

### Finding 1: Trading Activity Increases During Fear Regimes

Markets experiencing strong negative sentiment exhibit:
- Higher trading frequency
- Larger position sizes
- Increased volatility

### Finding 2: Trader Profitability is Higher During Fear Periods

Average profit per trader:
Fear regime ≈ $2,790 Greed regime ≈ $2,108

Code

This suggests volatile market conditions create more opportunities for profitable trades.

### Finding 3: Traders Take Larger Positions During Fear Regimes

Upper tail position sizes:
Fear regime ≈ 9.1e5 Greed regime ≈ 3.6e5

Code

Traders appear to increase exposure during periods of high volatility.

### Finding 4: Trader Behavior Varies Significantly Across Segments

Three distinct trader profiles emerged:

| Trader Profile | Characteristics |
|---|---|
| High Position Traders | Highest drawdowns, largest exposure |
| Frequent Traders | Higher total profits but higher volatility |
| Consistent Traders | Most stable risk-adjusted performance |

Drawdown comparison:
High position traders ≈ -$83,800 Low position traders ≈ -$7,900

Code

## Strategy Insights

The results suggest that sentiment-aware trading strategies may improve performance.

**During Fear Regimes:**
- Exploit high volatility with scaled position sizing
- Implement risk controls to limit drawdowns
- Monitor order flow imbalances

**During Greed Regimes:**
- Reduce leverage to manage risk
- Focus on selective trading opportunities
- Maintain disciplined position management

Combining market sentiment signals with trader segmentation can improve risk-adjusted performance.

## Project Structure

trader-sentiment-analysis/ ├── data/ │ ├── historical_data.csv │ └── fear_greed_index.csv ├── notebooks/ │ └── Sentiment_Analysis.ipynb ├── reports/ │ ├── chart1_pnl_per_trader_box.png │ ├── chart2_behavior_bars.png │ └── chart3_segment_frequency_pnl.png └── README.md

Code

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Future Work

Potential extensions include:
- Predictive sentiment models
- Volatility forecasting
- Regime-switching trading strategies
- Machine learning models for trader segmentation

## Author

Nirvan Jha
