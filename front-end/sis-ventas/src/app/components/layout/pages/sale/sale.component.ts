import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';

import { ProductService } from 'src/app/Services/product.service';
import { ClientService } from 'src/app/Services/client.service';
import { SaleService } from 'src/app/Services/sale.service';
import { UtilsService } from 'src/app/reusable/utils.service';

import { Product } from 'src/app/interfaces/product';
import { Client } from 'src/app/interfaces/client';
import { DetSale } from 'src/app/interfaces/det-sale';
import { Sale } from 'src/app/interfaces/sale';

import Swal from 'sweetalert2';

@Component({
  selector: 'app-sale',
  templateUrl: './sale.component.html',
  styleUrls: ['./sale.component.css']
})
export class SaleComponent implements OnInit{

  listProducts: Product[] = [];
  listClients: Client[] = [];
  listProductFilter: Product[] = [];
  listDetSale: DetSale[] = [];
  blockBottonRegister: boolean = false;

  productSelected!: Product;
  clientSelected!: Client;
  subtotalSale: number = 0;
  total: number = 0;
  iva_total: number = 0;
  date: Date = new Date();

  form_data_sale: FormGroup;
  form_product_sale: FormGroup;

  columnsTable: string[] = ['producto', 'precio', 'cantidad', 'subtotal', 'accion'];
  dataSale = new MatTableDataSource(this.listDetSale);

  returnProductFilter(filter:any):Product[]{
    const valueFilter = typeof filter === 'string' ? filter.toLowerCase() : filter.name.toLowerCase();
    return this.listProducts.filter(product => product.name.toLowerCase().includes(valueFilter));
  }

  constructor(
    private fb: FormBuilder,
    private _productService: ProductService,
    private _clientService: ClientService,
    private _saleService: SaleService,
    private _utilsService: UtilsService
  ){
    this.form_data_sale = this.fb.group({
      data_joined: ['', Validators.required],
      cli_id: ['', Validators.required],
      iva: ['', Validators.required],
    });

    this.form_product_sale = this.fb.group({
      prod_id: ['', Validators.required],
      cant: ['', Validators.required]
    });

    this._productService.list().subscribe({
      next:(response) => {
        if(response.status){
          const list = response.data as Product[];
          this.listProducts = list.filter(product => product.stock > 0);
        }
      },
      error:(error) => {
        this._utilsService.showAlert('error', 'Oops');
      }
    })

    this._clientService.list().subscribe({
      next: (response) => {
        if(response.status){
          this.listClients = response.data;
        }
      },
      error: (error) => {
        this._utilsService.showAlert('error', 'Oops');
      }
    })

    this.form_product_sale.get('prod_id')?.valueChanges.subscribe(value=>{
      this.listProductFilter = this.returnProductFilter(value);
    });
  }


  ngOnInit(): void {
  }

  onInputChange(event: any) {
    const enteredValue: number = event.target.valueAsNumber;
    if (enteredValue % 1 !== 0) {
      event.target.value = Math.round(enteredValue);
    }
  }

  showProductFilter(product: Product){
    return product.name;
  }

  getClientFilter(id: String){
    const cliente = this.listClients.find(client => client.id === id);
    return cliente ? cliente.balance : undefined;
  }

  productForSale(event:any){
    this.productSelected = event.option.value;
  }

  showProductName(id:String){
    const productFound = this.listProductFilter.find(producto => producto.id === id);
    return productFound ? productFound.name : undefined;
  }

  addDetSale(){

    if (this.productSelected.stock < this.form_product_sale.value.cant){
      return this._utilsService.showAlert("No hay suficiente stock", 'Error');
    }
    const _cant:number = this.form_product_sale.value.cant;
    const _price:number = this.productSelected.pvp;
    const _subtotal:number = +(_cant * _price).toFixed(2);
    this.subtotalSale += +_subtotal.toFixed(2);

    this.iva_total = (this.form_data_sale.value.iva * this.subtotalSale)/100;
    this.total = +(this.iva_total + this.subtotalSale).toFixed(2);
    
    this.listDetSale.push({
      id:'',
      prod_id: this.productSelected.id,
      price: _price,
      cant: _cant,
      subtotal: _subtotal
    });

    this.dataSale = new MatTableDataSource(this.listDetSale);

    this.form_product_sale.patchValue({
      prod_id: '',
      cant: ''
    });

    console.log(this.listDetSale)
  };

  deleteDetSale(detSale: DetSale){
    this.total -= detSale.subtotal,
    this.listDetSale = this.listDetSale.filter(det => det.prod_id !== detSale.prod_id);
    this.dataSale = new MatTableDataSource(this.listDetSale);
    
  }

  registerSale(){
    this.blockBottonRegister = false;
    this.iva_total = (this.form_data_sale.value.iva * this.subtotalSale)/100;
    this.total = +(this.iva_total + this.subtotalSale).toFixed(2);
    const clientBalance = this.getClientFilter(this.form_data_sale.value.cli_id);

    if(clientBalance === undefined){
      return this._utilsService.showAlert("El cliente no existe", 'Error');
    }
    
    if(this.listDetSale.length > 0 && clientBalance >= this.total){
        const sale: Sale = {
        id: '',
        date_joined: this.form_data_sale.value.data_joined,
        subtotal: +(this.subtotalSale).toFixed(2),
        iva: +(this.form_data_sale.value.iva).toFixed(2),
        total: this.total,
        cli_id: this.form_data_sale.value.cli_id,
        det: this.listDetSale
      }

      console.log(sale);

      this._saleService.create(sale).subscribe({
        next: (response) => {
          if(response.status){
            this.subtotalSale = 0.00;
            this.iva_total = 0.00;
            this.total = 0.00;
            this.listDetSale = [];
            this.form_data_sale.reset();
            this.dataSale = new MatTableDataSource(this.listDetSale);

            Swal.fire({
              icon: 'success',
              title: 'Venta Registrada',
              text: `${response.msg}: ${response.data.id}`,
            })
            this.blockBottonRegister = true;
          }else
            this._utilsService.showAlert("Venta Denegada", 'Error');

        },
        complete: () => {
          this.blockBottonRegister = false;
        },
        error: (error) => {
          this._utilsService.showAlert('error', 'Oops');
        }
      })
    }else{
      if(clientBalance < this.total)
        this._utilsService.showAlert("El cliente no tiene suficiente saldo", 'Error');
    }
  }
}
