from pydantic import BaseModel
from typing import List, Optional


class TripCreate(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    currency: str = "INR"
    travelers: int = 1

    interests: List[str] = []

    preferences: Optional[str] = None

    hotel_name: Optional[str] = None
    hotel_location: Optional[str] = None