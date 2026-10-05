from __future__ import annotations

import streamlit as st

st.title("Feedback & Learning")
st.caption("The farmer’s feedback improves the next recommendation.")

with st.form("feedback_form"):
    source = st.text_input("Advice source", value="assistant")
    rating = st.selectbox("Was this advice helpful?", ["Helpful", "Partially helpful", "Not helpful"])
    feedback_text = st.text_area("Share what happened after the advice")
    submitted = st.form_submit_button("Save feedback")
    if submitted:
        payload = {"source": source, "rating": rating, "feedback_text": feedback_text}
        st.session_state.db_service.save_feedback(payload)
        st.session_state.memory_service.update_memory_from_feedback(feedback_text, rating)
        st.success("Feedback stored and used in future memory-based recommendations.")

feedback = st.session_state.db_service.list_feedback()
if feedback:
    for item in feedback:
        with st.expander(f"{item['rating']} - {item['created_at']}"):
            st.json(item)
else:
    st.info("No feedback yet. Share a result to improve future guidance.")
