import pickle
import numpy as np
import talib
from datetime import datetime
import sys
import pandas as pd

def bare_metal_scan():
    start_time = datetime.now()

    # Load with minimal overhead
    load_start = datetime.now()
    with open("/media/remuru/0D021B660D021B66/pkscreener/sample-data/stock_data_optimized.pkl", "rb") as f:
        stock_data = pickle.load(f)
    load_time = (datetime.now() - load_start).total_seconds()

    scan_start = datetime.now()
    results = []

    # Raw loop with minimal Python overhead
    items = stock_data.items()

    for symbol, df in items:
        if df is None or len(df) < 14:
            continue

        try:
            # Direct access with error handling
            close = df["Close"].values
            if len(close) < 14 or close[-1] <= 0:
                continue

            # Ensure float64
            if close.dtype != np.float64:
                close = close.astype(np.float64)

            # Fast calculations
            rsi = talib.RSI(close, 14)
            if np.isnan(rsi[-1]) or rsi[-1] < 55:
                continue

            open_price = df["Open"].values
            if open_price.dtype != np.float64:
                open_price = open_price.astype(np.float64)

            high = df["High"].values
            if high.dtype != np.float64:
                high = high.astype(np.float64)

            low = df["Low"].values
            if low.dtype != np.float64:
                low = low.astype(np.float64)

            volume = df["Volume"].values
            if volume.dtype != np.float64:
                volume = volume.astype(np.float64)

            # Calculate remaining indicators
            atr = talib.ATR(high, low, close, 14)
            if np.isnan(atr[-1]) or atr[-1] <= 0:
                continue

            vol_ma7 = talib.SMA(volume, 7)
            if (np.isnan(vol_ma7[-1]) or vol_ma7[-1] <= 0 or 
                volume[-1] <= vol_ma7[-1]):
                continue

            # Final check
            candle = close[-1] - open_price[-1]
            if candle >= atr[-1]:
                # Ultra-fast string building
                results.append(symbol + ": " + str(round(close[-1], 2)))

        except:
            continue

    scan_time = (datetime.now() - scan_start).total_seconds()
    total_time = (datetime.now() - start_time).total_seconds()

    print(f"Load Time: {load_time:.3f}s")
    print(f"Scan Time: {scan_time:.3f}s")
    print(f"Total Time: {total_time:.3f}s | Found: {len(results)} stocks")

    # Save to Excel
    if results:
        # Parse results for Excel
        watchlist_data = []
        for item in results:
            symbol, price = item.split(": ")
            watchlist_data.append({
                "Symbol": symbol, 
                "Price": float(price),
                "Scan_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Save to Excel
        df_watchlist = pd.DataFrame(watchlist_data)
        df_watchlist.to_excel("watchlist.xlsx", index=False)
        print("✅ Watchlist saved to watchlist.xlsx")
        
        # Ultra-fast output to console
        sys.stdout.write('\n'.join(results) + '\n')
        sys.stdout.flush()
    else:
        print("❌ No stocks found matching criteria")


if __name__ == "__main__":
    bare_metal_scan()