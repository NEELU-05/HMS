from datetime import datetime
from sqlalchemy import or_

class ContextBuilder:
    """Build relevant context from database for AI queries."""
    
    @staticmethod
    def get_context(user_message: str) -> dict:
        from app import Patient, Doctor, Appointment, Billing
        
        context = {}
        msg = user_message.lower()
        
        # 1. Patient Search Context
        if any(w in msg for w in ['patient', 'find', 'search', 'who is', 'details']):
            # Simple keyword extraction (naive approach)
            patients = Patient.query.limit(5).all()
            context['recent_patients'] = [
                {
                    'id': p.id,
                    'name': p.name,
                    'age': p.age,
                    'gender': p.gender,
                    'condition': p.medical_history
                } for p in patients
            ]
            
        # 2. Doctor/Appointment Context
        if any(w in msg for w in ['doctor', 'appointment', 'schedule', 'book', 'availab']):
            doctors = Doctor.query.all()
            context['doctors'] = [
                {
                    'name': d.name,
                    'specialization': d.specialization,
                    'schedule': d.schedule
                } for d in doctors
            ]
            
            today = datetime.now().strftime('%Y-%m-%d')
            todays_appts = Appointment.query.filter_by(appointment_date=today).all()
            context['todays_appointments'] = [
                {
                    'patient': a.patient.name,
                    'doctor': a.doctor.name,
                    'time': a.appointment_time,
                    'status': a.status
                } for a in todays_appts
            ]

        # 3. Statistics Context
        if any(w in msg for w in ['stats', 'how many', 'total', 'count', 'overview']):
            context['statistics'] = {
                'total_patients': Patient.query.count(),
                'total_doctors': Doctor.query.count(),
                'total_appointments': Appointment.query.count(),
                'pending_bills': Billing.query.filter_by(status='Pending').count()
            }
            
        return context
