import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { ModalModule } from 'ngx-modialog';
import { BootstrapModalModule } from 'ngx-modialog/plugins/bootstrap';
import { RouterModule,Routes } from '@angular/router';
import {LocationStrategy, HashLocationStrategy} from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { L_SEMANTIC_UI_MODULE } from 'angular2-semantic-ui';
import {NgxPaginationModule} from 'ngx-pagination'; // <-- import the module


import { AppComponent } from './app.component';
import { ServerSideDealingsComponent } from './server-side-dealings/server-side-dealings.component';
import { DatasetComponent } from './dataset/dataset.component';
import { ReportsComponent } from './reports/reports.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ModelComponent } from './model/model.component';
import { PslTeamsComponent } from './psl-teams/psl-teams.component';
import { OwnerProfileComponent } from './owner-profile/owner-profile.component';
import { SignOutComponent } from './sign-out/sign-out.component';
import { ProfilePopupComponent } from './profile-popup/profile-popup.component';
import { PlayerProfileComponent } from './player-profile/player-profile.component';
import { ErrorComponent } from './error/error.component';
import { HowPSLWorksComponent } from './how-pslworks/how-pslworks.component';

const routes: Routes = [ { path: '', redirectTo: 'home', pathMatch: 'full' },
{ path: 'home', component: ServerSideDealingsComponent },
{ path: 'PSL_teams',component:PslTeamsComponent},
{ path: 'dataset', component: DatasetComponent },
{ path: 'reports', component: ReportsComponent},
{ path: 'aboutUs',component:AboutUsComponent},
{ path: 'signUp',component:SignUpComponent},
{ path: 'model',component:ModelComponent},
{ path: 'Owner_profile',component:OwnerProfileComponent},
{ path: 'player_profile',component:PlayerProfileComponent},
{ path: 'login',component:LoginComponent},
{ path: 'error',component:ErrorComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    ServerSideDealingsComponent,
    DatasetComponent,
    ReportsComponent,
    AboutUsComponent,
    LoginComponent,
    SignUpComponent,
    ModelComponent,
    PslTeamsComponent,
    OwnerProfileComponent,
    SignOutComponent,
    ProfilePopupComponent,
    PlayerProfileComponent,
    ErrorComponent,
    HowPSLWorksComponent,
   
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    ReactiveFormsModule,
    L_SEMANTIC_UI_MODULE,
    RouterModule.forRoot(routes),
    ModalModule.forRoot(),
    BootstrapModalModule,
    NgxPaginationModule
  ],
  providers: [{ provide: LocationStrategy, useClass: HashLocationStrategy }],
  bootstrap: [AppComponent]
})
export class AppModule { 
  
}
