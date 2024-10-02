from pyrogram import Client, filters
from pyrogram.types import Message
from keyboards.reply import keyboards as keyboard
from database.db import DatabaseSession
from models.user import User

class States:
    name = "name"
    username = "username"

user_states = {}
user_data = {}

async def start(client: Client, message: Message) -> None:
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
    user_id = message.from_user.id
    if user_states.get(user_id) == States.name:
        user_data[user_id] = {"name": message.text}
        user_states[user_id] = States.username
        await message.reply("<b>Отлично! Теперь придумай юзернейм!</b>")

async def handle_username(client: Client, message: Message) -> None:
    user_id = message.from_user.id
    if user_states.get(user_id) == States.username:
        session = DatabaseSession()
        new_user = User.create(session=session,
            user_id=message.from_user.id,
            username=message.text,
            name=user_data[user_id]['name']
        )
        session.add(new_user)
        session.commit()
        await message.reply(
            """<b>❗️Регистрация прошла успешно!</b>
<i>Снизу представлено навигационное меню бота.</i>""",
            reply_markup=await keyboard.menu()
        )


