from pathlib import Path
from datetime import datetime
import time
import sqlite3
import pandas as pd
from pytrends.request import TrendReq

pd.set_option("future.no_silent_downcasting", True)

# ----------------------------------------------------------------------------
# 1. Resolve project directories inside the container
# ----------------------------------------------------------------------------
BASE_DIR = Path(_file_).resolve().parent.parent  # repo root
WAREHOUSE_DIR = BASE_DIR / "warehouse"  # mounted by Docker
DB_PATH = WAREHOUSE_DIR / "raw_data.db"
WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)  # first-run safety

# ----------------------------------------------------------------------------
# 2. Config
# ----------------------------------------------------------------------------
pytrend = TrendReq(hl="en-US", tz=360)

CRYPTO_NAMES = [
    "Bitcoin",
    "Ethereum",
    "Solana",
    "Avalanche",
    "Arbitrum",
    "Polygon",
    "Optimism",
    "Chainlink",
    "Cosmos",
    "Sui",
    "Aptos",
    "Injective",
    "Render Network",
    "Celestia",
    "Toncoin",
]

CRYPTO_TICKERS = [
    "BTC",
    "ETH",
    "SOL",
    "AVAX",
    "ARB",
    "MATIC",
    "OP",
    "LINK",
    "ATOM",
    "SUI",
    "APT",
    "INJ",
    "RNDR",
    "TIA",
    "TON",
]


# ----------------------------------------------------------------------------
# 3. Helpers
# ----------------------------------------------------------------------------
def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def collect_interest(keywords, retries=3):
    """Pull Google Trends interest_over_time and return a DF with load_ts."""
    df_all = pd.DataFrame()

    for sub in chunk(keywords, 1):  # 1 keyword per call
        for attempt in range(1, retries + 1):
            try:
                print(f"Collecting {sub} (attempt {attempt})")
                pytrend.build_payload(sub, timeframe="now 1-d")
                time.sleep(10)  # light throttle
                tmp = pytrend.interest_over_time()

                # Clean up dataframe
                tmp = (
                    tmp.drop(columns=["isPartial"], errors="ignore")
                    .rename_axis("date")
                    .reset_index()
                )
                tmp["load_ts"] = int(time.time())

                df_all = pd.concat([df_all, tmp], ignore_index=True)
                break  # success → stop retry loop

            except Exception as exc:
                print(f"Error on {sub}: {exc}")
                if attempt < retries:
                    print("Retrying in 100 s …")
                    time.sleep(100)
                else:
                    print(f"Giving up on {sub}")

    return df_all


# ----------------------------------------------------------------------------
# 4. Main ETL
# ----------------------------------------------------------------------------
if _name_ == "_main_":
    names_df = collect_interest(CRYPTO_NAMES)
    tickers_df = collect_interest(CRYPTO_TICKERS)

    print(f"SQLite path: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    names_df.to_sql("data_raw_names", conn, if_exists="replace", index=True)
    tickers_df.to_sql("data_raw_tickers", conn, if_exists="replace", index=True)

    # Bootstrap helper tables once
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS final_data (
            date        DATETIME,
            name        TEXT,
            name_hype   INTEGER,
            ticker_hype INTEGER,
            load_ts     INTEGER,
            PRIMARY KEY (name, date)
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS names_dict (
            name   TEXT PRIMARY KEY,
            ticker TEXT
        );
        """
    )
    for name, ticker in zip(CRYPTO_NAMES, CRYPTO_TICKERS):
        conn.execute(
            "INSERT OR IGNORE INTO names_dict (name, ticker) VALUES (?, ?)",
            (name, ticker),
        )

    conn.commit()
    conn.close()

    print("✔ Data saved to warehouse/raw_data.db")
