"""
Macroeconomic data.

FRED is used for US macroeconomic indicators.

The system is designed so that missing API data does
not break the entire report.
"""

import os
import requests

from dotenv import load_dotenv


load_dotenv()


FRED_API_KEY = os.getenv(
    "FRED_API_KEY",
    ""
)


FRED_URL = (
    "https://api.stlouisfed.org/"
    "fred/series/observations"
)


FRED_SERIES = {

    # US
    "US CPI": "CPIAUCSL",

    "US Unemployment": "UNRATE",

    "US Fed Funds Rate": "FEDFUNDS",

    "US 10Y Treasury": "DGS10",

    "US 2Y Treasury": "DGS2",

    "US GDP": "GDP",

    "US Real GDP": "GDPC1",

    # Financial conditions
    "US Financial Conditions": "NFCI",
}


def get_fred_series(
    series_id,
    limit=5
):

    if not FRED_API_KEY:

        return None

    params = {

        "series_id": series_id,

        "api_key": FRED_API_KEY,

        "file_type": "json",

        "sort_order": "desc",

        "limit": limit,
    }

    try:

        response = requests.get(
            FRED_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        observations = response.json().get(
            "observations",
            []
        )

        valid = []

        for item in observations:

            if item["value"] != ".":

                valid.append(
                    item
                )

        return valid

    except Exception as e:

        print(
            f"FRED {series_id} failed: {e}"
        )

        return None


def get_macro_snapshot():

    result = {}

    for name, series_id in FRED_SERIES.items():

        print(
            f"  Fetching macro: {name}"
        )

        data = get_fred_series(
            series_id
        )

        result[name] = {
            "series": series_id,
            "observations": data,
        }

    return result