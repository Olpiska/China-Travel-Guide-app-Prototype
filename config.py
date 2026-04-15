"""
config.py
---------
Central configuration constants for the AI China Travel Assistant.
Change MODEL_NAME or MAX_TOKENS here to affect the whole app.
"""

APP_TITLE    = "AI China Travel Assistant"
APP_SUBTITLE = "Your intelligent guide to exploring the Middle Kingdom 🇨🇳"

# OpenRouter / OpenAI proxy model to use
MODEL_NAME = "openai/gpt-oss-120b"

# OpenRouter API base URL
API_BASE_URL = "https://openrouter.ai/api/v1"

# Maximum tokens the model may return per response
MAX_TOKENS = 6000
