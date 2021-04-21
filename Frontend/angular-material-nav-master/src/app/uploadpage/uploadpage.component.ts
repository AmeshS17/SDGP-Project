import { Component, OnInit } from '@angular/core';
import {UploadpageService} from './uploadpage.service';
import {url_response} from './uploadpage.model';

@Component({
  selector: 'app-uploadpage',
  templateUrl: './uploadpage.component.html',
  styleUrls: ['./uploadpage.component.scss']
})
export class UploadpageComponent implements OnInit {

  uploadurl : string = 'null';
  filekey : string = 'null';
  url_response : url_response = {uploadurl : 'null' , filekey : 'null'};
  fileToUpload: File;

  constructor( private UploadService : UploadpageService ) { }

  getUploadUrl(): void{
    this.UploadService.getUploadUrl().subscribe(
      data =>{
        this.url_response = data;
        this.uploadurl = this.url_response['uploadurl'];
        this.filekey = this.url_response['filekey'];
        console.log("Upload url - " + this.uploadurl);
        console.log("Filekey - " + this.filekey);
        

      },
      error=>{
        console.log(error);
      })
  }


ngOnInit() {

    this.getUploadUrl();
    console.log(this.fileToUpload)
  }

  uploadFileToActivity() {
    if(this.fileToUpload == undefined){
      console.log("No file selected!");
       return
    }
    this.UploadService.uploadFile(this.fileToUpload,this.uploadurl).subscribe(data => {
      // do something, if upload success
      }, error => {
        console.log(error);
      });
  }

  importFile(event: Event) {

    if ((<HTMLInputElement>event.target).files.length == 0) {
       console.log("No file selected!");
       return
    }
      let file: File = (<HTMLInputElement>event.target).files[0];
      this.fileToUpload = file;
      // after here 'file' can be accessed and used for further process
    }

    

}