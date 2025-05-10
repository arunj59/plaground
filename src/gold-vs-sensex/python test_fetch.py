from gold_vs_sensex import fetch_gold_prices, fetch_sensex_prices, prepare_combined_data
from datetime import datetime, timedelta
import yfinance as yf

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 4, 1)

print(f"Testing from {start_date.date()} to {end_date.date()}")

# Fetch gold prices
try:
    gold_df = fetch_gold_prices(start_date, end_date)
    print("\nGold Data:")
    print(gold_df.head())
except Exception as e:
    print(f"Gold fetch error: {e}")

# Fetch Sensex prices
try:
    sensex_raw = yf.download("^BSESN", start=start_date, end=end_date)
    print("\nRaw Sensex DataFrame from yfinance:")
    print(sensex_raw.head())
except Exception as e:
    print(f"Sensex fetch error: {e}")


prepare_combined_data(start_date, end_date)