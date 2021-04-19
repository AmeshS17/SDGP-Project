import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultspageComponent } from './resultspage.component';

describe('ResultspageComponent', () => {
  let component: ResultspageComponent;
  let fixture: ComponentFixture<ResultspageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ResultspageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ResultspageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
