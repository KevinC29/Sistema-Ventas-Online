import { Component, OnInit, Inject } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { User } from 'src/app/interfaces/user';

import { UserService } from 'src/app/Services/user.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import { RoleEnum } from './enums';

@Component({
  selector: 'app-modal-user',
  templateUrl: './modal-user.component.html',
  styleUrls: ['./modal-user.component.css']
})
export class ModalUserComponent implements OnInit{
  form_user: FormGroup;
  titleAction: string = "Agregar";
  hide_password : boolean = true;
  buttonAction: string = "Guardar";
  role_enum = RoleEnum

  constructor(
    private modalCurrent: MatDialogRef<ModalUserComponent>,
    @Inject(MAT_DIALOG_DATA) public dataUser: User,
    private fb: FormBuilder,
    private _userService: UserService,
    private _utilsService: UtilsService
  ) { 
    this.form_user = this.fb.group({
      name: ['', Validators.required],
      role: ['', Validators.required],
      password_hash: ['', Validators.required],
    });

    if(this.dataUser != null){
      this.titleAction = "Editar";
      this.buttonAction = "Actualizar";
    }

  }

  ngOnInit(): void {
    if(this.dataUser !=null){
      this.form_user.patchValue({
        name: this.dataUser.name,
        role: this.dataUser.role,
        password_hash: this.dataUser.password_hash,
      });
    }
  }

  saveUpdate_User(){

    const _user: User = {
      id: this.dataUser == null ? '': this.dataUser.id,
      name: this.form_user.value.name,
      role: this.form_user.value.role,
      password_hash: this.form_user.value.password_hash,
    }

    if(this.dataUser == null){
      this._userService.create(_user).subscribe({
        next: (response) => {
          if(response.status){
            this._utilsService.showAlert(response.msg, 'Éxito');
            this.modalCurrent.close("true");
          }else
            this._utilsService.showAlert(response.msg, 'Error');
            
          },
        error: (error) => {
          this._utilsService.showAlert('error', 'Oops');
        }
      })
    }else{

      this._userService.update(_user.id, _user).subscribe({
        next: (response) => {
          if(response.status){
            this._utilsService.showAlert(response.msg, 'Éxito');
            this.modalCurrent.close("true");
          }else
            this._utilsService.showAlert(response.msg, 'Error');
            
          },
        error: (error) => {
          this._utilsService.showAlert('error', 'Oops');
        }
      })
    }
  }
}
