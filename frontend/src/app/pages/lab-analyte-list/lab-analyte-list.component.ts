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
import { ReferenceRange, ReferenceRangeService } from '../../services/reference-range.service';

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
  referenceRanges: ReferenceRange[] = [];

  createFormModel: LabAnalyteResultCreatePayload = {
    lab_test_id: 0, // Will be updated in loadLabTests or openCreateModal
    loinc_code: '',
    value: '',
    unit: null,
    reference_low: null,
    reference_high: null,
    interpretation: null,
    reference_range_loinc_code: null
  };
  updateFormModel: LabAnalyteResultUpdatePayload & { id?: number } = {
    id: undefined,
    lab_test_id: 0,
    loinc_code: '',
    value: '',
    unit: null,
    reference_low: null,
    reference_high: null,
    interpretation: null,
    reference_range_loinc_code: null
  };
  analyteToDelete: LabAnalyteResult | null = null;

  private createModal: any;
  private updateModal: any;
  private deleteModal: any;

  constructor(
    private labAnalyteService: LabAnalyteService,
    private labTestService: LabTestService,
    private referenceRangeService: ReferenceRangeService
  ) { }

  ngOnInit(): void {
    this.loadLabAnalyteResults();
    this.loadLabTests();
    this.loadReferenceRanges();
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
      if (this.labTests.length > 0 && (this.createFormModel.lab_test_id === 0 || !this.createFormModel.lab_test_id) ) {
        this.createFormModel.lab_test_id = this.labTests[0].id;
      }
    });
  }

  loadReferenceRanges(): void {
    this.referenceRangeService.getReferenceRanges().subscribe((data: ReferenceRange[]) => {
      this.referenceRanges = data;
      // Optional: set default reference range if needed
      if (this.referenceRanges.length > 0 && !this.createFormModel.reference_range_loinc_code) {
        // this.createFormModel.reference_range_loinc_code = this.referenceRanges[0].loinc_code;
      }
    });
  }

  getLabTestName(labTestId: number): string {
    const labTest = this.labTests.find(lt => lt.id === labTestId);
    return labTest ? labTest.name : 'Unknown Lab Test';
  }

  getReferenceRangeDisplay(loincCode?: string | null): string {
    if (!loincCode) return 'N/A';
    const range = this.referenceRanges.find(rr => rr.loinc_code === loincCode);
    if (!range) return 'Unknown Reference Range';
    
    let display = `LOINC: ${range.loinc_code}`;
    if (range.low !== undefined && range.high !== undefined) {
      display += ` (Range: ${range.low}-${range.high} ${range.unit || ''})`;
    } else if (range.low !== undefined) {
      display += ` (Low: ${range.low} ${range.unit || ''})`;
    } else if (range.high !== undefined) {
      display += ` (High: ${range.high} ${range.unit || ''})`;
    } else if (range.unit) {
      display += ` (Unit: ${range.unit})`;
    }
    return display;
  }

  openCreateModal(): void {
    this.createFormModel = {
      lab_test_id: this.labTests.length > 0 ? this.labTests[0].id : 0,
      loinc_code: '',
      value: '',
      unit: '', // Default to empty string for form binding, will be converted to null if empty
      reference_low: '',
      reference_high: '',
      interpretation: '',
      reference_range_loinc_code: this.referenceRanges.length > 0 ? this.referenceRanges[0].loinc_code : undefined
    };
    if (this.createModal) this.createModal.show();
  }

  onCreateSubmit(): void {
    const payload: LabAnalyteResultCreatePayload = {
      ...this.createFormModel,
      unit: this.createFormModel.unit === '' ? null : this.createFormModel.unit,
      reference_low: this.createFormModel.reference_low === '' ? null : this.createFormModel.reference_low,
      reference_high: this.createFormModel.reference_high === '' ? null : this.createFormModel.reference_high,
      interpretation: this.createFormModel.interpretation === '' ? null : this.createFormModel.interpretation,
      reference_range_loinc_code: this.createFormModel.reference_range_loinc_code === undefined || this.createFormModel.reference_range_loinc_code === '' ? null : this.createFormModel.reference_range_loinc_code
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
      unit: analyte.unit || '', // Default to empty string for form binding
      reference_low: analyte.reference_low || '',
      reference_high: analyte.reference_high || '',
      interpretation: analyte.interpretation || '',
      reference_range_loinc_code: analyte.reference_range_loinc_code === null ? undefined : analyte.reference_range_loinc_code
    };
    if (this.updateModal) this.updateModal.show();
  }

  onUpdateSubmit(): void {
    if (!this.updateFormModel.id) return;
    const { id, ...data } = this.updateFormModel;
    const payload: LabAnalyteResultUpdatePayload = {
      ...data,
      unit: data.unit === '' ? null : data.unit,
      reference_low: data.reference_low === '' ? null : data.reference_low,
      reference_high: data.reference_high === '' ? null : data.reference_high,
      interpretation: data.interpretation === '' ? null : data.interpretation,
      reference_range_loinc_code: data.reference_range_loinc_code === undefined || data.reference_range_loinc_code === '' ? null : data.reference_range_loinc_code
    };
    this.labAnalyteService.updateLabAnalyteResult(id, payload).subscribe(() => {
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
