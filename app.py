import os
import streamlit as st
from generator import generate_itinerary
from schemas import ItineraryRequest, BudgetLevel
from pdf_generator import create_itinerary_pdf

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
elif "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.markdown("""
<style>
    .transport-badge {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("✈️ AI Travel Planner")
st.markdown("Generate a personalized travel itinerary powered by AI.")

with st.sidebar:
    st.header("Trip Details")
    destination = st.text_input("Destination", "Thiruvananthapuram, Kerala, India")
    duration = st.number_input("Duration (days)", min_value=1, max_value=14, value=3)
    travelers = st.number_input("Travelers", min_value=1, max_value=10, value=2)
    budget_level = st.selectbox("Budget Level", ["budget", "moderate", "luxury"], index=0)
    
    interests_input = st.multiselect(
        "Interests", 
        ["culture", "nature", "food", "adventure", "history", "relaxation"], 
        default=["culture", "nature"]
    )
    must_see = st.text_area("Must-See Locations (optional)")
    
    generate_btn = st.button("✨ Generate Itinerary", type="primary", use_container_width=True)

if generate_btn:
    with st.spinner("Generating your custom itinerary..."):
        try:
            request_data = ItineraryRequest(
                destination=destination,
                duration_days=duration,
                travelers=travelers,
                budget_level=BudgetLevel(budget_level),
                interests=interests_input,
                must_see_locations=must_see if must_see else None
            )
            itinerary = generate_itinerary(request_data)
            st.session_state["itinerary"] = itinerary
            st.session_state["destination"] = destination
        except Exception as e:
            st.error(f"Error generating itinerary: {e}")

if "itinerary" in st.session_state:
    itinerary = st.session_state["itinerary"]
    destination = st.session_state.get("destination", destination)
    
    st.header(f"Trip to {destination}")
    st.write(f"**Duration:** {itinerary.duration_days} Days | **Travelers:** {itinerary.travelers} | **Budget:** {itinerary.budget_level.value.capitalize()}")
    
    if hasattr(itinerary, 'estimated_cost') and itinerary.estimated_cost:
        st.caption(f"Estimated Total Cost: {itinerary.estimated_cost}")
        
    st.divider()

    day_tabs = st.tabs([f"Day {day.day_number}" for day in itinerary.days])
    for tab, day in zip(day_tabs, itinerary.days):
        with tab:
            st.subheader(f"Day {day.day_number}: {getattr(day, 'theme', '')}")
            for activity in day.activities:
                with st.expander(f"🕒 {activity.time_slot} - {activity.location_name}", expanded=True):
                    if hasattr(activity, 'transport_mode') and activity.transport_mode:
                        st.markdown(f'<div class="transport-badge">🚆 Mode of Transport: {activity.transport_mode}</div>', unsafe_allow_html=True)
                    st.write(activity.description)
                    if hasattr(activity, 'estimated_cost') and activity.estimated_cost:
                        st.caption(f"Estimated Cost: {activity.estimated_cost}")

    st.divider()

    pdf_data = create_itinerary_pdf(itinerary)
    st.download_button(
        label="📥 Download Itinerary (PDF)",
        data=pdf_data,
        file_name=f"{destination.lower().replace(' ', '_')}_itinerary.pdf",
        mime="application/pdf"
    )
