import sqlite3
import os
from datetime import datetime

ATL_DB_PATH = os.getenv("ATL_DB_PATH", "atl.db")

def init_atl():
    conn = sqlite3.connect(ATL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS action_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action_type TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_action(action_type: str, description: str):
    conn = sqlite3.connect(ATL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO action_log (timestamp, action_type, description)
        VALUES (?, ?, ?)
    ''', (datetime.utcnow().isoformat() + "Z", action_type, description))
    conn.commit()
    conn.close()

# Initialize DB on import
init_atl()
