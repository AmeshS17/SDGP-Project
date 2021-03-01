import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Game} from '../classes/game';

@Injectable({
  providedIn: 'root'
})
export class GameService {

  private baseurl = 'http://127.0.0.1:5000/game';


  constructor(private httpClient: HttpClient) {
  }



  getGame(): Observable<Game[]> {
    return this.httpClient.get<GetResponse>(this.baseurl).pipe(
      map(response => response.Game)
    );
  }



}

interface GetResponse {
  Game: Game[];

}

