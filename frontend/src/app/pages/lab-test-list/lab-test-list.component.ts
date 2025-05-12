import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LabTest, LabTestService, LabTestCreatePayload, LabTestUpdatePayload } from '../../services/lab-test.service';
import { Composition, CompositionService } from '../../services/composition.service';
import { PatientService, Patient } from '../../services/patient.service'; // Corrected import path
import { Specimen, SpecimenService } from '../../services/specimen.service';

declare var bootstrap: any; // Declare bootstrap for modal usage

@Component({
  selector: 'app-lab-test-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lab-test-list.component.html',
  styleUrls: ['./lab-test-list.component.scss']
})
export class LabTestListComponent implements OnInit, AfterViewInit {
  labTests: LabTest[] = [];
  compositions: Composition[] = [];
  specimens: Specimen[] = [];
  patients: Patient[] = []; // To display patient names for compositions

  // Form model for creating a LabTest
  createFormModel = {
    loinc_code: '',
    composition_id: undefined as number | undefined,
    specimen_id: undefined as number | undefined,
  };

  // Form model for updating a LabTest
  updateFormModel = {
    id: undefined as number | undefined,
    loinc_code: '',
    composition_id: undefined as number | undefined,
    specimen_id: undefined as number | undefined,
    version: 1
  };

  testToDelete: LabTest | null = null;

  private createModal: any;
  private updateModal: any;
  private deleteModal: any;

  constructor(
    private labTestService: LabTestService,
    private compositionService: CompositionService,
    private specimenService: SpecimenService,
    private patientService: PatientService // Inject PatientService
  ) { }

  ngOnInit(): void {
    this.loadLabTests();
    this.loadPatients(); // Load patients first or concurrently
    this.loadCompositions();
    this.loadSpecimens();
  }

  ngAfterViewInit(): void {
    const createModalEl = document.getElementById('createLabTestModal');
    if (createModalEl) this.createModal = new bootstrap.Modal(createModalEl);
    else console.error('Create LabTest modal (createLabTestModal) not found.');

    const updateModalEl = document.getElementById('updateLabTestModal');
    if (updateModalEl) this.updateModal = new bootstrap.Modal(updateModalEl);
    else console.error('Update LabTest modal (updateLabTestModal) not found.');

    const deleteModalEl = document.getElementById('deleteLabTestModal');
    if (deleteModalEl) this.deleteModal = new bootstrap.Modal(deleteModalEl);
    else console.error('Delete LabTest modal (deleteLabTestModal) not found.');
  }

  loadLabTests(): void {
    this.labTestService.getLabTests().subscribe((data: LabTest[]) => this.labTests = data);
  }

  loadPatients(): void {
    this.patientService.getPatients().subscribe((data: Patient[]) => this.patients = data);
  }

  loadCompositions(): void {
    this.compositionService.getCompositions().subscribe((data: Composition[]) => {
      this.compositions = data;
      // Optionally set default for create form if not already set and compositions are loaded
      if (this.compositions.length > 0 && this.createFormModel.composition_id === undefined) {
        // this.createFormModel.composition_id = this.compositions[0].id; // Example: default to first
      }
    });
  }

  loadSpecimens(): void {
    this.specimenService.getSpecimens().subscribe((data: Specimen[]) => { // Added type Specimen[] for data
      this.specimens = data;
      // Optionally set default for create form
      if (this.specimens.length > 0 && this.createFormModel.specimen_id === undefined) {
        // this.createFormModel.specimen_id = this.specimens[0].id; // Example: default to first
      }
    });
  }

  getPatientName(patientId: number): string {
    const patient = this.patients.find(p => p.id === patientId);
    return patient ? `${patient.first_name} ${patient.last_name}` : 'Unknown Patient';
  }

  getCompositionDisplay(compositionId?: number): string {
    if (compositionId === undefined || compositionId === null) return 'N/A';
    const composition = this.compositions.find(c => c.id === compositionId);
    if (!composition) return 'Unknown Composition';
    const patientName = this.getPatientName(composition.patient_id);
    return `Comp ID: ${composition.id} (Patient: ${patientName}, Start: ${new Date(composition.start_time).toLocaleDateString()})`;
  }

  getSpecimenDisplay(specimenId?: number): string {
    if (specimenId === undefined || specimenId === null) return 'N/A';
    const specimen = this.specimens.find(s => s.id === specimenId);
    return specimen ? `${specimen.specimen_type} (ID: ${specimen.id}, Collected: ${new Date(specimen.collection_time).toLocaleDateString()})` : 'Unknown Specimen';
  }

  openCreateModal(): void {
    this.createFormModel = {
      loinc_code: '',
      composition_id: this.compositions.length > 0 ? this.compositions[0].id : undefined,
      specimen_id: this.specimens.length > 0 ? this.specimens[0].id : undefined,
    };
    if (this.createModal) this.createModal.show();
  }

  onCreateSubmit(): void {
    // Ensure that composition_id and specimen_id are defined
    if (this.createFormModel.composition_id === undefined || this.createFormModel.specimen_id === undefined) {
      alert('Composition and Specimen are required fields');
      return;
    }
    
    const payload: LabTestCreatePayload = {
      composition_id: this.createFormModel.composition_id,
      specimen_id: this.createFormModel.specimen_id,
      loinc_code: this.createFormModel.loinc_code === '' ? null : this.createFormModel.loinc_code
    };
    this.labTestService.createLabTest(payload).subscribe(() => {
      this.loadLabTests();
      if (this.createModal) this.createModal.hide();
    });
  }

  openUpdateModal(labTest: LabTest): void {
    this.updateFormModel = {
      id: labTest.id,
      loinc_code: labTest.loinc_code || '',
      composition_id: labTest.composition_id,
      specimen_id: labTest.specimen_id,
      version: labTest.version
    };
    if (this.updateModal) this.updateModal.show();
  }

  onUpdateSubmit(): void {
    if (!this.updateFormModel.id) {
      console.error("Cannot update without an ID.");
      return;
    }
    
    // Ensure that composition_id and specimen_id are defined
    if (this.updateFormModel.composition_id === undefined || this.updateFormModel.specimen_id === undefined) {
      alert('Composition and Specimen are required fields');
      return;
    }
    
    const payload: LabTestUpdatePayload = {
      composition_id: this.updateFormModel.composition_id,
      specimen_id: this.updateFormModel.specimen_id,
      loinc_code: this.updateFormModel.loinc_code === '' ? null : this.updateFormModel.loinc_code
    };
    this.labTestService.updateLabTest(this.updateFormModel.id, payload).subscribe(() => {
      this.loadLabTests();
      if (this.updateModal) this.updateModal.hide();
    });
  }

  openDeleteModal(labTest: LabTest): void {
    this.testToDelete = labTest;
    if (this.deleteModal) this.deleteModal.show();
  }

  confirmDelete(): void {
    if (this.testToDelete && this.testToDelete.id) {
      this.labTestService.deleteLabTest(this.testToDelete.id).subscribe(() => {
        this.loadLabTests();
        if (this.deleteModal) this.deleteModal.hide();
        this.testToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) this.deleteModal.hide();
    this.testToDelete = null;
  }
}
