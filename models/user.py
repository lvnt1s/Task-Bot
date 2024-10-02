from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Integer, String,BigInteger
from database.db import Base
from typing import Optional
from models.task import Task

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger,unique=True,index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    tasks = relationship(Task, back_populates="owner")

    @classmethod
    def get_by_user_id(cls, session: Session, user_id: int) -> Optional['User']:
        """Получает пользователя по user_id.
        
        Возвращает найденного пользователя
        """
        return session.query(cls).filter_by(user_id=user_id).first()
    
    @classmethod
    def get_by_username(cls, session, username: str) -> Optional['User']:
        """Получает пользователя по username.
        
        Возвращает найденного пользователя
        """
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def create(cls, session: Session,user_id: int, username: str, name: str) -> 'User':
        """Создает нового пользователя
        
        Возвращает созданного пользователя
        """
        new_user = cls(user_id=user_id, username=username, name=name)
        session.add(new_user)
        session.commit()
        return new_user
