import { Component, OnInit, Inject } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Product } from 'src/app/interfaces/product';
import { Category } from 'src/app/interfaces/category';

import { ProductService } from 'src/app/Services/product.service';
import { UtilsService } from 'src/app/reusable/utils.service';
import { CategoryService } from 'src/app/Services/category.service';

@Component({
  selector: 'app-modal-product',
  templateUrl: './modal-product.component.html',
  styleUrls: ['./modal-product.component.css']
})
export class ModalProductComponent implements OnInit{
  form_product: FormGroup;
  titleAction: string = "Agregar";
  buttonAction: string = "Guardar";
  listCategory: Category[] = [];

  constructor(
    private modalCurrent: MatDialogRef<ModalProductComponent>,
    @Inject(MAT_DIALOG_DATA) public dataProduct: Product,
    private fb: FormBuilder,
    private _categoryService: CategoryService,
    private _productService: ProductService,
    private _utilsService: UtilsService
  ) { 

    this.form_product = this.fb.group({
      name: ['', Validators.required],
      image: ['', Validators.required],
      stock: ['', Validators.required],
      pvp: ['', Validators.required],
      cat_id: ['', Validators.required],
    });

    if(this.dataProduct != null){
      this.titleAction = "Editar";
      this.buttonAction = "Actualizar";
    }

    this._categoryService.list().subscribe({
      next: (response) => {
        if(response.status){
          this.listCategory = response.data;
        }
      },
      error: (error) => {
        this._utilsService.showAlert(error, 'Oops');
      }
    })
  }

  ngOnInit(): void {
    if(this.dataProduct !=null){
      this.form_product.patchValue({
        name: this.dataProduct.name,
        image: this.dataProduct.image,
        stock: this.dataProduct.stock,
        pvp: this.dataProduct.pvp,
        cat_id: this.dataProduct.cat_id
      });
    }
  }

  saveUpdate_Product(){
    const _product: Product = {
      id: this.dataProduct == null ? '': this.dataProduct.id,
      name: this.form_product.value.name,
      image: this.form_product.value.image,
      stock: this.form_product.value.stock,
      pvp: this.form_product.value.pvp,
      cat_id: this.form_product.value.cat_id
    }

    if(this.dataProduct == null){
      this._productService.create(_product).subscribe({
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
    }else{

      this._productService.update(_product.id, _product).subscribe({
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
