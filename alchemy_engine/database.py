"""
Database operations for storing elements and combinations.
Uses SQLite for local, deterministic storage.
"""
import sqlite3
import json
from typing import Optional, List
from .models import Element
from .config import DATABASE_PATH
import os


class AlchemyDatabase:
    """Handles all database operations for the alchemy engine."""

    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path

        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Initialize database
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Elements table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS elements (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    tags TEXT,
                    visual_hint TEXT,
                    behavior_hints TEXT,
                    is_base BOOLEAN,
                    parent_a TEXT,
                    parent_b TEXT,
                    combination_order TEXT,
                    created_at TEXT,
                    properties TEXT
                )
            """)

            # Combinations table for deterministic caching
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS combinations (
                    combo_key TEXT PRIMARY KEY,
                    result_id TEXT,
                    created_at TEXT,
                    FOREIGN KEY (result_id) REFERENCES elements (id)
                )
            """)

            conn.commit()

    def save_element(self, element: Element) -> None:
        """Save an element to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO elements
                (id, name, description, tags, visual_hint, behavior_hints,
                 is_base, parent_a, parent_b, combination_order, created_at, properties)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                element.id,
                element.name,
                element.description,
                json.dumps(element.tags),
                element.visual_hint,
                json.dumps(element.behavior_hints),
                element.is_base,
                element.parent_a,
                element.parent_b,
                element.combination_order,
                element.created_at,
                json.dumps(element.properties)
            ))

            conn.commit()

    def get_element(self, element_id: str) -> Optional[Element]:
        """Retrieve an element by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM elements WHERE id = ?", (element_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_element(row)
            return None

    def get_element_by_name(self, name: str) -> Optional[Element]:
        """Retrieve an element by name."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM elements WHERE name = ?", (name,))
            row = cursor.fetchone()

            if row:
                return self._row_to_element(row)
            return None

    def get_all_elements(self) -> List[Element]:
        """Get all elements from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM elements ORDER BY created_at ASC")
            rows = cursor.fetchall()

            return [self._row_to_element(row) for row in rows]

    def get_base_elements(self) -> List[Element]:
        """Get only base elements."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM elements WHERE is_base = 1 ORDER BY name ASC")
            rows = cursor.fetchall()

            return [self._row_to_element(row) for row in rows]

    def save_combination(self, combo_key: str, result_id: str, created_at: str) -> None:
        """Save a combination mapping for deterministic caching."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO combinations (combo_key, result_id, created_at)
                VALUES (?, ?, ?)
            """, (combo_key, result_id, created_at))

            conn.commit()

    def get_combination(self, combo_key: str) -> Optional[Element]:
        """Check if a combination has been done before."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT e.* FROM elements e
                JOIN combinations c ON e.id = c.result_id
                WHERE c.combo_key = ?
            """, (combo_key,))

            row = cursor.fetchone()

            if row:
                return self._row_to_element(row)
            return None

    def _row_to_element(self, row) -> Element:
        """Convert a database row to an Element object."""
        return Element(
            id=row[0],
            name=row[1],
            description=row[2],
            tags=json.loads(row[3]),
            visual_hint=row[4],
            behavior_hints=json.loads(row[5]),
            is_base=bool(row[6]),
            parent_a=row[7],
            parent_b=row[8],
            combination_order=row[9],
            created_at=row[10],
            properties=json.loads(row[11])
        )

    def get_stats(self) -> dict:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM elements WHERE is_base = 1")
            base_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM elements WHERE is_base = 0")
            combined_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM combinations")
            total_combinations = cursor.fetchone()[0]

            return {
                "base_elements": base_count,
                "combined_elements": combined_count,
                "total_elements": base_count + combined_count,
                "total_combinations": total_combinations
            }
