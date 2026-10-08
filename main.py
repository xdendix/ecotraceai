import logging
from bot.handlers import (
    handle_photo_message,
    handle_text_message,
    menu_callback,
    start_command,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from core.config import TELEGRAM_BOT_TOKEN, init_sentry

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Initialize and run the bot."""
    # 1. Initialize Sentry (Prize Category Target)
    init_sentry()

    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is missing in .env file!")
        return

    # 2. Build application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 3. Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(
        CallbackQueryHandler(menu_callback, pattern="^menu_")
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
    )
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))

    # 4. Start polling
    logger.info("EcoTrace AI is running locally...")
    application.run_polling()


if __name__ == "__main__":
    main()
