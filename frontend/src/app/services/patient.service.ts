import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  sex: string;
  identifier: string;
}

export interface PatientCreatePayload {
  first_name: string;
  last_name: string;
  sex: string;
  identifier: string;
}

@Injectable({
  providedIn: 'root'
})
export class PatientService {
  private apiUrl = 'http://localhost:8000/patients';

  constructor(private http: HttpClient) { }

  getPatients(): Observable<Patient[]> {
    return this.http.get<Patient[]>(this.apiUrl);
  }

  createPatient(patient: PatientCreatePayload): Observable<Patient> {
    return this.http.post<Patient>(this.apiUrl, patient);
  }

  updatePatient(id: number, patient: Patient): Observable<Patient> {
    return this.http.put<Patient>(`${this.apiUrl}/${id}`, patient);
  }

  deletePatient(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
