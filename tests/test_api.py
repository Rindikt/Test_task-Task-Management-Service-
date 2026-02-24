import pytest
from core.models.tasks import Status


@pytest.mark.asyncio
async def test_create_task_api(client):
    """Проверка создания задачи через API."""
    payload = {"title": "Test Task"}
    response = await client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == payload['title']
    assert data["status"] == "new"
    assert "id" in data

@pytest.mark.asyncio
async def test_filter_tasks_by_status(client):
    """Тест фильтрации."""
    await client.post("/tasks/", json={"title": "Task to filter"})
    response = await client.get("/tasks/", params={"status": "new"})
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) > 0
    assert all(task["status"] == "new" for task in items)

@pytest.mark.asyncio
async def test_create_task_invalid_data(client):
    """Проверка, что пустые данные не пройдут."""
    response = await client.post("/tasks/", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_pagination_invalid_page(client):
    """Проверка валидации номера страницы."""
    response = await client.get("/tasks/", params={"page": 0})
    assert response.status_code == 422

