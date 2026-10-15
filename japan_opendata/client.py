"""Japan Official Data Megabank API Client (Python SDK).

Seamless access to US-Standard normalized Japanese public open data.
"""

from typing import Any, Dict, Optional
import requests
import pandas as pd


class JapanDataClient:
    """Client for Japan Official Data Megabank API on RapidAPI."""

    RAPIDAPI_HOST = "japan-official-data-megabank-api-us-standard-normalized.p.rapidapi.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        rapidapi_host: Optional[str] = None,
    ):
        """Initialize JapanDataClient.

        Args:
            api_key: RapidAPI key (or direct backend API key).
            base_url: Override base URL (e.g., custom proxy or enterprise gateway).
            rapidapi_host: Override RapidAPI host header.
        """
        self.api_key = api_key
        self.rapidapi_host = rapidapi_host or self.RAPIDAPI_HOST
        self.base_url = (base_url or f"https://{self.rapidapi_host}").rstrip("/")
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "JapanOpenDataSDK/1.0",
        }
        if self.api_key:
            headers["X-RapidAPI-Key"] = self.api_key
            headers["X-RapidAPI-Host"] = self.rapidapi_host
        return headers

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        resp = self.session.get(url, headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        resp = self.session.post(url, headers=self._headers(), json=json_data, timeout=45)
        resp.raise_for_status()
        return resp.json()

    # ---------------------------------------------------------
    # 00. System Health & Catalog
    # ---------------------------------------------------------

    def get_health_status(self) -> Dict[str, Any]:
        """Check API liveness and mounted datasets (no API key required)."""
        return self._get("/health")

    def catalog(
        self,
        q: Optional[str] = None,
        format: str = "json",
    ) -> Dict[str, Any]:
        """Get public catalog of all 162 normalized master datasets."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/catalog/", params=params)

    # ---------------------------------------------------------
    # Core Data Endpoints (RapidAPI Groups 01 - 08)
    # ---------------------------------------------------------

    def procurement(
        self,
        q: Optional[str] = None,
        supplier: Optional[str] = None,
        corporate_number: Optional[str] = None,
        year: Optional[int] = None,
        min_amount: Optional[float] = None,
        municipality_code: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        category: Optional[str] = None,
        max_amount: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Query Japanese Central Government Procurement Awards (GEPS 2020-2026)."""
        if category and not q:
            q = category
        params = {
            "q": q,
            "supplier": supplier,
            "corporate_number": corporate_number,
            "year": year,
            "min_amount": min_amount,
            "municipality_code": municipality_code,
            "cursor": cursor,
            "limit": limit,
            "offset": offset,
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        return self._get("/api/v1/procurement/", params=clean_params)

    def corporate_invoices(
        self,
        q: Optional[str] = None,
        corporate_number: Optional[str] = None,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        municipality_code: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Nationwide Corporate Registry & Qualified Invoice Issuers."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/corporate-invoices/", params=params)

    def medical_facilities(
        self,
        q: Optional[str] = None,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        facility_type: Optional[str] = None,
        min_beds: Optional[int] = None,
        municipality_code: Optional[str] = None,
        corporate_number: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        specialty: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Query Hospitals, Clinics, and Pharmacies (MHLW Medical Net)."""
        if specialty and not q:
            q = specialty
        params = {
            "q": q,
            "prefecture": prefecture,
            "city": city,
            "facility_type": facility_type,
            "min_beds": min_beds,
            "municipality_code": municipality_code,
            "corporate_number": corporate_number,
            "limit": limit,
            "offset": offset,
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        return self._get("/api/v1/medical/", params=clean_params)

    def nursing_care(
        self,
        q: Optional[str] = None,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        service_type: Optional[str] = None,
        min_capacity: Optional[int] = None,
        municipality_code: Optional[str] = None,
        corporate_number: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Senior Care & Welfare Service Providers (MHLW)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/nursing-care/", params=params)

    def land_prices(
        self,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        municipality_code: Optional[str] = None,
        year: Optional[int] = None,
        country_code: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query MLIT Official Land Valuation & Real Estate Benchmark (44-year archive)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/real-estate/", params=params)

    def land_prices_official(
        self,
        q: Optional[str] = None,
        prefecture: Optional[str] = None,
        station: Optional[str] = None,
        min_price_jpy: Optional[float] = None,
        municipality_code: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query MLIT Official Land Price Benchmark Points (with station & coordinates)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/land-prices-official/", params=params)

    def ghg_emissions(
        self,
        q: Optional[str] = None,
        fiscal_year: Optional[int] = None,
        min_emissions_ton: Optional[float] = None,
        corporate_number: Optional[str] = None,
        municipality_code: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        corporate_name: Optional[str] = None,
        prefecture: Optional[str] = None,
        year: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query Corporate GHG Carbon Emissions Reports (MOE Mandatory Disclosures)."""
        if corporate_name and not q:
            q = corporate_name
        elif prefecture and not q:
            q = prefecture
        if year is not None and fiscal_year is None:
            fiscal_year = year
        params = {
            "q": q,
            "fiscal_year": fiscal_year,
            "min_emissions_ton": min_emissions_ton,
            "corporate_number": corporate_number,
            "municipality_code": municipality_code,
            "limit": limit,
            "offset": offset,
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        return self._get("/api/v1/corporate-ghg/", params=clean_params)

    def industrial_emissions(
        self,
        q: Optional[str] = None,
        prefecture: Optional[str] = None,
        industry: Optional[str] = None,
        min_co2_ton: Optional[int] = None,
        sales_category: Optional[str] = None,
        chemical: Optional[str] = None,
        municipality_code: Optional[str] = None,
        corporate_number: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Plant-level Industrial GHG Emissions & PRTR Chemical Releases."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/industrial-emissions/", params=params)

    def traffic_accidents(
        self,
        q: Optional[str] = None,
        prefecture: Optional[str] = None,
        accident_type: Optional[str] = None,
        danger_rank: Optional[str] = None,
        min_accidents: Optional[int] = None,
        fatal_only: Optional[bool] = None,
        municipality_code: Optional[str] = None,
        corporate_number: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query NPA Traffic Accident Blackspots & Road Safety Statistics."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/traffic-safety/", params=params)

    def demographics(
        self,
        municipality: Optional[str] = None,
        prefecture: Optional[str] = None,
        municipality_code: Optional[str] = None,
        corporate_number: Optional[str] = None,
        country_code: Optional[str] = None,
        year: Optional[int] = None,
        min_income: Optional[float] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query All 1,741 Municipalities Demographics & Per Capita Taxable Incomes."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/demographics/", params=params)

    # ---------------------------------------------------------
    # 09. Cross-Dataset SQL Analytics (MEGA Tier Exclusive)
    # ---------------------------------------------------------

    def query_sql(self, sql: str) -> Dict[str, Any]:
        """Execute in-memory analytical SQL with multi-table cross-joins (MEGA Tier).

        Args:
            sql: Read-only SELECT SQL query string.

        Returns:
            JSON response containing query results.
        """
        return self._post("/api/v1/query/", json_data={"sql": sql})

    def list_sql_tables(self) -> Dict[str, Any]:
        """List all mounted DuckDB tables (views) and columns available for SQL query."""
        return self._get("/api/v1/query/tables")

    # ---------------------------------------------------------
    # Helper Utilities
    # ---------------------------------------------------------

    @staticmethod
    def to_dataframe(api_response: Dict[str, Any]) -> pd.DataFrame:
        """Convert API response data to a clean Pandas DataFrame."""
        if isinstance(api_response, list):
            return pd.DataFrame(api_response)
        data = api_response.get("data", api_response.get("results", api_response.get("rows", [])))
        return pd.DataFrame(data)
