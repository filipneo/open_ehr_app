from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SexEnum(str, Enum):
    male = "male"
    female = "female"


# =========================
# PATIENT
# =========================
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    sex: SexEnum
    identifier: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# COMPOSITION
# =========================
class CompositionBase(BaseModel):
    patient_id: int
    start_time: datetime


class CompositionCreate(CompositionBase):
    pass


class CompositionUpdate(CompositionBase):
    pass


class Composition(CompositionBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# SPECIMEN
# =========================
class SpecimenBase(BaseModel):
    specimen_type: str
    collection_time: datetime
    snomed_code: Optional[str] = None
    description: Optional[str] = None


class SpecimenCreate(SpecimenBase):
    pass


class SpecimenUpdate(SpecimenBase):
    pass


class Specimen(SpecimenBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# LAB TEST
# =========================
class LabTestBase(BaseModel):
    composition_id: int
    specimen_id: int
    loinc_code: Optional[str] = None


class LabTestCreate(LabTestBase):
    pass


class LabTestUpdate(LabTestBase):
    pass


class LabTest(LabTestBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# LAB ANALYTE RESULT
# =========================
class LabAnalyteResultBase(BaseModel):
    lab_test_id: int
    loinc_code: str
    value: float
    unit: str
    reference_low: Optional[float] = None
    reference_high: Optional[float] = None
    interpretation: Optional[str] = None


class LabAnalyteResultCreate(LabAnalyteResultBase):
    pass


class LabAnalyteResultUpdate(LabAnalyteResultBase):
    pass


class LabAnalyteResult(LabAnalyteResultBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# CBC PANEL
# =========================
class CBCPanelBase(BaseModel):
    lab_test_id: int
    hemoglobin_id: Optional[int] = None
    white_cell_id: Optional[int] = None
    platelet_id: Optional[int] = None


class CBCPanelCreate(CBCPanelBase):
    pass


class CBCPanelUpdate(CBCPanelBase):
    pass


class CBCPanel(CBCPanelBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# BLOOD TYPE PANEL
# =========================
class BloodTypePanelBase(BaseModel):
    lab_test_id: int
    abo_id: Optional[int] = None
    rh_id: Optional[int] = None


class BloodTypePanelCreate(BloodTypePanelBase):
    pass


class BloodTypePanelUpdate(BloodTypePanelBase):
    pass


class BloodTypePanel(BloodTypePanelBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# BODY MEASUREMENT
# =========================
class BodyMeasurementBase(BaseModel):
    patient_id: int
    record_time: datetime
    value: float
    unit: str
    snomed_code: str


class BodyMeasurementCreate(BodyMeasurementBase):
    pass


class BodyMeasurementUpdate(BodyMeasurementBase):
    pass


class BodyMeasurement(BodyMeasurementBase):
    id: int
    version: int

    class Config:
        from_attributes = True


# =========================
# REFERENCE RANGE
# =========================
class ReferenceRangeBase(BaseModel):
    loinc_code: str
    low: Optional[float] = None
    high: Optional[float] = None
    unit: Optional[str] = None


class ReferenceRangeCreate(ReferenceRangeBase):
    pass


class ReferenceRangeUpdate(ReferenceRangeBase):
    pass


class ReferenceRange(ReferenceRangeBase):
    version: int

    class Config:
        from_attributes = True
