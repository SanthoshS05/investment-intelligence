"""
Market breadth analysis.
"""


def analyze_breadth(
    advances,
    declines,
    unchanged,
):

    total = (
        advances
        + declines
        + unchanged
    )

    if total == 0:

        return {
            "ratio": None,
            "status": "UNKNOWN",
        }

    advance_ratio = (
        advances / total
    ) * 100

    decline_ratio = (
        declines / total
    ) * 100

    if advance_ratio >= 65:

        status = "VERY STRONG"

    elif advance_ratio >= 55:

        status = "POSITIVE"

    elif decline_ratio >= 65:

        status = "VERY WEAK"

    elif decline_ratio >= 55:

        status = "NEGATIVE"

    else:

        status = "MIXED"

    return {

        "advance_percent":
            advance_ratio,

        "decline_percent":
            decline_ratio,

        "status":
            status,
    }