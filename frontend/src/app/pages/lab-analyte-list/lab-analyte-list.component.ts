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
  selectedReferenceRange: ReferenceRange | null = null;

  createFormModel: LabAnalyteResultCreatePayload = {
    lab_test_id: 0,
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
      if (this.labTests.length > 0 && (this.createFormModel.lab_test_id === 0 || !this.createFormModel.lab_test_id)) {
        this.createFormModel.lab_test_id = this.labTests[0].id;
      }
    });
  }

  loadReferenceRanges(): void {
    this.referenceRangeService.getReferenceRanges().subscribe(data => {
      this.referenceRanges = data;
    });
  }

  getLabTestName(labTestId: number): string {
    const test = this.labTests.find(lt => lt.id === labTestId);
    if (!test) return 'Unknown Lab Test';
    
    // Return a descriptive name with the test description if available
    return test.description 
      ? `Lab Test ${test.id}: ${test.description}` 
      : `Lab Test ID: ${test.id} (LOINC: ${test.loinc_code || 'N/A'})`;
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
    // Validate that a reference range was selected
    if (!this.createFormModel.loinc_code) {
      alert('Please select a reference range');
      return;
    }
    
      // Calculate interpretation based on value and reference range
    let interpretation = this.createFormModel.interpretation;
    if (!interpretation) {
      const value = this.createFormModel.value;
      const low = this.createFormModel.reference_low;
      const high = this.createFormModel.reference_high;
      
      if (low !== null && low !== undefined && value < low) {
        interpretation = 'L'; // Low
      } else if (high !== null && high !== undefined && value > high) {
        interpretation = 'H'; // High
      } else {
        interpretation = 'N'; // Normal
      }
    }
    
    const payload: LabAnalyteResultCreatePayload = {
      lab_test_id: this.createFormModel.lab_test_id,
      loinc_code: this.createFormModel.loinc_code,
      value: this.createFormModel.value,
      unit: this.createFormModel.unit,
      reference_low: this.createFormModel.reference_low,
      reference_high: this.createFormModel.reference_high,
      interpretation: interpretation
    };
    
    this.labAnalyteService.createLabAnalyteResult(payload).subscribe(
      () => {
        this.loadLabAnalyteResults();
        if (this.createModal) this.createModal.hide();
      },
      error => {
        console.error('Error creating lab analyte:', error);
        alert('Failed to create lab analyte. Please check the console for details.');
      }
    );
  }
  
  // Helper method to automatically determine the interpretation based on the value and reference ranges
  private getInterpretation(value: number, low: number | null, high: number | null): string {
    if (low !== null && value < low) {
      return 'L'; // Low
    } else if (high !== null && value > high) {
      return 'H'; // High
    } else {
      return 'N'; // Normal
    }
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
    
    // Check if a matching reference range exists
    const matchingRange = this.referenceRanges.find(r => r.loinc_code === analyte.loinc_code);
    if (matchingRange) {
      this.selectedReferenceRange = matchingRange;
    } else {
      this.selectedReferenceRange = null;
    }
    
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

  onReferenceRangeChange(event: any, isUpdate: boolean = false): void {
    const selectedLoincCode = event.target.value;
    const selected = this.referenceRanges.find(r => r.loinc_code === selectedLoincCode);
    
    if (selected) {
      if (isUpdate) {
        // For update form
        this.updateFormModel.loinc_code = selected.loinc_code;
        this.updateFormModel.unit = selected.unit || '';
        this.updateFormModel.reference_low = selected.low;
        this.updateFormModel.reference_high = selected.high;
        // Auto-calculate interpretation based on the current value if it exists
        if (this.updateFormModel.value !== undefined && this.updateFormModel.value !== null) {
          this.updateFormModel.interpretation = this.getInterpretation(
            this.updateFormModel.value, 
            selected.low, 
            selected.high
          );
        }
      } else {
        // For create form
        this.createFormModel.loinc_code = selected.loinc_code;
        this.createFormModel.unit = selected.unit || '';
        this.createFormModel.reference_low = selected.low;
        this.createFormModel.reference_high = selected.high;
        // Auto-calculate interpretation based on the current value if it exists
        if (this.createFormModel.value !== undefined && this.createFormModel.value !== null) {
          this.createFormModel.interpretation = this.getInterpretation(
            this.createFormModel.value, 
            selected.low, 
            selected.high
          );
        }
      }
    }
  }

  getReferenceRangeDisplay(loincCode: string): string {
    const range = this.referenceRanges.find(r => r.loinc_code === loincCode);
    if (!range) return loincCode;
    
    const low = range.low !== null ? range.low : 'n/a';
    const high = range.high !== null ? range.high : 'n/a';
    const unit = range.unit || '';
    
    // Map common LOINC codes to more readable names
    const loincNameMap: {[key: string]: string} = {
      '718-7': 'Hemoglobin',
      '6690-2': 'White Blood Cell Count',
      '777-3': 'Platelets',
      '789-8': 'Red Blood Cell Count',
      '785-6': 'MCH',
      '4544-3': 'Hematocrit',
      '2345-7': 'Glucose',
      '2823-3': 'Potassium',
      '2951-2': 'Sodium',
      '2075-0': 'Creatinine',
      '3094-0': 'Urea',
      '2093-3': 'Total Cholesterol',
      '2571-8': 'Triglycerides',
      '2085-9': 'HDL Cholesterol',
      '18262-6': 'LDL Cholesterol',
      '882-1': 'ABO Blood Type',
      '10331-7': 'Rh Type',
      '1920-8': 'AST',
      '6768-6': 'ALT',
      '1975-2': 'Total Bilirubin'
    };
    
    const displayName = loincNameMap[loincCode] || `LOINC: ${loincCode}`;
    return `${displayName} (${low}-${high} ${unit})`;
  }
}
