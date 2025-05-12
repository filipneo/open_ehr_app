import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Composition {
  id: number;
  patient_id: number;
  start_time: string; // Using string for datetime, will be handled by input type in HTML
  version?: number;
}

export interface CompositionCreatePayload {
  patient_id: number;
  start_time: string; // Using string for datetime
}

@Injectable({
  providedIn: 'root'
})
export class CompositionService {
  private apiUrl = 'http://localhost:8000/compositions'; // Corrected API URL

  constructor(private http: HttpClient) { }

  getCompositions(): Observable<Composition[]> {
    return this.http.get<Composition[]>(this.apiUrl);
  }

  createComposition(composition: CompositionCreatePayload): Observable<Composition> {
    return this.http.post<Composition>(this.apiUrl, composition);
  }

  updateComposition(id: number, composition: Composition): Observable<Composition> {
    return this.http.put<Composition>(`${this.apiUrl}/${id}`, composition);
  }

  deleteComposition(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
