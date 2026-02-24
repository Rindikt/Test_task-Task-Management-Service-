import asyncio
import logging

from core.db import async_session_maker
from core.models.tasks import Task, Status
from core.redis_client import redis_client
from core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Worker")

async def work():
    """Основной цикл воркера."""
    logger.info("Воркер успешно запущен и мониторит очередь...")

    while True:
        try:
            result = await redis_client.brpop([settings.TASK_QUEUE], timeout=0)
            task_id = int(result[1])
            logger.info(f'Задача {task_id} взята в работу')

            async with async_session_maker() as session:

                db_task = await session.get(Task, task_id)

                if not db_task:
                    logger.warning(f'Задача {task_id} не найдена в БД')
                    continue

                db_task.status = Status.PROCESSING
                await session.commit()
                await session.refresh(db_task)
                logger.info(f'Статус задачи {task_id} изменен на {Status.PROCESSING}')

                await asyncio.sleep(3)

                title_length = len(db_task.title)

                if title_length % 2 != 0:
                    db_task.status = Status.FAILED
                    db_task.result = 'error'
                    logger.info(f'Задача {task_id}: длина {title_length} (нечёт) -> FAILED')
                else:
                    db_task.status = Status.DONE
                    db_task.result = 'success'
                    logger.info(f'Задача {task_id}: длина {title_length} (чёт) -> DONE')

                await session.commit()
        except Exception as e:
            logger.error(f"Ошибка воркера: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(work())



