import { TestBed } from '@angular/core/testing';

import { ResultspageService } from './resultspage.service';

describe('ResultspageService', () => {
  let service: ResultspageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ResultspageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
