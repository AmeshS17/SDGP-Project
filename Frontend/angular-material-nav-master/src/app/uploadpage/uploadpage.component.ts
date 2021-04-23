import { Component, OnInit } from '@angular/core';
import {UploadpageService} from './uploadpage.service';
import {url_response} from './uploadpage.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-uploadpage',
  templateUrl: './uploadpage.component.html',
  styleUrls: ['./uploadpage.component.scss']
})
export class UploadpageComponent implements OnInit {

  title: string = '';
  id: number = 0;
  desc: string = '';
  uploadurl : string = '';
  filekey : string = '';
  url_response : url_response = {uploadurl : '' , filekey : ''};
  fileToUpload: File;
  warning: string = ''
  validSubmission: boolean = false;
  warningColor: string = 'red'

  constructor( private UploadService : UploadpageService, 
                private router: Router) { }

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
  }

  uploadFileToActivity() {
    this.validateSubmission();

    if(this.validSubmission){
      this.warningColor = 'green';
      this.warning = 'Uploading';
      this.UploadService.uploadFile(this.fileToUpload,this.uploadurl).subscribe(
        (data: boolean) => {
          
          console.log(data);
          if (data){
            this.router.navigateByUrl('/resultspage', {
              state:{
                data:{
                  title: this.title,
                  desc: this.desc,
                  filekey: this.filekey,
                  id: this.id
                }
              }
            })
          }else{
            console.log(data)
          }
        }, error => {
          console.log(error);
          this.warningColor = 'red';
          this.warning = 'Upload failed. Please refresh the page'
        });
    }
  }

  importFile(event: Event) {

    if ((<HTMLInputElement>event.target).files.length == 0) {
       console.log("No file selected!");
       return
    }
      let file: File = (<HTMLInputElement>event.target).files[0];
      this.fileToUpload = file;
      console.log(this.fileToUpload)
    }

    setTitle(event: Event){
      if((<HTMLInputElement>event.target).value == ''){
        console.log("Game Name is empty")
        return
      }
      let title: string = (<HTMLInputElement>event.target).value;
      this.title = title;
      console.log(this.title);
    }

    setDesc(event: Event){
      if((<HTMLInputElement>event.target).value == ''){
        console.log("Game Description is empty")
        return
      }
      let desc: string = (<HTMLInputElement>event.target).value;
      this.desc = desc;
      console.log(this.desc);
    }

    validateSubmission(){
      if (this.title == ''){
        this.warning = 'Game name cannot be empty';
        this.validSubmission = false;
        return
      }
      if (this.desc == ''){
        this.warning = 'Game description cannot be empty';
        this.validSubmission = false;
        return
      }
      if(this.fileToUpload == undefined){
        this.warning = 'Please select a csv file';
        return
      }
      if(this.fileToUpload.name.split('.').pop() != 'csv'){
        this.warning = 'Invalid File! Please select a csv file';
        return
      }
      if(this.fileToUpload.size > 2293760){
        this.warning = 'File is too large'
        return
      }
      if(this.filekey == ''){
        this.warning = 'Unknown error occured, Please refresh and try again.'
        return
      }
      if(this.uploadurl == ''){
        this.warning = 'Unknown error occured, Please refresh and try again.'
        return
      }
      this.warning = '';
      this.validSubmission = true;
    }

}