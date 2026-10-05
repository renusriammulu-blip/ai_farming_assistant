from __future__ import annotations


def build_memory_summary_prompt(language: str = "en") -> str:
    if language == "te":
        return (
            "మీ వ్యవసాయ చరిత్ర, పంట సమస్యలు, చికిత్సలు మరియు ప్రతిస్పందనలను మీకు వ్యక్తిగతమైన సలహాల కోసం ఉపయోగించండి. "
            "ఆలోచనల శృంఖలాన్ని చూపించకుండా, పూర్తి, సులభమైన మరియు ఉపయోగపడే సారాంశాన్ని ఇవ్వండి."
        )
    return (
        "Use the farmer's crop history, previous problems, treatments, and feedback to create personal advice. "
        "Do not expose internal reasoning. Keep the answer practical and easy to understand."
    )
