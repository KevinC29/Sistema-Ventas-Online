import { Component, OnInit, Inject } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Category } from 'src/app/interfaces/category';

import { CategoryService } from 'src/app/Services/category.service';
import { UtilsService } from 'src/app/reusable/utils.service';

@Component({
  selector: 'app-modal-category',
  templateUrl: './modal-category.component.html',
  styleUrls: ['./modal-category.component.css']
})
export class ModalCategoryComponent implements OnInit {

  form_category: FormGroup;
  titleAction: string = "Agregar";
  buttonAction: string = "Guardar";

  constructor(
    private modalCurrent: MatDialogRef<ModalCategoryComponent>,
    @Inject(MAT_DIALOG_DATA) public dataCategory: Category,
    private fb: FormBuilder,
    private _categoryService: CategoryService,
    private _utilsService: UtilsService
  ) { 
    this.form_category = this.fb.group({
      name: ['', Validators.required],
      desc: ['', Validators.required],
    });

    if(this.dataCategory != null){
      this.titleAction = "Editar";
      this.buttonAction = "Actualizar";
    }

  }

  ngOnInit(): void {
    if(this.dataCategory !=null){
      this.form_category.patchValue({
        name: this.dataCategory.name,
        desc: this.dataCategory.desc,
      });
    }
  }

  saveUpdate_Category(){

    const _category: Category = {
      id: this.dataCategory == null ? '': this.dataCategory.id,
      name: this.form_category.value.name,
      desc: this.form_category.value.desc,
    }

    if(this.dataCategory == null){
      this._categoryService.create(_category).subscribe({
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

      this._categoryService.update(_category.id, _category).subscribe({
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
