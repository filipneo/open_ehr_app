import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LabTest {
  id: number;
  name: string;
  description?: string;
  loinc_code?: string;
  composition_id?: number; // Foreign Key to Composition
  specimen_id?: number;    // Foreign Key to Specimen
  version?: number;
}

export interface LabTestCreatePayload {
  name: string;
  description?: string | null; // Allow null
  loinc_code?: string | null;  // Allow null
  composition_id?: number | null; // Allow null
  specimen_id?: number | null;    // Allow null
}

export interface LabTestUpdatePayload {
  name?: string;
  description?: string | null; // Allow null
  loinc_code?: string | null;  // Allow null
  composition_id?: number | null; // Allow null
  specimen_id?: number | null;    // Allow null
}

@Injectable({
  providedIn: 'root'
})
export class LabTestService {
  private apiUrl = 'http://localhost:8000/lab_tests';

  constructor(private http: HttpClient) { }

  getLabTests(): Observable<LabTest[]> {
    return this.http.get<LabTest[]>(this.apiUrl);
  }

  getLabTest(id: number): Observable<LabTest> {
    return this.http.get<LabTest>(`${this.apiUrl}/${id}`);
  }

  createLabTest(payload: LabTestCreatePayload): Observable<LabTest> {
    return this.http.post<LabTest>(this.apiUrl, payload);
  }

  updateLabTest(id: number, payload: LabTestUpdatePayload): Observable<LabTest> {
    return this.http.put<LabTest>(`${this.apiUrl}/${id}`, payload);
  }

  deleteLabTest(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
