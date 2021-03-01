import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {GamePageComponent} from './components/game-page/game-page.component';

const routes: Routes = [
  { path: 'game', component: GamePageComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
