"""
Valuation analysis.

Future versions will calculate:
- Nifty P/E
- P/B
- earnings yield
- historical percentile
- market cap/GDP
"""


def valuation_status(pe_ratio):

    if pe_ratio is None:

        return {
            "status": "UNKNOWN",
            "message": "Valuation data unavailable."
        }

    if pe_ratio < 18:

        return {
            "status": "ATTRACTIVE",
            "message": "Market valuation appears relatively attractive."
        }

    elif pe_ratio < 22:

        return {
            "status": "NORMAL",
            "message": "Market valuation appears within a normal range."
        }

    elif pe_ratio < 25:

        return {
            "status": "EXPENSIVE",
            "message": "Market valuation appears elevated."
        }

    else:

        return {
            "status": "VERY EXPENSIVE",
            "message": "Market valuation appears significantly elevated."
        }


def analyze_valuation(pe_ratio=None):

    return valuation_status(pe_ratio)