# Mock data and constants for the StockIQ app

# Stock data
STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "logo": "🍏", "sector": "Technology", "risk": "Low"},
    {"symbol": "TSLA", "name": "Tesla, Inc.", "logo": "🚗", "sector": "Automotive", "risk": "High"},
    {"symbol": "AMZN", "name": "Amazon.com, Inc.", "logo": "📦", "sector": "Consumer Discretionary", "risk": "Medium"},
    {"symbol": "META", "name": "Meta Platforms, Inc.", "logo": "📱", "sector": "Communication Services", "risk": "High"},
    {"symbol": "GOOG", "name": "Alphabet Inc.", "logo": "🔍", "sector": "Technology", "risk": "Low"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "logo": "🎮", "sector": "Technology", "risk": "Medium"},
]

# Sector data
SECTORS = [
    "Technology", "Healthcare", "Finance", "Energy", 
    "Consumer Discretionary", "Industrials", "Utilities"
]

# Onboarding questions
ONBOARDING_QUESTIONS = [
    ("Are you a beginner, intermediate, or expert trader?", ["Beginner", "Intermediate", "Expert"]),
    ("How much capital do you usually invest?", None),
    ("What's your average holding period?", None),
    ("Are you interested in short-term or long-term analysis?", ["Short-term", "Long-term", "Both"]),
    ("Which sectors are you most interested in?", SECTORS),
    ("List your 3 favorite stocks", None),
    ("How often do you trade per week?", None),
    ("Are you risk-averse, neutral, or risk-seeking?", ["Risk-averse", "Neutral", "Risk-seeking"]),
    ("Do you use technical indicators? (Yes/No + which ones)", None),
    ("What kind of predictions would you like (price, trend, sentiment, etc.)?", None),
]

# News headlines
NEWS_HEADLINES = [
    "Stock surges after strong earnings report.",
    "Analysts predict continued growth in the sector.",
    "Company announces new product line.",
    "Market volatility expected to increase.",
    "Regulatory changes impact industry outlook.",
    "CEO announces strategic partnership with tech giant.",
    "Quarterly results exceed market expectations.",
    "Investors respond positively to dividend increase.",
    "New market expansion planned for next quarter.",
    "Industry leaders gather for annual conference."
]

# Navigation items
NAVIGATION_ITEMS = [
    ("Welcome", "welcome"),
    ("Login/Signup", "auth"),
    ("Onboarding", "onboard"),
    ("Dashboard", "dashboard"),
    ("Stock Detail", "stock_detail"),
    ("AI Assistant", "chatbot")
    # ("Glossary", "glossary"),
]