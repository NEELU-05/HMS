import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# -----------------------------
# Handle PyInstaller bundled path
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Add modules folder to path
sys.path.append(os.path.join(BASE_DIR, "modules"))

# Import patient module
from modules import patient

class PatientWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Patient Management")
        self.geometry("700x500")
        self.resizable(False, False)

        tk.Label(self, text="Patient Management", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="e")
        tk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky="e")
        tk.Label(form_frame, text="Contact:").grid(row=3, column=0, sticky="e")
        tk.Label(form_frame, text="Medical History:").grid(row=4, column=0, sticky="e")

        self.name_entry = tk.Entry(form_frame)
        self.age_entry = tk.Entry(form_frame)
        self.gender_entry = tk.Entry(form_frame)
        self.contact_entry = tk.Entry(form_frame)
        self.medical_entry = tk.Entry(form_frame)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5)
        self.contact_entry.grid(row=3, column=1, padx=5, pady=5)
        self.medical_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Patient", width=15, command=self.add_patient).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Patient", width=15, command=self.update_patient).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Patient", width=15, command=self.delete_patient).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh List", width=15, command=self.load_patients).grid(row=0, column=3, padx=5)

        # Table
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)

        columns = ("ID", "Name", "Age", "Gender", "Contact", "Medical History")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_patients()

    # -----------------------------
    def load_patients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in patient.get_all_patients():
            self.tree.insert("", "end", values=p)

    def add_patient(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        contact = self.contact_entry.get()
        medical = self.medical_entry.get()

        if not name or not age:
            messagebox.showwarning("Input Error", "Name and Age are required")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a number")
            return

        patient.add_patient(name, age, gender, contact, medical)
        self.load_patients()

    def update_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a patient to update")
            return
        patient_id = self.tree.item(selected[0])["values"][0]

        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        contact = self.contact_entry.get()
        medical = self.medical_entry.get()

        try:
            age = int(age) if age else None
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a number")
            return

        patient.update_patient(patient_id, name=name, age=age, gender=gender, contact=contact, medical_history=medical)
        self.load_patients()

    def delete_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a patient to delete")
            return
        patient_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?"):
            patient.delete_patient(patient_id)
            self.load_patients()


# Run independently for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = PatientWindow()
    win.mainloop()
