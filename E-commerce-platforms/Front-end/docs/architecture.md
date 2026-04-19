# Architecture — E-Commerce Next.js (User + Admin)

> Stack: Next.js 16 · TypeScript · Tailwind v4 · TanStack Query · Zustand · Axios · Zod · RHF · Shadcn/UI · next-intl
>
> Tài liệu liên quan: [design-system.md](./design-system.md) · [frontend-guidelines.md](./frontend-guidelines.md)

---

## 1. Tổng quan

```
ecommerce-next/
├── src/
│   ├── app/            # Next.js App Router — routing only
│   ├── shared/         # Code dùng chung toàn app (no business logic)
│   └── messages/       # i18n JSON (vi.json, en.json)
├── public/
│   ├── images/
│   ├── icons/          # PWA icons
│   └── manifest.json   # Web App Manifest
├── middleware.ts        # next-intl + auth guard cho /admin
├── next.config.ts       # withPWA() + withBundleAnalyzer
├── tsconfig.json
├── vitest.config.ts
├── eslint.config.mjs
├── .env.example
└── package.json
```

---

## 2. Chi tiết đầy đủ

```
ecommerce-next/
│
├── src/
│   │
│   ├── app/
│   │   ├── globals.css                         # @import "tailwindcss" + @theme (Tailwind v4)
│   │   ├── layout.tsx                          # Root layout: <html> <body> <Providers>
│   │   ├── providers.tsx                       # QueryClientProvider + ThemeProvider
│   │   ├── not-found.tsx                       # Global 404
│   │   ├── sitemap.ts                          # Dynamic sitemap: / + /products/[slug]
│   │   ├── robots.ts                           # Disallow: /admin /api
│   │   ├── opengraph-image.tsx                 # Default OG image
│   │   │
│   │   ├── [locale]/                           # next-intl: vi | en
│   │   │   ├── layout.tsx                      # Locale layout: setRequestLocale + fonts
│   │   │   ├── page.tsx                        # Trang chủ (Server Component)
│   │   │   ├── loading.tsx
│   │   │   ├── error.tsx                       # 'use client' — root error boundary
│   │   │   │
│   │   │   ├── (auth)/                         # ── Xác thực ───────────────────────────
│   │   │   │   ├── _components/
│   │   │   │   │   ├── login-form.tsx          # 'use client' — RHF + Zod
│   │   │   │   │   └── register-form.tsx
│   │   │   │   ├── _lib/
│   │   │   │   │   ├── actions.ts              # proxy → Django /api/auth/
│   │   │   │   │   ├── hooks.ts                # useLogin(), useRegister()
│   │   │   │   │   ├── schemas.ts              # loginSchema, registerSchema
│   │   │   │   │   └── types.ts                # LoginFormValues, RegisterFormValues
│   │   │   │   ├── login/page.tsx
│   │   │   │   ├── register/page.tsx
│   │   │   │   └── forgot-password/page.tsx
│   │   │   │
│   │   │   ├── (shop)/                         # ── Khu vực mua sắm (Customer) ─────────
│   │   │   │   ├── _components/
│   │   │   │   │   ├── product-card.tsx
│   │   │   │   │   ├── product-grid.tsx        # Server Component
│   │   │   │   │   ├── product-filters.tsx     # 'use client' — URL search params
│   │   │   │   │   ├── product-gallery.tsx     # 'use client' — ảnh zoom
│   │   │   │   │   ├── add-to-cart-button.tsx  # 'use client' — useTransition
│   │   │   │   │   ├── cart-drawer.tsx         # 'use client' — Vaul drawer
│   │   │   │   │   ├── cart-item.tsx
│   │   │   │   │   ├── checkout-form.tsx       # 'use client' — RHF + Zod
│   │   │   │   │   ├── payment-method-selector.tsx  # COD / VNPay / Momo / ZaloPay
│   │   │   │   │   └── order-status-badge.tsx
│   │   │   │   ├── _lib/
│   │   │   │   │   ├── actions.ts              # createOrder(), cancelOrder(), applyVoucher()
│   │   │   │   │   ├── hooks.ts                # useProducts(), useProduct(), useCreateOrder()
│   │   │   │   │   ├── query-keys.ts           # productKeys, orderKeys, categoryKeys
│   │   │   │   │   ├── schemas.ts              # checkoutSchema, filterSchema, addressSchema
│   │   │   │   │   └── types.ts                # Product, Order, CartItem, CheckoutData
│   │   │   │   │
│   │   │   │   ├── products/
│   │   │   │   │   ├── page.tsx                # HydrationBoundary prefetch + ProductGrid
│   │   │   │   │   ├── loading.tsx             # ProductGridSkeleton
│   │   │   │   │   └── [slug]/
│   │   │   │   │       ├── page.tsx            # generateMetadata + JSON-LD + ProductDetail
│   │   │   │   │       ├── loading.tsx
│   │   │   │   │       └── not-found.tsx
│   │   │   │   │
│   │   │   │   ├── cart/
│   │   │   │   │   ├── page.tsx                # 'use client' — đọc từ cartStore
│   │   │   │   │   └── loading.tsx
│   │   │   │   │
│   │   │   │   ├── checkout/
│   │   │   │   │   ├── page.tsx                # 'use client' — CheckoutForm + PaymentSelector
│   │   │   │   │   ├── loading.tsx
│   │   │   │   │   └── success/
│   │   │   │   │       ├── page.tsx            # Xác nhận đơn (orderId từ searchParams)
│   │   │   │   │       └── loading.tsx
│   │   │   │   │
│   │   │   │   ├── orders/
│   │   │   │   │   ├── page.tsx                # Danh sách đơn hàng user (Server Component)
│   │   │   │   │   ├── loading.tsx
│   │   │   │   │   └── [id]/
│   │   │   │   │       ├── page.tsx            # Chi tiết đơn + nút huỷ
│   │   │   │   │       └── loading.tsx
│   │   │   │   │
│   │   │   │   └── profile/
│   │   │   │       ├── page.tsx                # 'use client' — cập nhật thông tin cá nhân
│   │   │   │       └── loading.tsx
│   │   │   │
│   │   │   └── (admin)/                        # ── Quản trị (Admin) ────────────────────
│   │   │       ├── layout.tsx                  # Admin layout: sidebar + header + auth check
│   │   │       ├── _components/
│   │   │       │   ├── admin-sidebar.tsx       # 'use client' — navigation links
│   │   │       │   ├── admin-header.tsx        # Breadcrumb + user menu
│   │   │       │   ├── admin-stats-card.tsx    # Card thống kê dashboard
│   │   │       │   └── data-table.tsx          # Reusable TanStack Table wrapper
│   │   │       ├── _lib/
│   │   │       │   ├── hooks.ts                # useAdminProducts(), useAdminOrders()
│   │   │       │   ├── actions.ts              # createProduct(), updateOrderStatus()
│   │   │       │   ├── query-keys.ts           # adminProductKeys, adminOrderKeys
│   │   │       │   └── types.ts                # AdminProduct, AdminOrder, DashboardStats
│   │   │       │
│   │   │       ├── dashboard/
│   │   │       │   ├── page.tsx                # Revenue + Orders overview (Server Component)
│   │   │       │   └── loading.tsx
│   │   │       │
│   │   │       ├── products/
│   │   │       │   ├── page.tsx                # TanStack Table — danh sách + filter
│   │   │       │   ├── loading.tsx
│   │   │       │   ├── _lib/columns.tsx        # Column definitions cho products table
│   │   │       │   ├── new/page.tsx            # Form tạo sản phẩm + Tiptap (dynamic import)
│   │   │       │   └── [id]/
│   │   │       │       ├── page.tsx            # Form chỉnh sửa + upload ảnh S3
│   │   │       │       └── loading.tsx
│   │   │       │
│   │   │       ├── orders/
│   │   │       │   ├── page.tsx                # TanStack Table — filter theo status/date
│   │   │       │   ├── loading.tsx
│   │   │       │   ├── _lib/columns.tsx        # Column definitions cho orders table
│   │   │       │   └── [id]/
│   │   │       │       ├── page.tsx            # Chi tiết + cập nhật trạng thái đơn
│   │   │       │       └── loading.tsx
│   │   │       │
│   │   │       ├── users/
│   │   │       │   ├── page.tsx                # Danh sách user + khoá tài khoản
│   │   │       │   └── [id]/page.tsx           # Chi tiết user + lịch sử đơn hàng
│   │   │       │
│   │   │       └── categories/
│   │   │           ├── page.tsx                # CRUD danh mục sản phẩm
│   │   │           └── loading.tsx
│   │   │
│   │   └── api/                                # ── Route Handlers (proxy → Django) ────
│   │       ├── auth/
│   │       │   ├── login/route.ts              # POST → Django /api/auth/login/
│   │       │   ├── register/route.ts           # POST → Django /api/auth/register/
│   │       │   ├── logout/route.ts             # POST — xoá cookie access_token
│   │       │   └── refresh/route.ts            # POST → Django /api/auth/token/refresh/
│   │       └── payment/
│   │           ├── vnpay/
│   │           │   ├── create/route.ts         # POST — tạo URL thanh toán VNPay
│   │           │   └── callback/route.ts       # GET — xác thực chữ ký HMAC từ VNPay
│   │           ├── momo/
│   │           │   ├── create/route.ts         # POST — tạo URL thanh toán Momo
│   │           │   └── callback/route.ts       # POST — IPN webhook từ Momo
│   │           ├── zalopay/
│   │           │   ├── create/route.ts         # POST — tạo order ZaloPay
│   │           │   └── callback/route.ts       # POST — callback từ ZaloPay
│   │           └── cod/
│   │               └── confirm/route.ts        # POST — xác nhận đơn COD
│   │
│   ├── shared/
│   │   ├── components/
│   │   │   ├── ui/                             # Shadcn/UI — CLI generated (không sửa tay)
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── skeleton.tsx
│   │   │   │   └── ...
│   │   │   ├── layouts/
│   │   │   │   ├── header.tsx                  # Nav + cart icon + user menu + locale switcher
│   │   │   │   └── footer.tsx
│   │   │   ├── skeletons/
│   │   │   │   ├── product-card-skeleton.tsx
│   │   │   │   ├── product-grid-skeleton.tsx
│   │   │   │   └── order-list-skeleton.tsx
│   │   │   └── rich-text-editor.tsx            # Tiptap wrapper — dynamic import only
│   │   │
│   │   ├── hooks/
│   │   │   ├── use-debounce.ts
│   │   │   ├── use-local-storage.ts
│   │   │   └── use-media-query.ts
│   │   │
│   │   ├── lib/
│   │   │   ├── http/
│   │   │   │   ├── client.ts                   # Axios instance (baseURL, timeout, headers)
│   │   │   │   ├── methods.ts                  # Typed: get/post/put/patch/delete
│   │   │   │   └── interceptors/
│   │   │   │       ├── auth.interceptor.ts     # Bearer token + silent refresh (mutex)
│   │   │   │       └── error.interceptor.ts    # AxiosError → ApiError + Sentry
│   │   │   ├── payment/
│   │   │   │   ├── vnpay.ts                    # Tạo URL + verify HMAC VNPay
│   │   │   │   ├── momo.ts                     # Tạo request + verify signature Momo
│   │   │   │   └── zalopay.ts                  # Tạo order + verify callback ZaloPay
│   │   │   ├── errors/
│   │   │   │   ├── api-error.ts                # ApiError class (status, isUnauthorized...)
│   │   │   │   └── error-codes.ts              # Django error code constants
│   │   │   ├── guards/
│   │   │   │   └── auth-guard.tsx              # 'use client' — redirect /login nếu chưa auth
│   │   │   ├── monitoring/
│   │   │   │   └── sentry.ts                   # Sentry init + captureException wrapper
│   │   │   ├── pwa/
│   │   │   │   └── register-sw.ts              # Đăng ký Service Worker phía client
│   │   │   ├── env.ts                          # Zod env validation — fail-fast
│   │   │   ├── query-client.ts                 # staleTime 60s + global onError → toast
│   │   │   └── utils.ts                        # cn() = clsx + twMerge
│   │   │
│   │   ├── stores/
│   │   │   ├── cart-store.ts                   # CartState + CartActions — persist localStorage
│   │   │   └── auth-store.ts                   # AuthState + AuthActions — JWT tokens + role
│   │   │
│   │   ├── types/
│   │   │   ├── product.ts                      # Product, ProductVariant, Category
│   │   │   ├── order.ts                        # Order, OrderItem, OrderStatus, PaymentMethod
│   │   │   ├── user.ts                         # User, Address, UserRole
│   │   │   ├── payment.ts                      # VNPayResponse, MomoResponse, ZaloPayResponse
│   │   │   └── api.ts                          # PaginatedResponse<T>, DjangoErrorResponse
│   │   │
│   │   └── constants/
│   │       ├── api-endpoints.ts                # Tất cả path constants → Django API
│   │       ├── payment-config.ts               # VNPay/Momo/ZaloPay config keys (từ env)
│   │       └── app-config.ts                   # ITEMS_PER_PAGE, ORDER_STATUSES, LOCALES
│   │
│   ├── __tests__/
│   │   ├── setup.ts                            # @testing-library/jest-dom global setup
│   │   └── helpers/
│   │       ├── render.tsx                      # Custom render với Providers
│   │       └── mock-handlers.ts                # MSW handlers cho test
│   │
│   └── messages/
│       ├── vi.json
│       └── en.json
│
├── public/
│   ├── images/                                 # logo, placeholder, og-default
│   ├── icons/
│   │   ├── icon-192x192.png
│   │   ├── icon-512x512.png
│   │   └── icon-maskable.png
│   └── manifest.json
│
├── middleware.ts                               # next-intl routing + /admin auth guard
├── next.config.ts                              # withPWA() + withBundleAnalyzer + i18n
├── tsconfig.json                               # strict: true, paths @/*
├── vitest.config.ts
├── eslint.config.mjs
├── .env.example
└── package.json
```

