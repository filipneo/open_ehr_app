import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Specimen {
  id: number;
  specimen_type: string;
  collection_time: string; // Using string for datetime, will be handled by input type in HTML
  snomed_code: string | null;
  description: string | null;
  version: number;
}

export interface SpecimenCreatePayload {
  specimen_type: string;
  collection_time: string;
  snomed_code?: string | null;
  description?: string | null;
}

export interface SpecimenUpdatePayload {
  specimen_type: string;
  collection_time: string;
  snomed_code?: string | null;
  description?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class SpecimenService {
  private apiUrl = 'http://localhost:8000/specimen'; 

  constructor(private http: HttpClient) { }

  getSpecimens(): Observable<Specimen[]> {
    return this.http.get<Specimen[]>(`${this.apiUrl}/all`);
  }

  createSpecimen(specimen: SpecimenCreatePayload): Observable<Specimen> {
    return this.http.post<Specimen>(`${this.apiUrl}/create`, specimen);
  }

  updateSpecimen(id: number, specimen: SpecimenUpdatePayload): Observable<Specimen> {
    return this.http.put<Specimen>(`${this.apiUrl}/update/${id}`, specimen);
  }

  deleteSpecimen(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
