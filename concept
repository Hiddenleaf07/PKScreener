import os
import sys
import time
import pickle
import pandas as pd
import numpy as np
import warnings
import multiprocessing
from datetime import datetime

warnings.filterwarnings("ignore", category=FutureWarning)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test.classes.test_Pktalib import pktalib


def load_stock_data(original_path, optimized_path):
    if os.path.exists(optimized_path):
        try:
            print("📦 Loading optimized stock data...")
            load_start = time.time()
            with open(optimized_path, "rb") as f:
                data = pickle.load(f)
            print(f"✅ Loaded stock data for {len(data)} tickers in {time.time() - load_start:.2f} seconds.")
            return data
        except Exception as e:
            print(f"⚠️ Error loading optimized file: {e}. Falling back to original.")

    print("📦 Loading stock data from original source...")
    if not os.path.exists(original_path):
        print(f"❌ Original pickle file {original_path} does not exist.")
        return {}

    try:
        load_start = time.time()
        with open(original_path, "rb") as f:
            data = pickle.load(f)

        print("⚙️ Converting dictionaries to DataFrames...")
        data = {
            k: pd.DataFrame(**v).sort_index(ascending=True)
            if isinstance(v, dict) else v
            for k, v in data.items()
        }

        print("💾 Saving optimized data...")
        try:
            with open(optimized_path, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            print("✅ Optimized data saved.")
        except Exception as e:
            print(f"❌ Error saving optimized file: {e}")

        print(f"✅ Loaded & optimized {len(data)} tickers in {time.time() - load_start:.2f} seconds.")
        return data
    except Exception as e:
        print(f"❌ Error loading original pickle file: {e}")
        return {}


def calculate_technical_indicators(df):
    if df is None or df.empty:
        return None

    df = df.copy()
    close = df["Close"].astype(np.float64).values
    high = df["High"].astype(np.float64).values
    low = df["Low"].astype(np.float64).values
    volume = df["Volume"].astype(np.float64).values


    df['RSI'] = pktalib.RSI(close, 14)
    df['RSIi'] = df['RSI']
    df['SMA50'] = pktalib.SMA(close, 50)
    df['SMA200'] = pktalib.SMA(close, 200)
    df['VolumeMA7'] = pktalib.SMA(volume, 7)
    df['VolumeMA20'] = pktalib.SMA(volume, 20)
    df['CCI'] = pktalib.CCI(high, low, close, 14)
    df['ATR'] = pktalib.ATR(high, low, close, 14)

    return df


def screen_one_stock(stock_tuple):
    symbol, df = stock_tuple
    if df is None or df.empty:
        return None

    try:
        df = calculate_technical_indicators(df)
        if df is None or df.empty:
            return None

        recent = df.iloc[-1]
        recent = recent.replace([np.inf, -np.inf], 0).fillna(0)

        atr = recent['ATR']
        candle = recent['Close'] - recent['Open']
        atr_cross = candle >= atr
        bullish_rsi = recent['RSI'] >= 55
        smav7 = recent['VolumeMA7']
        volume_rise = recent["Volume"] > smav7 if smav7 != 0 else False

        if not (atr_cross and bullish_rsi and volume_rise):
            return None

        high_52w = df["High"].max()
        low_52w = df["Low"].min()
        if len(df) > 1:
            pct_change = ((recent['Close'] - df.iloc[-2]['Close']) / df.iloc[-2]['Close']) * 100
        else:
            pct_change = 0

        df_22 = df.tail(22)
        range_22 = ((df_22["High"].max() - df_22["Low"].min()) / df_22["Low"].min() * 100) if len(df_22) > 0 else 0
        consol_range = f"Range:{range_22:.1f}%"

        volume_ratio = recent["Volume"] / smav7 if smav7 != 0 else 0
        volume_str = f"{volume_ratio:.2f}x" if volume_ratio >= 1 else f"{recent['Volume']/1e5:.2f}L"

        ma_signal = []
        if recent['Close'] > recent['SMA50']:
            ma_signal.append("Bullish")
        if recent['Close'] > recent['SMA200']:
            ma_signal.append("Above MA200")

        trend = "Strong Up" if recent['Close'] > recent['SMA50'] and recent['SMA50'] > recent['SMA200'] else "Mixed"
        pattern = "ATR Breakout" if atr_cross else ""
        current_time = datetime.now().strftime("%d/%m %H:%M")

        return {
            "Stock": symbol,
            "LTP": recent['Close'],
            "%Chng": pct_change,
            "52Wk-H": high_52w,
            "52Wk-L": low_52w,
            "RSI": recent['RSI'],
            "Volume": volume_str,
            "22-Pd": f"{range_22:.2f}%",
            "Consol.": consol_range,
            "Breakout(22Prds)": f"BO: {df_22['High'].max():.2f} R: {df_22['Low'].min():.2f}",
            "MA-Signal": ", ".join(ma_signal),
            "Trend(22Prds)": trend,
            "Pattern": pattern,
            "CCI": recent['CCI'],
            "Time": current_time,
            "ATR": atr
        }

    except Exception as e:
        print(f"⚠️ Error processing {symbol}: {str(e)}")
        return None


def format_results(results_df):
    headers = results_df.columns
    separator_parts = []
    for header in headers:
        if header == "Stock":
            separator_parts.append("N=======")
        elif header == "LTP":
            separator_parts.append("E=====")
        elif header in ["%Chng", "22-Pd"]:
            separator_parts.append("R=======")
        elif header in ["52Wk-H", "52Wk-L"]:
            separator_parts.append("P========")
        elif header == "RSI":
            separator_parts.append("K========")
        elif header == "Volume":
            separator_parts.append("S=====")
        elif header == "Consol.":
            separator_parts.append("C========")
        elif header == "Breakout(22Prds)":
            separator_parts.append("R=======")
        elif header == "MA-Signal":
            separator_parts.append("E===========")
        elif header == "Trend(22Prds)":
            separator_parts.append("N======================")
        elif header == "Pattern":
            separator_parts.append("E=======")
        elif header == "CCI":
            separator_parts.append("P=====")
        elif header == "Time":
            separator_parts.append("K======")
        elif header == "ATR":
            separator_parts.append("S====")
    separator_line = "|" + "|".join(separator_parts) + "|"

    formatted_df = results_df.copy()
    formatted_df["LTP"] = formatted_df["LTP"].apply(lambda x: f"{x:.2f}")
    formatted_df["%Chng"] = formatted_df["%Chng"].apply(lambda x: f"{x:.1f}%")
    formatted_df["52Wk-H"] = formatted_df["52Wk-H"].apply(lambda x: f"{x:.2f}")
    formatted_df["52Wk-L"] = formatted_df["52Wk-L"].apply(lambda x: f"{x:.2f}")
    formatted_df["RSI"] = formatted_df["RSI"].astype(int)
    formatted_df["CCI"] = formatted_df["CCI"].astype(int)
    formatted_df["ATR"] = formatted_df["ATR"].astype(int)

    return formatted_df, separator_line


def main():
    original_pickle = "/media/remuru/0D021B660D021B66/pkscreener/results_pkl/stock_data_080725.pkl"
    optimized_pickle = "/media/remuru/0D021B660D021B66/pkscreener/results_pkl/stock_data_optimized.pkl"

    stock_data = load_stock_data(original_pickle, optimized_pickle)
    if not stock_data:
        print("🚪 No stock data loaded. Exiting.")
        return

    print("\n🔍 Starting ATR Crossover scan (Parallel)...")
    print("📌 Conditions: ATR Cross + RSI ≥ 55 + Volume Rise")
    scan_start = time.time()

    cpu_count = max(1, multiprocessing.cpu_count() - 1)
    with multiprocessing.Pool(processes=cpu_count) as pool:
        results = pool.imap_unordered(screen_one_stock, stock_data.items(), chunksize=50)
        screened_stocks = [r for r in results if r is not None]

    scan_elapsed = time.time() - scan_start
    print(f"\n⏱️ Scan completed in {scan_elapsed:.2f} seconds.")
    print(f"📊 {len(screened_stocks)} stocks matched ATR crossover criteria.")

    if screened_stocks:
        results_df = pd.DataFrame(screened_stocks)
        formatted_df, separator_line = format_results(results_df)

        print("\n📊 ATR Crossover Results:")
        print("|" + "|".join([col.center(8) for col in formatted_df.columns]) + "|")
        print(separator_line)
        for _, row in formatted_df.iterrows():
            print("|" + "|".join(str(x).center(8) for x in row) + "|")
    else:
        print("📭 No stocks matched ATR crossover criteria.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    total_start = time.time()
    main()
    print(f"\n⏳ Total time (load + scan): {time.time() - total_start:.2f} seconds.")
