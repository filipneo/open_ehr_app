import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LabAnalyteResult {
  id: number;
  lab_test_id: number;
  loinc_code: string;
  value: string;
  unit?: string | null;
  reference_low?: string | null;
  reference_high?: string | null;
  interpretation?: string | null;
  reference_range_loinc_code?: string | null; // FK to ReferenceRange
  version?: number;
}

export interface LabAnalyteResultCreatePayload {
  lab_test_id: number;
  loinc_code: string;
  value: string;
  unit?: string | null;
  reference_low?: string | null;
  reference_high?: string | null;
  interpretation?: string | null;
  reference_range_loinc_code?: string | null;
}

export interface LabAnalyteResultUpdatePayload {
  lab_test_id?: number;
  loinc_code?: string;
  value?: string;
  unit?: string | null;
  reference_low?: string | null;
  reference_high?: string | null;
  interpretation?: string | null;
  reference_range_loinc_code?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class LabAnalyteService {
  private apiUrl = 'http://localhost:8000/lab_analytes'; // Based on backend router

  constructor(private http: HttpClient) { }

  getLabAnalyteResults(): Observable<LabAnalyteResult[]> {
    return this.http.get<LabAnalyteResult[]>(this.apiUrl);
  }

  getLabAnalyteResult(id: number): Observable<LabAnalyteResult> {
    return this.http.get<LabAnalyteResult>(`${this.apiUrl}/${id}`);
  }

  createLabAnalyteResult(payload: LabAnalyteResultCreatePayload): Observable<LabAnalyteResult> {
    return this.http.post<LabAnalyteResult>(this.apiUrl, payload);
  }

  updateLabAnalyteResult(id: number, payload: LabAnalyteResultUpdatePayload): Observable<LabAnalyteResult> {
    return this.http.put<LabAnalyteResult>(`${this.apiUrl}/${id}`, payload);
  }

  deleteLabAnalyteResult(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
