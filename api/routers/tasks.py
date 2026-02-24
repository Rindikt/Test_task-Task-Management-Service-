from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.models.tasks import Status
from core.schemas.tasks import (
    TaskCreateSchema,
    TaskListResponse,
    TaskReadSchema,
)
from services.task_service import TaskService

router = APIRouter(
    tags=["tasks"],
    prefix="/tasks")


@router.post("/", status_code=201,
             summary="Создать новую задачу",
             description="Регистрирует задачу в базе и отправляет"
                         "ID в очередь Redis для обработки воркером."
             )
async def create_task(
        task: TaskCreateSchema,
        db: AsyncSession = Depends(get_db)):
    """Ручка для создания задачи."""
    task_service = TaskService(db)
    return await task_service.create_task(task)


@router.get("/{id}",
            response_model=TaskReadSchema,
            summary="Получить информацию о задаче",
            responses={404: {"description": "Задача не найдена"}}
            )
async def get_task(
        id: int,
        db: AsyncSession = Depends(get_db)):
    """Ручка для получения задачи по id."""

    task_service = TaskService(db)
    task = await task_service.get_task_by_id(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/",
            response_model=TaskListResponse,
            summary="Получить список задач",
            description=(
                    "Возвращает список всех задач с поддержкой фильтрации "
                    "по статусу и пагинации. По умолчанию возвращает первые 20 задач."
            ))
async def get_tasks(
                   status: Annotated[Optional[Status], Query()] = None,
                   page:int = Query(1, gt=0, description="Номер страницы"),
                   limit: int = Query(20, gt=0, le=100,
                                      description="Количество задач на одну страницу (макс. 100)"),
                   db: AsyncSession = Depends(get_db)):
    """Ручка для получения списка задачь по статусу."""
    task_service = TaskService(db)
    return await task_service.get_tasks_list(status=status, page=page, limit=limit)


