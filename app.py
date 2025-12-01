from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-fallback')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    medical_history = db.Column(db.Text)
    assigned_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.String(20), nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    services = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    billing_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')
    
    patient = db.relationship('Patient', backref='bills')

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    today = datetime.now().strftime('%Y-%m-%d')
    todays_appointments = Appointment.query.filter_by(appointment_date=today).all()
    pending_bills = Billing.query.filter_by(status='Pending').all()
    total_pending = sum(bill.amount for bill in pending_bills)
    
    return render_template('dashboard.html',
                         total_patients=total_patients,
                         total_doctors=total_doctors,
                         todays_appointments=todays_appointments,
                         total_pending=total_pending)

@app.route('/patients')
def patients():
    all_patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('patients.html', patients=all_patients, doctors=doctors)

@app.route('/patients/add', methods=['POST'])
def add_patient():
    data = request.json
    patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        address=data['address'],
        contact=data['contact'],
        medical_history=data.get('medical_history', ''),
        assigned_doctor_id=data.get('assigned_doctor_id')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'success': True, 'id': patient.id})

@app.route('/patients/<int:id>/update', methods=['PUT'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    data = request.json
    patient.name = data['name']
    patient.age = data['age']
    patient.gender = data['gender']
    patient.address = data['address']
    patient.contact = data['contact']
    patient.medical_history = data.get('medical_history', '')
    patient.assigned_doctor_id = data.get('assigned_doctor_id')
    db.session.commit()
    return jsonify({'success': True})

@app.route('/patients/<int:id>/delete', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/doctors/add', methods=['POST'])
def add_doctor():
    data = request.json
    doctor = Doctor(
        name=data['name'],
        specialization=data['specialization'],
        schedule=data['schedule']
    )
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'success': True, 'id': doctor.id})

@app.route('/doctors/<int:id>/delete', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.all()
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointments.html', appointments=all_appointments, patients=patients, doctors=doctors)

@app.route('/appointments/add', methods=['POST'])
def add_appointment():
    data = request.json
    appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_date=data['appointment_date'],
        appointment_time=data['appointment_time'],
        status=data.get('status', 'Scheduled')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'success': True, 'id': appointment.id})

@app.route('/appointments/<int:id>/cancel', methods=['PUT'])
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'Cancelled'
    db.session.commit()
    return jsonify({'success': True})

@app.route('/billing')
def billing():
    all_bills = Billing.query.all()
    patients = Patient.query.all()
    return render_template('billing.html', bills=all_bills, patients=patients)

@app.route('/billing/add', methods=['POST'])
def add_bill():
    data = request.json
    bill = Billing(
        patient_id=data['patient_id'],
        services=data['services'],
        amount=data['amount'],
        status=data.get('status', 'Pending')
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify({'success': True, 'id': bill.id})

@app.route('/billing/<int:id>/pay', methods=['PUT'])
def pay_bill(id):
    bill = Billing.query.get_or_404(id)
    bill.status = 'Paid'
    db.session.commit()
    return jsonify({'success': True})

# AI Chat Route
print("Initializing AI Chat Route...")
from ai_assistant.ai_service import AIAssistant
from ai_assistant.context_builder import ContextBuilder

# Initialize AI (lazy loading to avoid startup errors if key is missing)
ai_assistant = None

@app.route('/ai/chat', methods=['POST'])
def ai_chat():
    global ai_assistant
    try:
        if not ai_assistant:
            ai_assistant = AIAssistant()
            
        data = request.json
        user_message = data.get('message', '')
        
        # Build context
        context = ContextBuilder.get_context(user_message)
        
        # Get response
        response = ai_assistant.chat(user_message, context)
        
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        error_msg = str(e).lower()
        
        # Check if it's a quota/rate limit error
        if 'quota' in error_msg or 'rate limit' in error_msg or '429' in error_msg or 'resource_exhausted' in error_msg:
            return jsonify({
                'success': True,  # Still return success so UI shows the message
                'response': "🚫 **Free tier limit reached!**\n\nI've used up my daily quota. Please try again tomorrow, or consider upgrading to a paid API plan for unlimited access.\n\nIn the meantime, you can still use all other HMS features! 😊"
            })
        
        # For other errors, show a generic message
        print(f"Error in AI chat: {e}")
        return jsonify({
            'success': True,
            'response': "⚠️ I'm having trouble connecting right now. Please try again in a moment."
        })

def init_db():
    with app.app_context():
        db.create_all()
        
        # Seed data if empty
        if Doctor.query.count() == 0:
            doctors = [
                Doctor(name="Dr. Ava Chen", specialization="Cardiology", schedule="Mon-Fri 9AM-5PM"),
                Doctor(name="Dr. Ben Carter", specialization="Neurology", schedule="Tue-Thu 10AM-4PM"),
                Doctor(name="Dr. Emily Carter", specialization="Pediatrics", schedule="Mon-Wed-Fri 8AM-2PM"),
                Doctor(name="Dr. Leo Martinez", specialization="Orthopedics", schedule="Mon-Fri 9AM-3PM")
            ]
            for doc in doctors:
                db.session.add(doc)
            
            patients = [
                Patient(name="Liam Johnson", age=35, gender="Male", address="123 Oak St", contact="555-0101", medical_history="Hypertension", assigned_doctor_id=1),
                Patient(name="Noah Williams", age=28, gender="Male", address="456 Pine Ave", contact="555-0102", medical_history="None", assigned_doctor_id=2),
                Patient(name="Olivia Brown", age=42, gender="Female", address="789 Elm Rd", contact="555-0103", medical_history="Diabetes", assigned_doctor_id=3),
                Patient(name="Emma Jones", age=31, gender="Female", address="321 Maple Dr", contact="555-0104", medical_history="Asthma", assigned_doctor_id=4),
                Patient(name="James Davis", age=55, gender="Male", address="654 Cedar Ln", contact="555-0105", medical_history="Arthritis", assigned_doctor_id=1)
            ]
            for pat in patients:
                db.session.add(pat)
            
            today = datetime.now().strftime('%Y-%m-%d')
            appointments = [
                Appointment(patient_id=1, doctor_id=1, appointment_date=today, appointment_time="09:30 AM", status="Scheduled"),
                Appointment(patient_id=2, doctor_id=2, appointment_date=today, appointment_time="10:00 AM", status="Completed"),
                Appointment(patient_id=3, doctor_id=3, appointment_date=today, appointment_time="11:15 AM", status="Scheduled"),
                Appointment(patient_id=4, doctor_id=4, appointment_date=today, appointment_time="01:00 PM", status="Cancelled"),
                Appointment(patient_id=5, doctor_id=1, appointment_date=today, appointment_time="02:30 PM", status="Scheduled")
            ]
            for appt in appointments:
                db.session.add(appt)
            
            db.session.commit()
            print("Database seeded successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000, threaded=False, use_reloader=False)
