import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BloodTypePanel, BloodTypePanelService, BloodTypePanelCreatePayload, BloodTypePanelUpdatePayload } from '../../services/blood-type-panel.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-blood-type-panel-list',
  standalone: true,
  imports: [CommonModule, FormsModule], // Added CommonModule and FormsModule
  templateUrl: './blood-type-panel-list.component.html',
  styleUrl: './blood-type-panel-list.component.scss'
})
export class BloodTypePanelListComponent implements OnInit, AfterViewInit {
  bloodTypePanels: BloodTypePanel[] = [];
  panelToUpdate: BloodTypePanel = {} as BloodTypePanel;
  panelToCreate: BloodTypePanelCreatePayload = {} as BloodTypePanelCreatePayload;
  panelToDelete: BloodTypePanel | null = null;

  private updateModal: any;
  private deleteModal: any;
  private createModal: any;

  constructor(private bloodTypePanelService: BloodTypePanelService) { }

  ngOnInit(): void {
    this.loadBloodTypePanels();
  }

  ngAfterViewInit(): void {
    const bootstrap = (window as any).bootstrap;
    if (bootstrap && typeof bootstrap.Modal === 'function') {
      const updateModalEl = document.getElementById('updateBloodTypePanelModal');
      if (updateModalEl) {
        this.updateModal = new bootstrap.Modal(updateModalEl);
      } else {
        console.error('Update BloodTypePanel modal element (updateBloodTypePanelModal) not found.');
      }

      const deleteModalEl = document.getElementById('deleteBloodTypePanelModal');
      if (deleteModalEl) {
        this.deleteModal = new bootstrap.Modal(deleteModalEl);
      } else {
        console.error('Delete BloodTypePanel modal element (deleteBloodTypePanelModal) not found.');
      }

      const createModalEl = document.getElementById('createBloodTypePanelModal');
      if (createModalEl) {
        this.createModal = new bootstrap.Modal(createModalEl);
      } else {
        console.error('Create BloodTypePanel modal element (createBloodTypePanelModal) not found.');
      }
    } else {
      console.error('Bootstrap JavaScript or Bootstrap.Modal is not loaded or not available on the window object.');
      if (bootstrap) {
        console.error('Bootstrap object found, but Modal constructor is missing:', bootstrap);
      }
    }
  }

  loadBloodTypePanels(): void {
    this.bloodTypePanelService.getBloodTypePanels().subscribe(data => {
      this.bloodTypePanels = data;
    });
  }

  openCreateModal(): void {
    this.panelToCreate = { lab_test_id: 0 }; // Reset the form, ensure required fields have defaults if necessary
    if (this.createModal) {
      this.createModal.show();
    } else {
      console.error('Create modal instance is not available. Cannot show modal.');
    }
  }

  onCreateSubmit(): void {
    this.bloodTypePanelService.createBloodTypePanel(this.panelToCreate).subscribe(() => {
      this.loadBloodTypePanels();
      if (this.createModal) {
        this.createModal.hide();
      }
    });
  }

  openUpdateModal(panel: BloodTypePanel): void {
    this.panelToUpdate = { ...panel };
    if (this.updateModal) {
      this.updateModal.show();
    } else {
      console.error('Update modal instance is not available. Cannot show modal.');
    }
  }
  onUpdateSubmit(): void {
    if (this.panelToUpdate && this.panelToUpdate.id) {
      // Create update payload from the current panel data, omitting id and version
      const updatePayload: BloodTypePanelUpdatePayload = {
        lab_test_id: this.panelToUpdate.lab_test_id,
        abo_id: this.panelToUpdate.abo_id,
        rh_id: this.panelToUpdate.rh_id
      };
      
      this.bloodTypePanelService.updateBloodTypePanel(this.panelToUpdate.id, updatePayload).subscribe(() => {
        this.loadBloodTypePanels();
        if (this.updateModal) {
          this.updateModal.hide();
        }
      });
    }
  }

  openDeleteModal(panel: BloodTypePanel): void {
    this.panelToDelete = panel;
    if (this.deleteModal) {
      this.deleteModal.show();
    } else {
      console.error('Delete modal instance is not available. Cannot show modal.');
    }
  }

  confirmDelete(): void {
    if (this.panelToDelete && this.panelToDelete.id) {
      this.bloodTypePanelService.deleteBloodTypePanel(this.panelToDelete.id).subscribe(() => {
        this.loadBloodTypePanels();
        if (this.deleteModal) {
          this.deleteModal.hide();
        }
        this.panelToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) {
      this.deleteModal.hide();
    }
    this.panelToDelete = null;
  }
}
