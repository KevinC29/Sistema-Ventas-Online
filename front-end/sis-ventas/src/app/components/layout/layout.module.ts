import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LayoutRoutingModule } from './layout-routing.module';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { CategoryComponent } from './pages/category/category.component';
import { ProductComponent } from './pages/product/product.component';
import { SaleComponent } from './pages/sale/sale.component';
import { ClientComponent } from './pages/client/client.component';
import { UserComponent } from './pages/user/user.component';
import { SharedModule } from 'src/app/reusable/shared/shared.module';
import { ModalClientComponent } from './modales/modal-client/modal-client.component';
import { ModalCategoryComponent } from './modales/modal-category/modal-category.component';
import { ModalProductComponent } from './modales/modal-product/modal-product.component';
import { ModalUserComponent } from './modales/modal-user/modal-user.component';


@NgModule({
  declarations: [
    DashboardComponent,
    CategoryComponent,
    ProductComponent,
    SaleComponent,
    ClientComponent,
    ModalClientComponent,
    ModalProductComponent,
    ModalCategoryComponent,
    ModalUserComponent,
    UserComponent,
  ],
  imports: [
    CommonModule,
    LayoutRoutingModule,
    SharedModule
  ]
})
export class LayoutModule { }
