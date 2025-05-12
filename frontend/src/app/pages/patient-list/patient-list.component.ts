import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Patient, PatientService, PatientCreatePayload, PatientFull } from '../../services/patient.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class PatientListComponent implements OnInit, AfterViewInit {
  patients: Patient[] = [];
  selectedPatient: Patient | null = null;
  patientToUpdate: Patient = {} as Patient;
  patientToCreate: PatientCreatePayload = {} as PatientCreatePayload;
  patientToDelete: Patient | null = null;
  patientFullDetails: PatientFull | null = null;

  private updateModal: any; // This will hold the Bootstrap Modal instance
  private deleteModal: any; // This will hold the Bootstrap Modal instance
  private createModal: any; // This will hold the Bootstrap Modal instance
  private detailsModal: any; // This will hold the Bootstrap Modal instance for patient details

  constructor(private patientService: PatientService) { }

  ngOnInit(): void {
    this.loadPatients();
  }
  ngAfterViewInit(): void {
    const bootstrap = (window as any).bootstrap;
    if (bootstrap && typeof bootstrap.Modal === 'function') {
      const updateModalEl = document.getElementById('updatePatientModal');
      if (updateModalEl) {
        this.updateModal = new bootstrap.Modal(updateModalEl);
      } else {
        console.error('Update patient modal element (updatePatientModal) not found.');
      }

      const deleteModalEl = document.getElementById('deletePatientModal');
      if (deleteModalEl) {
        this.deleteModal = new bootstrap.Modal(deleteModalEl);
      } else {
        console.error('Delete patient modal element (deletePatientModal) not found.');
      }

      const createModalEl = document.getElementById('createPatientModal');
      if (createModalEl) {
        this.createModal = new bootstrap.Modal(createModalEl);
      } else {
        console.error('Create patient modal element (createPatientModal) not found.');
      }
      
      const detailsModalEl = document.getElementById('patientDetailsModal');
      if (detailsModalEl) {
        this.detailsModal = new bootstrap.Modal(detailsModalEl);
      } else {
        console.error('Patient details modal element (patientDetailsModal) not found.');
      }
    } else {
      console.error('Bootstrap JavaScript or Bootstrap.Modal is not loaded or not available on the window object.');
      if (bootstrap) {
        console.error('Bootstrap object found, but Modal constructor is missing:', bootstrap);
      }
    }
  }

  loadPatients(): void {
    this.patientService.getPatients().subscribe(data => {
      this.patients = data;
    });
  }

  openCreateModal(): void {
    this.patientToCreate = {} as PatientCreatePayload; // Reset the form
    if (this.createModal) {
      this.createModal.show();
    } else {
      console.error('Create modal instance is not available. Cannot show modal.');
    }
  }

  onCreateSubmit(): void {
    this.patientService.createPatient(this.patientToCreate).subscribe(() => {
      this.loadPatients();
      if (this.createModal) {
        this.createModal.hide();
      }
    });
  }

  openUpdateModal(patient: Patient): void {
    this.patientToUpdate = { ...patient };
    if (this.updateModal) {
      this.updateModal.show();
    } else {
      console.error('Update modal instance is not available. Cannot show modal.');
    }
  }

  onUpdateSubmit(): void {
    if (this.patientToUpdate && this.patientToUpdate.id) {
      this.patientService.updatePatient(this.patientToUpdate.id, this.patientToUpdate).subscribe(() => {
        this.loadPatients();
        if (this.updateModal) {
          this.updateModal.hide();
        }
      });
    }
  }

  openDeleteModal(patient: Patient): void {
    this.patientToDelete = patient;
    if (this.deleteModal) {
      this.deleteModal.show();
    } else {
      console.error('Delete modal instance is not available. Cannot show modal.');
    }
  }

  confirmDelete(): void {
    if (this.patientToDelete && this.patientToDelete.id) {
      this.patientService.deletePatient(this.patientToDelete.id).subscribe(() => {
        this.loadPatients();
        if (this.deleteModal) {
          this.deleteModal.hide();
        }
        this.patientToDelete = null;
      });
    }
  }
  cancelDelete(): void {
    if (this.deleteModal) {
      this.deleteModal.hide();
    }
    this.patientToDelete = null;
  }

  openDetailsModal(patient: Patient): void {
    this.patientFullDetails = null; // Reset previous data
    this.patientService.getPatientFull(patient.id).subscribe(
      (data) => {
        this.patientFullDetails = data;
        if (this.detailsModal) {
          this.detailsModal.show();
        } else {
          console.error('Details modal instance is not available. Cannot show modal.');
        }
      },
      (error) => {
        console.error('Error fetching patient details:', error);
      }
    );
  }

  closeDetailsModal(): void {
    if (this.detailsModal) {
      this.detailsModal.hide();
    }
    this.patientFullDetails = null;
  }
}
