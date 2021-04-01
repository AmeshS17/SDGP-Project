import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamelibraryComponent } from './gamelibrary.component';

describe('GamelibraryComponent', () => {
  let component: GamelibraryComponent;
  let fixture: ComponentFixture<GamelibraryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GamelibraryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GamelibraryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
