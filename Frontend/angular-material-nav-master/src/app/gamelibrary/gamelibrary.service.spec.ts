import { TestBed } from '@angular/core/testing';

import { GamelibraryService } from './gamelibrary.service';

describe('GamelibraryService', () => {
  let service: GamelibraryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GamelibraryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
