from sqlalchemy import Column, Integer, String, Text, ForeignKey,Boolean,BigInteger
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy.exc import NoResultFound

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(BigInteger, ForeignKey('users.user_id'))
    is_complited = Column(Boolean,default=False)
    owner = relationship("User", back_populates="tasks")

    @classmethod
    def create_task(cls, session: Session, title: str, description: str, owner_id: int) -> 'Task':
        """Создает новую задачу и сохраняет её в базе данных.
        
        Возвращает созданную задачу.
        """
        new_task = cls(title=title, description=description, owner_id=owner_id)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

    @classmethod
    def get_task(cls, session: Session, task_id: int) -> 'Task':
        """Получает задачу по ID.
        
        Возвращает найденную задачу
        """
        task = session.query(cls).filter(cls.id == task_id).first()
        return task

    @classmethod
    def update_task(cls, session: Session, task_id: int, title: str = None,is_complited: bool = None, description: str = None) -> 'Task':
        """Обновляет задачу по ID.
        
        Возвращает обновленную задачу.
        """
        task = session.query(cls).filter(cls.id == task_id).first()
        if task is None:
            raise NoResultFound("Task not found")

        if title is not None:
            task.title = title
        if is_complited is not None:
            task.is_complited = is_complited

        if description is not None:
            task.description = description

        session.commit()
        session.refresh(task)
        return task

    @classmethod
    def delete_task(cls, session: Session, task_id: int) -> 'Task':
        """Удаляет задачу по ID.
        
        Возвращает удалённую задачу.
        """
        task = session.query(cls).filter(cls.id == task_id).first()
        if task is None:
            raise NoResultFound("Task not found")

        session.delete(task)
        session.commit()
        return task

    @classmethod
    def get_tasks_by_owner(cls, session: Session, owner_id: int) -> list['Task']:
        """Получает все задачи определенного пользователя.
        
        Возвращает список задач.
        """
        tasks = session.query(cls).filter(cls.owner_id == owner_id).all()
        return tasks