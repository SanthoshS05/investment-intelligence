import os
from dotenv import load_dotenv

load_dotenv()

# API configuration
MARKET_API_KEY = os.getenv("MARKET_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
FRED_API_KEY = os.getenv("FRED_API_KEY", "")

# Application settings
APP_NAME = "Investment Intelligence"
