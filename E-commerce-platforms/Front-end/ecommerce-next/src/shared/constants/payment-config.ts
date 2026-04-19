export const PAYMENT_CONFIG = {
  VNPAY: {
    VERSION:    "2.1.0",
    COMMAND:    "pay",
    CURRENCY:   "VND",
    LOCALE:     "vn",
    ORDER_TYPE: "other",
    RETURN_URL: `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/vnpay/callback`,
  },
  MOMO: {
    PARTNER_CODE: process.env.MOMO_PARTNER_CODE ?? "",
    REQUEST_TYPE: "payWithMethod",
    REDIRECT_URL: `${process.env.NEXT_PUBLIC_APP_URL}/payment/result`,
    IPN_URL:      `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/momo/webhook`,
    LANG:         "vi",
  },
  ZALOPAY: {
    APP_ID:       process.env.ZALOPAY_APP_ID ?? "",
    EMBED_DATA:   "{}",
    CALLBACK_URL: `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/zalopay/webhook`,
  },
} as const;

export const PAYMENT_LABELS: Record<string, string> = {
  cod:     "Thanh toán khi nhận hàng",
  vnpay:   "VNPay",
  momo:    "Ví MoMo",
  zalopay: "ZaloPay",
};
