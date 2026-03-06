# PrimeTrade.ai-Assignment
Trader Performance vs Market Sentiment

Quantitative analysis of trader behavior and profitability under varying market sentiment regimes using historical trading data and the Crypto Fear & Greed Index.

This project investigates whether market sentiment influences trading activity, profitability, and risk-taking behavior, and proposes strategy implications based on empirical findings.

Overview

Financial markets are strongly influenced by investor sentiment. Periods of fear often correspond to high volatility and rapid price movements, while greed periods are typically characterized by strong directional momentum and reduced uncertainty.

This project explores the relationship between:

Market sentiment (Fear & Greed Index)

Trader performance

Trading behavior

Risk exposure

By aligning daily trading activity with sentiment data, we analyze how trader behavior changes across sentiment regimes and derive actionable strategy insights.

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
│   ├── chart3_segment_frequency_pnl.png
│
└── README.md
Data Sources
1. Historical Trading Data

Contains detailed execution-level records including:

trade size

execution price

realized profit/loss

fees

position sizes

trader accounts

timestamps

2. Fear & Greed Index

Market sentiment indicator ranging from 0 to 100.

Range	Market State
0–40	Fear
40–60	Neutral
60–100	Greed
Methodology
1. Data Preprocessing

Steps performed:

timestamp normalization

daily aggregation of trading data

merging sentiment and trading datasets by date

removal of missing and duplicate entries

2. Feature Engineering

Key trading metrics were constructed.

Profitability
𝑃
𝑛
𝐿
𝑖
,
𝑡
=
∑
𝑘
=
1
𝑛
𝑖
,
𝑡
(
𝐶
𝑙
𝑜
𝑠
𝑒
𝑑
𝑃
𝑛
𝐿
𝑘
−
𝐹
𝑒
𝑒
𝑘
)
PnL
i,t
	​

=
k=1
∑
n
i,t
	​

	​

(ClosedPnL
k
	​

−Fee
k
	​

)
Trading Volume
𝑉
𝑖
,
𝑡
=
∑
𝑘
=
1
𝑛
𝑖
,
𝑡
𝑆
𝑖
𝑧
𝑒
𝑈
𝑆
𝐷
𝑘
V
i,t
	​

=
k=1
∑
n
i,t
	​

	​

SizeUSD
k
	​

Average Trade Size
𝐴
𝑇
𝑆
𝑖
,
𝑡
=
𝑉
𝑖
,
𝑡
𝑛
𝑖
,
𝑡
ATS
i,t
	​

=
n
i,t
	​

V
i,t
	​

	​

Directional Order Flow
𝑁
𝑒
𝑡
𝐹
𝑙
𝑜
𝑤
𝑖
,
𝑡
=
𝐵
𝑢
𝑦
𝑉
𝑜
𝑙
𝑖
,
𝑡
−
𝑆
𝑒
𝑙
𝑙
𝑉
𝑜
𝑙
𝑖
,
𝑡
NetFlow
i,t
	​

=BuyVol
i,t
	​

−SellVol
i,t
	​

Position Size Proxy
𝑃
𝑜
𝑠
𝑖
,
𝑡
=
∣
𝑆
𝑡
𝑎
𝑟
𝑡
𝑃
𝑜
𝑠
𝑖
𝑡
𝑖
𝑜
𝑛
𝑖
,
𝑡
∣
×
𝑃
𝑟
𝑖
𝑐
𝑒
𝑖
,
𝑡
Pos
i,t
	​

=∣StartPosition
i,t
	​

∣×Price
i,t
	​

3. Market Aggregation

Market-wide metrics were derived by aggregating trader-level features:

𝑉
𝑡
=
∑
𝑖
𝑉
𝑖
,
𝑡
V
t
	​

=
i
∑
	​

V
i,t
	​

𝐴
𝑡
=
∑
𝑖
1
(
𝑛
𝑖
,
𝑡
>
0
)
A
t
	​

=
i
∑
	​

1(n
i,t
	​

>0)

Normalized trader returns:

𝑅
𝑖
,
𝑡
=
𝑃
𝑛
𝐿
𝑖
,
𝑡
𝑉
𝑖
,
𝑡
R
i,t
	​

=
V
i,t
	​

PnL
i,t
	​

	​

4. Risk Metrics

Cumulative profit:

