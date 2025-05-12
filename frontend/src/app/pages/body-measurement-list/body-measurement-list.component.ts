import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BodyMeasurement, BodyMeasurementService, BodyMeasurementCreatePayload, BodyMeasurementUpdatePayload } from '../../services/body-measurement.service';
import { Patient, PatientService } from '../../services/patient.service'; // For patient dropdown

// It's better to import bootstrap if you have type definitions, or ensure it's globally available.
// For now, using 'any' to avoid compilation errors if types are not set up.
declare var bootstrap: any;

@Component({
  selector: 'app-body-measurement-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './body-measurement-list.component.html',
  styleUrls: ['./body-measurement-list.component.scss']
})
export class BodyMeasurementListComponent implements OnInit, AfterViewInit {
  bodyMeasurements: BodyMeasurement[] = [];
  patients: Patient[] = []; // To store patient list for dropdown

  measurementToCreate: BodyMeasurementCreatePayload = {
    patient_id: 0, // Initialize with a default or ensure it's set before use
    record_time: '',
    value: 0,
    unit: ''
  };
  // For update, ensure all fields are potentially part of the form.
  // id is crucial for the update operation itself.
  measurementToUpdate: BodyMeasurementUpdatePayload & { id?: number } = {
    id: undefined, // Keep id for context, but it's not part of the payload for update typically
    patient_id: 0,
    record_time: '',
    value: 0,
    unit: ''
  };
  measurementToDelete: BodyMeasurement | null = null;

  private createModal: any;
  private updateModal: any;
  private deleteModal: any;

  constructor(
    private bodyMeasurementService: BodyMeasurementService,
    private patientService: PatientService // Inject PatientService
  ) { }

  ngOnInit(): void {
    this.loadBodyMeasurements();
    this.loadPatients(); // Load patients for the dropdown
  }

  ngAfterViewInit(): void {
    // Initialize Bootstrap modals
    const createModalEl = document.getElementById('createBodyMeasurementModal');
    if (createModalEl) {
      this.createModal = new bootstrap.Modal(createModalEl);
    } else {
      console.error('Create BodyMeasurement modal (createBodyMeasurementModal) not found.');
    }

    const updateModalEl = document.getElementById('updateBodyMeasurementModal');
    if (updateModalEl) {
      this.updateModal = new bootstrap.Modal(updateModalEl);
    } else {
      console.error('Update BodyMeasurement modal (updateBodyMeasurementModal) not found.');
    }

    const deleteModalEl = document.getElementById('deleteBodyMeasurementModal');
    if (deleteModalEl) {
      this.deleteModal = new bootstrap.Modal(deleteModalEl);
    } else {
      console.error('Delete BodyMeasurement modal (deleteBodyMeasurementModal) not found.');
    }
  }

  loadBodyMeasurements(): void {
    this.bodyMeasurementService.getBodyMeasurements().subscribe(data => {
      this.bodyMeasurements = data;
    });
  }

  loadPatients(): void {
    this.patientService.getPatients().subscribe(data => {
      this.patients = data;
      // Set default patient_id for creation form if patients are loaded
      if (this.patients.length > 0 && !this.measurementToCreate.patient_id) {
        this.measurementToCreate.patient_id = this.patients[0].id;
      }
    });
  }

  getPatientName(patientId: number): string {
    const patient = this.patients.find(p => p.id === patientId);
    return patient ? `${patient.first_name} ${patient.last_name}` : 'Unknown Patient';
  }

  // Helper to format ISO string to 'YYYY-MM-DDTHH:mm' for datetime-local input
  private formatDateTimeForInput(isoString: string | undefined | null): string {
    if (!isoString) {
      // Return current time formatted for datetime-local if no date is provided
      const now = new Date();
      const offset = now.getTimezoneOffset();
      const adjustedDate = new Date(now.getTime() - (offset*60*1000));
      return adjustedDate.toISOString().slice(0,16);
    }
    try {
      const date = new Date(isoString);
      // Adjust for timezone offset to display correctly in local time input
      const offset = date.getTimezoneOffset();
      const adjustedDate = new Date(date.getTime() - (offset*60*1000));
      return adjustedDate.toISOString().slice(0, 16);
    } catch (e) {
      console.error("Error formatting date for input:", e);
      const now = new Date();
      const offset = now.getTimezoneOffset();
      const adjustedDate = new Date(now.getTime() - (offset*60*1000));
      return adjustedDate.toISOString().slice(0,16);
    }
  }

  // Helper to format datetime-local input value to ISO string for backend
  private formatDateTimeToISO(localDateTime: string | undefined): string {
    if (!localDateTime) {
      return new Date().toISOString(); // Fallback, though should be validated
    }
    // The input 'datetime-local' provides date and time in local timezone.
    // New Date() will parse it correctly. Then toISOString() converts to UTC.
    return new Date(localDateTime).toISOString();
  }

  openCreateModal(): void {
    this.measurementToCreate = {
      patient_id: this.patients.length > 0 ? this.patients[0].id : 0,
      record_time: this.formatDateTimeForInput(null), // Default to current time
      value: 0,
      unit: '',
      snomed_code: '',
    };
    if (this.createModal) {
      this.createModal.show();
    }
  }

  onCreateSubmit(): void {
    const payload: BodyMeasurementCreatePayload = {
      ...this.measurementToCreate,
      record_time: this.formatDateTimeToISO(this.measurementToCreate.record_time)
    };
    this.bodyMeasurementService.createBodyMeasurement(payload).subscribe(() => {
      this.loadBodyMeasurements();
      if (this.createModal) this.createModal.hide();
    });
  }

  openUpdateModal(measurement: BodyMeasurement): void {
    // Create a deep copy for the form model
    this.measurementToUpdate = {
      ...measurement, // Spread existing measurement data
      record_time: this.formatDateTimeForInput(measurement.record_time) // Format for input
    };
    if (this.updateModal) {
      this.updateModal.show();
    }
  }

  onUpdateSubmit(): void {
    if (!this.measurementToUpdate.id) {
      console.error("Cannot update without an ID.");
      return;
    }

    // Construct the payload, excluding 'id' from the main body
    const { id, ...payloadData } = this.measurementToUpdate;
    const payload: BodyMeasurementUpdatePayload = {
        ...payloadData,
        record_time: this.formatDateTimeToISO(this.measurementToUpdate.record_time)
    };

    this.bodyMeasurementService.updateBodyMeasurement(id, payload).subscribe(() => {
      this.loadBodyMeasurements();
      if (this.updateModal) this.updateModal.hide();
    });
  }

  openDeleteModal(measurement: BodyMeasurement): void {
    this.measurementToDelete = measurement;
    if (this.deleteModal) {
      this.deleteModal.show();
    }
  }

  confirmDelete(): void {
    if (this.measurementToDelete && this.measurementToDelete.id) {
      this.bodyMeasurementService.deleteBodyMeasurement(this.measurementToDelete.id).subscribe(() => {
        this.loadBodyMeasurements();
        if (this.deleteModal) this.deleteModal.hide();
        this.measurementToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) this.deleteModal.hide();
    this.measurementToDelete = null;
  }
}
