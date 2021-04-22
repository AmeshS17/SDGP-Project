import { HttpResponse } from '@angular/common/http';
import { templateJitUrl } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { game } from './gamelibrary.model';
import { GamelibraryService } from './gamelibrary.service';

@Component({
  selector: 'app-gamelibrary',
  templateUrl: './gamelibrary.component.html',
  styleUrls: ['./gamelibrary.component.scss']
})
export class GamelibraryComponent implements OnInit {

  games: game[] = [];
  selectedGame: game; 

  constructor(private GamelibraryService: GamelibraryService,
              private router: Router) { }

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
        if(data.status == 200){
          this.router.navigateByUrl('/resultspage', {
            state:{
              data:{
                title: this.selectedGame.title,
                desc: this.selectedGame.desc,
                filekey: this.selectedGame.filekey,
                id: this.selectedGame.id
              }
            }
          })
        }
      }
    );
  }

  selectGame(game: game){
    if(this.selectedGame == undefined){
      this.selectedGame = game;
      console.log(this.selectedGame)
      this.triggerModel(this.selectedGame.filekey);
    }
  }
}
