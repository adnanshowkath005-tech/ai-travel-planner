import os
import json
from google import generativeai as genai
from schemas import ItineraryRequest, ItineraryResponse, PackingListResponse

# Configure Gemini API key
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.6-flash")

def get_mock_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    # Destination-specific day themes & activities for realistic offline mock mode
    dest = request.destination
    days_data = []
    
    themes = [
        f"Arrival & Historic Landmarks of {dest}",
        f"Cultural Heritage & Local Markets",
        f"Scenic Nature & Adventure Exploration",
        f"Hidden Gems & Local Culinary Tour",
        f"Relaxation & Souvenir Shopping"
    ]
    
    morning_activities = [
        ("Morning Heritage Tour", f"Explore the iconic historical sites and monuments of {dest}.", "₹800"),
        ("Local Breakfast & Market Walk", "Experience authentic regional cuisine and browse traditional crafts.", "₹500"),
        ("Scenic Viewpoint Trek", f"Enjoy breathtaking panoramic views of nature around {dest}.", "₹400"),
        ("Museum & Art Gallery Visit", "Discover the rich history, art, and heritage artifacts.", "₹600"),
        ("Riverside or Coastal Stroll", "Unwind with a peaceful morning walk by the local waterfront.", "₹300")
    ]
    
    afternoon_activities = [
        ("Afternoon Sightseeing & Gardens", f"Visit prominent botanical gardens and landmarks in {dest}.", "₹1,000"),
        ("Traditional Lunch & Craft Workshop", "Savor a local thali/specialty meal followed by an interactive workshop.", "₹1,200"),
        ("Adventure Activity / Excursion", f"Engage in thrilling outdoor experiences tailored to {dest}.", "₹1,500"),
        ("Architectural Wonder Tour", "Marvel at ancient carvings, palaces, or modern architectural marvels.", "₹900"),
        ("Café Hopping & Leisure", "Relax at popular local cafes and explore artisanal boutiques.", "₹700")
    ]
    
    for i in range(request.duration_days):
        theme_idx = i % len(themes)
        m_act = morning_activities[i % len(morning_activities)]
        a_act = afternoon_activities[i % len(afternoon_activities)]
        
        days_data.append({
            "day_number": i + 1,
            "theme": themes[theme_idx],
            "activities": [
                {
                    "time_slot": "Morning",
                    "activity_name": m_act[0],
                    "description": m_act[1],
                    "estimated_cost": m_act[2],
                    "transport_mode": request.transport_mode
                },
                {
                    "time_slot": "Afternoon",
                    "activity_name": a_act[0],
                    "description": a_act[1],
                    "estimated_cost": a_act[2],
                    "transport_mode": request.transport_mode
                }
            ]
        })

    return ItineraryResponse(
        destination=dest,
        duration_days=request.duration_days,
        travelers=request.travelers,
        overview=f"An amazing {request.duration_days}-day customized journey through {dest} for {request.travelers} traveler(s), crafted with unique daily experiences across your chosen interests ({', '.join(request.interests)}).",
        days=days_data
    )

def get_mock_packing_list(request: ItineraryRequest) -> PackingListResponse:
    return PackingListResponse(
        clothing=["Comfortable walking shoes", "Light breathable clothes", "Jacket or evening layer"],
        toiletries=["Sunscreen", "Toothbrush & toothpaste", "Personal medications"],
        electronics=["Phone & charger", "Power bank", "Universal adapter"],
        documents_and_money=["Government ID / Passport", "Credit cards / Cash", "Travel insurance docs"],
        transport_specific_gear=[f"Booking tickets for {request.transport_mode}", "Neck pillow / Eye mask"],
        extras=["Sunglasses", "Reusable water bottle"]
    )

def generate_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    try:
        prompt = f"""
        Create a detailed {request.duration_days}-day travel itinerary for {request.destination}.
        Travelers: {request.travelers}
        Budget Level: {request.budget_level.value}
        Interests: {', '.join(request.interests)}
        Must-see locations: {request.must_see_locations or 'None specified'}
        Preferred Transport Mode: {request.transport_mode}

        CRITICAL REQUIREMENT: Make sure every single day has unique, distinct themes and completely different activities suited specifically to {request.destination}. Do NOT repeat the same activities across days.

        Return the response strictly as valid JSON matching this schema structure:
        {{
          "destination": "{request.destination}",
          "duration_days": {request.duration_days},
          "travelers": {request.travelers},
          "overview": "A brief summary paragraph of the trip.",
          "days": [
            {{
              "day_number": 1,
              "theme": "Unique Day Theme",
              "activities": [
                {{
                  "time_slot": "Morning",
                  "activity_name": "Specific Activity Name",
                  "description": "Detailed description of the activity.",
                  "estimated_cost": "₹500",
                  "transport_mode": "{request.transport_mode}"
                }}
              ]
            }}
          ]
        }}
        """
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        return ItineraryResponse(**data)
        
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Rate limit reached. Falling back to diverse mock itinerary data.")
            return get_mock_itinerary(request)
        raise e


def generate_packing_list(request: ItineraryRequest) -> PackingListResponse:
    try:
        prompt = f"""
        Create a comprehensive smart packing list for a {request.duration_days}-day trip to {request.destination} 
        with a {request.budget_level.value} budget, focusing on interests like {', '.join(request.interests)}.
        Transport mode: {request.transport_mode}.

        Return the response strictly as valid JSON matching this schema:
        {{
          "clothing": ["Item 1", "Item 2"],
          "toiletries": ["Item 1", "Item 2"],
          "electronics": ["Item 1", "Item 2"],
          "documents_and_money": ["Item 1", "Item 2"],
          "transport_specific_gear": ["Item 1", "Item 2"],
          "extras": ["Item 1", "Item 2"]
        }}
        """
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        return PackingListResponse(**data)
        
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Rate limit reached. Falling back to mock packing list data.")
            return get_mock_packing_list(request)
        raise e