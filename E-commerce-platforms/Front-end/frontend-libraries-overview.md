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

## 3. Form & Validation

| Thư viện                                                                     | Phiên bản | Mục đích sử dụng                                |
| :--------------------------------------------------------------------------- | :-------- | :---------------------------------------------- |
| [**React Hook Form**](https://www.npmjs.com/package/react-hook-form)         | 7.72.1    | Quản lý trạng thái form mượt mà, hiệu năng cao. |
| [**Zod**](https://www.npmjs.com/package/zod)                                 | 4.3.6     | Định nghĩa Schema và validate dữ liệu đầu vào.  |
| [**@hookform/resolvers**](https://www.npmjs.com/package/@hookform/resolvers) | 5.2.2     | Kết nối React Hook Form với Zod (Zod resolver). |

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

| Thư viện                                                                       | Phiên bản | Mục đích sử dụng                                                     |
| :----------------------------------------------------------------------------- | :-------- | :------------------------------------------------------------------- |
| [**Shadcn/UI**](https://ui.shadcn.com/)                                        | @latest   | Bộ sưu tập UI component cao cấp (CLI initialization).                |
| [**TanStack Table**](https://www.npmjs.com/package/@tanstack/react-table)      | 8.20.x    | Xử lý bảng dữ liệu cực mạnh (cho quản lý đơn hàng/sản phẩm).         |
| [**Lucide React**](https://www.npmjs.com/package/lucide-react)                 | 1.8.0     | Bộ icon vector đồng bộ, hiện đại.                                    |
| [**Framer Motion**](https://www.npmjs.com/package/framer-motion)               | 12.38.0   | Tạo hiệu ứng chuyển động, transition mượt mà cho UI.                 |
| [**Sonner**](https://www.npmjs.com/package/sonner)                             | 2.0.7     | Hiển thị thông báo (Toast) dạng pop-up chuyên nghiệp.                |
| [**Vaul**](https://www.npmjs.com/package/vaul)                                 | 1.1.2     | Drawer trượt từ dưới lên (tối ưu cho trải nghiệm Mobile).            |
| [**next-nprogress-bar**](https://www.npmjs.com/package/next-nprogress-bar)     | 2.4.7     | Thanh tiến trình trên đầu trang khi chuyển Route.                    |
| [**@ducanh2912/next-pwa**](https://www.npmjs.com/package/@ducanh2912/next-pwa) | 10.2.9    | Biến website thành ứng dụng mobile (PWA), hỗ trợ offline.            |
| [**next-themes**](https://www.npmjs.com/package/next-themes)                   | 0.4.x     | Quản lý giao diện Sáng/Tối (Dark mode) dễ dàng.                      |
| [**Error Boundary**](https://www.npmjs.com/package/react-error-boundary)       | 6.1.1     | Bắt và xử lý lỗi UI cục bộ, tránh sập toàn trang.                    |
| [**@tiptap/react**](https://www.npmjs.com/package/@tiptap/react)               | 2.x       | Rich-text editor cho admin soạn mô tả sản phẩm (bold, list, image…). |

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

- **Loading States:** Luôn xử lý trạng thái chờ bằng Skeleton hoặc `loading.tsx` để giảm Layout Shift.
- **Empty States:** Luôn có giao diện minh họa khi danh sách trống (ví dụ: giỏ hàng trống, không tìm thấy sản phẩm).
- **Error States:** Hiển thị thông báo lỗi thân thiện (Toast hoặc Alert) thay vì để trắng trang hoặc hiện mã lỗi thô.
- **Accessibility (A11y):** Sử dụng semantic HTML (main, nav, section), đảm bảo mọi ảnh có `alt`, và các interactive elements có `aria-label` nếu cần.
- **Transitions:** Mọi tương tác click/hover quan trọng phải có transition mượt mà (sử dụng Framer Motion cho các trạng thái phức tạp).

### 9.6 API, Xử lý lỗi & Server Actions

- **Async/Await:** Luôn dùng `async/await` thay cho `.then()`.
- **Server Actions:** Ưu tiên dùng Server Actions cho các thao tác thay đổi dữ liệu (POST/PUT/DELETE). Đặt chúng trong file `_lib/actions.ts` của module.
- **Action States:** Sử dụng hook `useActionState` hoặc `useTransition` để quản lý trạng thái pending của Server Actions trên UI.
- **HTTP Status:** Sử dụng thư viện `http-status-codes` để kiểm tra mã lỗi (ví dụ: `StatusCodes.NOT_FOUND`).

### 9.7 Zustand Store Pattern

- **Selector:** Luôn truy xuất state qua selector để tránh re-render thừa (ví dụ: `useStore(s => s.data)`).
- **Action:** Các hàm cập nhật state nên đặt tên bắt đầu bằng động từ (ví dụ: `setAuth`, `removeCartItem`).

### 9.8 Zod & Schema

- **Naming Schema:** Luôn có hậu tố `Schema` để phân biệt với Types (ví dụ: `userSchema` vs `UserType`).
- **Validation:** Thực hiện validate dữ liệu ngay tại "cửa ngõ" (khi nhận dữ liệu từ API hoặc khi user submit form).

### 9.9 Quy trình Git (Conventional Commits)

- **feat:** Thêm tính năng mới.
- **fix:** Sửa lỗi.
- **chore:** Cập nhật build tool, thư viện, cấu hình...
- **refactor:** Sửa code nhưng không thay đổi tính năng.
- **docs:** Cập nhật tài liệu/comment.

### 9.10 Server vs Client Components

- **Server Default:** Mặc định tất cả các component là Server Components để tối ưu hiệu năng và SEO.
- **Client Only:** Chỉ dùng `'use client'` khi cần: Hooks (`useState`, `useEffect`), Event Listeners (`onClick`), hoặc Browser APIs.
- **Composition:** Ưu tiên đưa Client Component xuống sâu nhất có thể trong cây component để giữ được lợi ích của Server Rendering ở các phần khác.

### 9.11 Quy ước tối ưu SEO (Search Engine Optimization)

- **Metadata API:** Mọi trang (`page.tsx`) phải có `title` và `description`. Với các trang động (chi tiết sản phẩm), bắt buộc sử dụng hàm `generateMetadata`.
- **JSON-LD (Structured Data):** Các trang sản phẩm phải chứa script JSON-LD (Schema.org) để Google hiển thị Rich Snippets (giá, đánh giá, tình trạng hàng).
- **Heading Hierarchy:** Mỗi trang chỉ có **duy nhất một thẻ `<h1>`**. Đảm bảo thứ tự logic `<h2>` -> `<h3>` -> `<h4>`.
- **Image SEO:** Luôn sử dụng `next/image`, bắt buộc có thuộc tính `alt` mô tả sản phẩm chứa từ khóa SEO. Các ảnh Banner trên cùng phải có thuộc tính `priority`.
- **Canonical Tags:** Sử dụng link canonical để tránh lỗi trùng lặp nội dung khi có nhiều tham số lọc (filter) trên URL.
- **Sitemap & Robots:** Cấu hình tự động thông qua file `sitemap.ts` và `robots.ts` trong folder `app/`.
