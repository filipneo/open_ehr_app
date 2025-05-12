import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LabTest {
  id: number;
  composition_id: number;
  specimen_id: number;
  loinc_code: string | null;
  description: string | null;
  version: number;
}

export interface LabTestCreatePayload {
  composition_id: number;
  specimen_id: number;
  loinc_code?: string | null;
  description?: string | null;
}

export interface LabTestUpdatePayload {
  composition_id: number;
  specimen_id: number;
  loinc_code?: string | null;
  description?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class LabTestService {
  private apiUrl = 'http://localhost:8000/lab_test';

  constructor(private http: HttpClient) { }

  getLabTests(): Observable<LabTest[]> {
    return this.http.get<LabTest[]>(`${this.apiUrl}/all`);
  }

  getLabTest(id: number): Observable<LabTest> {
    return this.http.get<LabTest>(`${this.apiUrl}/${id}`);
  }

  createLabTest(payload: LabTestCreatePayload): Observable<LabTest> {
    return this.http.post<LabTest>(`${this.apiUrl}/create`, payload);
  }

  updateLabTest(id: number, payload: LabTestUpdatePayload): Observable<LabTest> {
    return this.http.put<LabTest>(`${this.apiUrl}/update/${id}`, payload);
  }

  deleteLabTest(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
