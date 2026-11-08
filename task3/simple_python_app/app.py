import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

def connect_db():
    return psycopg2.connect(
        host=os.getenv("API_DB_HOST", "postgres-db"),
        port=5432,
        dbname=os.getenv("API_DB_NAME", "api"),
        user=os.getenv("API_DB_USER", "apiuser"),
        password=os.environ["API_DB_PASS"]
    )

@app.get("/")
def root():
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
    return {"message": "Hello World", "postgres_version": version}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/items/{name}")
def add_item(name: str):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
            cursor.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (name,))
            item_id = cursor.fetchone()[0]
    return {"id": item_id, "name": name}

@app.get("/items")
def get_items():
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
            cursor.execute("SELECT id, name FROM items ORDER BY id")
            rows = cursor.fetchall()
    return [{"id": r[0], "name": r[1]} for r in rows]
