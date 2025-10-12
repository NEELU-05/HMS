import sqlite3
from database.db_init import create_connection

# Add a new appointment
def add_appointment(patient_id, doctor_id, date, time, status="Scheduled"):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, doctor_id, date, time, status))
        conn.commit()
        print(f"[INFO] Appointment for patient {patient_id} with doctor {doctor_id} added successfully.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

# Get appointment by ID
def get_appointment_by_id(appointment_id):
    conn = create_connection()
    appointment = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
        appointment = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return appointment

# List all appointments
def get_all_appointments():
    conn = create_connection()
    appointments = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return appointments

# Update appointment
def update_appointment(appointment_id, patient_id=None, doctor_id=None, date=None, time=None, status=None):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if patient_id:
            updates.append("patient_id=?")
            params.append(patient_id)
        if doctor_id:
            updates.append("doctor_id=?")
            params.append(doctor_id)
        if date:
            updates.append("date=?")
            params.append(date)
        if time:
            updates.append("time=?")
            params.append(time)
        if status:
            updates.append("status=?")
            params.append(status)

        params.append(appointment_id)
        cursor.execute(f"UPDATE appointments SET {', '.join(updates)} WHERE id=?", params)
        conn.commit()
        print(f"[INFO] Appointment ID {appointment_id} updated.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

# Delete appointment
def delete_appointment(appointment_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        conn.commit()
        print(f"[INFO] Appointment ID {appointment_id} deleted.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
