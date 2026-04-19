import { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { httpClient } from "../client";
import { useAuthStore } from "@/shared/stores/auth-store";
import { API } from "@/shared/constants/api-endpoints";
import { http } from "../methods";

let refreshPromise: Promise<string> | null = null;

httpClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

httpClient.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;

      if (!refreshPromise) {
        refreshPromise = http.post<string>(API.AUTH.REFRESH).finally(() => {
          refreshPromise = null;
        });
      }

      try {
        const newToken = await refreshPromise;
        useAuthStore.getState().setAccessToken(newToken);
        original.headers.Authorization = `Bearer ${newToken}`;
        return httpClient(original);
      } catch {
        useAuthStore.getState().clearAuth();
        window.location.href = "/vi/login";
      }
    }

    return Promise.reject(error);
  },
);
