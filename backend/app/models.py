from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# =========================
# MAIN TABLES (LATEST ONLY)
# =========================


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    sex = Column(String(255), nullable=False)
    identifier = Column(String(255), nullable=False)
    version = Column(Integer, default=1)


class Composition(Base):
    __tablename__ = "composition"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    version = Column(Integer, default=1)


class Specimen(Base):
    __tablename__ = "specimen"
    id = Column(Integer, primary_key=True, autoincrement=True)
    specimen_type = Column(String(255), nullable=False)
    collection_time = Column(DateTime, nullable=False)
    snomed_code = Column(String(20))
    description = Column(String(255))
    version = Column(Integer, default=1)


class LabTest(Base):
    __tablename__ = "lab_test"
    id = Column(Integer, primary_key=True, autoincrement=True)
    composition_id = Column(Integer, ForeignKey("composition.id"), nullable=False)
    specimen_id = Column(Integer, ForeignKey("specimen.id"), nullable=False)
    loinc_code = Column(String(20))
    description = Column(String(255))
    version = Column(Integer, default=1)


class LabAnalyteResult(Base):
    __tablename__ = "lab_analyte_result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lab_test_id = Column(Integer, ForeignKey("lab_test.id"), nullable=False)
    loinc_code = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    reference_low = Column(Float)
    reference_high = Column(Float)
    interpretation = Column(String(20))
    version = Column(Integer, default=1)


class BodyMeasurement(Base):
    __tablename__ = "body_measurement"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    record_time = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    snomed_code = Column(String(20), nullable=False)
    version = Column(Integer, default=1)


class ReferenceRange(Base):
    __tablename__ = "reference_range"
    loinc_code = Column(String(20), primary_key=True)
    low = Column(Float)
    high = Column(Float)
    unit = Column(String(20))
    version = Column(Integer, default=1)


# =========================
# HISTORY TABLES (ARCHIVED)
# =========================


class PatientHistory(Base):
    __tablename__ = "patient_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    sex = Column(String(255), nullable=False)
    identifier = Column(String(255), nullable=False)
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


class CompositionHistory(Base):
    __tablename__ = "composition_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    composition_id = Column(Integer, ForeignKey("composition.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


class SpecimenHistory(Base):
    __tablename__ = "specimen_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    specimen_id = Column(Integer, ForeignKey("specimen.id"), nullable=False)
    specimen_type = Column(String(255), nullable=False)
    collection_time = Column(DateTime, nullable=False)
    snomed_code = Column(String(20))
    description = Column(String(255))
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


class LabTestHistory(Base):
    __tablename__ = "lab_test_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lab_test_id = Column(Integer, ForeignKey("lab_test.id"), nullable=False)
    composition_id = Column(Integer, ForeignKey("composition.id"), nullable=False)
    specimen_id = Column(Integer, ForeignKey("specimen.id"), nullable=False)
    loinc_code = Column(String(20))
    description = Column(String(255))
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


class LabAnalyteResultHistory(Base):
    __tablename__ = "lab_analyte_result_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lab_analyte_result_id = Column(Integer, ForeignKey("lab_analyte_result.id"), nullable=False)
    lab_test_id = Column(Integer, ForeignKey("lab_test.id"), nullable=False)
    loinc_code = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    reference_low = Column(Float)
    reference_high = Column(Float)
    interpretation = Column(String(20))
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


class BodyMeasurementHistory(Base):
    __tablename__ = "body_measurement_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    body_measurement_id = Column(Integer, ForeignKey("body_measurement.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    record_time = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    snomed_code = Column(String(20), nullable=False)
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ReferenceRangeHistory(Base):
    __tablename__ = "reference_range_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_range_loinc_code = Column(
        String(20), ForeignKey("reference_range.loinc_code"), nullable=False
    )
    loinc_code = Column(String(20), nullable=False)
    low = Column(Float)
    high = Column(Float)
    unit = Column(String(20))
    version = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)
