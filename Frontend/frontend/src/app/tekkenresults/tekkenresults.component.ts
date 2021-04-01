import { Component, OnInit } from '@angular/core';
import { Chart } from "chart.js";

@Component({
  selector: 'app-tekkenresults',
  templateUrl: './tekkenresults.component.html',
  styleUrls: ['./tekkenresults.component.css']
})
export class TekkenresultsComponent implements OnInit {

  homeSlider={items: 1, dots: true, nav: true};

  constructor() { }

  ngOnInit(){
    var myChart1 = new Chart('myChart1', {
      type: 'line',
      data: {
        labels:['a','b','c','d','e','f','g','h'],
        datasets:[
          {
            label:'My First Dataset',
            data: [1,3,5,10,56,65,35,543,543,543],
            backgroundColor: 'red',
            borderColor: 'red',
            fill: false,
          },
          {
            label: 'My Second Dataset',
            data: [1,3,5,10,56,65,35,543,543,543].reverse(),
            backgroundColor: 'blue',
            borderColor:'blue',
            fill: false
          }
        ]
      }
      })

      var myChart2 = new Chart('myChart2', {
        type: 'line',
        data: {
          labels:['a','b','c','d','e','f','g','h'],
          datasets:[
            {
              label:'My First Dataset',
              data: [1,3,5,10,56,65,35,543,543,543],
              backgroundColor: 'red',
              borderColor: 'red',
              fill: false,
            },
            {
              label: 'My Second Dataset',
              data: [1,3,5,10,56,65,35,543,543,543].reverse(),
              backgroundColor: 'blue',
              borderColor:'blue',
              fill: false
            }
          ]
        }
        })

        var myChart3 = new Chart('myChart3', {
          type: 'line',
          data: {
            labels:['a','b','c','d','e','f','g','h'],
            datasets:[
              {
                label:'My First Dataset',
                data: [1,3,5,10,56,65,35,543,543,543],
                backgroundColor: 'red',
                borderColor: 'red',
                fill: false,
              },
              {
                label: 'My Second Dataset',
                data: [1,3,5,10,56,65,35,543,543,543].reverse(),
                backgroundColor: 'blue',
                borderColor:'blue',
                fill: false
              }
            ]
          }
          })

          var myChart4 = new Chart('myChart4', {
            type: 'line',
            data: {
              labels:['a','b','c','d','e','f','g','h'],
              datasets:[
                {
                  label:'My First Dataset',
                  data: [1,3,5,10,56,65,35,543,543,543],
                  backgroundColor: 'red',
                  borderColor: 'red',
                  fill: false,
                },
                {
                  label: 'My Second Dataset',
                  data: [1,3,5,10,56,65,35,543,543,543].reverse(),
                  backgroundColor: 'blue',
                  borderColor:'blue',
                  fill: false
                }
              ]
            }
            })

            var myChart5 = new Chart('myChart5', {
              type: 'line',
              data: {
                labels:['a','b','c','d','e','f','g','h'],
                datasets:[
                  {
                    label:'My First Dataset',
                    data: [1,3,5,10,56,65,35,543,543,543],
                    backgroundColor: 'red',
                    borderColor: 'red',
                    fill: false,
                  },
                  {
                    label: 'My Second Dataset',
                    data: [1,3,5,10,56,65,35,543,543,543].reverse(),
                    backgroundColor: 'blue',
                    borderColor:'blue',
                    fill: false
                  }
                ]
              }
              })

              var myChart6 = new Chart('myChart6', {
                type: 'line',
                data: {
                  labels:['a','b','c','d','e','f','g','h'],
                  datasets:[
                    {
                      label:'My First Dataset',
                      data: [1,3,5,10,56,65,35,543,543,543],
                      backgroundColor: 'red',
                      borderColor: 'red',
                      fill: false,
                    },
                    {
                      label: 'My Second Dataset',
                      data: [1,3,5,10,56,65,35,543,543,543].reverse(),
                      backgroundColor: 'blue',
                      borderColor:'blue',
                      fill: false
                    }
                  ]
                }
                })

                var myChart7 = new Chart('myChart7', {
                type: 'doughnut',
                options: {
                  responsive: true,
                  title: {
                    display: true,
                    text: 'Doughnute Chart'
                  }, legend: {
                    position: 'top',
                  }, animation: {
                    animateScale: true,
                    animateRotate: true
                  }
                  },
                  data: {
                    datasets:[{
                      data:[45,10,5,25,15],
                      backgroundColor: ['red','orange','yellow','green','blue'],
                      label: 'Dataset 1'
                    }],
                    labels: ['Red', 'Orange', 'Yellow','Green','Blue']
                  }
                })

                var myChart8 = new Chart('myChart8', {
                  type: 'doughnut',
                  options: {
                    responsive: true,
                    title: {
                      display: true,
                      text: 'Doughnute Chart'
                    }, legend: {
                      position: 'top',
                    }, animation: {
                      animateScale: true,
                      animateRotate: true
                    }
                    },
                    data: {
                      datasets:[{
                        data:[45,10,5,25,15],
                        backgroundColor: ['red','orange','yellow','green','blue'],
                        label: 'Dataset 1'
                      }],
                      labels: ['Red', 'Orange', 'Yellow','Green','Blue']
                    }
                  })
                }
              }
