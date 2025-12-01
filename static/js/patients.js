// Patients Management JavaScript

function openAddPatientModal() {
    document.getElementById('patientModal').classList.add('active');
    document.getElementById('modalTitle').textContent = 'Add New Patient';
    document.getElementById('patientForm').reset();
    document.getElementById('patientId').value = '';
}

function closePatientModal() {
    document.getElementById('patientModal').classList.remove('active');
}

async function editPatient(id) {
    // For now, just open the modal - in a full implementation, we'd fetch patient data
    openAddPatientModal();
    document.getElementById('modalTitle').textContent = 'Edit Patient';
    document.getElementById('patientId').value = id;
    // TODO: Fetch patient data and populate form
}

async function deletePatient(id) {
    if (!confirm('Are you sure you want to delete this patient?')) {
        return;
    }

    const result = await apiCall(`/patients/${id}/delete`, 'DELETE');
    if (result && result.success) {
        showNotification('Patient deleted successfully');
        location.reload();
    }
}

document.getElementById('patientForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const patientId = document.getElementById('patientId').value;
    const data = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        address: document.getElementById('address').value,
        contact: document.getElementById('contact').value,
        medical_history: document.getElementById('medical_history').value,
        assigned_doctor_id: document.getElementById('assigned_doctor_id').value || null
    };

    let result;
    if (patientId) {
        result = await apiCall(`/patients/${patientId}/update`, 'PUT', data);
    } else {
        result = await apiCall('/patients/add', 'POST', data);
    }

    if (result && result.success) {
        showNotification('Patient saved successfully');
        location.reload();
    }
});

// Close modal when clicking outside
document.getElementById('patientModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'patientModal') {
        closePatientModal();
    }
});
