import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CbcPanel {
  id: number;
  lab_test_id: number; // Foreign Key to LabTest
  hemoglobin_id: number | null; // Foreign Key to LabAnalyteResult ID
  white_cell_id: number | null; // Foreign Key to LabAnalyteResult ID
  platelet_id: number | null; // Foreign Key to LabAnalyteResult ID
  version: number;
}

export interface CbcPanelCreatePayload {
  lab_test_id: number;
  hemoglobin_id?: number | null;
  white_cell_id?: number | null;
  platelet_id?: number | null;
}

export interface CbcPanelUpdatePayload {
  lab_test_id: number;
  hemoglobin_id?: number | null;
  white_cell_id?: number | null;
  platelet_id?: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class CbcPanelService {
  private apiUrl = 'http://localhost:8000/cbc_panel';

  constructor(private http: HttpClient) { }

  getCbcPanels(): Observable<CbcPanel[]> {
    return this.http.get<CbcPanel[]>(`${this.apiUrl}/all`);
  }

  getCbcPanel(id: number): Observable<CbcPanel> {
    return this.http.get<CbcPanel>(`${this.apiUrl}/${id}`);
  }

  createCbcPanel(payload: CbcPanelCreatePayload): Observable<CbcPanel> {
    return this.http.post<CbcPanel>(`${this.apiUrl}/create`, payload);
  }

  updateCbcPanel(id: number, payload: CbcPanelUpdatePayload): Observable<CbcPanel> {
    return this.http.put<CbcPanel>(`${this.apiUrl}/update/${id}`, payload);
  }

  deleteCbcPanel(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`);
  }
}
