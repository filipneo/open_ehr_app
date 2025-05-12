import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BodyMeasurement {
  id: number;
  patient_id: number;
  record_time: string; // ISO string format
  value: number;
  unit: string;
  snomed_code: string;
  version: number;
}

export interface BodyMeasurementCreatePayload {
  patient_id: number;
  record_time: string; // ISO string format
  value: number;
  unit: string;
  snomed_code: string;
}

export interface BodyMeasurementUpdatePayload {
  patient_id?: number; 
  record_time?: string; // ISO string format
  value?: number;
  unit?: string;
  snomed_code?: string;
}

@Injectable({
  providedIn: 'root'
})
export class BodyMeasurementService {
  private apiUrl = 'http://localhost:8000/body_measurement'; 

  constructor(private http: HttpClient) { }

  getBodyMeasurements(): Observable<BodyMeasurement[]> {
    return this.http.get<BodyMeasurement[]>(`${this.apiUrl}/all`);
  }

  getBodyMeasurement(id: number): Observable<BodyMeasurement> {
    return this.http.get<BodyMeasurement>(`${this.apiUrl}/${id}`);
  }

  createBodyMeasurement(payload: BodyMeasurementCreatePayload): Observable<BodyMeasurement> {
    return this.http.post<BodyMeasurement>(`${this.apiUrl}/create`, payload);
  }

  updateBodyMeasurement(id: number, payload: BodyMeasurementUpdatePayload): Observable<BodyMeasurement> {
    return this.http.put<BodyMeasurement>(`${this.apiUrl}/update/${id}`, payload);
  }

  deleteBodyMeasurement(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
