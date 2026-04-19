export const APP_CONFIG = {
  ITEMS_PER_PAGE:    20,
  MAX_CART_QUANTITY: 99,
  LOCALES:           ["vi", "en"] as const,
  DEFAULT_LOCALE:    "vi" as const,
} as const;

export const ORDER_STATUS_LABEL: Record<string, string> = {
  pending:    "Chờ xác nhận",
  confirmed:  "Đã xác nhận",
  processing: "Đang xử lý",
  shipped:    "Đang giao",
  delivered:  "Đã giao",
  cancelled:  "Đã huỷ",
};

export const PAYMENT_METHOD_LABEL: Record<string, string> = {
  cod:     "Thanh toán khi nhận hàng",
  vnpay:   "VNPay",
  momo:    "Momo",
  zalopay: "ZaloPay",
};
