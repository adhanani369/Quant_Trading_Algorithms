import requests
import yfinance as yf
import time
from datetime import datetime

# API Configuration
ALPHA_API_KEY = "VZY9IQ4ECHCYMQVP"
ALPHA_BASE_URL = "https://www.alphavantage.co/query"
STOCK_TICKER = "AAPL"

# Strategy Parameters
momentum_threshold = 0.01  # 1% intraday move
beta_threshold = 1.2  # High-volatility filter
sharpe_min_threshold = 0.5  # Minimum Sharpe Ratio
risk_adjusted_return_min = 0.01  # Minimum Risk-Adjusted Return

# Store price and volume history
price_history = []
volume_history = []  # Store past volumes for dynamic threshold

# Function to Fetch Historical Volume from Yahoo Finance
def get_yahoo_historical_volume(symbol):
    print("📥 Fetching 8-day historical volume from Yahoo Finance...")
    stock = yf.Ticker(symbol)
    data = stock.history(period="8d", interval="1m")  # Fetch last 8 days of 1-minute data

    if not data.empty:
        avg_minute_volume = data["Volume"].mean()  # Calculate average volume per minute
        avg_second_volume = avg_minute_volume / 60  # Convert to per-second volume
        print(f"✅ 8-days Avg Minute Volume: {avg_minute_volume:,.0f}, Per-Second: {avg_second_volume:.2f}")
        return avg_second_volume
    print("❌ Failed to fetch historical volume from Yahoo Finance.")
    return None

# Function to Fetch Last 5 Close Prices from Yahoo Finance
def get_yahoo_historical_prices(symbol):
    print("📥 Fetching last 5 close prices from Yahoo Finance...")
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="1m")  # Fetch today's 1-minute data

    if not data.empty:
        last_5_prices = data["Close"].dropna().tail(5).tolist()  # Get the last 5 closing prices
        print(f"✅ Preloaded last 5 close prices: {last_5_prices}")
        return last_5_prices
    print("❌ Failed to fetch historical close prices.")
    return []

# Function to Fetch Live Price & Volume from Alpha Vantage
def get_live_price(symbol):
    url = f"{ALPHA_BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&outputsize=compact&apikey={ALPHA_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (1min)" in data:
        timestamps = list(data["Time Series (1min)"].keys())[:3]  # Get last 3 timestamps
        latest_data = data["Time Series (1min)"][timestamps[0]]
        prev_data1 = data["Time Series (1min)"][timestamps[1]]
        prev_data2 = data["Time Series (1min)"][timestamps[2]]

        open_price = float(latest_data["1. open"])
        close_price = float(latest_data["4. close"])

        # Fetch cumulative volume over last 3 minutes
        volume = float(latest_data["5. volume"]) + float(prev_data1["5. volume"]) + float(prev_data2["5. volume"])

        return open_price, close_price, volume

    print(f"❌ API failed for {symbol}: {data}")
    return None, None, None

# Function to Calculate Smoothed 5-Minute Momentum
def calculate_momentum(prices):
    if len(prices) < 5:
        return 0  # Not enough data points yet

    avg_price_5min = sum(prices[-5:]) / 5  # 5-minute moving average
    latest_price = prices[-1]

    momentum = ((latest_price - avg_price_5min) / avg_price_5min) * 100  # Percentage change
    return momentum

# Function to Track AAPL in Real-Time & Print Factor Values
def track_stock(avg_second_volume):
    print(f"🔄 Tracking {STOCK_TICKER} in real-time (1-minute interval)...")

    while True:
        try:
            open_price, close_price, volume = get_live_price(STOCK_TICKER)

            if open_price and close_price and volume:
                # Debug: Print price history before updating
                print(f"Before appending: {price_history}")

                # Store the latest price
                price_history.append(close_price)
                volume_history.append(volume)  # Store volume history

                # Keep only last 5 prices
                if len(price_history) > 5:
                    price_history.pop(0)

                # Keep only last 60 minutes of volume
                if len(volume_history) > 60:
                    volume_history.pop(0)

                # Calculate smoothed momentum
                momentum_5min = calculate_momentum(price_history)

                # Dynamically update volume threshold using correct value
                dynamic_second_volume = avg_second_volume  # Fix: Use correct volume

                # Simulate other factors (placeholders for now)
                beta = 1.25  # Mock beta value
                sharpe_ratio = 0.6  # Mock Sharpe ratio
                risk_adjusted_return = 0.012  # Mock risk-adjusted return

                # Print all values at each interval
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {STOCK_TICKER} Live Factors:")
                print(f"   📈 Momentum (5-min): {momentum_5min:.2f}% (Threshold: {momentum_threshold*100:.2f}%)")
                print(f"   📊 Beta: {beta:.2f} (Threshold: {beta_threshold:.2f})")
                print(f"   📉 Volume (Last 3-min Sum): {volume:,.0f} (Threshold: {dynamic_second_volume:,.0f})")
                print(f"   📏 Sharpe Ratio: {sharpe_ratio:.2f} (Threshold: {sharpe_min_threshold:.2f})")
                print(f"   📊 Risk-Adjusted Return: {risk_adjusted_return:.4f} (Threshold: {risk_adjusted_return_min:.4f})")

                # Entry & Exit Conditions
                if momentum_5min >= momentum_threshold and volume >= dynamic_second_volume:
                    print(f"✅ ENTER TRADE: {STOCK_TICKER} meets momentum & volume criteria!")
                elif momentum_5min < momentum_threshold:
                    print(f"🚨 EXIT TRADE: Momentum Below Threshold!")

            time.sleep(60)  # Fetch new data every 1 minute
        except Exception as e:
            print(f"❌ Error tracking {STOCK_TICKER}: {e}")
            break

# Run the Live Tracking for AAPL with Dynamic Volume Benchmark
if __name__ == "__main__":

    avg_second_volume = get_yahoo_historical_volume(STOCK_TICKER)  # Get volume from Yahoo Finance
    if avg_second_volume:
        # Preload price history before starting tracking
        price_history = get_yahoo_historical_prices(STOCK_TICKER)
        if price_history:  # Ensure at least 5 prices are available
            track_stock(avg_second_volume)
        else:
            print("❌ Not enough historical price data to start tracking.")
