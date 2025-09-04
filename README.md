# Healthcare Backend (Django + DRF + PostgreSQL)

A secure backend for a healthcare application featuring JWT authentication and CRUD for patients, doctors, and patient-doctor mappings.

## Features
- User registration (name, email, password)
- JWT login (access/refresh)
- Patients: CRUD; users only see/manage their own patients
- Doctors: Public GET; auth required for create/update/delete
- Patient-Doctor mappings: assign/unassign, list all (restricted to user's patients), list doctors for a given patient
- PostgreSQL via DATABASE_URL or env vars
- DRF + SimpleJWT configured

## Setup
1. Create and fill `.env` (copy from `.env.example`)
2. Create and activate a virtualenv (Python 3.11+ recommended)
3. Install dependencies:
   pip install -r requirements.txt
4. Apply migrations:
   python manage.py migrate
5. Create a superuser (optional):
   python manage.py createsuperuser
6. Run server:
   python manage.py runserver

## API Overview

- Auth
  - POST /api/auth/register/  {name, email, password}
  - POST /api/auth/login/     {email, password} -> access/refresh
  - POST /api/auth/refresh/   {refresh} -> new access

- Patients (Auth required, limited to owner)
  - POST   /api/patients/
  - GET    /api/patients/
  - GET    /api/patients/:id/
  - PUT    /api/patients/:id/
  - DELETE /api/patients/:id/

- Doctors
  - POST   /api/doctors/        (Auth)
  - GET    /api/doctors/
  - GET    /api/doctors/:id/
  - PUT    /api/doctors/:id/    (Auth)
  - DELETE /api/doctors/:id/    (Auth)

- Mappings (Auth required; only for your patients)
  - POST   /api/mappings/                 {patient, doctor}
  - GET    /api/mappings/                 (only mappings for your patients)
  - GET    /api/mappings/patient/:pid/    doctors for patient
  - DELETE /api/mappings/:id/

Use Authorization: Bearer <access_token> for protected endpoints.
