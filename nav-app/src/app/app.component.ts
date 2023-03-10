import { Component, ViewChild, HostListener, OnInit } from '@angular/core';
import { TabsComponent } from './tabs/tabs.component';
import { ConfigService } from './config.service';
import * as globals from "./globals";
import { IconsService } from "./icons.service";
import { deleteCookie, getCookie, hasCookie, setCookie } from "./cookies";
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import config from '../assets/config.json';
import matrixConf from '../assets/MatrixConfigurationInitial.json';
import { ApiService } from './api.service';
import { environment } from '../environments/environment.prod';
import { saveAs } from 'file-saver/dist/FileSaver.js';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';

// https://raw.githubusercontent.com/ElasticSA/elsec_dr2an/master/layers/All.json
// https://raw.githubusercontent.com/ElasticSA/elsec_dr2an/master/layers/AWS.json
// https://raw.githubusercontent.com/ElasticSA/elsec_dr2an/master/layers/Azure.json
// https://raw.githubusercontent.com/ElasticSA/elsec_dr2an/master/layers/Cloud.json
// https://raw.githubusercontent.com/ElasticSA/elsec_dr2an/master/layers/GCP.json

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  @ViewChild(TabsComponent) tabsComponent;

  nav_version: string = globals.nav_version;
  links?: string = ''
  actualLoadedJson?: string = ''
  configFinal: object
  apiURL = environment.apiURL
  matrixPort = environment.matrixPort
  plotsPort = environment.plotsPort
  backPort = environment.backPort
  public selectedVal: string;
  public availability: string;
  public missing: string = "#FA9494";
  public partial: string = "#F7F6DC";
  public complete: string = "#59CE8F";

  public newColor = "#fff"
  public user_theme: string;

  @HostListener('window:beforeunload', ['$event'])
  promptNavAway($event) {
    if (!this.configService.getFeature('leave_site_dialog')) return;
    $event.returnValue = 'Are you sure you want to navigate away? Your data may be lost!';
  }

  constructor(public configService: ConfigService, private iconsService: IconsService, private readonly router: Router, private apiService: ApiService, private http: HttpClient) {
    Array.prototype.includes = function (value): boolean {
      for (let i = 0; i < this.length; i++) {
        if (this[i] === value) return true
      }
      return false;
    }
    if (hasCookie("is_user_theme_dark") && getCookie("is_user_theme_dark") === "true") {
      this.user_theme = 'theme-override-dark';
    } else if (getCookie("is_user_theme_dark") === "false") {
      this.user_theme = 'theme-override-light';
    } else {
      this.user_theme = 'theme-use-system';
    }
  }

  ngOnInit() {
    this.iconsService.registerIcons();
    this.selectedVal = 'home';
  }

  /**
   * 
   * @param filtering -> Type of the data wanted by the user. Complete, partial or missing.
   * 
   * This functions makes a request to /get_results on the backend, which returns all the matrix colors for each technique.
   * Once the new config is created, it is sent to saveConfig() function.
   * 
   */

  createConfig(filtering?: string) {

    const headers = new Headers();
    headers.append('Accept', 'text/plain');
    this.http.get(this.apiURL + ':' + this.backPort + '/get_results')
      .subscribe((response: any) => {
        let colors = {
          "#ed4f4f": 0,
          "#ffd966": 50,
          "#8cdd69": 100
        }

        matrixConf['techniques'] = []
        for (const key in response["MITRE"]) {
          switch (filtering) {
            case 'missing':
              if (response["MITRE"][key] == '#ed4f4f') {
                matrixConf['techniques'].push(
                  {
                    "techniqueID": key,
                    "enabled": true,
                    "score": colors[response["MITRE"][key]]
                  }
                )
              }
              this.newColor = "missing"
              break;
            case 'partial':
              if (response["MITRE"][key] == '#ffd966') {
                matrixConf['techniques'].push(
                  {
                    "techniqueID": key,
                    "enabled": true,
                    "score": colors[response["MITRE"][key]]
                  }
                )
              }
              this.newColor = "partial"
              break;
            case 'complete':
              if (response["MITRE"][key] == '#8cdd69') {
                matrixConf['techniques'].push(
                  {
                    "techniqueID": key,
                    "enabled": true,
                    "score": colors[response["MITRE"][key]]
                  }
                )
              }
              this.newColor = "complete"
              break;
            default:

              matrixConf['techniques'].push(
                {
                  "techniqueID": key,
                  "enabled": true,
                  "score": colors[response["MITRE"][key]]
                }
              )
              break;
          }
        }
        this.saveConfig(matrixConf)

      })
    return matrixConf;
  }

  toggleFullClick() {
    this.createConfig()
    window.location.reload()
  }

  /**
   * 
   * @param config -> Final configuration for the Matrix.
   * 
   * This function gets the config and saves it on the backend. This way the front end is able to read this new config once its reloaded.
   * 
   */

  saveConfig(config) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    return this.http.post(this.apiURL + ':' + this.backPort + '/uploadConfig', config, { headers: headers }).subscribe((response: any) => {
    },
      (error: any) => {
        console.log("Error", error)
      })

  }
  selectChanged($event) {
    if ($event.value == 'missing') {
      this.newColor = this.missing;
      this.createConfig($event.value)
      window.location.reload()
    }
    if ($event.value == 'partial') {
      this.newColor = this.partial;
      this.createConfig($event.value)
      window.location.reload()
    }
    if ($event.value == 'complete') {

      this.newColor = this.complete;
      this.createConfig($event.value)
      window.location.reload()
    }
  }
}
