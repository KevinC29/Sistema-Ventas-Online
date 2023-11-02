import { Category } from './category.model';	

export interface Product {
    id: string;
    name: string;
    image: string;
    stock: number;
    pvp: number;
    cat: Category;
}

// export interface Product {
//     id: number;
//     title: string;
//     price: number;
//     images: string[];
// }
