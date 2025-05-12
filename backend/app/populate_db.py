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
            {"loinc_code": "718-7", "low": 12.0, "high": 17.5, "unit": "g/dL"},
            {"loinc_code": "6690-2", "low": 4.0, "high": 10.0, "unit": "10^9/L"},
            {"loinc_code": "777-3", "low": 150, "high": 400, "unit": "10^9/L"},
            {"loinc_code": "882-1", "low": None, "high": None, "unit": None},
            {"loinc_code": "10331-7", "low": None, "high": None, "unit": None},
        ],
        "patients": [
            {
                "first_name": "John",
                "last_name": "Doe",
                "sex": "male",
                "identifier": "PAT-001",
            }
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

        # Create a composition for the first patient
        patient_id = patient_map["PAT-001"]
        composition = models.Composition(
            patient_id=patient_id, start_time=parse_datetime("2025-04-28T08:00:00Z")
        )
        session.add(composition)
        session.flush()
        composition_id = composition.id

        # Create a specimen
        specimen = models.Specimen(
            specimen_type="Venous blood",
            collection_time=parse_datetime("2025-04-27T07:45:00Z"),
            snomed_code="122555007",
            description="Venous blood specimen",
        )
        session.add(specimen)
        session.flush()
        specimen_id = specimen.id

        # Create a lab test
        lab_test = models.LabTest(
            composition_id=composition_id,
            specimen_id=specimen_id,
            loinc_code="57021-8",
            description="Complete Blood Count (CBC)",
        )
        session.add(lab_test)
        session.flush()
        lab_test_id = lab_test.id

        # Create lab analyte results
        analyte_map = {}

        # Hemoglobin
        hemoglobin = models.LabAnalyteResult(
            lab_test_id=lab_test_id,
            loinc_code="718-7",
            value=14.2,
            unit="g/dL",
            reference_low=12.0,
            reference_high=17.5,
            interpretation="N",
        )
        session.add(hemoglobin)
        session.flush()
        analyte_map["hemoglobin"] = hemoglobin.id

        # White Blood Cell
        wbc = models.LabAnalyteResult(
            lab_test_id=lab_test_id,
            loinc_code="6690-2",
            value=7.1,
            unit="10^9/L",
            reference_low=4.0,
            reference_high=10.0,
            interpretation="N",
        )
        session.add(wbc)
        session.flush()
        analyte_map["wbc"] = wbc.id

        # Platelets
        platelets = models.LabAnalyteResult(
            lab_test_id=lab_test_id,
            loinc_code="777-3",
            value=225,
            unit="10^9/L",
            reference_low=150,
            reference_high=400,
            interpretation="N",
        )
        session.add(platelets)
        session.flush()
        analyte_map["platelets"] = platelets.id

        # Create Body Measurements
        height = models.BodyMeasurement(
            patient_id=patient_id,
            record_time=parse_datetime("2025-04-27T08:00:00Z"),
            value=180,
            unit="cm",
            snomed_code="50373000",
        )
        session.add(height)

        weight = models.BodyMeasurement(
            patient_id=patient_id,
            record_time=parse_datetime("2025-04-27T08:00:00Z"),
            value=78,
            unit="kg",
            snomed_code="27113001",
        )
        session.add(weight)

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
