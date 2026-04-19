export type OrderStatus =
  | "pending"
  | "confirmed"
  | "processing"
  | "shipped"
  | "delivered"
  | "cancelled";

export type PaymentMethod = "cod" | "vnpay" | "momo" | "zalopay";
export type PaymentStatus = "pending" | "paid" | "failed" | "refunded";

export interface OrderItem {
  id:           number;
  product_name: string;
  variant_name: string;
  image:        string;
  price:        number;
  quantity:     number;
  subtotal:     number;
}

export interface Order {
  id:             number;
  code:           string;
  status:         OrderStatus;
  payment_method: PaymentMethod;
  payment_status: PaymentStatus;
  items:          OrderItem[];
  subtotal:       number;
  shipping_fee:   number;
  total:          number;
  address:        string;
  note:           string;
  created_at:     string;
  updated_at:     string;
}
