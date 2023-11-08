import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';

import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';

import { ModalUserComponent } from '../../modales/modal-user/modal-user.component';
import { User } from 'src/app/interfaces/user';
import { UserService } from 'src/app/Services/user.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import { RoleEnum } from 'src/app/components/layout/modales/modal-user/enums';
import Swal from 'sweetalert2';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit, AfterViewInit{

  colTable : string[] = ['Nombre', 'Rol', 'Acciones'];
  dataStart : User[] = [];
  dataListUser = new MatTableDataSource(this.dataStart);
  @ViewChild(MatPaginator) paginatorTable !: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private dialog: MatDialog,
    private _userService: UserService,
    private _utilsService: UtilsService
  ){}

  getUsers() {
    this._userService.list().subscribe({
      next: (response) => {
        if (response.status) {
          this.dataListUser = response.data;
        } else {
          this._utilsService.showAlert(response.msg, 'Oops');
        }
      },
      error: (error) => {
        this._utilsService.showAlert('error', 'Oops');
      }
    });
  }

  ngOnInit(): void {
    this.getUsers();
  }

  ngAfterViewInit(): void {
    this.dataListUser.paginator = this.paginatorTable;
    this.dataListUser.sort = this.sort;
  }

  filterTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataListUser.filter = filterValue.trim().toLowerCase();
    
    if (this.dataListUser.paginator) {
      this.dataListUser.paginator.firstPage();
    }
  }

  getRoleText(role: string): string {
    switch (role) {
      case RoleEnum.EDITOR:
        return 'Editor';
      case RoleEnum.BASIC:
        return 'Basico';
      default:
        return 'Desconocido';
    }
  }

  newUser() {
    this.dialog.open(ModalUserComponent, {
      disableClose: true
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getUsers();
      }
    });
  }

  updateUser(user: User) {
    this.dialog.open(ModalUserComponent, {
      disableClose: true,
      data: user
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getUsers();
      }
    });
  }

  deleteUser(user: User) {
    Swal.fire({
      title: '¿Está seguro de eliminar el cliente?',
      text: user.name,
      icon: 'warning',
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Si, eliminar',
      showCancelButton: true,
      cancelButtonColor: '#d33',
      cancelButtonText: 'No, volver'
      }).then((resultSwal) => {
        if (resultSwal.isConfirmed) {
          this._userService.delete(user.id).subscribe({
            next: (response) => {
              if (response.status) {
                this._utilsService.showAlert(response.msg, 'Éxito');
                this.getUsers();
              } else {
                this._utilsService.showAlert(response.msg, 'Oops');
              }
            },
            error: (error) => {
              this._utilsService.showAlert('error', 'Oops');
            }
          });
        }
      });
  }
}
