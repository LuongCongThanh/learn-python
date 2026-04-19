# Setup Guide — E-Commerce Next.js

> Tài liệu liên quan: [architecture.md](./architecture.md) · [design-system.md](./design-system.md) · [frontend-guidelines.md](./frontend-guidelines.md)

---

## 1. Khởi tạo project

```bash
npx create-next-app@latest ecommerce-next \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-eslint

cd ecommerce-next
```

---

## 2. Cài đặt thư viện

### 2.1 Core & Infrastructure

```bash
npm install \
  next-intl \
  server-only \
  client-only
```

### 2.2 Data Fetching & State

```bash
npm install \
  @tanstack/react-query \
  @tanstack/react-query-devtools \
  zustand \
  axios
```

### 2.3 Form & Validation

```bash
npm install \
  react-hook-form \
  zod \
  @hookform/resolvers
```

### 2.4 UI Components

```bash
# Shadcn/UI — init trước, add component sau
npx shadcn@latest init

# Add components
npx shadcn@latest add \
  button input label textarea select checkbox \
  dialog sheet dropdown-menu popover \
  table badge skeleton card avatar \
  form alert separator scroll-area \
  tooltip command
```

### 2.5 UI & Animation

```bash
npm install \
  lucide-react \
  framer-motion \
  sonner \
  vaul \
  next-nprogress-bar \
  next-themes \
  react-error-boundary \
  @tiptap/react \
  @tiptap/starter-kit \
  @tiptap/extension-image \
  @tiptap/extension-link
```

### 2.6 Data Table (Admin)

```bash
npm install @tanstack/react-table
```

### 2.7 Utilities

```bash
npm install \
  date-fns \
  http-status-codes \
  clsx \
  tailwind-merge
```

### 2.8 PWA

```bash
npm install @ducanh2912/next-pwa
```

### 2.9 Monitoring

```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

### 2.10 Testing

```bash
# Vitest + Testing Library
npm install -D \
  vitest \
  @vitejs/plugin-react \
  vite-tsconfig-paths \
  @testing-library/react \
  @testing-library/jest-dom \
  @testing-library/user-event \
  jsdom

# MSW — mock API trong test
npm install -D msw

# Playwright — E2E
npm install -D @playwright/test
npx playwright install
```

### 2.11 Code Quality

```bash
npm install -D \
  eslint \
  eslint-config-next \
  prettier \
  eslint-config-prettier \
  husky \
  lint-staged \
  @next/bundle-analyzer
```

### 2.12 Bundle phân tích

```bash
npm install -D @next/bundle-analyzer
```

---

## 3. Tất cả trong 1 lệnh (Production deps)

```bash
npm install \
  next-intl \
  server-only \
  client-only \
  @tanstack/react-query \
  @tanstack/react-query-devtools \
  @tanstack/react-table \
  zustand \
  axios \
  react-hook-form \
  zod \
  @hookform/resolvers \
  lucide-react \
  framer-motion \
  sonner \
  vaul \
  next-nprogress-bar \
  next-themes \
  react-error-boundary \
  @tiptap/react \
  @tiptap/starter-kit \
  @tiptap/extension-image \
  @tiptap/extension-link \
  date-fns \
  http-status-codes \
  clsx \
  tailwind-merge \
  @ducanh2912/next-pwa \
  @sentry/nextjs
```

```bash
npm install -D \
  vitest \
  @vitejs/plugin-react \
  vite-tsconfig-paths \
  @testing-library/react \
  @testing-library/jest-dom \
  @testing-library/user-event \
  jsdom \
  msw \
  @playwright/test \
  eslint \
  eslint-config-next \
  prettier \
  eslint-config-prettier \
  husky \
  lint-staged \
  @next/bundle-analyzer
```

---

## 4. Tạo folder structure

```bash
# ── app/ ────────────────────────────────────────────────────────────────────

# (auth)
mkdir -p src/app/\[locale\]/\(auth\)/_components
mkdir -p src/app/\[locale\]/\(auth\)/_lib
mkdir -p src/app/\[locale\]/\(auth\)/login
mkdir -p src/app/\[locale\]/\(auth\)/register
mkdir -p src/app/\[locale\]/\(auth\)/forgot-password

