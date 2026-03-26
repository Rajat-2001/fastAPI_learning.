from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse (BaseModel):
    predicted_category : str = Field (..., description="the predicted insurance premium category", example = "High")
    confidence : float = Field(..., description="Model's confidence score for the predicted class (range: 0 to 1)", example= 0.4543)
    class_probabilities : Dict = Field(..., description="Probability distribution across all possible classes", example={'low': 0.01, 'Medium': 0.15, "high": 0.84})
    