import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_HASH = os.getenv("API_HASH")
    API_ID = os.getenv("API_ID")
    DATABASE_URL = os.getenv("DATABASE_URL")