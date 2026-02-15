"""
MimicGram - SQLite Storage Layer
Persistent channel state
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("storage/state.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channel_state (
            channel_id INTEGER PRIMARY KEY,
            last_action TEXT,
            skip_count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
