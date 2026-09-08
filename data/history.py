"""
Historical market data engine.

Uses Yahoo Finance historical data to calculate:

- 1D performance
- 5D performance
- 1M performance
- 3M performance
- 6M performance
- 1Y performance
- 52-week high / low
- Distance from 52-week high
- Distance from 52-week low
- Maximum drawdown
- Annualized volatility

This module is for analysis, not prediction.
"""

import yfinance as yf
import pandas as pd


# =========================================================
# HISTORICAL TICKERS
# =========================================================

HISTORICAL_TICKERS = {

    "Nifty 50": "^NSEI",

    "Sensex": "^BSESN",

    "India VIX": "^INDIAVIX",

    "S&P 500": "^GSPC",

    "Nasdaq": "^IXIC",

    "Dow Jones": "^DJI",
}


# =========================================================
# SECTOR TICKERS
# =========================================================

SECTOR_TICKERS = {

    "Nifty IT": "^CNXIT",

    "Nifty Bank": "^NSEBANK",

    "Nifty Pharma": "^CNXPHARMA",

    "Nifty Auto": "^CNXAUTO",

    "Nifty FMCG": "^CNXFMCG",

    "Nifty Metal": "^CNXMETAL",

    "Nifty Realty": "^CNXREALTY",

    "Nifty Energy": "^CNXENERGY",

    "Nifty PSU Bank": "^CNXPSUBANK",

    # Yahoo currently does not reliably provide this symbol.
    # We will replace it with NSE historical data later.
    #
    # "Nifty Private Bank": "^NIFTYPVTBANK",
}


# =========================================================
# DOWNLOAD HISTORY
# =========================================================

def get_history(
    symbol,
    period="2y"
):

    """
    Download historical daily data.

    Two years are downloaded so that 1Y calculations
    have sufficient trading-day history.
    """

    try:

        data = yf.download(
            symbol,
            period=period,
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

        if data is None or data.empty:

            return None

        # yfinance can return MultiIndex columns.
        if isinstance(
            data.columns,
            pd.MultiIndex
        ):

            data.columns = (
                data.columns
                .get_level_values(0)
            )

        if "Close" not in data.columns:

            return None

        # Convert Close to numeric.
        data["Close"] = pd.to_numeric(
            data["Close"],
            errors="coerce"
        )

        # Remove invalid rows.
        data = data.dropna(
            subset=["Close"]
        )

        if data.empty:

            return None

        return data

    except Exception as e:

        print(
            f"Historical data error "
            f"for {symbol}: {e}"
        )

        return None


# =========================================================
# CLEAN CLOSE SERIES
# =========================================================

def get_close_series(data):

    """
    Return a clean Close price series.
    """

    if data is None or data.empty:

        return None

    if "Close" not in data.columns:

        return None

    close = pd.to_numeric(
        data["Close"],
        errors="coerce"
    )

    close = close.dropna()

    if close.empty:

        return None

    return close


# =========================================================
# PERCENTAGE CHANGE
# =========================================================

def percentage_change(
    data,
    periods
):

    """
    Calculate percentage return over
    a number of trading sessions.
    """

    close = get_close_series(
        data
    )

    if close is None:

        return None

    if len(close) <= periods:

        return None

    current = float(
        close.iloc[-1]
    )

    previous = float(
        close.iloc[-periods - 1]
    )

    if previous == 0:

        return None

    result = (
        (current - previous)
        / previous
    ) * 100

    if pd.isna(result):

        return None

    return float(result)


# =========================================================
# 52-WEEK METRICS
# =========================================================

def calculate_52_week_metrics(
    data
):

    if data is None or data.empty:

        return {}

    close = get_close_series(
        data
    )

    if close is None:

        return {}

    # Last approximately 252 trading sessions.
    close_52w = close.tail(252)

    if close_52w.empty:

        return {}

    current = float(
        close.iloc[-1]
    )

    high_52w = float(
        close_52w.max()
    )

    low_52w = float(
        close_52w.min()
    )

    if high_52w == 0:

        distance_from_high = None

    else:

        distance_from_high = (
            (current - high_52w)
            / high_52w
        ) * 100

    if low_52w == 0:

        distance_from_low = None

    else:

        distance_from_low = (
            (current - low_52w)
            / low_52w
        ) * 100

    return {

        "current": current,

        "52w_high": high_52w,

        "52w_low": low_52w,

        "distance_from_52w_high":
            distance_from_high,

        "distance_from_52w_low":
            distance_from_low,
    }


# =========================================================
# MAXIMUM DRAWDOWN
# =========================================================

def calculate_drawdown(
    data
):

    if data is None or data.empty:

        return None

    close = get_close_series(
        data
    )

    if close is None:

        return None

    running_high = (
        close.cummax()
    )

    drawdown = (
        (close - running_high)
        / running_high
    ) * 100

    drawdown = drawdown.dropna()

    if drawdown.empty:

        return None

    result = float(
        drawdown.min()
    )

    if pd.isna(result):

        return None

    return result


# =========================================================
# ANNUALIZED VOLATILITY
# =========================================================

def calculate_volatility(
    data
):

    if data is None or data.empty:

        return None

    close = get_close_series(
        data
    )

    if close is None:

        return None

    returns = (
        close
        .pct_change(
            fill_method=None
        )
        .dropna()
    )

    if len(returns) < 2:

        return None

    volatility = (
        returns.std()
        * (252 ** 0.5)
        * 100
    )

    if pd.isna(volatility):

        return None

    return float(
        volatility
    )


# =========================================================
# ANALYZE ONE INSTRUMENT
# =========================================================

def analyze_history(
    symbol
):

    data = get_history(
        symbol
    )

    if data is None:

        return {

            "symbol": symbol,

            "status": "UNAVAILABLE",
        }

    metrics = (
        calculate_52_week_metrics(
            data
        )
    )

    metrics.update({

        "symbol": symbol,

        "status": "OK",

        # Approximately 1 trading session
        "1D": percentage_change(
            data,
            1
        ),

        # Approximately 1 trading week
        "5D": percentage_change(
            data,
            5
        ),

        # Approximately 1 trading month
        "1M": percentage_change(
            data,
            21
        ),

        # Approximately 1 quarter
        "3M": percentage_change(
            data,
            63
        ),

        # Approximately 6 months
        "6M": percentage_change(
            data,
            126
        ),

        # Approximately 1 year
        "1Y": percentage_change(
            data,
            252
        ),

        "maximum_drawdown":
            calculate_drawdown(
                data
            ),

        "annualized_volatility":
            calculate_volatility(
                data
            ),
    })

    return metrics


# =========================================================
# HISTORICAL MARKET SNAPSHOT
# =========================================================

def get_historical_snapshot():

    result = {}

    for name, symbol in HISTORICAL_TICKERS.items():

        print(
            f"  Historical data: {name}..."
        )

        result[name] = (
            analyze_history(
                symbol
            )
        )

    return result


# =========================================================
# HISTORICAL SECTOR SNAPSHOT
# =========================================================

def get_sector_history():

    result = {}

    for name, symbol in SECTOR_TICKERS.items():

        print(
            f"  Sector history: {name}..."
        )

        data = analyze_history(
            symbol
        )

        # Store the human-readable name
        # explicitly. This makes the data
        # contract consistent for analysis.
        data["name"] = name

        result[name] = data

    return result   