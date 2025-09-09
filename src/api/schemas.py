from pydantic import BaseModel, Field
from typing import List, Optional

class PredictIn(BaseModel):
    headline: Optional[str] = Field(None, max_length=300)
    body: Optional[str] = Field(None, max_length=10000)

class PredictOut(BaseModel):
    label: str
    proba: float
    top_features: List[str]

class FeedbackIn(BaseModel):
    headline: Optional[str] = None
    body: Optional[str] = None
    predicted: str
    correct_label: str
