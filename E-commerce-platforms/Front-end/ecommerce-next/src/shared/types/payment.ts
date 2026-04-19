export type PaymentMethod = "cod" | "vnpay" | "momo" | "zalopay";
export type PaymentStatus = "pending" | "paid" | "failed" | "refunded";

export interface PaymentResult {
  orderId:        string;
  transactionId:  string;
  amount:         number;
  status:         "success" | "failed" | "pending";
  method:         PaymentMethod;
  message?:       string;
  paidAt?:        string;
}

export interface CheckoutPayload {
  cartItems: Array<{ productId: number; quantity: number }>;
  shippingAddress: {
    fullName: string;
    phone:    string;
    address:  string;
    city:     string;
  };
  paymentMethod: PaymentMethod;
  note?:         string;
}
