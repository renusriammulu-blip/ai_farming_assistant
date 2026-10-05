# AgriMitra – AI Farming Assistant with Long-Term Memory

## Project name
AgriMitra

## Problem statement
Small and medium-scale farmers often rely on memory, local advice, and short-term notes, but this information is rarely connected over time. As a result, they may repeat mistakes, forget the outcome of earlier treatments, and make decisions without using their own past experience.

## Solution
AgriMitra is a Streamlit-based AI farming assistant that stores and retrieves a farmer's historical context through Hindsight Memory. It remembers crop history, soil type, previous problems, treatment outcomes, and feedback, then uses these memories to personalize future recommendations.

## Why this problem matters
A farmer’s past knowledge is valuable, but it is often lost when it sits in scattered notes, conversations, or memory. A system that remembers previous results can reduce repeated mistakes, improve treatment decisions, and make advice more relevant to each farm.

## Key features
- Farmer profile with reusable details
- Crop history tracking
- Farm problem capture
- Memory-based personalization
- Feedback loop that improves future recommendations
- Memory dashboard for judges
- Judge demo showing the before/after impact of long-term memory
- English and Telugu support
- SQLite for structured data
- Hindsight-inspired memory layer with local fallback when no external API is available

## Hindsight Memory role
Hindsight Memory is the heart of the project. It is used to:
1. Store useful information from previous interactions.
2. Retrieve only relevant memories when new farm problems are discussed.
3. Personalize responses based on past crop behavior and treatments.
4. Learn from farmer feedback over time.
5. Explain when a recommendation is based on the farmer’s historical context.

The app keeps a clear distinction between:
- SQLite: structured application data such as profile, crop records, and feedback.
- Hindsight Memory: long-term semantic memory used for retrieval and personalization.

## Why Hindsight Memory is essential
Without Hindsight Memory, the assistant gives generic advice. With memory, the assistant can say: "You previously had leaf curling in red soil; let’s compare it with your current symptoms before deciding what to do next."

This matters because the farmer’s real experience accumulates over multiple seasons. The system becomes more personalized as it learns which crop varieties, soil types, irrigation patterns, and treatments worked or failed before.

## Architecture
This project follows a simple but practical structure:

- Streamlit frontend for pages and dashboards
- SQLite database for structured data
- Memory service for Hindsight retrieval and fallback storage
- AI service for response generation
- Utility helpers for prompts and multilingual text

## Technology stack
- Python
- Streamlit
- SQLite
- Requests
- OpenAI-compatible API support (optional)
- Hindsight-aware memory layer with local fallback

## Project structure
```text
agri-mitra/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   └── sample_farm_data.json
├── database/
│   └── database.py
├── pages/
│   ├── home.py
│   ├── farmer_profile.py
│   ├── crop_history.py
│   ├── farming_assistant.py
│   ├── farm_problems.py
│   ├── memory_dashboard.py
│   ├── feedback.py
│   └── judge_demo.py
├── services/
│   ├── ai_service.py
│   ├── database_service.py
│   └── memory_service.py
├── utils/
│   ├── language.py
│   └── prompts.py
└── .venv
```

## Installation
From the project folder:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Environment variables
Copy the sample file and update values if needed:

```bash
copy .env.example .env
```

Example variables:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
USE_LLM=false
HINDSIGHT_API_KEY=
HINDSIGHT_BASE_URL=
```

If the official Hindsight SDK is installed later, the app will use it automatically. If not, it uses the local fallback memory storage so the app still works for demos.

## How to run
Use the project virtual environment and start the app:

```powershell
& "C:/Users/renus/OneDrive/Desktop/New folder/Project/.venv/Scripts/python.exe" -m streamlit run "c:/Users/renus/OneDrive/Desktop/New folder/Project/app.py" --server.headless true --server.port 8501
```

Then visit:

```text
http://localhost:8501
```

## Demo flow
1. Create a farmer profile.
2. Enter crop records and previous problems.
3. Save the farmer feedback and treatment outcome.
4. Start a new chat and ask about a similar issue.
5. Show how the relevant memories are retrieved.
6. Show the personalized recommendation and how it compares to a generic answer.

## Safety considerations
This app is a decision-support tool and not a replacement for local agronomists or agricultural officers. Disease identification is never presented as a confirmed diagnosis unless validated by an expert. When a description looks serious, the app suggests consulting a local agricultural officer or agronomist.

## Future improvements
- Real Hindsight SDK integration for production-grade memory storage
- Image upload and crop disease recognition
- SMS or WhatsApp farmer interaction
- Better multilingual farming advice
- More advanced memory scoring and filtering

## Hackathon demo note
The project is built around memory-first behavior. The most important slide for judges is:

- Without memory: generic advice
- With Hindsight Memory: personalized advice linked to the farmer's actual history

This is where the app demonstrates real value and long-term learning.
