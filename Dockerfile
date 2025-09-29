# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/
RUN pip install --no-cache-dir build && python -m build --sdist --wheel || true
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic sympy numpy python-dotenv httpx pytest

COPY api /app/api
COPY engines /app/engines
COPY services /app/services
COPY content /app/content

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
