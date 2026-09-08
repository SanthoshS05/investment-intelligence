"""
Financial news collector.

RSS feeds are used because they are free and don't require
expensive news APIs.
"""

import feedparser


FEEDS = {

    "Google Finance India":
        "https://news.google.com/rss/search?q=Indian+stock+market",

    "Google RBI":
        "https://news.google.com/rss/search?q=RBI+India",

    "Google Economy":
        "https://news.google.com/rss/search?q=India+economy+inflation+GDP",

    "Google Crude":
        "https://news.google.com/rss/search?q=crude+oil+India",

    "Google Global Markets":
        "https://news.google.com/rss/search?q=global+stock+market",

    "Google Fed":
        "https://news.google.com/rss/search?q=Federal+Reserve+interest+rates",

    "Google Geopolitics":
        "https://news.google.com/rss/search?q=geopolitics+markets",
}


KEYWORDS = {

    "RBI": [
        "RBI",
        "Reserve Bank",
        "repo rate",
        "monetary policy",
    ],

    "Inflation": [
        "inflation",
        "CPI",
        "prices",
    ],

    "Growth": [
        "GDP",
        "growth",
        "economy",
    ],

    "Crude": [
        "crude",
        "oil",
        "Brent",
        "OPEC",
    ],

    "Fed": [
        "Federal Reserve",
        "Fed",
        "interest rate",
        "rate cut",
        "rate hike",
    ],

    "Geopolitics": [
        "war",
        "Iran",
        "Israel",
        "Russia",
        "Ukraine",
        "China",
        "tariff",
    ],

    "Markets": [
        "Nifty",
        "Sensex",
        "stocks",
        "equities",
        "shares",
    ],
}


def classify_news(title):

    lower = title.lower()

    categories = []

    for category, words in KEYWORDS.items():

        if any(
            word.lower() in lower
            for word in words
        ):

            categories.append(
                category
            )

    return categories


def get_news():

    news = []

    for source, url in FEEDS.items():

        print(
            f"  Reading {source}..."
        )

        try:

            feed = feedparser.parse(
                url
            )

            for entry in feed.entries[:10]:

                title = entry.get(
                    "title",
                    ""
                )

                news.append({

                    "source": source,

                    "title": title,

                    "link": entry.get(
                        "link",
                        ""
                    ),

                    "published": entry.get(
                        "published",
                        ""
                    ),

                    "categories":
                        classify_news(
                            title
                        ),
                })

        except Exception as e:

            print(
                f"News feed failed: {e}"
            )

    return news