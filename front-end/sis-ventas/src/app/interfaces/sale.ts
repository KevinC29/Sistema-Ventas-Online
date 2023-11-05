import { DetSale } from "./det-sale";

export interface Sale {
    id: string;
    date_joined: Date;
    subtotal: number;
    iva: number;
    total: number;
    cli_id: string;
    det: DetSale[];
}
  