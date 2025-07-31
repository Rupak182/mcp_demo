from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
typing_import = __import__('typing')
from typing import List, Dict
import os

import database
import schemas
# import services

router = APIRouter()

@router.get(
    "/availability/{doctor_name}",
    response_model=List[str],
    operation_id="check_doctor_availability"
)
def check_doctor_availability(
    doctor_name: str,
    appointment_date: date,
    db: Session = Depends(database.get_db)
) -> List[str]:
    """
    Checks a specific doctor's open appointment slots for a given day.
    Considers their standard availability and existing appointments.
    Returns a list of available start times in 'HH:MM' format.
    """
    # Fetch doctor record
    doctor = (
        db.query(database.Doctor)
        .filter(database.Doctor.name == doctor_name)
        .first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Determine weekday index
    day_of_week = appointment_date.weekday()  # Monday is 0 and Sunday is 6
    availability = (
        db.query(database.Availability)
        .filter_by(doctor_id=doctor.id, day_of_week=day_of_week)
        .first()
    )
    if not availability:
        # No availability defined for this day
        return []

    # Get all appointments for that day
    start_of_day = datetime.combine(appointment_date, datetime.min.time())
    end_of_day = datetime.combine(appointment_date, datetime.max.time())
    appointments = (
        db.query(database.Appointment)
        .filter(
            database.Appointment.doctor_id == doctor.id,
            database.Appointment.start_time >= start_of_day,
            database.Appointment.start_time <= end_of_day,
        )
        .all()
    )
    booked_slots = {appt.start_time.time() for appt in appointments}

    # Generate 30-minute slots
    available_slots: List[str] = []
    current_time = datetime.combine(appointment_date, availability.start_time)
    end_time = datetime.combine(appointment_date, availability.end_time)

    while current_time < end_time:
        if current_time.time() not in booked_slots:
            available_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    return available_slots


@router.post(
    "/appointments",
    response_model=schemas.AppointmentOut,
    operation_id="schedule_appointment"
)
def schedule_appointment(
    request: schemas.AppointmentCreate,
    db: Session = Depends(database.get_db)
) -> schemas.AppointmentOut:
    """
    Books a new appointment. Creates a DB record, Use this only after confirming the desired
    time slot with the user.
    """
    # Fetch doctor record
    doctor = (
        db.query(database.Doctor)
        .filter(database.Doctor.name == request.doctor_name)
        .first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Fetch or create patient record
    patient = (
        db.query(database.Patient)
        .filter(database.Patient.email == request.patient_email)
        .first()
    )
    if not patient:
        patient = database.Patient(
            name=request.patient_name,
            email=request.patient_email,
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

    # Calculate appointment end time
    end_time = request.start_time + timedelta(minutes=30)

    # Create Google Calendar event
    # event_id = services.create_google_calendar_event(
    #     patient_email=patient.email,
    #     doctor_email=os.getenv("DOCTOR_CALENDAR_ID"),
    #     start_time=request.start_time,
    #     end_time=end_time,
    #     reason=request.reason,
    # )

    # Persist appointment in database
    new_appointment = database.Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        start_time=request.start_time,
        end_time=end_time,
        reason=request.reason,
        google_calendar_event_id=100,  # Placeholder for event ID  #change
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # Send confirmation email
    # services.send_confirmation_email(
    #     patient_email=patient.email,
    #     patient_name=patient.name,
    #     doctor_name=doctor.name,
    #     appt_time=request.start_time.strftime("%Y-%m-%d %H:%M %Z"),
    # )

    return schemas.AppointmentOut(
        id=new_appointment.id,
        doctor_name=doctor.name,
        patient_name=patient.name,
        start_time=new_appointment.start_time,
        end_time=new_appointment.end_time,
        reason=new_appointment.reason,
        status=new_appointment.status,
    )


@router.get(
    "/reports/symptoms",
    response_model=List[Dict[str, str]],
    operation_id="get_patients_by_symptom"
)
def get_patients_by_symptom(
    symptom: str,
    days_ago: int,
    db: Session = Depends(database.get_db)
) -> List[Dict[str, str]]:
    """
    Finds a list of patients who visited within a past number of days for a
    specific symptom, like 'fever'.
    """
    # Calculate cutoff datetime
    start_date = datetime.now() - timedelta(days=days_ago)

    # Filter appointments
    appointments = (
        db.query(database.Appointment)
        .filter(
            database.Appointment.reason.ilike(f"%{symptom}%"),
            database.Appointment.start_time >= start_date,
        )
        .all()
    )

    # Build report data
    report: List[Dict[str, str]] = [
        {
            "patient_name": appt.patient.name,
            "patient_email": appt.patient.email,
            "visit_date": appt.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "reason": appt.reason,
        }
        for appt in appointments
    ]

    return report
