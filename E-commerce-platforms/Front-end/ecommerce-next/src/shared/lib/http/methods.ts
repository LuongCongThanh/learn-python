import { httpClient } from "./client";

export const http = {
  get: <T>(url: string, params?: object) =>
    httpClient.get<T>(url, { params }).then((r) => r.data),

  post: <T>(url: string, body?: unknown) =>
    httpClient.post<T>(url, body).then((r) => r.data),

  put: <T>(url: string, body?: unknown) =>
    httpClient.put<T>(url, body).then((r) => r.data),

  patch: <T>(url: string, body?: unknown) =>
    httpClient.patch<T>(url, body).then((r) => r.data),

  delete: <T>(url: string) =>
    httpClient.delete<T>(url).then((r) => r.data),
};
