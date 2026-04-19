import { AxiosError } from "axios";
import { httpClient } from "../client";
import { ApiError } from "@/shared/lib/errors/api-error";
import { captureError } from "@/shared/lib/monitoring/sentry";
import type { DjangoErrorResponse } from "@/shared/types/api";

httpClient.interceptors.response.use(
  (res) => res,
  (error: AxiosError<DjangoErrorResponse>) => {
    const status  = error.response?.status ?? 0;
    const data    = error.response?.data;
    const message = typeof data?.detail === "string" ? data.detail : "Đã có lỗi xảy ra";

    if (status >= 500) {
      captureError(error, { url: error.config?.url, status });
    }

    return Promise.reject(new ApiError(status, message, data));
  },
);
