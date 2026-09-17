from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class BudgetLevel(str, Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"

class ItineraryRequest(BaseModel):
    destination: str
    duration_days: int
    travelers: int
    budget_level: BudgetLevel
    interests: List[str]
    must_see_locations: Optional[str] = None
