from google import genai
from google.genai import types
from schemas import ItineraryRequest, ItineraryResponse

client = genai.Client()
def generate_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    prompt = f"""
    You are an expert AI Travel Planner. Create a comprehensive, highly detailed day-by-day itinerary based on these preferences:
    - Destination: {request.destination}
    - Duration: {request.duration_days} days
    - Budget Level: {request.budget.value}
    - Interests: {', '.join([i if isinstance(i, str) else i.value for i in request.interests])}
    - Travelers: {request.travelers_count}
    - Must-see locations: {', '.join(request.must_see_spots) if request.must_see_spots else 'None'}

    STRICT CURRENCY RULES:
    1. If the destination is anywhere in India (e.g., Kerala, Goa, Maharashtra, Rajasthan, Karnataka, Thiruvananthapuram, etc.), display ALL budget estimates and itemized activity costs strictly in Indian Rupees (INR / ₹).
    2. For any destination outside of India, display ALL estimated costs strictly in US Dollars ($).

    DETAILED ACTIVITY & TRANSPORT REQUIREMENTS:
    - Provide rich, informative descriptions for each location detailing what to see, local tips, and highlights.
    - Specify the best mode of transport (e.g., Airplane, Taxi, Metro, Local Bus, Auto-Rickshaw, Ferry, Walking) to reach each activity and travel between spots.

    Ensure daily activities are logically clustered by proximity to minimize transit time.
    """

    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.6-flash"]

    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ItineraryResponse,
                    temperature=0.7,
                ),
            )
            return response.parsed
        except Exception as e:
            last_error = e
            print(f"Failed with model {model_name}: {e}")
            continue

    raise Exception(f"API Error details: {last_error}")