# (shop)
mkdir -p src/app/\[locale\]/\(shop\)/_components
mkdir -p src/app/\[locale\]/\(shop\)/_lib
mkdir -p src/app/\[locale\]/\(shop\)/products/\[slug\]
mkdir -p src/app/\[locale\]/\(shop\)/cart
mkdir -p src/app/\[locale\]/\(shop\)/checkout/success
mkdir -p src/app/\[locale\]/\(shop\)/orders/\[id\]
mkdir -p src/app/\[locale\]/\(shop\)/profile

# (admin)
mkdir -p src/app/\[locale\]/\(admin\)/_components
mkdir -p src/app/\[locale\]/\(admin\)/_lib
mkdir -p src/app/\[locale\]/\(admin\)/dashboard
mkdir -p src/app/\[locale\]/\(admin\)/products/_lib
mkdir -p src/app/\[locale\]/\(admin\)/products/new
mkdir -p src/app/\[locale\]/\(admin\)/products/\[id\]
mkdir -p src/app/\[locale\]/\(admin\)/orders/_lib
mkdir -p src/app/\[locale\]/\(admin\)/orders/\[id\]
mkdir -p src/app/\[locale\]/\(admin\)/users/\[id\]
mkdir -p src/app/\[locale\]/\(admin\)/categories

# api/
mkdir -p src/app/api/auth/login
mkdir -p src/app/api/auth/register
mkdir -p src/app/api/auth/logout
mkdir -p src/app/api/auth/refresh
mkdir -p src/app/api/payment/vnpay/create
mkdir -p src/app/api/payment/vnpay/callback
mkdir -p src/app/api/payment/momo/create
mkdir -p src/app/api/payment/momo/callback
mkdir -p src/app/api/payment/zalopay/create
mkdir -p src/app/api/payment/zalopay/callback
mkdir -p src/app/api/payment/cod/confirm

# ── shared/ ──────────────────────────────────────────────────────────────────
mkdir -p src/shared/components/ui
mkdir -p src/shared/components/layouts
mkdir -p src/shared/components/skeletons
mkdir -p src/shared/hooks
mkdir -p src/shared/lib/http/interceptors
mkdir -p src/shared/lib/payment
mkdir -p src/shared/lib/errors
mkdir -p src/shared/lib/guards
mkdir -p src/shared/lib/monitoring
mkdir -p src/shared/lib/pwa
mkdir -p src/shared/stores
mkdir -p src/shared/types
mkdir -p src/shared/constants

# ── tests/ ───────────────────────────────────────────────────────────────────
mkdir -p src/__tests__/helpers
mkdir -p src/__tests__/integration

# ── messages/ ────────────────────────────────────────────────────────────────
mkdir -p src/messages

# ── e2e/ ─────────────────────────────────────────────────────────────────────
mkdir -p e2e

# ── public/ ──────────────────────────────────────────────────────────────────
mkdir -p public/images
mkdir -p public/icons
```

---

## 5. Tạo các file cơ bản

```bash
# ── shared/lib ───────────────────────────────────────────────────────────────
touch src/shared/lib/env.ts
touch src/shared/lib/utils.ts
touch src/shared/lib/query-client.ts
touch src/shared/lib/http/client.ts
touch src/shared/lib/http/methods.ts
touch src/shared/lib/http/interceptors/auth.interceptor.ts
touch src/shared/lib/http/interceptors/error.interceptor.ts
touch src/shared/lib/errors/api-error.ts
touch src/shared/lib/errors/error-codes.ts
touch src/shared/lib/guards/auth-guard.tsx
touch src/shared/lib/monitoring/sentry.ts
touch src/shared/lib/pwa/register-sw.ts
touch src/shared/lib/payment/vnpay.ts
touch src/shared/lib/payment/momo.ts
touch src/shared/lib/payment/zalopay.ts

# ── shared/stores ─────────────────────────────────────────────────────────────
touch src/shared/stores/cart-store.ts
touch src/shared/stores/auth-store.ts

# ── shared/types ──────────────────────────────────────────────────────────────
touch src/shared/types/product.ts
touch src/shared/types/order.ts
touch src/shared/types/user.ts
touch src/shared/types/payment.ts
touch src/shared/types/api.ts

# ── shared/constants ──────────────────────────────────────────────────────────
touch src/shared/constants/api-endpoints.ts
touch src/shared/constants/payment-config.ts
touch src/shared/constants/app-config.ts

