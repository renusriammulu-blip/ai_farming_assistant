from __future__ import annotations

import streamlit as st

st.title("Memory Dashboard")
st.caption("A user-friendly view of the long-term memory the assistant is using.")

profile = st.session_state.db_service.get_farmer_profile()
memories = st.session_state.memory_service.db_service.list_memories()
records = st.session_state.db_service.list_crop_history()
problems = st.session_state.db_service.list_problems()
feedback = st.session_state.db_service.list_feedback()

if profile:
    with st.expander("Farmer Profile"):
        st.json(profile)

with st.expander("Crop History"):
    if records:
        st.json(records)
    else:
        st.info("No crop records yet.")

with st.expander("Previous Problems"):
    if problems:
        st.json(problems)
    else:
        st.info("No previous problems yet.")

with st.expander("Farmer Feedback"):
    if feedback:
        st.json(feedback)
    else:
        st.info("No feedback yet.")

with st.expander("Hindsight Memory Entries"):
    if memories:
        for memory in memories:
            st.markdown(f"- **{memory.get('memory_type', 'memory')}**: {memory.get('summary', '')}")
            if memory.get('details'):
                st.caption(memory.get('details'))
    else:
        st.info("No memories yet.")

st.success("This dashboard demonstrates how AgriMitra keeps useful agricultural context over time.")
