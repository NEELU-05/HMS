// Appointments Management JavaScript

function openAddAppointmentModal() {
    document.getElementById('appointmentModal').classList.add('active');
    document.getElementById('appointmentForm').reset();
}

function closeAppointmentModal() {
    document.getElementById('appointmentModal').classList.remove('active');
}

async function cancelAppointment(id) {
    if (!confirm('Are you sure you want to cancel this appointment?')) {
        return;
    }

    const result = await apiCall(`/appointments/${id}/cancel`, 'PUT');
    if (result && result.success) {
        showNotification('Appointment cancelled successfully');
        location.reload();
    }
}

document.getElementById('appointmentForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const timeInput = document.getElementById('appointment_time').value;
    const [hours, minutes] = timeInput.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour > 12 ? hour - 12 : (hour === 0 ? 12 : hour);
    const formattedTime = `${displayHour.toString().padStart(2, '0')}:${minutes} ${ampm}`;

    const data = {
        patient_id: parseInt(document.getElementById('patient_id').value),
        doctor_id: parseInt(document.getElementById('doctor_id').value),
        appointment_date: document.getElementById('appointment_date').value,
        appointment_time: formattedTime,
        status: 'Scheduled'
    };

    const result = await apiCall('/appointments/add', 'POST', data);

    if (result && result.success) {
        showNotification('Appointment booked successfully');
        location.reload();
    }
});

// Close modal when clicking outside
document.getElementById('appointmentModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'appointmentModal') {
        closeAppointmentModal();
    }
});
