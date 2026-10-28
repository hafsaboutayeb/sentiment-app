from typing import Literal

from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    status: str
    model: str

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    @field_validator("text")
    @classmethod
    def reject_whitespace_only(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("le texte ne peut pas être vide ou composé d'espaces")
        return value


class PredictResponse(BaseModel):
    label: Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
    score: float