import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LabAnalyteResult {
  id: number;
  lab_test_id: number;
  loinc_code: string;
  value: number;
  unit: string;
  reference_low: number | null;
  reference_high: number | null;
  interpretation: string | null;
  version: number;
}

export interface LabAnalyteResultCreatePayload {
  lab_test_id: number;
  loinc_code: string;
  value: number;
  unit: string;
  reference_low?: number | null;
  reference_high?: number | null;
  interpretation?: string | null;
}

export interface LabAnalyteResultUpdatePayload {
  lab_test_id: number;
  loinc_code: string;
  value: number;
  unit: string;
  reference_low?: number | null;
  reference_high?: number | null;
  interpretation?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class LabAnalyteService {
  private apiUrl = 'http://localhost:8000/lab_analyte';

  constructor(private http: HttpClient) { }

  getLabAnalyteResults(): Observable<LabAnalyteResult[]> {
    return this.http.get<LabAnalyteResult[]>(`${this.apiUrl}/all`);
  }

  getLabAnalyteResult(id: number): Observable<LabAnalyteResult> {
    return this.http.get<LabAnalyteResult>(`${this.apiUrl}/${id}`);
  }

  createLabAnalyteResult(payload: LabAnalyteResultCreatePayload): Observable<LabAnalyteResult> {
    return this.http.post<LabAnalyteResult>(`${this.apiUrl}/create`, payload);
  }

  updateLabAnalyteResult(id: number, payload: LabAnalyteResultUpdatePayload): Observable<LabAnalyteResult> {
    return this.http.put<LabAnalyteResult>(`${this.apiUrl}/update/${id}`, payload);
  }

  deleteLabAnalyteResult(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
