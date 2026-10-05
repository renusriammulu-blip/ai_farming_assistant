from __future__ import annotations

import streamlit as st

st.title("Farmer Profile")

profile = st.session_state.db_service.get_farmer_profile()

with st.form("farmer_profile_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Farmer name", value=profile.get("name", ""))
        location = st.text_input("Location", value=profile.get("location", ""))
        preferred_language = st.selectbox("Preferred language", ["en", "te"], index=0 if profile.get("preferred_language", "en") == "en" else 1)
        land_size = st.text_input("Land size", value=profile.get("land_size", ""))
    with col2:
        soil_type = st.text_input("Soil type", value=profile.get("soil_type", ""))
        main_crops = st.text_input("Main crops", value=profile.get("main_crops", ""))
        farming_experience = st.text_input("Farming experience", value=profile.get("farming_experience", ""))
        irrigation_type = st.text_input("Irrigation type", value=profile.get("irrigation_type", ""))

    submitted = st.form_submit_button("Save profile")
    if submitted:
        payload = {
            "name": name,
            "location": location,
            "preferred_language": preferred_language,
            "land_size": land_size,
            "soil_type": soil_type,
            "main_crops": main_crops,
            "farming_experience": farming_experience,
            "irrigation_type": irrigation_type,
        }
        st.session_state.db_service.save_farmer_profile(payload)
        st.session_state.memory_service.store_memory(
            "profile",
            f"Farmer {name} in {location} with {soil_type} soil and {main_crops} crops",
            f"Land size: {land_size}; irrigation: {irrigation_type}; experience: {farming_experience}",
            "profile,farmer,soil,location",
        )
        st.success("Farmer profile saved to structured database and Hindsight memory.")

if profile:
    st.subheader("Current profile")
    st.json(profile)
