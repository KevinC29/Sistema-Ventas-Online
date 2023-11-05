export interface Client {
    id: string;
    names: string;
    surnames: string;
    dni: string;
    address: string;
    gender: 'male' | 'female' | 'other';
    balance: number;
}
