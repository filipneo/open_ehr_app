import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { PatientListComponent } from './pages/patient-list/patient-list.component';
import { BodyMeasurementListComponent } from './pages/body-measurement-list/body-measurement-list.component';
import { CompositionListComponent } from './pages/composition-list/composition-list.component';
import { LabAnalyteListComponent } from './pages/lab-analyte-list/lab-analyte-list.component';
import { LabTestListComponent } from './pages/lab-test-list/lab-test-list.component';
import { ReferenceRangeListComponent } from './pages/reference-range-list/reference-range-list.component';
import { SpecimenListComponent } from './pages/specimen-list/specimen-list.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'patients', component: PatientListComponent },
    { path: 'body-measurements', component: BodyMeasurementListComponent },
    { path: 'compositions', component: CompositionListComponent },
    { path: 'lab-analytes', component: LabAnalyteListComponent },
    { path: 'lab-tests', component: LabTestListComponent },
    { path: 'reference-ranges', component: ReferenceRangeListComponent },
    { path: 'specimens', component: SpecimenListComponent }
];
