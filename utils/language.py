LANGUAGE_TEXT = {
    "en": {
        "title": "AgriMitra",
        "profile": "Farmer Profile",
        "assistant": "AI Farming Assistant",
        "memory_dashboard": "Memory Dashboard",
        "feedback": "Feedback & Learning",
        "judge_demo": "Judge Demo",
        "farm_problems": "Farm Problems",
        "crop_history": "Crop History",
    },
    "te": {
        "title": "అగ్రిమిత్ర",
        "profile": "రైతు ప్రొఫైల్",
        "assistant": "ఏఐ వ్యవసాయ సహాయకుడు",
        "memory_dashboard": "మెమరీ డాష్‌బోర్డ్",
        "feedback": "ప్రతిస్పందన & అభ్యాసం",
        "judge_demo": "జడ్జ్ డెమో",
        "farm_problems": "పంట సమస్యలు",
        "crop_history": "పంట చరిత్ర",
    },
}


def get_lang_label(language: str, key: str) -> str:
    return LANGUAGE_TEXT.get(language, LANGUAGE_TEXT["en"]).get(key, key)
