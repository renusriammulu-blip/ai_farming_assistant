from __future__ import annotations

import streamlit as st

from services.ai_service import AIService

st.title("AI Farming Assistant")

profile = st.session_state.db_service.get_farmer_profile()
crop_history = st.session_state.db_service.list_crop_history()
feedback = st.session_state.db_service.list_feedback()
selected_language = st.session_state.get("language", "en")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if profile:
    st.caption(f"Farmer: {profile.get('name', 'Unknown')} | Location: {profile.get('location', 'Unknown')} | Crop: {profile.get('main_crops', '')}")

st.subheader("Crop disease detection from photo")
st.caption("Only crop or leaf photos are accepted for disease analysis. Human, book, or unrelated photos are not valid for this tool.")
col1, col2 = st.columns(2)
with col1:
    uploaded_image = st.file_uploader(
        "Upload a crop/leaf photo only",
        type=["png", "jpg", "jpeg"],
        help="Use a close-up image of the crop leaves, stem, or plant. Do not upload people, books, documents, or unrelated objects.",
    )
with col2:
    crop_name = st.text_input("Crop name", value=profile.get("main_crops", "Tomato") if profile else "Tomato")

is_crop_photo = st.checkbox("This photo is a close-up crop or leaf image of the plant", value=False)
symptom_notes = st.text_area(
    "Describe the symptoms",
    value=("Brown spots and yellowing on leaves" if selected_language == "en" else "ఆకులపై వంగిన మచ్చలు మరియు పసుపు రంగు"),
    height=120,
)

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded crop image", use_container_width=True)

if not is_crop_photo:
    st.warning("Please confirm this is a crop/leaf photo before analysis. Unrelated pictures are not allowed for disease detection.")

if st.button("Analyze crop disease", disabled=not is_crop_photo or uploaded_image is None):
    result = AIService().analyze_crop_image(uploaded_image, crop_name=crop_name, user_notes=symptom_notes, language=selected_language)
    st.session_state["disease_result"] = result

if "disease_result" in st.session_state:
    disease_result = st.session_state["disease_result"]
    st.success(f"Likely disease: {disease_result['disease']} ({disease_result['confidence']} confidence)")
    st.markdown(disease_result["instructions"])

st.divider()

initial_question = "నా టమాటా మొక్కల ఆకులు పసుపు రంగులోకి మారుతున్నాయి. ఏం చేయాలి?" if selected_language == "te" else "My tomato leaves are curling again. What should I check?"
query = st.text_area("Ask a farming question", value=initial_question)

if st.button("Get personalized advice"):
    relevant_memories = st.session_state.memory_service.retrieve_relevant_memories(query, limit=5)
    response = AIService().build_response(
        query,
        farmer_profile=profile,
        memories=relevant_memories,
        crop_history=crop_history,
        feedback=feedback,
        language=selected_language,
    )
    st.session_state.chat_history.append({"question": query, "answer": response, "memories": relevant_memories})

if st.session_state.chat_history:
    for item in reversed(st.session_state.chat_history):
        with st.container(border=True):
            st.markdown(f"**Farmer question:** {item['question']}")
            st.markdown(f"**AgriMitra answer:** {item['answer']}")
            if item["memories"]:
                st.markdown("**Relevant memories used:**")
                for memory in item["memories"]:
                    st.write(f"• {memory.get('summary', '')}")
else:
    st.info("Ask a question to see how Hindsight Memory personalizes the response.")

st.subheader("Recent memory retrieval")
relevant = st.session_state.memory_service.retrieve_relevant_memories(query, limit=5)
for memory in relevant:
    st.write(f"• {memory.get('summary', '')}")
