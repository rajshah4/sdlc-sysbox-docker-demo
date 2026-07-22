FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/app

WORKDIR /app
COPY app ./app
RUN pip install --no-cache-dir \
    'fastapi>=0.116' \
    'httpx>=0.28' \
    'psycopg[binary]>=3.2' \
    'pytest>=8.0' \
    'redis>=6.2' \
    'uvicorn>=0.35'

EXPOSE 8000
CMD ["uvicorn", "petstore_app.api:app", "--host", "0.0.0.0", "--port", "8000"]
