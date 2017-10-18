import { Component, OnInit } from '@angular/core';
import { Router,ActivatedRoute, NavigationEnd} from '@angular/router';
import { Http,Response} from '@angular/http'

@Component({
  selector: 'app-psl-teams',
  templateUrl: './psl-teams.component.html',
  styleUrls: ['./psl-teams.component.css']
})
export class PslTeamsComponent implements OnInit {

  options : Object;
  data : Object;
  teamName : String;
  players : Object;
  loading : Object;
  heading : string;

  info : String = ""
  constructor(private router: Router,private route: ActivatedRoute,private http:Http) { }

  ngOnInit() {
    

    this.route
    .queryParams
    .subscribe(params => {

      // Defaults to 0 if no query param provided.
      this.teamName = params['result'];
      
      if (this.teamName == 'peshawar Zalmi'){
        this.peshawarZalmiTeam();
      }

      if (this.teamName == 'queta Gladiators'){
        this.quetaGladiatorsTeam();
      }

      if (this.teamName == 'islamabad United'){
        this.islamabadUnitedTeam();
      }

      if (this.teamName == 'lahore Qalandars'){
        this.lahoreQalandarsTeam();
      }

      if (this.teamName == 'karachi Kings'){
        this.karachiKingsTeam();
      }

      if (this.teamName == 'multan Sultan'){
        this.multanSultanTeam();
      }
    
    });
  }

  peshawarZalmiTeam() : void{
    this.options = {
      teamName : 'peshawar_zalmi',
    }
    this.loading = true;
    this.http.post('http://127.0.0.1:8081/PSL/Teams/PeshawarZalmi',this.options)
    .subscribe((res:Response)=>{
      
      this.players = res.json();
      this.loading = false;
      this.heading = "Peshawar Zalmi Squad"
    });
  }

  quetaGladiatorsTeam() : void{
    this.options = {
      teamName : 'quetta_gladiators',
    }
    this.loading = true;
    this.http.post('http://127.0.0.1:8081/PSL/Teams/QuetaGladiators',this.options)
    .subscribe((res:Response)=>{
      this.players = res.json();
      this.loading = false;
      this.heading = "Quetta Gladiators Squad"
    });
  }

  islamabadUnitedTeam() : void{
    this.options = {
      teamName : 'islamabad_united',
    }
    this.loading = true;
    this.http.post('http://127.0.0.1:8081/PSL/Teams/IslamabadUnited',this.options)
    .subscribe((res:Response)=>{
      this.players = res.json();
      this.loading = false;
      this.heading = "Islamabad United Squad"
    });
  }

  karachiKingsTeam() : void{
    this.players = ""
    this.options = {
      teamName : 'karachi_kings',
    }
    this.loading = true;
    this.http.post('http://127.0.0.1:8081/PSL/Teams/KarachiKings',this.options)
    .subscribe((res:Response)=>{
      this.players = res.json();
      this.loading = false;
      this.heading = "Karachi Kings Squad"
    });
  }

  lahoreQalandarsTeam() : void{
    this.options = {
      teamName : 'lahore_qalandars',
    }
    this.loading = true;
    this.http.post('http://127.0.0.1:8081/PSL/Teams/LahoreQalandars',this.options)
    .subscribe((res:Response)=>{
      this.players = res.json();
      this.loading = false;
      this.heading = "Lahore Qalandars Squad"
    });
  }

  multanSultanTeam() : void{
   
    
    this.options = {
      teamName : 'multan_sultan',
    }
    this.loading = true;
    this.http.post('http://127.0.0.1:8081/PSL/Teams/MultanSultan',this.options)
    .subscribe((res:Response)=>{
      this.players = res.json();
      this.loading = false;
      this.heading = "Multan Sultan Squad"
    });
  }


}
