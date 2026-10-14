"""Example 02: Querying Live Production API via RapidAPI Hub.

Requires a free or paid API key from:
https://rapidapi.com/organization/japan-opendata-lab
"""

import os
import sys

# Add parent directory to path for direct local import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from japan_opendata import JapanDataClient

def main():
    # Replace with your actual RapidAPI Key
    api_key = os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")

    client = JapanDataClient(api_key=api_key)

    print("=" * 70)
    print("Japan Official Data Megabank API - RapidAPI Client Quickstart")
    print("=" * 70)

    # 1. Search Government Procurement Awards for IT / Cloud
    print("\n[1] Searching IT / Cloud procurement awards (min 10M JPY):")
    try:
        proc_resp = client.procurement(q="クラウド", min_amount=10_000_000, limit=5)
        df = client.to_dataframe(proc_resp)
        if not df.empty:
            cols = [c for c in ["primary_name", "legal_name", "capital_amount_jpy", "corporate_number"] if c in df.columns]
            print(df[cols].to_string(index=False))
        else:
            print("No records returned or empty response.")
    except Exception as e:
        print(f"Request note (Check API Key): {e}")

    # 2. Search Land Valuation Benchmarks in Tokyo
    print("\n[2] Searching Land Prices in Tokyo (Shinjuku-ku):")
    try:
        land_resp = client.land_prices(city="新宿区", limit=5)
        df_land = client.to_dataframe(land_resp)
        if not df_land.empty:
            cols = [c for c in ["area_name_local", "current_value", "yoy_change_pct"] if c in df_land.columns]
            print(df_land[cols].to_string(index=False))
        else:
            print("No records returned or empty response.")
    except Exception as e:
        print(f"Request note: {e}")

if __name__ == "__main__":
    main()
