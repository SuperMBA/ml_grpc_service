# gRPC ML Inference Service

## Project Overview

This project demonstrates a containerized gRPC service for machine learning model inference.

The service exposes a versioned prediction API based on a Protocol Buffers contract and includes both a gRPC server and a Python client for local testing. The project focuses on practical ML engineering concepts such as API contracts, service health checks, model versioning, inference endpoints and Docker-based deployment.

## Key Features

* gRPC service for ML model inference
* Protocol Buffers API contract
* Health check endpoint
* Prediction endpoint with confidence score
* Python client for local testing
* Serialized ML model artifact
* Dockerized service
* Local testing with `grpcurl`

## Service API

The service implements:

```text
mlservice.v1.PredictionService
```

The service provides two methods:

### `Health`

Checks whether the service is running and returns model version information.

### `Predict`

Returns a model prediction and confidence score for the input data.

The API contract is defined in:

```text
protos/model.proto
```

## Repository Structure

```text
ml_grpc_service/
├── protos/
│   ├── model.proto              # Protobuf service contract
│   ├── model_pb2.py             # Generated protobuf Python classes
│   └── model_pb2_grpc.py        # Generated gRPC service classes
├── server/
│   └── server.py                # gRPC server implementation
├── client/
│   └── client.py                # Python client for local testing
├── models/
│   └── model.pkl                # Serialized ML model
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Local Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the gRPC server:

```bash
MODEL_PATH=models/model.pkl MODEL_VERSION=v1.0.0 python -m server.server
```

In another terminal, run the Python client:

```bash
python -m client.client
```

## Docker Run

Build the Docker image:

```bash
docker build -t grpc-ml-service .
```

Run the container:

```bash
docker run -p 50051:50051 grpc-ml-service
```

The service will be available on:

```text
localhost:50051
```

## Health Check

The health endpoint can be tested with `grpcurl`:

```bash
grpcurl -plaintext -proto protos/model.proto localhost:50051 mlservice.v1.PredictionService.Health
```

## Prediction Request

The prediction endpoint can be tested with the Python client:

```bash
python -m client.client
```

The response includes:

* predicted class or value;
* confidence score;
* model version information.

## Screenshots

The screenshots below show local service execution and gRPC endpoint testing.

<img width="974" height="582" alt="gRPC service screenshot" src="https://github.com/user-attachments/assets/b304fc88-05bf-4812-8aef-763ab57ded50" />

<img width="974" height="582" alt="gRPC client test screenshot" src="https://github.com/user-attachments/assets/3dbf1b42-a93b-4e6a-ae2b-d655ee2e51ad" />

## Tech Stack

* Python
* gRPC
* Protocol Buffers
* scikit-learn
* Docker
* grpcurl
* ML model inference
* API contract design

## ML Engineering Concepts Demonstrated

This project demonstrates several practical ML engineering concepts:

* serving ML models through a gRPC API;
* defining a strict service contract with Protocol Buffers;
* separating server and client logic;
* exposing health and prediction endpoints;
* returning prediction confidence;
* managing model path and model version through environment variables;
* containerizing an inference service with Docker.

## Relevance

gRPC is commonly used for efficient service-to-service communication in production systems. This project demonstrates how an ML model can be wrapped into a structured inference service with a clear API contract.

The same approach can be extended to larger ML systems, including healthcare analytics, Medical AI services and production-oriented model serving pipelines.

## Author

**Margarita Balandina**
Medical Data Scientist | Dentist with German Approbation | MSc Data Science

Focus areas: Medical AI, Healthcare Analytics, Clinical Data, Machine Learning, MedTech and ML Engineering.
