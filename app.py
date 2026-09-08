"""
Investment Intelligence
Main application and daily report composer.

Generates:
    reports/daily_report.txt
    docs/index.html

"""

from datetime import datetime
from pathlib import Path
import math

from web.dashboard import generate_dashboard

from data.market import (
    get_global_market
)

from data.nse import (
    get_indian_market
)

from data.fii_dii import (
    get_fii_dii
)

from data.macro import (
    get_macro_snapshot
)

from data.news import (
    get_news
)

from data.history import (
    get_historical_snapshot,
    get_sector_history,
)

from analysis.sectors import (
    analyze_sectors
)

from analysis.market import (
    analyze_market
)


# =========================================================
# REPORT CONFIGURATION
# =========================================================

REPORT_DIR = Path("reports")

REPORT_FILE = (
    REPORT_DIR /
    "daily_report.txt"
)


# =========================================================
# FORMATTING HELPERS
# =========================================================

def clean_value(value):

    """
    Convert invalid numeric values to None.
    """

    if value is None:
        return None

    try:

        value = float(value)

        if math.isnan(value):
            return None

        if math.isinf(value):
            return None

        return value

    except (
        TypeError,
        ValueError
    ):

        return None


def format_number(value):

    value = clean_value(value)

    if value is None:
        return "N/A"

    return f"{value:,.2f}"


def format_pct(value):

    value = clean_value(value)

    if value is None:
        return "N/A"

    return f"{value:+.2f}%"


def format_plain_pct(value):

    value = clean_value(value)

    if value is None:
        return "N/A"

    return f"{value:.2f}%"


def format_change(value):

    value = clean_value(value)

    if value is None:
        return "N/A"

    if value > 0:
        return f"▲ {value:.2f}%"

    if value < 0:
        return f"▼ {abs(value):.2f}%"

    return "━ 0.00%"


def value_or_na(value):

    if value is None:
        return "N/A"

    return str(value)


# =========================================================
# REPORT BUILDER
# =========================================================

class ReportBuilder:

    def __init__(self):

        self.lines = []

    def add(self, text=""):

        self.lines.append(
            str(text)
        )

    def blank(self):

        self.lines.append("")

    def separator(self):

        self.lines.append(
            "─" * 78
        )

    def section(self, title):

        self.blank()

        self.lines.append(
            "╔" + "═" * 76 + "╗"
        )

        self.lines.append(
            f"║ {title:<74} ║"
        )

        self.lines.append(
            "╚" + "═" * 76 + "╝"
        )

    def subsection(self, title):

        self.blank()

        self.lines.append(
            f"▸ {title}"
        )

        self.lines.append(
            "─" * 78
        )

    def text(self):

        return "\n".join(
            self.lines
        )


# =========================================================
# INDIAN MARKET
# =========================================================

def add_indian_market(
    report,
    indian_market
):

    report.section(
        "🇮🇳 INDIAN MARKET"
    )

    indices = indian_market.get(
        "indices",
        {}
    )

    if not indices:

        report.add(
            "No Indian market data available."
        )

        return

    report.add(
        f"{'INDEX':<35}"
        f"{'PRICE':>15}"
        f"{'CHANGE':>15}"
    )

    report.separator()

    for name, data in indices.items():

        if not isinstance(
            data,
            dict
        ):
            continue

        price = data.get(
            "price"
        )

        change = data.get(
            "change_percent"
        )

        report.add(
            f"{name:<35}"
            f"{format_number(price):>15}"
            f"{format_change(change):>15}"
        )

    report.blank()

    # Detailed Nifty information

    nifty = indices.get(
        "NIFTY 50"
    )

    if nifty:

        report.subsection(
            "NIFTY 50 — SESSION DATA"
        )

        report.add(
            f"Open            : "
            f"{format_number(nifty.get('open'))}"
        )

        report.add(
            f"High            : "
            f"{format_number(nifty.get('high'))}"
        )

        report.add(
            f"Low             : "
            f"{format_number(nifty.get('low'))}"
        )

        report.add(
            f"Previous Close  : "
            f"{format_number(nifty.get('previous_close'))}"
        )

        report.add(
            f"52W High        : "
            f"{format_number(nifty.get('year_high'))}"
        )

        report.add(
            f"52W Low         : "
            f"{format_number(nifty.get('year_low'))}"
        )

        report.add(
            f"P/E             : "
            f"{format_number(nifty.get('pe'))}"
        )

        report.add(
            f"P/B             : "
            f"{format_number(nifty.get('pb'))}"
        )

        report.add(
            f"Dividend Yield  : "
            f"{format_number(nifty.get('dividend_yield'))}"
        )


