FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir uv \
    && uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8000