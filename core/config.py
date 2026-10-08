import os
from dotenv import load_dotenv
import sentry_sdk

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SENTRY_DSN = os.getenv("SENTRY_DSN")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemma2:2b")


def init_sentry():
    """Initialize Sentry for error and performance tracing."""
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        print("Sentry initialized successfully.")
