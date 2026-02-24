from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.tasks import Task, Status


class TaskRepository:
    """Репозиторий для управления объектами Task в базе данных."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str)->Task:
        """Создает новую задачу и сохраняет её в БД."""

        try:
            new_task = Task(title=title)
            self.db.add(new_task)
            await self.db.commit()
            await self.db.refresh(new_task)
            return new_task
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get_by_id(self, task_id: int)->Task|None:
        """Получает задачу по её уникальному идентификатору."""

        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        return task

    async def get_list(self, status: Status | None, limit: int, offset: int):
        """Возвращает список задач с фильтрацией и общее количество."""

        query = select(Task)
        if status:
            query = query.where(Task.status == status)
        count_tasks = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_tasks) or 0
        if total == 0:
            return [], 0

        items = (await self.db.scalars(query.offset(offset).limit(limit))).all()
        return items, total
