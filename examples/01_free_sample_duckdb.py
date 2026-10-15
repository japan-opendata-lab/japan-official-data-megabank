"""Example 01: Free Sample Exploration via DuckDB & Hugging Face.

Zero API keys or download steps required.
Queries remote Parquet files hosted on Hugging Face directly in memory.
"""

import duckdb

HF_BASE = "https://huggingface.co/datasets/japan-opendata/japan-official-data-megabank-showcase/resolve/main/data"


def main():
    print("=" * 70)
    print("Japan Open Data Showcase - Instant In-Memory DuckDB Query")
    print("=" * 70)

    con = duckdb.connect()

    # 1. Government Procurement Top Awardees
    procurement_url = f"{HF_BASE}/japan_public_procurement_sample_5k.parquet"
    print("\n[1] Top 5 Suppliers by Total Public Award Value (GEPS):")
    query_proc = f"""
        SELECT
            legal_name,
            corporate_number,
            count(*) AS total_contracts,
            ROUND(SUM(capital_amount_jpy) / 1e8, 2) AS total_award_100m_yen
        FROM read_parquet('{procurement_url}')
        WHERE legal_name IS NOT NULL
        GROUP BY legal_name, corporate_number
        ORDER BY total_award_100m_yen DESC
        LIMIT 5
    """
    df_proc = con.execute(query_proc).df()
    print(df_proc.to_string(index=False))

    # 2. Historical Land Price Leaders
    land_url = f"{HF_BASE}/japan_land_prices_sample_5k.parquet"
    print("\n[2] Benchmark Land Valuation Points (MLIT):")
    query_land = f"""
        SELECT
            area_name_local,
            current_value AS land_price_yen_per_sqm,
            yoy_change_pct,
            event_date
        FROM read_parquet('{land_url}')
        ORDER BY current_value DESC
        LIMIT 5
    """
    df_land = con.execute(query_land).df()
    print(df_land.to_string(index=False))

    print("\n[OK] Query completed successfully.")


if __name__ == "__main__":
    main()
