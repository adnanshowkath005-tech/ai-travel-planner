import streamlit as st
from generator import generate_itinerary
from schemas import ItineraryRequest, BudgetLevel, Interest
from pdf_generator import create_itinerary_pdf

# Page Config
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 50%, #dbeafe 100%) !important;
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #dbeafe 0%, #e0e7ff 100%) !important;
        border-right: 1px solid #c7d2fe !important;
        box-shadow: 4px 0 15px rgba(79, 70, 229, 0.08);
    }

    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label {
        color: #1e1b4b !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] input, 
    section[data-testid="stSidebar"] textarea, 
    section[data-testid="stSidebar"] div[role="combobox"] {
        background-color: #ffffff !important;
        border: 1px solid #a5b4fc !important;
        border-radius: 10px !important;
        color: #1e293b !important;
    }

    .header-container {
        display: flex;
        align-items: center;
        gap: 16px;
        background: #ffffff;
        border: 1px solid #c7d2fe;
        padding: 20px 28px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.08);
    }
    
    .logo-badge {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: #ffffff;
        width: 56px;
        height: 56px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e1b4b;
        margin: 0;
    }

    .app-subtitle {
        color: #475569;
        font-size: 0.95rem;
        margin-top: 2px;
    }

    /* Target grid images to enforce uniform height and aspect cropping */
    div[data-testid="stImage"] > img {
        height: 160px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        width: 100% !important;
    }

    .stButton > button {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 6px 16px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25) !important;
    }

    .stButton > button:hover {
        background-color: #4338ca !important;
        color: #ffffff !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
    }

    .route-box {
        background: #ffffff;
        border-left: 6px solid #4f46e5;
        border-radius: 12px;
        padding: 18px 24px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.08);
    }

    .transport-badge {
        background: linear-gradient(90deg, #0284c7, #2563eb);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
    }

    h1, h2, h3, h4 {
        color: #1e1b4b !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initializations
if "destination_input" not in st.session_state:
    st.session_state["destination_input"] = "Thiruvananthapuram, Kerala, India"

# Transit route information map
HOW_TO_REACH_MAP = {
    "uzbekistan": "✈️ **Nearest Airport:** Islam Karimov Tashkent International Airport (TAS)\n🚆 **Rail Network:** Afrosiyob High-Speed Train links Tashkent, Samarkand, and Bukhara.\n🚗 **Local Transit:** Yandex Go taxi service or Metro in Tashkent.",
    "tashkent": "✈️ **Nearest Airport:** Islam Karimov Tashkent International Airport (TAS)\n🚆 **Metro:** Tashkent Metro system or Afrosiyob High-Speed Rail.",
    "kerala": "✈️ **Nearest Airport:** Cochin International Airport (COK) / Trivandrum Airport (TRV)\n🚆 **Nearest Railway:** Ernakulam Junction (ERS) / Trivandrum Central (TVC)\n🚗 **Road:** Connected via NH 66.",
    "goa": "✈️ **Nearest Airport:** Dabolim Airport (GOI) / Mopa Airport (GOX)\n🚆 **Nearest Railway:** Madgaon Junction (MAO)\n🚗 **Road:** Direct buses available from Mumbai, Pune, and Bengaluru.",
    "rajasthan": "✈️ **Nearest Airport:** Jaipur International Airport (JAI)\n🚆 **Nearest Railway:** Jaipur Junction (JP)\n🚗 **Road:** Connected via NH 48 from New Delhi.",
    "thiruvananthapuram": "✈️ **Nearest Airport:** Trivandrum International Airport (TRV)\n🚆 **Nearest Railway:** Trivandrum Central (TVC)\n🚗 **Road:** Well-connected via NH 66.",
    "maharashtra": "✈️ **Nearest Airport:** Chhatrapati Shivaji Maharaj International Airport, Mumbai (BOM)\n🚆 **Nearest Railway:** Chhatrapati Shivaji Maharaj Terminus (CSMT)",
    "karnataka": "✈️ **Nearest Airport:** Kempegowda International Airport, Bengaluru (BLR)\n🚆 **Nearest Railway:** KSR Bengaluru City Junction (SBC)",
    "himachal pradesh": "✈️ **Nearest Airport:** Bhuntar Airport, Kullu (KUU) / Chandigarh Airport (IXC)\n🚆 **Nearest Railway:** Kalka Railway Station (KLK)",
    "varanasi": "✈️ **Nearest Airport:** Lal Bahadur Shastri International Airport (VNS)\n🚆 **Nearest Railway:** Varanasi Junction (BSB)",
    "ladakh": "✈️ **Nearest Airport:** Kushok Bakula Rimpochee Airport, Leh (IXL)\n🚗 **Road:** Accessible via Leh-Manali Highway or Srinagar-Leh Highway.",
    "amritsar": "✈️ **Nearest Airport:** Sri Guru Ram Dass Jee International Airport (ATQ)\n🚆 **Nearest Railway:** Amritsar Junction (ASR)",
    "sri lanka": "✈️ **Nearest Airport:** Bandaranaike International Airport, Colombo (CMB)",
    "thailand": "✈️ **Nearest Airport:** Suvarnabhumi Airport (BKK) or Don Mueang (DMK)",
    "london": "✈️ **Nearest Airport:** London Heathrow (LHR) or Gatwick Airport (LGW)",
    "uk": "✈️ **Nearest Airport:** London Heathrow (LHR) or Gatwick Airport (LGW)",
    "kabul": "✈️ **Nearest Airport:** Kabul International Airport (KBL)",
    "afghanistan": "✈️ **Nearest Airport:** Kabul International Airport (KBL)",
    "lahore": "✈️ **Nearest Airport:** Allama Iqbal International Airport (LHE)",
    "pakistan": "✈️ **Nearest Airport:** Allama Iqbal International Airport (LHE)",
    "paris": "✈️ **Nearest Airport:** Charles de Gaulle Airport (CDG) / Orly Airport (ORY)",
    "france": "✈️ **Nearest Airport:** Charles de Gaulle Airport (CDG)",
    "tokyo": "✈️ **Nearest Airport:** Narita International Airport (NRT) / Haneda Airport (HND)",
    "japan": "✈️ **Nearest Airport:** Narita International Airport (NRT) / Haneda Airport (HND)",
    "dubai": "✈️ **Nearest Airport:** Dubai International Airport (DXB)",
    "uae": "✈️ **Nearest Airport:** Dubai International Airport (DXB)",
    "rome": "✈️ **Nearest Airport:** Leonardo da Vinci–Fiumicino Airport (FCO)",
    "italy": "✈️ **Nearest Airport:** Leonardo da Vinci–Fiumicino Airport (FCO)"
}

def get_transit_info(target_dest):
    clean_target = target_dest.lower().strip()
    for key, value in HOW_TO_REACH_MAP.items():
        if key in clean_target:
            return value
    return f"✈️ **Transit Info:** Book direct or connecting flights to the main international or domestic airport near **{target_dest}**."

# ---------------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="logo-badge">✈️</div>
    <div>
        <div class="app-title">AI Travel Planner</div>
        <div class="app-subtitle">Select a destination below or set your custom travel details in the sidebar.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Trip Preferences")
    
    destination = st.text_input(
        "Destination",
        value=st.session_state["destination_input"]
    )
    duration = st.number_input("Duration (days)", min_value=1, max_value=14, value=3)
    travelers = st.number_input("Travelers", min_value=1, value=2)
    budget = st.selectbox("Budget Level", [b.value for b in BudgetLevel])
    selected_interests = st.multiselect(
        "Interests",
        [i.value for i in Interest],
        default=["culture", "nature"]
    )
    must_see = st.text_area("Must-See Locations (optional)", "")

    submit = st.button("✨ Generate Itinerary", type="primary", use_container_width=True)

# Synchronize state when sidebar input changes
st.session_state["destination_input"] = destination

# ---------------------------------------------------------
# FEATURED DESTINATION LISTS
# ---------------------------------------------------------
india_places = [
    ("🌴 Kerala", "Kerala, India", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400&h=300&fit=crop"),
    ("🏖️ Goa", "Goa, India", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400&h=300&fit=crop"),
    ("🏰 Rajasthan", "Rajasthan, India", "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=300&fit=crop"),
    ("🛕 Thiruvananthapuram", "Thiruvananthapuram, Kerala, India", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=400&h=300&fit=crop"),
    ("🌆 Maharashtra", "Maharashtra, India", "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=400&h=300&fit=crop"),
    ("🏛️ Karnataka", "Karnataka, India", "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=400&h=300&fit=crop"),
    ("🏔️ Himachal Pradesh", "Himachal Pradesh, India", "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=300&fit=crop"),
    ("🛕 Varanasi", "Varanasi, India", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400&h=300&fit=crop"),
    ("🏔️ Ladakh", "Ladakh, India", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?w=400&h=300&fit=crop"),
    ("🛕 Amritsar", "Amritsar, Punjab, India", "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?w=400&h=300&fit=crop")
]

global_places = [
    ("🏛️ Uzbekistan", "Uzbekistan", "https://images.unsplash.com/photo-1528642474498-1af0c17fd8c3?w=400&h=300&fit=crop"),
    ("🏝️ Sri Lanka", "Sri Lanka", "https://images.unsplash.com/photo-1546708973-b339540b5162?w=400&h=300&fit=crop"),
    ("🇹🇭 Thailand", "Thailand", "https://images.unsplash.com/photo-1528181304800-259b08848526?w=400&h=300&fit=crop"),
    ("🇬🇧 UK", "London, UK", "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400&h=300&fit=crop"),
    ("🏔️ Afghanistan", "Kabul, Afghanistan", "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?w=400&h=300&fit=crop"),
    ("🕌 Pakistan", "Lahore, Pakistan", "https://images.unsplash.com/photo-1586016413664-864c0dd76f53?w=400&h=300&fit=crop"),
    ("🗼 Paris", "Paris, France", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=300&fit=crop"),
    ("🗾 Tokyo", "Tokyo, Japan", "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=400&h=300&fit=crop"),
    ("🏙️ Dubai", "Dubai, UAE", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=300&fit=crop"),
    ("🏛️ Rome", "Rome, Italy", "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=300&fit=crop")
]

def render_destination_grid(places, key_prefix):
    num_cols = 5
    for i in range(0, len(places), num_cols):
        cols = st.columns(num_cols)
        batch = places[i:i + num_cols]
        for idx, (label, loc_val, img_url) in enumerate(batch):
            with cols[idx]:
                with st.container():
                    st.image(img_url, use_container_width=True)
                    st.markdown(f"**{label}**")
                    if st.button("Select", key=f"{key_prefix}_{i + idx}", use_container_width=True):
                        st.session_state["destination_input"] = loc_val
                        st.rerun()

st.markdown("### 🇮🇳 Inside India *(Currency: INR ₹)*")
render_destination_grid(india_places, "in")

st.markdown("---")

st.markdown("### 🌍 Outside India *(Currency: USD $)*")
render_destination_grid(global_places, "out")

# ---------------------------------------------------------
# DYNAMIC "HOW TO REACH" SECTION
# ---------------------------------------------------------
route_info = get_transit_info(destination)

st.markdown(f"""
<div class="route-box">
    <h3>📍 How to Reach {destination}</h3>
    <p style="font-size: 0.95rem; line-height: 1.6; margin-top: 8px;">
        {route_info.replace(chr(10), '<br>')}
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# GENERATED ITINERARY DISPLAY
# ---------------------------------------------------------
if submit:
    request = ItineraryRequest(
        destination=destination,
        duration_days=duration,
        travelers_count=travelers,
        budget=BudgetLevel(budget),
        interests=[Interest(i) for i in selected_interests],
        must_see_spots=[s.strip() for s in must_see.split(",") if s.strip()]
    )

    with st.spinner("Crafting your itinerary with mode of transport details..."):
        try:
            itinerary = generate_itinerary(request)
            
            # Metric Columns
            m1, m2, m3 = st.columns(3)
            m1.metric("📍 Destination", itinerary.destination)
            m2.metric("📅 Duration", f"{itinerary.duration_days} Days")
            m3.metric("💰 Est. Total Budget", getattr(itinerary, 'estimated_cost', 'N/A'))

            st.divider()

            # Day Plans
            if hasattr(itinerary, 'days') and itinerary.days:
                day_tabs = st.tabs([f"Day {day.day_number}" for day in itinerary.days])
                
                for tab, day in zip(day_tabs, itinerary.days):
                    with tab:
                        st.subheader(f"Day {day.day_number}: {getattr(day, 'theme', '')}")
                        for activity in day.activities:
                            with st.expander(f"📍 {activity.time_slot} - {activity.location_name}", expanded=True):
                                if hasattr(activity, 'transport_mode') and activity.transport_mode:
                                    st.markdown(f'<div class="transport-badge">🚆 Mode of Transport: {activity.transport_mode}</div>', unsafe_allow_html=True)
                                
                                st.write(activity.description)
                                if hasattr(activity, 'estimated_cost'):
                                    st.caption(f"Estimated Cost: {activity.estimated_cost}")

            st.divider()
            
            # Download Button
            pdf_data = create_itinerary_pdf(itinerary)
            st.download_button(
                label="📄 Download Itinerary (PDF)",
                data=pdf_data,
                file_name=f"{destination.lower().replace(' ', '_')}_itinerary.pdf",
                mime="application/pdf"
            )
            if hasattr(itinerary, 'weather_forecast') and itinerary.weather_forecast:
             st.subheader("🌦️ Weather Forecast & Packing Advice")
             w = itinerary.weather_forecast
             col1, col2 = st.columns(2)
             with col1:
                 st.metric("Expected Temp", w.expected_temp_range)
             with col2:
                 st.info(f"**Climate Summary:** {w.climate_summary}")
             st.success(f"**Clothing & Packing Advice:** {w.clothing_advice}")
             st.divider()

        except Exception as e:
            st.error(f"Error generating itinerary: {e}")