# ── shared/hooks ──────────────────────────────────────────────────────────────
touch src/shared/hooks/use-debounce.ts
touch src/shared/hooks/use-local-storage.ts
touch src/shared/hooks/use-media-query.ts

# ── shared/components ────────────────────────────────────────────────────────
touch src/shared/components/layouts/header.tsx
touch src/shared/components/layouts/footer.tsx
touch src/shared/components/skeletons/product-card-skeleton.tsx
touch src/shared/components/skeletons/product-grid-skeleton.tsx
touch src/shared/components/skeletons/order-list-skeleton.tsx
touch src/shared/components/rich-text-editor.tsx

# ── messages ─────────────────────────────────────────────────────────────────
touch src/messages/vi.json
touch src/messages/en.json

# ── tests ────────────────────────────────────────────────────────────────────
touch src/__tests__/setup.ts
touch src/__tests__/helpers/render.tsx
touch src/__tests__/helpers/mock-handlers.ts

# ── root ─────────────────────────────────────────────────────────────────────
touch public/manifest.json
touch .env.example
```

---

## 6. Config các file quan trọng

### `tsconfig.json` — thêm path alias

```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### `.env.example` — template biến môi trường

```bash
# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Django API (server-side only)
DJANGO_API_URL=http://localhost:8000

# VNPay
VNPAY_TMN_CODE=
VNPAY_HASH_SECRET=
VNPAY_URL=https://sandbox.vnpayment.vn/paymentv2/vpcpay.html
VNPAY_RETURN_URL=${NEXT_PUBLIC_APP_URL}/api/payment/vnpay/callback

# Momo
MOMO_PARTNER_CODE=
MOMO_ACCESS_KEY=
MOMO_SECRET_KEY=
MOMO_ENDPOINT=https://test-payment.momo.vn/v2/gateway/api/create

# ZaloPay
ZALOPAY_APP_ID=
ZALOPAY_KEY1=
ZALOPAY_KEY2=
ZALOPAY_ENDPOINT=https://sb-openapi.zalopay.vn/v2/create

# Sentry
SENTRY_DSN=
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_AUTH_TOKEN=
```

### `vitest.config.ts`

```typescript
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/__tests__/setup.ts"],
    globals: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      include: ["src/shared/lib/**", "src/shared/utils/**"],
      thresholds: { lines: 70, functions: 70, branches: 70 },
    },
  },
});
```

### `eslint.config.mjs`

```js
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({ baseDirectory: __dirname });

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript", "prettier"),
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_" },
      ],
    },
  },
];

export default eslintConfig;
```

### `.prettierrc`

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

> Cần cài thêm: `npm install -D prettier-plugin-tailwindcss`

### `package.json` — thêm scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "analyze": "ANALYZE=true next build",
    "prepare": "husky"
  }
}
```

### Husky + lint-staged

```bash
# Init husky
npx husky init

# Pre-commit hook
echo "npx lint-staged" > .husky/pre-commit
```

Thêm vào `package.json`:

```json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

---

## 7. Nội dung các file cốt lõi

### 7.1 `next.config.ts`

```typescript
import type { NextConfig } from "next";
import withBundleAnalyzer from "@next/bundle-analyzer";
import withPWA from "@ducanh2912/next-pwa";

const withAnalyzer = withBundleAnalyzer({
  enabled: process.env.ANALYZE === "true",
});

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**.amazonaws.com" }, // S3
      { protocol: "http", hostname: "localhost" },
    ],
  },
};

export default withAnalyzer(
  withPWA({
    dest: "public",
    disable: process.env.NODE_ENV === "development",
    register: true,
    skipWaiting: true,
    cacheOnFrontEndNav: true,
    reloadOnOnline: true,
  })(nextConfig),
);
```

---

### 7.2 `middleware.ts`

```typescript
import createMiddleware from "next-intl/middleware";
import { NextRequest, NextResponse } from "next/server";

const intlMiddleware = createMiddleware({
  locales: ["vi", "en"],
  defaultLocale: "vi",
});

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Auth guard cho /admin — kiểm tra cookie, không phụ thuộc JS client
  if (pathname.match(/^\/(vi|en)\/admin/)) {
    const token = request.cookies.get("access_token");
    if (!token) {
      return NextResponse.redirect(new URL("/vi/login", request.url));
    }
  }

  return intlMiddleware(request);
}

export const config = {
  matcher: ["/((?!api|_next|.*\\..*).*)"],
};
```

