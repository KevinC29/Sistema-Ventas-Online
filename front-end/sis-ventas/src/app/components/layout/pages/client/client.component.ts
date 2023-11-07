import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';

import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';

import { ModalClientComponent } from '../../modales/modal-client/modal-client.component';
import { Client } from 'src/app/interfaces/client';
import { ClientService } from 'src/app/Services/client.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import { GenderEnum } from 'src/app/components/layout/modales/modal-client/enums';
import Swal from 'sweetalert2';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.css']
})
export class ClientComponent implements OnInit, AfterViewInit{

  colTable : string[] = ['Nombres', 'Apellidos', 'Cédula', 'Dirección', 'Género', 'Saldo', 'Acciones'];
  dataStart : Client[] = [];
  dataListClient = new MatTableDataSource(this.dataStart);
  @ViewChild(MatPaginator) paginatorTable !: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private dialog: MatDialog,
    private _clientService: ClientService,
    private _utilsService: UtilsService
  ){}

  getClients() {
    this._clientService.list().subscribe({
      next: (response) => {
        if (response.status) {
          this.dataListClient = response.data;
        } else {
          this._utilsService.showAlert(response.msg, 'Oops');
        }
      },
      error: (error) => {
        this._utilsService.showAlert(error, 'Oops');
      }
    });
  }

  ngOnInit(): void {
    this.getClients();
  }

  ngAfterViewInit(): void {
    this.dataListClient.paginator = this.paginatorTable;
    this.dataListClient.sort = this.sort;
  }

  filterTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataListClient.filter = filterValue.trim().toLowerCase();
    
    if (this.dataListClient.paginator) {
      this.dataListClient.paginator.firstPage();
    }
  }

  getGenderText(gender: string): string {
    switch (gender) {
      case GenderEnum.Male:
        return 'Masculino';
      case GenderEnum.Female:
        return 'Femenino';
      case GenderEnum.Other:
        return 'Otro';
      default:
        return 'Desconocido';
    }
  }

  newClient() {
    this.dialog.open(ModalClientComponent, {
      disableClose: true
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getClients();
      }
    });
  }

  updateClient(client: Client) {
    this.dialog.open(ModalClientComponent, {
      disableClose: true,
      data: client
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getClients();
      }
    });
  }

  deleteClient(client: Client) {
    Swal.fire({
      title: '¿Está seguro de eliminar el cliente?',
      text: client.names,
      icon: 'warning',
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Si, eliminar',
      showCancelButton: true,
      cancelButtonColor: '#d33',
      cancelButtonText: 'No, volver'
      }).then((resultSwal) => {
        if (resultSwal.isConfirmed) {
          this._clientService.delete(client.id).subscribe({
            next: (response) => {
              if (response.status) {
                this._utilsService.showAlert(response.msg, 'Éxito');
                this.getClients();
              } else {
                this._utilsService.showAlert(response.msg, 'Oops');
              }
            },
            error: (error) => {
              this._utilsService.showAlert(error, 'Oops');
            }
          });
        }
      });
  }
}
