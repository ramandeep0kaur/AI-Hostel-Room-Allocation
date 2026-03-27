import sqlite3

def connect_db():

    conn = sqlite3.connect("room_allocation.db")
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        department TEXT,
        roll_no TEXT,
        userid TEXT,
        phone TEXT,
        room_no TEXT,
        year INTEGER,i8m
        study_time TEXT,
        dietary TEXT,
        cleanliness TEXT
    )
    """)

    # ---------------- ROOMS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms(
        room_no TEXT PRIMARY KEY,
        capacity INTEGER,
        floor INTEGER,
        beds TEXT
    )
    """)

     # ---------------- ROOM REQUESTS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS room_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        room_no TEXT,
        bed_no TEXT,
        reason TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # ---------------- NOTIFICATIONS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT
    )
    """)

    # ---------------- COMPLAINTS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        type TEXT,
        description TEXT,
        complaint TEXT,
        category TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)
    

    conn.commit()
    return conn, cursor