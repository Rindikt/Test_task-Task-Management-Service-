from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    REDIS_URL: str = Field('redis://redis:6379/0')
    DB_URL: str = Field('postgresql+asyncpg://postgres:postgres@db:5432/tasks_db')
    TASK_QUEUE: str = 'task_queue'

    PROJECT_NAME: str = 'Task Management Service'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()