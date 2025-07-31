from database import SessionLocal, create_db_and_tables
from database import Doctor, Patient, Availability
from datetime import time

db = SessionLocal()
create_db_and_tables()

# ---- Add Doctors ----
doctor1 = Doctor(name="Dr. Smith")
doctor2 = Doctor(name="Dr. Alice")

db.add_all([doctor1, doctor2])
db.commit()

# ---- Add Availability for each Doctor (Mon–Fri, 9am–5pm) ----
for doctor in [doctor1, doctor2]:
    for day in range(5):  # 0=Monday, ..., 4=Friday
        availability = Availability(
            doctor_id=doctor.id,
            day_of_week=day,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        db.add(availability)

db.commit()

# ---- Add Patients ----
patient1 = Patient(name="John Doe", email="john@example.com")
patient2 = Patient(name="Jane Roe", email="jane@example.com")

db.add_all([patient1, patient2])
db.commit()

db.close()
print("Sample data inserted.")
