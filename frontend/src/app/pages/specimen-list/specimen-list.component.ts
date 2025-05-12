import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Specimen, SpecimenService, SpecimenCreatePayload, SpecimenUpdatePayload } from '../../services/specimen.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-specimen-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './specimen-list.component.html',
  styleUrl: './specimen-list.component.scss'
})
export class SpecimenListComponent implements OnInit, AfterViewInit {
  specimens: Specimen[] = [];
  specimenToUpdate: Specimen = {} as Specimen;
  specimenToCreate: SpecimenCreatePayload = {} as SpecimenCreatePayload;
  specimenToDelete: Specimen | null = null;

  private updateModal: any;
  private deleteModal: any;
  private createModal: any;

  constructor(private specimenService: SpecimenService) { }

  ngOnInit(): void {
    this.loadSpecimens();
  }

  ngAfterViewInit(): void {
    const bootstrap = (window as any).bootstrap;
    if (bootstrap && typeof bootstrap.Modal === 'function') {
      const updateModalEl = document.getElementById('updateSpecimenModal');
      if (updateModalEl) {
        this.updateModal = new bootstrap.Modal(updateModalEl);
      } else {
        console.error('Update Specimen modal element (updateSpecimenModal) not found.');
      }

      const deleteModalEl = document.getElementById('deleteSpecimenModal');
      if (deleteModalEl) {
        this.deleteModal = new bootstrap.Modal(deleteModalEl);
      } else {
        console.error('Delete Specimen modal element (deleteSpecimenModal) not found.');
      }

      const createModalEl = document.getElementById('createSpecimenModal');
      if (createModalEl) {
        this.createModal = new bootstrap.Modal(createModalEl);
      } else {
        console.error('Create Specimen modal element (createSpecimenModal) not found.');
      }
    } else {
      console.error('Bootstrap JavaScript or Bootstrap.Modal is not loaded or not available on the window object.');
      if (bootstrap) {
        console.error('Bootstrap object found, but Modal constructor is missing:', bootstrap);
      }
    }
  }

  loadSpecimens(): void {
    this.specimenService.getSpecimens().subscribe(data => {
      this.specimens = data;
    });
  }

  openCreateModal(): void {
    this.specimenToCreate = {
      specimen_type: '',
      collection_time: new Date().toISOString().slice(0, 16) // Default to current time
    };
    if (this.createModal) {
      this.createModal.show();
    } else {
      console.error('Create modal instance is not available. Cannot show modal.');
    }
  }

  onCreateSubmit(): void {
    // Ensure collection_time is in ISO format
    this.specimenToCreate.collection_time = new Date(this.specimenToCreate.collection_time).toISOString();
    this.specimenService.createSpecimen(this.specimenToCreate).subscribe(() => {
      this.loadSpecimens();
      if (this.createModal) {
        this.createModal.hide();
      }
    });
  }

  openUpdateModal(specimen: Specimen): void {
    this.specimenToUpdate = { ...specimen };
    // Format collection_time for datetime-local input
    if (this.specimenToUpdate.collection_time) {
      try {
        const date = new Date(this.specimenToUpdate.collection_time);
        if (!isNaN(date.getTime())) {
          this.specimenToUpdate.collection_time = date.toISOString().slice(0, 16);
        } else {
          this.specimenToUpdate.collection_time = new Date().toISOString().slice(0, 16);
        }
      } catch (e) {
        this.specimenToUpdate.collection_time = new Date().toISOString().slice(0, 16);
      }
    }
    if (this.updateModal) {
      this.updateModal.show();
    } else {
      console.error('Update modal instance is not available. Cannot show modal.');
    }
  }

  onUpdateSubmit(): void {
    if (this.specimenToUpdate && this.specimenToUpdate.id) {
      // Ensure collection_time is in ISO format
      this.specimenToUpdate.collection_time = new Date(this.specimenToUpdate.collection_time).toISOString();
      const { id, ...updatePayload } = this.specimenToUpdate;
      this.specimenService.updateSpecimen(id, updatePayload as SpecimenUpdatePayload).subscribe(() => {
        this.loadSpecimens();
        if (this.updateModal) {
          this.updateModal.hide();
        }
      });
    }
  }

  openDeleteModal(specimen: Specimen): void {
    this.specimenToDelete = specimen;
    if (this.deleteModal) {
      this.deleteModal.show();
    } else {
      console.error('Delete modal instance is not available. Cannot show modal.');
    }
  }

  confirmDelete(): void {
    if (this.specimenToDelete && this.specimenToDelete.id) {
      this.specimenService.deleteSpecimen(this.specimenToDelete.id).subscribe(() => {
        this.loadSpecimens();
        if (this.deleteModal) {
          this.deleteModal.hide();
        }
        this.specimenToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) {
      this.deleteModal.hide();
    }
    this.specimenToDelete = null;
  }
}
