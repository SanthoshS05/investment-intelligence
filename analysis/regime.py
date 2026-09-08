"""
Market regime detection.

This is NOT a prediction engine.

It describes the current environment.
"""


def determine_regime(
    nifty_change,
    breadth_status,
    fii_net,
    vix_change,
):

    bullish_points = 0
    bearish_points = 0

    # Nifty
    if nifty_change is not None:

        if nifty_change > 0:
            bullish_points += 1

        elif nifty_change < 0:
            bearish_points += 1

    # Breadth
    if breadth_status in [
        "POSITIVE",
        "VERY STRONG",
    ]:

        bullish_points += 1

    elif breadth_status in [
        "NEGATIVE",
        "VERY WEAK",
    ]:

        bearish_points += 1

    # FII
    if fii_net is not None:

        if fii_net > 0:
            bullish_points += 1

        elif fii_net < 0:
            bearish_points += 1

    # VIX
    if vix_change is not None:

        if vix_change > 10:
            bearish_points += 1

        elif vix_change < -10:
            bullish_points += 1

    if (
        bullish_points
        >= bearish_points + 2
    ):

        return "RISK-ON"

    if (
        bearish_points
        >= bullish_points + 2
    ):

        return "RISK-OFF"

    return "MIXED / TRANSITION"