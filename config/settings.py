import os

from pytrends.request import TrendReq
import google.generativeai as genai


# ============================================================
# Project paths
# ============================================================

PROJECT_DIR = os.getenv(
    "PROJECT_DIR",
    "/content/drive/MyDrive/GEO_MVP"
)

os.makedirs(
    PROJECT_DIR,
    exist_ok=True
)


# ============================================================
# API Keys
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)


# ============================================================
# Gemini
# ============================================================

gemini_model = None

if GEMINI_API_KEY:

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    gemini_model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )


# ============================================================
# Google Trends
# ============================================================

pytrends = TrendReq(
    hl="en-US",
    tz=360
)
