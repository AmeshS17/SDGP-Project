import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-uploadpage',
  templateUrl: './uploadpage.component.html',
  styleUrls: ['./uploadpage.component.css']
})
export class UploadpageComponent implements OnInit {

  uploadurl : string = 'null';
    filekey : string = 'null';

    url_response : url[];

  constructor( private UploadpageService : UploadpageService ) { }

  ngOnInit() {

    this.getUploadUrl();

    getUploadUrl(): void{
      this.UploadpageService.getUploadUrl().subscribe(
        data =>{
          this.
        }

      )
    }


  }

}


