import logging
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.tasks import Status
from core.redis_client import redis_client
from core.repositories.task_repository import TaskRepository
from core.schemas.tasks import TaskCreateSchema, TaskListResponse
from core.config import settings

logger = logging.getLogger(__name__)

class TaskService:
    """
        Сервис для управления бизнес-логикой задач.
        Связывает API с репозиторием и в дальнейшем с очередью Redis.
    """

    def __init__(self, db: AsyncSession):
        self.repo = TaskRepository(db)

    async def create_task(self, task_data: TaskCreateSchema):
        """
            Регистрирует новую задачу и отправляет её в очередь.
        """

        try:
            title = task_data.title
            task = await self.repo.create(title=title)
            await redis_client.lpush(settings.TASK_QUEUE, str(task.id))
            return task
        except SQLAlchemyError:
            logger.exception("Ошибка базы данных при создании задачи.")
            raise HTTPException(status_code=500, detail="Ошибка при создании задачи в базе данных")

    async def get_task_by_id(self, task_id: int):
        """
            Возвращает задачу по ID или бросает 404.
        """

        task = await self.repo.get_by_id(task_id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Задача с id {task_id} не найдена")
        return task

    async def get_tasks_list(self, status: Status | None, page: int, limit: int):
        """
        Формирует пагинированный ответ со списком задач.
        """

        offset = (page - 1) * limit
        try:
            items, total = await self.repo.get_list(status=status, offset=offset, limit=limit)

            return {
                'items': items,
                'total': total,
                'page': page,
                'limit': limit
            }
        except Exception as e:
            logger.error(f'Неожиданная ошибка в функции get_tasks_list: {e}')
            raise HTTPException(status_code=500, detail='Ошибка при получении списка задач')
