import asyncio
import sys
from pyrogram import Client, filters
from config import Config
from database.db import init_db
import logging
from pyrogram.enums import ParseMode
from handlers.authorization import start, handle_name, handle_username
from states.states import user_states,States
from handlers.my_tasks import handle_my_tasks,handle_create_task,\
    handle_cancel_create,handle_task_name,\
    handle_task_description,show_user_task,delete_task,finish_task

# Создание клиента бота
app = Client(name = 'tasks_bot',
            api_id=Config.API_ID,
            api_hash=Config.API_HASH, 
            bot_token=Config.BOT_TOKEN,
            parse_mode=ParseMode.HTML)

# Регистрация обработчиков команд
def register_handlers(app: Client):
    app.on_message(filters.command("start"))(start)
    app.on_message(filters.text & filters.private & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == States.name))(handle_name)
    app.on_message(filters.text & filters.private & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == States.username))(handle_username)
    app.on_message(filters.text & filters.private & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == States.task_name))(handle_task_name)
    app.on_message(filters.text & filters.private & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == States.task_description))(handle_task_description)
    app.on_message(filters.regex("^📝 Мои задачи") & filters.private)(handle_my_tasks)
    app.on_callback_query(filters.regex("^create_task"))(handle_create_task)
    app.on_callback_query(filters.regex("^show_task"))(show_user_task)
    app.on_callback_query(filters.regex("^cancel_create"))(handle_cancel_create)
    app.on_callback_query(filters.regex("^delete_task"))(delete_task)
    app.on_callback_query(filters.regex("^finish_task"))(finish_task)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    register_handlers(app)
    init_db()
    app.run()
