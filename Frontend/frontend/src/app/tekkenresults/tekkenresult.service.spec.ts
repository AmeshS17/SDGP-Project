import { TestBed } from '@angular/core/testing';

import { TekkenresultService } from './tekkenresult.service';

describe('TekkenresultService', () => {
  let service: TekkenresultService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TekkenresultService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
