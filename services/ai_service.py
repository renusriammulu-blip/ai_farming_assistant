from __future__ import annotations

import io
import os
from collections import Counter
from typing import Any

import requests
from PIL import Image


class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def build_response(
        self,
        user_query: str,
        farmer_profile: dict | None = None,
        memories: list[dict] | None = None,
        crop_history: list[dict] | None = None,
        feedback: list[dict] | None = None,
        language: str = "en",
    ) -> str:
        if self.api_key and os.getenv("USE_LLM", "false").lower() == "true":
            try:
                return self._call_openai(user_query, farmer_profile, memories, crop_history, feedback, language)
            except Exception:
                pass

        return self._fallback_response(user_query, farmer_profile, memories, crop_history, feedback, language)

    def analyze_crop_image(
        self,
        uploaded_image: Any | None,
        crop_name: str = "",
        user_notes: str = "",
        language: str = "en",
    ) -> dict[str, str]:
        if uploaded_image is None:
            message = "Please upload a crop photo to begin disease analysis."
            return {"disease": "No image uploaded", "confidence": "Low", "instructions": message}

        text_signal = f"{crop_name} {user_notes or ''}".lower()
        image = None
        try:
            image = Image.open(io.BytesIO(uploaded_image.getvalue() if hasattr(uploaded_image, "getvalue") else uploaded_image)).convert("RGB")
            image = image.resize((120, 120))
        except Exception:
            image = None

        disease = self._detect_disease_from_text(text_signal)
        confidence = "Medium"

        if image is not None:
            dominant = self._get_dominant_color(image)
            brown_ratio = self._get_color_ratio(image, (120, 60, 0), tolerance=60)
            yellow_ratio = self._get_color_ratio(image, (200, 180, 40), tolerance=90)
            white_ratio = self._get_color_ratio(image, (255, 255, 255), tolerance=60)
            green_ratio = self._get_color_ratio(image, (50, 140, 40), tolerance=80)
            red_ratio = self._get_color_ratio(image, (180, 40, 30), tolerance=80)

            if brown_ratio > 0.08 or (dominant[0] > 100 and dominant[1] < 110 and dominant[2] < 100):
                disease = "Leaf Spot"
                confidence = "High"
            elif white_ratio > 0.12 or "powder" in text_signal:
                disease = "Powdery Mildew"
                confidence = "High"
            elif red_ratio > 0.1 or "rust" in text_signal:
                disease = "Rust"
                confidence = "High"
            elif yellow_ratio > 0.18 or "yellow" in text_signal:
                disease = "Nutrient Deficiency"
                confidence = "Medium"
            elif green_ratio < 0.45 and brown_ratio > 0.04:
                disease = "Bacterial Blight"
                confidence = "Medium"

        instructions = self._get_disease_instructions(disease, crop_name, language)
        return {"disease": disease, "confidence": confidence, "instructions": instructions}

    def _detect_disease_from_text(self, text_signal: str) -> str:
        lower = text_signal.lower()
        if any(word in lower for word in ["powder", "white dust", "dusty", "white coating"]):
            return "Powdery Mildew"
        if any(word in lower for word in ["rust", "orange", "orange spots", "brown pustules"]):
            return "Rust"
        if any(word in lower for word in ["wilting", "drooping", "collapse", "dry stem"]):
            return "Wilt"
        if any(word in lower for word in ["brown spots", "lesions", "spots", "dark patches", "leaf spot"]):
            return "Leaf Spot"
        if any(word in lower for word in ["yellow", "pale", "stunted", "chlorosis"]):
            return "Nutrient Deficiency"
        if any(word in lower for word in ["water-soaked", "dark blight", "blight", "burnt"]):
            return "Bacterial Blight"
        return "Leaf Spot"

    def _get_dominant_color(self, image: Image.Image) -> tuple[int, int, int]:
        pixels = list(image.getdata())
        color_counts = Counter(pixels)
        return max(color_counts, key=color_counts.get)

    def _get_color_ratio(self, image: Image.Image, reference_color: tuple[int, int, int], tolerance: int = 60) -> float:
        pixels = list(image.getdata())
        if not pixels:
            return 0.0
        match_count = 0
        for pixel in pixels:
            r, g, b = pixel
            rr, gg, bb = reference_color
            if abs(r - rr) <= tolerance and abs(g - gg) <= tolerance and abs(b - bb) <= tolerance:
                match_count += 1
        return match_count / len(pixels)

    def _get_disease_instructions(self, disease: str, crop_name: str, language: str) -> str:
        crop_hint = crop_name.strip() or "this crop"
        if language == "te":
            guidance = {
                "Leaf Spot": (
                    "మొదట సోకిన ఆకులను తీసివేయండి. నీరు పై నుంచి పూయకుండగా, నేలపై చల్లడం తగ్గించండి. "
                    "కాపర్-ఆధారిత ఫంగిసైడ్/స్ప్రేను సూచించిన డోస్లో ఉపయోగించండి. గాలి సరిగ్గా ఉండేలా చెత్త మరియు మూలాలను తొలగించండి."
                ),
                "Powdery Mildew": (
                    "మొక్కల మధ్యన గాలి సరిపడేలా space ఇవ్వండి. నీటిని ఆకులపై పడకుండా చూసుకోండి. సల్ఫర్/పొటాషియం బైకార్బొనేట్ ఆధారిత స్ప్రేను ఉపయోగించండి. "
                    "అధిక స్తబ్ద నీరు, అకాల తేమను తగ్గించండి."
                ),
                "Rust": (
                    "ఇన్ఫెక్టెడ్ ఆకులు మరియు కొమ్మలు తొలగించండి. మాంగనీస్/సల్ఫర్ ఆధారిత ఫంగిసైడ్ లేదా డోస్ను అనుసరించి వాడండి. తక్కువ నీటితో, బాగా విత్తనాలు మరియు బలమైన విత్తనాల ఎంపిక చేయండి."
                ),
                "Bacterial Blight": (
                    "సోకిన మొక్కలను తొలగించి, వాటి నుంచి ఇతర మొక్కలకు వ్యాప్తి చెందకుండా చూసుకోండి. ఆవర్తక నీటిని తగ్గించండి. "
                    "కాపర్-ఆధారిత ఉత్పత్తిని ఉపయోగించండి మరియు పనిముట్లను శుభ్రం చేసుకోండి."
                ),
                "Wilt": (
                    "నేలలో నీరు నిలువకుండా చూసుకోండి. వృద్ధి చెందుతున్న మొక్కలకు ఎండిన రూట్లను పరిశీలించండి. రూట్ రోట్/సామాన్య అనారోగ్యాన్ని నివారించడానికి సురక్షిత విత్తనాలు మరియు మంచి డ్రైనేజ్ని ఉపయోగించండి."
                ),
                "Nutrient Deficiency": (
                    "మొక్కకు సరైన NPK సంతులనం ఇవ్వండి. నేల పరీక్ష చేయించి పీహ్ మరియు పోషకాలను సరిదిద్దండి. మంచి నీరు, మిక్షర మరియు సారవంతమైన ఎరువులను ఉపయోగించండి."
                ),
            }
            return (
                f"{crop_hint} కోసం గుర్తించిన రోగం: {disease}. "
                f"సాధారణంగా చేయవలసిన చర్యలు: {guidance.get(disease, 'ప్రత్యక్షంగా పరిశీలించి ఎంపిక చేసిన పర్యవేక్షణను అందించండి.')}"
            )

        guidance = {
            "Leaf Spot": (
                "Remove infected leaves immediately and avoid overhead watering. Use a copper-based fungicide or a recommended spray at the correct dose. "
                "Improve air circulation, remove fallen debris, and keep the field dry to reduce spread."
            ),
            "Powdery Mildew": (
                "Improve airflow around the crop and avoid wetting the leaves. Apply sulfur or potassium bicarbonate spray according to label instructions. "
                "Remove heavily infected shoots and reduce overcrowding."
            ),
            "Rust": (
                "Prune and remove infected leaves or stems. Apply a suitable fungicide and maintain a regular field inspection schedule. "
                "Avoid excess moisture and prefer resistant varieties where possible."
            ),
            "Bacterial Blight": (
                "Remove infected plants and keep water off the leaves. Use a copper-based treatment and disinfect farm tools after use. "
                "Avoid moving infected plant material between rows."
            ),
            "Wilt": (
                "Check the roots and drainage, as waterlogging can worsen wilting. Avoid over-irrigation and use healthy seed or disease-free seedlings. "
                "If the whole plant is collapsing, contact an agronomist quickly."
            ),
            "Nutrient Deficiency": (
                "Do a soil test and apply a balanced fertilizer according to crop stage. Correct pH or nutrient imbalance, and maintain timely irrigation. "
                "Watch for yellowing, stunted growth, or poor flowering and fruiting."
            ),
        }
        return (
            f"Detected disease for {crop_hint}: {disease}. "
            f"Recommended action: {guidance.get(disease, 'Inspect the crop closely, remove affected parts, and consult an agronomist if symptoms spread rapidly.')}"
        )

    def _call_openai(
        self,
        user_query: str,
        farmer_profile: dict | None,
        memories: list[dict] | None,
        crop_history: list[dict] | None,
        feedback: list[dict] | None,
        language: str,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are AgriMitra, a practical farming assistant for Indian farmers. "
                        "Respond in a friendly and simple style. Avoid diagnosing diseases as certain. "
                        "Use the farmer's memory, crop history, and previous feedback when relevant. "
                        "Always mention when advice is general and not a professional diagnosis."
                    ),
                },
                {
                    "role": "user",
                    "content": self._compose_prompt(user_query, farmer_profile, memories, crop_history, feedback, language),
                },
            ],
            "temperature": 0.4,
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def _compose_prompt(
        self,
        user_query: str,
        farmer_profile: dict | None,
        memories: list[dict] | None,
        crop_history: list[dict] | None,
        feedback: list[dict] | None,
        language: str,
    ) -> str:
        profile = farmer_profile or {}
        memory_text = "\n".join(f"- {item.get('summary', '')}" for item in (memories or [])[:5])
        crop_text = "\n".join(f"- {item.get('crop_name', '')}: {item.get('final_outcome', '')}" for item in (crop_history or [])[:5])
        feedback_text = "\n".join(f"- {item.get('feedback_text', '')}" for item in (feedback or [])[:5])
        return (
            f"Language: {language}\n"
            f"Farmer: {profile.get('name', 'Unknown')}\n"
            f"Location: {profile.get('location', '')}\n"
            f"Soil: {profile.get('soil_type', '')}\n"
            f"Main crops: {profile.get('main_crops', '')}\n"
            f"Relevant memories:\n{memory_text or 'None'}\n"
            f"Crop history:\n{crop_text or 'None'}\n"
            f"Feedback:\n{feedback_text or 'None'}\n"
            f"Question: {user_query}"
        )

    def _fallback_response(
        self,
        user_query: str,
        farmer_profile: dict | None,
        memories: list[dict] | None,
        crop_history: list[dict] | None,
        feedback: list[dict] | None,
        language: str,
    ) -> str:
        lowered = user_query.lower()
        profile = farmer_profile or {}
        memory_lines = [item.get("summary", "") for item in (memories or [])[:3]]
        history_lines = [item.get("crop_name", "") for item in (crop_history or [])[:3]]

        if any(word in lowered for word in ["curl", "yellow", "leaf", "curling"]):
            memory_note = (
                "You previously mentioned a similar issue: " + "; ".join(memory_lines) + ". "
                if memory_lines else ""
            )
            history_note = (
                "Your previous crop records include: " + ", ".join(history_lines) + ". " if history_lines else ""
            )
            advice = (
                "This looks like a general plant stress or nutrient-related issue, and I cannot confirm the exact disease without closer inspection. "
                "Check whether the leaves are curling with yellowing, whether watering is uneven, and whether the plant is under strong heat or pest pressure. "
                "Use a balanced nutrient plan, avoid overwatering, and inspect the undersides of leaves for pests. "
                "If symptoms spread quickly or the whole field is affected, contact your local agricultural officer or agronomist." 
            )
            return f"{memory_note}{history_note}In simple terms: {advice}"

        if "fertilizer" in lowered or "nutrient" in lowered:
            return (
                "Consider soil test data, crop stage, and your past fertilizer history before applying anything. "
                "Avoid excessive nitrogen on tomato or leafy crops during flowering or fruiting. "
                "If the crop is already showing stress, reduce the dose and re-check moisture and soil condition."
            )

        if "what should i monitor" in lowered or "monitor" in lowered or "week" in lowered:
            return (
                "This week, monitor leaf colour, soil moisture, pest pressure, irrigation timing, and signs of nutrient imbalance. "
                "Compare with your previous crop records and earlier treatments so you do not repeat the same mistake."
            )

        if "mistake" in lowered or "previous crop" in lowered:
            previous = "; ".join(feedback or [])
            return (
                "To improve future outcomes, compare the previous crop history with current conditions. Review watering frequency, fertilizer dose, pest control timing, and symptom timing. "
                f"Your previous learning notes include: {previous or 'No explicit feedback recorded yet.'}"
            )

        if language == "te":
            return (
                "మీ వ్యవసాయ చరిత్రను పరిగణనలోకి తీసుకుని, ముందుగా నేల, నీరు, కీటకాలు, మరియు పచ్చిక దశను పరిశీలించండి. "
                "ఇది ఖచ్చితమైన వ్యాధి నిర్ధారణ కాదని గుర్తుంచుకోండి. తీవ్రంగా పెరిగిన లక్షణాల కోసం స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి."
            )

        return (
            "I recommend checking the crop stage, soil moisture, irrigation pattern, pests, and any weather stress first. "
            "Use your previous crop history and memory to compare new symptoms with earlier issues. "
            "This is general guidance, not a confirmed diagnosis, and expert advice is important if the field is worsening quickly."
        )
