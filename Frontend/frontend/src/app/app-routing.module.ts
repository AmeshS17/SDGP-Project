import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GamelibraryComponent } from './gamelibrary/gamelibrary.component';
import { HomepageComponent } from './homepage/homepage.component';
import { HovermeComponent } from './hoverme/hoverme.component';
import { TekkenresultsComponent } from './tekkenresults/tekkenresults.component';
import { UploadpageComponent } from './uploadpage/uploadpage.component';

const routes: Routes = [
  {path : '' , component : HovermeComponent},
  {path : 'homepage' , component : HomepageComponent},
  {path : 'uploadpage' , component : UploadpageComponent },
  {path : 'game library' , component : GamelibraryComponent },
  {path : 'tekkenresults' , component : TekkenresultsComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
