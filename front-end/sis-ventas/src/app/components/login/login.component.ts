import { Component, OnInit } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { response } from 'express';
import { Login } from 'src/app/interfaces/login';
import { UtilsService } from 'src/app/reusable/utils.service';
import { LoginService } from 'src/app/Services/login.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  form_login: FormGroup;
  hide_password : boolean = true;
  show_loading : boolean = false;

  constructor(
    private fb :FormBuilder,
    private router : Router,
    private _userService : LoginService,
    private _utilsService : UtilsService
  ) {

    this.form_login = this.fb.group({
      username:['',Validators.required],
      password:['',Validators.required]
    });

  }

  ngOnInit():void{

  }

  login(){
    this.show_loading = true;

    const request: Login = {
      username: this.form_login.value.username,
      password: this.form_login.value.password
    }

    this._userService.login(request).subscribe({
      next:(response)=>{
        if(response.status){
          this._utilsService.saveSesionUser(response.data);
          this.router.navigate(["pages"])
        }else{
          this._utilsService.showAlert(response.msg, "Opps!")
        }
      },
      complete: ()=>{
          this.show_loading = false;
      },
      error: ()=>{
        this._utilsService.showAlert("Existió un error", "Error");
      }
    })
  }
}
