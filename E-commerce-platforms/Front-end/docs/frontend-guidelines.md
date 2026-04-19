# Frontend Guidelines — E-Commerce Next.js

> Tài liệu liên quan: [architecture.md](./architecture.md) · [design-system.md](./design-system.md)

---

## 1. State Management — Khi nào dùng gì

### 1.1 Decision table

| Tình huống                               | Dùng                       | Lý do                                     |
| ---------------------------------------- | -------------------------- | ----------------------------------------- |
| Data từ API, cần cache                   | **TanStack Query**         | Cache, stale/refetch, SSR hydration       |
| Data từ API, đơn giản, không cần cache   | **Server Component fetch** | Nhẹ hơn, không cần hook                   |
| State chỉ tồn tại trên client (giỏ hàng) | **Zustand**                | Persist localStorage, không phụ thuộc API |
| Auth token, user info                    | **Zustand**                | Cần truy xuất ngoài React (interceptor)   |
| Form state                               | **React Hook Form**        | Tối ưu cho form, không cần global store   |
| URL state (filter, page)                 | **URL search params**      | Shareable, SEO-friendly                   |
| UI state cục bộ (modal, accordion)       | **useState**               | Không cần global                          |

### 1.2 Quy tắc rõ ràng

```
Server state (data từ API)       → TanStack Query
Client-only state (cart, auth)   → Zustand
Form state                       → React Hook Form
URL state (filter, sort, page)   → useSearchParams
UI state cục bộ                  → useState / useReducer
```

### 1.3 Khi nào dùng Server Component fetch thay vì TanStack Query

**Dùng Server Component fetch khi:**

- Trang chỉ cần data 1 lần khi load (không refetch)
- Data phục vụ SEO (generateMetadata, JSON-LD)
- Không cần cache phía client

```tsx
// ✅ Server Component — không cần TanStack Query
export default async function ProductDetailPage({ params }) {
  const product = await http.get<Product>(API.PRODUCTS.DETAIL(params.slug));
  return <ProductDetail product={product} />;
}
```

**Dùng TanStack Query khi:**

- Data cần cache (tránh refetch khi back/tab switch)
- Cần invalidate sau mutation (thêm vào giỏ → update count)
- Có pagination, infinite scroll
- Real-time hoặc polling

```tsx
// ✅ TanStack Query — cần cache + invalidation
export function useProducts(filters: ProductFilters) {
  return useQuery({
    queryKey: productKeys.list(filters),
    queryFn: () => http.get(API.PRODUCTS.LIST, filters),
    staleTime: 60_000,
  });
}
```

---

## 2. Auth Refresh Strategy — Mutex Pattern

Vấn đề: Nhiều request đồng thời nhận 401 → tất cả cùng gọi `refreshToken()` → race condition.

**`shared/lib/http/interceptors/auth.interceptor.ts`:**

```typescript
let refreshPromise: Promise<string> | null = null; // mutex

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

      // Dùng chung 1 promise — các request sau chờ request đầu refresh xong
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
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  },
);
```

---

## 3. Testing Strategy

### 3.1 Phân loại test

| Loại        | Tool                     | Test gì               | Ở đâu                    |
| ----------- | ------------------------ | --------------------- | ------------------------ |
| Unit        | Vitest                   | hooks, utils, schemas | `*.test.ts` cạnh file    |
| Component   | Vitest + Testing Library | render, interaction   | `*.test.tsx` cạnh file   |
| Integration | Vitest + MSW             | API flow, form submit | `__tests__/integration/` |
| E2E         | Playwright               | Happy path toàn trình | `e2e/`                   |

### 3.2 Coverage targets

| Layer             | Target                     |
| ----------------- | -------------------------- |
| `shared/lib/`     | ≥ 80% — logic cốt lõi      |
| `shared/utils/`   | ≥ 90% — pure functions     |
| `_lib/hooks.ts`   | ≥ 70% — business logic     |
| `_lib/schemas.ts` | ≥ 90% — validation         |
| Page components   | Không bắt buộc (E2E cover) |

### 3.3 Cấu trúc test

