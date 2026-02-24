import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from core.models.tasks import Status


class BaseTaskSchema(BaseModel):
    title: str

class TaskCreateSchema(BaseTaskSchema):
    pass

class TaskReadSchema(BaseTaskSchema):
    id: int
    status: Status
    result: str | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    items: List[TaskReadSchema]
    total: int
    page: int
    limit: int

    model_config = ConfigDict(from_attributes=True)
