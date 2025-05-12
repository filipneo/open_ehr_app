import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  LabAnalyteResult,
  LabAnalyteService,
  LabAnalyteResultCreatePayload,
  LabAnalyteResultUpdatePayload
} from '../../services/lab-analyte.service';
import { LabTest, LabTestService } from '../../services/lab-test.service';

declare var bootstrap: any;

@Component({
  selector: 'app-lab-analyte-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lab-analyte-list.component.html',
  styleUrls: ['./lab-analyte-list.component.scss']
})
export class LabAnalyteListComponent implements OnInit, AfterViewInit {
  labAnalyteResults: LabAnalyteResult[] = [];
  labTests: LabTest[] = [];

  createFormModel: LabAnalyteResultCreatePayload = {
    lab_test_id: 0, // Will be updated in loadLabTests or openCreateModal
    loinc_code: '',
    value: 0,
    unit: '',
    reference_low: null,
    reference_high: null,
    interpretation: null
  };
  
  updateFormModel: LabAnalyteResultUpdatePayload & { id?: number, version?: number } = {
    id: undefined,
    lab_test_id: 0,
    loinc_code: '',
    value: 0,
    unit: '',
    reference_low: null,
    reference_high: null,
    interpretation: null,
    version: 1
  };
  
  analyteToDelete: LabAnalyteResult | null = null;

  private createModal: any;
  private updateModal: any;
  private deleteModal: any;

  constructor(
    private labAnalyteService: LabAnalyteService,
    private labTestService: LabTestService
  ) { }

  ngOnInit(): void {
    this.loadLabAnalyteResults();
    this.loadLabTests();
  }

  ngAfterViewInit(): void {
    const createModalEl = document.getElementById('createLabAnalyteModal');
    if (createModalEl) this.createModal = new bootstrap.Modal(createModalEl);
    else console.error('Create LabAnalyte modal (createLabAnalyteModal) not found.');

    const updateModalEl = document.getElementById('updateLabAnalyteModal');
    if (updateModalEl) this.updateModal = new bootstrap.Modal(updateModalEl);
    else console.error('Update LabAnalyte modal (updateLabAnalyteModal) not found.');

    const deleteModalEl = document.getElementById('deleteLabAnalyteModal');
    if (deleteModalEl) this.deleteModal = new bootstrap.Modal(deleteModalEl);
    else console.error('Delete LabAnalyte modal (deleteLabAnalyteModal) not found.');
  }

  loadLabAnalyteResults(): void {
    this.labAnalyteService.getLabAnalyteResults().subscribe((data: LabAnalyteResult[]) => {
      this.labAnalyteResults = data;
    });
  }

  loadLabTests(): void {
    this.labTestService.getLabTests().subscribe((data: LabTest[]) => {
      this.labTests = data;
      if (this.labTests.length > 0 && (this.createFormModel.lab_test_id === 0 || !this.createFormModel.lab_test_id)) {
        this.createFormModel.lab_test_id = this.labTests[0].id;
      }
    });
  }

  getLabTestName(labTestId: number): string {
    const test = this.labTests.find(lt => lt.id === labTestId);
    return test ? `Lab Test ID: ${test.id}` : 'Unknown Lab Test';
  }

  openCreateModal(): void {
    this.createFormModel = {
      lab_test_id: this.labTests.length > 0 ? this.labTests[0].id : 0,
      loinc_code: '',
      value: 0,
      unit: '',
      reference_low: null,
      reference_high: null,
      interpretation: null
    };
    if (this.createModal) this.createModal.show();
  }

  onCreateSubmit(): void {
    const payload: LabAnalyteResultCreatePayload = {
      lab_test_id: this.createFormModel.lab_test_id,
      loinc_code: this.createFormModel.loinc_code,
      value: this.createFormModel.value,
      unit: this.createFormModel.unit,
      reference_low: this.createFormModel.reference_low,
      reference_high: this.createFormModel.reference_high,
      interpretation: this.createFormModel.interpretation
    };
    
    this.labAnalyteService.createLabAnalyteResult(payload).subscribe(() => {
      this.loadLabAnalyteResults();
      if (this.createModal) this.createModal.hide();
    });
  }

  openUpdateModal(analyte: LabAnalyteResult): void {
    this.updateFormModel = {
      id: analyte.id,
      lab_test_id: analyte.lab_test_id,
      loinc_code: analyte.loinc_code,
      value: analyte.value,
      unit: analyte.unit,
      reference_low: analyte.reference_low,
      reference_high: analyte.reference_high,
      interpretation: analyte.interpretation,
      version: analyte.version
    };
    if (this.updateModal) this.updateModal.show();
  }

  onUpdateSubmit(): void {
    if (!this.updateFormModel.id) {
      console.error("Cannot update without an ID.");
      return;
    }
    
    const payload: LabAnalyteResultUpdatePayload = {
      lab_test_id: this.updateFormModel.lab_test_id,
      loinc_code: this.updateFormModel.loinc_code,
      value: this.updateFormModel.value,
      unit: this.updateFormModel.unit,
      reference_low: this.updateFormModel.reference_low,
      reference_high: this.updateFormModel.reference_high,
      interpretation: this.updateFormModel.interpretation
    };
    
    this.labAnalyteService.updateLabAnalyteResult(this.updateFormModel.id, payload).subscribe(() => {
      this.loadLabAnalyteResults();
      if (this.updateModal) this.updateModal.hide();
    });
  }

  openDeleteModal(analyte: LabAnalyteResult): void {
    this.analyteToDelete = analyte;
    if (this.deleteModal) this.deleteModal.show();
  }

  confirmDelete(): void {
    if (this.analyteToDelete && this.analyteToDelete.id) {
      this.labAnalyteService.deleteLabAnalyteResult(this.analyteToDelete.id).subscribe(() => {
        this.loadLabAnalyteResults();
        if (this.deleteModal) this.deleteModal.hide();
        this.analyteToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) this.deleteModal.hide();
    this.analyteToDelete = null;
  }
}
