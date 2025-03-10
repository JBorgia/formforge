import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

# Load the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Create a connection to the Supabase PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.get("/db-test")
def test_db():
    """Test the database connection by retrieving the current timestamp."""
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    db_time = cursor.fetchone()
    conn.close()
    
    return {"database_time": db_time[0]}
