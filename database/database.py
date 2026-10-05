from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str | Path | None = None):
        base_path = Path(db_path) if db_path else Path(__file__).resolve().parent.parent / "data" / "app.db"
        base_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = str(base_path)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS farmer_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    location TEXT,
                    preferred_language TEXT,
                    land_size TEXT,
                    soil_type TEXT,
                    main_crops TEXT,
                    farming_experience TEXT,
                    irrigation_type TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS crop_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crop_name TEXT,
                    variety TEXT,
                    season TEXT,
                    planting_date TEXT,
                    harvest_date TEXT,
                    land_area TEXT,
                    soil_type TEXT,
                    fertilizer_used TEXT,
                    irrigation_method TEXT,
                    yield_value TEXT,
                    problems_encountered TEXT,
                    final_outcome TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS farm_problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crop_name TEXT,
                    issue_description TEXT,
                    symptoms TEXT,
                    location TEXT,
                    soil_type TEXT,
                    image_path TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    rating TEXT,
                    feedback_text TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS hindsight_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_type TEXT,
                    summary TEXT,
                    details TEXT,
                    tags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT,
                    message TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
