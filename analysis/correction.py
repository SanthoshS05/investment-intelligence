"""
Correction and accumulation analysis.

This module identifies market corrections and recovery
conditions.

It does NOT attempt to predict the bottom.
"""


def analyze_correction(
    one_month,
    three_month,
    distance_from_high,
    volatility,
):

    score = 50

    reasons = []

    # --------------------------------
    # Correction depth
    # --------------------------------

    if one_month is not None:

        if one_month <= -10:

            score += 20

            reasons.append(
                "Market is down more than 10% over one month."
            )

        elif one_month <= -5:

            score += 10

            reasons.append(
                "Market is experiencing a meaningful correction."
            )

        elif one_month < 0:

            score += 5

            reasons.append(
                "Market is moderately below its recent level."
            )

    # --------------------------------
    # Distance from 52W high
    # --------------------------------

    if distance_from_high is not None:

        if distance_from_high <= -15:

            score += 15

            reasons.append(
                "Market is significantly below its 52-week high."
            )

        elif distance_from_high <= -10:

            score += 10

            reasons.append(
                "Market is more than 10% below its 52-week high."
            )

    # --------------------------------
    # Volatility
    # --------------------------------

    if volatility is not None:

        if volatility > 30:

            score -= 10

            reasons.append(
                "Volatility is very high."
            )

        elif volatility > 20:

            score -= 5

            reasons.append(
                "Volatility is elevated."
            )

    score = max(
        0,
        min(score, 100)
    )

    if score >= 75:

        status = (
            "DEEP CORRECTION — "
            "STUDY ACCUMULATION CONDITIONS"
        )

    elif score >= 60:

        status = (
            "MEANINGFUL CORRECTION"
        )

    elif score >= 45:

        status = (
            "NORMAL CORRECTION / WATCH"
        )

    else:

        status = (
            "NO SIGNIFICANT CORRECTION"
        )

    return {

        "score": score,

        "status": status,

        "reasons": reasons,

    }