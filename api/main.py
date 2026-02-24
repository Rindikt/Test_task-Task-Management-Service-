from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.db import async_engine, Base
from api.routers.tasks import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


app = FastAPI(
    title="Task Runner API",
    lifespan=lifespan
)
app.include_router(router)