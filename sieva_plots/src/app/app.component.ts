import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { environment } from 'src/environments/environment.prod';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Plot Analysis';

  public selectedVal?: string;
  apiURL = environment.apiURL
  matrixPort = environment.matrixPort
  plotsPort = environment.plotsPort
  backPort = environment.backPort

  ngOnInit() {
    this.selectedVal = 'home';
    this.selectedVal = 'plots';
  }

  public myControl = new FormControl('');
  public options: string[] = ['One', 'Two', 'Three'];

}
