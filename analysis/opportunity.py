"""
Investment opportunity analysis.

This module does NOT attempt to predict market bottoms.

It evaluates multiple conditions together.
"""


def calculate_accumulation_score(
    market_change=None,
    vix_change=None,
    valuation_status="UNKNOWN",
    crude_change=None
):

    score = 50

    reasons = []

    # Market correction
    if market_change is not None:

        if market_change < -10:

            score += 15

            reasons.append(
                "Market has experienced a significant correction."
            )

        elif market_change < -5:

            score += 8

            reasons.append(
                "Market has experienced a moderate correction."
            )

    # Volatility
    if vix_change is not None:

        if vix_change > 20:

            score -= 5

            reasons.append(
                "Volatility is elevated."
            )

    # Valuation
    if valuation_status == "ATTRACTIVE":

        score += 15

        reasons.append(
            "Valuation appears attractive."
        )

    elif valuation_status == "EXPENSIVE":

        score -= 10

        reasons.append(
            "Valuation appears elevated."
        )

    # Crude
    if crude_change is not None:

        if crude_change > 10:

            score -= 5

            reasons.append(
                "Sharp crude increase is a macro risk."
            )

    score = max(0, min(score, 100))

    if score >= 70:

        status = "ATTRACTIVE ACCUMULATION CONDITIONS"

    elif score >= 45:

        status = "NORMAL / WATCH"

    else:

        status = "HIGH UNCERTAINTY"

    return {
        "score": score,
        "status": status,
        "reasons": reasons,
    }