# =========================================================
# MARKET BREADTH
# =========================================================

def add_breadth(
    report,
    indian_market
):

    report.section(
        "📊 MARKET BREADTH"
    )

    breadth = indian_market.get(
        "breadth"
    )

    if not breadth:

        indices = indian_market.get(
            "indices",
            {}
        )

        nifty = indices.get(
            "NIFTY 50",
            {}
        )

        advances = nifty.get(
            "advances"
        )

        declines = nifty.get(
            "declines"
        )

        unchanged = nifty.get(
            "unchanged"
        )

        if (
            advances is not None
            or declines is not None
        ):

            report.add(
                f"Advances    : "
                f"{value_or_na(advances)}"
            )

            report.add(
                f"Declines    : "
                f"{value_or_na(declines)}"
            )

            report.add(
                f"Unchanged   : "
                f"{value_or_na(unchanged)}"
            )

            return

        report.add(
            "Breadth data unavailable."
        )

        return

    for key, value in breadth.items():

        if isinstance(
            value,
            float
        ):

            report.add(
                f"{key:<25}: "
                f"{format_plain_pct(value)}"
            )

        else:

            report.add(
                f"{key:<25}: "
                f"{value_or_na(value)}"
            )


# =========================================================
# CURRENT SECTORS
# =========================================================

def add_current_sectors(
    report,
    indian_market,
    sector_analysis
):

    report.section(
        "🏭 SECTOR PERFORMANCE — LATEST SESSION"
    )

    sectors = indian_market.get(
        "sectors",
        []
    )

    if isinstance(
        sectors,
        dict
    ):

        sectors = list(
            sectors.values()
        )

    clean_sectors = []

    for sector in sectors:

        if not isinstance(
            sector,
            dict
        ):
            continue

        name = sector.get(
            "name",
            sector.get(
                "index",
                sector.get(
                    "sector",
                    "Unknown Sector"
                )
            )
        )

        change = clean_value(
            sector.get(
                "change_percent"
            )
        )

        clean_sectors.append(
            (
                name,
                change
            )
        )

    clean_sectors.sort(
        key=lambda x: (
            x[1]
            if x[1] is not None
            else -999
        ),
        reverse=True
    )

    if not clean_sectors:

        report.add(
            "No sector data available."
        )

        return

    report.add(
        f"{'SECTOR':<50}"
        f"{'CHANGE':>15}"
    )

    report.separator()

    for name, change in clean_sectors:

        report.add(
            f"{name:<50}"
            f"{format_change(change):>15}"
        )

    # -----------------------------------------------------
    # Leaders / laggards from analysis engine
    # -----------------------------------------------------

    leaders = sector_analysis.get(
        "leaders",
        []
    )

    laggards = sector_analysis.get(
        "laggards",
        []
    )

    if leaders:

        report.subsection(
            "Today's Leaders"
        )

        for sector in leaders[:5]:

            name = sector.get(
                "name",
                sector.get(
                    "sector",
                    "Unknown"
                )
            )

            change = sector.get(
                "change_percent"
            )

            report.add(
                f"  ▲ {name:<40}"
                f"{format_pct(change):>12}"
            )

    if laggards:

        report.subsection(
            "Today's Laggards"
        )

        for sector in laggards[:5]:

            name = sector.get(
                "name",
                sector.get(
                    "sector",
                    "Unknown"
                )
            )

            change = sector.get(
                "change_percent"
            )

            report.add(
                f"  ▼ {name:<40}"
                f"{format_pct(change):>12}"
            )


