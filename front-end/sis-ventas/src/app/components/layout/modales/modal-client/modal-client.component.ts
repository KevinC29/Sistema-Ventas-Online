import { Component, OnInit, Inject } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Client } from 'src/app/interfaces/client';

import { ClientService } from 'src/app/Services/client.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import { GenderEnum } from './enums';

@Component({
  selector: 'app-modal-client',
  templateUrl: './modal-client.component.html',
  styleUrls: ['./modal-client.component.css']
})
export class ModalClientComponent implements OnInit{

  form_client: FormGroup;
  titleAction: string = "Agregar";
  buttonAction: string = "Guardar";
  gender_enum = GenderEnum

  constructor(
    private modalCurrent: MatDialogRef<ModalClientComponent>,
    @Inject(MAT_DIALOG_DATA) public dataClient: Client,
    private fb: FormBuilder,
    private _clientService: ClientService,
    private _utilsService: UtilsService
  ) { 
    this.form_client = this.fb.group({
      names: ['', Validators.required],
      surnames: ['', Validators.required],
      dni: ['', Validators.required],
      address: ['', Validators.required],
      gender_value: ['', Validators.required],
      balance: ['', Validators.required]
    });

    if(this.dataClient != null){
      this.titleAction = "Editar";
      this.buttonAction = "Actualizar";
    }

  }

  ngOnInit(): void {
    if(this.dataClient !=null){
      this.form_client.patchValue({
        names: this.dataClient.names,
        surnames: this.dataClient.surnames,
        dni: this.dataClient.dni,
        address: this.dataClient.address,
        gender_value: this.dataClient.gender,
        balance: this.dataClient.balance
      });
    }
  }

  saveUpdate_Client(){

    // const balanceString: string = this.form_client.value.balance;
    // const balanceFloat: number = parseFloat(parseFloat(balanceString).toFixed(2));


    const _client: Client = {
      id: this.dataClient == null ? '': this.dataClient.id,
      names: this.form_client.value.names,
      surnames: this.form_client.value.surnames,
      dni: this.form_client.value.dni,
      address: this.form_client.value.address,
      gender: this.form_client.value.gender_value,
      balance: this.form_client.value.balance
    }

    if(this.dataClient == null){
      this._clientService.create(_client).subscribe({
        next: (response) => {
          // console.log(response)
          if(response.status){
            this._utilsService.showAlert(response.msg, 'Éxito');
            this.modalCurrent.close("true");
          }else
            this._utilsService.showAlert(response.msg, 'Error');
            
          },
        error: (error) => {
          this._utilsService.showAlert(error, 'Oops');
        }
      })
    }else{

      this._clientService.update(_client.id, _client).subscribe({
        next: (response) => {
          if(response.status){
            this._utilsService.showAlert(response.msg, 'Éxito');
            this.modalCurrent.close("true");
          }else
            this._utilsService.showAlert(response.msg, 'Error');
            
          },
        error: (error) => {
          this._utilsService.showAlert(error, 'Oops');
        }
      })

    }
  }
}
