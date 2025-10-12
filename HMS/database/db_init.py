import sqlite3
from sqlite3 import Error
import os
import sys

# Determine base directory (normal run vs PyInstaller bundle)
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "hospital.db")

def create_connection():
    """Create a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"[INFO] Connected to database '{DB_PATH}' successfully.")
    except Error as e:
        print(f"[ERROR] Cannot connect to database: {e}")
    return conn

def create_tables(conn):
    """Create all necessary tables."""
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER CHECK(age >= 0),
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
            contact TEXT UNIQUE NOT NULL,
            medical_history TEXT
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            contact TEXT UNIQUE NOT NULL,
            availability TEXT CHECK(availability IN ('Available', 'Unavailable')) NOT NULL DEFAULT 'Available'
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT CHECK(status IN ('Scheduled', 'Completed', 'Cancelled')) NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY(doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            amount REAL CHECK(amount >= 0),
            date TEXT NOT NULL,
            status TEXT CHECK(status IN ('Paid', 'Unpaid')) NOT NULL DEFAULT 'Unpaid',
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );""")

        conn.commit()
        print("[INFO] All tables created successfully.")
    except Error as e:
        print(f"[ERROR] Error creating tables: {e}")
        conn.rollback()

def insert_sample_data(conn):
    """Insert basic sample data."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO patients (name, age, gender, contact, medical_history)
            VALUES 
            ('John Doe', 35, 'Male', '0171234567', 'Diabetes Type 2'),
            ('Sarah Ali', 28, 'Female', '0181234567', 'Allergy - Penicillin');
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO doctors (name, specialization, contact, availability)
            VALUES 
            ('Dr. A. Rahman', 'Cardiologist', '0151234567', 'Available'),
            ('Dr. Priya Sen', 'Dermatologist', '0161234567', 'Unavailable');
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO appointments (patient_id, doctor_id, date, time, status)
            VALUES 
            (1, 1, '2025-10-12', '10:30', 'Scheduled'),
            (2, 2, '2025-10-13', '12:00', 'Scheduled');
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO billing (patient_id, amount, date, status)
            VALUES 
            (1, 1200.50, '2025-10-12', 'Paid'),
            (2, 800.00, '2025-10-13', 'Unpaid');
        """)

        conn.commit()
        print("[INFO] Sample data inserted successfully.")
    except Error as e:
        print(f"[ERROR] Error inserting sample data: {e}")
        conn.rollback()

def reset_database():
    """Reset the database by dropping all tables and recreating them."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = OFF;")
            cursor.execute("DROP TABLE IF EXISTS billing;")
            cursor.execute("DROP TABLE IF EXISTS appointments;")
            cursor.execute("DROP TABLE IF EXISTS doctors;")
            cursor.execute("DROP TABLE IF EXISTS patients;")
            conn.commit()
            print("[INFO] Database reset successfully.")
        except Error as e:
            print(f"[ERROR] Error resetting database: {e}")
        finally:
            cursor.execute("PRAGMA foreign_keys = ON;")
            create_tables(conn)
            insert_sample_data(conn)
            conn.close()

def initialize_database():
    """Initialize the database with tables and sample data."""
    conn = create_connection()
    if conn:
        create_tables(conn)
        insert_sample_data(conn)
        conn.close()
        print("[INFO] Database initialization complete.")

if __name__ == "__main__":
    initialize_database()
