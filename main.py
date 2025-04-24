from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///./lab_reports.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="CBC Lab Report API",
    description="Backend API for submitting and viewing CBC lab results.",
    version="1.0.0",
)


# Database Models
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(String, unique=True, index=True)
    name_given = Column(String)
    name_family = Column(String)
    birth_date = Column(Date)
    sex = Column(String)
    reports = relationship("Report", back_populates="patient")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    start_time = Column(DateTime)
    report_type = Column(String)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="reports")
    laboratory_test = relationship("LaboratoryTest", uselist=False, back_populates="report")
    height = relationship("Height", uselist=False, back_populates="report")
    weight = relationship("Weight", uselist=False, back_populates="report")


class LaboratoryTest(Base):
    __tablename__ = "laboratory_tests"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    test_name = Column(String)
    report = relationship("Report", back_populates="laboratory_test")
    specimen = relationship("Specimen", uselist=False, back_populates="laboratory_test")
    analytes = relationship("Analyte", back_populates="laboratory_test")


class Specimen(Base):
    __tablename__ = "specimens"
    id = Column(Integer, primary_key=True, index=True)
    laboratory_test_id = Column(Integer, ForeignKey("laboratory_tests.id"))
    specimen_type = Column(String)
    collection_time = Column(DateTime)
    collector_name = Column(String)
    collector_id = Column(String)
    collector_role = Column(String)
    laboratory_test = relationship("LaboratoryTest", back_populates="specimen")


class Analyte(Base):
    __tablename__ = "analytes"
    id = Column(Integer, primary_key=True, index=True)
    laboratory_test_id = Column(Integer, ForeignKey("laboratory_tests.id"))
    name = Column(String)
    value = Column(Float)
    unit = Column(String)
    laboratory_test = relationship("LaboratoryTest", back_populates="analytes")


class Height(Base):
    __tablename__ = "heights"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    value = Column(Float)
    unit = Column(String)
    report = relationship("Report", back_populates="height")


class Weight(Base):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    value = Column(Float)
    unit = Column(String)
    report = relationship("Report", back_populates="weight")


Base.metadata.create_all(bind=engine)


# Pydantic Schemas
class AnalyteCreate(BaseModel):
    name: str
    value: float
    unit: str


class SpecimenCreate(BaseModel):
    specimen_type: str
    collection_time: datetime
    collector_name: str
    collector_id: str
    collector_role: str


class LaboratoryTestCreate(BaseModel):
    test_name: str
    specimen: SpecimenCreate
    analytes: List[AnalyteCreate]


class HeightCreate(BaseModel):
    value: float
    unit: str


class WeightCreate(BaseModel):
    value: float
    unit: str


class ReportCreate(BaseModel):
    name: str
    start_time: datetime
    report_type: str
    laboratory_test: LaboratoryTestCreate
    height: HeightCreate
    weight: WeightCreate


class PatientCreate(BaseModel):
    hospital_id: str
    name_given: str
    name_family: str
    birth_date: datetime
    sex: str


# FastAPI Endpoints


@app.get("/patients/", response_model=List[dict])
def get_all_patients():
    db = SessionLocal()
    patients = db.query(Patient).all()
    db.close()
    return [
        {
            "id": p.id,
            "hospital_id": p.hospital_id,
            "name_given": p.name_given,
            "name_family": p.name_family,
            "birth_date": p.birth_date.isoformat(),
            "sex": p.sex,
        }
        for p in patients
    ]


@app.post("/patients/", response_model=dict)
def create_patient(patient: PatientCreate):
    db = SessionLocal()
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    db.close()
    return {"id": db_patient.id, "hospital_id": db_patient.hospital_id}


@app.post("/patients/{patient_id}/reports/", response_model=dict)
def create_report(patient_id: int, report: ReportCreate):
    db = SessionLocal()
    db_report = Report(
        name=report.name,
        start_time=report.start_time,
        report_type=report.report_type,
        patient_id=patient_id,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    db_test = LaboratoryTest(test_name=report.laboratory_test.test_name, report_id=db_report.id)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)

    specimen = report.laboratory_test.specimen
    db_specimen = Specimen(
        laboratory_test_id=db_test.id,
        specimen_type=specimen.specimen_type,
        collection_time=specimen.collection_time,
        collector_name=specimen.collector_name,
        collector_id=specimen.collector_id,
        collector_role=specimen.collector_role,
    )
    db.add(db_specimen)

    for analyte in report.laboratory_test.analytes:
        db.add(Analyte(laboratory_test_id=db_test.id, **analyte.dict()))

    db_height = Height(report_id=db_report.id, **report.height.dict())
    db_weight = Weight(report_id=db_report.id, **report.weight.dict())
    db.add(db_height)
    db.add(db_weight)

    db.commit()
    db.close()

    return {"report_id": db_report.id, "patient_id": patient_id}
