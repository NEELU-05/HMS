import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Handle PyInstaller path for database
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))
from modules import billing, patient

class BillingWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Billing Management")
        self.geometry("800x500")
        self.resizable(False, False)

        tk.Label(self, text="Billing Management", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.patient_entry = tk.Entry(form_frame)
        self.patient_entry.grid(row=0, column=1, padx=5, pady=5)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.status_entry = tk.Entry(form_frame)
        self.status_entry.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Billing", width=15, command=self.add_billing).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Billing", width=15, command=self.update_billing).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Billing", width=15, command=self.delete_billing).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh List", width=15, command=self.load_billing).grid(row=0, column=3, padx=5)

        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)
        columns = ("ID", "Patient ID", "Amount", "Date", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_billing()

    def load_billing(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        all_bills = billing.get_all_billing()
        for b in all_bills:
            self.tree.insert("", "end", values=b)

    def add_billing(self):
        patient_id = self.patient_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        status = self.status_entry.get() or "Unpaid"

        if not patient_id or not amount or not date:
            messagebox.showwarning("Input Error", "Patient ID, Amount, and Date are required")
            return

        try:
            patient_id = int(patient_id)
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Patient ID must be integer and Amount must be a number")
            return

        billing.add_billing(patient_id, amount, date, status)
        self.load_billing()

    def update_billing(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a billing record to update")
            return
        billing_id = self.tree.item(selected[0])["values"][0]

        patient_id = self.patient_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        status = self.status_entry.get()

        try:
            patient_id = int(patient_id) if patient_id else None
            amount = float(amount) if amount else None
        except ValueError:
            messagebox.showwarning("Input Error", "Patient ID must be integer and Amount must be a number")
            return

        billing.update_billing(billing_id, patient_id=patient_id, amount=amount, date=date, status=status)
        self.load_billing()

    def delete_billing(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a billing record to delete")
            return
        billing_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this billing record?"):
            billing.delete_billing(billing_id)
            self.load_billing()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = BillingWindow()
    win.mainloop()
