import time
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Animated AI Travel Planner Demo",
    page_icon="✈️",
    layout="wide",
)

# 2. Custom CSS Injection for Animations and Movable UI Aesthetics
st.markdown(
    """
<style>
    /* Smooth Fade-in Animation for Elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Gentle Floating Animation */
    @keyframes floatSlow {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    /* Apply Fade-in to main blocks */
    .stMainBlockContainer > div {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Animated and Glowing Buttons */
    .stButton > button {
        transition: all 0.3s ease-in-out;
        border-radius: 12px;
        font-weight: bold;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        border: none;
    }
    
    .stButton > button:hover {
        transform: scale(1.03) translateY(-2px);
        box-shadow: 0 10px 25px rgba(255, 75, 75, 0.4);
    }

    /* Floating transport badge */
    .animated-badge {
        display: inline-block;
        animation: floatSlow 3s ease-in-out infinite;
        background-color: #1f2937;
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* Polished Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        transition: background-color 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(255, 75, 75, 0.08);
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. Sidebar Layout Controls
with st.sidebar:
    st.markdown("### 🎛️ Trip Controls")
    destination = st.text_input("Destination", "Goa, India")
    duration = st.slider("Duration (Days)", 1, 5, 3)
    travelers = st.number_input("Travelers", 1, 10, 2)

    generate_btn = st.button("✨ Generate Itinerary", use_container_width=True)

# 4. Main App Content Area
st.markdown(
    "# ✈️ Interactive AI Travel Planner",
    help="Powered by Gemini & Streamlit",
)
st.markdown(
    "Explore your customized travel timeline below with dynamic, collapsible UI cards and smooth animations."
)
st.markdown("---")

if generate_btn:
    with st.spinner("🤖 Crafting your personalized journey..."):
        time.sleep(1.2)  # Simulating smooth loading transition

# Sample Mock Itinerary Data for the Demo
mock_days = [
    {
        "day": 1,
        "theme": "Coastal Exploration & Historic Forts",
        "summary": (
            "Immerse yourself in heritage architecture and sun-kissed beaches."
        ),
        "transport": "🚗 Private AC Cab",
        "activities": [
            ("09:00 AM", "Visit the historic Fort Aguada lighthouse and ramparts."),
            (
                "01:00 PM",
                "Seafood lunch at a beachside shack in Candolim beach.",
            ),
            ("04:30 PM", "Sunset stroll across Vagator cliffs."),
        ],
    },
    {
        "day": 2,
        "theme": "Old Goa Heritage & Spice Plantations",
        "summary": "Discover UNESCO world heritage churches and lush green trails.",
        "transport": "🚐 Guided Tour Bus",
        "activities": [
            (
                "09:30 AM",
                "Explore the Basilica of Bom Jesus and Se Cathedral.",
            ),
            (
                "01:30 PM",
                "Traditional Goan spice plantation tour with authentic lunch.",
            ),
            ("05:00 PM", "Sunset river cruise along the Mandovi river."),
        ],
    },
    {
        "day": 3,
        "theme": "Cultural Markets & Sunset Dining",
        "summary": "Shop local artisan goods and enjoy vibrant local nightlife.",
        "transport": "🚶 Walking & Local Tuk-Tuk",
        "activities": [
            ("10:00 AM", "Anjuna Flea Market shopping experience."),
            ("02:00 PM", "Café hopping in the Latin Quarter of Fontainhas."),
            (
                "07:00 PM",
                "Farewell dinner and live acoustic music by the beach.",
            ),
        ],
    },
]

# 5. Displaying Movable & Collapsible UI Expanders
for day_data in mock_days[:duration]:
    with st.expander(
        f"🌟 Day {day_data['day']}: {day_data['theme']}",
        expanded=(day_data["day"] == 1),
    ):
        st.markdown(f"*{day_data['summary']}*")
        st.markdown("")

        col1, col2 = st.columns([3, 1])
        with col1:
            for time_slot, desc in day_data["activities"]:
                st.markdown(f"- **{time_slot}** — {desc}")
        with col2:
            st.markdown(
                f"<div class='animated-badge'>{day_data['transport']}</div>",
                unsafe_allow_html=True,
            )

st.markdown("---")
col_down, col_share = st.columns(2)
with col_down:
    if st.button("📥 Download Itinerary (PDF)", use_container_width=True):
        st.success("Download ready!")