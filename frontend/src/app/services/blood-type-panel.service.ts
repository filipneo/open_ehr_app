import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BloodTypePanel {
  id: number;
  lab_test_id: number;
  abo_id: number | null;
  rh_id: number | null;
  version: number;
}

export interface BloodTypePanelCreatePayload {
  lab_test_id: number;
  abo_id?: number | null;
  rh_id?: number | null;
}

export interface BloodTypePanelUpdatePayload {
  lab_test_id: number;
  abo_id?: number | null;
  rh_id?: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class BloodTypePanelService {
  private apiUrl = 'http://localhost:8000/blood_type_panel';

  constructor(private http: HttpClient) { }

  getBloodTypePanels(): Observable<BloodTypePanel[]> {
    return this.http.get<BloodTypePanel[]>(`${this.apiUrl}/all`);
  }

  createBloodTypePanel(panel: BloodTypePanelCreatePayload): Observable<BloodTypePanel> {
    return this.http.post<BloodTypePanel>(`${this.apiUrl}/create`, panel);
  }

  updateBloodTypePanel(id: number, panel: BloodTypePanelUpdatePayload): Observable<BloodTypePanel> {
    return this.http.put<BloodTypePanel>(`${this.apiUrl}/update/${id}`, panel);
  }

  deleteBloodTypePanel(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
