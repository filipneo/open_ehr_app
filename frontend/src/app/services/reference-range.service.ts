import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ReferenceRange {
  loinc_code: string;
  low?: number;
  high?: number;
  unit?: string;
  version?: number;
}

export interface ReferenceRangeCreatePayload {
  loinc_code: string;
  low?: number;
  high?: number;
  unit?: string;
}

export interface ReferenceRangeUpdatePayload {
  low?: number;
  high?: number;
  unit?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReferenceRangeService {
  private apiUrl = 'http://localhost:8000/reference_ranges';

  constructor(private http: HttpClient) { }

  getReferenceRanges(): Observable<ReferenceRange[]> {
    return this.http.get<ReferenceRange[]>(this.apiUrl);
  }

  createReferenceRange(range: ReferenceRangeCreatePayload): Observable<ReferenceRange> {
    return this.http.post<ReferenceRange>(this.apiUrl, range);
  }

  updateReferenceRange(loinc_code: string, range: ReferenceRangeUpdatePayload): Observable<ReferenceRange> {
    return this.http.put<ReferenceRange>(`${this.apiUrl}/${loinc_code}`, range);
  }

  deleteReferenceRange(loinc_code: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${loinc_code}`);
  }
}
