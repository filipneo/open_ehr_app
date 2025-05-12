import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  sex: 'male' | 'female';
  identifier: string | null;
  version: number;
}

export interface PatientCreatePayload {
  first_name: string;
  last_name: string;
  sex: 'male' | 'female';
  identifier?: string | null;
}

export interface PatientFull {
  id: number;
  first_name: string;
  last_name: string;
  sex: 'male' | 'female';
  identifier: string | null;
  version: number;
  compositions: Composition[];
  body_measurements: BodyMeasurement[];
}

export interface Composition {
  id: number;
  start_time: string;
  version: number;
  lab_tests: LabTest[];
}

export interface LabTest {
  id: number;
  loinc_code: string;
  description: string | null;
  version: number;
  specimen: Specimen | null;
  analytes: LabAnalyte[];
}

export interface Specimen {
  id: number;
  type: string;
  collection_time: string;
  snomed_code: string;
  description: string;
  version: number;
}

export interface LabAnalyte {
  id: number;
  loinc_code: string;
  value: number;
  unit: string;
  reference_low: number | null;
  reference_high: number | null;
  interpretation: string | null;
  version: number;
}

export interface BodyMeasurement {
  id: number;
  record_time: string;
  value: number;
  unit: string;
  snomed_code: string;
  version: number;
}

@Injectable({
  providedIn: 'root'
})
export class PatientService {
  private apiUrl = 'http://localhost:8000/patient';

  constructor(private http: HttpClient) { }

  getPatients(): Observable<Patient[]> {
    return this.http.get<Patient[]>(`${this.apiUrl}/all`);
  }

  getPatientFull(id: number): Observable<PatientFull> {
    return this.http.get<PatientFull>(`${this.apiUrl}/${id}/full`);
  }

  createPatient(patient: PatientCreatePayload): Observable<Patient> {
    return this.http.post<Patient>(`${this.apiUrl}/create`, patient);
  }

  updatePatient(id: number, patient: Patient): Observable<Patient> {
    return this.http.put<Patient>(`${this.apiUrl}/update/${id}`, patient);
  }

  deletePatient(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
