import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.prod';
@Injectable({
  providedIn: 'root'
})
export class DataService {

  url = environment.apiURL + ':' + environment.backPort

  constructor(private httpClient: HttpClient) { }

  getDataPredict() {
    return this.httpClient.get(this.url + "/predict")
  }


}