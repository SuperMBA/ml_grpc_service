# ml_grpc_service

gRPC-сервис для инференса простой ML-модели.

## Описание

Реализован сервис `mlservice.v1.PredictionService` с методами:

- `Health` — проверка здоровья сервиса и версии модели.
- `Predict` — получение предсказания и вероятности (confidence).

Контракт описан в `protos/model.proto`.

## Структура проекта

- `protos/` — model.proto, сгенерированные model_pb2.py, model_pb2_grpc.py  
- `server/` — реализация gRPC-сервера (`server.py`)  
- `client/` — Python-клиент для локального тестирования (`client.py`)  
- `models/` — сериализованная модель (`model.pkl`)  
- `Dockerfile` — сборка контейнера  
- `requirements.txt` — зависимости

## Локальный запуск

```bash
pip install -r requirements.txt
MODEL_PATH=models/model.pkl MODEL_VERSION=v1.0.0 python -m server.server
```












