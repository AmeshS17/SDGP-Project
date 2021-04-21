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

  id: number = 1;
  title: string = 'test title';
  desc: string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc convallis, nulla eget interdum euismod, velit ante bibendum lectus, ac ullamcorper quam erat sit amet orci. Duis facilisis, est non maximus ultrices, velit leo efficitur erat, id lobortis turpis tortor eget mi. Aenean id convallis dolor. Curabitur et purus ut nisi luctus auctor sit amet non nisi. Morbi placerat eget risus at volutpat. Aliquam mattis ultrices odio tempor lacinia. Suspendisse convallis velit sit amet imperdiet tempor. Praesent venenatis dignissim massa, at posuere urna commodo a. Curabitur in efficitur nisl. Nam vitae egestas diam, at dignissim lacus. Nunc suscipit velit vel accumsan pellentesque. Aliquam dolor nisl, congue et tincidunt et, posuere et nulla. Phasellus volutpat orci et molestie egestas. Sed quis rhoncus dolor. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Sed interdum, enim non pellentesque posuere, est risus luctus augue, eget cursus orci magna at lectus. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna. Cras ut lorem sollicitudin, accumsan ex ut, luctus urna.';
  filekey: string = 'testfile.json';
  // imageUrl: string = "url(/assets/images/image "+this.id.toString+".jpg )";
  imageName:string = "image"+this.id.toString()+".jpg";
  imageUrl: string = "url(/assets/images/"+this.imageName+")" ;
  tries: number = 0;
  loaded: boolean = false;
  attempts: number = 0;


  homeSlider={items: 1, dots: true, nav: true};

  constructor(private ResultsService: ResultspageService) { }

  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }

  getResults(){
    this.ResultsService.getResults(this.filekey).subscribe(
      (data: HttpResponse<Results>) => {
        this.attempts++;
        let statuscode = data.status
        if (statuscode == 200 && this.attempts < 5) {
          console.log(data.status)
          let body = {...data.body}
          this.loaded = true;
          this.generateSummaryChart(body);

        }
        else if (statuscode == 204 && this.attempts < 5){
          (async () => {
            console.log('File not found');
            await this.delay(5000);
            this.getResults();
          })();
        }
        console.log(data);
      });
  };

  ngOnInit(){
    Chart.register(...registerables);
    this.getResults();
  }

  generateSummaryChart(data: Results | any){

    let posDataset =[
                      data['Gameplay_Mechanics'][0]*100,
                      data['Network_Performance'][0]*100,
                      data['Content_Value'][0]*100,
                      data['Overall_Experience'][0]*100
                    ]
    let negDataset =[
                      data['Gameplay_Mechanics'][2]*100,
                      data['Network_Performance'][2]*100,
                      data['Content_Value'][2]*100,
                      data['Overall_Experience'][2]*100
                    ]
    let neutralDataset =[
                          data['Gameplay_Mechanics'][1]*100,
                          data['Network_Performance'][1]*100,
                          data['Content_Value'][1]*100,
                          data['Overall_Experience'][1]*100
                        ]

    var summaryChart = new Chart('summary-chart', {
      type: 'bar',
      data: {
        labels:['Gameplay Mechanics','Network Performance','Content/Value','Overall Experience'],
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
            label:'Network Performance',
            data: data['Network_Performance'],
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