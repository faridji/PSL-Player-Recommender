import { Component, OnInit,Input,Output,EventEmitter } from '@angular/core';
import {Http, Response,Headers,RequestOptions} from '@angular/http';
import { FormBuilder,FormGroup,Validators,AbstractControl,FormControl} from '@angular/forms';

function validateEmail(c: FormControl) : { [s: string]: boolean } {
  if (!c.value.match(/^[a-z0-9!#$%&'*+\/=?^_`{|}~.-]+@[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*$/i)) {
   
    return {invalidemail: true};
  }

  };

  function validateNIC(c: FormControl) : { [s: string]: boolean } {

    if (!c.value.match(/^[0-9+]{5}-[0-9+]{7}-[0-9]{1}$/)) {
  
      return {invalidNIC: true};}
    };

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  myForm : FormGroup;
  owner_name : AbstractControl;
  email : AbstractControl;
  password : AbstractControl;
  cnic : AbstractControl;
  team_name : AbstractControl;
  
  success : boolean;
  err_message : String;
  success_message : String;
  
  
  constructor(private http:Http,private fb:FormBuilder) { 
    
    this.myForm = fb.group({
      'email': ['', Validators.compose(
        [Validators.required,validateEmail]
      )],
      'password': ['', Validators.required],
      'owner_name': ['', Validators.required],
      'cnic': ['', Validators.compose(
        [Validators.required,validateNIC]
      )],
      'team_name': ['', Validators.required],
  
    });

    this.owner_name = this.myForm.controls['owner_name'];
    this.password = this.myForm.controls['password']
    this.email = this.myForm.controls['email'];
    this.cnic = this.myForm.controls['cnic']
    this.team_name = this.myForm.controls['team_name'];

  }

  onSubmit(value: JSON): void{
    this.err_message = ""
    this.success_message = ""
    if(value['owner_name']){
      
        this.http.post('http://127.0.0.1:8081/PSL/createOwner',value)
        .subscribe((res:Response)=>{
          this.success = res.json().success;
          
          //Check whether server responded with success or failure and set message accordingly.
          if (this.success){
            console.log('Success Value',this.success)
            this.success_message = res.json().message;
            console.log(this.success_message)
            //Reload the page after 2 seconds
            setTimeout(function(){
              location.reload(); 
            },1000);
          }
          else{
            this.err_message = res.json().message;
          }
            
        });
      
    }

  
    
  }

  ngOnInit() {

  }
}