---

### 7.3 `src/app/layout.tsx`

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin", "vietnamese"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: { default: "E-Commerce Shop", template: "%s | E-Commerce Shop" },
  description: "Mua sắm trực tuyến nhanh chóng, tiện lợi",
  manifest: "/manifest.json",
  themeColor: "#e85d04",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "E-Commerce Shop",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" suppressHydrationWarning className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

---

### 7.4 `src/app/providers.tsx`

```tsx
"use client";
import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";
import { AppProgressBar } from "next-nprogress-bar";
import { makeQueryClient } from "@/shared/lib/query-client";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => makeQueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="light"
        enableSystem={false}
      >
        {children}
        <Toaster richColors position="top-right" />
        <AppProgressBar
          color="#e85d04"
          height="2px"
          options={{ showSpinner: false }}
        />
        <ReactQueryDevtools initialIsOpen={false} />
      </ThemeProvider>
    </QueryClientProvider>
  );
}
```

---

### 7.5 `src/app/[locale]/layout.tsx`

```tsx
import { notFound } from "next/navigation";
import { getMessages, setRequestLocale } from "next-intl/server";
import { NextIntlClientProvider } from "next-intl";
import { Providers } from "@/app/providers";

const locales = ["vi", "en"];

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  if (!locales.includes(locale)) notFound();

  setRequestLocale(locale);
  const messages = await getMessages();

  return (
    <NextIntlClientProvider messages={messages}>
      <Providers>{children}</Providers>
    </NextIntlClientProvider>
  );
}
```

---

### 7.6 `src/shared/lib/env.ts`

```typescript
import { z } from "zod";

const envSchema = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url(),
  NEXT_PUBLIC_API_URL: z.string().url(),
  DJANGO_API_URL: z.string().url().optional(),
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),

  // VNPay
  VNPAY_TMN_CODE: z.string().optional(),
  VNPAY_HASH_SECRET: z.string().optional(),
  VNPAY_URL: z.string().url().optional(),

  // Momo
  MOMO_PARTNER_CODE: z.string().optional(),
  MOMO_ACCESS_KEY: z.string().optional(),
  MOMO_SECRET_KEY: z.string().optional(),

  // ZaloPay
  ZALOPAY_APP_ID: z.string().optional(),
  ZALOPAY_KEY1: z.string().optional(),
  ZALOPAY_KEY2: z.string().optional(),

  // Sentry
  NEXT_PUBLIC_SENTRY_DSN: z.string().optional(),
});

export const env = envSchema.parse(process.env);
```

---

### 7.7 `src/shared/lib/utils.ts`

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { format } from "date-fns";
import { vi } from "date-fns/locale";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
  }).format(amount);
}

export function formatDate(date: string | Date): string {
  return format(new Date(date), "dd/MM/yyyy", { locale: vi });
}

export function formatDateTime(date: string | Date): string {
  return format(new Date(date), "HH:mm dd/MM/yyyy", { locale: vi });
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}
```

---

### 7.8 `src/shared/lib/query-client.ts`

```typescript
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
```

---

### 7.9 `src/shared/lib/http/client.ts`

```typescript
import axios from "axios";
import { env } from "@/shared/lib/env";

export const httpClient = axios.create({
  baseURL: env.NEXT_PUBLIC_API_URL,
  timeout: 10_000,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});
```

---

### 7.10 `src/shared/lib/http/methods.ts`

```typescript
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

  delete: <T>(url: string) => httpClient.delete<T>(url).then((r) => r.data),
};
```

---

### 7.11 `src/shared/lib/http/interceptors/auth.interceptor.ts`

```typescript
import { AxiosError, AxiosRequestConfig } from "axios";
import { httpClient } from "../client";
import { useAuthStore } from "@/shared/stores/auth-store";
import { API } from "@/shared/constants/api-endpoints";
import { http } from "../methods";

let refreshPromise: Promise<string> | null = null; // mutex — tránh race condition

httpClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