# =========================================================
# GLOBAL MARKET
# =========================================================

def add_global_market(
    report,
    global_market
):

    report.section(
        "🌎 GLOBAL MARKETS"
    )

    if not global_market:

        report.add(
            "Global market data unavailable."
        )

        return

    report.add(
        f"{'ASSET':<30}"
        f"{'VALUE':>20}"
        f"{'CHANGE':>15}"
    )

    report.separator()

    for name, data in global_market.items():

        if not isinstance(
            data,
            dict
        ):
            continue

        value = data.get(
            "price",
            data.get(
                "value"
            )
        )

        change = data.get(
            "change_percent"
        )

        report.add(
            f"{name:<30}"
            f"{format_number(value):>20}"
            f"{format_change(change):>15}"
        )


# =========================================================
# COMMODITIES
# =========================================================

def add_commodities(
    report,
    global_market
):

    report.section(
        "🛢️ COMMODITIES & CROSS-ASSET"
    )

    commodity_names = [
        "Gold Futures",
        "Silver Futures",
        "Crude Oil",
    ]

    found = False

    for name in commodity_names:

        data = global_market.get(
            name
        )

        if not isinstance(
            data,
            dict
        ):
            continue

        found = True

        value = data.get(
            "price",
            data.get(
                "value"
            )
        )

        change = data.get(
            "change_percent"
        )

        report.add(
            f"{name:<30}"
            f"{format_number(value):>20}"
            f"{format_change(change):>15}"
        )

    if not found:

        report.add(
            "Commodity data unavailable."
        )

    report.blank()

    report.add(
        "Note: Commodity futures are global reference prices."
    )


# =========================================================
# FII / DII
# =========================================================

def add_fii_dii(
    report,
    fii_dii
):

    report.section(
        "💰 FII / DII ACTIVITY"
    )

    if not fii_dii:

        report.add(
            "FII/DII data unavailable."
        )

        return

    if isinstance(
        fii_dii,
        list
    ):

        report.add(
            f"{'DATE':<18}"
            f"{'CATEGORY':<15}"
            f"{'BUY':>15}"
            f"{'SELL':>15}"
            f"{'NET':>15}"
        )

        report.separator()

        for item in fii_dii:

            if not isinstance(
                item,
                dict
            ):
                continue

            report.add(
                f"{str(item.get('date', 'N/A')):<18}"
                f"{str(item.get('category', 'N/A')):<15}"
                f"{format_number(item.get('buyValue')):>15}"
                f"{format_number(item.get('sellValue')):>15}"
                f"{format_number(item.get('netValue')):>15}"
            )

    elif isinstance(
        fii_dii,
        dict
    ):

        for key, value in fii_dii.items():

            report.add(
                f"{key:<25}: "
                f"{value_or_na(value)}"
            )

    else:

        report.add(
            str(fii_dii)
        )


# =========================================================
# MACRO
# =========================================================

def add_macro(
    report,
    macro
):

    report.section(
        "🌐 MACROECONOMICS"
    )

    if not macro:

        report.add(
            "Macro data unavailable."
        )

        return

    for name, data in macro.items():

        if isinstance(
            data,
            dict
        ):

            value = data.get(
                "value"
            )

            date = data.get(
                "date"
            )

            line = (
                f"{name:<30}"
                f"{format_number(value):>15}"
            )

            if date:

                line += (
                    f"   [{date}]"
                )

            report.add(
                line
            )

        else:

            report.add(
                f"{name:<30}"
                f"{value_or_na(data):>15}"
            )


# =========================================================
# NEWS
# =========================================================

