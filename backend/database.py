import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for storing all module scan records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_type TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT,
        data_json TEXT NOT NULL,
        is_demo INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    )
    """)

    # Table for storing generated meal plans
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meal_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_json TEXT NOT NULL,
        plan_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # Table for user preference storage
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        profile_json TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def save_analysis(module_type: str, title: str, summary: str, data: dict, is_demo: bool = True) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO analyses (module_type, title, summary, data_json, is_demo, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (module_type, title, summary, json.dumps(data), 1 if is_demo else 0, now_str))
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def get_history(limit: int = 50, module_type: str = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    if module_type:
        cursor.execute("""
            SELECT id, module_type, title, summary, data_json, is_demo, created_at
            FROM analyses
            WHERE module_type = ?
            ORDER BY id DESC
            LIMIT ?
        """, (module_type, limit))
    else:
        cursor.execute("""
            SELECT id, module_type, title, summary, data_json, is_demo, created_at
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    
    rows = cursor.fetchall()
    results = []
    for row in rows:
        try:
            parsed_data = json.loads(row["data_json"])
        except Exception:
            parsed_data = {}
        results.append({
            "id": row["id"],
            "module_type": row["module_type"],
            "title": row["title"],
            "summary": row["summary"],
            "data": parsed_data,
            "is_demo": bool(row["is_demo"]),
            "created_at": row["created_at"]
        })
    conn.close()
    return results

def get_analysis_by_id(record_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "module_type": row["module_type"],
        "title": row["title"],
        "summary": row["summary"],
        "data": json.loads(row["data_json"]),
        "is_demo": bool(row["is_demo"]),
        "created_at": row["created_at"]
    }

def delete_analysis(record_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def clear_history() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count

def save_meal_plan(profile: dict, plan: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO meal_plans (profile_json, plan_json, created_at)
        VALUES (?, ?, ?)
    """, (json.dumps(profile), json.dumps(plan), now_str))
    plan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return plan_id

def get_latest_meal_plan():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meal_plans ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "profile": json.loads(row["profile_json"]),
        "plan": json.loads(row["plan_json"]),
        "created_at": row["created_at"]
    }

def save_user_profile(profile: dict):
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO user_profile (id, profile_json, updated_at)
        VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            profile_json = excluded.profile_json,
            updated_at = excluded.updated_at
    """, (json.dumps(profile), now_str))
    conn.commit()
    conn.close()

def get_user_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT profile_json FROM user_profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row["profile_json"])

# Initialize schema immediately upon load
init_db()
