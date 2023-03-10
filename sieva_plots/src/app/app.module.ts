
import { ZingchartAngularModule } from 'zingchart-angular';
import { StackedHorizontalBarPlotComponent } from './stacked-horizontal-bar-plot/stacked-horizontal-bar-plot.component';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatToolbarModule } from '@angular/material/toolbar';



import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { NgxUiLoaderModule, NgxUiLoaderConfig, SPINNER, PB_DIRECTION } from 'ngx-ui-loader';
const ngxUiLoaderConfig: NgxUiLoaderConfig = {
  text: '',
  textColor: '#FFFFFF',
  textPosition: 'center-center',
  pbColor: 'grey',
  bgsColor: 'grey',
  fgsColor: 'grey',
  fgsType: SPINNER.ballScaleMultiple,
  fgsSize: 100,
  pbDirection: PB_DIRECTION.leftToRight,
  pbThickness: 5
}


@NgModule({
  declarations: [
    AppComponent,
    StackedHorizontalBarPlotComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ZingchartAngularModule,
    HttpClientModule,
    NgxUiLoaderModule.forRoot(ngxUiLoaderConfig),
    MatIconModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatFormFieldModule,
    MatToolbarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
