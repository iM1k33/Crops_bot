from pathlib import Path
from .api import OPENAI_API_KEY, TELEGRAM_TOKEN

# API Keys
OPENAI_API_KEY = OPENAI_API_KEY
TELEGRAM_TOKEN = TELEGRAM_TOKEN

# OpenAI Settings
GPT_MODEL = "openai/gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-ada-002"
BASE_URL = "https://api.vsegpt.ru/v1"

# Data Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CROPS_CSV_PATH = PROJECT_ROOT / "data" / "crops.csv"

# Token Limits
TOKEN_BUDGET = 3500
MAX_TOKENS_RESPONSE = 800