httpClient.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const original = error.config as AxiosRequestConfig & { _retry?: boolean };

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
        original.headers!.Authorization = `Bearer ${newToken}`;
        return httpClient(original);
      } catch {
        useAuthStore.getState().clearAuth();
        window.location.href = "/vi/login";
      }
    }

    return Promise.reject(error);
  },
);
```

---

### 7.12 `src/shared/lib/http/interceptors/error.interceptor.ts`

```typescript
import { AxiosError } from "axios";
import { httpClient } from "../client";
import { ApiError } from "@/shared/lib/errors/api-error";
import { captureError } from "@/shared/lib/monitoring/sentry";
import type { DjangoErrorResponse } from "@/shared/types/api";

httpClient.interceptors.response.use(
  (res) => res,
  (error: AxiosError<DjangoErrorResponse>) => {
    const status = error.response?.status ?? 0;
    const data = error.response?.data;
    const message =
      typeof data?.detail === "string" ? data.detail : "Đã có lỗi xảy ra";

    if (status >= 500) {
      captureError(error, { url: error.config?.url, status });
    }

    return Promise.reject(new ApiError(status, message, data));
  },
);
```

---

### 7.13 `src/shared/lib/errors/api-error.ts`

```typescript
export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
    public readonly data?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }

  get isUnauthorized() {
    return this.status === 401;
  }
  get isForbidden() {
    return this.status === 403;
  }
  get isNotFound() {
    return this.status === 404;
  }
  get isValidation() {
    return this.status === 400 || this.status === 422;
  }
  get isServerError() {
    return this.status >= 500;
  }
}
```

---

### 7.14 `src/shared/lib/errors/error-codes.ts`

```typescript
export const ERROR_CODES = {
  // Django SimpleJWT
  TOKEN_INVALID: "token_not_valid",
  TOKEN_EXPIRED: "token_expired",
  NOT_AUTHENTICATED: "not_authenticated",
  PERMISSION_DENIED: "permission_denied",

  // Business logic
  PRODUCT_NOT_FOUND: "product_not_found",
  OUT_OF_STOCK: "out_of_stock",
  ORDER_ALREADY_PAID: "order_already_paid",

  // DRF validation
  FIELD_REQUIRED: "required",
  INVALID_FORMAT: "invalid",
  UNIQUE_VIOLATION: "unique",
} as const;

export type ErrorCode = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];
```

---

### 7.15 `src/shared/lib/monitoring/sentry.ts`

```typescript
import * as Sentry from "@sentry/nextjs";

export function captureError(
  error: unknown,
  context?: Record<string, unknown>,
) {
  if (process.env.NODE_ENV === "production") {
    Sentry.captureException(error, { extra: context });
  } else {
    console.error("[Dev Error]", error, context);
  }
}

