import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';

import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';

import { ModalCategoryComponent } from '../../modales/modal-category/modal-category.component';
import { Category } from 'src/app/interfaces/category';
import { CategoryService } from 'src/app/Services/category.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import Swal from 'sweetalert2';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit, AfterViewInit{
  colTable : string[] = ['Nombre', 'Descripción', 'Acciones'];
  dataStart : Category[] = [];
  dataListCategory = new MatTableDataSource(this.dataStart);
  @ViewChild(MatPaginator) paginatorTable !: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private dialog: MatDialog,
    private _categoryService: CategoryService,
    private _utilsService: UtilsService
  ){}


  getCategorys() {
    this._categoryService.list().subscribe({
      next: (response) => {
        if (response.status) {
          this.dataListCategory = response.data;
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
    this.getCategorys();
  }

  ngAfterViewInit(): void {
    this.dataListCategory.paginator = this.paginatorTable;
    this.dataListCategory.sort = this.sort;
  }

  filterTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataListCategory.filter = filterValue.trim().toLowerCase();
    
    if (this.dataListCategory.paginator) {
      this.dataListCategory.paginator.firstPage();
    }
  }

  newCategory() {
    this.dialog.open(ModalCategoryComponent, {
      disableClose: true
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getCategorys();
      }
    });
  }

  updateCategory(category: Category) {
    this.dialog.open(ModalCategoryComponent, {
      disableClose: true,
      data: category
    }).afterClosed().subscribe((result) => {
      if(result === 'true'){
        this.getCategorys();
      }
    });
  }

  deleteCategory(category: Category) {
    Swal.fire({
      title: '¿Está seguro de eliminar la categoria?',
      text: category.name,
      icon: 'warning',
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Si, eliminar',
      showCancelButton: true,
      cancelButtonColor: '#d33',
      cancelButtonText: 'No, volver'
      }).then((resultSwal) => {
        if (resultSwal.isConfirmed) {
          this._categoryService.delete(category.id).subscribe({
            next: (response) => {
              if (response.status) {
                this._utilsService.showAlert(response.msg, 'Éxito');
                this.getCategorys();
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
