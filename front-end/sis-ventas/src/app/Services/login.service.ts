import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.prod';
import { ResponseApi } from '../interfaces/response-api';
import { Login } from '../interfaces/login';


@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private url: string = environment.url_api;

  constructor(private http:HttpClient) { }

  login(request: Login): Observable<ResponseApi> {
    return this.http.post<ResponseApi>(`${this.url}/login`, request);
  }
  logout(): Observable<ResponseApi> {
    return this.http.get<ResponseApi>(`${this.url}/logout`);
  }

}