export function captureMessage(
  message: string,
  level: Sentry.SeverityLevel = "info",
) {
  if (process.env.NODE_ENV === "production") {
    Sentry.captureMessage(message, level);
  }
}
```

---

### 7.16 `src/shared/lib/guards/auth-guard.tsx`

```tsx
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/shared/stores/auth-store";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => !!s.accessToken);

  useEffect(() => {
    if (!isAuthenticated) router.replace("/vi/login");
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;
  return <>{children}</>;
}
```

---

### 7.17 `src/shared/stores/auth-store.ts`

```typescript
import { create } from "zustand";
import { subscribeWithSelector, persist } from "zustand/middleware";

interface AuthState {
  accessToken: string | null;
  user: AuthUser | null;
}

interface AuthUser {
  id: number;
  email: string;
  name: string;
  is_staff: boolean;
}

interface AuthActions {
  setAccessToken: (token: string) => void;
  setUser: (user: AuthUser) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  subscribeWithSelector(
    persist(
      (set) => ({
        accessToken: null,
        user: null,
        setAccessToken: (token) => set({ accessToken: token }),
        setUser: (user) => set({ user }),
        clearAuth: () => set({ accessToken: null, user: null }),
      }),
      { name: "auth-storage", partialize: (state) => ({ user: state.user }) },
    ),
  ),
);
```

---

### 7.18 `src/shared/stores/cart-store.ts`

```typescript
import { create } from "zustand";
import { subscribeWithSelector, persist } from "zustand/middleware";

export interface CartItem {
  variantId: string;
  productId: string;
  name: string;
  image: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
  itemCount: number;
}

interface CartActions {
  addToCart: (item: CartItem) => void;
  removeCartItem: (variantId: string) => void;
  updateQuantity: (variantId: string, quantity: number) => void;
  clearCart: () => void;
}

function calcTotal(items: CartItem[]) {
  return items.reduce((s, i) => s + i.price * i.quantity, 0);
}
function calcItemCount(items: CartItem[]) {
  return items.reduce((s, i) => s + i.quantity, 0);
}

export const useCartStore = create<CartState & CartActions>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        items: [],
        total: 0,
        itemCount: 0,

        addToCart: (item) => {
          const items = get().items;
          const existing = items.find((i) => i.variantId === item.variantId);
          const updated = existing
            ? items.map((i) =>
                i.variantId === item.variantId
                  ? { ...i, quantity: i.quantity + item.quantity }
                  : i,
              )
            : [...items, item];
          set({
            items: updated,
            total: calcTotal(updated),
            itemCount: calcItemCount(updated),
          });
        },

        removeCartItem: (variantId) => {
          const updated = get().items.filter((i) => i.variantId !== variantId);
          set({
            items: updated,
            total: calcTotal(updated),
            itemCount: calcItemCount(updated),
          });
        },

        updateQuantity: (variantId, quantity) => {
          const updated = get().items.map((i) =>
            i.variantId === variantId ? { ...i, quantity } : i,
          );
          set({
            items: updated,
            total: calcTotal(updated),
            itemCount: calcItemCount(updated),
          });
        },

        clearCart: () => set({ items: [], total: 0, itemCount: 0 }),
      }),
      { name: "cart-storage" },
    ),
  ),
);
```

---

### 7.19 `src/shared/types/api.ts`

```typescript
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface DjangoErrorResponse {
  detail?: string;
  code?: string;
  [field: string]: string | string[] | undefined;
}
```

---

### 7.20 `src/shared/types/order.ts`

```typescript
export type OrderStatus =
  | "pending"
  | "confirmed"
  | "processing"
  | "shipped"
  | "delivered"
  | "cancelled";

export type PaymentMethod = "cod" | "vnpay" | "momo" | "zalopay";

export type PaymentStatus = "pending" | "paid" | "failed" | "refunded";

export interface OrderItem {
  id: number;
  product_name: string;
  variant_name: string;
  image: string;
  price: number;
  quantity: number;
  subtotal: number;
}

export interface Order {
  id: number;
  code: string;
  status: OrderStatus;
  payment_method: PaymentMethod;
  payment_status: PaymentStatus;
  items: OrderItem[];
  subtotal: number;
  shipping_fee: number;
  total: number;
  address: string;
  note: string;
  created_at: string;
  updated_at: string;
}
```

---

### 7.21 `src/shared/constants/api-endpoints.ts`

```typescript
export const API = {
  AUTH: {
    LOGIN: "/api/auth/login/",
    REGISTER: "/api/auth/register/",
    REFRESH: "/api/auth/token/refresh/",
    LOGOUT: "/api/auth/logout/",
  },
  PRODUCTS: {
    LIST: "/api/products/",
    DETAIL: (slug: string) => `/api/products/${slug}/`,
    CATEGORIES: "/api/categories/",
  },
  ORDERS: {
    LIST: "/api/orders/",
    DETAIL: (id: string) => `/api/orders/${id}/`,
    CANCEL: (id: string) => `/api/orders/${id}/cancel/`,
  },
  PROFILE: {
    ME: "/api/auth/me/",
    UPDATE: "/api/auth/me/update/",
  },
  ADMIN: {
    PRODUCTS: "/api/admin/products/",
    PRODUCT_DETAIL: (id: string) => `/api/admin/products/${id}/`,
    ORDERS: "/api/admin/orders/",
    ORDER_DETAIL: (id: string) => `/api/admin/orders/${id}/`,
    ORDER_STATUS: (id: string) => `/api/admin/orders/${id}/status/`,
    USERS: "/api/admin/users/",
    USER_DETAIL: (id: string) => `/api/admin/users/${id}/`,
    DASHBOARD_STATS: "/api/admin/dashboard/",
  },
} as const;
```

---

### 7.22 `src/shared/constants/app-config.ts`

```typescript
export const APP_CONFIG = {
  ITEMS_PER_PAGE: 20,
  MAX_CART_QUANTITY: 99,
  LOCALES: ["vi", "en"] as const,
  DEFAULT_LOCALE: "vi" as const,
} as const;

