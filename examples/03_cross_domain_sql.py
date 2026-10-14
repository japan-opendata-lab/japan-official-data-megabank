"""Example 03: Cross-Domain Multi-Table JOIN via 13-Digit Corporate Key.

Demonstrates cross-linking Government Procurement Awards with Corporate Registry.
Runs entirely in-memory using DuckDB and remote Hugging Face sample Parquet.
"""

import duckdb

HF_BASE = "https://huggingface.co/datasets/japan-opendata/japan-official-data-megabank-showcase/resolve/main/data"

def main():
    print("=" * 75)
    print("Multi-Table Cross-Domain Analysis (Corporate Key JOIN)")
    print("=" * 75)

    con = duckdb.connect()

    procurement_url = f"{HF_BASE}/japan_public_procurement_sample_5k.parquet"
    corporate_url = f"{HF_BASE}/japan_corporate_invoices_sample_5k.parquet"

    # SQL Cross-Join using the universal 13-digit corporate_number
    query = f"""
        SELECT 
            p.legal_name AS vendor_name,
            p.corporate_number,
            c.prefecture AS corporate_headquarters,
            c.city AS headquarters_city,
            COUNT(p.primary_name) AS award_count,
            ROUND(SUM(p.capital_amount_jpy) / 1e6, 2) AS total_award_million_jpy
        FROM read_parquet('{procurement_url}') p
        INNER JOIN read_parquet('{corporate_url}') c
            ON p.corporate_number = c.corporate_number
        WHERE p.corporate_number IS NOT NULL
        GROUP BY p.legal_name, p.corporate_number, c.prefecture, c.city
        ORDER BY total_award_million_jpy DESC
        LIMIT 10
    """

    print("\nExecuting Cross-Domain JOIN across Procurement & Corporate Master...")
    df = con.execute(query).df()

    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("Note: Sample sets contain random samples; try querying individual tables or subscribe to MEGA tier for full 5M+ database joins.")

    print("\n[OK] Demonstration finished.")

if __name__ == "__main__":
    main()