---

## 3. Nguyên tắc cốt lõi

| Nguyên tắc | Quy tắc |
| --- | --- |
| **Routing** | `app/` chỉ chứa `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx` |
| **Business logic** | Nằm trong `_lib/hooks.ts` — không viết trong page |
| **API call** | Qua `_lib/actions.ts` → `shared/lib/http/methods.ts` — không fetch trực tiếp trong component |
| **Shared** | Component/hook dùng ≥ 2 module → chuyển vào `shared/` |
| **Import** | `shared` không import từ feature; feature không import từ feature khác |
| **Types** | Dùng `z.infer<typeof Schema>` — không viết interface riêng song song |

---

## 4. Auth Guard — 2 lớp bảo vệ

```
Request → middleware.ts (Edge)
              ├── /admin/** → kiểm tra cookie access_token → redirect /login nếu thiếu
              └── Các route khác → next-intl xử lý locale

Client render → (admin)/layout.tsx
              └── Kiểm tra role is_staff từ authStore → redirect nếu không đủ quyền
```

**Phân vai:**

| | `middleware.ts` | `AuthGuard` client |
| --- | --- | --- |
| Runtime | Server (Edge) | Client (browser) |
| Dùng cho | `/admin/**` | `/orders`, `/checkout`, `/profile` |
| Token từ | Cookie `access_token` | Zustand `authStore` |
| UX | Hard redirect, không render | Render 1 frame → redirect |

