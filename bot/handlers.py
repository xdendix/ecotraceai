import html
import json
import os
import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.menus import get_back_keyboard, get_welcome_keyboard
from ai.gemma_service import analyze_nature_image
from ai.gemma_service import generate_nature_insight
import sentry_sdk


_BOLD_MARKDOWN = re.compile(r"\*{1,2}([^*\n]+?)\*{1,2}")
_LIST_MARKER = re.compile(r"^(\s*)(?:[-+]|\*{1,2})\s+")


def get_text(key: str) -> str:
    """Fetch a fixed English interface string."""
    file_path = os.path.join(os.path.dirname(__file__), "../locales/en.json")
    with open(file_path, "r", encoding="utf-8") as f:
        translations = json.load(f)
    return translations.get(key, key)


def _format_ai_response(text: str) -> str:
    """Convert AI emphasis and list markers to safe Telegram HTML."""
    formatted_lines = []
    for line in text.splitlines():
        list_marker = _LIST_MARKER.match(line)
        prefix = ""
        if list_marker:
            prefix = f"{list_marker.group(1)}• "
            line = line[list_marker.end() :]
        else:
            line = re.sub(r"^\s*\*{2,}\s+", "", line)

        parts = []
        position = 0
        for match in _BOLD_MARKDOWN.finditer(line):
            parts.append(html.escape(line[position : match.start()]))
            parts.append(f"<b>{html.escape(match.group(1))}</b>")
            position = match.end()
        parts.append(html.escape(line[position:].replace("*", "")))
        formatted_lines.append(prefix + "".join(parts))

    return "\n".join(formatted_lines)


async def start_command(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    if update.message is None:
        return

    await update.message.reply_text(
        get_text("welcome"),
        reply_markup=get_welcome_keyboard(),
    )


async def menu_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Handle main-menu navigation and usage instructions."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    callback_data = query.data
    if callback_data is None:
        return

    if callback_data == "menu_main":
        await query.edit_message_text(
            text=get_text("welcome"),
            reply_markup=get_welcome_keyboard(),
        )
        return

    messages = {
        "menu_help": get_text("help"),
        "menu_photo": get_text("photo_help"),
        "menu_text": get_text("text_help"),
    }
    message = messages.get(callback_data)
    if message is not None:
        await query.edit_message_text(
            text=message,
            reply_markup=get_back_keyboard(),
        )


async def handle_text_message(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Handles text messages and routes them to Gemma AI."""
    if update.message is None or update.effective_user is None:
        return

    user_text = update.message.text
    if user_text is None:
        return

    processing_msg = await update.message.reply_text(get_text("processing"))

    with sentry_sdk.start_transaction(op="ai_inference", name="Gemma2_Local"):
        ai_response = await generate_nature_insight(prompt=user_text)

    # Reply to user
    if ai_response:
        await processing_msg.edit_text(
            text=_format_ai_response(ai_response),
            parse_mode=ParseMode.HTML,
        )
    else:
        await processing_msg.edit_text(text=get_text("error_ai"))


async def handle_photo_message(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Handles photo messages and routes them to the Vision AI."""
    if update.message is None or update.effective_user is None:
        return

    caption = update.message.caption or "Please identify this image."

    processing_msg = await update.message.reply_text(
        get_text("processing_photo")
    )

    photo_file = await update.message.photo[-1].get_file()
    user_id = update.effective_user.id
    temp_image_path = f"temp_{user_id}.jpg"
    await photo_file.download_to_drive(temp_image_path)

    try:
        with sentry_sdk.start_transaction(op="ai_vision", name="LLaVA_Local"):
            ai_response = await analyze_nature_image(
                image_path=temp_image_path, caption=caption
            )

        if ai_response:
            await processing_msg.edit_text(
                text=_format_ai_response(ai_response),
                parse_mode=ParseMode.HTML,
            )

        else:
            await processing_msg.edit_text(text=get_text("error_ai"))

    finally:
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
