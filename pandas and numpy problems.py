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

'''
Problem 2: NumPy – Custom Multi-Dimensional Tensor Operations
Problem Statement:
You are given a 4D tensor stored in a NumPy array X of shape (B, C, H, W), representing a batch of images:

B: Number of images in the batch (batch size).
C: Number of channels (e.g., RGB → 3 channels).
H: Height of the image.
W: Width of the image.
You need to perform the following operations efficiently (without explicit loops for large tensors):

Compute the per-channel mean and standard deviation across the entire batch and normalize each channel independently (standardization).
Apply a Gaussian blur filter of kernel size (3,3), but only on the first half of the images in the batch (X[:B//2]), while keeping the other half unchanged.
Rotate each image by 90° clockwise, but only for images where the sum of pixel intensities in the first channel (X[:,0,:,:]) is greater than the median sum across the batch.
Flatten the final result back to shape (B, -1) for further processing.
'''




import numpy as np

from scipy.ndimage import gaussian_filter 
# Set parameters
B, C, H, W = 128, 3, 64, 64  # Batch size, Channels, Height, Width

# Generate random image data (pixel values between 0 and 255)
x = np.random.randint(0, 256, (B, C, H, W), dtype=np.uint8)

channels_means = x.mean(axis = (0,2,3), keepdims  = True).round(2)
channels_std = x.std(axis = (0,2,3), keepdims = True).round(2)  
x_standardized = ((x - channels_means)/ (channels_std + 1e-8))

x[:B//2] = gaussian_filter(x[:B//2],sigma = (0,0,1,1))
    
filters_sum = x[:,0,:,:].sum(axis = (1,2))
filters_median  = np.median(filters_sum)
filter_index = filters_sum > filters_median
x[filter_index] = np.rot90(x[filter_index], k =-1,axes = (2,3))
reshaped = x.reshape(B,-1)
print(reshaped)

