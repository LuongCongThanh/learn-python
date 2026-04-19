import { http, HttpResponse } from "msw";
import { API } from "@/shared/constants/api-endpoints";

export const handlers = [
  http.post(API.AUTH.LOGIN, () =>
    HttpResponse.json({ access: "mock-access", refresh: "mock-refresh" }),
  ),
  http.post(API.AUTH.LOGOUT, () =>
    HttpResponse.json({ detail: "Logged out" }),
  ),
  http.post(API.AUTH.REFRESH, () =>
    HttpResponse.json({ access: "new-mock-access" }),
  ),
  http.get(API.PRODUCTS.LIST, () =>
    HttpResponse.json({ results: [], count: 0, next: null, previous: null }),
  ),
  http.get(API.ORDERS.LIST, () =>
    HttpResponse.json({ results: [], count: 0 }),
  ),
];
