"""
Sector classification and analysis.

Separates genuine sector indices from:
- factor indices
- strategy indices
- thematic indices
- volatility indices
"""

SECTOR_MAP = {
    "BANK": "Banking",
    "FINANCIAL SERVICES": "Financial Services",
    "IT": "Information Technology",
    "PHARMA": "Pharma",
    "HEALTHCARE": "Healthcare",
    "AUTO": "Automobile",
    "FMCG": "FMCG",
    "METAL": "Metals",
    "REALTY": "Real Estate",
    "OIL & GAS": "Oil & Gas",
    "ENERGY": "Energy",
    "MEDIA": "Media",
    "TELECOM": "Telecom",
    "CONSUMER": "Consumer",
    "CAPITAL GOODS": "Capital Goods",
    "CHEMICAL": "Chemicals",
    "DEFENCE": "Defence",
    "INFRA": "Infrastructure",
}


EXCLUDED_KEYWORDS = [
    "ALPHA",
    "QUALITY",
    "LOW-VOLATILITY",
    "MOMENTUM",
    "VALUE",
    "DIVIDEND",
    "MULTIFACTOR",
    "STRATEGY",
    "VOLATILITY",
    "EQUAL WEIGHT",
]


def classify_sector(name):

    upper = name.upper()

    # Don't treat factor/strategy indices as sectors
    for keyword in EXCLUDED_KEYWORDS:

        if keyword in upper:

            return None

    for keyword, sector_name in SECTOR_MAP.items():

        if keyword in upper:

            return sector_name

    return None


def analyze_sectors(sectors):

    classified = []

    for name, data in sectors.items():

        change = data.get(
            "change_percent"
        )

        if change is None:
            continue

        sector = classify_sector(name)

        if sector is None:
            continue

        classified.append({
            "index": name,
            "sector": sector,
            "change": float(change),
        })

    classified.sort(
        key=lambda x: x["change"],
        reverse=True
    )

    return {

        "leaders": classified[:5],

        "laggards": (
            classified[-5:]
            if len(classified) >= 5
            else classified
        ),

        "all": classified,

    }