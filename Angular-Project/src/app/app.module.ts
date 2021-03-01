import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { GamePageComponent } from './components/game-page/game-page.component';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule} from '@angular/router';

@NgModule({
  declarations: [
    AppComponent,
    GamePageComponent
  ],
  imports: [
    BrowserModule, HttpClientModule, RouterModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
