"""
Trend and momentum analysis.
"""


def classify_trend(
    one_day,
    five_day,
    one_month,
    three_month,
):

    values = [
        one_day,
        five_day,
        one_month,
        three_month,
    ]

    if any(
        value is None
        for value in values
    ):

        return "INSUFFICIENT DATA"

    if all(
        value > 0
        for value in values
    ):

        return "STRONG UP TREND"

    if all(
        value < 0
        for value in values
    ):

        return "STRONG DOWN TREND"

    if (
        one_day > 0
        and five_day > 0
        and one_month < 0
    ):

        return "RECOVERY / BOUNCE"

    if (
        one_day < 0
        and five_day < 0
        and one_month > 0
    ):

        return "SHORT-TERM WEAKNESS"

    return "MIXED"