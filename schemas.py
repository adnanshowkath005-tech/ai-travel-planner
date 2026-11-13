from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class BudgetLevel(str, Enum):
    budget = "budget"
    moderate = "moderate"
    luxury = "luxury"

class ItineraryRequest(BaseModel):
    destination: str
    duration_days: int
    travelers: int
    budget_level: BudgetLevel
    interests: List[str]
    must_see_locations: Optional[str] = None
    transport_mode: str = "Flight"

class Activity(BaseModel):
    time_slot: str
    activity_name: str
    description: str
    estimated_cost: Optional[str] = None
    transport_mode: Optional[str] = None

class DayItinerary(BaseModel):
    day_number: int
    theme: str
    activities: List[Activity]

class ItineraryResponse(BaseModel):
    destination: str
    duration_days: int
    travelers: int
    overview: str
    days: List[DayItinerary]

class PackingListResponse(BaseModel):
    clothing: List[str] = Field(default_factory=list)
    toiletries: List[str] = Field(default_factory=list)
    electronics: List[str] = Field(default_factory=list)
    documents_and_money: List[str] = Field(default_factory=list)
    transport_specific_gear: List[str] = Field(default_factory=list)
    extras: List[str] = Field(default_factory=list)