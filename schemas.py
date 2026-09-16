from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class BudgetLevel(str, Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"

class Interest(str, Enum):
    CULTURE = "culture"
    NATURE = "nature"
    FOODIE = "foodie"
    RELAXATION = "relaxation"
    ADVENTURE = "adventure"
    SHOPPING = "shopping"

class Activity(BaseModel):
    time_slot: str = Field(description="Morning, Afternoon, or Evening")
    location_name: str = Field(description="Name of the venue or location")
    description: str = Field(description="Detailed overview of what to do, see, and experience at this spot")
    transport_mode: str = Field(description="Best transport option to get to/from here, e.g., 'Flight / Taxi', 'Local Bus', 'Metro', 'Auto Rickshaw', 'Walking'")
    estimated_cost: str = Field(description="Estimated cost for this activity")

class DayPlan(BaseModel):
    day_number: int = Field(description="The sequential day number starting at 1")
    theme: str = Field(description="Main theme or highlight for the day")
    activities: List[Activity] = Field(description="List of planned activities")

class ItineraryRequest(BaseModel):
    destination: str
    duration_days: int
    travelers_count: int
    budget: BudgetLevel
    interests: List[Interest]
    must_see_spots: Optional[List[str]] = None
    
class WeatherInfo(BaseModel):
    expected_temp_range: str = Field(description="Expected temperature range for the destination")
    climate_summary: str = Field(description="Brief summary of the weather/climate")
    clothing_advice: str = Field(description="Packing and clothing recommendations based on weather")
    
class ItineraryResponse(BaseModel):
    destination: str
    duration_days: int
    estimated_cost: str
    days: List[DayPlan]
    weather_forecast: Optional[WeatherInfo] = Field(default=None, description="Weather forecast and clothing recommendations")