```
src/
├── shared/
│   └── lib/
│       ├── utils.ts
│       └── utils.test.ts          ← unit test cạnh file
├── __tests__/
│   ├── setup.ts                   ← @testing-library/jest-dom
│   ├── helpers/
│   │   ├── render.tsx             ← custom render với Providers
│   │   └── mock-handlers.ts      ← MSW handlers
│   └── integration/
│       ├── checkout.test.tsx      ← form submit + API mock
│       └── auth.test.tsx          ← login flow
e2e/
├── checkout.spec.ts               ← happy path: login → add to cart → checkout COD
├── admin-products.spec.ts         ← admin: tạo/sửa/xoá sản phẩm
└── auth.spec.ts                   ← login, register, forgot password
```

### 3.4 Vitest config

```typescript
// vitest.config.ts
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

### 3.5 Custom render với Providers

```tsx
// src/__tests__/helpers/render.tsx
import { render, RenderOptions } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: RenderOptions,
) {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
    options,
  );
}
```

### 3.6 Ví dụ test hook

```typescript
// (shop)/_lib/hooks.test.ts
import { renderHook, waitFor } from "@testing-library/react";
import { server } from "@/__tests__/helpers/mock-handlers";
import { useProducts } from "./hooks";

describe("useProducts", () => {
  it("trả về danh sách sản phẩm", async () => {
    const { result } = renderHook(() => useProducts({}), {
      wrapper: Providers,
    });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(2);
  });
});
```

### 3.7 E2E happy path (Playwright)

```typescript
// e2e/checkout.spec.ts
test("checkout COD thành công", async ({ page }) => {
  await page.goto("/vi/login");
  await page.fill("[name=email]", "test@example.com");
  await page.fill("[name=password]", "password123");
  await page.click("button[type=submit]");

  await page.goto("/vi/products");
  await page.click("text=Thêm vào giỏ");

  await page.goto("/vi/checkout");
  await page.click("text=Thanh toán khi nhận hàng");
  await page.click("text=Đặt hàng");

  await expect(page).toHaveURL(/\/checkout\/success/);
  await expect(page.locator("h1")).toContainText("Đặt hàng thành công");
});
```

---

## 4. Monitoring & Error Tracking

### 4.1 Sentry Setup

```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

**`shared/lib/monitoring/sentry.ts`:**

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
```

### 4.2 Tích hợp vào error handlers

```tsx
// app/[locale]/error.tsx
import { captureError } from "@/shared/lib/monitoring/sentry";

export default function GlobalError({ error, reset }) {
  useEffect(() => {
    captureError(error);
  }, [error]);
  // ...
}

// shared/lib/http/interceptors/error.interceptor.ts
import { captureError } from "@/shared/lib/monitoring/sentry";

httpClient.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    const status = error.response?.status ?? 0;
    if (status >= 500) captureError(error, { url: error.config?.url });
    // ...
  },
);
```

### 4.3 Logging strategy

| Event                 | Action                                          |
| --------------------- | ----------------------------------------------- |
| Server error (5xx)    | Sentry + toast "Lỗi hệ thống, thử lại sau"      |
| Client error (4xx)    | Toast message từ Django error response          |
| 401                   | Silent refresh → nếu thất bại → redirect /login |
| Payment callback fail | Sentry + redirect trang lỗi thanh toán          |
| JS runtime error      | `error.tsx` + Sentry                            |

---

## 5. Naming Conventions

### 5.1 Files & Folders

| Loại           | Convention                  | Ví dụ                                   |
| -------------- | --------------------------- | --------------------------------------- |
| Folder         | `kebab-case`                | `product-detail/`, `order-list/`        |
| Component file | `kebab-case`                | `product-card.tsx`, `cart-drawer.tsx`   |
| Hook file      | `use-` prefix               | `use-cart.ts`, `use-products.ts`        |
| Store file     | `-store` suffix             | `cart-store.ts`, `auth-store.ts`        |
| Schema file    | `-schema` hoặc `schemas.ts` | `checkout-schema.ts`                    |
| Util file      | `.utils` suffix             | `date.utils.ts`, `currency.utils.ts`    |
| Constant file  | `.config` hoặc `.enum`      | `app.config.ts`, `order-status.enum.ts` |

### 5.2 Components

Dùng **`function` declaration** cho tất cả components và hooks — không dùng arrow function ở cấp top-level.

> **Lưu ý:** React 19 không yêu cầu style này — cả hai đều hợp lệ về mặt kỹ thuật. Đây là **quy ước của project** để đảm bảo nhất quán.

**Lý do chọn `function` declaration:**

- **Generic trong `.tsx`** — `<T>` trong arrow function bị parser nhầm thành JSX tag; `function` declaration không có vấn đề này (workaround arrow: dùng `<T,>` trailing comma nhưng dễ bị bỏ sót)
- **Nhất quán với Next.js App Router** — `page.tsx`, `layout.tsx`, `generateMetadata` đều dùng `function` declaration theo convention cộng đồng
- **Đồng nhất trong codebase** — chọn một style duy nhất tránh mix-and-match

```tsx
// ✅ PascalCase — named export, function declaration
export function ProductCard({ product }: ProductCardProps) {}
export function CartDrawer() {}

