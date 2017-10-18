import { Component,OnInit} from '@angular/core';
import { Http,Response} from '@angular/http'


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  
  loading: Boolean;
  options : Object;
  owners : Object;
  title: Object;
  noOfOwners : number
  Loading_heading : String;
  mainData : Boolean;
  data : Object; 
  isDataExits : Boolean = false;
  constructor(private http:Http) {

    
    this.mainData = true;
    
   }
  updateT20Dataset() : void{
    this.isDataExits = false;
    this.loading = true;
    this.title = "Updating T20_dataset"
    this.mainData = false;
    this.Loading_heading = "updating_Dataset"
    this.options = {
      update : 't20_dataset'
    }

    this.http.post('http://127.0.0.1:8081/PSL/updateDataset',this.options)
    .subscribe((res:Response)=>{
      this.data = res.json();
      this.loading = false;

    });
  }

  updatePSLDataset() : void{
    this.isDataExits = false;
    this.loading = true;
    this.mainData = false;
    this.title = "Updating PSL_dataset"
    this.options = {
      update : 'psl_dataset'
    }

    this.http.post('http://127.0.0.1:8081/PSL/updateDataset',this.options)
    .subscribe((res:Response)=>{
      this.data = res.json();
      this.loading = false;

    });
  }

  updateDomesticDataset() : void{
    this.isDataExits = false;
    this.loading = true;
    this.mainData = false;
    this.title = "Updating Domestic_dataset"
    this.options = {
      update : 'domestic_dataset'
    }

    this.http.post('http://127.0.0.1:8081/PSL/updateDataset',this.options)
    .subscribe((res:Response)=>{
      this.data = res.json();
      this.loading = false;

    });
  }

  viewPSLOwners() : void{
    this.isDataExits = false;
    this.loading = true;
    this.title = "PSL Owners"
    this.mainData = false;

    this.http.get('http://127.0.0.1:8081/PSL/Owners')
    .subscribe((res:Response)=>{
      this.owners = res.json();
      this.loading = false;
    });
  }

  makeCategories(): void{
    this.loading = true;
    this.mainData = false;
    this.title = "PSL Categories Formation"
    
    this.http.get('http://127.0.0.1:8081/PSL/makePSLCategories')
    .subscribe((res:Response)=>{
      this.data = res.json();
      this.isDataExits = true;
      this.owners = []
      console.log(this.data)
      this.loading = false;
    });
  }

  setAdminFunctionalities() : void{
    this.title = "Admin Dashboard"
  }
  
  ngOnInit() {
    this.setAdminFunctionalities()
    this.http.get('http://127.0.0.1:8081/PSL/Owners')
    .subscribe((res:Response)=>{
      this.noOfOwners = res.json().length;
      this.loading = false;
    });

    console.log(this.owners)
  }
}
