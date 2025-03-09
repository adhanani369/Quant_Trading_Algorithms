import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime

# Load the natural gas price data
file_path = "/Users/aayushdhanani/Downloads/Nat_Gas.csv"  # Ensure the CSV file is in the same directory
df = pd.read_csv(file_path)
df['Dates'] = pd.to_datetime(df['Dates'])
df.set_index('Dates', inplace=True)
df = df.asfreq('M')  # Ensure monthly frequency

# Fit SARIMA model (Seasonal ARIMA for better trend & seasonality capture)
sarima_model = SARIMAX(df['Prices'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
sarima_fitted = sarima_model.fit()

# Forecast the next 12 months (Base Forecast)
future_dates = pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')
base_forecast = sarima_fitted.forecast(steps=12)
base_forecast_df = pd.DataFrame({'Dates': future_dates, 'Base_Forecast': base_forecast})

# Simulate Weather Surge Adjustment using historical weather impact coefficients
weather_adjustments = np.random.uniform(0.5, 2.0, 12)  # Impact range per MMBtu
base_forecast_df['Weather_Adjustment'] = weather_adjustments
base_forecast_df['Weather_Adjusted_Forecast'] = base_forecast_df['Base_Forecast'] + base_forecast_df['Weather_Adjustment']

# Simulate Futures Roll & Contango Adjustments
roll_yield_adjustments = np.random.uniform(-0.5, 1.5, 12)
base_forecast_df['Roll_Yield_Adjustment'] = roll_yield_adjustments
base_forecast_df['Final_Adjusted_Forecast'] = base_forecast_df['Weather_Adjusted_Forecast'] + base_forecast_df['Roll_Yield_Adjustment']

# Plot the final forecast
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Prices'], marker='o', linestyle='-', label="Historical Prices")
plt.plot(base_forecast_df['Dates'], base_forecast_df['Final_Adjusted_Forecast'], marker='o', linestyle='--', label="Forecasted Prices", color='red')
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.title("Enhanced Natural Gas Price Forecast (Weather & Futures Adjustments)")
plt.legend()
plt.grid(True)
plt.show()

# Function to estimate price on a given date
def estimate_gas_price(input_date):
    input_date = pd.to_datetime(input_date)
    if df.index.min() <= input_date <= df.index.max():
        closest_date = df.iloc[(df.index - input_date).abs().argsort()[:1]]
        return float(closest_date['Prices'].values[0])
    elif df.index.max() < input_date <= base_forecast_df['Dates'].max():
        closest_date = base_forecast_df.iloc[(base_forecast_df['Dates'] - input_date).abs().argsort()[:1]]
        return float(closest_date['Final_Adjusted_Forecast'].values[0])
    else:
        return "Date out of range for estimation."

# Example usage
example_date = "2025-06-30"
estimated_price = estimate_gas_price(example_date)
print(f"Estimated natural gas price on {example_date}: ${estimated_price:.2f}")
