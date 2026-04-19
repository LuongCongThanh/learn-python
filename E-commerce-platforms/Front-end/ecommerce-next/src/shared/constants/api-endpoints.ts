export const API = {
  AUTH: {
    LOGIN:    "/api/auth/login/",
    REGISTER: "/api/auth/register/",
    REFRESH:  "/api/auth/token/refresh/",
    LOGOUT:   "/api/auth/logout/",
  },
  PRODUCTS: {
    LIST:       "/api/products/",
    DETAIL:     (slug: string) => `/api/products/${slug}/`,
    CATEGORIES: "/api/categories/",
  },
  ORDERS: {
    LIST:   "/api/orders/",
    DETAIL: (id: string) => `/api/orders/${id}/`,
    CANCEL: (id: string) => `/api/orders/${id}/cancel/`,
  },
  PROFILE: {
    ME:     "/api/auth/me/",
    UPDATE: "/api/auth/me/update/",
  },
  ADMIN: {
    PRODUCTS:        "/api/admin/products/",
    PRODUCT_DETAIL:  (id: string) => `/api/admin/products/${id}/`,
    ORDERS:          "/api/admin/orders/",
    ORDER_DETAIL:    (id: string) => `/api/admin/orders/${id}/`,
    ORDER_STATUS:    (id: string) => `/api/admin/orders/${id}/status/`,
    USERS:           "/api/admin/users/",
    USER_DETAIL:     (id: string) => `/api/admin/users/${id}/`,
    DASHBOARD_STATS: "/api/admin/dashboard/",
  },
} as const;
