import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Composition, CompositionService, CompositionCreatePayload } from '../../services/composition.service';
import { Patient, PatientService } from '../../services/patient.service'; // Import Patient and PatientService
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-composition-list',
  standalone: true,
  imports: [CommonModule, FormsModule], // Added CommonModule and FormsModule
  templateUrl: './composition-list.component.html',
  styleUrl: './composition-list.component.scss'
})
export class CompositionListComponent implements OnInit, AfterViewInit {
  compositions: Composition[] = [];
  patients: Patient[] = []; // Add patients array
  compositionToUpdate: Composition = {} as Composition;
  compositionToCreate: CompositionCreatePayload = {} as CompositionCreatePayload;
  compositionToDelete: Composition | null = null;

  private updateModal: any;
  private deleteModal: any;
  private createModal: any;

  constructor(
    private compositionService: CompositionService,
    private patientService: PatientService // Inject PatientService
  ) { }

  ngOnInit(): void {
    this.loadCompositions();
    this.loadPatients(); // Load patients on init
  }

  ngAfterViewInit(): void {
    const bootstrap = (window as any).bootstrap;
    if (bootstrap && typeof bootstrap.Modal === 'function') {
      const updateModalEl = document.getElementById('updateCompositionModal');
      if (updateModalEl) {
        this.updateModal = new bootstrap.Modal(updateModalEl);
      } else {
        console.error('Update Composition modal element (updateCompositionModal) not found.');
      }

      const deleteModalEl = document.getElementById('deleteCompositionModal');
      if (deleteModalEl) {
        this.deleteModal = new bootstrap.Modal(deleteModalEl);
      } else {
        console.error('Delete Composition modal element (deleteCompositionModal) not found.');
      }

      const createModalEl = document.getElementById('createCompositionModal');
      if (createModalEl) {
        this.createModal = new bootstrap.Modal(createModalEl);
      } else {
        console.error('Create Composition modal element (createCompositionModal) not found.');
      }
    } else {
      console.error('Bootstrap JavaScript or Bootstrap.Modal is not loaded or not available on the window object.');
      if (bootstrap) {
        console.error('Bootstrap object found, but Modal constructor is missing:', bootstrap);
      }
    }
  }

  loadCompositions(): void {
    this.compositionService.getCompositions().subscribe(data => {
      this.compositions = data;
    });
  }

  loadPatients(): void { // Method to load patients
    this.patientService.getPatients().subscribe(data => {
      this.patients = data;
    });
  }

  getPatientName(patientId: number): string { // Method to get patient name
    const patient = this.patients.find(p => p.id === patientId);
    return patient ? `${patient.first_name} ${patient.last_name}` : 'Unknown Patient';
  }

  openCreateModal(): void {
    // Ensure a default patient_id is selected if patients list is not empty
    const defaultPatientId = this.patients.length > 0 ? this.patients[0].id : 0;
    this.compositionToCreate = { 
      patient_id: defaultPatientId, 
      start_time: new Date().toISOString().slice(0, 16) 
    };
    if (this.createModal) {
      this.createModal.show();
    } else {
      console.error('Create modal instance is not available. Cannot show modal.');
    }
  }

  onCreateSubmit(): void {
    // Ensure start_time is in ISO format if needed by backend, or adjust as necessary
    this.compositionToCreate.start_time = new Date(this.compositionToCreate.start_time).toISOString();
    this.compositionService.createComposition(this.compositionToCreate).subscribe(() => {
      this.loadCompositions();
      if (this.createModal) {
        this.createModal.hide();
      }
    });
  }

  openUpdateModal(composition: Composition): void {
    this.compositionToUpdate = { ...composition };
    // Format start_time for datetime-local input
    if (this.compositionToUpdate.start_time) {
      // Ensure the date is valid before trying to slice it
      try {
        const date = new Date(this.compositionToUpdate.start_time);
        if (!isNaN(date.getTime())) {
          this.compositionToUpdate.start_time = date.toISOString().slice(0,16);
        } else {
          // Handle invalid date string if necessary, perhaps set to now or clear
          console.warn('Invalid start_time for composition update:', composition.start_time);
          this.compositionToUpdate.start_time = new Date().toISOString().slice(0,16);
        }
      } catch (e) {
        console.error('Error processing start_time for update:', e);
        this.compositionToUpdate.start_time = new Date().toISOString().slice(0,16);
      }
    }
    if (this.updateModal) {
      this.updateModal.show();
    } else {
      console.error('Update modal instance is not available. Cannot show modal.');
    }
  }

  onUpdateSubmit(): void {
    if (this.compositionToUpdate && this.compositionToUpdate.id) {
      // Ensure start_time is in ISO format if needed by backend
      this.compositionToUpdate.start_time = new Date(this.compositionToUpdate.start_time).toISOString();
      this.compositionService.updateComposition(this.compositionToUpdate.id, this.compositionToUpdate).subscribe(() => {
        this.loadCompositions();
        if (this.updateModal) {
          this.updateModal.hide();
        }
      });
    }
  }

  openDeleteModal(composition: Composition): void {
    this.compositionToDelete = composition;
    if (this.deleteModal) {
      this.deleteModal.show();
    } else {
      console.error('Delete modal instance is not available. Cannot show modal.');
    }
  }

  confirmDelete(): void {
    if (this.compositionToDelete && this.compositionToDelete.id) {
      this.compositionService.deleteComposition(this.compositionToDelete.id).subscribe(() => {
        this.loadCompositions();
        if (this.deleteModal) {
          this.deleteModal.hide();
        }
        this.compositionToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) {
      this.deleteModal.hide();
    }
    this.compositionToDelete = null;
  }
}
