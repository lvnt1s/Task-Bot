from sqlalchemy import Column, Integer, String, Text, ForeignKey,Boolean
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy.exc import NoResultFound

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    is_complited = Column(Boolean,default=False)
    owner = relationship("User", back_populates="tasks")

    @classmethod
    def create_task(cls, db: Session, title: str, description: str, owner_id: int) -> 'Task':
        """Создает новую задачу и сохраняет её в базе данных.
        
        Возвращает созданную задачу.
        """
        new_task = cls(title=title, description=description, owner_id=owner_id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    @classmethod
    def get_task(cls, db: Session, task_id: int) -> 'Task':
        """Получает задачу по ID.
        
        Возвращает найденную задачу
        """
        task = db.query(cls).filter(cls.id == task_id).first()
        return task

    @classmethod
    def update_task(cls, db: Session, task_id: int, title: str = None,is_complited: bool = None, description: str = None) -> 'Task':
        """Обновляет задачу по ID.
        
        Возвращает обновленную задачу.
        """
        task = db.query(cls).filter(cls.id == task_id).first()
        if task is None:
            raise NoResultFound("Task not found")

        if title is not None:
            task.title = title
        if is_complited is not None:
            task.is_complited = is_complited

        if description is not None:
            task.description = description

        db.commit()
        db.refresh(task)
        return task

    @classmethod
    def delete_task(cls, db: Session, task_id: int) -> 'Task':
        """Удаляет задачу по ID.
        
        Возвращает удалённую задачу.
        """
        task = db.query(cls).filter(cls.id == task_id).first()
        if task is None:
            raise NoResultFound("Task not found")

        db.delete(task)
        db.commit()
        return task

    @classmethod
    def get_tasks_by_owner(cls, db: Session, owner_id: int) -> list['Task']:
        """Получает все задачи определенного пользователя.
        
        Возвращает список задач.
        """
        tasks = db.query(cls).filter(cls.owner_id == owner_id).all()
        return tasks