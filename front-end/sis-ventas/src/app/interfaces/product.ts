export interface Product {
    id: string;
    name: string;
    image?: string | null;
    stock: number;
    pvp: number;
    cat_id: string;
}
