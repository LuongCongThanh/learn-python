export const ERROR_CODES = {
  TOKEN_INVALID:      "token_not_valid",
  TOKEN_EXPIRED:      "token_expired",
  NOT_AUTHENTICATED:  "not_authenticated",
  PERMISSION_DENIED:  "permission_denied",

  PRODUCT_NOT_FOUND:  "product_not_found",
  OUT_OF_STOCK:       "out_of_stock",
  ORDER_ALREADY_PAID: "order_already_paid",

  FIELD_REQUIRED:     "required",
  INVALID_FORMAT:     "invalid",
  UNIQUE_VIOLATION:   "unique",
} as const;

export type ErrorCode = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];
