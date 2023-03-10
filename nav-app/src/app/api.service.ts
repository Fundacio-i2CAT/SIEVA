import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.prod';
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiURL = environment.apiURL
  matrixPort = environment.matrixPort
  plotsPort = environment.plotsPort
  backPort = environment.backPort

  url = this.apiURL + ':' + this.backPort


  constructor(private httpClient: HttpClient) { }

  getDataDummy() {
    return this.httpClient.get(this.url + "/dummy")
  }

  saveConfigBackend(data: any) {
    return this.httpClient.post(this.url + '/uploadConfig', data, {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    })
  }
}