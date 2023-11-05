import { Injectable } from '@angular/core';

import { MatSnackBar } from '@angular/material/snack-bar';
import { Sesion } from '../interfaces/sesion';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor(private _snackBar: MatSnackBar) { }

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
    localStorage.removeItem("user");
  }
}
