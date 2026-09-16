from schemas import ItineraryRequest

# Test valid input payload
sample_request = {
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": "moderate",
    "interests": ["culture", "foodie"],
    "travelers_count": 2,
    "must_see_spots": ["Shinjuku Gyoen", "Senso-ji"]
}

req = ItineraryRequest(**sample_request)
print("\n--- Successfully Validated Request Schema ---")
print(req.model_dump_json(indent=2))