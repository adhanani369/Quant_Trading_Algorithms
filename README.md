📌 Quantitative Trading & Financial Forecasting Models
🚀 Algorithmic Trading | Market Volume Analysis | Asset Price Prediction

This repository contains Python-based trading algorithms and predictive models for analyzing financial markets. These scripts utilize quantitative finance, econometrics, and machine learning techniques to identify market trends, optimize trading decisions, and predict asset price movements.

📂 Project Overview
1️⃣ Volume-Based Market Analysis (VolumeCode.py)
Description:

Fetches real-time trading volume for stocks using Yahoo Finance API.
Helps analyze liquidity trends and volume surges for trade execution strategies.
Key Features:
✅ Extracts 1-minute interval trading volume for any stock.
✅ Tracks liquidity for high-frequency trading (HFT) strategies.

2️⃣ Momentum-Based Trading Strategy (MomentumBasedTradingFactorCode.py)
Description:

Implements a quantitative factor-based trading model with momentum indicators, beta filters, Sharpe ratio constraints, and volume-based thresholds.
Designed for intraday trading strategies in equities and cryptocurrencies.
Key Features:
✅ Uses real-time price & volume data from Yahoo Finance & Alpha Vantage APIs.
✅ Implements 5-minute momentum smoothing to filter trade signals.
✅ Risk-adjusted trade execution based on Sharpe ratio & volatility filters.
✅ Backtested on historical stock data to optimize trade performance.

3️⃣ SARIMA-Based Oil Price Prediction (CodeToPredictOilPrices.py)
Description:

Uses SARIMA (Seasonal ARIMA) modeling to forecast crude oil & natural gas prices.
Incorporates macroeconomic factors, weather adjustments, and futures market roll yields to enhance predictive accuracy.
Key Features:
✅ Forecasts future oil prices with statistical time-series analysis.
✅ Integrates seasonal trends and external market shocks.
✅ Simulates contango & backwardation effects in the futures market.


📊 Example Output
Momentum-Based Trading Strategy Output (Live Market Tracking)

[10:32:45] AAPL Live Factors:
   📈 Momentum (5-min): 1.23% (Threshold: 1.00%)
   📊 Beta: 1.25 (Threshold: 1.20)
   📉 Volume (Last 3-min Sum): 432,000 (Threshold: 420,000)
   📏 Sharpe Ratio: 0.65 (Threshold: 0.50)
   📊 Risk-Adjusted Return: 0.0125 (Threshold: 0.0100)
✅ ENTER TRADE: AAPL meets momentum & volume criteria!

Oil Price Prediction Example

Estimated natural gas price on 2025-06-30: $4.52
🌟 Contributing
Feel free to fork the repository and propose improvements for new trading strategies, machine learning models, or risk management enhancements.

📩 Connect With Me
📧 Email: adhanani369@gmail.com
🔗 LinkedIn: # Quant_Trading_Algorithms
