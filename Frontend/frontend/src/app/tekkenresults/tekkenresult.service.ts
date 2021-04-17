import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Game} from './tekkenresults.model';
import {API_URL} from '../api_url';

@Injectable({
    providedIn:'root'
})
export class GameService {

    private baseurl = API_URL+'/games?id=0';

    constructor(private http:HttpClient){}

    getGame(): Observable<Game[]>{
        return this.http.get<GetResponse>(this.baseurl).pipe(
            map(response => response.Game)
        );
    }    
}

interface GetResponse{
    Game:Game[]
}
