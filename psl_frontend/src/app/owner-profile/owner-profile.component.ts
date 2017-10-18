import { Component, OnInit, Directive, ElementRef, Renderer, ChangeDetectorRef } from '@angular/core';
import {Http, Response} from '@angular/http';
import {Router} from '@angular/router'


@Component({
  selector: 'app-owner-profile',
  templateUrl: './owner-profile.component.html',
  styleUrls: ['./owner-profile.component.css']
})


@Directive({selector : 'best20Tab'})
@Directive({selector : 'personalInfo'})
@Directive({selector : 'best11Tab'})

export class OwnerProfileComponent implements OnInit {
  signUp_Visibility : boolean;
  login_Visibility : boolean;
  
  _id : Object;
  ownerImageUrl : String;
  selectedOwner : Object;
  best20_player : Object;
  best11_player : Object;
  options : Object;
  
  data : Object;
  message:String = ""
  ownerName : String;

  loading : boolean;
  p_info : boolean;
  success : boolean = false;
  best20 : boolean;
  best11 : boolean;
  mainHeading : string;


  constructor(private http:Http,private changeDetectorRef: ChangeDetectorRef, private router : Router,private renderer: Renderer) {
    this.p_info = true;
    this.mainHeading = "Personal Information"
   }

  ngOnInit() {
    this._id = localStorage.getItem('currentUserId')
    this.ownerName = localStorage.getItem('currentUserName')

    this.options = {
      _id : this._id,
      name : this.ownerName,
      pick : 'best_11'
    }
  

  this.http.post('http://127.0.0.1:8081/PSL/specificOwner',this.options)
  .subscribe((res:Response)=>{
    this.selectedOwner = res.json();
    localStorage.setItem('currentUserName',this.selectedOwner['name'])
  });


  this.http.post('http://127.0.0.1:8081/PSL/best_20',this.options)
  .subscribe((res:Response)=>{
    this.best20_player = res.json();
  });


  this.http.post('http://127.0.0.1:8081/PSL/getbest_11',this.options)
  .subscribe((res:Response)=>{
    this.best11_player = JSON.parse(res.json().data);
  });
}

saveChanges(value: JSON): void{
 
  this._id = localStorage.getItem('currentUserId')
  this.options = {
    _id : this._id,
    'form':value
  }
  if(value['owner_name']){
      this.http.put('http://127.0.0.1:8081/PSL/updateOwnerInformation', this.options)
      .subscribe((res:Response)=>{
        this.success = res.json().success; 
        this.message = res.json().message;
        this.data = res.json().owner;
        console.log(this.data['name'])

        localStorage.setItem('currentUserName',this.data['name']);
        location.reload()
        this.ownerName = this.data['name']
      });
  }
}

closeMessageBox(): void{
  this.success = false;
}

deleteAccount() : void{
  this.loading = true;
  this.options = {
    ownerId : localStorage.getItem('currentUserId'),
    ownerName : localStorage.getItem('currentUserName')
  }
  this.http.post('http://127.0.0.1:8081/PSL/deleteSpecificOwner',this.options).subscribe((res:Response)=>{
    this.success = res.json().success; 
    if(this.success){
      this.loading = false;
      this.message = res.json().message;
      localStorage.removeItem('currentUserToken');
      localStorage.removeItem('currentUserName');
      localStorage.removeItem('currentUserId');

      
      this.router.navigate(['/home'],{ queryParams: { message: this.message }  });
      
    }
  });
}

deleteBest11() : void{
  this.options = {
    ownerName : localStorage.getItem('currentUserName')
  }
  this.http.post('http://127.0.0.1:8081/PSL/deletebest11',this.options).subscribe((res:Response)=>{
    this.success = res.json().success; 
    if(this.success){
      this.message = res.json().message; 
      location.reload()     
    }
  });
}
best_20(): void{

  this.mainHeading = "20 Players Team"
  this.p_info = false;
  this.best20 = true;
  this.best11 = false;
}

personal_Info(): void{
  
  this.mainHeading = "Personal Information"
  this.p_info = true;
  this.best20 = false;
  this.best11 = false;

}

best_11(): void{
 
  this.mainHeading = "";
  this.mainHeading = "Best Playing Eleven"
  this.p_info = false;
  this.best20 = false;
  this.best11 = true;
}

signOut() : void{
  localStorage.removeItem('currentUserToken');
  this.router.navigateByUrl('/home')
}

public getTokenData() : String{
  return localStorage.getItem('currentUserToken')
}

toggle_SignUpVisibility(): void{
  this.signUp_Visibility = true;
  this.login_Visibility = false;
}

toggle_LoginVisibility(): void{
  this.signUp_Visibility = false;
  this.login_Visibility = true;
}
}
