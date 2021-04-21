import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { APP_BASE_HREF } from '@angular/common';
//
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CustomMaterialModule } from './shared/custom.material.module';
import { FlexLayoutModule } from '@angular/flex-layout';
//
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavigationComponent } from './navigation/navigation.component';
// routed components
import { UploadpageComponent } from './uploadpage/uploadpage.component';
import { GamelibraryComponent } from './gamelibrary/gamelibrary.component';
import { ResultspageComponent } from './resultspage/resultspage.component';
import { MatTabsModule } from '@angular/material/tabs';
import { HttpClientModule } from '@angular/common/http';
import {NgxCSVtoJSONModule} from 'ngx-csvto-json';

@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    UploadpageComponent,
    GamelibraryComponent,
    ResultspageComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CustomMaterialModule,
    FlexLayoutModule,
    MatTabsModule,
    AppRoutingModule,
    NgxCSVtoJSONModule,
    HttpClientModule,
  ],
  providers: [
    {
      provide: APP_BASE_HREF,
      useValue: '/angular-material-nav'
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
