import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ReferenceRange {
  loinc_code: string;
  low: number | null;
  high: number | null;
  unit: string | null;
  version: number;
}

export interface ReferenceRangeCreatePayload {
  loinc_code: string;
  low?: number | null;
  high?: number | null;
  unit?: string | null;
}

export interface ReferenceRangeUpdatePayload {
  low?: number | null;
  high?: number | null;
  unit?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class ReferenceRangeService {
  private apiUrl = 'http://localhost:8000/reference_range';

  constructor(private http: HttpClient) { }

  getReferenceRanges(): Observable<ReferenceRange[]> {
    return this.http.get<ReferenceRange[]>(`${this.apiUrl}/all`);
  }

  createReferenceRange(range: ReferenceRangeCreatePayload): Observable<ReferenceRange> {
    return this.http.post<ReferenceRange>(`${this.apiUrl}/create`, range);
  }

  updateReferenceRange(loinc_code: string, range: ReferenceRangeUpdatePayload): Observable<ReferenceRange> {
    return this.http.put<ReferenceRange>(`${this.apiUrl}/update/${loinc_code}`, range);
  }

  deleteReferenceRange(loinc_code: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${loinc_code}`);
  }
}
