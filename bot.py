import asyncio
import sys
from pyrogram import Client, filters
from config import Config
from database.db import init_db
import logging
from pyrogram.enums import ParseMode
from handlers.authorization import start, handle_name, handle_username,user_states,States

app = Client(name = 'tasks_bot',
            api_id=Config.API_ID,
            api_hash=Config.API_HASH, 
            bot_token=Config.BOT_TOKEN,
            parse_mode=ParseMode.HTML)

def register_handlers(app: Client):
    app.on_message(filters.command("start"))(start)
    app.on_message(filters.text & filters.private & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == States.name))(handle_name)
    app.on_message(filters.text & filters.private & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == States.username))(handle_username)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    register_handlers(app)
    init_db()
    app.run()
