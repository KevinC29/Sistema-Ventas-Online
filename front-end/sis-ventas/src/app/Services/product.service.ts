import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.prod';
import { ResponseApi } from '../interfaces/response-api';
import { Product } from '../interfaces/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  private url: string = environment.url_api+'/product';

  constructor(private http:HttpClient) {}

  list(): Observable<ResponseApi> {
    return this.http.get<ResponseApi>(`${this.url}/list/`);
  }

  create(request: Product): Observable<ResponseApi> {
    return this.http.post<ResponseApi>(`${this.url}/add/`, request);
  }

  update(id: string, request: Product): Observable<ResponseApi> {
    return this.http.put<ResponseApi>(`${this.url}/update/${id}/`, request);
  }

  delete(id: string): Observable<ResponseApi> {
    return this.http.delete<ResponseApi>(`${this.url}/delete/${id}/`);
  }

}
