"""
NSE data collector.

Collects:
- Nifty 50
- Midcap
- Smallcap
- VIX
- Sector indices
- Market breadth
- Valuation information
"""

import requests


NSE_URL = "https://www.nseindia.com/api/allIndices"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/146.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}


SECTOR_KEYWORDS = [
    "IT",
    "BANK",
    "FINANCIAL",
    "PHARMA",
    "HEALTHCARE",
    "AUTO",
    "FMCG",
    "METAL",
    "REALTY",
    "OIL",
    "GAS",
    "ENERGY",
    "MEDIA",
    "TELECOM",
    "CONSUMER",
    "CAPITAL GOODS",
    "CHEMICAL",
    "INFRA",
    "DEFENCE",
]


def create_session():

    session = requests.Session()

    session.headers.update(
        HEADERS
    )

    try:

        session.get(
            "https://www.nseindia.com/",
            timeout=10
        )

    except Exception as e:

        print(
            f"NSE homepage request failed: {e}"
        )

    return session


def get_all_indices():

    session = create_session()

    try:

        response = session.get(
            NSE_URL,
            timeout=15
        )

        response.raise_for_status()

        return response.json().get(
            "data",
            []
        )

    except Exception as e:

        print(
            f"NSE index API failed: {e}"
        )

        return []


def normalize_index(item):

    return {
        "name": item.get("index"),
        "price": item.get("last"),
        "change": item.get("variation"),
        "change_percent": item.get(
            "percentChange"
        ),
        "open": item.get("open"),
        "high": item.get("high"),
        "low": item.get("low"),
        "previous_close": item.get(
            "previousClose"
        ),
        "year_high": item.get(
            "yearHigh"
        ),
        "year_low": item.get(
            "yearLow"
        ),
        "pe": item.get("pe"),
        "pb": item.get("pb"),
        "dividend_yield": item.get(
            "dy"
        ),
        "advances": item.get(
            "advances"
        ),
        "declines": item.get(
            "declines"
        ),
        "unchanged": item.get(
            "unchanged"
        ),
    }


def get_indian_market():

    raw = get_all_indices()

    result = {
        "indices": {},
        "sectors": {},
    }

    for item in raw:

        index = normalize_index(
            item
        )

        name = index["name"]

        if not name:
            continue

        # Main indices
        important = [
            "NIFTY 50",
            "NIFTY MIDCAP 100",
            "NIFTY SMALLCAP 100",
            "INDIA VIX",
            "NIFTY NEXT 50",
        ]

        if name in important:

            result["indices"][name] = index

        # Sector detection
        upper_name = name.upper()

        if any(
            keyword in upper_name
            for keyword in SECTOR_KEYWORDS
        ):

            result["sectors"][name] = index

    return result