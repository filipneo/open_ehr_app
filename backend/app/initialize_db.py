from app import database, models
from app.populate_db import populate_database
from sqlalchemy.orm import Session


def initialize_database():
    """Check if database is empty and populate it if needed"""
    # Create tables first
    models.Base.metadata.create_all(bind=database.engine)

    # Create a database session
    session = Session(database.engine)

    try:
        # Check if patients table is empty (as a proxy for checking if DB is empty)
        patient_count = session.query(models.Patient).count()

        if patient_count == 0:
            print("Database is empty. Populating with initial data...")
            # Close this session and let populate_database create its own session
            session.close()
            populate_database()
        else:
            print(f"Database already has {patient_count} patients. Skipping initialization.")

    except Exception as e:
        print(f"❌ Error checking database: {e}")
    finally:
        if session.is_active:
            session.close()


if __name__ == "__main__":
    initialize_database()
