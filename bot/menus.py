from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_welcome_keyboard() -> InlineKeyboardMarkup:
    """Return the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("How to Use", callback_data="menu_help")],
        [
            InlineKeyboardButton("Photo ID", callback_data="menu_photo"),
            InlineKeyboardButton("Text ID", callback_data="menu_text"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Return a keyboard with a button to reopen the main menu."""
    keyboard = [[InlineKeyboardButton("Main Menu", callback_data="menu_main")]]
    return InlineKeyboardMarkup(keyboard)
