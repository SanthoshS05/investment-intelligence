"""
Public GitHub Pages dashboard generator.

Generates:
    docs/index.html

This dashboard contains only public market intelligence.
"""

from pathlib import Path
from html import escape


DOCS_DIR = Path("docs")
DASHBOARD_FILE = DOCS_DIR / "index.html"


def safe(value, default="N/A"):
    if value is None:
        return default
    return escape(str(value))


def format_price(value):
    if value is None:
        return "N/A"

    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def format_change(value):
    if value is None:
        return "N/A"

    try:
        value = float(value)

        if value > 0:
            return f"▲ {value:.2f}%"

        if value < 0:
            return f"▼ {abs(value):.2f}%"

        return "━ 0.00%"

    except (TypeError, ValueError):
        return "N/A"


def change_class(value):
    if value is None:
        return "neutral"

    try:
        value = float(value)

        if value > 0:
            return "positive"

        if value < 0:
            return "negative"

        return "neutral"

    except (TypeError, ValueError):
        return "neutral"


def build_index_cards(indian_market):
    indices = indian_market.get("indices", {})

    cards = []

    preferred = [
        "NIFTY 50",
        "NIFTY MIDCAP 100",
        "NIFTY SMALLCAP 100",
        "NIFTY NEXT 50",
        "INDIA VIX",
    ]

    for name in preferred:

        data = indices.get(name)

        if not isinstance(data, dict):
            continue

        price = data.get("price")
        change = data.get("change_percent")

        cards.append(
            f"""
            <div class="card">
                <div class="card-title">{safe(name)}</div>
                <div class="card-value">
                    {format_price(price)}
                </div>
                <div class="change {change_class(change)}">
                    {format_change(change)}
                </div>
            </div>
            """
        )

    return "\n".join(cards)


def build_sector_table(indian_market):
    sectors = indian_market.get("sectors", {})

    if isinstance(sectors, dict):
        sectors = list(sectors.values())

    rows = []

    for sector in sectors:

        if not isinstance(sector, dict):
            continue

        name = sector.get("name", "Unknown")
        change = sector.get("change_percent")

        rows.append(
            (
                name,
                change,
            )
        )

    rows.sort(
        key=lambda item: (
            float(item[1])
            if item[1] is not None
            else -999
        ),
        reverse=True,
    )

    for name, change in rows:

        rows_html = f"""
            <tr>
                <td>{safe(name)}</td>
                <td class="{change_class(change)}">
                    {format_change(change)}
                </td>
            </tr>
        """

        yield rows_html


def build_global_table(global_market):
    rows = []

    for name, data in global_market.items():

        if not isinstance(data, dict):
            continue

        value = data.get(
            "price",
            data.get("value"),
        )

        change = data.get(
            "change_percent"
        )

        rows.append(
            f"""
            <tr>
                <td>{safe(name)}</td>
                <td>{format_price(value)}</td>
                <td class="{change_class(change)}">
                    {format_change(change)}
                </td>
            </tr>
            """
        )

    return "\n".join(rows)


def build_fii_dii(fii_dii):
    if not isinstance(fii_dii, list):
        return "<p>FII/DII data unavailable.</p>"

    rows = []

    for item in fii_dii:

        if not isinstance(item, dict):
            continue

        date = item.get("date", "N/A")
        category = item.get("category", "N/A")
        net = item.get("netValue")

        rows.append(
            f"""
            <tr>
                <td>{safe(date)}</td>
                <td>{safe(category)}</td>
                <td>{format_price(net)}</td>
            </tr>
            """
        )

    return "\n".join(rows)


def build_news(news):
    if not news:
        return "<p>No news available.</p>"

    items = []

    for item in news[:15]:

        if isinstance(item, dict):

            title = item.get(
                "title",
                "Untitled",
            )

            category = item.get(
                "category",
                "",
            )

            source = item.get(
                "source",
                "",
            )

            metadata = " • ".join(
                x
                for x in [category, source]
                if x
            )

            items.append(
                f"""
                <div class="news-item">
                    <div class="news-title">
                        {safe(title)}
                    </div>

                    <div class="news-meta">
                        {safe(metadata)}
                    </div>
                </div>
                """
            )

        else:

            items.append(
                f"""
                <div class="news-item">
                    <div class="news-title">
                        {safe(item)}
                    </div>
                </div>
                """
            )

    return "\n".join(items)


