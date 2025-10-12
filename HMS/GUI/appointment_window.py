import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Handle PyInstaller path for database
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))
from modules import appointment, patient, doctor

class AppointmentWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Appointment Management")
        self.geometry("900x500")
        self.resizable(False, False)

        tk.Label(self, text="Appointment Management", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Doctor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Dropdowns for patients and doctors
        self.patients = patient.get_all_patients()
        self.patient_map = {f"{p[1]} (ID:{p[0]})": p[0] for p in self.patients}
        self.patient_combo = ttk.Combobox(form_frame, values=list(self.patient_map.keys()))
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)

        self.doctors = doctor.get_all_doctors()
        self.doctor_map = {f"{d[1]} (ID:{d[0]})": d[0] for d in self.doctors}
        self.doctor_combo = ttk.Combobox(form_frame, values=list(self.doctor_map.keys()))
        self.doctor_combo.grid(row=1, column=1, padx=5, pady=5)

        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.time_entry = tk.Entry(form_frame)
        self.time_entry.grid(row=3, column=1, padx=5, pady=5)
        self.status_entry = tk.Entry(form_frame)
        self.status_entry.grid(row=4, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Add Appointment", width=15, command=self.add_appointment).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Appointment", width=15, command=self.update_appointment).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Appointment", width=15, command=self.delete_appointment).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh List", width=15, command=self.load_appointments).grid(row=0, column=3, padx=5)

        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)
        columns = ("ID", "Patient", "Doctor", "Date", "Time", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        self.tree.pack(side="left", fill="y")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_appointments()

    def load_appointments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        all_apps = appointment.get_all_appointments()
        for a in all_apps:
            p = patient.get_patient_by_id(a[1])
            patient_name = p[1] if p else f"Unknown(ID:{a[1]})"
            d = doctor.get_doctor_by_id(a[2])
            doctor_name = d[1] if d else f"Unknown(ID:{a[2]})"
            self.tree.insert("", "end", values=(a[0], patient_name, doctor_name, a[3], a[4], a[5]))

    def add_appointment(self):
        patient_key = self.patient_combo.get()
        doctor_key = self.doctor_combo.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        status = self.status_entry.get() or "Scheduled"
        if not patient_key or not doctor_key or not date or not time:
            messagebox.showwarning("Input Error", "All fields except status are required")
            return
        patient_id = self.patient_map[patient_key]
        doctor_id = self.doctor_map[doctor_key]
        appointment.add_appointment(patient_id, doctor_id, date, time, status)
        self.load_appointments()

    def update_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select an appointment to update")
            return
        appointment_id = self.tree.item(selected[0])["values"][0]
        patient_key = self.patient_combo.get()
        doctor_key = self.doctor_combo.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        status = self.status_entry.get()
        patient_id = self.patient_map[patient_key] if patient_key else None
        doctor_id = self.doctor_map[doctor_key] if doctor_key else None
        appointment.update_appointment(appointment_id, patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, status=status)
        self.load_appointments()

    def delete_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select an appointment to delete")
            return
        appointment_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?"):
            appointment.delete_appointment(appointment_id)
            self.load_appointments()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = AppointmentWindow()
    win.mainloop()
