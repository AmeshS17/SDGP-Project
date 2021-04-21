import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { game } from './gamelibrary.model';
import { GamelibraryService } from './gamelibrary.service';

@Component({
  selector: 'app-gamelibrary',
  templateUrl: './gamelibrary.component.html',
  styleUrls: ['./gamelibrary.component.scss']
})
export class GamelibraryComponent implements OnInit {

  constructor(private GamelibraryService: GamelibraryService) { }

  ngOnInit(): void {
    this.getGames();
  }

  getGames(){
    this.GamelibraryService.getGames().subscribe(
      (data: game[]) => {
        console.log(data)
        this.triggerModel("brawlhalla.json");
      }
    )
  }

  triggerModel(filekey: string){
    this.GamelibraryService.triggerModel(filekey).subscribe(
      (data: HttpResponse<string>) =>{
        console.log(data)
        console.log(data.status)
      }
    );
  }
}
