from pyrogram import Client, filters
from pyrogram.types import Message
from keyboards.reply import keyboards as keyboard
from database.db import DatabaseSession
from models.user import User
from states.states import user_data,user_states,States



async def start(client: Client, message: Message) -> None:
    """Обработчик команды /start. Проверяет, существует ли пользователь в базе данных."""
    session = DatabaseSession()
    try:
        user = session.query(User).filter_by(user_id=message.from_user.id).first()
        if user:
            await message.reply(f"С возвращением, {user.name}!")
        else:
            user_states[message.from_user.id] = States.name
            await message.reply("<b>Привет! Как тебя зовут?</b>")
    finally:
        session.close()

async def handle_name(client: Client, message: Message) -> None:
    """Обработчик для получения имени пользователя."""
    user_id = message.from_user.id
    if user_states.get(user_id) == States.name:
        if user_states.get(user_id) == States.name:
            user_data[user_id] = {"name": message.text}
            user_states[user_id] = States.username
            await message.reply("<b>Отлично! Теперь придумай юзернейм!</b>")

async def handle_username(client: Client, message: Message) -> None:
    """Обработчик для получения юзернейма пользователя."""
    user_id = message.from_user.id
    if user_states.get(user_id) == States.username:
        session = DatabaseSession()
        existing_user = User.get_by_username(session=session, username=message.text)
        if existing_user:
            await message.reply(
                """<b>❗️Этот юзернейм уже занят!</b>
Пожалуйста, введите уникальный юзернейм:""",
                parse_mode="HTML"
            )
            return

        User.create(session=session,
            user_id=message.from_user.id,
            username=message.text,
            name=user_data[user_id]['name']
        )
        await message.reply(
            """<b>❗️Регистрация прошла успешно!</b>
<i>Снизу представлено навигационное меню бота.</i>""",
            reply_markup=await keyboard.menu()
        )
        user_states[user_id] = None


