import sqlite3
from database.db_init import create_connection

# Add a new billing record
def add_billing(patient_id, amount, date, status="Unpaid"):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO billing (patient_id, amount, date, status)
            VALUES (?, ?, ?, ?)
        """, (patient_id, amount, date, status))
        conn.commit()
        print(f"[INFO] Billing record for patient {patient_id} added successfully.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

# Get billing record by ID
def get_billing_by_id(billing_id):
    conn = create_connection()
    billing = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM billing WHERE id = ?", (billing_id,))
        billing = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return billing

# List all billing records
def get_all_billing():
    conn = create_connection()
    bills = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM billing")
        bills = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
    return bills

# Update billing record
def update_billing(billing_id, patient_id=None, amount=None, date=None, status=None):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if patient_id:
            updates.append("patient_id=?")
            params.append(patient_id)
        if amount is not None:
            updates.append("amount=?")
            params.append(amount)
        if date:
            updates.append("date=?")
            params.append(date)
        if status:
            updates.append("status=?")
            params.append(status)

        params.append(billing_id)
        cursor.execute(f"UPDATE billing SET {', '.join(updates)} WHERE id=?", params)
        conn.commit()
        print(f"[INFO] Billing ID {billing_id} updated.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

# Delete billing record
def delete_billing(billing_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM billing WHERE id=?", (billing_id,))
        conn.commit()
        print(f"[INFO] Billing ID {billing_id} deleted.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
