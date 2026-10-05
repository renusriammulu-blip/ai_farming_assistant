from __future__ import annotations

import streamlit as st

from services.database_service import DatabaseService
from services.memory_service import MemoryService

st.set_page_config(
    page_title="AgriMitra",
    page_icon="🌾",
    layout="wide",
)

if "db_service" not in st.session_state:
    st.session_state.db_service = DatabaseService()
if "memory_service" not in st.session_state:
    st.session_state.memory_service = MemoryService(st.session_state.db_service)
if "language" not in st.session_state:
    st.session_state.language = "en"

st.session_state.db_service.seed_sample_data()

st.sidebar.title("AgriMitra")
st.sidebar.caption("Hindsight memory + farmer support")
st.session_state.language = st.sidebar.selectbox(
    "Language / భాష",
    ["English", "తెలుగు"],
    index=0,
    help="Choose the language for the assistant responses.",
)
st.session_state.language = "te" if st.session_state.language == "తెలుగు" else "en"

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠"),
    st.Page("pages/farmer_profile.py", title="Farmer Profile", icon="👨‍🌾"),
    st.Page("pages/farming_assistant.py", title="AI Farming Assistant", icon="🤖"),
    st.Page("pages/crop_history.py", title="Crop History", icon="🌱"),
    st.Page("pages/farm_problems.py", title="Farm Problems", icon="🩺"),
    st.Page("pages/memory_dashboard.py", title="Memory Dashboard", icon="🧠"),
    st.Page("pages/feedback.py", title="Feedback & Learning", icon="📣"),
    st.Page("pages/judge_demo.py", title="Judge Demo", icon="🚀"),
]

navigation = st.navigation(pages)
navigation.run()
