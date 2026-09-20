import sqlite3

DATABASE_NAME = "travelpilot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            budget REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            travelers INTEGER DEFAULT 1,
            interests TEXT,
            preferences TEXT,
            hotel_name TEXT,
            hotel_location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER,
            cost REAL DEFAULT 0,
            category TEXT,
            priority TEXT,
            travel_from_previous INTEGER DEFAULT 0,
            status TEXT DEFAULT 'scheduled',
            FOREIGN KEY (trip_id) REFERENCES trips(id)
        )
    """)

    connection.commit()
    connection.close()