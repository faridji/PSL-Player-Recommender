import { Component, OnInit,Pipe} from '@angular/core';
import {Http, Response} from '@angular/http';
import { Router } from '@angular/router';


@Component({
  selector: 'app-server-side-dealings',
  templateUrl: './server-side-dealings.component.html',
  styleUrls: ['./server-side-dealings.component.css']
})
@Pipe({name: 'round'})
export class ServerSideDealingsComponent implements OnInit {
  // Variables for different Categories Players
  players : Object;
  diamondPlayers : Object;
  goldPlayers : Object;
  silverPlayers : Object;
  supplementoryPlayers : Object;
  emergingPlayers : Object;
  bestPlaying_20 : Object;

  domesticPlayers : Object;

  p: number = 1;
  //Variables for different Drafting picks
  draftingPick : Object;

  //Best 20 Players and Best Playing Eleven
  best_20 : Object;
  best_11 : Object;
  
  //Survey Variables
  survey1Result : String = null
  survey2Result : String = null
  survey1 : Array<Object>;
  survey2 : Array<Object>;
  Shahid_Afridi_Votes : number;
  Chris_Ghyle_Votes : number
  Kevin_Peiterson_Votes : number
  Umar_Akmal_Votes : number
  Ahmad_Shahzad_Votes : number
  Brendom_Mecculum_Votes : number
  Muhammad_Amir_Votes : number
  Shane_Watson_Votes : number

  Peshawar_Zalmi_Votes : number;
  Karachi_Kings_Votes : number
  Quetta_Gladiators_Votes : number
  Lahore_Qalandars_Votes : number
  Multan_Sultan_Votes : number
  Islamabad_United_Votes : number
  

  totalVotes : number;

  //Others
  loading : boolean;
  options : Object;
  teamHeading : String;
  ownerName : String;
  data : string;
  selectedItem : String;
  token : String;
  showBestPlaying11 : boolean
  categoryHeading : String;
  
  // Toggle Buttons Variables 
  signUp_Visibility : boolean;
  login_Visibility : boolean;
  signUpForDrafting : boolean;
  loginForDrafting : boolean;
  dialogVisibility : boolean;
  
  constructor(private http : Http,private router: Router) {

    console.log("I am in Constructor")
    this.dialogVisibility = false;
    this.showBestPlaying11 = true;

      
      this.loading = true;
      this.http.get('http://127.0.0.1:8081/PSL/Categories/Platinum')
      .subscribe((res:Response)=>{
        this.players = res.json();
        this.categoryHeading = "Platinum Category Players"
        this.loading = false;
        
      });

   }

   listClick(event, newValue) {
    console.log(newValue);
    this.selectedItem = newValue;  // don't forget to update the model here
    // ... do other stuff here ...
}
   
   loadPlatinumCategory() : void{
    this.domesticPlayers = "";
    this.loading = true;
    this.http.get('http://127.0.0.1:8081/PSL/Categories/Platinum')
    .subscribe((res:Response)=>{
      this.categoryHeading = "Platinum Category Players"
      this.players = res.json();
      this.loading = false;

    });
  }
  

  loadDiamondCategory() : void{
    this.domesticPlayers = "";
    this.loading = true;
    this.http.get('http://127.0.0.1:8081/PSL/Categories/Diamond')
    .subscribe((res:Response)=>{
      
      this.players = res.json();
      this.categoryHeading = "Diamond Category Players"
      this.loading = false;
    });
  }

  loadGoldCategory() : void{
    this.domesticPlayers = "";
    this.loading = true;
    this.http.get('http://127.0.0.1:8081/PSL/Categories/Gold')
    .subscribe((res:Response)=>{
     
      this.players = res.json();
      this.categoryHeading = "Gold Category Players"
      this.loading = false;
    });
  }

  loadSilverCategory() : void{
    this.domesticPlayers = "";
    this.loading = true;
    this.http.get('http://127.0.0.1:8081/PSL/Categories/Silver')
    .subscribe((res:Response)=>{
      
      this.players = res.json();
      this.categoryHeading = "Silver Category Players"
      this.loading = false;
    });
  }

