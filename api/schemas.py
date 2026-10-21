from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    model: str

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

class PredictResponse(BaseModel):
    label: Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
    score: float