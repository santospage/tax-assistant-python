from pydantic import BaseModel
from typing import List


class TaxPredictionRequest(BaseModel):
    customerType: str
    productType: str


class TaxPredictionResponse(BaseModel):
    taxCode: str
    descriptionTax: str
    taxAliquot: float
    probability: float
    level: str
