import sqlite3

DB_PATH = "data/prices.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop TEXT,
        price INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
