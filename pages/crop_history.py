from __future__ import annotations

import streamlit as st

st.title("Crop History")

with st.form("crop_history_form"):
    col1, col2 = st.columns(2)
    with col1:
        crop_name = st.text_input("Crop name")
        variety = st.text_input("Variety")
        season = st.text_input("Season")
        planting_date = st.date_input("Planting date")
        harvest_date = st.date_input("Harvest date")
    with col2:
        land_area = st.text_input("Land area")
        soil_type = st.text_input("Soil type")
        fertilizer_used = st.text_input("Fertilizer used")
        irrigation_method = st.text_input("Irrigation method")
        yield_value = st.text_input("Yield")

    problems_encountered = st.text_area("Problems encountered")
    final_outcome = st.text_area("Final outcome")
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Save crop record")
    if submitted:
        payload = {
            "crop_name": crop_name,
            "variety": variety,
            "season": season,
            "planting_date": str(planting_date),
            "harvest_date": str(harvest_date),
            "land_area": land_area,
            "soil_type": soil_type,
            "fertilizer_used": fertilizer_used,
            "irrigation_method": irrigation_method,
            "yield_value": yield_value,
            "problems_encountered": problems_encountered,
            "final_outcome": final_outcome,
            "notes": notes,
        }
        st.session_state.db_service.save_crop_history(payload)
        st.session_state.memory_service.store_memory(
            "crop_history",
            f"{crop_name} in {season} season with {problems_encountered or 'no major issues'}",
            f"Soil: {soil_type}; fertilizer: {fertilizer_used}; outcome: {final_outcome}; yield: {yield_value}",
            f"crop,{crop_name},{season},{soil_type}",
        )
        st.success("Crop history saved and stored in memory.")

records = st.session_state.db_service.list_crop_history()
if records:
    st.subheader("Saved crop records")
    for record in records:
        with st.expander(f"{record['crop_name']} - {record['season']}"):
            st.json(record)
else:
    st.info("No crop history yet. Add your first crop record.")
