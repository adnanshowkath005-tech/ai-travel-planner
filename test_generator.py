from dotenv import load_dotenv

# Ensure .env is loaded before importing modules that need it
load_dotenv()

from schemas import ItineraryRequests
from generator import generate_itinerary

request = ItineraryRequest(
    destination="Tokyo, Japan",
    duration_days=2,
    budget="moderate",
    interests=["culture", "foodie"],
    travelers_count=2,
    must_see_spots=["Senso-ji"]
)

print("Generating itinerary... please wait.")
result = generate_itinerary(request)
print("\n--- Generated Itinerary ---")
print(result.model_dump_json(indent=2))