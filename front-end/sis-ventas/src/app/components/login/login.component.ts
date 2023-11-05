import { Component, OnInit } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Login } from 'src/app/interfaces/login';
import { UtilsService } from 'src/app/reusable/utils.service';
import { UserService } from 'src/app/services/user.service';

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
    private _userService : UserService,
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

    this._userService.login(request).subscibe({
      next:(data)=>{
        if(data.)
      }
    })
  }

}
