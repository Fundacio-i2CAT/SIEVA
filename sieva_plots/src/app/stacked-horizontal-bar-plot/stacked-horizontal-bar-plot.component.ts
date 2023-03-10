import { Component, HostListener, OnInit } from '@angular/core';
import "zingchart/modules-es6/zingchart-maps.min.js";
import "zingchart/modules-es6/zingchart-maps-usa.min.js";
import { NgxUiLoaderService } from 'ngx-ui-loader';
import { DataService } from '../data.service';
import config from '../../assets/config.json';

@Component({
  selector: 'app-stacked-horizontal-bar-plot',
  templateUrl: './stacked-horizontal-bar-plot.component.html',
  styleUrls: ['./stacked-horizontal-bar-plot.component.scss']
})
export class StackedHorizontalBarPlotComponent implements OnInit {

  constructor(private ngxService: NgxUiLoaderService, private dataService: DataService) { }

  series: any = []

  initialBottom: any = "-200px"
  height: any = "0px"
  clicked: boolean = false
  graph_data_json: any = ""
  graph_data: any = ""
  index_title: any = ""
  logEntities: any = []
  arr_configs_aux: any = []
  arr_configs_final: any = []

  config: any = config

  ESCAPE_KEYCODE = 27;

  @HostListener('document:keydown', ['$event']) onKeydownHandler(event: KeyboardEvent) {
    if (event.keyCode === this.ESCAPE_KEYCODE) {
      this.clicked = false
    }
  }


  ngOnInit(): void {
    this.createConfigsArray__final()
  }


  /**
   * @param event 
   * @param config
   * 
   * This function get the data on the table format once one of the plots is clicked.
   *  
   */

  getdata(event: any, config: any) {

    this.initialBottom = "50px"
    this.clicked = !this.clicked
    this.graph_data = ""
    this.graph_data_json = ""
    this.index_title = ""


    this.logEntities.forEach((element: any) => {
      if (element[config['scaleX']['values'][0]] !== undefined) {
        this.graph_data_json = element[config['scaleX']['values'][0]]
        this.index_title = Object.keys(element)[0];

      }

    });
    this.graph_data = '<p class="index_title">' + this.index_title + '</p>';

    for (const key in this.graph_data_json) {
      if (this.graph_data_json[key].length != 0) {
        this.graph_data = this.graph_data + '<h3 class="entity">' + key + '</h3><p class="entity__data">' + this.graph_data_json[key].toString().replace(/,/g, ', ') + '</p>'
      } else {
        this.graph_data = this.graph_data + '<h3 class="entity">' + key + '</h3><p class="entity__data">No Data</p>'
      }
    }

  }

  /**
   * 
   * This functions gets the data from the /predict endpoint and modifies the "series" key on the /src/assets/config files. Which is the key zingcharts needs to read to show the values.
   * 
   */

  createConfigsArray__final() {

    this.ngxService.start()
    this.dataService.getDataPredict().subscribe((response: any) => {
      this.ngxService.stop()
      let arr_series_final: any = []
      let arr_indexes: any = []

      for (const key in response) {
        let arr_obj_aux = []
        let cont = 0

        if (key != "MITRE") {
          if (key != "log-entities") {
            arr_indexes.push(key)
            for (const tecnique in response[key]["Category Split: Data types"]) {

              arr_obj_aux.push({ "text": tecnique, values: [parseFloat(response[key]["Category Split: Data types"][tecnique])], "backgroundColor": "" })
              cont += 1
            }
            arr_series_final.push(arr_obj_aux)
          }
        }
      }

      arr_series_final.forEach((element: any) => {
        let toPush: any = Object.assign({}, this.config)
        toPush['series'] = element
        this.arr_configs_aux.push(toPush)
      });

      let cont = 0
      this.arr_configs_aux.forEach((element: any) => {
        let obj: any = Object.assign({}, element)
        let toPush: any = Object.assign({}, element['scaleX'])

        toPush['values'] = [arr_indexes[cont]]
        obj['scaleX'] = toPush

        if (response['log-entities'][cont] != undefined) {
          this.logEntities.push({
            [obj['scaleX']['values'][0]]: response['log-entities'][cont][obj['scaleX']['values'][0]]
          })
        }
        this.arr_configs_final.push(obj)
        cont += 1
      });

    })


  }


}
