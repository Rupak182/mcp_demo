# Smart Doctor Assistant API

FastAPI-based doctor appointment system with AI assistant using Model Context Protocol (MCP).

<img width="1330" height="992" alt="image" src="https://github.com/user-attachments/assets/33532c3a-b595-4ad3-8bd8-36789e324706" />


<img width="1559" height="978" alt="image" src="https://github.com/user-attachments/assets/89d49110-310a-4238-b163-db140a6c62be" />




## Features

- AI assistant for appointment management
- Doctor availability checking
- Appointment scheduling
- Patient symptom reporting
- PostgreSQL database
- Docker support

## Prerequisites

- Python 
- Docker and Docker Compose
- PostgreSQL (via Docker)

## Setup with Virtual Environment (Recommended)

### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

```

### Linux/Mac
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate


```

## Quick Start

1. **Create & activate virtual environment** (see above)
2. **Install dependencies**: 
   ```bash
   pip install fastapi sqlalchemy python-dotenv pydantic[email]
   ```
3. **Start database**: `docker-compose up -d`
3. **Setup environment**: Create `.env` with:
   ```
   DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/doctordb
   ```
4. **Initialize database & sample data**: `python seed.py`
5. **Run app**: `python -m uvicorn main2:app --reload`

API: `http://localhost:8000` | Docs: `http://localhost:8000/docs`

## API Endpoints (MCP Tools)

### 1. Check Availability
`GET /api/availability/Dr.%20Smith?appointment_date=2025-08-04`

Returns: `["09:00", "09:30", "10:00", "14:00", "14:30"]`

### 2. Schedule Appointment
`POST /api/appointments`
```json
{
  "doctor_name": "Dr. Smith",
  "patient_name": "John Doe",
  "patient_email": "john@email.com",
  "start_time": "2025-08-04T14:00:00",
  "reason": "Checkup"
}
```

### 3. Symptom Reports
`GET /api/reports/symptoms?symptom=fever&days_ago=7`

## VS Code MCP Integration

When using VS Code as an MCP client, you can ask natural language questions that will use these API endpoints:

### Sample Queries for VS Code MCP

**Check Doctor Availability:**
```
"What times is Dr. Smith available on August 7th, 2025?"
```
*Uses: check_doctor_availability tool*

**Schedule Appointments:**
```
"Book an appointment for John Smith with Dr. Alice on Friday at 3 PM for treatment of fever"
```
*Uses: schedule_appointment tool*

**Find Patients by Symptoms:**
```
"Show me patients who visited for general checkup in the last 7 days"
```
*Uses: get_patients_by_symptom tool*



## Database

**Entities**: Doctors, Patients, Availability, Appointments

**Sample Data** (via `seed.py`):
- 2 doctors: Dr. Smith, Dr. Alice  
- Schedule: Monday-Friday, 9 AM - 5 PM
- 2 patients: John Doe, Jane Roe
- 30-minute appointment slots

## Development

- **Run**: `python -m uvicorn main2:app --reload`
- **Reset DB**: `docker-compose down && docker-compose up -d && python seed.py`
- **Re-seed data**: `python seed.py`

## Docker
```bash
docker-compose up -d  # Start
docker-compose down   # Stop
```
