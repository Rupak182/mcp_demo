# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, date, time

# Availability
class AvailabilityOut(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time

# Appointments
class AppointmentCreate(BaseModel):
    doctor_name: str
    patient_name: str
    patient_email: EmailStr
    start_time: datetime
    reason: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    doctor_name: str
    patient_name: str
    start_time: datetime
    end_time: datetime
    reason: Optional[str]
    status: str

# Reports
class AppointmentStats(BaseModel):
    date: date
    total_appointments: int
    completed_appointments: int

class PatientSymptomReport(BaseModel):
    patient_name: str
    appointment_date: datetime
    reason_for_visit: Optional[str]

# Agent Invocation
class AgentRequest(BaseModel):
    prompt: str
    session_id: str
    conversation_history: List[dict] = []

class AgentResponse(BaseModel):
    response: str