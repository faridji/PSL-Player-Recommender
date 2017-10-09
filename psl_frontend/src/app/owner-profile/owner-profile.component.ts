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
  
  ownerName : String;

  p_info : boolean;
  best20 : boolean;
  best11 : boolean;
  mainHeading : string;


  path = '';  
  public file_srcs: string[] = [];  
  public debug_size_before: string[] = [];  
  public debug_size_after: string[] = [];  

  constructor(private http:Http,private changeDetectorRef: ChangeDetectorRef, private router : Router,private renderer: Renderer) {
    this.p_info = true;
    this.mainHeading = "Personal Information"
   }

   
   fileChange(input) { 
     
    console.log('Owner Image::' ,input.file_srcs)
  //   this.readFiles(input.files); 
  //   console.log()
  //   this._id = localStorage.getItem('currentUserId')
  //   this.ownerName = localStorage.getItem('currentUserName')
  //   this.options = {
  //     _id : this._id,
  //     image: this.ownerImageUrl
  //   }
  

  // this.http.put('http://127.0.0.1:8081/PSL/updateOwner',this.options)
  // .subscribe((res:Response)=>{
  //   this.selectedOwner = res.json();
  // }); 
}  
readFile(file, reader, callback) {  
    reader.onload = () => {  
        callback(reader.result);  
        this.ownerImageUrl = reader.result;
        console.log("Owner Image::", this.ownerImageUrl);  
    }  
    reader.readAsDataURL(file);  
}  
readFiles(files, index = 0) {  
    // Create the file reader  
    let reader = new FileReader();  
    // If there is a file  
    if (index in files) {  
        // Start reading this file  
        this.readFile(files[index], reader, (result) => {  
            // Create an img element and add the image file data to it  
            var img = document.createElement("img");  
            img.src = result;  
            // Send this img to the resize function (and wait for callback)  
            this.resize(img, 250, 250, (resized_jpeg, before, after) => {  
                // For debugging (size in bytes before and after)  
                this.debug_size_before.push(before);  
                this.debug_size_after.push(after);  
                // Add the resized jpeg img source to a list for preview  
                // This is also the file you want to upload. (either as a  
                // base64 string or img.src = resized_jpeg if you prefer a file).  
                this.file_srcs.push(resized_jpeg);  
                // Read the next file;  
                this.readFiles(files, index + 1);  
            });  
        });  
    } else {  
        // When all files are done This forces a change detection  
        this.changeDetectorRef.detectChanges();  
    }  
}  
resize(img, MAX_WIDTH: number, MAX_HEIGHT: number, callback) {  
    // This will wait until the img is loaded before calling this function  
    return img.onload = () => {  
        // Get the images current width and height  
        var width = img.width;  
        var height = img.height;  
        // Set the WxH to fit the Max values (but maintain proportions)  
        if (width > height) {  
            if (width > MAX_WIDTH) {  
                height *= MAX_WIDTH / width;  
                width = MAX_WIDTH;  
            }  
        } else {  
            if (height > MAX_HEIGHT) {  
                width *= MAX_HEIGHT / height;  
                height = MAX_HEIGHT;  
            }  
        }  
        // create a canvas object  
        var canvas = document.createElement("canvas");  
        // Set the canvas to the new calculated dimensions  
        canvas.width = width;  
        canvas.height = height;  
        var ctx = canvas.getContext("2d");  
        ctx.drawImage(img, 0, 0, width, height);  
        // Get this encoded as a jpeg  
        // IMPORTANT: 'jpeg' NOT 'jpg'  
        var dataUrl = canvas.toDataURL('image/jpeg');  
        // callback with the results  
        callback(dataUrl, img.src.length, dataUrl.length);  
    };  
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
  });


  this.http.post('http://127.0.0.1:8081/PSL/best_20',this.options)
  .subscribe((res:Response)=>{
    this.best20_player = res.json();
  });
  this.http.post('http://127.0.0.1:8081/PSL/best_11',this.options)
  .subscribe((res:Response)=>{
    this.best11_player = JSON.parse(res.json().data);
  });
}

  

deleteAccount() : void{
  this.options = {
    ownerId : localStorage.getItem('currentUserId')
  }
  console.log(this.options)
  
  this.http.delete('http://127.0.0.1:8081/PSL/deleteDocument',this.options).subscribe((res:Response)=>{
    localStorage.removeItem('currentUserToken');
    localStorage.removeItem('currentUserName');
    localStorage.removeItem('currentUserId');

  });
  //location.reload();
}


best_20(event:any): void{
  this.renderer.setElementClass(event.target,"active",true);
  this.mainHeading = "20 Players Team"
  this.p_info = false;
  this.best20 = true;
  this.best11 = false;
}

personal_Info(event:any): void{
  console.log(event)
  this.renderer.setElementClass(event.target,"active",true);
  this.mainHeading = "Personal Information"
  this.p_info = true;
  this.best20 = false;
  this.best11 = false;

}

best_11(event:any): void{
  this.renderer.setElementClass(event.target,"active",true);
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
