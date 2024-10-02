from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

# Создание базового класса для декларативных моделей
Base = declarative_base()
# Создание подключения к базе данных с использованием URL из конфигурации
engine = create_engine(Config.DATABASE_URL)
# Настройка сессии для работы с базой данных
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Инициализация базы данных и создание всех таблиц, определённых в моделях."""
    Base.metadata.create_all(bind=engine)
