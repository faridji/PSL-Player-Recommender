import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router'
@Component({
  selector: 'app-sign-out',
  templateUrl: './sign-out.component.html',
  styleUrls: ['./sign-out.component.css'],
})
export class SignOutComponent implements OnInit {
  ownerName : String;
  constructor(private router:Router) { 
    this.ownerName = localStorage.getItem('currentUserName')
  }

  ngOnInit() {
  }

  signOut() : void{
    
    localStorage.removeItem('currentUserToken');
    this.router.navigateByUrl('/home')
    location.reload(); 
    
  }

  change($event) {
    alert($event)
  }

  

}
