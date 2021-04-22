import { HttpResponse } from '@angular/common/http';
import { templateJitUrl } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { game } from './gamelibrary.model';
import { GamelibraryService } from './gamelibrary.service';

@Component({
  selector: 'app-gamelibrary',
  templateUrl: './gamelibrary.component.html',
  styleUrls: ['./gamelibrary.component.scss']
})
export class GamelibraryComponent implements OnInit {

  games = [];

  constructor(private GamelibraryService: GamelibraryService) { }

  ngOnInit(): void {
    this.getGames();
  }

  getGames(){
    this.GamelibraryService.getGames().subscribe(
      (data: game[]) => {
        let tempgames = data;
        tempgames = tempgames.filter(function(obj){
          return obj.id !== 0;
        })
        console.log(tempgames)
        this.games = tempgames
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
