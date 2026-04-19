# 📊 Danh Sách Thư Viện Front-end & Version (Cập nhật 04/2026)

Bảng dưới đây liệt kê chi tiết các thư viện sẽ được cài đặt, mục đích sử dụng và phiên bản mới nhất tính đến tháng 04/2026.

> [!IMPORTANT]
> **Cảnh báo bảo mật (Axios):** Dự án sẽ sử dụng bản **1.15.0** trở lên để đảm bảo an toàn tuyệt đối khỏi các lỗ hổng chuỗi cung ứng đã phát hiện.

## 1. Core & Infrastructure

| Thư viện                                                      | Phiên bản   | Mục đích sử dụng                                              |
| :------------------------------------------------------------ | :---------- | :------------------------------------------------------------ |
| **Node.js (LTS)**                                             | **v24.0.0** | Môi trường thực thi code phía server ổn định nhất hiện nay.   |
| [**Next.js**](https://www.npmjs.com/package/next)             | 16.2.3      | React framework mạnh mẽ nhất, tối ưu SEO và tốc độ tải trang. |
| [**next-intl**](https://www.npmjs.com/package/next-intl)      | 4.9.1       | Thư viện đa ngôn ngữ (i18n) tối ưu riêng cho App Router.      |
| [**TypeScript**](https://www.npmjs.com/package/typescript)    | 6.0.2       | Ngôn ngữ gõ tĩnh, giúp code sạch, ít lỗi và dễ bảo trì.       |
| [**Tailwind CSS**](https://www.npmjs.com/package/tailwindcss) | 4.2.2       | Framework CSS giúp xây dựng giao diện nhanh và responsive.    |

## 2. Quản lý Dữ liệu & State

| Thư viện                                                                  | Phiên bản | Mục đích sử dụng                                             |
| :------------------------------------------------------------------------ | :-------- | :----------------------------------------------------------- |
| [**TanStack Query**](https://www.npmjs.com/package/@tanstack/react-query) | 5.99.0    | Quản lý fetching, caching và đồng bộ dữ liệu API từ Backend. |
| [**Zustand**](https://www.npmjs.com/package/zustand)                      | 5.0.12    | Quản lý State toàn cục (Giỏ hàng, Auth) siêu nhẹ.            |
| [**Axios**](https://www.npmjs.com/package/axios)                          | 1.15.0    | Thư viện gọi HTTP request chuyên nghiệp.                     |

> [!NOTE]
> **TanStack Query — patterns bắt buộc theo `tanstack-query-expert` skill:**
>
> - Dùng `HydrationBoundary` + `dehydrate` để prefetch data tại Server Component, tránh waterfall trên client.
> - Cấu hình global `staleTime: 60_000` và `refetchOnWindowFocus: false` trong `QueryClient` (tránh refetch thừa khi khách tab-switch trên trang sản phẩm).
> - Tổ chức Query Key theo **factory pattern**: `productKeys.detail(slug)`, `orderKeys.list()` — không dùng string literal rải rác.
> - Mọi `useQuery` / `useMutation` phải được wrap trong **custom hook** (`useProducts`, `useCreateOrder`). View component chỉ gọi hook, không gọi fetch trực tiếp.
>
> **Zustand — patterns bắt buộc theo `zustand-store-ts` skill:**
>
> - Luôn dùng `subscribeWithSelector` middleware để enable selector subscription bên ngoài React.
> - Tách rõ `interface State` và `interface Actions` trước khi viết store.
> - Truy xuất state qua **individual selector** (`useCartStore(s => s.items)`) — không destructure toàn bộ store.

## 3. Form & Validation

| Thư viện                                                                     | Phiên bản | Mục đích sử dụng                                |
| :--------------------------------------------------------------------------- | :-------- | :---------------------------------------------- |
| [**React Hook Form**](https://www.npmjs.com/package/react-hook-form)         | 7.72.1    | Quản lý trạng thái form mượt mà, hiệu năng cao. |
| [**Zod**](https://www.npmjs.com/package/zod)                                 | 4.3.6     | Định nghĩa Schema và validate dữ liệu đầu vào.  |
| [**@hookform/resolvers**](https://www.npmjs.com/package/@hookform/resolvers) | 5.2.2     | Kết nối React Hook Form với Zod (Zod resolver). |

> [!NOTE]
> **Zod — patterns bắt buộc theo `zod-validation-expert` skill:**
>
> - Dùng `z.infer<typeof Schema>` để suy ra TypeScript type — **không viết interface riêng** song song với schema.
> - Ưu tiên `safeParse` thay vì `parse` để tránh `try/catch` rải rác — kết quả là union `{ success: true, data }` hoặc `{ success: false, error }`.
> - Dùng `z.coerce` khi nhận data từ `FormData` hoặc `URLSearchParams` (giá trị luôn là string).
> - **Validate biến môi trường** tại `shared/lib/env.ts`:
>
>   ```typescript
>   const envSchema = z.object({
>     NEXT_PUBLIC_API_URL: z.string().url(),
>     NODE_ENV: z.enum(["development", "production"]).default("development"),
>   });
>   export const env = envSchema.parse(process.env); // fail-fast khi thiếu env
>   ```
>
> - Đặt tên schema với hậu tố `Schema` (`loginSchema`, `checkoutSchema`) để phân biệt với TypeScript types (`LoginFormValues`, `CheckoutData`).

## 4. Tích hợp Thanh toán (Payment Integration)

> [!NOTE]
> Các cổng thanh toán được tích hợp trực tiếp qua REST API theo tài liệu chính thức — không có SDK npm riêng. Logic gọi API thanh toán đặt tại `shared/lib/payment/`.

| Cổng thanh toán | Phương thức tích hợp        | Mục đích sử dụng                                                   |
| :-------------- | :-------------------------- | :----------------------------------------------------------------- |
| **VNPay**       | REST API (sandbox miễn phí) | Thanh toán thẻ ATM nội địa, thẻ tín dụng, QR code.                 |
| **Momo**        | REST API                    | Ví điện tử phổ biến nhất tại Việt Nam.                             |
| **ZaloPay**     | REST API                    | Ví điện tử tích hợp hệ sinh thái Zalo.                             |
| **COD**         | Logic nội bộ                | Thanh toán tiền mặt khi nhận hàng — không cần tích hợp bên thứ ba. |

**Quy ước tích hợp:**

- Mỗi cổng thanh toán có file riêng: `shared/lib/payment/vnpay.ts`, `momo.ts`, `zalopay.ts`.
- Toàn bộ secret key lưu trong biến môi trường (`.env.local`), tuyệt đối không hardcode.
- Validate callback/webhook từ cổng thanh toán bằng chữ ký HMAC trước khi xử lý đơn hàng.
- Sử dụng Next.js Route Handlers (`app/api/payment/`) làm proxy để che giấu secret key khỏi client.

## 5. UI/UX & Animation (Premium Experience)

| Thư viện                                                                       | Phiên bản | Mục đích sử dụng                                                                        |
| :----------------------------------------------------------------------------- | :-------- | :-------------------------------------------------------------------------------------- |
| [**Shadcn/UI**](https://ui.shadcn.com/)                                        | @latest   | Bộ sưu tập UI component cao cấp (CLI initialization).                                   |
| [**TanStack Table**](https://www.npmjs.com/package/@tanstack/react-table)      | 8.20.x    | Xử lý bảng dữ liệu cực mạnh (cho quản lý đơn hàng/sản phẩm).                            |
| [**Lucide React**](https://www.npmjs.com/package/lucide-react)                 | 1.8.0     | Bộ icon vector đồng bộ, hiện đại.                                                       |
| [**Framer Motion**](https://www.npmjs.com/package/framer-motion)               | 12.38.0   | Tạo hiệu ứng chuyển động, transition mượt mà. ⚠️ ~150KB — bắt buộc dùng dynamic import. |
| [**Sonner**](https://www.npmjs.com/package/sonner)                             | 2.0.7     | Hiển thị thông báo (Toast) dạng pop-up chuyên nghiệp.                                   |
| [**Vaul**](https://www.npmjs.com/package/vaul)                                 | 1.1.2     | Drawer trượt từ dưới lên (tối ưu cho trải nghiệm Mobile).                               |
| [**next-nprogress-bar**](https://www.npmjs.com/package/next-nprogress-bar)     | 2.4.7     | Thanh tiến trình trên đầu trang khi chuyển Route.                                       |
| [**@ducanh2912/next-pwa**](https://www.npmjs.com/package/@ducanh2912/next-pwa) | 10.2.9    | PWA, hỗ trợ offline. ⏳ Phase 2.                                                        |
| [**next-themes**](https://www.npmjs.com/package/next-themes)                   | 0.4.x     | Quản lý giao diện Sáng/Tối (Dark mode) dễ dàng.                                         |
| [**Error Boundary**](https://www.npmjs.com/package/react-error-boundary)       | 6.1.1     | Bắt và xử lý lỗi UI cục bộ, tránh sập toàn trang.                                       |
| [**@tiptap/react**](https://www.npmjs.com/package/@tiptap/react)               | 2.x       | Rich-text editor cho admin soạn mô tả sản phẩm. ⚠️ ~300KB — dùng dynamic import.        |

> [!IMPORTANT]
> **Thư viện nặng — bắt buộc dùng `dynamic import` theo `nextjs-best-practices` + `web-performance-optimization` skills:**
>
> Bundle mặc định phải < 200KB (gzipped). Framer Motion (~150KB) và Tiptap (~300KB) vi phạm nếu import tĩnh.
>
> ```typescript
> // Framer Motion — chỉ load khi component mount trên client
> const MotionDiv = dynamic(() =>
>   import('framer-motion').then(mod => mod.motion.div), { ssr: false }
> );
>
> // Tiptap editor — chỉ cần ở trang Admin
> const RichTextEditor = dynamic(() => import('@/shared/components/RichTextEditor'), {
>   loading: () => <Skeleton className="h-40 w-full" />,
>   ssr: false,
> });
> ```
>
> **`ui-review` skill — reduced-motion bắt buộc cho mọi animation:**
>
> ```typescript
> // Tất cả animation Framer Motion phải respect prefers-reduced-motion
> const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
> <motion.div animate={prefersReducedMotion ? {} : { opacity: 1, y: 0 }} />
> ```

## 6. Tiện ích & Công cụ (Utilities & DX)

| Thư viện                                                                                                      | Phiên bản     | Mục đích sử dụng                                      |
| :------------------------------------------------------------------------------------------------------------ | :------------ | :---------------------------------------------------- |
| [**date-fns**](https://www.npmjs.com/package/date-fns)                                                        | 4.1.0         | Thư viện xử lý và định dạng ngày tháng (siêu nhẹ).    |
| [**http-status-codes**](https://www.npmjs.com/package/http-status-codes)                                      | 2.3.0         | Định nghĩa hằng số cho mã lỗi HTTP chuyên nghiệp.     |
| [**clsx**](https://www.npmjs.com/package/clsx) / [**tw-merge**](https://www.npmjs.com/package/tailwind-merge) | 2.1.1 / 3.5.0 | Quản lý và gộp class Tailwind thông minh.             |
| [**server-only**](https://www.npmjs.com/package/server-only)                                                  | 0.0.1         | Đảm bảo mã nguồn chỉ chạy ở phía Server (bảo mật).    |
| [**client-only**](https://www.npmjs.com/package/client-only)                                                  | 0.0.1         | Đánh dấu các component chỉ chạy phía Client.          |
| [**RQ Devtools**](https://www.npmjs.com/package/@tanstack/react-query-devtools)                               | 5.99.0        | Bảng điều khiển debug dữ liệu API (chỉ dùng khi Dev). |

> [!NOTE]
> **`ahooks` đã được loại bỏ.** TanStack Query + Zustand + React Hook Form đã xử lý đủ các use case. Nếu sau này cần hook tiện ích cụ thể (ví dụ: `useInfiniteScroll`, `useVirtualList`), cài đặt riêng theo nhu cầu thực tế thay vì import toàn bộ thư viện.

## 7. Chất lượng Code & Testing

| Thư viện                                                                                                        | Phiên bản      | Mục đích sử dụng                                         |
| :-------------------------------------------------------------------------------------------------------------- | :------------- | :------------------------------------------------------- |
| [**Vitest**](https://www.npmjs.com/package/vitest)                                                              | 4.1.4          | Framework chạy test siêu nhanh, thay thế cho Jest.       |
| [**Testing Library**](https://www.npmjs.com/package/@testing-library/react)                                     | 16.3.2         | Bộ công cụ test giao diện React tương thích với Vitest.  |
| [**ESLint**](https://www.npmjs.com/package/eslint) / [**Prettier**](https://www.npmjs.com/package/prettier)     | 10.2.0 / 3.8.3 | Kiểm tra lỗi code và tự động format định dạng code sạch. |
| [**Husky**](https://www.npmjs.com/package/husky) / [**lint-staged**](https://www.npmjs.com/package/lint-staged) | 9.1.7 / 16.4.0 | Git Hooks tự động kiểm tra code trước khi commit.        |
| [**bundle-analyzer**](https://www.npmjs.com/package/@next/bundle-analyzer)                                      | 15.3.0         | Phân tích dung lượng bundle để tối ưu tốc độ tải trang.  |

## 8. Cấu trúc Thư mục (Architecture - Colocation Focus)

Dự án được tổ chức theo mô hình **Colocation**, giúp đóng gói logic tính năng ngay bên trong cấu trúc của App Router.

```text
src/
├── app/
│   ├── [locale]/
│   │   ├── (auth)/               # Module Xử lý Xác thực
│   │   │   ├── _components/      # UI components (LoginForm, SocialLogin...)
│   │   │   ├── _lib/             # Logic: hooks, services, types của Auth
│   │   │   ├── login/            # Route: /login
│   │   │   └── register/         # Route: /register
│   │   │
│   │   ├── (shop)/               # Module Mua sắm
│   │   │   ├── _components/      # UI components (ProductCard, CartDrawer...)
│   │   │   ├── _lib/             # Logic: hooks, services cho Products/Cart
│   │   │   ├── products/         # Route: /products & /[slug]
│   │   │   ├── cart/             # Route: /cart
│   │   │   └── checkout/         # Route: /checkout
│   │   │
│   │   └── layout.tsx            # Root layout cho cả locale
│   ├── api/
│   │   └── payment/              # Route Handlers cho callback/webhook thanh toán (VNPay, Momo, ZaloPay)
│   ├── globals.css               # Style toàn cục & Tailwind layer
│   └── loading.tsx               # UI loading mặc định cấp root
│
├── shared/                       # (Shared Layer - Thành phần dùng chung toàn app)
│   ├── components/               # Shadcn/UI (Button, Input...), Header, Footer
│   ├── hooks/                    # Global hooks (useDebounce, useLocalStorage...)
│   ├── lib/
│   │   ├── axios.ts              # Cấu hình Axios instance
│   │   ├── query-client.ts       # Cấu hình TanStack Query
│   │   ├── payment/              # Logic tích hợp VNPay, Momo, ZaloPay
│   │   └── utils.ts             # Hàm tiện ích dùng chung
│   ├── types/                    # Các Interfaces/Types dùng chung
│   └── constants/                # Định nghĩa Enums, API Endpoints
│
├── messages/                     # (i18n) Nơi chứa các file JSON dịch thuật (vi.json, en.json) cho đa ngôn ngữ
└── ...
```

## 9. Quy ước Lập trình (Coding Conventions)

Để đảm bảo code sạch và nhất quán, dự án áp dụng các quy tắc sau:

### 9.1 Đặt tên (Naming)

- **Thư mục & File:** Luôn dùng `kebab-case` (ví dụ: `order-details.tsx`, `use-cart-store.ts`).
- **Component:** Dùng `PascalCase` (ví dụ: `const ProductGallery = () => ...`).
- **Interface/Type:** Dùng `PascalCase` và đặt tên mô tả rõ ràng (ví dụ: `ProductItem`, `UserPayload`).
- **Hằng số (Constants):** Dùng `SCREAMING_SNAKE_CASE` (ví dụ: `API_BASE_URL`, `MAX_RETRY_COUNT`).

### 9.2 Cấu trúc Component

- Ưu tiên **Arrow Function** cho tất cả các functional components.
- Sử dụng **Named Exports** (trừ trường hợp file `page.tsx`, `layout.tsx` bắt buộc dùng default export của Next.js).
- Áp dụng **Early Return** để giảm độ sâu của các khối lệnh `if/else`.

### 9.3 Import & Export

- Sử dụng **Absolute Imports** với alias `@/` (ví dụ: `import { Button } from "@/shared/components/ui/button"`).
- **Thứ tự Import:**
  1. React & Next.js built-in
  2. Thư viện bên thứ ba (lucide, framer-motion...)
  3. Shared components/hooks/utils
  4. Feature-specific code (local components/hooks)
  5. Styles/Types

### 9.4 State, Logic & Type Safety

- **Strict Typing (Không dùng any):** Tuyệt đối không sử dụng kiểu dữ liệu `any`. Nếu không biết rõ kiểu dữ liệu, hãy sử dụng `unknown` và thực hiện type guards.
- **Khai báo Type minh bạch:** Mọi tham số của hàm (parameters) và giá trị trả về (return type) đều phải được khai báo tường minh.
- **Co-location:** Giữ state và logic gần nhất có thể với nơi nó được sử dụng.
- **Private Folders:** Sử dụng prefix `_` cho các folder chứa logic trong `app/` để Next.js không tạo route nhầm.
- **Zod Validation:** Luôn validate dữ liệu đầu vào từ API hoặc Form bằng Zod để đảm bảo an toàn từ "cửa ngõ".

### 9.5 UI/UX (Premium Standard)

- **Loading States:** Luôn xử lý trạng thái chờ bằng Skeleton hoặc `loading.tsx` để giảm Layout Shift (CLS).
- **Empty States:** Luôn có giao diện minh họa khi danh sách trống (giỏ hàng trống, không tìm thấy sản phẩm).
- **Error States:** Hiển thị thông báo lỗi thân thiện (Toast hoặc Alert) thay vì để trắng trang hoặc hiện mã lỗi thô.
- **Accessibility (A11y) — `ui-review` skill:**
  - Semantic HTML (`main`, `nav`, `section`, `article`).
  - Mọi `<img>` có `alt` mô tả sản phẩm (không để trống).
  - Interactive elements có `aria-label` khi icon-only.
  - Touch targets tối thiểu 44×44px trên mobile.
  - Visible keyboard focus states cho tất cả interactive elements.
  - Color contrast tối thiểu 4.5:1 cho text thường, 3:1 cho text lớn.
- **Reduced Motion — bắt buộc cho mọi animation Framer Motion:**
  - Dùng `useReducedMotion()` hook của Framer Motion hoặc CSS `@media (prefers-reduced-motion: reduce)`.
- **Transitions:** CSS transition (`transition-colors duration-150`) ưu tiên hơn Framer Motion cho hover/focus đơn giản. Framer Motion chỉ cho animated mount/unmount phức tạp.

### 9.6 API, Xử lý lỗi & Server Actions

- **Async/Await:** Luôn dùng `async/await` thay cho `.then()`.
- **Server Actions:** Ưu tiên dùng Server Actions cho các thao tác thay đổi dữ liệu (POST/PUT/DELETE). Đặt chúng trong file `_lib/actions.ts` của module.
- **Action States:** Sử dụng hook `useActionState` hoặc `useTransition` để quản lý trạng thái pending của Server Actions trên UI.
- **HTTP Status:** Sử dụng thư viện `http-status-codes` để kiểm tra mã lỗi (ví dụ: `StatusCodes.NOT_FOUND`).

> [!NOTE]
> **Server Actions trong dự án này = Next.js Route Handler gọi Django API** — không phải direct DB mutation.
> Backend là Django REST Framework. "Server Action" ở đây là Route Handler (`app/api/`) đóng vai trò proxy:
> client → Route Handler (Next.js) → Django REST API → DB.
> Lợi ích: che giấu Django endpoint URL và xử lý CSRF/auth token phía server.

### 9.7 Zustand Store Pattern

- **Middleware:** Luôn bọc store trong `subscribeWithSelector` để enable selector subscription bên ngoài React component.
- **Tách State/Actions:** Định nghĩa riêng `interface CartState` và `interface CartActions` trước khi viết `create<CartState & CartActions>()`.
- **Selector:** Luôn truy xuất state qua selector để tránh re-render thừa (`useCartStore(s => s.items)`, không destructure toàn store).
- **Action:** Tên action bắt đầu bằng động từ (`addToCart`, `removeCartItem`, `clearCart`).

### 9.8 Zod & Schema

- **Naming:** Luôn có hậu tố `Schema` (`loginSchema`, `checkoutSchema`) để phân biệt với TypeScript types (`LoginFormValues`).
- **Inference:** Dùng `z.infer<typeof Schema>` — không viết interface riêng song song với schema.
- **Safe parse:** Ưu tiên `safeParse` thay vì `parse` để kiểm soát lỗi mà không dùng `try/catch`.
- **Coercion:** Dùng `z.coerce.number()` / `z.coerce.boolean()` khi nhận data từ `FormData` hoặc URL params.
- **Env validation:** Validate tất cả `process.env` qua Zod schema tại `shared/lib/env.ts` (fail-fast khi thiếu biến).
- **Validation:** Thực hiện validate ngay tại "cửa ngõ" — khi nhận data từ API response hoặc khi user submit form.

### 9.9 Tailwind CSS v4 — CSS-first Setup

> [!NOTE]
> Dự án dùng **Tailwind v4** (Oxide engine). Không có `tailwind.config.js` — cấu hình hoàn toàn qua CSS.

- **`@theme` directive** thay thế `theme.extend` trong `tailwind.config.js`:

  ```css
  /* app/globals.css */
  @import "tailwindcss";

  @theme {
    --color-brand-500: oklch(0.6 0.2 260);
    --font-sans: "Inter Variable", sans-serif;
    --spacing-18: 4.5rem;
  }
  ```

- **OKLCH color system** — dùng `oklch()` thay HEX/RGB cho màu brand/semantic để đồng nhất với Tailwind v4 default palette.
- **Container queries** (`@container`) cho các component tái sử dụng thay vì breakpoint toàn trang:

  ```html
  <div class="@container">
    <div class="grid @sm:grid-cols-2 @lg:grid-cols-4">...</div>
  </div>
  ```

- **`@apply` bị discouraged trong v4** — viết utility class trực tiếp hoặc dùng CSS variables. Chỉ dùng `@apply` cho reset/base layer khi thực sự cần.
- **No prefix needed** — v4 bỏ `content` config, class detection tự động qua source scanning.

### 9.11 Quy trình Git (Conventional Commits)

- **feat:** Thêm tính năng mới.
- **fix:** Sửa lỗi.
- **chore:** Cập nhật build tool, thư viện, cấu hình...
- **refactor:** Sửa code nhưng không thay đổi tính năng.
- **docs:** Cập nhật tài liệu/comment.

### 9.12 Server vs Client Components

- **Server Default:** Mặc định tất cả các component là Server Components để tối ưu hiệu năng và SEO.
- **Client Only:** Chỉ dùng `'use client'` khi cần: Hooks (`useState`, `useEffect`), Event Listeners (`onClick`), hoặc Browser APIs.
- **Composition:** Ưu tiên đưa Client Component xuống sâu nhất có thể trong cây component để giữ được lợi ích của Server Rendering ở các phần khác.

### 9.13 Quy ước tối ưu SEO (Search Engine Optimization)

- **Metadata API:** Mọi trang (`page.tsx`) phải có `title` và `description`. Với các trang động (chi tiết sản phẩm), bắt buộc sử dụng hàm `generateMetadata`.
- **JSON-LD (Structured Data):** Các trang sản phẩm phải chứa script JSON-LD (Schema.org) để Google hiển thị Rich Snippets (giá, đánh giá, tình trạng hàng).
- **Heading Hierarchy:** Mỗi trang chỉ có **duy nhất một thẻ `<h1>`**. Đảm bảo thứ tự logic `<h2>` -> `<h3>` -> `<h4>`.
- **Image SEO:** Luôn sử dụng `next/image`, bắt buộc có thuộc tính `alt` mô tả sản phẩm chứa từ khóa SEO. Các ảnh Banner trên cùng phải có thuộc tính `priority`.
- **Canonical Tags:** Sử dụng link canonical để tránh lỗi trùng lặp nội dung khi có nhiều tham số lọc (filter) trên URL.
- **Sitemap & Robots:** Cấu hình tự động thông qua file `sitemap.ts` và `robots.ts` trong folder `app/`.

## 10. Quality Gates — Pre-deploy Checklist

> Dựa trên `react-nextjs-development` skill. Không merge PR nếu chưa pass tất cả mục bên dưới.

### 10.1 Code Quality

- [ ] `tsc --noEmit` pass — không có TypeScript error
- [ ] `eslint` pass — không có warning/error
- [ ] `prettier --check` pass — code đã format đúng
- [ ] Không có `any` type còn sót, không có `console.log` trong production code

### 10.2 Testing

- [ ] `vitest run` pass — unit tests xanh
- [ ] Playwright E2E pass cho happy path: đăng nhập, thêm vào giỏ, checkout COD, xem đơn hàng
- [ ] Coverage không giảm so với baseline (target: ≥ 70% cho shared/lib)

### 10.3 Performance (Core Web Vitals)

- [ ] **LCP < 2.5s** — trang sản phẩm (đo bằng Lighthouse hoặc WebPageTest)
- [ ] **CLS < 0.1** — không có layout shift từ ảnh/font chưa có `size`
- [ ] **FID/INP < 100ms** — trang checkout không bị blocking
- [ ] Bundle gzipped < 200KB — kiểm tra bằng `@next/bundle-analyzer`
- [ ] Framer Motion và Tiptap đã dùng dynamic import (không xuất hiện trong initial bundle)

### 10.4 Accessibility (WCAG 2.1 AA)

- [ ] Tất cả ảnh sản phẩm có `alt` text
- [ ] Icon-only buttons có `aria-label`
- [ ] Color contrast ≥ 4.5:1 (kiểm tra bằng Axe DevTools hoặc Lighthouse)
- [ ] Keyboard navigation hoạt động cho: menu, form, cart drawer, modal
- [ ] `prefers-reduced-motion` được respect trên tất cả Framer Motion animation

### 10.5 Mobile & Responsive

- [ ] Giao diện không bị vỡ ở 375px (iPhone SE)
- [ ] Touch targets ≥ 44×44px cho tất cả interactive elements
- [ ] Cart drawer/modal đóng được bằng swipe hoặc nút rõ ràng
- [ ] Toast notification không che khuất nội dung quan trọng trên mobile
