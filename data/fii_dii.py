"""
FII / DII activity collector.
"""

import requests


URL = (
    "https://www.nseindia.com/api/"
    "fiidiiTradeReact"
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/146.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/",
}


def get_fii_dii():

    session = requests.Session()

    session.headers.update(
        HEADERS
    )

    try:

        session.get(
            "https://www.nseindia.com/",
            timeout=10
        )

        response = session.get(
            URL,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print(
            f"FII/DII data unavailable: {e}"
        )

        return []