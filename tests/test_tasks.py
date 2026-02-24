import pytest
from core.models.tasks import Status, Task


@pytest.mark.asyncio
async def test_task_status_change_integration(client, db_session):
    """
        Тест смены статуса.
        Проверяем, что если в БД статус изменился (имитация работы воркера),
        API отдает корректное значение.
    """
    create_resp = await client.post("/tasks/", json={"title": "Integration Test"})
    task_id = create_resp.json()["id"]

    db_task = await db_session.get(Task, task_id)
    db_task.status = Status.DONE
    db_task.result = "success"
    await db_session.commit()

    response = await client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["result"] == "success"