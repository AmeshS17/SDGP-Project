import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TekkenresultsComponent } from './tekkenresults.component';

describe('TekkenresultsComponent', () => {
  let component: TekkenresultsComponent;
  let fixture: ComponentFixture<TekkenresultsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TekkenresultsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TekkenresultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
