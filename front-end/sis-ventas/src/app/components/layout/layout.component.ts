import { Component, OnInit } from '@angular/core';

import { Router } from '@angular/router';	
import { Menu } from 'src/app/interfaces/menu';

import { UtilsService } from 'src/app/reusable/utils.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.css']
})
export class LayoutComponent implements OnInit{

  listaMenu: Menu[] = [];
  nameUser: string = '';
  rolUser: string = '';

  constructor(
    private router: Router, 
    private _utilsService: UtilsService) 
  { 

  }  

  ngOnInit(): void {
    const user = this._utilsService.getSesionUser();
    if (user != null){
      this.nameUser = user.name;
      this.rolUser = user.role;


      const dashboard_page: Menu = 
      {
        url: '/pages/dashboard',
        name: 'Dashboard',
        icono: 'dashboard'
      }
      const user_page: Menu = {
        url: '/pages/user',
        name: 'Usuarios',
        icono: 'people'
      }
  
      const client_page: Menu = {
        url: '/pages/client',
        name: 'Clientes',
        icono: 'people'
      }
  
      const category_page: Menu = {
        url: '/pages/category',
        name: 'Categorias',
        icono: 'category'
      }
  
      const product_page: Menu = {
        url: '/pages/product',
        name: 'Productos',
        icono: 'shopping_cart'
      }
  
      const sale_page: Menu = {
        url: '/pages/sale',
        name: 'Ventas',
        icono: 'currency_exchange'
      }
    
      if (this.rolUser ==='editor'){
        this.listaMenu = [dashboard_page, user_page, client_page, category_page, product_page, sale_page]
      }else{
        this.listaMenu = [client_page, sale_page]
      }
    }
  }

  closeSesion(){
    this._utilsService.deleteSesionUser();
    this.router.navigate(['/login']);
  }

}
