import { Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Results} from './resultspage.model';
import {API_URL} from '../../api_url';

@Injectable({
    providedIn:'root'
})
export class ResultspageService {

    private baseurl = API_URL+'/results';

    constructor(private http:HttpClient){}

    getResults(filekey: string): Observable<HttpResponse<Results>>{
        return this.http.get<Results>(this.baseurl,
            {
                params:{
                    filekey: filekey
                },
                observe: 'response'
            });
    }    
}
