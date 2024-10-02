from pyrogram.types import ReplyKeyboardMarkup

async def menu() -> ReplyKeyboardMarkup:
    """Создание меню для пользователя."""
    keyboard = ReplyKeyboardMarkup(
        [["📝 Мои задачи"]],
        resize_keyboard=True,one_time_keyboard=False
    )
    return keyboard