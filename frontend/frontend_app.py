import os

import requests
from nicegui import ui

API_BASE = os.getenv("API_BASE", "http://localhost:8000")


@ui.page("/")
def home():
    ui.label("🏥 Welcome to the EHR System").classes("text-2xl p-4")
    ui.link("📋 View Patients", "/patients")
    ui.link("➕ Add Patient", "/patients/new")


@ui.page("/patients")
def patient_list():
    ui.label("👥 Patients").classes("text-xl p-2")

    with ui.table(
        columns=[
            {"name": "first_name", "label": "First Name", "field": "first_name"},
            {"name": "last_name", "label": "Last Name", "field": "last_name"},
            {"name": "sex", "label": "Sex", "field": "sex"},
            {"name": "identifier", "label": "Identifier", "field": "identifier"},
        ],
        rows=[],
        row_key="id",
    ) as table:
        try:
            r = requests.get(f"{API_BASE}/patients")
            r.raise_for_status()
            table.rows = r.json()
        except Exception as e:
            ui.notify(f"Error loading patients: {e}", type="negative")


@ui.page("/patients/new")
def patient_form():
    ui.label("➕ Add New Patient").classes("text-xl p-2")

    first_name = ui.input(label="First Name")
    last_name = ui.input(label="Last Name")
    sex = ui.select(["male", "female", "other"], label="Sex")
    identifier = ui.input(label="Identifier")

    def submit():
        payload = {
            "first_name": first_name.value,
            "last_name": last_name.value,
            "sex": sex.value,
            "identifier": identifier.value,
        }
        try:
            r = requests.post(f"{API_BASE}/patients", json=payload)
            r.raise_for_status()
            ui.notify("Patient created successfully!")
            ui.navigate.to("/patients")
        except Exception as e:
            ui.notify(f"Failed to create patient: {e}", type="negative")

    ui.button("Create Patient", on_click=submit).classes("mt-4")


ui.run(title="EHR Frontend", reload=False)
ui.run(title="EHR Frontend", reload=False)
