import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';

import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';

import { Sale } from 'src/app/interfaces/sale';
import { SaleService } from 'src/app/Services/sale.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import Swal from 'sweetalert2';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, AfterViewInit{

  colTable : string[] = ['Cliente','Fecha', 'Subtotal', 'Iva', 'Total' , 'Acciones'];
  dataStart : Sale[] = [];
  dataListSale = new MatTableDataSource(this.dataStart);
  @ViewChild(MatPaginator) paginatorTable !: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private _saleService: SaleService,
    private _utilsService: UtilsService
  ){}

  getClients() {
    this._saleService.list().subscribe({
      next: (response) => {
        if (response.status) {
          this.dataListSale = response.data;
          console.log(this.dataListSale)
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
    this.dataListSale.paginator = this.paginatorTable;
    this.dataListSale.sort = this.sort;
  }

  filterTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataListSale.filter = filterValue.trim().toLowerCase();
    
    if (this.dataListSale.paginator) {
      this.dataListSale.paginator.firstPage();
    }
  }

  deleteSale(sale: Sale) {
    Swal.fire({
      title: '¿Está seguro de eliminar la venta?',
      text: sale.cli_id,
      icon: 'warning',
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Si, eliminar',
      showCancelButton: true,
      cancelButtonColor: '#d33',
      cancelButtonText: 'No, volver'
      }).then((resultSwal) => {
        if (resultSwal.isConfirmed) {
          this._saleService.delete(sale.id).subscribe({
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
