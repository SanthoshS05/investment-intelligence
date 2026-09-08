"""
Market data collection.

Sources:
- Yahoo Finance for global/liquid market instruments
- NSE module for Indian indices
"""

import yfinance as yf


YAHOO_TICKERS = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "USD/INR": "USDINR=X",

    # US Treasury 10Y yield
    "US 10Y Yield": "^TNX",

    # VIX
    "US VIX": "^VIX",

    # Commodities
    "Gold Futures": "GC=F",
    "Silver Futures": "SI=F",
    "Crude Oil": "CL=F",
}


def get_yahoo_data(symbol):

    try:

        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period="10d",
            interval="1d"
        )

        if history.empty:
            return None

        latest = history.iloc[-1]

        price = float(latest["Close"])

        previous = None

        if len(history) >= 2:

            previous = float(
                history.iloc[-2]["Close"]
            )

        change_percent = None

        if previous:

            change_percent = (
                (price - previous)
                / previous
            ) * 100

        return {
            "price": price,
            "change_percent": change_percent,
            "date": history.index[-1].strftime(
                "%Y-%m-%d"
            ),
            "source": "Yahoo Finance",
        }

    except Exception as e:

        print(
            f"Error fetching {symbol}: {e}"
        )

        return None


def get_global_market():

    result = {}

    for name, symbol in YAHOO_TICKERS.items():

        print(
            f"  Fetching {name}..."
        )

        result[name] = get_yahoo_data(
            symbol
        )

    return result