def add_news(
    report,
    news
):

    report.section(
        "📰 MARKET-MOVING NEWS"
    )

    if not news:

        report.add(
            "No news available."
        )

        return

    for item in news:

        if isinstance(
            item,
            dict
        ):

            title = item.get(
                "title",
                "Untitled"
            )

            category = item.get(
                "category"
            )

            source = item.get(
                "source"
            )

            report.add(
                f"• {title}"
            )

            metadata = []

            if category:
                metadata.append(
                    str(category)
                )

            if source:
                metadata.append(
                    str(source)
                )

            if metadata:

                report.add(
                    "  "
                    + " | ".join(
                        metadata
                    )
                )

        else:

            report.add(
                f"• {item}"
            )


# =========================================================
# HISTORICAL MARKET
# =========================================================

def add_historical_market(
    report,
    historical
):

    report.section(
        "📈 HISTORICAL MARKET ANALYSIS"
    )

    for name, data in historical.items():

        if not isinstance(
            data,
            dict
        ):

            continue

        if data.get(
            "status"
        ) != "OK":

            report.add(
                f"{name}: unavailable"
            )

            continue

        report.subsection(
            name
        )

        report.add(
            f"1D                  "
            f"{format_pct(data.get('1D'))}"
        )

        report.add(
            f"5D                  "
            f"{format_pct(data.get('5D'))}"
        )

        report.add(
            f"1M                  "
            f"{format_pct(data.get('1M'))}"
        )

        report.add(
            f"3M                  "
            f"{format_pct(data.get('3M'))}"
        )

        report.add(
            f"6M                  "
            f"{format_pct(data.get('6M'))}"
        )

        report.add(
            f"1Y                  "
            f"{format_pct(data.get('1Y'))}"
        )

        report.blank()

        report.add(
            f"52W High            "
            f"{format_number(data.get('52w_high'))}"
        )

        report.add(
            f"52W Low             "
            f"{format_number(data.get('52w_low'))}"
        )

        report.add(
            f"From 52W High       "
            f"{format_pct(data.get('distance_from_52w_high'))}"
        )

        report.add(
            f"From 52W Low        "
            f"{format_pct(data.get('distance_from_52w_low'))}"
        )

        report.add(
            f"Maximum Drawdown    "
            f"{format_pct(data.get('maximum_drawdown'))}"
        )

        report.add(
            f"Annualized Volatility"
            f" {format_plain_pct(data.get('annualized_volatility'))}"
        )


# =========================================================
# HISTORICAL SECTORS
# =========================================================

def add_sector_history(
    report,
    sector_history
):

    report.section(
        "🔄 SECTOR PERFORMANCE — MULTI-HORIZON"
    )

    report.add(
        f"{'SECTOR':<25}"
        f"{'1D':>12}"
        f"{'1M':>12}"
        f"{'3M':>12}"
        f"{'1Y':>12}"
    )

    report.separator()

    valid = []

    for name, data in sector_history.items():

        if not isinstance(
            data,
            dict
        ):
            continue

        if data.get(
            "status"
        ) != "OK":

            continue

        valid.append(
            (
                name,
                data
            )
        )

    # Sort by 1Y performance

    valid.sort(
        key=lambda item: (
            clean_value(
                item[1].get("1Y")
            )
            if clean_value(
                item[1].get("1Y")
            ) is not None
            else -999
        ),
        reverse=True
    )

    for name, data in valid:

        report.add(
            f"{name:<25}"
            f"{format_pct(data.get('1D')):>12}"
            f"{format_pct(data.get('1M')):>12}"
            f"{format_pct(data.get('3M')):>12}"
            f"{format_pct(data.get('1Y')):>12}"
        )


# =========================================================
# MARKET INTERPRETATION
# =========================================================

def add_market_interpretation(
    report,
    analysis
):

    report.section(
        "🧠 MARKET INTERPRETATION"
    )

    observations = analysis.get(
        "observations",
        []
    )

    if not observations:

        report.add(
            "No market observations available."
        )

        return

    for observation in observations:

        report.add(
            f"• {observation}"
        )


