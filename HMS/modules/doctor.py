import sqlite3
from database.db_init import create_connection

# Add a new doctor
def add_doctor(name, specialization, contact, availability="Available"):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO doctors (name, specialization, contact, availability)
            VALUES (?, ?, ?, ?)
        """, (name, specialization, contact, availability))
        conn.commit()
        print(f"[INFO] Doctor '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

# Get doctor by ID
def get_doctor_by_id(doctor_id):
    conn = create_connection()
    doctor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        doctor = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return doctor

# List all doctors
def get_all_doctors():
    conn = create_connection()
    doctors = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return doctors

# Update doctor details
def update_doctor(doctor_id, name=None, specialization=None, contact=None, availability=None):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if name:
            updates.append("name=?")
            params.append(name)
        if specialization:
            updates.append("specialization=?")
            params.append(specialization)
        if contact:
            updates.append("contact=?")
            params.append(contact)
        if availability:
            updates.append("availability=?")
            params.append(availability)

        params.append(doctor_id)
        cursor.execute(f"UPDATE doctors SET {', '.join(updates)} WHERE id=?", params)
        conn.commit()
        print(f"[INFO] Doctor ID {doctor_id} updated.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

# Delete a doctor
def delete_doctor(doctor_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
        conn.commit()
        print(f"[INFO] Doctor ID {doctor_id} deleted.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