---

## 5. Payment Flow

```
User chọn phương thức → checkout/page.tsx
    ├── COD     → POST /api/payment/cod/confirm/
    ├── VNPay   → POST /api/payment/vnpay/create/ → redirect URL VNPay
    │               ← GET /api/payment/vnpay/callback/ (verify HMAC)
    ├── Momo    → POST /api/payment/momo/create/ → redirect URL Momo
    │               ← POST /api/payment/momo/callback/ (IPN webhook)
    └── ZaloPay → POST /api/payment/zalopay/create/ → redirect URL ZaloPay
                    ← POST /api/payment/zalopay/callback/

Route Handler (Next.js) → Django REST API → cập nhật OrderStatus → redirect /checkout/success
```

---

## 6. Data Flow

```
Django REST API (port 8000)
        ↕ JWT Bearer token
Next.js Route Handlers (app/api/) — proxy, ẩn endpoint + xử lý payment secret
        ↕
TanStack Query
  ├── Server Component → HydrationBoundary + dehydrate (SSR prefetch)
  └── Client Component → useQuery / useMutation qua custom hooks
        ↕
Zustand (client state)
  ├── cartStore   — giỏ hàng, persist localStorage
  └── authStore   — JWT tokens, user info, role
        ↕
React Components
  ├── Server Components (default) — data display, SEO, generateMetadata
  └── Client Components ('use client') — form, interaction, animation
```

