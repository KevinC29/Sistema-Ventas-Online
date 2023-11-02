import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Product } from './models/product.model';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'sis-ventasKC';
  
  // products = [{"id": "2efd704b-4eb6-4de6-8006-2701e3838a3d", "name": "Product 1", "image": "URL_imagen_1", "stock": 10, "pvp": 49.99, "cat": {"id": "5dc575cd-0d7a-4216-a481-ba9dbfd5c8e5", "name": "Carnes", "desc": "Cualquier tipo de carne"}}, {"id": "28b95d48-059f-4016-8d02-388aaf2eca05", "name": "Product 2", "image": "URL_imagen_2", "stock": 10, "pvp": 49.99, "cat": {"id": "9efecf6c-dc4d-45ff-a499-5374be0bf267", "name": "Frituras", "desc": "Cualquier tipo de marisco"}}, {"id": "b5c9198c-7c33-4f18-abb1-d30dc4575da4", "name": "Product 3", "image": "URL_imagen_3", "stock": 10, "pvp": 49.99, "cat": {"id": "9efecf6c-dc4d-45ff-a499-5374be0bf267", "name": "Frituras", "desc": "Cualquier tipo de marisco"}}];

  changeTitle() {
    this.title = 'Changed title';
  }
  products: Product[] = [];
  constructor(private http: HttpClient) {}
  ngOnInit() {
    this.http.get<Product[]>('http://localhost:6543/product/list/')
      .subscribe((data) => {
        console.log('Tipo de datos en data:', typeof data);
        if (Array.isArray(data)) {
          console.log('Es un array');
        }
        this.products = data;
        console.log('Datos recuperados:', this.products);
    },
    (error) => {
      console.error('Hubo un error al recuperar los datos:', error);
      // Podrías asignar un valor predeterminado a this.products o mostrar un mensaje de error al usuario
    });
  }
  
}
