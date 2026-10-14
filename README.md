# Japan Public Open Data Megabank (Python SDK & Starter Kit)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/japan-opendata-lab/japan-official-data-megabank/blob/main/notebooks/japan_open_data_in_3_minutes.ipynb)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97-Hugging%20Face%20Showcase-yellow)](https://huggingface.co/datasets/japan-opendata/japan-official-data-megabank-showcase)
[![RapidAPI Hub](https://img.shields.io/badge/Production%20API-RapidAPI%20Hub-orange)](https://rapidapi.com/organization/japan-opendata-lab)

**Institutional-grade Japanese public open data normalized to US Federal & SEC standards (by Japan Open Data Lab).**

Messy quirks common in Japanese government spreadsheets (Shift_JIS encoding, Reiwa/Heisei imperial eras, merged cells, zenkaku strings, and individual proprietorship PII) have been **mechanically eliminated**. 

All records are cross-linkable via the official **13-digit National Tax Agency Corporate Number (`corporate_number`)** and **5-digit JIS Municipality Code (`municipality_code`)**.

👉 **[Try the 3-Minute Google Colab Recipe (Zero Setup Required)](https://colab.research.google.com/github/japan-opendata-lab/japan-official-data-megabank/blob/main/notebooks/japan_open_data_in_3_minutes.ipynb)**

---

## ⚡ 30-Second Quickstart (Zero API Key / Zero Download)

Query remote Parquet samples hosted on Hugging Face directly in-memory using **DuckDB**:

```python
import duckdb

url = "https://huggingface.co/datasets/japan-opendata/japan-official-data-megabank-showcase/resolve/main/data/japan_public_procurement_sample_5k.parquet"

# Query government tender awards in 1 line
df = duckdb.query(f"""
    SELECT legal_name, SUM(capital_amount_jpy) AS total_won, COUNT(*) AS deals
    FROM read_parquet('{url}')
    GROUP BY legal_name
    ORDER BY total_won DESC
    LIMIT 5
""").df()

print(df)
```

---

## 🏛️ Why This Dataset? (Overcoming Japan's Data Quirks)

Working with Japanese public government data typically requires dozens of hours of manual cleaning:

| Traditional Government Data Obstacle | Japan Megabank Solution |
| :--- | :--- |
| **Shift_JIS Encoding** (Broken text / mojibake in modern pipelines) | **100% UTF-8 Cleaned** across all files and API endpoints |
| **Imperial Eras** (令和5年, 平成28年 require complex parsing) | **ISO-8601 Western Dates** (`YYYY-MM-DD` / `YYYY`) |
| **Merged Cells & Multilevel Headers** in Excel tables | **Flat 24-Column snake_case Tables** conforming to US SEC standards |
| **PII & Sole Proprietorships** mixed with commercial corporations | **100% Corporate Purge**: Verified against National Tax Agency registry |
| **Disparate Key Systems** across ministries | **Universal 13-Digit Corporate Key & 5-Digit JIS Municipal Code** |

---

## 📦 Master Datasets Included

| Domain | Historical Coverage | Production Records | Primary Source |
| :--- | :---: | :---: | :--- |
| **Public Procurement (GEPS)** | 2020 – 2026 (7 Yrs) | ~285,000+ | Digital Agency / All Central Ministries |
| **Corporate Tax Registry** | Nationwide Live | ~5,100,000+ | National Tax Agency (法人番号公表サイト) |
| **Land Price Benchmark** | 1983 – 2026 (44 Yrs) | ~1,100,000+ | Ministry of Land, Infrastructure, Transport (地価公示) |
| **Healthcare & Clinics** | Nationwide Live | ~220,000+ | Ministry of Health, Labour and Welfare (医療情報ネット) |
| **Senior & Nursing Care** | Nationwide Live | ~250,000+ | Ministry of Health, Labour and Welfare (介護サービス公表) |
| **GHG Carbon Emissions** | Multi-Year | Mandatory Filers | Ministry of the Environment (温室効果ガス算定公表) |
| **Municipal Demographics** | All 1,741 Cities | Nationwide | Ministry of Internal Affairs and Communications (MIC) |

---

## 🚀 Live Production API (RapidAPI Hub)

For live real-time access to the entire 40+ year archive or high-frequency analytical queries, connect via **[RapidAPI Hub](https://rapidapi.com/organization/japan-opendata-lab)**.

### Pricing Tiers

| Tier | Price | Monthly Quota | Historical Archive | Key Feature |
| :--- | :---: | :---: | :---: | :--- |
| **BASIC** | **$0 / mo** | 50 req/mo | Past 2 Years | Free schema testing & integration validation |
| **PRO** | **$99 / mo** | 10,000 req/mo | Past 5 Years | All nationwide categories, up to 1,000 records/req |
| **ULTRA** | **$299 / mo** | 50,000 req/mo | Past 10 Years | High-volume commercial SaaS & AI training pipeline |
| **MEGA** | **$499 / mo** | 200,000 req/mo | **Full 40+ Yr Archive** | **Exclusive Direct Live DuckDB SQL Query (`POST /api/v1/query`)** |

---

## 🐍 Python SDK Usage

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/japan-opendata-lab/japan-official-data-megabank.git
cd japan-official-data-megabank
pip install -r requirements.txt
```

### Basic Query Example

```python
from japan_opendata import JapanDataClient

# Initialize client with your RapidAPI Key
client = JapanDataClient(api_key="YOUR_RAPIDAPI_KEY")

# 1. Query Government Procurement
awards = client.procurement(q="AI", min_amount=50_000_000, limit=10)
df_awards = client.to_dataframe(awards)
print(df_awards)

# 2. Query Land Benchmark Valuations
prices = client.land_prices(city="Shinjuku", year=2024, limit=10)
df_prices = client.to_dataframe(prices)
print(df_prices)
```

### MEGA Tier: In-Memory Analytical SQL (`POST /api/v1/query`)

```python
# Execute ad-hoc SQL across multiple Japanese government tables
res = client.query_sql("""
    SELECT 
        p.legal_name,
        p.corporate_number,
        COUNT(*) AS contracts_won,
        SUM(p.capital_amount_jpy) AS total_award_jpy
    FROM procurement p
    WHERE p.capital_amount_jpy > 100000000
    GROUP BY p.legal_name, p.corporate_number
    ORDER BY total_award_jpy DESC
    LIMIT 10
""")
print(res)
```

---

## 📁 Repository Structure

```text
japan-official-data-megabank/
├── README.md               # Documentation and guides
├── LICENSE                 # MIT License
├── requirements.txt        # Minimal dependencies (requests, duckdb, pandas)
├── japan_opendata/         # Ultra-lightweight Python SDK
│   ├── __init__.py
│   └── client.py
└── examples/               # Runnable code walkthroughs
    ├── 01_free_sample_duckdb.py
    ├── 02_rapidapi_quickstart.py
    └── 03_cross_domain_sql.py
```

---

## 🛡️ Data Quality & Compliance

- **Commercial Licensing**: Derived strictly from Government of Japan Open Data (Standard Terms of Use 2.0 / CC BY 4.0).
- **PII Zero Risk**: Sole proprietorship records have been programmatically excluded to ensure full GDPR/APPI compliance for commercial B2B use.
- **Support & Custom Datasets**: Contact `japan.opendata.lab@gmail.com` for bespoke enterprise snapshots or dedicated private database instances.

---

## ⚠️ Disclaimer & Attribution

- **Independent Project**: This project, SDK, and API are developed and maintained independently by **Japan Open Data Lab**.
- **Not Government Affiliated**: This project is **not** endorsed by, operated by, or directly affiliated with the Government of Japan or any public ministry.
- **Source Integrity**: All underlying public domain data is cited with full attribution to original government ministries pursuant to the Government of Japan Standard Terms of Use (Version 2.0).

---

## 📄 License

This repository and the SDK are open-sourced under the [MIT License](LICENSE).
The underlying data is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
