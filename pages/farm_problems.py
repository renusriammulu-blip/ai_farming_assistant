from __future__ import annotations

import streamlit as st

st.title("Farm Problems")

with st.form("problem_form"):
    crop_name = st.text_input("Crop name")
    issue_description = st.text_area("Describe the problem")
    symptoms = st.text_area("Symptoms observed")
    location = st.text_input("Location or plot")
    soil_type = st.text_input("Soil type")
    notes = st.text_area("Any extra notes")

    submitted = st.form_submit_button("Save problem record")
    if submitted:
        payload = {
            "crop_name": crop_name,
            "issue_description": issue_description,
            "symptoms": symptoms,
            "location": location,
            "soil_type": soil_type,
            "notes": notes,
        }
        st.session_state.db_service.save_problem(payload)
        st.session_state.memory_service.store_memory(
            "problem",
            f"{crop_name} issue: {issue_description}",
            f"Symptoms: {symptoms}; soil: {soil_type}; notes: {notes}",
            f"problem,{crop_name},{soil_type}",
        )
        st.success("Problem saved to the farm records and long-term memory.")

problems = st.session_state.db_service.list_problems()
if problems:
    for problem in problems:
        with st.expander(f"{problem['crop_name']} - {problem['issue_description'][:60]}"):
            st.json(problem)
else:
    st.info("No farm problems recorded yet.")
