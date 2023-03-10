import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StackedHorizontalBarPlotComponent } from './stacked-horizontal-bar-plot.component';

describe('StackedHorizontalBarPlotComponent', () => {
  let component: StackedHorizontalBarPlotComponent;
  let fixture: ComponentFixture<StackedHorizontalBarPlotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StackedHorizontalBarPlotComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StackedHorizontalBarPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
