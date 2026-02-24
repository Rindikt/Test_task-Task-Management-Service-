FROM python:3.11-slim

WORKDIR /app

# Отключаем кеш pip и .pyc файлы для экономии места
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

# По умолчанию запускаем API.
# Путь api.main:app, так как main лежит в папке api (судя по твоему скрину)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]