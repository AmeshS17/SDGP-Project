import { TestBed } from '@angular/core/testing';

import { UploadpageService } from './uploadpage.service';

describe('UploadpageService', () => {
  let service: UploadpageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UploadpageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
