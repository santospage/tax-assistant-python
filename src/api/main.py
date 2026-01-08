from fastapi import FastAPI, Body, Query
from typing import List

import pandas as pd

from src.api.schemas import (
    TaxPredictionRequest,
    TaxPredictionResponse
)
from src.ml.simple_tax_predictor import predict_taxes

app = FastAPI(title="Tax Assistant ML API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(
    payload: dict = Body(...),
    page: int = Query(0, ge=0),
    size: int = Query(10, gt=0)
):
    type_customer = payload.get("typeCustomer")
    type_product = payload.get("typeProduct")

    df = pd.read_csv("src/data/processed/tax_prediction.csv")

    filtered = df[
        (
            (df["typeCustomer"] == type_customer) |
            (df["typeCustomer"] == "__ANY__")
        ) &
        (
            (df["typeProduct"] == type_product) |
            (df["typeProduct"] == "__ANY__")
        )
    ]

    # ?? PAGINATION
    start = page * size
    end = start + size

    paged = filtered.iloc[start:end]

    return paged[[
        "taxCode",
        "descriptionTax",
        "taxAliquot",
        "probability",
        "level"
    ]].to_dict(orient="records")
