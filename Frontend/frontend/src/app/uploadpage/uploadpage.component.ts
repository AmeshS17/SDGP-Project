import { Component, OnInit } from '@angular/core';
import {UploadpageService} from './uploadpage.service';
import {url_response} from './uploadpage.model';


@Component({
  selector: 'app-uploadpage',
  templateUrl: './uploadpage.component.html',
  styleUrls: ['./uploadpage.component.css']
})
export class UploadpageComponent implements OnInit {

  uploadurl : string = 'null';
    filekey : string = 'null';
  url_response : url_response = {uploadurl : 'null' , filekey : 'null'};

    

  constructor( private UploadService : UploadpageService ) { }
  getUploadUrl(): void{
    this.UploadService.getUploadUrl().subscribe(
      data =>{
        this.url_response = data;
        this.uploadurl = this.url_response['uploadurl'];
        this.filekey = this.url_response['filekey'];

        console.log(data);
      })

  }
    
  

  ngOnInit() {

    this.getUploadUrl();

      

      
    


  }

}


