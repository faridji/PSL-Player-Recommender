import { Component, OnInit } from '@angular/core';
import { Router,ActivatedRoute} from '@angular/router';
import {Http, Response} from '@angular/http';


@Component({
  selector: 'app-player-profile',
  templateUrl: './player-profile.component.html',
  styleUrls: ['./player-profile.component.css']
})
export class PlayerProfileComponent implements OnInit {
  options : Object;
  data : Object;
  playerName : String;
  constructor(private router: Router,private route: ActivatedRoute, private http:Http) {
    
   }

  ngOnInit() {
  
    this.route
    .queryParams
    .subscribe(params => {

      // Defaults to 0 if no query param provided.
      this.playerName = params['result'];
      this.options = {
        playerName : this.playerName
      }
      this.http.post('http://127.0.0.1:8081/PSL/T20Dataset/player',this.options)
      .subscribe((res:Response)=>{
        this.data = res.json();
        console.log(this.data)
      });
    });
  }



}
