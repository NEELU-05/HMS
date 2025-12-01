// Billing Management JavaScript

function openAddBillModal() {
    document.getElementById('billModal').classList.add('active');
    document.getElementById('billForm').reset();
}

function closeBillModal() {
    document.getElementById('billModal').classList.remove('active');
}

async function payBill(id) {
    if (!confirm('Mark this bill as paid?')) {
        return;
    }

    const result = await apiCall(`/billing/${id}/pay`, 'PUT');
    if (result && result.success) {
        showNotification('Bill marked as paid');
        location.reload();
    }
}

document.getElementById('billForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        patient_id: parseInt(document.getElementById('patient_id').value),
        services: document.getElementById('services').value,
        amount: parseFloat(document.getElementById('amount').value),
        status: 'Pending'
    };

    const result = await apiCall('/billing/add', 'POST', data);

    if (result && result.success) {
        showNotification('Bill generated successfully');
        location.reload();
    }
});

// Close modal when clicking outside
document.getElementById('billModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'billModal') {
        closeBillModal();
    }
});
