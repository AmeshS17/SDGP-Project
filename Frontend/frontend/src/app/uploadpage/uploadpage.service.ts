import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {url_response} from './uploadpage.model';

import { Observable, throwError } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from '../api_url';

@Injectable({
  providedIn: 'root'
})


export class ConfigService {
  
}
export class UploadpageService {

  private baseurl = API_URL + '/upload-url';

  constructor(private http: HttpClient) { }

  getUploadUrl() : Observable<url_response>{
    return this.http.get<GetResponse>(this.baseurl).pipe(
      map(response => response.url)
    );

  }
}

interface GetResponse{
  url : url_response;
}

