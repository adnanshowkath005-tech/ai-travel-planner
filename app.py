import os
import streamlit as st
import streamlit.components.v1 as components
from generator import generate_itinerary, generate_packing_list
from schemas import ItineraryRequest, BudgetLevel
from pdf_generator import create_itinerary_pdf

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Key handling via secrets
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
elif "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# --- ULTRA-MODERN ANIMATED GLASSMORPHIC CSS THEME ---
st.markdown("""
<style>
    .stAppViewContainer, .stMain, .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 75%) !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid rgba(51, 65, 85, 0.6);
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    
    @keyframes slideUpFade {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes floatCard {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    div[data-testid="stVerticalBlock"] > div {
        animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .main-title {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0px;
    }

    .transport-badge {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.25), rgba(56, 189, 248, 0.15));
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        animation: floatCard 3.5s ease-in-out infinite;
    }
    
    .dest-desc {
        color: #94a3b8 !important;
        font-size: 0.9rem;
        min-height: 40px;
        margin-bottom: 12px;
        line-height: 1.4;
    }

    .dest-title {
        color: #f8fafc !important;
        font-weight: 700;
        font-size: 1.15rem;
        display: block;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(16px);
        padding: 16px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 20px 40px -10px rgba(2, 132, 199, 0.3);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
    }

    .stButton > button:hover {
        transform: scale(1.03) translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(2, 132, 199, 0.65) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">✈️ AI Travel Planner</p>', unsafe_allow_html=True)
st.markdown("Generate a personalized travel itinerary powered by AI or pick a featured destination below.")

if "destination" not in st.session_state:
    st.session_state["destination"] = "Goa"

if "active_day_tab" not in st.session_state:
    st.session_state["active_day_tab"] = 0

# --- SIDEBAR INPUTS & FULLY ANIMATED 3D MODEL ---
with st.sidebar:
    st.header("Trip Details")
    
    # Fully Animated 3D Model Widget with Action Playback Enabled
    fully_animated_model_html = """
    <div style="width: 100%; height: 200px; display: flex; justify-content: center; align-items: center; background: rgba(15, 23, 42, 0.7); border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.3); overflow: hidden; margin-bottom: 15px;">
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        <model-viewer id="animated-model"
                    src="https://modelviewer.dev/shared-assets/models/Astronaut.glb" 
                    alt="Fully Animated 3D Travel Assistant" 
                    auto-rotate 
                    camera-controls 
                    disable-zoom 
                    autoplay 
                    animation-name="*"
                    style="width: 100%; height: 100%; background-color: transparent;">
        </model-viewer>
    </div>
    """
    components.html(fully_animated_model_html, height=210)

    destination = st.text_input("Destination", value=st.session_state["destination"])
    st.session_state["destination"] = destination
    
    duration = st.number_input("Duration (days)", min_value=1, max_value=14, value=3)
    travelers = st.number_input("Travelers", min_value=1, max_value=10, value=2)
    budget_level = st.selectbox("Budget Level", ["budget", "moderate", "luxury"], index=0)
    
    transport_mode = st.selectbox(
        "Preferred Mode of Transport",
        ["Flight", "Train", "Bus", "Car / Road Trip", "Any / Mixed"],
        index=0
    )
    
    interests_input = st.multiselect(
        "Interests", 
        ["culture", "foodie", "nature", "adventure", "relaxation"], 
        default=["culture", "nature"]
    )
    must_see = st.text_area("Must-See Locations (optional)")
    
    generate_btn = st.button("✨ Generate Itinerary", type="primary", use_container_width=True)

# --- GENERATION LOGIC ---
if generate_btn:
    with st.spinner("✨ Crafting your custom itinerary & smart packing list with AI..."):
        try:
            request_data = ItineraryRequest(
                destination=destination,
                duration_days=duration,
                travelers=travelers,
                budget_level=BudgetLevel(budget_level),
                interests=interests_input,
                must_see_locations=must_see if must_see else None,
                transport_mode=transport_mode
            )
            itinerary = generate_itinerary(request_data)
            packing_list = generate_packing_list(request_data)
            
            st.session_state["itinerary"] = itinerary
            st.session_state["packing_list"] = packing_list
            st.session_state["current_dest"] = destination
            st.session_state["selected_budget"] = budget_level
            st.session_state["active_day_tab"] = 0
        except Exception as e:
            st.error(f"Error generating trip details: {e}")

# --- DESTINATIONS LIST ---
india_destinations = [
    {"name": "Tamil Nadu", "img": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=600&q=80", "desc": "Ancient Temples & Rich Heritage"},
    {"name": "Goa", "img": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600&q=80", "desc": "Sun-Kissed Beaches & Vibrant Nightlife"},
    {"name": "Telangana", "img": "images/telangana-state-.jpg", "desc": "Historic Monuments & Modern Tech Hub"},
    {"name": "Andhra Pradesh", "img": "images/andhra-pradesh.jpg", "desc": "Scenic Coastlines & Sacred Sites"},
    {"name": "Gujarat", "img": "images/gujarat.jpg", "desc": "Rich Culture, White Rann & Wildlife"},
    {"name": "Punjab", "img": "images/punjab.jpg", "desc": "Warm Hospitality & Golden Temple"},
    {"name": "Haryana", "img": "images/haryana.jpg", "desc": "Vibrant Culture & Heritage Sites"},
    {"name": "Uttar Pradesh", "img": "images/uttar-pradesh.jpg", "desc": "Home of the Taj Mahal & Spirituality"},
    {"name": "West Bengal", "img": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=600&q=80", "desc": "Art, Literature & Colonial Architecture"},
    {"name": "Odisha", "img": "images/odisha.jpg", "desc": "Magnificent Temples & Pristine Beaches"},
    {"name": "Madhya Pradesh", "img": "images/madhya-pradesh.jpg", "desc": "Wildlife Sanctuaries & Ancient Temples"},
    {"name": "Uttarakhand", "img": "images/uttarakhand.jpg", "desc": "The Land of Gods & Himalayan Views"},
    {"name": "Jammu & Kashmir", "img": "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&w=600&q=80", "desc": "Snowy Mountains & Scenic Valleys"},
    {"name": "Assam", "img": "images/assam.jpg", "desc": "Lush Tea Gardens & Wildlife Safari"},
]

outside_destinations = [
    {"name": "Saudi Arabia", "img": "images/saudi-arabia.jpg", "desc": "Ancient Heritage & Modern Wonders"},
    {"name": "Qatar", "img": "images/qatar.jpg", "desc": "Futuristic Skylines & Rich Traditions"},
    {"name": "Oman", "img": "images/oman.jpg", "desc": "Dramatic Mountains & Coastal Heritage"},
    {"name": "Bahrain", "img": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80", "desc": "Island Charm & Pearling History"},
    {"name": "Kuwait", "img": "images/kuwait.jpg", "desc": "Modern Skyline & Rich Arabian Culture"},
    {"name": "USA", "img": "https://images.unsplash.com/photo-1485738422979-f5c462d49f74?auto=format&fit=crop&w=600&q=80", "desc": "Iconic Cities & National Parks"},
    {"name": "UK", "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=600&q=80", "desc": "Royal Landmarks & Historic Towns"},
    {"name": "Canada", "img": "images/canada.jpg", "desc": "Stunning Wilderness & Vibrant Cities"},
    {"name": "Australia", "img": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=600&q=80", "desc": "Stunning Beaches & Unique Wildlife"},
    {"name": "Germany", "img": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?auto=format&fit=crop&w=600&q=80", "desc": "Fairytale Castles & Modern Cities"},
    {"name": "South Korea", "img": "images/south-korea.jpg", "desc": "Dynamic Seoul, Palaces & Scenic Beauty"},
    {"name": "Singapore", "img": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=600&q=80", "desc": "Garden City & Futuristic Skyline"},
    {"name": "Malaysia", "img": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=600&q=80", "desc": "Tropical Rainforests & Cityscapes"},
    {"name": "Thailand", "img": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?auto=format&fit=crop&w=600&q=80", "desc": "Golden Temples & Tropical Islands"},
    {"name": "Nepal", "img": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=600&q=80", "desc": "Himalayan Peaks & Ancient Stupas"},
    {"name": "UAE", "img": "images/uae.jpg", "desc": "Iconic Skylines & Luxury Desert Escapes"},
    {"name": "Pakistan", "img": "images/pakistan.jpg", "desc": "Majestic Peaks & Rich Cultural Heritage"},
    {"name": "Uzbekistan", "img": "images/uzbekistan.jpg", "desc": "Historic Silk Road Cities & Mosaics"},
    {"name": "Russia", "img": "images/russia.jpg", "desc": "Historic Architecture & Vast Landscapes"},
]

# --- HOME VIEW: DESTINATION CARDS ---
if "itinerary" not in st.session_state:
    st.markdown("---")
    st.subheader("🇮🇳 Explore Destinations Inside India")
    
    for i in range(0, len(india_destinations), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(india_destinations):
                dest = india_destinations[i + j]
                with cols[j]:
                    with st.container(border=True):
                        st.image(dest["img"], use_container_width=True)
                        st.markdown(f"<span class='dest-title'>{dest['name']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<div class='dest-desc'>{dest['desc']}</div>", unsafe_allow_html=True)
                        if st.button(f"Select {dest['name']}", key=f"ind_{i+j}", use_container_width=True):
                            st.session_state["destination"] = dest["name"]
                            if "itinerary" in st.session_state:
                                del st.session_state["itinerary"]
                            if "packing_list" in st.session_state:
                                del st.session_state["packing_list"]
                            st.rerun()

    st.markdown("---")
    st.subheader("🌍 Explore Destinations Outside India")
    
    for i in range(0, len(outside_destinations), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(outside_destinations):
                dest = outside_destinations[i + j]
                with cols[j]:
                    with st.container(border=True):
                        st.image(dest["img"], use_container_width=True)
                        st.markdown(f"<span class='dest-title'>{dest['name']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<div class='dest-desc'>{dest['desc']}</div>", unsafe_allow_html=True)
                        if st.button(f"Select {dest['name']}", key=f"out_{i+j}", use_container_width=True):
                            st.session_state["destination"] = dest["name"]
                            if "itinerary" in st.session_state:
                                del st.session_state["itinerary"]
                            if "packing_list" in st.session_state:
                                del st.session_state["packing_list"]
                            st.rerun()
                
    st.markdown("---")

# --- ITINERARY & PACKING LIST VIEW ---
if "itinerary" in st.session_state:
    
    if st.button("🔙 Back to All Destinations"):
        del st.session_state["itinerary"]
        if "packing_list" in st.session_state:
            del st.session_state["packing_list"]
        st.rerun()

    itinerary = st.session_state["itinerary"]
    current_destination = st.session_state.get("current_dest", destination)
    selected_budget_tier = st.session_state.get("selected_budget", "budget")
    
    dur = getattr(itinerary, 'duration_days', getattr(itinerary, 'duration', 3))
    trav = getattr(itinerary, 'travelers', getattr(itinerary, 'traveler_count', 2))
    
    cost_multipliers = {"budget": 3000, "moderate": 7500, "luxury": 20000}
    multiplier = cost_multipliers.get(selected_budget_tier, 5000)
    base_default_cost = float(dur * trav * multiplier)

    overview_text = getattr(itinerary, 'overview', f"Enjoy an incredible {dur}-day journey through {current_destination} tailored to your preferences.")

    st.markdown(f"""
        <div style="padding: 24px; border-radius: 16px; background: rgba(30, 41, 59, 0.75); backdrop-filter: blur(14px); margin-bottom: 25px; border: 1px solid rgba(56, 189, 248, 0.2); box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.5);">
            <h2 style="color: #f8fafc; margin-top: 0;">Trip Summary: {current_destination}</h2>
            <p style="color: #cbd5e1; font-size: 1.15rem; margin-top: 8px; line-height: 1.5;">{overview_text}</p>
            <hr style="border-color: rgba(255, 255, 255, 0.1); margin: 18px 0;">
            <p style="color: #94a3b8; font-size: 1rem; margin-top: 8px;">Duration: {dur} Days | Travelers: {trav} | Budget Tier: {str(selected_budget_tier).capitalize()}</p>
        </div>
    """, unsafe_allow_html=True)

    tab_itinerary, tab_packing, tab_expense = st.tabs([
        "📅 Daily Itinerary", 
        "🧳 Smart Packing List", 
        "💰 Expense Splitter"
    ])

    days_list = getattr(itinerary, 'days', getattr(itinerary, 'daily_itinerary', []))

    with tab_itinerary:
        if days_list:
            day_tab_titles = [f"Day {getattr(d, 'day_number', i+1)}" for i, d in enumerate(days_list)]
            day_tabs = st.tabs(day_tab_titles)
            
            for i, (tab, day) in enumerate(zip(day_tabs, days_list)):
                with tab:
                    st.session_state["active_day_tab"] = i
                    
                    day_num = getattr(day, 'day_number', i+1)
                    theme = getattr(day, 'theme', getattr(day, 'day_title', 'Exploration & Sights'))
                    st.subheader(f"Day {day_num}: {theme}")
                    
                    activities = getattr(day, 'activities', [])
                    for activity in activities:
                        time_slot = getattr(activity, 'time_slot', '')
                        loc_name = getattr(activity, 'activity_name', getattr(activity, 'name', ''))
                        
                        with st.expander(f"🕒 {time_slot} - {loc_name}", expanded=True):
                            transport = getattr(activity, 'transport_mode', None)
                            if transport:
                                st.markdown(f'<div class="transport-badge">🚆 Mode of Transport: {transport}</div>', unsafe_allow_html=True)
                            
                            desc = getattr(activity, 'description', '')
                            st.write(desc)
                            
                            cost = getattr(activity, 'estimated_cost', None)
                            if cost:
                                st.caption(f"Estimated Cost: {cost}")

    with tab_packing:
        st.subheader(f"Smart Luggage Checklist for {current_destination}")
        packing_list = st.session_state.get("packing_list")
        
        if packing_list:
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown("👕 **Clothing & Apparel**")
                    for item in getattr(packing_list, 'clothing', []):
                        st.checkbox(item, key=f"cl_{item}")
                
                with st.container(border=True):
                    st.markdown("🔌 **Electronics & Gear**")
                    for item in getattr(packing_list, 'electronics', []):
                        st.checkbox(item, key=f"el_{item}")

                with st.container(border=True):
                    st.markdown("🚆 **Transport-Specific Essentials**")
                    for item in getattr(packing_list, 'transport_specific_gear', []):
                        st.checkbox(item, key=f"tr_{item}")

            with col2:
                with st.container(border=True):
                    st.markdown("🧴 **Toiletries & Personal Care**")
                    for item in getattr(packing_list, 'toiletries', []):
                        st.checkbox(item, key=f"to_{item}")

                with st.container(border=True):
                    st.markdown("📄 **Documents, ID & Money**")
                    for item in getattr(packing_list, 'documents_and_money', []):
                        st.checkbox(item, key=f"doc_{item}")

                with st.container(border=True):
                    st.markdown("🎒 **Extras & Comfort Items**")
                    for item in getattr(packing_list, 'extras', []):
                        st.checkbox(item, key=f"ex_{item}")

    with tab_expense:
        st.subheader("💰 Group Expense Splitter & Budget Calculator")
        st.markdown("Calculate and split trip costs evenly across all travelers, including individual custom fares.")
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            total_budget_input = st.number_input("Total Estimated Trip Cost (Base)", min_value=0.0, value=base_default_cost, step=500.0)
            num_travelers_input = st.number_input("Number of Travelers to Split Between", min_value=1, max_value=20, value=trav)
            
            # Collect custom individual fares
            st.markdown("### Individual Custom Fares / Expenses")
            individual_extras = []
            for i in range(int(num_travelers_input)):
                fare = st.number_input(f"Custom Fare / Expense for Traveler {i+1} (₹)", min_value=0.0, value=0.0, step=100.0, key=f"traveler_fare_{i}")
                individual_extras.append(fare)
        
        with col_ex2:
            total_individual_extras = sum(individual_extras)
            grand_total = total_budget_input + total_individual_extras
            per_person_cost = grand_total / num_travelers_input if num_travelers_input > 0 else 0
            
            st.markdown("### Cost Breakdown")
            st.metric(label="Base Cost", value=f"₹{total_budget_input:,.2f}")
            st.metric(label="Total Custom Fares Added", value=f"₹{total_individual_extras:,.2f}")
            st.metric(label="Grand Total Combined Cost", value=f"₹{grand_total:,.2f}")
            st.metric(label="Cost Per Traveler", value=f"₹{per_person_cost:,.2f}", delta=f"Split across {num_travelers_input} Travelers")

    st.divider()

    pdf_data = create_itinerary_pdf(itinerary)
    st.download_button(
        label="📥 Download Itinerary (PDF)",
        data=pdf_data,
        file_name=f"{current_destination.lower().replace(' ', '_')}_itinerary.pdf",
        mime="application/pdf",
        key="download_pdf_btn"
    )