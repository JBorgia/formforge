import os
import psycopg2
from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()

# Load the database URLs from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")

def get_db_connection():
    """Create a connection to the Supabase PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def get_mongo_client():
    """Lazy-load MongoDB connection."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5-second timeout
        client.admin.command("ping")  # Test connection
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

@app.get("/db-test")
def test_db():
    """Test PostgreSQL connection."""
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    db_time = cursor.fetchone()
    conn.close()
    
    return {"database_time": db_time[0]}

@app.get("/mongo-test")
def test_mongo():
    """Test MongoDB connection."""
    client = get_mongo_client()
    if not client:
        return {"error": "MongoDB connection failed"}
    
    db = client["formforge"]  # Connect to the correct database
  
