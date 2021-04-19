import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadpageComponent } from './uploadpage.component';

describe('UploadpageComponent', () => {
  let component: UploadpageComponent;
  let fixture: ComponentFixture<UploadpageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadpageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadpageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
