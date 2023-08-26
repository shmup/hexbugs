import sqlite3
from hexbugs.config import Config

def check_trigger_exists(trigger_name):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='trigger' AND name='{trigger_name}';")
    result = cursor.fetchone()

    conn.close()

    return result is not None

def execute_sql_file(filename):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()

    with open(filename, 'r') as f:
        sql_file = f.read()

    cursor.executescript(sql_file)

    conn.commit()
    conn.close()
