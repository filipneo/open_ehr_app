import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CbcPanel, CbcPanelService, CbcPanelCreatePayload, CbcPanelUpdatePayload } from '../../services/cbc-panel.service';
import { LabTest, LabTestService } from '../../services/lab-test.service';
import { LabAnalyteResult, LabAnalyteService } from '../../services/lab-analyte.service'; // For FKs

declare var bootstrap: any;

@Component({
  selector: 'app-cbc-panel-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cbc-panel-list.component.html',
  styleUrls: ['./cbc-panel-list.component.scss']
})
export class CbcPanelListComponent implements OnInit, AfterViewInit {
  cbcPanels: CbcPanel[] = [];
  labTests: LabTest[] = [];
  labAnalyteResults: LabAnalyteResult[] = []; // For Hemoglobin, White Cell, Platelet dropdowns

  createFormModel: CbcPanelCreatePayload = {
    lab_test_id: 0,
    hemoglobin_id: 0,
    white_cell_id: 0,
    platelet_id: 0
  };
  updateFormModel: CbcPanelUpdatePayload & { id?: number } = {
    id: undefined,
    lab_test_id: 0,
    hemoglobin_id: 0,
    white_cell_id: 0,
    platelet_id: 0
  };
  panelToDelete: CbcPanel | null = null;

  private createModal: any;
  private updateModal: any;
  private deleteModal: any;

  constructor(
    private cbcPanelService: CbcPanelService,
    private labTestService: LabTestService,
    private labAnalyteService: LabAnalyteService
  ) { }

  ngOnInit(): void {
    this.loadCbcPanels();
    this.loadLabTests();
    this.loadLabAnalyteResults();
  }

  ngAfterViewInit(): void {
    const createModalEl = document.getElementById('createCbcPanelModal');
    if (createModalEl) this.createModal = new bootstrap.Modal(createModalEl);
    else console.error('Create CbcPanel modal (createCbcPanelModal) not found.');

    const updateModalEl = document.getElementById('updateCbcPanelModal');
    if (updateModalEl) this.updateModal = new bootstrap.Modal(updateModalEl);
    else console.error('Update CbcPanel modal (updateCbcPanelModal) not found.');

    const deleteModalEl = document.getElementById('deleteCbcPanelModal');
    if (deleteModalEl) this.deleteModal = new bootstrap.Modal(deleteModalEl);
    else console.error('Delete CbcPanel modal (deleteCbcPanelModal) not found.');
  }

  loadCbcPanels(): void {
    this.cbcPanelService.getCbcPanels().subscribe((data: CbcPanel[]) => {
      this.cbcPanels = data;
    });
  }

  loadLabTests(): void {
    this.labTestService.getLabTests().subscribe((data: LabTest[]) => {
      this.labTests = data;
      if (this.labTests.length > 0 && (this.createFormModel.lab_test_id === 0 || !this.createFormModel.lab_test_id)) {
        // Set default for create form if not already set and lab tests are loaded
        this.createFormModel.lab_test_id = this.labTests[0].id;
      }
    });
  }

  loadLabAnalyteResults(): void {
    this.labAnalyteService.getLabAnalyteResults().subscribe((data: LabAnalyteResult[]) => {
      this.labAnalyteResults = data;
      if (this.labAnalyteResults.length > 0) {
        // Set defaults for create form if not already set and analytes are loaded
        if (this.createFormModel.hemoglobin_id === 0 || !this.createFormModel.hemoglobin_id) {
           // this.createFormModel.hemoglobin_id = this.labAnalyteResults[0].id; // Example default
        }
        if (this.createFormModel.white_cell_id === 0 || !this.createFormModel.white_cell_id) {
          // this.createFormModel.white_cell_id = this.labAnalyteResults[0].id; // Example default
        }
        if (this.createFormModel.platelet_id === 0 || !this.createFormModel.platelet_id) {
          // this.createFormModel.platelet_id = this.labAnalyteResults[0].id; // Example default
        }
      }
    });
  }

  getLabTestName(labTestId: number): string {
    const labTest = this.labTests.find(lt => lt.id === labTestId);
    return labTest ? labTest.name : 'Unknown Lab Test';
  }

  getLabAnalyteDisplay(analyteId: number): string {
    const analyte = this.labAnalyteResults.find(lar => lar.id === analyteId);
    return analyte ? `ID: ${analyte.id} (${analyte.loinc_code} - ${analyte.value} ${analyte.unit || ''})` : 'Unknown Analyte';
  }

  openCreateModal(): void {
    this.createFormModel = {
      lab_test_id: this.labTests.length > 0 ? this.labTests[0].id : 0,
      hemoglobin_id: this.labAnalyteResults.length > 0 ? this.labAnalyteResults[0].id : 0, 
      white_cell_id: this.labAnalyteResults.length > 0 ? this.labAnalyteResults[0].id : 0, 
      platelet_id: this.labAnalyteResults.length > 0 ? this.labAnalyteResults[0].id : 0,
    };
    if (this.createModal) this.createModal.show();
  }

  onCreateSubmit(): void {
    this.cbcPanelService.createCbcPanel(this.createFormModel).subscribe(() => {
      this.loadCbcPanels();
      if (this.createModal) this.createModal.hide();
    });
  }

  openUpdateModal(panel: CbcPanel): void {
    this.updateFormModel = {
      id: panel.id,
      lab_test_id: panel.lab_test_id,
      hemoglobin_id: panel.hemoglobin_id,
      white_cell_id: panel.white_cell_id,
      platelet_id: panel.platelet_id,
    };
    if (this.updateModal) this.updateModal.show();
  }

  onUpdateSubmit(): void {
    if (!this.updateFormModel.id) return;
    const { id, ...payload } = this.updateFormModel;
    this.cbcPanelService.updateCbcPanel(id, payload).subscribe(() => {
      this.loadCbcPanels();
      if (this.updateModal) this.updateModal.hide();
    });
  }

  openDeleteModal(panel: CbcPanel): void {
    this.panelToDelete = panel;
    if (this.deleteModal) this.deleteModal.show();
  }

  confirmDelete(): void {
    if (this.panelToDelete && this.panelToDelete.id) {
      this.cbcPanelService.deleteCbcPanel(this.panelToDelete.id).subscribe(() => {
        this.loadCbcPanels();
        if (this.deleteModal) this.deleteModal.hide();
        this.panelToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) this.deleteModal.hide();
    this.panelToDelete = null;
  }
}
