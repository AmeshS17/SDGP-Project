import { NgModule } from '@angular/core';
import { Routes, RouterModule, ExtraOptions } from '@angular/router';
//
import { HomeComponent } from './home/home.component';
import { UploadpageComponent } from  './uploadpage/uploadpage.component';
import { GamelibraryComponent} from './gamelibrary/gamelibrary.component';
import { ResultspageComponent} from './resultspage/resultspage.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent, data: { label: 'Home' } },
  { path: 'uploadpage', component:UploadpageComponent, data: {label: 'Upload'}},
  { path: 'gamelibrary', component:GamelibraryComponent, data: {label: 'Game Library'}},
  { path: 'resultspage', component:ResultspageComponent, data: {label: 'Results Page'}},
  { path: '', redirectTo: 'home', pathMatch: 'full' },
];

const routeOptions: ExtraOptions = {
  enableTracing: true
};

@NgModule({
  imports: [RouterModule.forRoot(routes, routeOptions)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
