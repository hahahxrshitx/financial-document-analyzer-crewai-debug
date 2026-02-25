import sqlite3
from datetime import datetime
import json

DB_NAME = "analysis.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        job_id TEXT PRIMARY KEY,
        file_name TEXT,
        query TEXT,
        status TEXT,
        result TEXT,
        execution_time REAL,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def create_job(job_id, file_name, query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analyses (job_id, file_name, query, status, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (job_id, file_name, query, "processing", datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

def update_job(job_id, status, result=None, execution_time=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE analyses
    SET status=?, result=?, execution_time=?
    WHERE job_id=?
    """, (status, result, execution_time, job_id))

    conn.commit()
    conn.close()

def get_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM analyses WHERE job_id=?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    job = {
        "job_id": row[0],
        "file_name": row[1],
        "query": row[2],
        "status": row[3],
        "result": None,
        "execution_time": row[5],
        "created_at": row[6],
    }

    # Convert JSON string back to dictionary
    if row[4] and job["status"] == "completed":
        try:
            job["result"] = json.loads(row[4])
        except Exception:
            job["result"] = row[4]

    return job