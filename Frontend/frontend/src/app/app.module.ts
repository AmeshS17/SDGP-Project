import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {OwlModule} from 'ngx-owl-carousel';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TekkenresultsComponent } from './tekkenresults/tekkenresults.component';
import { UploadpageComponent } from './uploadpage/uploadpage.component';
import { RegisterpageComponent } from './registerpage/registerpage.component';
import { GamelibraryComponent } from './gamelibrary/gamelibrary.component';
import { HomepageComponent } from './homepage/homepage.component';

@NgModule({
  declarations: [
    AppComponent,
    TekkenresultsComponent,
    UploadpageComponent,
    RegisterpageComponent,
    GamelibraryComponent,
    HomepageComponent
  ],
  imports: [
    BrowserModule,
    OwlModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