def generate_dashboard(
    indian_market,
    global_market,
    fii_dii,
    news,
    analysis=None,
):
    """
    Generate the public dashboard.
    """

    analysis = analysis or {}

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    index_cards = build_index_cards(
        indian_market
    )

    sector_rows = "".join(
        build_sector_table(
            indian_market
        )
    )

    global_rows = build_global_table(
        global_market
    )

    fii_dii_rows = build_fii_dii(
        fii_dii
    )

    news_html = build_news(
        news
    )

    observations = analysis.get(
        "observations",
        [],
    )

    interpretation_html = ""

    for observation in observations:
        interpretation_html += (
            f"<li>{safe(observation)}</li>"
        )

    if not interpretation_html:
        interpretation_html = (
            "<li>No market interpretation available.</li>"
        )

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<meta name="description"
      content="Investment Intelligence - Public Market Dashboard">

<title>Investment Intelligence</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;

    background: #f5f7fa;
    color: #1f2937;
}}

.container {{
    max-width: 1200px;
    margin: auto;
    padding: 24px;
}}

header {{
    background: #111827;
    color: white;
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 24px;
}}

header h1 {{
    margin: 0 0 8px 0;
    font-size: 30px;
}}

header p {{
    margin: 0;
    opacity: 0.75;
}}

section {{
    margin-bottom: 24px;
}}

.section-title {{
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 14px;
}}

.cards {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(190px, 1fr));

    gap: 14px;
}}

.card {{
    background: white;
    padding: 20px;
    border-radius: 14px;

    box-shadow:
        0 2px 10px rgba(0,0,0,0.06);
}}

.card-title {{
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 10px;
}}

.card-value {{
    font-size: 25px;
    font-weight: 700;
}}

.change {{
    margin-top: 8px;
    font-weight: 600;
}}

.positive {{
    color: #15803d;
}}

.negative {{
    color: #dc2626;
}}

.neutral {{
    color: #6b7280;
}}

.panel {{
    background: white;
    border-radius: 14px;
    padding: 20px;

    box-shadow:
        0 2px 10px rgba(0,0,0,0.06);

    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th,
td {{
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}}

th {{
    color: #6b7280;
    font-size: 13px;
    text-transform: uppercase;
}}

.news-item {{
    padding: 14px 0;
    border-bottom: 1px solid #e5e7eb;
}}

.news-item:last-child {{
    border-bottom: none;
}}

.news-title {{
    font-weight: 600;
}}

.news-meta {{
    margin-top: 5px;
    color: #6b7280;
    font-size: 13px;
}}

.interpretation li {{
    margin-bottom: 10px;
    line-height: 1.5;
}}

footer {{
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    padding: 20px;
}}

@media (max-width: 600px) {{

    .container {{
        padding: 12px;
    }}

    header {{
        padding: 20px;
    }}

    header h1 {{
        font-size: 24px;
    }}

}}

</style>

</head>

<body>

<div class="container">

<header>

<h1>📈 Investment Intelligence</h1>

<p>
Public Market Intelligence Dashboard
</p>

</header>


<section>

<div class="section-title">
🇮🇳 Indian Market
</div>

<div class="cards">

{index_cards}

</div>

</section>


<section>

<div class="section-title">
🔄 Sector Performance
</div>

<div class="panel">

<table>

<thead>

<tr>
<th>Sector</th>
<th>Latest Session</th>
</tr>

</thead>

<tbody>

{sector_rows}

</tbody>

</table>

</div>

</section>


<section>

<div class="section-title">
🌎 Global Markets
</div>

<div class="panel">

<table>

<thead>

<tr>
<th>Asset</th>
<th>Value</th>
<th>Change</th>
</tr>

</thead>

<tbody>

{global_rows}

</tbody>

</table>

</div>

</section>


<section>

<div class="section-title">
💰 FII / DII Activity
</div>

<div class="panel">

<table>

<thead>

<tr>
<th>Date</th>
<th>Category</th>
<th>Net</th>
</tr>

</thead>

<tbody>

{fii_dii_rows}

</tbody>

</table>

</div>

</section>


<section>

<div class="section-title">
📰 Market News
</div>

<div class="panel">

{news_html}

</div>

</section>


<section>

<div class="section-title">
🧠 Market Interpretation
</div>

<div class="panel interpretation">

<ul>

{interpretation_html}

</ul>

</div>

</section>


<footer>

⚠️ Educational market intelligence.
Not financial advice.

</footer>

</div>

</body>

</html>
"""

    DASHBOARD_FILE.write_text(
        html,
        encoding="utf-8",
    )

    print(
        f"Dashboard generated → {DASHBOARD_FILE}"
    )

    return DASHBOARD_FILE