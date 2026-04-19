import axios from "axios";

export const httpClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  timeout: 10_000,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});
