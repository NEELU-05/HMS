from modules import billing

billing.add_billing(1, 1500.50, "2025-10-15")

print("All billing records:", billing.get_all_billing())

billing.update_billing(1, status="Paid")
billing.delete_billing(2)

print("Billing after update/delete:", billing.get_all_billing())