𝐶
𝑢
𝑚
𝑃
𝑛
𝐿
𝑖
,
𝑡
=
∑
𝜏
=
1
𝑡
𝑃
𝑛
𝐿
𝑖
,
𝜏
CumPnL
i,t
	​

=
τ=1
∑
t
	​

PnL
i,τ
	​


Drawdown proxy:

𝐷
𝑟
𝑎
𝑤
𝑑
𝑜
𝑤
𝑛
𝑖
,
𝑡
=
𝐶
𝑢
𝑚
𝑃
𝑛
𝐿
𝑖
,
𝑡
−
max
⁡
𝜏
≤
𝑡
𝐶
𝑢
𝑚
𝑃
𝑛
𝐿
𝑖
,
𝜏
Drawdown
i,t
	​

=CumPnL
i,t
	​

−
τ≤t
max
	​

CumPnL
i,τ
	​


Return distribution:

𝜇
𝑅
=
𝐸
[
𝑅
𝑖
,
𝑡
]
μ
R
	​

=E[R
i,t
	​

]
𝜎
𝑅
2
=
𝑉
𝑎
𝑟
(
𝑅
𝑖
,
𝑡
)
σ
R
2
	​

=Var(R
i,t
	​

)
5. Sentiment Regime Modeling

Market regimes are defined using the Fear & Greed index:

𝑅
𝑒
𝑔
𝑖
𝑚
𝑒
𝑡
=
{
𝐹
𝑒
𝑎
𝑟
	
𝑆
𝑡
≤
40


𝑁
𝑒
𝑢
𝑡
𝑟
𝑎
𝑙
	
40
<
𝑆
𝑡
≤
60


𝐺
𝑟
𝑒
𝑒
𝑑
	
𝑆
𝑡
>
60
Regime
t
	​

=
⎩
⎨
⎧
	​

Fear
Neutral
Greed
	​

S
t
	​

≤40
40<S
t
	​

≤60
S
t
	​

>60
	​


Statistical relationships between sentiment and trading activity were evaluated using Spearman rank correlation:

𝜌
=
1
−
6
∑
𝑑
𝑖
2
𝑛
(
𝑛
2
−
1
)
ρ=1−
n(n
2
−1)
6∑d
i
2
	​

	​

Key Findings
1. Fear regimes produce higher trading activity

Increased number of trades

Larger position sizes

Higher market volatility

2. Trader profitability is higher during fear periods

Average profit per trader:

Fear regime   ≈ 2790 USD
Greed regime  ≈ 2108 USD
3. Risk exposure increases significantly during fear regimes

Position size tails:

P95 Position (Fear)  ≈ 9.1e5
P95 Position (Greed) ≈ 3.6e5

This suggests traders increase leverage during volatile markets.

4. Trader heterogeneity is substantial

Segmentation revealed different trader profiles:

Segment	Characteristics
High Position Traders	Highest drawdowns
Frequent Traders	High PnL but volatile
Consistent Traders	Best risk-adjusted returns

Drawdown comparison:

High position traders  ≈ -83.8k
Low position traders   ≈ -7.9k
Strategy Implications
Fear Regime Strategy

Exploit volatility while controlling risk.

Position sizing rule:

𝑃
𝑜
𝑠
𝑖
𝑡
𝑖
𝑜
𝑛
𝑆
𝑖
𝑧
𝑒
𝑡
=
𝑤
0
+
𝑤
1
𝑆
𝑡
PositionSize
t
	​

=w
0
	​

+w
1
	​

S
t
	​

Greed Regime Strategy

Reduce leverage and trade selectivity.

𝐿
𝑒
𝑣
𝑒
𝑟
𝑎
𝑔
𝑒
𝑡
=
𝐿
0
−
𝜆
(
𝑆
𝑡
−
𝑆
ˉ
)
Leverage
t
	​

=L
0
	​

−λ(S
t
	​

−
S
ˉ
)
Portfolio Construction

Combining sentiment signals with trader segmentation can significantly improve:

capital efficiency

drawdown control

risk-adjusted returns

Visualizations

The project includes several analytical charts:

PnL distribution by sentiment regime

Behavioral differences (trade frequency, position size)

Trader segment performance comparison

Example outputs are stored in:

reports/
Technologies Used

Python

Pandas

NumPy

Matplotlib

Seaborn

Jupyter Notebook

Future Improvements

Potential extensions include:

regime-switching models

volatility forecasting

predictive sentiment-based trading strategies

reinforcement learning for position sizing

Author

Nirvan Jha