// ✅ page.tsx / layout.tsx — default export (Next.js convention)
export default function ProductsPage() {}
export default function AdminLayout({ children }) {}

// ✅ Generic an toàn với function declaration trong .tsx
function identity<T>(value: T): T { return value }

// ❌ Không dùng — arrow function ở top-level component/hook
export const ProductCard = ({ product }: ProductCardProps) => {}
export const CartDrawer = () => {}

// ❌ Không dùng — generic trong arrow function .tsx dễ gây lỗi parse
const identity = <T>(value: T) => value   // <T> bị nhầm thành JSX
const identity = <T,>(value: T) => value  // workaround nhưng dễ bỏ sót

// ❌ Sai — tên
export default function productCard() {}   // không phải PascalCase
export function Product_Card() {}          // không dùng underscore
```

**Arrow function vẫn dùng trong các trường hợp:**

```tsx
// ✅ Inline callback trong JSX
<button onClick={() => handleClick(id)}>Xoá</button>;

// ✅ Array methods
items.map((item) => <Item key={item.id} />);

// ✅ API endpoint constants
DETAIL: (slug: string) => `/api/products/${slug}/`;

// ✅ Zustand actions trong store definition
addToCart: (item) => set((s) => ({ items: [...s.items, item] }));
```

### 5.3 TypeScript Types

```ts
// ✅ PascalCase, không prefix I/T
interface ProductCardProps { product: Product }
type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'

// ✅ Zod — suffix Schema, dùng z.infer
const checkoutSchema = z.object({ ... })
type CheckoutData = z.infer<typeof checkoutSchema>

// ❌ Sai
interface IProduct { ... }    // không dùng prefix I
type TOrderStatus = ...       // không dùng prefix T
```

### 5.4 Variables & Functions

```ts
// camelCase — biến và hàm
const productList: Product[] = [];
function formatCurrency(amount: number): string {}
function fetchProducts(filters: ProductFilters) {}

// SCREAMING_SNAKE_CASE — constants
const ITEMS_PER_PAGE = 20;
const MAX_CART_QUANTITY = 99;

// Action — bắt đầu bằng động từ
function addToCart(item: CartItem) {}
function removeCartItem(variantId: string) {}
function updateOrderStatus(id: string, status: OrderStatus) {}
```

### 5.5 Hooks

```ts
// prefix "use" + camelCase
function useProducts(filters: ProductFilters) {}
function useCreateOrder() {}
function useDebounce<T>(value: T, delay: number) {}

// ❌ Sai
function getProducts() {} // thiếu prefix use
function UseCart() {} // không phải camelCase sau use
```

### 5.6 Zustand Store

```ts
interface CartState {
  items: CartItem[];
  total: number;
  itemCount: number;
}

interface CartActions {
  addToCart: (item: CartItem) => void;
  removeCartItem: (variantId: string) => void;
  updateQuantity: (variantId: string, qty: number) => void;
  clearCart: () => void;
}

