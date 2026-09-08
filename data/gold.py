"""
Commodity data collection.

Global commodity futures:
- Gold: USD / troy ounce
- Silver: USD / troy ounce
- Crude Oil: USD / barrel

Indian bullion:
- Gold 24K: INR / 10 grams
- Silver 999: INR / kilogram

Note:
Indian bullion prices are currently maintained as a separate
reference layer. We will connect an automated Indian bullion
source in a later step.
"""

import yfinance as yf


GLOBAL_COMMODITIES = {
    "Gold Futures": "GC=F",
    "Silver Futures": "SI=F",
    "Crude Oil": "CL=F",
}


# Reference values for the latest Indian market session.
# These are NOT used for automated trading decisions.
INDIAN_BULLION_REFERENCE = {
    "Gold 24K": {
        "price": 155270,
        "unit": "INR / 10g",
        "location": "Bengaluru",
    },
    "Silver 999": {
        "price": 240350,
        "unit": "INR / kg",
        "location": "Bengaluru",
    },
}


def get_commodity_price(symbol):

    try:

        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period="5d",
            interval="1d"
        )

        if history.empty:
            return None

        latest = history.iloc[-1]

        price = float(latest["Close"])

        previous = None

        if len(history) >= 2:
            previous = float(history.iloc[-2]["Close"])

        change_percent = None

        if previous:
            change_percent = (
                (price - previous) / previous
            ) * 100

        return {
            "price": price,
            "change_percent": change_percent,
            "date": history.index[-1].strftime("%Y-%m-%d"),
        }

    except Exception as e:

        print(
            f"Error fetching commodity {symbol}: {e}"
        )

        return None


def get_commodity_snapshot():

    result = {
        "global": {},
        "india": INDIAN_BULLION_REFERENCE,
    }

    for name, symbol in GLOBAL_COMMODITIES.items():

        print(f"  Fetching {name}...")

        result["global"][name] = get_commodity_price(
            symbol
        )

    return result