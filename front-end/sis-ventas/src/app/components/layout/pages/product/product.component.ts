import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';

import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';

import { ModalProductComponent } from '../../modales/modal-product/modal-product.component';
import { Product } from 'src/app/interfaces/product';
import { ProductService } from 'src/app/Services/product.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import Swal from 'sweetalert2';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})

export class ProductComponent implements OnInit, AfterViewInit{
  colTable : string[] = ['Nombre', 'Imagen', 'Stock', 'PVP', 'Categoría', 'Acciones'];
  dataStart : Product[] = [];
  dataListProduct = new MatTableDataSource(this.dataStart);
  @ViewChild(MatPaginator) paginatorTable !: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private dialog: MatDialog,
    private _productService: ProductService,
    private _utilsService: UtilsService
  ){}


  getProducts() {
    this._productService.list().subscribe({
      next: (response) => {
        if (response.status) {
          this.dataListProduct = response.data;
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
    this.getProducts();

  }

  ngAfterViewInit(): void {
    this.dataListProduct.paginator = this.paginatorTable;
    this.dataListProduct.sort = this.sort;
  }

  filterTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataListProduct.filter = filterValue.trim().toLowerCase();
    
    if (this.dataListProduct.paginator) {
      this.dataListProduct.paginator.firstPage();
    }
  }

  newProduct() {
    this.dialog.open(ModalProductComponent, {
      disableClose: true
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getProducts();
      }
    });
  }

  updateProduct(product: Product) {
    this.dialog.open(ModalProductComponent, {
      disableClose: true,
      data: product
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getProducts();
      }
    });
  }

  deleteProduct(product: Product) {
    Swal.fire({
      title: '¿Está seguro de eliminar el producto?',
      text: product.name,
      icon: 'warning',
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Si, eliminar',
      showCancelButton: true,
      cancelButtonColor: '#d33',
      cancelButtonText: 'No, volver'
      }).then((resultSwal) => {
        if (resultSwal.isConfirmed) {
          this._productService.delete(product.id).subscribe({
            next: (response) => {
              if (response.status) {
                this._utilsService.showAlert(response.msg, 'Éxito');
                this.getProducts();
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
