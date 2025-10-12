import tkinter as tk
from tkinter import messagebox
import sys
import os

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "modules"))

from GUI.patient_window import PatientWindow
from GUI.doctor_window import DoctorWindow
from GUI.appointment_window import AppointmentWindow
from GUI.billing_window import BillingWindow
from modules import patient, doctor, appointment, billing

class MainDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hospital Management System")
        self.geometry("600x400")
        self.resizable(False, False)

        title_label = tk.Label(self, text="Hospital Management System", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="Patients", width=20, height=2, command=self.open_patient_window).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Doctors", width=20, height=2, command=self.open_doctor_window).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Appointments", width=20, height=2, command=self.open_appointment_window).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Billing", width=20, height=2, command=self.open_billing_window).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Exit", width=20, height=2, bg="red", fg="white", command=self.quit_app).pack(pady=20)

    def open_patient_window(self):
        PatientWindow()

    def open_doctor_window(self):
        DoctorWindow()

    def open_appointment_window(self):
        AppointmentWindow()

    def open_billing_window(self):
        BillingWindow()

    def quit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()
