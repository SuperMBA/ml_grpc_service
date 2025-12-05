FROM python:3.11-slim

# Переменные окружения
ENV PORT=50051 \
    MODEL_PATH=/app/models/model.pkl \
    MODEL_VERSION=v1.0.0

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Открываем порт gRPC
EXPOSE 50051

# Команда запуска сервера
CMD ["python", "-m", "server.server"]
