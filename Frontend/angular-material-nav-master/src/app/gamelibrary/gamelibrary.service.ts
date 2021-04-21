import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { API_URL } from 'src/api_url';
import {game} from './gamelibrary.model'

@Injectable({
  providedIn: 'root'
})
export class GamelibraryService {

  private baseurl = API_URL

  constructor(private http: HttpClient) { }

  getGames(): Observable<game[]>{
    return this.http.get<game[]>(this.baseurl + '/games');
  }

  triggerModel(filekey: string): Observable<HttpResponse<string>>{
    return this.http.get<string>(this.baseurl + '/model',
      {
        params:{
            filekey: filekey
        },
        observe: 'response'
      });
  }
}