  loadEmergingCategory() : void{
    this.loading = true;
    this.players = []
    this.http.get('http://127.0.0.1:8081/PSL/Categories/Emerging')
    .subscribe((res:Response)=>{
      this.domesticPlayers = res.json();
      this.categoryHeading = "Emerging Category Players"
      this.loading = false;
    });
  }


//Drafting Process i.e Picking best players from the given 6 categories.
// (1) Picking Players from Platinum Category
platinumPick() : void{
  this.options = {
    pick : 'platinumPick',
    owner : localStorage.getItem('currentUserName')
  }
  this.loading = true;
  this.http.post('http://127.0.0.1:8081/PSL/platinumPick',this.options)
  .subscribe((res:Response)=>{
    this.draftingPick = res.json();
    this.loading = false;
  });

}
// (2) Picking Players from Diamond Category
diamondPick() : void{
  this.options = {
    pick : 'diamondPick',
    owner : localStorage.getItem('currentUserName')
  };

  this.loading = true;
  this.http.post('http://127.0.0.1:8081/PSL/diamondPick',this.options)
  .subscribe((res:Response)=>{
    this.draftingPick = res.json();
    this.loading = false;
  });
}
// (3) Picking Players from Gold Category
goldPick() : void{ 
  this.options = {
    pick : 'goldPick',
    owner : localStorage.getItem('currentUserName')
  }
  this.loading = true;
  this.http.post('http://127.0.0.1:8081/PSL/goldPick',this.options)
  .subscribe((res:Response)=>{
    this.loading = false;
    this.draftingPick = res.json();
   
  });
}
// (4) Picking Players from Silver Category
silverPick() : void{
  this.options = {
    pick : 'silverPick',
    owner : localStorage.getItem('currentUserName')
  }

  this.loading = true;
  this.http.post('http://127.0.0.1:8081/PSL/silverPick',this.options)
  .subscribe((res:Response)=>{

    this.loading = false;
    this.draftingPick = res.json();
    
  });
}
// (5) Picking Players from Supplementory Category
supplementoryPick() : void{
  this.options = {
    pick : 'supplementoryPick',
    owner : localStorage.getItem('currentUserName')
  }

  this.loading = true;
  this.http.post('http://127.0.0.1:8081/PSL/supplementoryPick',this.options)
  .subscribe((res:Response)=>{
    this.loading = false;
    this.draftingPick= res.json();
  });
}
// (6) Picking Players from Emerging Category
emergingPick() : void{
  this.options = {
    pick : 'emergingPick',
    owner : localStorage.getItem('currentUserName')
  }

  this.loading = true;
  this.http.post('http://127.0.0.1:8081/PSL/emergingPick',this.options)
  .subscribe((res:Response)=>{

    this.loading = false;
    this.draftingPick = res.json();
    
  });
}

getBest20_Players(): void{
  this.showBestPlaying11 = true;  
  this.options = {
    name : localStorage.getItem('currentUserName')
  }
  this.http.post('http://127.0.0.1:8081/PSL/best_20',this.options)
  .subscribe((res:Response)=>{
    this.best_20 = res.json();
   
    this.best_11 = []
    this.loading = false;
    this.teamHeading = "Best 20 Players"
  });
}

getBest11_Players(): void{
  this.loading = true;

  this.options = {
    pick : 'best_11',
    name : localStorage.getItem('currentUserName')
  }
  console.log("options",this.options)

  this.http.post('http://127.0.0.1:8081/PSL/best_11',this.options)
  .subscribe((res:Response)=>{
    
    if(res.json().success){

      this.showBestPlaying11 = true;
      this.best_11 = JSON.parse(res.json().data);
    
      this.best_20 = []
      this.loading = false;
      this.teamHeading = "Best 11 Players"
    }
    else{
      this.showBestPlaying11 = false;
      this.loading = false;
    }
  });
}

pslTeam(name) : void{
  this.router.navigate(['/PSL_teams'],{ queryParams: { result: name }  });
}

submitSurvey() : void{

  //Survey Results will show up in frontend when a player is selected, else nothing will showup
  if(this.survey1Result){

    this.totalVotes = 0;
    this.Shahid_Afridi_Votes = 0;
    this.Ahmad_Shahzad_Votes = 0;
    this.Brendom_Mecculum_Votes = 0;
    this.Kevin_Peiterson_Votes = 0;
    this.Chris_Ghyle_Votes = 0;
    this.Muhammad_Amir_Votes = 0;
    this.Shane_Watson_Votes = 0;
    this.Umar_Akmal_Votes = 0;
  
    //Store and retriev the results from db;
    this.options = {
      name : this.survey1Result
    }
    this.http.post('http://127.0.0.1:8081/PSL/survey/favouritePSLPlayer',this.options)
    .subscribe((res:Response)=>{
      this.survey1 = res.json();
    
    //processData
    for(let data of this.survey1) {
    if (data['name'] == "Shahid_Afridi"){
        this.Shahid_Afridi_Votes = data['vote']
        this.totalVotes += data['vote']
      }
      if (data['name'] ==  "Chris_Ghyle"){
        this.Chris_Ghyle_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
      if (data['name'] == "Brendom_Mecculum"){
        this.Brendom_Mecculum_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
      if (data['name'] == "Kevin_Peiterson"){
        this.Kevin_Peiterson_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
  
      if (data['name'] == "Ahmad_Shahzad"){
        this.Ahmad_Shahzad_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
      if (data['name'] == "Umar_Akmal"){
        this.Umar_Akmal_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
      if (data['name'] == "Muhammad_Amir"){
        this.Muhammad_Amir_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
      if (data['name'] == "Shane_Watson"){
        this.Shane_Watson_Votes = data['vote']
        this.totalVotes += data['vote'];
      }
    }
    
  
    //Calculating Voting in Percent
    
    this.Shahid_Afridi_Votes = (100 * this.Shahid_Afridi_Votes)/this.totalVotes;
    this.Ahmad_Shahzad_Votes = (100 * this.Ahmad_Shahzad_Votes)/this.totalVotes;
    this.Umar_Akmal_Votes = (100 * this.Umar_Akmal_Votes)/this.totalVotes;
    this.Muhammad_Amir_Votes = (100 * this.Muhammad_Amir_Votes)/this.totalVotes;
    this.Brendom_Mecculum_Votes = (100 * this.Brendom_Mecculum_Votes)/this.totalVotes;
    this.Shane_Watson_Votes = (100 * this.Shane_Watson_Votes)/this.totalVotes;
    this.Chris_Ghyle_Votes = (100 * this.Chris_Ghyle_Votes)/this.totalVotes;
    this.Kevin_Peiterson_Votes = (100 * this.Kevin_Peiterson_Votes)/this.totalVotes;
  
  });
}

//Survey 2
if(this.survey2Result){

  this.totalVotes = 0;

  this.Peshawar_Zalmi_Votes = 0
  this.Karachi_Kings_Votes = 0
  this.Quetta_Gladiators_Votes = 0
  this.Lahore_Qalandars_Votes = 0 
  this.Multan_Sultan_Votes = 0
  this.Islamabad_United_Votes = 0

  //Store and retriev the results from db;
  this.options = {
    name : this.survey2Result
  }
  this.http.post('http://127.0.0.1:8081/PSL/survey/favouritePSLTeam',this.options)
  .subscribe((res:Response)=>{
    this.survey2 = res.json();
  
  //processData
  for(let data of this.survey2) {
  if (data['name'] == "Peshawar_Zalmi"){
      this.Peshawar_Zalmi_Votes = data['vote']
      this.totalVotes += data['vote']
    }
    if (data['name'] ==  "Quetta_Gladiators"){
      this.Quetta_Gladiators_Votes = data['vote']
      this.totalVotes += data['vote'];
    }
    if (data['name'] == "Islamabad_United"){
      this.Islamabad_United_Votes = data['vote']
      this.totalVotes += data['vote'];
    }
    if (data['name'] == "Karachi_Kings"){
      this.Karachi_Kings_Votes = data['vote']
      this.totalVotes += data['vote'];
    }

    if (data['name'] == "Multan_Sultan"){
      this.Multan_Sultan_Votes = data['vote']
      this.totalVotes += data['vote'];
    }
    if (data['name'] == "Lahore_Qalandars"){
      this.Lahore_Qalandars_Votes = data['vote']
      this.totalVotes += data['vote'];
    }
    
  }
  

  //Calculating Voting in Percent
  console.log(this.totalVotes)
  this.Peshawar_Zalmi_Votes = (100 * this.Peshawar_Zalmi_Votes)/this.totalVotes;
  this.Quetta_Gladiators_Votes = (100 * this.Quetta_Gladiators_Votes)/this.totalVotes;
  this.Islamabad_United_Votes = (100 * this.Islamabad_United_Votes)/this.totalVotes;
  this.Multan_Sultan_Votes = (100 * this.Multan_Sultan_Votes)/this.totalVotes;
  this.Karachi_Kings_Votes = (100 * this.Karachi_Kings_Votes)/this.totalVotes;
  this.Lahore_Qalandars_Votes = (100 * this.Lahore_Qalandars_Votes)/this.totalVotes;
  
});
}
  
}

toggle_SignUpVisibility(): void{
  this.dialogVisibility = true;
  this.signUp_Visibility = true;
  this.login_Visibility = false;
}

toggle_LoginVisibility(): void{
  this.dialogVisibility = true;
  this.signUp_Visibility = false;
  this.login_Visibility = true;
}
  
showSignUpForDrafting() : void{
  this.dialogVisibility = true;
  this.signUpForDrafting = true;
  this.loginForDrafting = false;
}

showLoginForDrafting() : void{
  this.dialogVisibility = true;
  this.loginForDrafting = true;
  this.signUpForDrafting = false;
}

 public getTokenData() : String{
  return localStorage.getItem('currentUserToken')
}


ngOnInit() {
  console.log("I am in ngOnInit() Method")
}

}
