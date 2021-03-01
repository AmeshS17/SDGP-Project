import {Component, OnInit} from '@angular/core';
import {Game} from '../../classes/game';
import {GameService} from '../../services/game-service.service';

@Component({
  selector: 'app-game-page',
  templateUrl: './game-page.component.html',
  styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {
  games: Game[];

  constructor(private gameService: GameService) {
  }

  ngOnInit(): void {
    this.getGameInfo();
  }


  getGameInfo(): void {
    this.gameService.getGame().subscribe(
      data => {
        this.games = data;
      }
    );
  }


}
