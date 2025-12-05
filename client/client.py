import os

import grpc

from protos import model_pb2, model_pb2_grpc


# Адрес сервера gRPC
GRPC_ADDRESS = os.environ.get("GRPC_ADDRESS", "localhost:50051")


def call_health():
    """
    Вызов /health
    """
    with grpc.insecure_channel(GRPC_ADDRESS) as channel:
        stub = model_pb2_grpc.PredictionServiceStub(channel)
        request = model_pb2.HealthRequest()
        response = stub.Health(request)
        print("Health response:")
        print(f"  status: {response.status}")
        print(f"  modelVersion: {response.modelVersion}")


def call_predict():
    """
    Вызов /predict с тестовыми данными.
    """
    # Пример фич — просто три числа
    features = [1.0, 2.0, 3.0]

    with grpc.insecure_channel(GRPC_ADDRESS) as channel:
        stub = model_pb2_grpc.PredictionServiceStub(channel)
        request = model_pb2.PredictRequest(features=features)
        response = stub.Predict(request)
        print("Predict response:")
        print(f"  prediction: {response.prediction}")
        print(f"  confidence: {response.confidence}")
        print(f"  modelVersion: {response.modelVersion}")


if __name__ == "__main__":
    print("=== /health ===")
    call_health()
    print("\n=== /predict ===")
    call_predict()