---

## 7. Global Loading & Error Handling

### 7.1 Loading — 3 lớp

| Lớp | Cơ chế | Dùng khi |
| --- | --- | --- |
| Route transition | `next-nprogress-bar` | Chuyển trang |
| Page render | `loading.tsx` | Server Component đang stream |
| Data fetch | `isPending` + Skeleton | Client đang gọi API |

**Lớp 1 — Route transition (`app/providers.tsx`):**

```tsx
import { AppProgressBar } from 'next-nprogress-bar'

export function Providers({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <AppProgressBar color="#e85d04" height="2px" options={{ showSpinner: false }} />
    </QueryClientProvider>
  )
}
```

**Lớp 2 — Page loading (`loading.tsx`):**

```tsx
// app/[locale]/loading.tsx — root
export default function RootLoading() {
  return <div className="flex h-screen items-center justify-center"><Spinner /></div>
}

// app/[locale]/(shop)/products/loading.tsx — route specific
export default function ProductsLoading() {
  return <ProductGridSkeleton />
}
```

**Lớp 3 — Data loading (TanStack Query):**

```tsx
export function ProductGrid({ filters }) {
  const { data, isPending } = useProducts(filters)
  if (isPending) return <ProductGridSkeleton />
  return <div className="grid ...">{data.map(p => <ProductCard key={p.id} product={p} />)}</div>
}
```

