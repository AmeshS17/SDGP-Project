import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { API_URL } from '../api_url';

@Injectable({
  providedIn: 'root'
})

@Injectable({
  providedIn :'root'

})
export class ConfigService {
  
}
export class UploadpageService {

  private baseurl = API_URL + '/upload-url';

  constructor(private http: HttpClient) { }

  getUploadUrl() : Observable<uploadUrl[]>{
    return this.http.get<GetResponse>(this.baseurl).pipe(
      map(response => response.uploadUrl)
    );

  }
}


