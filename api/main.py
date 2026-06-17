"""
FastAPI application for serving house price prediction model
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import joblib
from pathlib import Path


app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices",
    version="1.0.0"
)


def get_latest_model_path() -> Path:
    """
    Find the most recently trained model file in the models/ directory.
    Filenames are timestamped (house_price_model_YYYYMMDD_HHMMSS.pkl),
    so sorting alphabetically also sorts them by training time.
    """
    models_dir = Path(__file__).parent.parent / "models"
    model_files = sorted(models_dir.glob("house_price_model_*.pkl"))
    return model_files[-1] if model_files else None


class HouseFeatures(BaseModel):
    """Input schema for house features"""
    features: List[float]
    
    class Config:
        schema_extra = {
            "example": {
                "features": [1, 2, 3, 4, 5]
            }
        }


class PredictionResponse(BaseModel):
    """Output schema for predictions"""
    prediction: float
    model_used: str = None
    confidence: float = None


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to House Price Prediction API"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(house: HouseFeatures):
    """
    Predict house price using the latest trained model

    Args:
        house (HouseFeatures): House features

    Returns:
        PredictionResponse: Predicted price
    """
    try:
        model_path = get_latest_model_path()

        if model_path is None:
            raise HTTPException(
                status_code=500,
                detail="Không tìm thấy model đã train. Hãy chạy 'py main.py' trước."
            )

        model = joblib.load(model_path)

        # Make prediction
        X = np.array(house.features).reshape(1, -1)
        prediction = model.predict(X)[0]

        return PredictionResponse(prediction=float(prediction), model_used=model_path.name)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
