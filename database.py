# backend/app/database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Date, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Models
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    availabilities = relationship("Availability", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    appointments = relationship("Appointment", back_populates="patient")

class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("Doctor", back_populates="availabilities")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    reason = Column(Text)
    status = Column(String, default="scheduled")
    google_calendar_event_id = Column(String)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

# Function to create tables
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()