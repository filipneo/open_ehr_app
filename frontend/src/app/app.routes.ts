import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { PatientListComponent } from './pages/patient-list/patient-list.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'patients', component: PatientListComponent }
];
