"""
API request/response schemas
"""

from pydantic import BaseModel
from typing import Optional, List


class HousePredictionRequest(BaseModel):
    """Request schema for house price prediction (HCMC)"""
    area: float
    bedrooms: int
    bathrooms: int
    age: int
    district: str
    house_type: str
    legal_status: str
    
    class Config:
        schema_extra = {
            "example": {
                "area": 80,
                "bedrooms": 3,
                "bathrooms": 2,
                "age": 5,
                "district": "Quận 7",
                "house_type": "Nhà phố",
                "legal_status": "Sổ đỏ/Sổ hồng đầy đủ"
            }
        }


class HousePredictionResponse(BaseModel):
    """Response schema for house price prediction"""
    predicted_price_billion_vnd: float
    confidence_interval: Optional[tuple] = None
    model_version: str = "1.0"
