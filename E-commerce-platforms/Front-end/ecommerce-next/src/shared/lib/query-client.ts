import { QueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { ApiError } from "@/shared/lib/errors/api-error";

export function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60_000,
        refetchOnWindowFocus: false,
        retry: (failureCount, error) => {
          if (error instanceof ApiError && error.status < 500) return false;
          return failureCount < 2;
        },
      },
      mutations: {
        onError: (error) => {
          const message =
            error instanceof ApiError
              ? error.message
              : "Đã có lỗi xảy ra, vui lòng thử lại";
          toast.error(message);
        },
      },
    },
  });
}
