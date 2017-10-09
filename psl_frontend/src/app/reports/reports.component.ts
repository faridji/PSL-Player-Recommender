import { Component, OnInit } from '@angular/core';
import {Http, Response} from '@angular/http';
@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent implements OnInit {
  mainHeading : String;
  top20_Batsman : Object;
  top20_WicketTaker: Object;
  bestEconomy_players : Object;
  top20_StrikeRaters : Object;
  top20_MostFifties : Object;
  top20_MostSixes : Object;

  constructor(private http: Http) {
    this.mainHeading = "Statian Super League"
    
  this.http.get('http://127.0.0.1:8081/PSL/PSL_Dataset/top_20_batsman').subscribe((res:Response)=>{
  this.top20_Batsman = res.json();
   });
   
   this.http.get('http://127.0.0.1:8081/PSL/PSL_Dataset/top_20_WicketTakers').subscribe((res:Response)=>{
    this.top20_WicketTaker = res.json();
   });

   this.http.get('http://127.0.0.1:8081/PSL/PSL_Dataset/top_20_EconomicalPlayers').subscribe((res:Response)=>{
    this.bestEconomy_players = res.json();
   });
  
  this.http.get('http://127.0.0.1:8081/PSL/PSL_Dataset/top_20_StrikeRaters').subscribe((res:Response)=>{
    this.top20_StrikeRaters = res.json();
     });
     
     this.http.get('http://127.0.0.1:8081/PSL/PSL_Dataset/top_20_MostFifties').subscribe((res:Response)=>{
      this.top20_MostFifties = res.json();
     });
  
     this.http.get('http://127.0.0.1:8081/PSL/PSL_Dataset/top_20_MostSixes').subscribe((res:Response)=>{
      this.top20_MostSixes = res.json();
     });

    }

  ngOnInit() {
  }

}
