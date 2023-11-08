import { Injectable } from '@angular/core';

import { MatSnackBar } from '@angular/material/snack-bar';
import { Sesion } from '../interfaces/sesion';
import { LoginService } from 'src/app/Services/login.service';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor(
    private _snackBar: MatSnackBar,
    private _userService : LoginService,
  ) { }

  showAlert(message: string, type: string) {
    this._snackBar.open(message,type,{
      horizontalPosition: "end",
      verticalPosition: "top",
      duration:3000
    })
  }

  saveSesionUser(userSesion:Sesion){
    localStorage.setItem("user",JSON.stringify(userSesion));
  }

  getSesionUser(){
    const data = localStorage.getItem("user");
    const user = JSON.parse(data!);
    return user
  }

  deleteSesionUser(){
    this._userService.logout().subscribe({
      next:(response)=>{
        if(response.status){
          localStorage.removeItem("user");
        }else{
          this.showAlert(response.msg, "Opps!")
        }
      },
      error: (error)=>{
        this.showAlert("Existió un error al deslogearse", "Error");
      }
    })
  }
}
