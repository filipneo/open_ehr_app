import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Specimen {
  id: number;
  specimen_type: string;
  collection_time: string; // Using string for datetime, will be handled by input type in HTML
  snomed_code?: string;
  description?: string;
  version?: number;
}

export interface SpecimenCreatePayload {
  specimen_type: string;
  collection_time: string;
  snomed_code?: string;
  description?: string;
}

export interface SpecimenUpdatePayload {
  specimen_type: string;
  collection_time: string;
  snomed_code?: string;
  description?: string;
}

@Injectable({
  providedIn: 'root'
})
export class SpecimenService {
  private apiUrl = 'http://localhost:8000/specimens'; 

  constructor(private http: HttpClient) { }

  getSpecimens(): Observable<Specimen[]> {
    return this.http.get<Specimen[]>(this.apiUrl);
  }

  createSpecimen(specimen: SpecimenCreatePayload): Observable<Specimen> {
    return this.http.post<Specimen>(this.apiUrl, specimen);
  }

  updateSpecimen(id: number, specimen: SpecimenUpdatePayload): Observable<Specimen> {
    return this.http.put<Specimen>(`${this.apiUrl}/${id}`, specimen);
  }

  deleteSpecimen(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
