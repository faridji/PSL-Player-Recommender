import { Component,OnInit} from '@angular/core';
import { Router,NavigationEnd,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{

  searchResult : String;
  searchValue:string = '';
  dialogVisibility : boolean;
  message : String = ""

  constructor(private router: Router,private route: ActivatedRoute) { 
    this.dialogVisibility = false;
  }

  public getOwnerTokenData() : String{
    return localStorage.getItem('currentUserToken')
  }
  
  searchPlayer(name) : void{
    //First make the input field for search to null
    this.searchValue = null;
    
    this.searchResult = name;
    if (this.searchResult){
      this.router.navigate(['/player_profile'],{ queryParams: { result: name }  });
    }
  }

  showDialog() : void{
    this.dialogVisibility = true;
  }

  ngOnInit(): void {


    this.router.events.subscribe((evt) => {
      if (!(evt instanceof NavigationEnd)) {
          return;
      }
      window.scrollTo(0, 0)
  });
  }
  
}