### 7.2 Error Handling — 4 tầng

| Tầng | Cơ chế | Bắt lỗi |
| --- | --- | --- |
| Route | `error.tsx` | Server Component throw |
| HTTP | `error.interceptor.ts` → `ApiError` | Axios response 4xx/5xx |
| Query/Mutation | TanStack Query `onError` global | Mọi mutation thất bại |
| Component | `<ErrorBoundary>` | Widget lỗi không sập cả trang |

**Tầng 1 — `app/[locale]/error.tsx`:**

```tsx
'use client'
import * as Sentry from '@sentry/nextjs'

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => { Sentry.captureException(error) }, [error])

  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4">
      <h2 className="text-xl font-semibold">Đã có lỗi xảy ra</h2>
      <p className="text-muted-foreground">{error.message}</p>
      <button onClick={reset} className="rounded bg-primary-500 px-4 py-2 text-white">
        Thử lại
      </button>
    </div>
  )
}
```

**Tầng 2 — `shared/lib/http/interceptors/error.interceptor.ts`:**

```tsx
httpClient.interceptors.response.use(
  (res) => res,
  (error: AxiosError<DjangoErrorResponse>) => {
    const status = error.response?.status ?? 0
    const data = error.response?.data
    const message = typeof data?.detail === 'string' ? data.detail : 'Đã có lỗi xảy ra'

    if (status === 401) useAuthStore.getState().clearAuth()

    return Promise.reject(new ApiError(status, message, data))
  }
)
```