# =========================================================
# REPORT FOOTER
# =========================================================

def add_footer(
    report
):

    report.blank()

    report.separator()

    report.add(
        "⚠️ EDUCATIONAL MARKET INTELLIGENCE"
    )

    report.add(
        "This report describes market conditions and trends."
    )

    report.add(
        "It does not provide guaranteed buy/sell signals."
    )

    report.add(
        "Always verify data before making investment decisions."
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 78)

    print(
        "INVESTMENT INTELLIGENCE"
    )

    print("=" * 78)

    # -----------------------------------------------------
    # Data collection
    # -----------------------------------------------------

    print(
        "\n[1/9] Fetching Indian market..."
    )

    indian_market = (
        get_indian_market()
    )

    print(
        "\n[2/9] Fetching global market..."
    )

    global_market = (
        get_global_market()
    )

    print(
        "\n[3/9] Fetching FII/DII..."
    )

    fii_dii = (
        get_fii_dii()
    )

    print(
        "\n[4/9] Fetching macro..."
    )

    macro = (
        get_macro_snapshot()
    )

    print(
        "\n[5/9] Collecting news..."
    )

    news = (
        get_news()
    )

    print(
        "\n[6/9] Fetching historical market data..."
    )

    historical = (
        get_historical_snapshot()
    )

    print(
        "\n[7/9] Fetching sector history..."
    )

    sector_history = (
        get_sector_history()
    )

    print(
        "\n[8/9] Analyzing sectors..."
    )

    sector_analysis = (
        analyze_sectors(
            indian_market.get(
                "sectors",
                []
            )
        )
    )

    print(
        "\n[9/9] Building intelligence..."
    )

    analysis = analyze_market(

        indian_market,

        global_market,

        sector_analysis,
    )

    # -----------------------------------------------------
    # Build report
    # -----------------------------------------------------

    report = ReportBuilder()

    now = datetime.now()

    report.add(
        "╔" + "═" * 76 + "╗"
    )

    report.add(
        "║"
        + " INVESTMENT INTELLIGENCE".ljust(76)
        + "║"
    )

    report.add(
        "║"
        + (
            f" Generated: "
            f"{now.strftime('%d %b %Y %H:%M')}"
        ).ljust(76)
        + "║"
    )

    report.add(
        "╚" + "═" * 76 + "╝"
    )

    report.add(
        "Market intelligence dashboard"
    )

    # -----------------------------------------------------
    # Sections
    # -----------------------------------------------------

    add_indian_market(
        report,
        indian_market
    )

    add_breadth(
        report,
        indian_market
    )

    add_current_sectors(
        report,
        indian_market,
        sector_analysis
    )

    add_sector_history(
        report,
        sector_history
    )

    add_global_market(
        report,
        global_market
    )

    add_commodities(
        report,
        global_market
    )

    add_fii_dii(
        report,
        fii_dii
    )

    add_macro(
        report,
        macro
    )

    add_news(
        report,
        news
    )

    add_historical_market(
        report,
        historical
    )

    add_market_interpretation(
        report,
        analysis
    )

    add_footer(
        report
    )

    # -----------------------------------------------------
    # Convert report to text
    # -----------------------------------------------------

    report_text = report.text()

    # -----------------------------------------------------
    # Generate public dashboard
    # -----------------------------------------------------

    generate_dashboard(
        indian_market=indian_market,
        global_market=global_market,
        fii_dii=fii_dii,
        news=news,
        analysis=analysis,
    )

    # -----------------------------------------------------
    # Save report
    # -----------------------------------------------------

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_FILE.write_text(
        report_text,
        encoding="utf-8"
    )

    # -----------------------------------------------------
    # Print report
    # -----------------------------------------------------

    print(
        "\n\n" + report_text
    )

    print(
        "\n"
        + "=" * 78
    )

    print(
        f"REPORT SAVED → {REPORT_FILE}"
    )

    print(
        "=" * 78
    )



if __name__ == "__main__":

    main()