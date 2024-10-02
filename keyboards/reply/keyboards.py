from pyrogram.types import ReplyKeyboardMarkup

async def menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        [["📝 Мои задачи"]],
        resize_keyboard=True
    )
    return keyboard