**Tầng 3 — `shared/lib/query-client.ts`:**

```tsx
import { toast } from 'sonner'
import { ApiError } from '@/shared/lib/errors/api-error'

export function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60_000,
        refetchOnWindowFocus: false,
        retry: (failureCount, error) => {
          if (error instanceof ApiError && error.status < 500) return false
          return failureCount < 2
        },
      },
      mutations: {
        onError: (error) => {
          const message = error instanceof ApiError ? error.message : 'Đã có lỗi xảy ra'
          toast.error(message)
        },
      },
    },
  })
}
```

**Tầng 4 — Component `<ErrorBoundary>`:**

```tsx
import { ErrorBoundary } from 'react-error-boundary'

export default function ProductDetailPage() {
  return (
    <div>
      <ProductInfo />
      <ErrorBoundary fallback={<p className="text-muted-foreground">Không tải được đánh giá</p>}>
        <ReviewSection />
      </ErrorBoundary>
    </div>
  )
}
```

---

## 8. .gitignore

```gitignore
# ─── Dependencies ────────────────────────────────────────────────────────────
node_modules/
.pnp
.pnp.js
.yarn/install-state.gz

# ─── Next.js ─────────────────────────────────────────────────────────────────
.next/
out/
build/
public/sw.js
public/workbox-*.js

# ─── Environment Variables ────────────────────────────────────────────────────
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# ─── Payment Secret Keys ──────────────────────────────────────────────────────
*.secret
*.key
payment-config.local.*

# ─── Testing ──────────────────────────────────────────────────────────────────
coverage/
.nyc_output/

# ─── Logs ─────────────────────────────────────────────────────────────────────
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# ─── OS & Editor ──────────────────────────────────────────────────────────────
.DS_Store
Thumbs.db
*.pem

.vscode/*
!.vscode/extensions.json
!.vscode/settings.json

.idea/
*.iml

# ─── Build Cache ──────────────────────────────────────────────────────────────
.turbo/
.cache/
*.tsbuildinfo
next-env.d.ts
.next/analyze/
analyze/

# ─── Misc ─────────────────────────────────────────────────────────────────────
*.tgz
.vercel
```

> Chỉ commit `.env.example` — template không có giá trị thật.

---

## 9. PWA Configuration

**`public/manifest.json`:**

```json
{
  "name": "E-Commerce Shop",
  "short_name": "Shop",
  "description": "Mua sắm trực tuyến nhanh chóng, tiện lợi",
  "start_url": "/vi",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#e85d04",
  "orientation": "portrait",
  "icons": [
    { "src": "/icons/icon-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512x512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

**`next.config.ts`:**

```typescript
import withBundleAnalyzer from '@next/bundle-analyzer'
import withPWA from '@ducanh2912/next-pwa'

const withAnalyzer = withBundleAnalyzer({ enabled: process.env.ANALYZE === 'true' })

const nextConfig = withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
  cacheOnFrontEndNav: true,
  reloadOnOnline: true,
})({
  // next config options
})

export default withAnalyzer(nextConfig)
```

**`app/layout.tsx`:**

```tsx
export const metadata: Metadata = {
  manifest: '/manifest.json',
  themeColor: '#e85d04',
  appleWebApp: { capable: true, statusBarStyle: 'default', title: 'E-Commerce Shop' },
}
```

**Lưu ý:**
- PWA tự tạo `public/sw.js` khi build → đã thêm vào `.gitignore`
- Disable trong development để tránh cache cản trở hot reload
- Chỉ hoạt động trên HTTPS (localhost được miễn trừ)
