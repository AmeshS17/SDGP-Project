import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-uploadpage',
  templateUrl: './uploadpage.component.html',
  styleUrls: ['./uploadpage.component.scss']
})
export class UploadpageComponent implements OnInit {

  constructor() { }

  convertedObj:any = "";
  
  convert(objArray) {
    console.log(objArray);
    this.convertedObj = JSON.stringify(objArray, null, 2);
  }
  
  onError(err) {
    this.convertedObj = err
    console.log(err);
  }


  ngOnInit(): void {
  }   

}
