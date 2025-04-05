# Import the fetch_data function from data_loader.py
from data_loader import fetch_data

# Define parameters
ticker = 'AAPL'
start = '2025-01-01'
end = '2025-03-31'

# Fetch data and save to CSV
data_frame = fetch_data(ticker, start, end, save_to_csv=True)

# The data is now saved in the 'csv' folder and also available as a DataFrame
print(data_frame.head())
