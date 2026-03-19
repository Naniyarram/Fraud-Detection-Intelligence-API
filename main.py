from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from datetime import datetime
from groq import Groq
import json
import os



client = Groq(api_key=os.getenv("GROQ_API_KEY"))


app = FastAPI(
    title="Fraud Detection Intelligence API",
    description="Machine Learning fraud detection with LLM-based explanation",
    version="1.0"
)



model = joblib.load("pipeline.pkl")



class Transaction(BaseModel):
    step: int = Field(..., example=1)
    type: str = Field(..., example="TRANSFER")
    amount: float = Field(..., example=9839.64)

    oldbalanceOrg: float = Field(..., example=170136)
    newbalanceOrig: float = Field(..., example=160296.36)

    oldbalanceDest: float = Field(..., example=0)
    newbalanceDest: float = Field(..., example=0)


class Prediction(BaseModel):
    label: str
    class_: int

class RiskAnalysis(BaseModel):
    fraud_probability: float
    risk_percentage: float
    risk_level: str

class TransactionSummary(BaseModel):
    type: str
    amount: float

class ModelInfo(BaseModel):
    model: str
    version: str

class FraudResponse(BaseModel):
    prediction: Prediction
    risk_analysis: RiskAnalysis
    transaction_summary: TransactionSummary
    model_info: ModelInfo
    timestamp: str
    llm_explanation: list



def get_risk_level(risk):
    if risk < 30:
        return "Low Risk"
    elif risk < 70:
        return "Medium Risk"
    else:
        return "High Risk"


def fraud_predict(df):
    proba = model.predict_proba(df)[0][1]

    prediction = 1 if proba >= 0.5 else 0
    label = "Fraudulent Transaction" if prediction == 1 else "Legitimate Transaction"
    risk = round(proba * 100, 2)

    return prediction, label, proba, risk


def extract_signals(tx):

    origin_change = tx["oldbalanceOrg"] - tx["newbalanceOrig"]
    dest_change = tx["newbalanceDest"] - tx["oldbalanceDest"]

    origin_ratio = tx["amount"] / (tx["oldbalanceOrg"] + 1)
    dest_ratio = tx["amount"] / (tx["oldbalanceDest"] + 1)

    return {
        "transaction_type": tx["type"],
        "amount": tx["amount"],
        "origin_balance_change": origin_change,
        "destination_balance_change": dest_change,
        "origin_balance_ratio": round(origin_ratio, 4),
        "destination_balance_ratio": round(dest_ratio, 4)
    }



def generate_llm_explanation(transaction, label, probability, risk_level):

    signals = extract_signals(transaction)

    prompt = f"""
    You are explaining a fraud detection prediction.

    Facts:
    transaction_type: {signals['transaction_type']}
    amount: {signals['amount']}
    origin_balance_change: {signals['origin_balance_change']}
    destination_balance_change: {signals['destination_balance_change']}
    origin_balance_ratio: {signals['origin_balance_ratio']}
    destination_balance_ratio: {signals['destination_balance_ratio']}
    fraud_probability: {round(probability,4)}
    risk_level: {risk_level}
    prediction: {label}

    Rules:
    - Use only these facts
    - Do not invent thresholds or averages
    - Do not assume historical behavior
    - Produce exactly 3 bullet points explaining the decision
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=120
    )

    text = completion.choices[0].message.content

    explanation = [
        line.strip("- ").strip()
        for line in text.split("\n")
        if line.strip().startswith("-")
    ]


    if len(explanation) != 3:
        explanation = [
            f"Origin account balance decreased by {signals['origin_balance_change']} indicating funds were transferred out.",
            f"Destination balance change recorded as {signals['destination_balance_change']} for this transaction.",
            f"The model estimated fraud probability {round(probability,4)} leading to a {risk_level} classification."
        ]

    return explanation


@app.get("/")
def home():
    return {
        "message": "Fraud Detection Intelligence API is running",
        "model": "ML Fraud Detection + LLM Explanation"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/model-info")
def model_info():
    return {
        "model": "Fraud Detection Pipeline",
        "version": "1.0",
        "features": [
            "step",
            "type",
            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest"
        ]
    }




@app.post("/predict", response_model=FraudResponse)
def predict(data: Transaction):

    df = pd.DataFrame([data.dict()])

    prediction, label, probability, risk = fraud_predict(df)

    transaction_data = df.to_dict(orient="records")[0]

    risk_level = get_risk_level(risk)

    explanation = generate_llm_explanation(
        transaction_data,
        label,
        probability,
        risk_level
    )

    return {

        "prediction": {
            "label": label,
            "class_": prediction
        },

        "risk_analysis": {
            "fraud_probability": round(probability, 4),
            "risk_percentage": risk,
            "risk_level": risk_level
        },

        "transaction_summary": {
            "type": data.type,
            "amount": data.amount
        },

        "model_info": {
            "model": "Fraud Detection Pipeline",
            "version": "1.0"
        },

        "timestamp": datetime.utcnow().isoformat() + "Z",

        "llm_explanation": explanation
    }