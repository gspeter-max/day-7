'''
Problem 1: Pandas – Complex Rolling Window Aggregation with Dynamic Conditions
Problem Statement:
You are given a large dataset of stock market trades with the following columns:

trade_id (int): Unique identifier of a trade.
timestamp (datetime): Timestamp when the trade happened.
symbol (str): Stock symbol (e.g., "AAPL", "GOOG", "TSLA").
price (float): The price of the stock at that time.
volume (int): The number of shares traded.
The dataset is stored in a pandas DataFrame called df, and it is not sorted by timestamp.

Task:

Compute the rolling 5-minute weighted average price (VWAP) per stock symbol, but only for timestamps where at least 10 trades have occurred in that 5-minute window.
If a trade does not belong to any 5-minute window meeting the 10-trade threshold, return NaN for that trade.
The dataset is huge (100M+ rows), so you must solve this efficiently.
Assume timestamps are not perfectly spaced, meaning a standard rolling window approach won’t work easily.'''

import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate random timestamps within a single trading day (e.g., 9:30 AM to 4:00 PM)
num_trades = 500_000  # Half a million trades
start_time = pd.Timestamp("2024-01-30 09:30:00")
end_time = pd.Timestamp("2024-01-30 16:00:00")

timestamps = pd.to_datetime(
    np.random.uniform(start_time.timestamp(), end_time.timestamp(), num_trades),
    unit="s"
)

# Random stock symbols
symbols = np.random.choice(["AAPL", "GOOG", "TSLA", "MSFT", "AMZN"], num_trades)

# Generate realistic stock prices and volumes
prices = np.random.uniform(100, 2000, num_trades).round(2)
volumes = np.random.randint(1, 1000, num_trades)

# Create the DataFrame
df = pd.DataFrame({"trade_id": np.arange(1, num_trades + 1),
                   "timestamp": timestamps,
                   "symbol": symbols,
                   "price": prices,
                   "volume": volumes})

# Shuffle the DataFrame to ensure timestamps are unsorted
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df = df.sort_values(by = ['symbol','timestamp'])

def compute_roling(group): 
    group = group.set_index('timestamp')
    total_upper = (group['price'] * group['volume']).rolling(window = '5min').sum() 
    count = group['volume'].rolling('5min').count() 
    lower_part  = group['volume'].rolling(window = '5min').sum() 
    vwap = total_upper / lower_part 
    vwap[count < 10] = np.nan
    return vwap

df['vwap'] = df.groupby('symbol', group_keys = False).apply(compute_roling).reset_index(drop = True )

print(df)
\



