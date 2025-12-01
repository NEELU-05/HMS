// Doctors Management JavaScript

function openAddDoctorModal() {
    document.getElementById('doctorModal').classList.add('active');
    document.getElementById('doctorForm').reset();
}

function closeDoctorModal() {
    document.getElementById('doctorModal').classList.remove('active');
}

async function deleteDoctor(id) {
    if (!confirm('Are you sure you want to delete this doctor?')) {
        return;
    }

    const result = await apiCall(`/doctors/${id}/delete`, 'DELETE');
    if (result && result.success) {
        showNotification('Doctor deleted successfully');
        location.reload();
    }
}

document.getElementById('doctorForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById('name').value,
        specialization: document.getElementById('specialization').value,
        schedule: document.getElementById('schedule').value
    };

    const result = await apiCall('/doctors/add', 'POST', data);

    if (result && result.success) {
        showNotification('Doctor added successfully');
        location.reload();
    }
});

// Close modal when clicking outside
document.getElementById('doctorModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'doctorModal') {
        closeDoctorModal();
    }
});
