"""
Institutional flow analysis.
"""


def analyze_institutional_flows(
    fii_dii
):

    result = {

        "fii_net": None,

        "dii_net": None,

        "fii_direction": "UNKNOWN",

        "dii_direction": "UNKNOWN",

    }

    for item in fii_dii:

        category = item.get(
            "category"
        )

        try:

            net = float(
                item.get(
                    "netValue",
                    0
                )
            )

        except:

            continue

        if category == "FII/FPI":

            result["fii_net"] = net

            if net > 0:

                result[
                    "fii_direction"
                ] = "BUYING"

            elif net < 0:

                result[
                    "fii_direction"
                ] = "SELLING"

        elif category == "DII":

            result["dii_net"] = net

            if net > 0:

                result[
                    "dii_direction"
                ] = "BUYING"

            elif net < 0:

                result[
                    "dii_direction"
                ] = "SELLING"

    return result