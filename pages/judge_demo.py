from __future__ import annotations

import streamlit as st

from services.ai_service import AIService

st.title("Judge Demo")
st.caption("This demo shows how history-based memory changes the response from generic to personalized.")

step_1 = st.text_area("STEP 1: Enter profile context", value="I grow tomatoes in red soil.")
step_2 = st.text_area(
    "STEP 2: Enter previous problem and outcome",
    value="Last season my tomatoes had leaf curling and the treatment I used worked after 7 days.",
)

if st.button("Run Memory Demo"):
    st.session_state.memory_service.store_memory(
        "profile",
        "Farmer grows tomatoes in red soil",
        "Crop: Tomato; soil: red soil; previous context recorded",
        "tomato,red_soil,profile",
    )
    st.session_state.memory_service.store_memory(
        "problem",
        "Tomato leaf curling in red soil before",
        "Previous treatment improved after 7 days; neem-based spray used; symptoms matched current case",
        "tomato,leaf_curling,red_soil,treatment",
    )

    relevant = st.session_state.memory_service.retrieve_relevant_memories(
        "My tomato leaves are curling again. What should I check?"
    )
    response = AIService().build_response(
        "My tomato leaves are curling again. What should I check?",
        farmer_profile={"name": "Ravi", "location": "Telangana", "soil_type": "Red soil", "main_crops": "Tomato"},
        memories=relevant,
        crop_history=st.session_state.db_service.list_crop_history(),
        feedback=st.session_state.db_service.list_feedback(),
        language="en",
    )
    st.session_state.demo_relevant = relevant
    st.session_state.demo_response = response

if "demo_relevant" in st.session_state:
    st.subheader("Relevant memories used")
    for memory in st.session_state.demo_relevant:
        st.write(f"• {memory.get('summary', '')}")

    st.subheader("Personalized recommendation")
    st.info(st.session_state.demo_response)
    st.markdown("### What the judges should notice")
    st.write("Without memory: general warning and generic checks")
    st.write("With Hindsight Memory: specific comparison with previous leaf curling in red soil and earlier successful treatment pattern")

st.markdown("---")
with st.expander("Demo steps"):
    st.write("1. Create a profile and save basic details.")
    st.write("2. Tell the AI about the previous tomato problem and the treatment that helped.")
    st.write("3. Start a new conversation and ask about the same or similar symptoms.")
    st.write("4. Show the retrieved memories and resulting personalized advice.")
