import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HovermeComponent } from './hoverme.component';

describe('HovermeComponent', () => {
  let component: HovermeComponent;
  let fixture: ComponentFixture<HovermeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HovermeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HovermeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
