"""
Market intelligence engine.

Converts collected market and sector data into
human-readable observations.
"""


def analyze_market(
    indian_market,
    global_market,
    sector_analysis,
):

    observations = []

    # ---------------------------------------
    # NIFTY
    # ---------------------------------------

    indices = indian_market.get(
        "indices",
        {}
    )

    nifty = indices.get(
        "NIFTY 50"
    )

    if nifty:

        change = nifty.get(
            "change_percent"
        )

        if change is not None:

            if change > 1:

                observations.append(
                    "Nifty is showing strong positive momentum."
                )

            elif change < -1:

                observations.append(
                    "Nifty is under significant selling pressure."
                )

            else:

                observations.append(
                    "Nifty is relatively stable in the latest session."
                )

    # ---------------------------------------
    # MIDCAP
    # ---------------------------------------

    midcap = indices.get(
        "NIFTY MIDCAP 100"
    )

    if midcap:

        change = midcap.get(
            "change_percent"
        )

        if change is not None:

            observations.append(
                f"Midcap 100 moved {change:.2f}%."
            )

    # ---------------------------------------
    # SMALLCAP
    # ---------------------------------------

    smallcap = indices.get(
        "NIFTY SMALLCAP 100"
    )

    if smallcap:

        change = smallcap.get(
            "change_percent"
        )

        if change is not None:

            observations.append(
                f"Smallcap 100 moved {change:.2f}%."
            )

    # ---------------------------------------
    # SECTORS
    # ---------------------------------------

    leaders = sector_analysis.get(
        "leaders",
        []
    )

    laggards = sector_analysis.get(
        "laggards",
        []
    )

    # Safely extract sector names
    if leaders:

        leader_names = []

        for sector in leaders[:3]:

            name = sector.get(
                "name",
                sector.get(
                    "sector",
                    "Unknown Sector"
                )
            )

            leader_names.append(name)

        names = ", ".join(
            leader_names
        )

        observations.append(
            f"Leading sectors: {names}."
        )

    # Safely extract laggard names
    if laggards:

        laggard_names = []

        for sector in laggards[:3]:

            name = sector.get(
                "name",
                sector.get(
                    "sector",
                    "Unknown Sector"
                )
            )

            laggard_names.append(name)

        names = ", ".join(
            laggard_names
        )

        observations.append(
            f"Weakest sectors: {names}."
        )

    # ---------------------------------------
    # GLOBAL
    # ---------------------------------------

    sp500 = global_market.get(
        "S&P 500"
    )

    if sp500:

        change = sp500.get(
            "change_percent"
        )

        if change is not None:

            observations.append(
                f"S&P 500 moved {change:.2f}%."
            )

    return {
        "observations": observations
    }