export const ORDER_STATUS_LABEL: Record<string, string> = {
  pending: "Chờ xác nhận",
  confirmed: "Đã xác nhận",
  processing: "Đang xử lý",
  shipped: "Đang giao",
  delivered: "Đã giao",
  cancelled: "Đã huỷ",
};

export const PAYMENT_METHOD_LABEL: Record<string, string> = {
  cod: "Thanh toán khi nhận hàng",
  vnpay: "VNPay",
  momo: "Momo",
  zalopay: "ZaloPay",
};
```

---

### 7.23 `src/shared/hooks/use-debounce.ts`

```typescript
import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delay = 500): T {
  const [debounced, setDebounced] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
```

---

### 7.24 `src/shared/hooks/use-local-storage.ts`

```typescript
import { useState, useEffect } from "react";

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // ignore
    }
  }, [key, value]);

  return [value, setValue] as const;
}
```

---

### 7.25 `src/shared/lib/pwa/register-sw.ts`

```typescript
export function registerServiceWorker() {
  if (typeof window !== "undefined" && "serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/sw.js").catch(console.error);
    });
  }
}
```

---

### 7.26 `src/__tests__/setup.ts`

```typescript
import "@testing-library/jest-dom";
```

---

### 7.27 `src/__tests__/helpers/render.tsx`

```tsx
import { render, type RenderOptions } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: RenderOptions,
) {
  return render(ui, { wrapper: Providers, ...options });
}
```

---

### 7.28 `src/messages/vi.json`

```json
{
  "common": {
    "loading": "Đang tải...",
    "error": "Đã có lỗi xảy ra",
    "retry": "Thử lại",
    "cancel": "Huỷ",
    "confirm": "Xác nhận",
    "save": "Lưu",
    "delete": "Xoá",
    "edit": "Chỉnh sửa",
    "search": "Tìm kiếm",
    "back": "Quay lại",
    "viewAll": "Xem tất cả"
  },
  "auth": {
    "login": "Đăng nhập",
    "register": "Đăng ký",
    "logout": "Đăng xuất",
    "email": "Email",
    "password": "Mật khẩu",
    "forgotPassword": "Quên mật khẩu?",
    "noAccount": "Chưa có tài khoản?",
    "hasAccount": "Đã có tài khoản?"
  },
  "product": {
    "addToCart": "Thêm vào giỏ",
    "buyNow": "Mua ngay",
    "outOfStock": "Hết hàng",
    "inStock": "Còn hàng",
    "lowStock": "Còn {count} sản phẩm",
    "price": "Giá",
    "category": "Danh mục",
    "description": "Mô tả"
  },
  "cart": {
    "title": "Giỏ hàng",
    "empty": "Giỏ hàng trống",
    "total": "Tổng cộng",
    "checkout": "Thanh toán",
    "remove": "Xoá",
    "quantity": "Số lượng"
  },
  "order": {
    "title": "Đơn hàng",
    "myOrders": "Đơn hàng của tôi",
    "orderCode": "Mã đơn",
    "status": "Trạng thái",
    "total": "Tổng tiền",
    "cancel": "Huỷ đơn",
    "success": "Đặt hàng thành công!",
    "detail": "Chi tiết đơn hàng"
  },
  "payment": {
    "method": "Phương thức thanh toán",
    "cod": "Thanh toán khi nhận hàng",
    "vnpay": "VNPay",
    "momo": "Momo",
    "zalopay": "ZaloPay"
  }
}
```

---

### 7.29 `playwright.config.ts`

```typescript
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "Mobile Safari", use: { ...devices["iPhone 13"] } },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## 8. Kiểm tra sau setup

```bash
# Chạy dev server
npm run dev

# Type check
npx tsc --noEmit

# Lint
npm run lint

# Format check
npm run format:check

# Test
npm run test

# Build production
npm run build
```

---

## 9. Thứ tự setup khuyên dùng

```
1. create-next-app
2. npm install (production deps)
3. npm install -D (dev deps)
4. npx shadcn@latest init + add components
5. mkdir tạo folder structure
6. touch tạo file cơ bản
7. Config tsconfig, .env.example, vitest, eslint, prettier
8. npx husky init + lint-staged
9. npx @sentry/wizard (cuối cùng — cần project đã có build)
10. npm run dev → kiểm tra
```
