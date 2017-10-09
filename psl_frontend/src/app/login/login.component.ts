import { Component, OnInit,Output,EventEmitter} from '@angular/core';
import {Http, Response,Headers,RequestOptions} from '@angular/http';
import { FormBuilder,FormGroup,Validators,AbstractControl,FormControl} from '@angular/forms';
import {Router} from '@angular/router'

function validateEmail(c: FormControl) : { [s: string]: boolean } {
  if (!c.value.match(/^[a-z0-9!#$%&'*+\/=?^_`{|}~.-]+@[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*$/i)) {
    return {invalidemail: true};}
  };

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  myForm : FormGroup;
  email : AbstractControl;
  password : AbstractControl;

  token : String;
  success : boolean;
  error_message : String;

  constructor(private http:Http, private fb:FormBuilder, private router: Router) { 
    this.myForm = fb.group({
      'email': ['',Validators.compose(
        [Validators.required,validateEmail]
      )],
      'password': ['', Validators.required]
    });

    this.email = this.myForm.controls['email'];
    this.password = this.myForm.controls['password']
  }

  onSubmit(value: String): void{
    this.error_message = ""
    this.http.post('http://127.0.0.1:8081/authenticate',value)
    .subscribe((res:Response)=>{

      this.success = res.json().success;
      
      //Check whether server responded with success or failure and set message accordingly.
      if (this.success){
        localStorage.setItem('currentUserToken', res.json().token);
        localStorage.setItem('currentUserName',res.json().name);
        localStorage.setItem('currentUserId',res.json().id);
      
        //Reload the page after 2 seconds
        setTimeout(function(){
          location.reload(); 
        },1);
      }
      else{
        this.error_message = res.json().message;
      }
    });
  
  }

  signUp(): void{
    this.router.navigateByUrl('/signUp')
  }

  ngOnInit() {
  }
}
