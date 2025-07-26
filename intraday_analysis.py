import pandas as pd
import yfinance as yf
import glob
import os

# Define the directory containing the CSV files
directory = "/media/remuru/new/performance/Reports/monday2"

# Use glob to find all CSV files in the directory
csv_files = glob.glob(os.path.join(directory, "*.csv"))

# Function to fetch stock data using yfinance
def get_stock_data(stock_ticker):
    try:
        # Append .NS if not present (for NSE stocks)
        if not stock_ticker.endswith('.NS') and not stock_ticker.endswith('.BO'):
            stock_ticker = stock_ticker + '.NS'
        stock = yf.Ticker(stock_ticker)
        data = stock.history(period="1d")
        day_high = data["High"].iloc[-1]
        close_price = data["Close"].iloc[-1]
        return day_high, close_price
    except Exception as e:
        print(f"Error fetching data for {stock_ticker}: {e}")
        return None, None

all_performance_rows = []  # Collect all rows for master sheet
# Process each CSV file
for csv_file in csv_files:
    print(f"Processing file: {csv_file}")

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Initialize a list to store performance data for the current CSV file
    performance_data = []

    # Process each stock and calculate required metrics
    for index, row in df.iterrows():
        stock = row["Stock"]
        ltp = row["LTP"]

        # Fetch Day High and Close Price
        day_high, close_price = get_stock_data(stock)

        if day_high is not None and close_price is not None:
            # Calculate Day High Difference
            day_high_diff = day_high - ltp
            # Calculate Day High Percentage Difference
            day_high_pct = (day_high_diff / ltp) * 100 if ltp != 0 else None

            # Assume EoD is the same as Close Price for this example
            eo_d = close_price
            eo_d_diff = eo_d - ltp
            eo_d_pct = (eo_d_diff / ltp) * 100 if ltp != 0 else None

            # Append to performance data
            performance_data.append({
                "Stock": stock,
                "LTP": round(ltp, 2),
                "DayHigh": round(day_high, 2),
                "DayHighDiff": round(day_high_diff, 2),
                # Removed DayHighDiffPct
                "EoD": round(eo_d, 2),
                "EoDDiff": round(eo_d_diff, 2),
                # Removed EoDDiffPct
            })
        else:
            # Still append row with NaN if data not found
            performance_data.append({
                "Stock": stock,
                "LTP": round(ltp, 2),
                "DayHigh": day_high if day_high is None else round(day_high, 2),
                "DayHighDiff": None,
                # Removed DayHighDiffPct
                "EoD": close_price if close_price is None else round(close_price, 2),
                "EoDDiff": None,
                # Removed EoDDiffPct
            })

    # Create the performance sheet for the current CSV file
    performance_df = pd.DataFrame(performance_data)

    # Calculate BASKET (total) row
    total_ltp = performance_df['LTP'].sum()
    total_dayhigh = performance_df['DayHigh'].sum()
    total_eod = performance_df['EoD'].sum()
    total_dayhighdiff = performance_df['DayHighDiff'].sum() if 'DayHighDiff' in performance_df else None
    total_eoddiff = performance_df['EoDDiff'].sum() if 'EoDDiff' in performance_df else None

    # Calculate percentage differences
    total_dayhighdiff_pct = (total_dayhighdiff / total_ltp * 100) if total_ltp != 0 and total_dayhighdiff is not None else None
    total_eoddiff_pct = (total_eoddiff / total_ltp * 100) if total_ltp != 0 and total_eoddiff is not None else None

    # Format the BASKET row
    basket_row = {
        'Stock': 'BASKET',
        'LTP': round(total_ltp, 2),
        'DayHigh': round(total_dayhigh, 2),
        'DayHighDiff': f"{round(total_dayhighdiff, 2)}({round(total_dayhighdiff_pct, 2)}%)" if total_dayhighdiff is not None and total_dayhighdiff_pct is not None else None,
        # Removed DayHighDiffPct
        'EoD': round(total_eod, 2),
        'EoDDiff': f"{round(total_eoddiff, 2)}({round(total_eoddiff_pct, 2)}%)" if total_eoddiff is not None and total_eoddiff_pct is not None else None,
        # Removed EoDDiffPct
    }

    # Append the BASKET row
    performance_df = pd.concat([performance_df, pd.DataFrame([basket_row])], ignore_index=True)

    # Add all rows except BASKET to master list
    all_performance_rows.extend(performance_df[performance_df['Stock'] != 'BASKET'].to_dict('records'))

    # Save the performance sheet with the same base name as the input CSV file
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    output_csv_path = os.path.join(directory, f"{base_name}_performance.csv")
    performance_df.to_csv(output_csv_path, index=False)

    print(f"Performance sheet generated successfully for {csv_file} and saved as {output_csv_path}")

# Create master sheet with unique stocks only (keep first occurrence)
master_df = pd.DataFrame(all_performance_rows)
master_df = master_df.drop_duplicates(subset=['Stock'], keep='first')

# Calculate BASKET (total) row for master sheet
if not master_df.empty:
    total_ltp = master_df['LTP'].sum()
    total_dayhigh = master_df['DayHigh'].sum()
    total_eod = master_df['EoD'].sum()
    total_dayhighdiff = master_df['DayHighDiff'].sum() if 'DayHighDiff' in master_df else None
    total_eoddiff = master_df['EoDDiff'].sum() if 'EoDDiff' in master_df else None
    total_dayhighdiff_pct = (total_dayhighdiff / total_ltp * 100) if total_ltp != 0 and total_dayhighdiff is not None else None
    total_eoddiff_pct = (total_eoddiff / total_ltp * 100) if total_ltp != 0 and total_eoddiff is not None else None
    basket_row = {
        'Stock': 'BASKET',
        'LTP': round(total_ltp, 2),
        'DayHigh': round(total_dayhigh, 2),
        'DayHighDiff': f"{round(total_dayhighdiff, 2)}({round(total_dayhighdiff_pct, 2)}%)" if total_dayhighdiff is not None and total_dayhighdiff_pct is not None else None,
        # Removed DayHighDiffPct
        'EoD': round(total_eod, 2),
        'EoDDiff': f"{round(total_eoddiff, 2)}({round(total_eoddiff_pct, 2)}%)" if total_eoddiff is not None and total_eoddiff_pct is not None else None,
        # Removed EoDDiffPct
    }
    master_df = pd.concat([master_df, pd.DataFrame([basket_row])], ignore_index=True)

master_output_path = os.path.join(directory, 'master_performance.csv')
master_df.to_csv(master_output_path, index=False)
print(f"Master performance sheet generated and saved as {master_output_path}")

print("All performance sheets generated successfully!")
