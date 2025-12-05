import os
import pickle
from concurrent import futures

import grpc

from protos import model_pb2, model_pb2_grpc


# Порт и версия модели из переменных окружения
PORT = int(os.environ.get("PORT", 50051))
MODEL_VERSION = os.environ.get("MODEL_VERSION", "v0.0.1")

# Путь к модели из окружения или по умолчанию: ../models/model.pkl
DEFAULT_MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
)
MODEL_PATH = os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH)


class PredictionServiceServicer(model_pb2_grpc.PredictionServiceServicer):
    """
    Реализация методов gRPC-сервиса PredictionService.
    """

    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        """
        Загрузка модели из MODEL_PATH.
        """
        try:
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            print(f"[SERVER] Model loaded from {MODEL_PATH}")
        except Exception as e:
            print(f"[SERVER] Failed to load model from {MODEL_PATH}: {e}")
            self.model = None

    def Health(self, request, context):
        """
        Реализация /health.
        """
        status = "ok" if self.model is not None else "model_not_loaded"
        return model_pb2.HealthResponse(
            status=status,
            modelVersion=MODEL_VERSION,
        )

    def Predict(self, request, context):
        """
        Реализация /predict.

        Используем загруженную модель:
        - features из запроса
        - model.predict_proba(features) -> confidence
        - prediction = "1" если confidence >= 0.5, иначе "0"
        """
        if self.model is None:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details("Model is not loaded")
            return model_pb2.PredictResponse()

        features = list(request.features)

        try:
            prob = float(self.model.predict_proba(features))
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Prediction failed: {e}")
            return model_pb2.PredictResponse()

        prediction = "1" if prob >= 0.5 else "0"

        return model_pb2.PredictResponse(
            prediction=prediction,
            confidence=prob,
            modelVersion=MODEL_VERSION,
        )


def serve():
    """
    Запуск gRPC-сервера.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServiceServicer(),
        server,
    )
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"[SERVER] gRPC server started on port {PORT}")
    print(f"[SERVER] Model version: {MODEL_VERSION}")
    print(f"[SERVER] Model path: {MODEL_PATH}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