// Selector — truy xuất từng field, không destructure
const cartItems = useCartStore((s) => s.items);
const cartTotal = useCartStore((s) => s.total);
const isLoggedIn = useAuthStore((s) => !!s.accessToken);
```

### 5.7 Query Keys

```ts
export const productKeys = {
  all: ["products"] as const,
  list: (filters: ProductFilters) =>
    [...productKeys.all, "list", filters] as const,
  detail: (slug: string) => [...productKeys.all, "detail", slug] as const,
};

export const orderKeys = {
  all: ["orders"] as const,
  list: () => [...orderKeys.all, "list"] as const,
  detail: (id: string) => [...orderKeys.all, "detail", id] as const,
};

// Admin keys — prefix "admin"
export const adminProductKeys = {
  all: ["admin", "products"] as const,
  list: (page: number) => [...adminProductKeys.all, "list", page] as const,
};
```

### 5.8 API Endpoints Constants

```ts
// shared/constants/api-endpoints.ts
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
  },
  ORDERS: {
    LIST: "/api/orders/",
    DETAIL: (id: string) => `/api/orders/${id}/`,
    CANCEL: (id: string) => `/api/orders/${id}/cancel/`,
  },
  ADMIN: {
    PRODUCTS: "/api/admin/products/",
    ORDERS: "/api/admin/orders/",
    USERS: "/api/admin/users/",
  },
} as const;
```

### 5.9 Tailwind Class Order

```
Layout → Flex/Grid → Sizing → Spacing → Typography → Color → Border → Effect → State
```

```tsx
<button
  className="
  flex items-center justify-center
  w-full h-11
  px-4 py-2 gap-2
  text-sm font-semibold
  text-white bg-primary-500
  rounded-btn border border-transparent
  shadow-sm
  hover:bg-primary-600 disabled:opacity-50
  transition-colors duration-150
"
>
  Mua ngay
</button>
```

### 5.10 Git Commit Convention

```
feat:     thêm tính năng mới
fix:      sửa bug
chore:    cập nhật config, thư viện, tool
refactor: sửa code không đổi tính năng
style:    sửa CSS/UI không đổi logic
test:     thêm/sửa test
docs:     cập nhật tài liệu
```

```bash
feat: add product filter by category and price range
fix: cart total not updating after remove item
chore: upgrade tanstack-query to v5.99
refactor: extract payment logic to shared/lib/payment
```

---

## 6. Quy tắc khi thêm tính năng mới

1. Tạo `_lib/types.ts` + `_lib/schemas.ts` trước — xác định data shape
2. Viết `_lib/actions.ts` (API call) → `_lib/query-keys.ts` → `_lib/hooks.ts`
3. Viết `_components/` sử dụng hooks — không logic trong component
4. Viết `page.tsx` chỉ compose components — không có business logic
5. Component/hook dùng ≥ 2 nơi → chuyển vào `shared/`
6. Viết test cho hook và schema trước khi merge

---

## 7. Pre-deploy Checklist

### Code Quality

- [ ] `tsc --noEmit` pass — không có TypeScript error
- [ ] `eslint` pass — không có warning/error
- [ ] Không có `any` type, không có `console.log` trong production code

### Testing

- [ ] `vitest run` pass — unit/integration tests xanh
- [ ] Playwright E2E pass: đăng nhập → thêm vào giỏ → checkout COD → xem đơn hàng
- [ ] Coverage ≥ 70% cho `shared/lib/`

### Performance (Core Web Vitals)

- [ ] LCP < 2.5s — trang sản phẩm
- [ ] CLS < 0.1 — không layout shift từ ảnh/font
- [ ] Bundle gzipped < 200KB — kiểm tra bằng `@next/bundle-analyzer`
- [ ] Framer Motion và Tiptap dùng dynamic import

### Accessibility (WCAG 2.1 AA)

- [ ] Tất cả ảnh sản phẩm có `alt` text
- [ ] Icon-only buttons có `aria-label`
- [ ] Color contrast ≥ 4.5:1
- [ ] Keyboard navigation hoạt động: menu, form, cart drawer, modal
- [ ] `prefers-reduced-motion` respected trên mọi animation

### Mobile

- [ ] Không vỡ layout ở 375px (iPhone SE)
- [ ] Touch targets ≥ 44×44px
- [ ] Cart drawer đóng được bằng swipe hoặc nút rõ ràng
