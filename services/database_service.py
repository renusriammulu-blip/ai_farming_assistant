from __future__ import annotations

import json
from pathlib import Path

from database.database import Database


class DatabaseService:
    def __init__(self, db_path: str | Path | None = None):
        self.db = Database(db_path)

    def _read_sample_data(self):
        sample_path = Path(__file__).resolve().parent.parent / "data" / "sample_farm_data.json"
        if not sample_path.is_file():
            return None
        with sample_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def seed_sample_data(self) -> None:
        with self.db.connect() as conn:
            profile_count = conn.execute("SELECT COUNT(*) FROM farmer_profile").fetchone()[0]
            if profile_count == 0:
                payload = self._read_sample_data()
                if payload is None:
                    return
                farmer = payload["farmer"]
                conn.execute(
                    """
                    INSERT INTO farmer_profile (
                        name, location, preferred_language, land_size,
                        soil_type, main_crops, farming_experience, irrigation_type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        farmer["name"],
                        farmer["location"],
                        farmer["preferred_language"],
                        farmer["land_size"],
                        farmer["soil_type"],
                        ", ".join(farmer["main_crops"]),
                        farmer["farming_experience"],
                        farmer["irrigation_type"],
                    ),
                )
                for crop in payload["crop_history"]:
                    conn.execute(
                        """
                        INSERT INTO crop_history (
                            crop_name, variety, season, planting_date, harvest_date,
                            land_area, soil_type, fertilizer_used, irrigation_method,
                            yield_value, problems_encountered, final_outcome, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            crop["crop_name"],
                            crop["variety"],
                            crop["season"],
                            crop["planting_date"],
                            crop["harvest_date"],
                            crop["land_area"],
                            crop["soil_type"],
                            crop["fertilizer_used"],
                            crop["irrigation_method"],
                            crop["yield_value"],
                            crop["problems_encountered"],
                            crop["final_outcome"],
                            crop.get("notes", ""),
                        ),
                    )
                for problem in payload["problems"]:
                    conn.execute(
                        """
                        INSERT INTO farm_problems (
                            crop_name, issue_description, symptoms, location,
                            soil_type, notes
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            problem["crop_name"],
                            problem["issue_description"],
                            problem["symptoms"],
                            problem["location"],
                            problem["soil_type"],
                            problem.get("notes", ""),
                        ),
                    )
                for feedback in payload["feedback"]:
                    conn.execute(
                        "INSERT INTO feedback (source, rating, feedback_text) VALUES (?, ?, ?)",
                        (feedback["source"], feedback["rating"], feedback["feedback_text"]),
                    )

    def save_farmer_profile(self, profile: dict):
        with self.db.connect() as conn:
            conn.execute(
                """
                DELETE FROM farmer_profile
                """
            )
            conn.execute(
                """
                INSERT INTO farmer_profile (
                    name, location, preferred_language, land_size,
                    soil_type, main_crops, farming_experience, irrigation_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    profile.get("name", ""),
                    profile.get("location", ""),
                    profile.get("preferred_language", "en"),
                    profile.get("land_size", ""),
                    profile.get("soil_type", ""),
                    profile.get("main_crops", ""),
                    profile.get("farming_experience", ""),
                    profile.get("irrigation_type", ""),
                ),
            )
            conn.commit()

    def get_farmer_profile(self):
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM farmer_profile ORDER BY id DESC LIMIT 1").fetchone()
            return dict(row) if row else {}

    def save_crop_history(self, record: dict):
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO crop_history (
                    crop_name, variety, season, planting_date, harvest_date,
                    land_area, soil_type, fertilizer_used, irrigation_method,
                    yield_value, problems_encountered, final_outcome, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get("crop_name", ""),
                    record.get("variety", ""),
                    record.get("season", ""),
                    record.get("planting_date", ""),
                    record.get("harvest_date", ""),
                    record.get("land_area", ""),
                    record.get("soil_type", ""),
                    record.get("fertilizer_used", ""),
                    record.get("irrigation_method", ""),
                    record.get("yield_value", ""),
                    record.get("problems_encountered", ""),
                    record.get("final_outcome", ""),
                    record.get("notes", ""),
                ),
            )
            conn.commit()

    def list_crop_history(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM crop_history ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def save_problem(self, record: dict):
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO farm_problems (
                    crop_name, issue_description, symptoms, location,
                    soil_type, image_path, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get("crop_name", ""),
                    record.get("issue_description", ""),
                    record.get("symptoms", ""),
                    record.get("location", ""),
                    record.get("soil_type", ""),
                    record.get("image_path", ""),
                    record.get("notes", ""),
                ),
            )
            conn.commit()

    def list_problems(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM farm_problems ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def save_feedback(self, record: dict):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO feedback (source, rating, feedback_text) VALUES (?, ?, ?)",
                (
                    record.get("source", "assistant"),
                    record.get("rating", ""),
                    record.get("feedback_text", ""),
                ),
            )
            conn.commit()

    def list_feedback(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def save_memory(self, memory_type: str, summary: str, details: str = "", tags: str = ""):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO hindsight_memories (memory_type, summary, details, tags) VALUES (?, ?, ?, ?)",
                (memory_type, summary, details, tags),
            )
            conn.commit()

    def list_memories(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM hindsight_memories ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def save_conversation_entry(self, session_name: str, message: str):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO conversation_metadata (session_name, message) VALUES (?, ?)",
                (session_name, message),
            )
            conn.commit()
