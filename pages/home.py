from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="AgriMitra Home", page_icon="🌾")

st.title("AgriMitra – AI Farming Assistant with Long-Term Memory")
st.caption("A memory-first farming assistant designed to remember crop history, treatments, and feedback over time.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Profile", "Ready")
with col2:
    st.metric("Crop Records", str(len(st.session_state.db_service.list_crop_history())))
with col3:
    st.metric("Memories", str(len(st.session_state.memory_service.db_service.list_memories())))
with col4:
    st.metric("Feedback", str(len(st.session_state.db_service.list_feedback())))

st.markdown("### Why this matters")
st.write(
    "Small and medium farmers lose valuable knowledge when they change seasons, crops, or grow multiple plots. "
    "AgriMitra remembers what worked before, what failed before, and which treatment outcomes were useful."
)

st.markdown("### Memory-first workflow")
steps = [
    "Farmer profile is saved once and reused later.",
    "Crop history and previous problems are remembered.",
    "The assistant retrieves relevant memories before giving advice.",
    "Feedback and outcomes improve future recommendations.",
]
for step in steps:
    st.write(f"• {step}")

st.markdown("### Quick actions")
if st.button("Open Judge Demo"):
    st.switch_page("pages/judge_demo.py")

st.markdown("### Core idea")
st.info(
    "Without memory, advice is generic. With Hindsight Memory, the assistant can say: 'You previously had leaf curling in red soil; let's compare that with the current pattern before deciding on the next step.'"
)
