# Fraud Detection Intelligence API

A production-style **fraud detection inference API** built using **FastAPI**, integrating a trained **Machine Learning pipeline** with **LLM-powered explainable AI**.

The system analyzes financial transactions, predicts the probability of fraud, assigns a risk level, and generates human-readable explanations for each prediction.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Capabilities](#key-capabilities)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Endpoint](#api-endpoint)
- [Installation & Setup](#installation--setup)
- [Running with Docker](#running-with-docker)
- [API Examples](#api-examples)
- [Use Cases](#use-cases)
- [Learning Outcomes](#learning-outcomes)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Fraud Detection Intelligence API** is a machine learning-powered system designed to detect suspicious financial transactions and provide interpretable explanations for predictions.

The API demonstrates how to build a **complete ML inference service**, combining predictive modeling, risk scoring, explainable AI, and containerized deployment.

### Key Capabilities

- **Real-time Fraud Detection**: Predicts fraudulent transactions using a trained ML pipeline
- **Explainable AI**: Generates human-readable explanations using LLM integration (Groq/LLaMA)
- **Risk Scoring**: Provides probability-based risk classification (Low / Medium / High)
- **Structured API Responses**: Clean JSON responses designed for production systems
- **Containerized Deployment**: Easily deployable using Docker
- **Interactive API Documentation**: FastAPI Swagger UI for testing endpoints
- **Model Transparency**: Understand why transactions are flagged as suspicious

---

## Features

### 🔍 Core Features

- ✅ Real-time fraud prediction using machine learning
- ✅ Risk scoring based on fraud probability
- ✅ LLM-based explanation layer for model predictions
- ✅ Clean REST API built with FastAPI
- ✅ Docker containerization for reproducible deployment
- ✅ Structured JSON responses designed for production use
- ✅ Interactive Swagger UI for API exploration
- ✅ Comprehensive logging and error handling
- ✅ Production-ready error responses

### 🛡️ Security & Reliability

- Input validation and data sanitization
- Secure environment variable management
- Structured error handling
- Comprehensive API documentation
- Health check endpoint

---

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Transaction Input                       │
│              (Transaction Data JSON)                     │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│       FastAPI Endpoint: POST /predict                    │
│            Input Validation & Parsing                    │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│      Machine Learning Model                              │
│   (Fraud Detection Pipeline - Scikit-Learn)             │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│        Fraud Probability Calculation                     │
│         (0.0 - 1.0 Confidence Score)                    │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│      Risk Classification                                 │
│   Low (0-0.33) | Medium (0.33-0.67) | High (0.67-1.0)  │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│       Signal Extraction & Analysis                       │
│   (Balance Changes, Transaction Features)               │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│    LLM Explanation Layer                                 │
│    (Groq API - LLaMA Model)                             │
│  Generate Human-Readable Explanations                   │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│        Response Formatting                               │
│     Structured JSON Response                             │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│         API Response Delivered                           │
│  Comprehensive Fraud Assessment & Explanation           │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **ML Framework** | Scikit-Learn | Fraud detection model |
| **API Framework** | FastAPI | REST API endpoints |
| **Web Server** | Uvicorn | ASGI application server |
| **Data Processing** | Pandas | Data manipulation |
| **Model Serialization** | Joblib | Model persistence |
| **LLM Integration** | Groq (LLaMA) | Explainable AI |
| **Containerization** | Docker | Deployment |
| **API Docs** | Swagger UI | Interactive documentation |

---

## Project Structure

```
fraud-detection-api/
│
├── main.py                    # FastAPI application & ML inference logic
├── pipeline.pkl               # Trained fraud detection model
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container configuration
├── .dockerignore              # Excludes unnecessary files from Docker image
├── .env                       # Environment variables (API keys, config)
├── .env.example              # Example environment template
└── README.md                  # Project documentation
```

### File Descriptions

| File | Description |
|------|-------------|
| `main.py` | FastAPI application with all endpoints and ML inference logic |
| `pipeline.pkl` | Serialized trained ML model (Joblib format) |
| `requirements.txt` | Python package dependencies |
| `Dockerfile` | Container build configuration for deployment |
| `.dockerignore` | Prevents unnecessary files from entering Docker image |
| `.env` | Environment variables (API keys, configuration) |
| `.env.example` | Template for environment configuration |
| `README.md` | Complete project documentation |

---

## API Endpoint

### POST `/predict`

Predicts whether a financial transaction is fraudulent and provides risk assessment with LLM-generated explanation.

**URL**: `POST http://localhost:8000/predict`



**Headers**:
```
Content-Type: application/json
```
<img width="1920" height="1028" alt="Screenshot 2026-03-19 155349" src="https://github.com/user-attachments/assets/802c83f1-7aa5-4033-899a-763ee71ab079" />
---

## Example Request

```json
{
  "step": 1,
  "type": "PAYMENT",
  "amount": 11633.76,
  "oldbalanceOrg": 10127,
  "newbalanceOrig": 0,
  "oldbalanceDest": 0,
  "newbalanceDest": 0
}
```

**Request Parameters**:

| Field | Type | Description |
|-------|------|-------------|
| `step` | integer | Transaction step/sequence |
| `type` | string | Transaction type (PAYMENT, TRANSFER, etc.) |
| `amount` | float | Transaction amount |
| `oldbalanceOrg` | float | Origin account balance before transaction |
| `newbalanceOrig` | float | Origin account balance after transaction |
| `oldbalanceDest` | float | Destination account balance before transaction |
| `newbalanceDest` | float | Destination account balance after transaction |

---

## Example Response

```json
{
  "prediction": {
    "label": "Legitimate Transaction",
    "class_": 0
  },
  "risk_analysis": {
    "fraud_probability": 0.0644,
    "risk_percentage": 6.44,
    "risk_level": "Low Risk"
  },
  "transaction_summary": {
    "type": "PAYMENT",
    "amount": 11633.76
  },
  "model_info": {
    "model": "Fraud Detection Pipeline",
    "version": "1.0"
  },
  "timestamp": "2026-03-18T12:17:27.752442Z",
  "llm_explanation": [
    "Origin account balance decreased by 10127.0 indicating funds were transferred out.",
    "Destination balance change recorded as 0.0 for this transaction.",
    "The model estimated fraud probability 0.0644 leading to a Low Risk classification."
  ]
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `prediction.label` | string | Human-readable prediction (Legitimate / Fraudulent) |
| `prediction.class_` | integer | Class label (0=Legitimate, 1=Fraudulent) |
| `risk_analysis.fraud_probability` | float | Fraud probability (0.0-1.0) |
| `risk_analysis.risk_percentage` | float | Risk as percentage (0-100) |
| `risk_analysis.risk_level` | string | Risk classification (Low/Medium/High) |
| `transaction_summary` | object | Transaction details |
| `model_info` | object | Model metadata and version |
| `timestamp` | string | API response timestamp (ISO format) |
| `llm_explanation` | array | Human-readable explanation from LLM |

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Groq API key (for LLM integration)

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Naniyarram/Fraud-Detection-Intelligence-API.git
cd Fraud-Detection-Intelligence-API
```

#### 2. Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
MODEL_PATH=./pipeline.pkl
LOG_LEVEL=INFO
```

**To get a Groq API key**:
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Create an API key
4. Add it to your `.env` file

#### 5. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

#### 6. Access API Documentation

Open your browser and navigate to:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

You can test the API directly in the Swagger UI.

---

## Running with Docker

### Prerequisites

- Docker installed on your system

### Build Docker Image

```bash
docker build -t fraud-api .
```

### Run Docker Container

```bash
docker run --env-file .env -p 8000:8000 fraud-api
```

**Explanation**:
- `--env-file .env`: Loads environment variables from `.env`
- `-p 8000:8000`: Maps port 8000 from container to host
- `fraud-api`: Image name

### Access the API

Once the container is running, access the API at:

```
http://localhost:8000/docs
```

### Stop the Container

```bash
docker ps                    # Find container ID
docker stop <container_id>   # Stop the container
```

---

## API Examples And Output Screenshots


<img width="1920" height="1017" alt="Screenshot 2026-03-19 155525" src="https://github.com/user-attachments/assets/e47cf636-de10-44ce-b170-ae5c919643e3" />

<img width="1920" height="1017" alt="Screenshot 2026-03-19 155506" src="https://github.com/user-attachments/assets/0151a7b5-a6bc-4cce-b9e0-d8e130452c62" />



### Example 1: Testing with cURL

#### Legitimate Transaction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 1,
    "type": "PAYMENT",
    "amount": 11633.76,
    "oldbalanceOrg": 10127,
    "newbalanceOrig": 0,
    "oldbalanceDest": 0,
    "newbalanceDest": 0
  }'
```

**Expected Output**: Low Risk

#### Suspicious Transaction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 1,
    "type": "TRANSFER",
    "amount": 999999.99,
    "oldbalanceOrg": 1000,
    "newbalanceOrig": 0,
    "oldbalanceDest": 0,
    "newbalanceDest": 999999.99
  }'
```

**Expected Output**: High Risk

### Example 2: Testing with Python

```python
import requests
import json

# API endpoint
url = "http://localhost:8000/predict"

# Transaction data
transaction = {
    "step": 1,
    "type": "PAYMENT",
    "amount": 11633.76,
    "oldbalanceOrg": 10127,
    "newbalanceOrig": 0,
    "oldbalanceDest": 0,
    "newbalanceDest": 0
}

# Make request
response = requests.post(url, json=transaction)

# Check response
if response.status_code == 200:
    result = response.json()
    
    print("=== FRAUD DETECTION RESULT ===")
    print(f"Prediction: {result['prediction']['label']}")
    print(f"Fraud Probability: {result['risk_analysis']['fraud_probability']:.2%}")
    print(f"Risk Level: {result['risk_analysis']['risk_level']}")
    print("\n=== LLM EXPLANATION ===")
    for explanation in result['llm_explanation']:
        print(f"• {explanation}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### Example 3: Testing with Postman

1. Open Postman
2. Create a new POST request
3. URL: `http://localhost:8000/predict`
4. Set header: `Content-Type: application/json`
5. Body (raw JSON):
```json
{
  "step": 1,
  "type": "PAYMENT",
  "amount": 11633.76,
  "oldbalanceOrg": 10127,
  "newbalanceOrig": 0,
  "oldbalanceDest": 0,
  "newbalanceDest": 0
}
```
6. Click Send

---

## Use Cases

This system can be used in:

✅ **Banking Systems**: Real-time fraud detection for customer transactions

✅ **Payment Gateways**: Monitor and flag suspicious payment attempts

✅ **Financial Risk Analysis**: Assess transaction risk for compliance

✅ **Fraud Detection Pipelines**: Integrate into existing fraud prevention systems

✅ **Explainable AI Systems**: Demonstrate ML predictions with human-readable explanations

✅ **Regulatory Compliance**: Meet audit requirements with transparent decision-making

✅ **Financial Institutions**: Enterprise fraud prevention and monitoring

✅ **Educational Purposes**: Learn ML model deployment and API design

---

## Key Learning Outcomes

This project demonstrates practical experience in:

### Machine Learning & AI
- 🤖 Deploying trained ML models as production services
- 🧠 Integrating Large Language Models (LLMs) for explainability
- 📊 Building end-to-end ML inference pipelines

### API Development
- 🔌 Building production-ready REST APIs with FastAPI
- 📝 Designing structured API responses
- ✅ Implementing proper error handling and validation
- 📚 Creating comprehensive API documentation

### DevOps & Deployment
- 🐳 Containerizing ML applications using Docker
- 🚀 Building scalable inference architectures
- 🔧 Managing environment configurations
- 📦 Packaging applications for production

### Software Engineering Best Practices
- 🏗️ Designing clean, maintainable code
- 📖 Writing comprehensive documentation
- 🧪 Implementing error handling and logging
- 🔐 Managing sensitive configuration (API keys)

---

## Contributing

We welcome contributions! Please follow these guidelines:

### 1. Fork the Repository

```bash
git clone https://github.com/yourusername/Fraud-Detection-Intelligence-API.git
cd Fraud-Detection-Intelligence-API
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Follow PEP 8 style guidelines
- Add appropriate comments
- Test your changes

### 4. Commit Your Changes

```bash
git commit -m "Add: description of your changes"
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

- Provide a clear description of changes
- Reference any related issues
- Include examples if applicable

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

**MIT License allows**:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

**Conditions**:
- Include license and copyright notice
- State changes made to the code

---

## Support & Contact

For questions, issues, or suggestions:

- 📧 **Email**: naniyarram1@gmail.com
- 🐛 **GitHub Issues**: [Report Issues](https://github.com/Naniyarram/Fraud-Detection-Intelligence-API/issues)
- 💬 **GitHub Discussions**: [Join Discussion](https://github.com/Naniyarram/Fraud-Detection-Intelligence-API/discussions)

---

## Acknowledgments

### Technologies & Libraries
- **FastAPI**: Modern, fast web framework for building APIs
- **Scikit-Learn**: Machine learning toolkit for Python
- **Groq**: Advanced LLM API provider
- **Docker**: Containerization platform
- **Pandas**: Data manipulation and analysis
- **Joblib**: Model serialization

### Inspiration & Resources
- Financial fraud detection research
- Machine learning deployment best practices
- Open-source community contributions

