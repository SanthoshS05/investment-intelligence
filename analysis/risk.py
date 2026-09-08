"""
Market risk analysis.
"""


def analyze_risk(
    india_vix=None,
    crude_change=None,
    usd_inr_change=None,
    us10y_change=None,
):

    risks = []

    score = 0

    if india_vix is not None:

        if india_vix > 20:

            score += 3

            risks.append(
                "India VIX is elevated."
            )

        elif india_vix > 15:

            score += 1

            risks.append(
                "India VIX is moderately elevated."
            )

    if crude_change is not None:

        if crude_change > 5:

            score += 2

            risks.append(
                "Crude oil is rising sharply."
            )

    if usd_inr_change is not None:

        if usd_inr_change > 1:

            score += 2

            risks.append(
                "Rupee is weakening significantly."
            )

    if us10y_change is not None:

        if us10y_change > 3:

            score += 2

            risks.append(
                "US Treasury yields are rising."
            )

    if score >= 6:

        level = "HIGH"

    elif score >= 3:

        level = "MODERATE"

    else:

        level = "LOW"

    return {
        "score": score,
        "level": level,
        "risks": risks,
    }