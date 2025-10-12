import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# ----------------------------
# Handle PyInstaller bundled path
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Add modules folder to path
sys.path.append(os.path.join(BASE_DIR, "modules"))

# Import doctor module
from modules import doctor

class DoctorWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Doctor Management")
        self.geometry("700x500")
        self.resizable(False, False)

        # Title Label
        tk.Label(self, text="Doctor Management", font=("Arial", 16, "bold")).pack(pady=10)

        # Form Frame
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Specialization:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Availability:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.spec_entry = tk.Entry(form_frame)
        self.spec_entry.grid(row=1, column=1, padx=5, pady=5)
        self.contact_entry = tk.Entry(form_frame)
        self.contact_entry.grid(row=2, column=1, padx=5, pady=5)
        self.avail_entry = tk.Entry(form_frame)
        self.avail_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Doctor", width=15, command=self.add_doctor).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Doctor", width=15, command=self.update_doctor).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Doctor", width=15, command=self.delete_doctor).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh List", width=15, command=self.load_doctors).grid(row=0, column=3, padx=5)

        # Table
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)

        columns = ("ID", "Name", "Specialization", "Contact", "Availability")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_doctors()

    # -----------------------------
    def load_doctors(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for d in doctor.get_all_doctors():
            self.tree.insert("", "end", values=d)

    def add_doctor(self):
        name = self.name_entry.get()
        spec = self.spec_entry.get()
        contact = self.contact_entry.get()
        avail = self.avail_entry.get() or "Available"

        if not name or not spec:
            messagebox.showwarning("Input Error", "Name and Specialization are required")
            return

        doctor.add_doctor(name, spec, contact, avail)
        self.load_doctors()

    def update_doctor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a doctor to update")
            return
        doctor_id = self.tree.item(selected[0])["values"][0]

        name = self.name_entry.get()
        spec = self.spec_entry.get()
        contact = self.contact_entry.get()
        avail = self.avail_entry.get()

        doctor.update_doctor(doctor_id, name=name, specialization=spec, contact=contact, availability=avail)
        self.load_doctors()

    def delete_doctor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a doctor to delete")
            return
        doctor_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?"):
            doctor.delete_doctor(doctor_id)
            self.load_doctors()


# Run independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = DoctorWindow()
    win.mainloop()
