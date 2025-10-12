import sqlite3
from database.db_init import create_connection

def add_patient(name, age, gender, contact, medical_history):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (name, age, gender, contact, medical_history)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, contact, medical_history))
        conn.commit()
        print(f"[INFO] Patient '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()


def get_patient_by_id(patient_id):
    conn = create_connection()
    patient = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return patient


def get_all_patients():
    conn = create_connection()
    patients = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return patients


def update_patient(patient_id, name=None, age=None, gender=None, contact=None, medical_history=None):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if name:
            updates.append("name=?")
            params.append(name)
        if age is not None:
            updates.append("age=?")
            params.append(age)
        if gender:
            updates.append("gender=?")
            params.append(gender)
        if contact:
            updates.append("contact=?")
            params.append(contact)
        if medical_history:
            updates.append("medical_history=?")
            params.append(medical_history)

        params.append(patient_id)
        cursor.execute(f"UPDATE patients SET {', '.join(updates)} WHERE id=?", params)
        conn.commit()
        print(f"[INFO] Patient ID {patient_id} updated.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()


def delete_patient(patient_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        conn.commit()
        print(f"[INFO] Patient ID {patient_id} deleted.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
