import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import {ResultspageService} from './resultspage.service';
import {Results} from './resultspage.model';

@Component({
  selector: 'app-resultspage',
  templateUrl: './resultspage.component.html',
  styleUrls: ['./resultspage.component.scss']
})
export class ResultspageComponent implements OnInit {

  id: number = 0;
  title: string = '';
  desc: string = '';
  filekey: string = '';
  imageName:string = "image"+this.id.toString()+".jpg";
  imageUrl: string = "url(/assets/images/"+this.imageName+")";
  tries: number = 0;
  loaded: boolean = false;
  attempts: number = 0;

  constructor(private ResultsService: ResultspageService) { }

  ngOnInit(){
    Chart.register(...registerables);

    let stateData = window.history.state.data;
    this.title = stateData.title;
    this.id = stateData.id;
    this.desc = stateData.desc;
    this.filekey = stateData.filekey;
    this.imageName = "image"+this.id.toString()+".jpg";
    this.imageUrl = "url(/assets/images/"+this.imageName+")";

    this.getResults();
  }

  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }

  getResults(){
    this.ResultsService.getResults(this.filekey).subscribe(
      (data: HttpResponse<Results>) => {
        this.attempts++;
        let statuscode = data.status
        if(this.attempts < 30){
          if (statuscode == 200) {
            console.log('Summary received on attempt - ' + this.attempts);
            console.log(data.status);
            let body = {...data.body}
            this.loaded = true;
            this.generateSummaryChart(body);
          }
          else if (statuscode == 204 ){
            (async () => {
              console.log('File not found');
              await this.delay(10000);
              this.getResults();
            })();
          }
        }
        if(this.attempts >= 30){
          console.log('Maximum Attempts reached');
        }
        console.log(data);
      });
  };


  generateSummaryChart(data: Results | any){
    let posDataset =[
                      data['Gameplay_Mechanics'][0]*100,
                      data['Performance'][0]*100,
                      data['Content_Value'][0]*100,
                      data['Overall_Experience'][0]*100
                    ]
    let negDataset =[
                      data['Gameplay_Mechanics'][2]*100,
                      data['Performance'][2]*100,
                      data['Content_Value'][2]*100,
                      data['Overall_Experience'][2]*100
                    ]
    let neutralDataset =[
                          data['Gameplay_Mechanics'][1]*100,
                          data['Performance'][1]*100,
                          data['Content_Value'][1]*100,
                          data['Overall_Experience'][1]*100
                        ]

    var summaryChart = new Chart('summary-chart', {
      type: 'bar',
      data: {
        labels:['Gameplay Mechanics','Performance','Content/Value','Overall Experience'],
        datasets:[
          {
            label:'Positive',
            data: posDataset,
            backgroundColor: 'blue',
            borderColor: 'blue'
          },
          {
            label:'Neutral',
            data: neutralDataset,
            backgroundColor: 'yellow',
            borderColor: 'yellow'
          },
          {
            label: 'Negative',
            data: negDataset,
            backgroundColor: 'red',
            borderColor:'red'
          }
        ]
      },
      options: {
        indexAxis: 'y',
        elements: {
          bar:{
            borderWidth: 2
          }
        },
        responsive: true,
        plugins: {
          legend: {
            position: 'right',
          }
        }
      }
    });

    var gameplayChart = new Chart('gameplay-chart', {
      type: 'pie',
      data: {
        labels:['Positive','Neutral','Negative'],
        datasets:[
          {
            label:'Gameplay Mechanics',
            data: data['Gameplay_Mechanics'],
            backgroundColor: ['blue','yellow','red']
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });

    var networkChart = new Chart('network-chart', {
      type: 'pie',
      data: {
        labels:['Positive','Neutral','Negative'],
        datasets:[
          {
            label:'Performance',
            data: data['Performance'],
            backgroundColor: ['blue','yellow','red']
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });

    var contentChart = new Chart('content-chart', {
      type: 'pie',
      data: {
        labels:['Positive','Neutral','Negative'],
        datasets:[
          {
            label:'Content/Value',
            data: data['Content_Value'],
            backgroundColor: ['blue','yellow','red']
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });

    var overallChart = new Chart('overall-chart', {
      type: 'pie',
      data: {
        labels:['Positive','Neutral','Negative'],
        datasets:[
          {
            label:'Overall Experience',
            data: data['Overall_Experience'],
            backgroundColor: ['blue','yellow','red']
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });
  }
}