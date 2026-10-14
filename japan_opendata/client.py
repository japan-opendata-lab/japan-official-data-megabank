"""Japan Official Data Megabank API Client (Python SDK).

Seamless access to US-Standard normalized Japanese public open data.
"""

from typing import Any, Dict, List, Optional
import requests
import pandas as pd


class JapanDataClient:
    """Client for Japan Official Data Megabank API on RapidAPI."""

    DEFAULT_HOST = "japan-demographics-api.onrender.com"
    RAPIDAPI_HOST = "japan-data-megabank-api.p.rapidapi.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        rapidapi_host: Optional[str] = None,
    ):
        """Initialize JapanDataClient.

        Args:
            api_key: RapidAPI key.
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
    # Core Data Endpoints
    # ---------------------------------------------------------

    def procurement(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        supplier: Optional[str] = None,
        corporate_number: Optional[str] = None,
        min_amount: Optional[int] = None,
        max_amount: Optional[int] = None,
        year: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Japanese Central Government Procurement Awards (GEPS 2020-2026)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/procurement", params=params)

    def corporate_invoices(
        self,
        q: Optional[str] = None,
        corporate_number: Optional[str] = None,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Nationwide Corporate Registry & Invoice Tax Payers (5M+ entities)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/corporate-invoices", params=params)

    def land_prices(
        self,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        municipality_code: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query MLIT Official Land Valuation Benchmark (1983-2026 44-year archive)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/land-prices", params=params)

    def medical_facilities(
        self,
        prefecture: Optional[str] = None,
        city: Optional[str] = None,
        specialty: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Hospitals, Clinics, and Pharmacies (MHLW Medical Net 220k+)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/medical", params=params)

    def nursing_care(
        self,
        prefecture: Optional[str] = None,
        service_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Senior Care & Welfare Service Providers (MHLW 250k+)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/nursing-care", params=params)

    def ghg_emissions(
        self,
        corporate_name: Optional[str] = None,
        prefecture: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query Industrial GHG Carbon Emissions Reports (MOE Mandatory Disclosures)."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/ghg-emissions", params=params)

    def demographics(
        self,
        municipality_code: Optional[str] = None,
        prefecture: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Query All 1,741 Municipalities Demographics & Per Capita Taxable Incomes."""
        params = {k: v for k, v in locals().items() if k not in ("self", "params") and v is not None}
        return self._get("/api/v1/demographics", params=params)

    # ---------------------------------------------------------
    # Analytical In-Memory SQL Query (MEGA Tier Exclusive)
    # ---------------------------------------------------------

    def query_sql(self, sql: str) -> Dict[str, Any]:
        """Execute in-memory analytical SQL with multi-table cross-joins (MEGA Tier).

        Args:
            sql: Read-only SELECT SQL query string.

        Returns:
            JSON response containing query results.
        """
        return self._post("/api/v1/query", json_data={"sql": sql})

    # ---------------------------------------------------------
    # Helper Utilities
    # ---------------------------------------------------------

    @staticmethod
    def to_dataframe(api_response: Dict[str, Any]) -> pd.DataFrame:
        """Convert API response data to a clean Pandas DataFrame."""
        data = api_response.get("data", [])
        return pd.DataFrame(data)
