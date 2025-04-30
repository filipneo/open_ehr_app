from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Patient
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    sex: str
    identifier: str


# Composition
class CompositionCreate(BaseModel):
    patient_id: int
    start_time: datetime
    version: Optional[int] = 1


# Specimen
class SpecimenCreate(BaseModel):
    specimen_type: str
    collection_time: datetime
    snomed_code: Optional[str] = None
    description: Optional[str] = None
    version: Optional[int] = 1


# Lab Test
class LabTestCreate(BaseModel):
    composition_id: int
    specimen_id: int
    loinc_code: Optional[str] = None
    version: Optional[int] = 1


# Lab Analyte Result
class LabAnalyteResultCreate(BaseModel):
    lab_test_id: int
    loinc_code: str
    value: float
    unit: str
    reference_low: Optional[float] = None
    reference_high: Optional[float] = None
    interpretation: Optional[str] = None
    version: Optional[int] = 1


# CBC Panel
class CBCPanelCreate(BaseModel):
    lab_test_id: int
    hemoglobin_id: Optional[int] = None
    white_cell_id: Optional[int] = None
    platelet_id: Optional[int] = None
    version: Optional[int] = 1


# Blood Type Panel
class BloodTypePanelCreate(BaseModel):
    lab_test_id: int
    abo_id: Optional[int] = None
    rh_id: Optional[int] = None
    version: Optional[int] = 1


# Body Measurement
class BodyMeasurementCreate(BaseModel):
    patient_id: int
    record_time: datetime
    value: float
    unit: str
    snomed_code: str
    version: Optional[int] = 1


# Reference Range
class ReferenceRangeCreate(BaseModel):
    loinc_code: str
    low: Optional[float] = None
    high: Optional[float] = None
    unit: Optional[str] = None
    version: Optional[int] = 1
