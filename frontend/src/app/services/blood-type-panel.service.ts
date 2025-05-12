import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BloodTypePanel {
  id: number;
  lab_test_id: number;
  abo_id?: number;
  rh_id?: number;
  version?: number;
}

export interface BloodTypePanelCreatePayload {
  lab_test_id: number;
  abo_id?: number;
  rh_id?: number;
}

@Injectable({
  providedIn: 'root'
})
export class BloodTypePanelService {
  private apiUrl = 'http://localhost:8000/blood_type_panels';

  constructor(private http: HttpClient) { }

  getBloodTypePanels(): Observable<BloodTypePanel[]> {
    return this.http.get<BloodTypePanel[]>(this.apiUrl);
  }

  createBloodTypePanel(panel: BloodTypePanelCreatePayload): Observable<BloodTypePanel> {
    return this.http.post<BloodTypePanel>(this.apiUrl, panel);
  }

  updateBloodTypePanel(id: number, panel: BloodTypePanel): Observable<BloodTypePanel> {
    return this.http.put<BloodTypePanel>(`${this.apiUrl}/${id}`, panel);
  }

  deleteBloodTypePanel(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
