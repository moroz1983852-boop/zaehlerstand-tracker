import os
import sqlite3

from models import Reading


def get_db_path() -> str:
    return os.getenv("DB_PATH", "zaehlerstaende.db")


def get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reading_date TEXT NOT NULL UNIQUE,
                value_kwh REAL NOT NULL
            )
        """)


def get_all_readings() -> list[Reading]:
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT id, reading_date, value_kwh FROM readings ORDER BY reading_date"
        ).fetchall()
    return [Reading(**dict(row)) for row in rows]


def add_reading(reading_date: str, value_kwh: float) -> Reading:
    with get_db_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO readings (reading_date, value_kwh) VALUES (?, ?)",
            (reading_date, value_kwh),
        )
        new_id = cursor.lastrowid
    return Reading(id=new_id, reading_date=reading_date, value_kwh=value_kwh)


def delete_reading(reading_id: int) -> bool:
    with get_db_connection() as connection:
        cursor = connection.execute("DELETE FROM readings WHERE id = ?", (reading_id,))
    return cursor.rowcount > 0
