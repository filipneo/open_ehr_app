from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.initialize_db import initialize_database
from app.routers import (
    blood_type_panel,
    body_measurement,
    cbc_panel,
    composition,
    lab_analyte,
    lab_test,
    patient,
    reference_range,
    specimen,
)

app = FastAPI(title="EHR API", version="1.0.0", description="A simple electronic health record API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database (create tables and populate if empty)
initialize_database()

# Include routers
app.include_router(patient.router)
app.include_router(composition.router)
app.include_router(specimen.router)
app.include_router(lab_test.router)
app.include_router(lab_analyte.router)
app.include_router(cbc_panel.router)
app.include_router(blood_type_panel.router)
app.include_router(body_measurement.router)
app.include_router(reference_range.router)
