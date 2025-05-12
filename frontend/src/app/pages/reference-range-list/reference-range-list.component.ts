import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ReferenceRange, ReferenceRangeService, ReferenceRangeCreatePayload, ReferenceRangeUpdatePayload } from '../../services/reference-range.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-reference-range-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reference-range-list.component.html',
  styleUrl: './reference-range-list.component.scss'
})
export class ReferenceRangeListComponent implements OnInit, AfterViewInit {
  referenceRanges: ReferenceRange[] = [];
  rangeToUpdate: ReferenceRange = {} as ReferenceRange; // For holding the range being updated
  rangeToCreate: ReferenceRangeCreatePayload = {} as ReferenceRangeCreatePayload; // For the create form
  rangeToDelete: ReferenceRange | null = null;

  // Store the original loinc_code for update, as it cannot be changed.
  originalLoincCodeForUpdate: string | null = null;

  private updateModal: any;
  private deleteModal: any;
  private createModal: any;

  constructor(private referenceRangeService: ReferenceRangeService) { }

  ngOnInit(): void {
    this.loadReferenceRanges();
  }

  ngAfterViewInit(): void {
    const bootstrap = (window as any).bootstrap;
    if (bootstrap && typeof bootstrap.Modal === 'function') {
      const updateModalEl = document.getElementById('updateReferenceRangeModal');
      if (updateModalEl) {
        this.updateModal = new bootstrap.Modal(updateModalEl);
      } else {
        console.error('Update ReferenceRange modal element (updateReferenceRangeModal) not found.');
      }

      const deleteModalEl = document.getElementById('deleteReferenceRangeModal');
      if (deleteModalEl) {
        this.deleteModal = new bootstrap.Modal(deleteModalEl);
      } else {
        console.error('Delete ReferenceRange modal element (deleteReferenceRangeModal) not found.');
      }

      const createModalEl = document.getElementById('createReferenceRangeModal');
      if (createModalEl) {
        this.createModal = new bootstrap.Modal(createModalEl);
      } else {
        console.error('Create ReferenceRange modal element (createReferenceRangeModal) not found.');
      }
    } else {
      console.error('Bootstrap JavaScript or Bootstrap.Modal is not loaded or not available on the window object.');
      if (bootstrap) {
        console.error('Bootstrap object found, but Modal constructor is missing:', bootstrap);
      }
    }
  }

  loadReferenceRanges(): void {
    this.referenceRangeService.getReferenceRanges().subscribe(data => {
      this.referenceRanges = data;
    });
  }

  openCreateModal(): void {
    this.rangeToCreate = { loinc_code: '' }; // Reset the form
    if (this.createModal) {
      this.createModal.show();
    } else {
      console.error('Create modal instance is not available. Cannot show modal.');
    }
  }

  onCreateSubmit(): void {
    this.referenceRangeService.createReferenceRange(this.rangeToCreate).subscribe(() => {
      this.loadReferenceRanges();
      if (this.createModal) {
        this.createModal.hide();
      }
    });
  }

  openUpdateModal(range: ReferenceRange): void {
    // Deep copy the range to avoid modifying the list directly
    this.rangeToUpdate = { ...range }; 
    this.originalLoincCodeForUpdate = range.loinc_code; // Store the original loinc_code
    if (this.updateModal) {
      this.updateModal.show();
    } else {
      console.error('Update modal instance is not available. Cannot show modal.');
    }
  }

  onUpdateSubmit(): void {
    if (this.rangeToUpdate && this.originalLoincCodeForUpdate) {
      // Prepare the payload, excluding the loinc_code itself from the body if it's immutable
      const { loinc_code, ...updatePayload } = this.rangeToUpdate;
      this.referenceRangeService.updateReferenceRange(this.originalLoincCodeForUpdate, updatePayload as ReferenceRangeUpdatePayload).subscribe(() => {
        this.loadReferenceRanges();
        if (this.updateModal) {
          this.updateModal.hide();
        }
        this.originalLoincCodeForUpdate = null;
      });
    }
  }

  openDeleteModal(range: ReferenceRange): void {
    this.rangeToDelete = range;
    if (this.deleteModal) {
      this.deleteModal.show();
    } else {
      console.error('Delete modal instance is not available. Cannot show modal.');
    }
  }

  confirmDelete(): void {
    if (this.rangeToDelete && this.rangeToDelete.loinc_code) {
      this.referenceRangeService.deleteReferenceRange(this.rangeToDelete.loinc_code).subscribe(() => {
        this.loadReferenceRanges();
        if (this.deleteModal) {
          this.deleteModal.hide();
        }
        this.rangeToDelete = null;
      });
    }
  }

  cancelDelete(): void {
    if (this.deleteModal) {
      this.deleteModal.hide();
    }
    this.rangeToDelete = null;
  }
}
