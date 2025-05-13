from datetime import datetime

from app import database, models
from sqlalchemy.orm import Session


def parse_datetime(dt_str):
    """Parse ISO 8601 datetime string to Python datetime"""
    if dt_str:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return None


def populate_database():
    """Populate the database with the sample data directly using SQLAlchemy"""

    # First, create all tables if they don't exist
    models.Base.metadata.create_all(bind=database.engine)

    # Sample data
    data = {
        "reference_ranges": [
            # Complete Blood Count (CBC) standard ranges
            {"loinc_code": "718-7", "low": 12.0, "high": 17.5, "unit": "g/dL"},  # Hemoglobin
            {
                "loinc_code": "6690-2",
                "low": 4.0,
                "high": 10.0,
                "unit": "10^9/L",
            },  # White Blood Cell Count
            {"loinc_code": "777-3", "low": 150, "high": 400, "unit": "10^9/L"},  # Platelets
            {
                "loinc_code": "789-8",
                "low": 4.2,
                "high": 5.8,
                "unit": "10^12/L",
            },  # Red Blood Cell Count
            {"loinc_code": "785-6", "low": 0.37, "high": 0.47, "unit": "L/L"},  # MCH
            {"loinc_code": "4544-3", "low": 37, "high": 47, "unit": "%"},  # Hematocrit
            # Basic Metabolic Panel
            {"loinc_code": "2345-7", "low": 135, "high": 145, "unit": "mmol/L"},  # Glucose
            {"loinc_code": "2823-3", "low": 3.5, "high": 5.0, "unit": "mmol/L"},  # Potassium
            {"loinc_code": "2951-2", "low": 136, "high": 145, "unit": "mmol/L"},  # Sodium
            {"loinc_code": "2075-0", "low": 60, "high": 110, "unit": "µmol/L"},  # Creatinine
            {"loinc_code": "3094-0", "low": 2.5, "high": 7.8, "unit": "mmol/L"},  # Urea
            # Lipid Panel
            {
                "loinc_code": "2093-3",
                "low": None,
                "high": 5.2,
                "unit": "mmol/L",
            },  # Total Cholesterol
            {"loinc_code": "2571-8", "low": None, "high": 1.7, "unit": "mmol/L"},  # Triglycerides
            {"loinc_code": "2085-9", "low": 1.0, "high": None, "unit": "mmol/L"},  # HDL Cholesterol
            {
                "loinc_code": "18262-6",
                "low": None,
                "high": 3.4,
                "unit": "mmol/L",
            },  # LDL Cholesterol
            # Other common tests
            {"loinc_code": "882-1", "low": None, "high": None, "unit": None},  # ABO Blood Type
            {"loinc_code": "10331-7", "low": None, "high": None, "unit": None},  # Rh Type
            {"loinc_code": "1920-8", "low": 0.3, "high": 1.2, "unit": "mg/dL"},  # AST
            {"loinc_code": "6768-6", "low": None, "high": 40, "unit": "U/L"},  # ALT
            {"loinc_code": "1975-2", "low": None, "high": 1.2, "unit": "mg/dL"},  # Total Bilirubin
        ],
        "patients": [
            {
                "first_name": "John",
                "last_name": "Doe",
                "sex": "male",
                "identifier": "PAT-001",
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "sex": "female",
                "identifier": "PAT-002",
            },
            {
                "first_name": "Michael",
                "last_name": "Johnson",
                "sex": "male",
                "identifier": "PAT-003",
            },
            {
                "first_name": "Sarah",
                "last_name": "Williams",
                "sex": "female",
                "identifier": "PAT-004",
            },
            {
                "first_name": "Robert",
                "last_name": "Brown",
                "sex": "male",
                "identifier": "PAT-005",
            },
        ],
    }

    # Create a database session
    session = Session(database.engine)

    try:
        # Clear existing data (optional - comment out if you don't want to clear the database)
        for table in reversed(models.Base.metadata.sorted_tables):
            session.execute(table.delete())

        # 1. Reference Ranges
        for rr in data["reference_ranges"]:
            reference_range = models.ReferenceRange(
                loinc_code=rr["loinc_code"], low=rr["low"], high=rr["high"], unit=rr["unit"]
            )
            session.add(reference_range)

        # 2. Patients
        patient_map = {}  # To store patient_id mappings
        for p in data["patients"]:
            patient = models.Patient(
                first_name=p["first_name"],
                last_name=p["last_name"],
                sex=p["sex"],
                identifier=p["identifier"],
            )
            session.add(patient)
            session.flush()  # Flush to get the ID
            patient_map[p["identifier"]] = patient.id

        # Commit to persist the initial entities
        session.commit()

        # Create compositions, specimens, and lab tests for patients

        # ======== PATIENT 1 (John Doe) - CBC and Basic Health Check ========
        patient_id = patient_map["PAT-001"]

        # Composition 1
        composition1 = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-04-28T08:00:00Z")
        )
        session.add(composition1)
        session.flush()

        # Specimen - Blood
        blood_specimen = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-04-27T07:45:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen",
        )
        session.add(blood_specimen)
        session.flush()

        # Lab Test - CBC
        cbc_test = models.LabTest(
            composition_id=composition1.id,
            specimen_id=blood_specimen.id,
            loinc_code="57021-8",
            description="Complete Blood Count (CBC)",
        )
        session.add(cbc_test)
        session.flush()

        # CBC Results
        cbc_results = [
            {
                "loinc_code": "718-7",  # Hemoglobin
                "value": 14.2,
                "unit": "g/dL",
                "reference_low": 12.0,
                "reference_high": 17.5,
                "interpretation": "N",
            },
            {
                "loinc_code": "6690-2",  # WBC
                "value": 7.1,
                "unit": "10^9/L",
                "reference_low": 4.0,
                "reference_high": 10.0,
                "interpretation": "N",
            },
            {
                "loinc_code": "777-3",  # Platelets
                "value": 225,
                "unit": "10^9/L",
                "reference_low": 150,
                "reference_high": 400,
                "interpretation": "N",
            },
            {
                "loinc_code": "789-8",  # RBC
                "value": 5.0,
                "unit": "10^12/L",
                "reference_low": 4.2,
                "reference_high": 5.8,
                "interpretation": "N",
            },
            {
                "loinc_code": "4544-3",  # Hematocrit
                "value": 42,
                "unit": "%",
                "reference_low": 37,
                "reference_high": 47,
                "interpretation": "N",
            },
        ]

        for result in cbc_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=cbc_test.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # Body Measurements for John
        body_measurements = [
            {
                "record_time": "2025-04-27T08:00:00Z",
                "value": 180,
                "unit": "cm",
                "snomed_code": "50373000",  # Height
                "description": "Body height",
            },
            {
                "record_time": "2025-04-27T08:00:00Z",
                "value": 78,
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
                "description": "Body weight",
            },
            {
                "record_time": "2025-04-27T08:10:00Z",
                "value": 120,
                "unit": "mmHg",
                "snomed_code": "271649006",  # Systolic BP
                "description": "Systolic blood pressure",
            },
            {
                "record_time": "2025-04-27T08:10:00Z",
                "value": 80,
                "unit": "mmHg",
                "snomed_code": "271650006",  # Diastolic BP
                "description": "Diastolic blood pressure",
            },
        ]

        for measurement in body_measurements:
            body_measure = models.BodyMeasurement(
                patient_id=patient_id,
                record_time=parse_datetime(measurement["record_time"]),
                value=measurement["value"],
                unit=measurement["unit"],
                snomed_code=measurement["snomed_code"],
            )
            session.add(body_measure)

        # ======== PATIENT 2 (Jane Smith) - Lipid Panel and Basic Metabolic Panel ========
        patient_id = patient_map["PAT-002"]

        # Composition for Jane
        composition2 = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-04-26T09:30:00Z")
        )
        session.add(composition2)
        session.flush()

        # Blood Specimen for Jane
        jane_specimen = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-04-26T09:15:00Z"),
            snomed_code="122555007",
            description="Blood sample taken after 12 hour fast",
        )
        session.add(jane_specimen)
        session.flush()

        # Lipid Panel Test
        lipid_test = models.LabTest(
            composition_id=composition2.id,
            specimen_id=jane_specimen.id,
            loinc_code="24331-1",
            description="Lipid Panel",
        )
        session.add(lipid_test)
        session.flush()

        # Lipid Panel Results
        lipid_results = [
            {
                "loinc_code": "2093-3",  # Total Cholesterol
                "value": 5.8,
                "unit": "mmol/L",
                "reference_low": None,
                "reference_high": 5.2,
                "interpretation": "H",  # High
            },
            {
                "loinc_code": "2571-8",  # Triglycerides
                "value": 1.4,
                "unit": "mmol/L",
                "reference_low": None,
                "reference_high": 1.7,
                "interpretation": "N",  # Normal
            },
            {
                "loinc_code": "2085-9",  # HDL Cholesterol
                "value": 1.8,
                "unit": "mmol/L",
                "reference_low": 1.0,
                "reference_high": None,
                "interpretation": "N",  # Normal
            },
            {
                "loinc_code": "18262-6",  # LDL Cholesterol
                "value": 3.6,
                "unit": "mmol/L",
                "reference_low": None,
                "reference_high": 3.4,
                "interpretation": "H",  # High
            },
        ]

        for result in lipid_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=lipid_test.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # Basic Metabolic Panel Test
        metabolic_test = models.LabTest(
            composition_id=composition2.id,
            specimen_id=jane_specimen.id,
            loinc_code="51990-0",
            description="Basic Metabolic Panel",
        )
        session.add(metabolic_test)
        session.flush()

        # Metabolic Panel Results
        metabolic_results = [
            {
                "loinc_code": "2345-7",  # Glucose
                "value": 5.1,
                "unit": "mmol/L",
                "reference_low": 3.9,
                "reference_high": 5.8,
                "interpretation": "N",
            },
            {
                "loinc_code": "2823-3",  # Potassium
                "value": 4.2,
                "unit": "mmol/L",
                "reference_low": 3.5,
                "reference_high": 5.0,
                "interpretation": "N",
            },
            {
                "loinc_code": "2951-2",  # Sodium
                "value": 140,
                "unit": "mmol/L",
                "reference_low": 136,
                "reference_high": 145,
                "interpretation": "N",
            },
            {
                "loinc_code": "2075-0",  # Creatinine
                "value": 70,
                "unit": "µmol/L",
                "reference_low": 60,
                "reference_high": 110,
                "interpretation": "N",
            },
        ]

        for result in metabolic_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=metabolic_test.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # Body Measurements for Jane
        jane_measurements = [
            {
                "record_time": "2025-04-26T09:30:00Z",
                "value": 165,
                "unit": "cm",
                "snomed_code": "50373000",  # Height
                "description": "Body height",
            },
            {
                "record_time": "2025-04-26T09:30:00Z",
                "value": 62,
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
                "description": "Body weight",
            },
            {
                "record_time": "2025-04-26T09:40:00Z",
                "value": 118,
                "unit": "mmHg",
                "snomed_code": "271649006",  # Systolic BP
                "description": "Systolic blood pressure",
            },
            {
                "record_time": "2025-04-26T09:40:00Z",
                "value": 75,
                "unit": "mmHg",
                "snomed_code": "271650006",  # Diastolic BP
                "description": "Diastolic blood pressure",
            },
        ]

        for measurement in jane_measurements:
            body_measure = models.BodyMeasurement(
                patient_id=patient_id,
                record_time=parse_datetime(measurement["record_time"]),
                value=measurement["value"],
                unit=measurement["unit"],
                snomed_code=measurement["snomed_code"],
            )
            session.add(body_measure)

        # ======== PATIENT 3 (Michael Johnson) - Liver Function Tests ========
        patient_id = patient_map["PAT-003"]

        # Composition for Michael
        composition3 = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-04-30T11:00:00Z")
        )
        session.add(composition3)
        session.flush()

        # Blood Specimen for Michael
        michael_specimen = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-04-30T10:45:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen",
        )
        session.add(michael_specimen)
        session.flush()

        # Liver Function Test
        liver_test = models.LabTest(
            composition_id=composition3.id,
            specimen_id=michael_specimen.id,
            loinc_code="10751-6",
            description="Liver Function Panel",
        )
        session.add(liver_test)
        session.flush()

        # Liver Function Results - Slightly elevated values
        liver_results = [
            {
                "loinc_code": "1920-8",  # AST
                "value": 1.4,
                "unit": "mg/dL",
                "reference_low": 0.3,
                "reference_high": 1.2,
                "interpretation": "H",  # High
            },
            {
                "loinc_code": "6768-6",  # ALT
                "value": 45,
                "unit": "U/L",
                "reference_low": None,
                "reference_high": 40,
                "interpretation": "H",  # High
            },
            {
                "loinc_code": "1975-2",  # Total Bilirubin
                "value": 1.3,
                "unit": "mg/dL",
                "reference_low": None,
                "reference_high": 1.2,
                "interpretation": "H",  # High
            },
        ]

        for result in liver_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=liver_test.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # CBC test for Michael as well
        cbc_michael = models.LabTest(
            composition_id=composition3.id,
            specimen_id=michael_specimen.id,
            loinc_code="57021-8",
            description="Complete Blood Count (CBC)",
        )
        session.add(cbc_michael)
        session.flush()

        # CBC Results for Michael - Normal
        michael_cbc_results = [
            {
                "loinc_code": "718-7",  # Hemoglobin
                "value": 15.1,
                "unit": "g/dL",
                "reference_low": 12.0,
                "reference_high": 17.5,
                "interpretation": "N",
            },
            {
                "loinc_code": "6690-2",  # WBC
                "value": 8.2,
                "unit": "10^9/L",
                "reference_low": 4.0,
                "reference_high": 10.0,
                "interpretation": "N",
            },
            {
                "loinc_code": "777-3",  # Platelets
                "value": 275,
                "unit": "10^9/L",
                "reference_low": 150,
                "reference_high": 400,
                "interpretation": "N",
            },
        ]

        for result in michael_cbc_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=cbc_michael.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # Body Measurements for Michael
        michael_measurements = [
            {
                "record_time": "2025-04-30T11:00:00Z",
                "value": 188,
                "unit": "cm",
                "snomed_code": "50373000",  # Height
                "description": "Body height",
            },
            {
                "record_time": "2025-04-30T11:00:00Z",
                "value": 92,
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
                "description": "Body weight",
            },
        ]

        for measurement in michael_measurements:
            body_measure = models.BodyMeasurement(
                patient_id=patient_id,
                record_time=parse_datetime(measurement["record_time"]),
                value=measurement["value"],
                unit=measurement["unit"],
                snomed_code=measurement["snomed_code"],
            )
            session.add(body_measure)

        # ======== PATIENT 4 (Sarah Williams) - Blood Type & CBC ========
        patient_id = patient_map["PAT-004"]

        # Composition for Sarah
        composition4 = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-05-02T14:15:00Z")
        )
        session.add(composition4)
        session.flush()

        # Blood Specimen for Sarah
        sarah_specimen = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-05-02T14:00:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen",
        )
        session.add(sarah_specimen)
        session.flush()

        # Blood Type Test
        blood_type_test = models.LabTest(
            composition_id=composition4.id,
            specimen_id=sarah_specimen.id,
            loinc_code="934-0",
            description="Blood Type Panel",
        )
        session.add(blood_type_test)
        session.flush()

        # Blood Type Results
        blood_type_results = [
            {
                "loinc_code": "882-1",  # ABO Blood Type
                "value": 0,  # Representing "A" (coded value)
                "unit": None,
                "reference_low": None,
                "reference_high": None,
                "interpretation": "A",  # Blood Type A
            },
            {
                "loinc_code": "10331-7",  # Rh Type
                "value": 1,  # Representing "Positive" (coded value)
                "unit": None,
                "reference_low": None,
                "reference_high": None,
                "interpretation": "POS",  # Rh Positive
            },
        ]

        for result in blood_type_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=blood_type_test.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"] if result["unit"] else "",  # Empty string for None
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # CBC for Sarah
        cbc_sarah = models.LabTest(
            composition_id=composition4.id,
            specimen_id=sarah_specimen.id,
            loinc_code="57021-8",
            description="Complete Blood Count (CBC)",
        )
        session.add(cbc_sarah)
        session.flush()

        # CBC Results - Slightly low hemoglobin
        sarah_cbc_results = [
            {
                "loinc_code": "718-7",  # Hemoglobin
                "value": 11.8,
                "unit": "g/dL",
                "reference_low": 12.0,
                "reference_high": 17.5,
                "interpretation": "L",  # Low
            },
            {
                "loinc_code": "6690-2",  # WBC
                "value": 6.2,
                "unit": "10^9/L",
                "reference_low": 4.0,
                "reference_high": 10.0,
                "interpretation": "N",  # Normal
            },
            {
                "loinc_code": "777-3",  # Platelets
                "value": 310,
                "unit": "10^9/L",
                "reference_low": 150,
                "reference_high": 400,
                "interpretation": "N",  # Normal
            },
            {
                "loinc_code": "789-8",  # RBC
                "value": 4.0,
                "unit": "10^12/L",
                "reference_low": 4.2,
                "reference_high": 5.8,
                "interpretation": "L",  # Low
            },
        ]

        for result in sarah_cbc_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=cbc_sarah.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # Body Measurements for Sarah
        sarah_measurements = [
            {
                "record_time": "2025-05-02T14:15:00Z",
                "value": 170,
                "unit": "cm",
                "snomed_code": "50373000",  # Height
                "description": "Body height",
            },
            {
                "record_time": "2025-05-02T14:15:00Z",
                "value": 65,
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
                "description": "Body weight",
            },
            {
                "record_time": "2025-05-02T14:20:00Z",
                "value": 37.2,
                "unit": "C",
                "snomed_code": "386725007",  # Body temperature
                "description": "Body temperature",
            },
        ]

        for measurement in sarah_measurements:
            body_measure = models.BodyMeasurement(
                patient_id=patient_id,
                record_time=parse_datetime(measurement["record_time"]),
                value=measurement["value"],
                unit=measurement["unit"],
                snomed_code=measurement["snomed_code"],
            )
            session.add(body_measure)

        # ======== PATIENT 5 (Robert Brown) - Multiple tests over time ========
        patient_id = patient_map["PAT-005"]

        # First visit - Three months ago
        composition5a = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-02-10T09:30:00Z")
        )
        session.add(composition5a)
        session.flush()

        robert_specimen1 = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-02-10T09:15:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen",
        )
        session.add(robert_specimen1)
        session.flush()

        # Glucose test - First visit (high)
        glucose_test1 = models.LabTest(
            composition_id=composition5a.id,
            specimen_id=robert_specimen1.id,
            loinc_code="2339-0",
            description="Glucose test",
        )
        session.add(glucose_test1)
        session.flush()

        glucose1 = models.LabAnalyteResult(
            lab_test_id=glucose_test1.id,
            loinc_code="2345-7",
            value=8.2,  # High
            unit="mmol/L",
            reference_low=3.9,
            reference_high=5.8,
            interpretation="H",  # High
        )
        session.add(glucose1)

        # Second visit - One month ago
        composition5b = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-04-15T10:00:00Z")
        )
        session.add(composition5b)
        session.flush()

        robert_specimen2 = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-04-15T09:45:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen",
        )
        session.add(robert_specimen2)
        session.flush()

        # Glucose test - Follow-up visit (still high but improved)
        glucose_test2 = models.LabTest(
            composition_id=composition5b.id,
            specimen_id=robert_specimen2.id,
            loinc_code="2339-0",
            description="Glucose test",
        )
        session.add(glucose_test2)
        session.flush()

        glucose2 = models.LabAnalyteResult(
            lab_test_id=glucose_test2.id,
            loinc_code="2345-7",
            value=7.1,  # Still high but improved
            unit="mmol/L",
            reference_low=3.9,
            reference_high=5.8,
            interpretation="H",  # High
        )
        session.add(glucose2)

        # Current visit - Most recent
        composition5c = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-05-03T09:45:00Z")
        )
        session.add(composition5c)
        session.flush()

        robert_specimen3 = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-05-03T09:30:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen after 8h fast",
        )
        session.add(robert_specimen3)
        session.flush()

        # Full metabolic panel - Most recent visit
        metabolic_robert = models.LabTest(
            composition_id=composition5c.id,
            specimen_id=robert_specimen3.id,
            loinc_code="51990-0",
            description="Basic Metabolic Panel",
        )
        session.add(metabolic_robert)
        session.flush()

        # Latest results - Improved, but still monitoring
        robert_metabolic_results = [
            {
                "loinc_code": "2345-7",  # Glucose
                "value": 6.5,  # Improving but still elevated
                "unit": "mmol/L",
                "reference_low": 3.9,
                "reference_high": 5.8,
                "interpretation": "H",  # High
            },
            {
                "loinc_code": "2823-3",  # Potassium
                "value": 4.1,
                "unit": "mmol/L",
                "reference_low": 3.5,
                "reference_high": 5.0,
                "interpretation": "N",
            },
            {
                "loinc_code": "2951-2",  # Sodium
                "value": 138,
                "unit": "mmol/L",
                "reference_low": 136,
                "reference_high": 145,
                "interpretation": "N",
            },
            {
                "loinc_code": "2075-0",  # Creatinine
                "value": 88,
                "unit": "µmol/L",
                "reference_low": 60,
                "reference_high": 110,
                "interpretation": "N",
            },
        ]

        for result in robert_metabolic_results:
            analyte = models.LabAnalyteResult(
                lab_test_id=metabolic_robert.id,
                loinc_code=result["loinc_code"],
                value=result["value"],
                unit=result["unit"],
                reference_low=result["reference_low"],
                reference_high=result["reference_high"],
                interpretation=result["interpretation"],
            )
            session.add(analyte)

        # Body measurements for Robert (tracking over time)
        # Initial measurements
        robert_measurements1 = [
            {
                "record_time": "2025-02-10T09:30:00Z",
                "value": 175,
                "unit": "cm",
                "snomed_code": "50373000",  # Height
            },
            {
                "record_time": "2025-02-10T09:30:00Z",
                "value": 95,  # Initial weight
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
            },
        ]

        # Follow-up measurements
        robert_measurements2 = [
            {
                "record_time": "2025-04-15T10:00:00Z",
                "value": 175,
                "unit": "cm",
                "snomed_code": "50373000",  # Height (unchanged)
            },
            {
                "record_time": "2025-04-15T10:00:00Z",
                "value": 93,  # Some weight loss
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
            },
        ]

        # Current measurements
        robert_measurements3 = [
            {
                "record_time": "2025-05-03T09:45:00Z",
                "value": 175,
                "unit": "cm",
                "snomed_code": "50373000",  # Height (unchanged)
            },
            {
                "record_time": "2025-05-03T09:45:00Z",
                "value": 90,  # Further weight loss
                "unit": "kg",
                "snomed_code": "27113001",  # Weight
            },
            {
                "record_time": "2025-05-03T09:50:00Z",
                "value": 135,
                "unit": "mmHg",
                "snomed_code": "271649006",  # Systolic BP
            },
            {
                "record_time": "2025-05-03T09:50:00Z",
                "value": 85,
                "unit": "mmHg",
                "snomed_code": "271650006",  # Diastolic BP
            },
        ]

        # Add all measurements
        for measurements in [robert_measurements1, robert_measurements2, robert_measurements3]:
            for measurement in measurements:
                body_measure = models.BodyMeasurement(
                    patient_id=patient_id,
                    record_time=parse_datetime(measurement["record_time"]),
                    value=measurement["value"],
                    unit=measurement["unit"],
                    snomed_code=measurement["snomed_code"],
                )
                session.add(body_measure)

        # Commit all changes
        session.commit()
        print("✅ Database populated successfully with direct SQLAlchemy access.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error populating database: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    populate_database()
