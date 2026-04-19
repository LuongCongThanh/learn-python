# Shop Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete customer-facing shopping experience — product listing, product detail, cart, checkout, orders, and profile pages — plus API payment proxy routes.

**Architecture:** Server Components for data-display pages (products, orders). Client Components for interactive UI (cart drawer, checkout form, product filters). TanStack Query for client-side data fetching with HydrationBoundary for SSR prefetch. Zustand cart/auth store for client state. URL search params for filters.

**Tech Stack:** Next.js 16, React 19, TypeScript, TanStack Query 5, Zustand 5, React Hook Form 7, Zod 4, Vaul (drawer), Framer Motion, Lucide React, Tailwind v4

**Key Next.js 16 rules:**
- `params` and `searchParams` are Promises → always `await` or `use()` in client components
- `cookies()` from `next/headers` is async → `await cookies()`

---

## File Map

| File | Role |
|---|---|
| `(shop)/_lib/types.ts` | Re-export Product, Order, CartItem types |
| `(shop)/_lib/schemas.ts` | checkoutSchema, filterSchema, addressSchema |
| `(shop)/_lib/query-keys.ts` | productKeys, orderKeys, categoryKeys |
| `(shop)/_lib/actions.ts` | createOrder, cancelOrder, applyVoucher, fetchProfile, updateProfile |
| `(shop)/_lib/hooks.ts` | useProducts, useProduct, useCategories, useCreateOrder, useCancelOrder, useOrders, useOrder, useProfile, useUpdateProfile |
| `(shop)/_components/order-status-badge.tsx` | Status badge (pure display) |
| `(shop)/_components/product-card.tsx` | Product card with image, name, price |
| `(shop)/_components/product-grid.tsx` | Grid of ProductCard, shows skeleton while loading |
| `(shop)/_components/product-filters.tsx` | Search, category, price filters using URL params |
| `(shop)/_components/product-gallery.tsx` | Image gallery with zoom/lightbox |
| `(shop)/_components/add-to-cart-button.tsx` | Button with quantity input, uses cartStore |
| `(shop)/_components/cart-item.tsx` | Single cart item row with qty controls |
| `(shop)/_components/cart-drawer.tsx` | Vaul drawer showing cart items |
| `(shop)/_components/payment-method-selector.tsx` | Radio group for COD/VNPay/Momo/ZaloPay |
| `(shop)/_components/checkout-form.tsx` | Full checkout form with RHF + payment |
| `products/page.tsx` | Product listing with filters + HydrationBoundary |
| `products/loading.tsx` | ProductGridSkeleton |
| `products/[slug]/page.tsx` | Product detail with generateMetadata + JSON-LD |
| `products/[slug]/loading.tsx` | Detail skeleton |
| `products/[slug]/not-found.tsx` | Product not found |
| `cart/page.tsx` | Cart page (client, reads from cartStore) |
| `cart/loading.tsx` | Cart skeleton |
| `checkout/page.tsx` | Checkout page |
| `checkout/loading.tsx` | Checkout skeleton |
| `checkout/success/page.tsx` | Order confirmation |
| `checkout/success/loading.tsx` | Success skeleton |
| `orders/page.tsx` | Order list (Server Component) |
| `orders/loading.tsx` | Order list skeleton |
| `orders/[id]/page.tsx` | Order detail + cancel button |
| `orders/[id]/loading.tsx` | Order detail skeleton |
| `profile/page.tsx` | Profile edit form |
| `profile/loading.tsx` | Profile skeleton |
| `app/api/payment/cod/confirm/route.ts` | COD confirm proxy |
| `app/api/payment/vnpay/create/route.ts` | VNPay create URL |
| `app/api/payment/vnpay/callback/route.ts` | VNPay HMAC verify |
| `app/api/payment/momo/create/route.ts` | Momo create request |
| `app/api/payment/momo/callback/route.ts` | Momo IPN webhook |
| `app/api/payment/zalopay/create/route.ts` | ZaloPay create order |
| `app/api/payment/zalopay/callback/route.ts` | ZaloPay callback |

All paths below are relative to `src/app/[locale]/(shop)/` unless prefixed with `src/app/`.

---

## Task 1: Types, schemas, and query keys

**Files:**
- Create: `src/app/[locale]/(shop)/_lib/types.ts`
- Create: `src/app/[locale]/(shop)/_lib/schemas.ts`
- Create: `src/app/[locale]/(shop)/_lib/query-keys.ts`

- [ ] **Step 1: Create `types.ts`**

```ts
// src/app/[locale]/(shop)/_lib/types.ts
export type { Product, ProductList, ProductFilters } from "@/shared/types/product";
export type { Order, OrderItem, OrderStatus, PaymentMethod, PaymentStatus } from "@/shared/types/order";
export type { CartItem } from "@/shared/stores/cart-store";
export type { User }     from "@/shared/types/user";
```

- [ ] **Step 2: Create `schemas.ts`**

```ts
// src/app/[locale]/(shop)/_lib/schemas.ts
import { z } from "zod";

export const addressSchema = z.object({
  fullName: z.string().min(1, "Vui lòng nhập họ tên"),
  phone:    z.string().regex(/^0\d{9}$/, "Số điện thoại không hợp lệ"),
  address:  z.string().min(5, "Vui lòng nhập địa chỉ"),
  city:     z.string().min(1, "Vui lòng chọn tỉnh/thành"),
});

export const checkoutSchema = addressSchema.extend({
  paymentMethod: z.enum(["cod", "vnpay", "momo", "zalopay"]),
  note:          z.string().optional(),
  voucherCode:   z.string().optional(),
});

export const filterSchema = z.object({
  search:   z.string().optional(),
  category: z.string().optional(),
  minPrice: z.coerce.number().optional(),
  maxPrice: z.coerce.number().optional(),
  ordering: z.enum(["price", "-price", "-created_at", "rating"]).optional(),
  page:     z.coerce.number().default(1),
});

export type AddressInput  = z.infer<typeof addressSchema>;
export type CheckoutInput = z.infer<typeof checkoutSchema>;
export type FilterInput   = z.infer<typeof filterSchema>;
```

- [ ] **Step 3: Create `query-keys.ts`**

```ts
// src/app/[locale]/(shop)/_lib/query-keys.ts
import type { ProductFilters } from "./types";

export const productKeys = {
  all:        ["products"] as const,
  list:       (filters: ProductFilters) => [...productKeys.all, "list", filters] as const,
  detail:     (slug: string)            => [...productKeys.all, "detail", slug]  as const,
  categories: ()                        => [...productKeys.all, "categories"]    as const,
};

export const orderKeys = {
  all:    ["orders"] as const,
  list:   ()           => [...orderKeys.all, "list"]        as const,
  detail: (id: string) => [...orderKeys.all, "detail", id]  as const,
};

export const profileKey = ["profile"] as const;
```

- [ ] **Step 4: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 5: Commit**

```bash
git add "src/app/[locale]/(shop)/_lib/types.ts" "src/app/[locale]/(shop)/_lib/schemas.ts" "src/app/[locale]/(shop)/_lib/query-keys.ts"
git commit -m "feat(shop): add types, schemas, and query keys"
```

---

## Task 2: Actions and hooks

**Files:**
- Create: `src/app/[locale]/(shop)/_lib/actions.ts`
- Create: `src/app/[locale]/(shop)/_lib/hooks.ts`

- [ ] **Step 1: Create `actions.ts`**

```ts
// src/app/[locale]/(shop)/_lib/actions.ts
import { http }  from "@/shared/lib/http/methods";
import { API }   from "@/shared/constants/api-endpoints";
import type { Product, ProductList, Order } from "./types";
import type { CheckoutInput } from "./schemas";
import type { User } from "./types";

export const productActions = {
  list:       (filters: object)   => http.get<ProductList>(API.PRODUCTS.LIST, filters),
  detail:     (slug: string)      => http.get<Product>(API.PRODUCTS.DETAIL(slug)),
  categories: ()                  => http.get<{ id: number; name: string; slug: string }[]>(API.PRODUCTS.CATEGORIES),
};

export const orderActions = {
  list:   ()           => http.get<Order[]>(API.ORDERS.LIST),
  detail: (id: string) => http.get<Order>(API.ORDERS.DETAIL(id)),
  cancel: (id: string) => http.post<Order>(API.ORDERS.CANCEL(id)),
  create: (data: CheckoutInput & { items: { variantId: string; quantity: number }[] }) =>
    http.post<Order>(API.ORDERS.LIST, data),
};

export const profileActions = {
  get:    ()           => http.get<User>(API.PROFILE.ME),
  update: (data: Partial<User>) => http.patch<User>(API.PROFILE.UPDATE, data),
};
```

- [ ] **Step 2: Create `hooks.ts`**

```ts
// src/app/[locale]/(shop)/_lib/hooks.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter, usePathname }                from "next/navigation";
import { toast }                                  from "sonner";
import { useCartStore }                           from "@/shared/stores/cart-store";
import { productActions, orderActions, profileActions } from "./actions";
import { productKeys, orderKeys, profileKey }          from "./query-keys";
import type { ProductFilters } from "./types";
import type { CheckoutInput }  from "./schemas";

export function useProducts(filters: ProductFilters) {
  return useQuery({
    queryKey:  productKeys.list(filters),
    queryFn:   () => productActions.list(filters),
    staleTime: 60_000,
  });
}

export function useProduct(slug: string) {
  return useQuery({
    queryKey: productKeys.detail(slug),
    queryFn:  () => productActions.detail(slug),
    staleTime: 5 * 60_000,
  });
}

export function useCategories() {
  return useQuery({
    queryKey:  productKeys.categories(),
    queryFn:   productActions.categories,
    staleTime: 10 * 60_000,
  });
}

export function useOrders() {
  return useQuery({
    queryKey: orderKeys.list(),
    queryFn:  orderActions.list,
  });
}

export function useOrder(id: string) {
  return useQuery({
    queryKey: orderKeys.detail(id),
    queryFn:  () => orderActions.detail(id),
  });
}

export function useCreateOrder(locale: string) {
  const qc        = useQueryClient();
  const router    = useRouter();
  const clearCart = useCartStore((s) => s.clearCart);
  const items     = useCartStore((s) => s.items);

  return useMutation({
    mutationFn: (data: CheckoutInput) =>
      orderActions.create({ ...data, items: items.map((i) => ({ variantId: i.variantId, quantity: i.quantity })) }),
    onSuccess: (order) => {
      clearCart();
      qc.invalidateQueries({ queryKey: orderKeys.list() });
      toast.success("Đặt hàng thành công!");
      router.push(`/${locale}/checkout/success?orderId=${order.id}`);
    },
  });
}

export function useCancelOrder(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => orderActions.cancel(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: orderKeys.detail(id) });
      qc.invalidateQueries({ queryKey: orderKeys.list() });
      toast.success("Đã huỷ đơn hàng");
    },
  });
}

export function useProfile() {
  return useQuery({ queryKey: profileKey, queryFn: profileActions.get });
}

export function useUpdateProfile() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: profileActions.update,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: profileKey });
      toast.success("Cập nhật thông tin thành công");
    },
  });
}
```

- [ ] **Step 3: Write hooks test**

```ts
// src/app/[locale]/(shop)/_lib/hooks.test.ts
import { renderHook, waitFor } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { server } from "@/__tests__/helpers/mock-handlers";
import { http as mswHttp, HttpResponse } from "msw";
import { renderWithProviders } from "@/__tests__/helpers/render";
import { useProducts } from "./hooks";

describe("useProducts", () => {
  it("fetches product list", async () => {
    server.use(
      mswHttp.get("/api/products/", () =>
        HttpResponse.json({ results: [{ id: 1, name: "Test", slug: "test", price: 100000 }], count: 1, next: null, previous: null }),
      ),
    );

    const wrapper = ({ children }: { children: React.ReactNode }) =>
      renderWithProviders(children as React.ReactElement).container.firstChild as React.FC;

    const { result } = renderHook(() => useProducts({}), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.results).toHaveLength(1);
  });
});
```

- [ ] **Step 4: Run test**

```bash
npx vitest run "src/app/\\[locale\\]/\\(shop\\)/_lib/hooks.test.ts" 2>&1 | tail -15
```

- [ ] **Step 5: Commit**

```bash
git add "src/app/[locale]/(shop)/_lib/actions.ts" "src/app/[locale]/(shop)/_lib/hooks.ts" "src/app/[locale]/(shop)/_lib/hooks.test.ts"
git commit -m "feat(shop): add product/order/profile actions and hooks"
```

---

## Task 3: Status badge and product card

**Files:**
- Create: `src/app/[locale]/(shop)/_components/order-status-badge.tsx`
- Create: `src/app/[locale]/(shop)/_components/product-card.tsx`

- [ ] **Step 1: Create `order-status-badge.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/order-status-badge.tsx
import { Badge } from "@/shared/components/ui/badge";
import type { OrderStatus } from "../_lib/types";

const STATUS_MAP: Record<OrderStatus, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
  pending:    { label: "Chờ xác nhận", variant: "secondary" },
  confirmed:  { label: "Đã xác nhận", variant: "default" },
  processing: { label: "Đang xử lý",  variant: "default" },
  shipped:    { label: "Đang giao",    variant: "default" },
  delivered:  { label: "Đã giao",     variant: "outline" },
  cancelled:  { label: "Đã huỷ",      variant: "destructive" },
};

export function OrderStatusBadge({ status }: { status: OrderStatus }) {
  const { label, variant } = STATUS_MAP[status] ?? { label: status, variant: "secondary" };
  return <Badge variant={variant}>{label}</Badge>;
}
```

- [ ] **Step 2: Create `product-card.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/product-card.tsx
import Link   from "next/link";
import Image  from "next/image";
import { Badge } from "@/shared/components/ui/badge";
import type { Product } from "../_lib/types";

function formatVND(amount: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(amount);
}

export function ProductCard({ product, locale }: { product: Product; locale: string }) {
  const displayPrice = product.salePrice ?? product.price;
  const hasDiscount  = product.salePrice !== null && product.salePrice < product.price;

  return (
    <Link
      href={`/${locale}/products/${product.slug}`}
      className="group flex flex-col rounded-xl border bg-background p-3 transition hover:shadow-md"
    >
      <div className="relative mb-3 aspect-square overflow-hidden rounded-lg bg-muted">
        {product.images[0] ? (
          <Image
            src={product.images[0]}
            alt={product.name}
            fill
            className="object-cover transition duration-300 group-hover:scale-105"
            sizes="(max-width: 768px) 50vw, 25vw"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-muted-foreground text-sm">
            Không có ảnh
          </div>
        )}
        {hasDiscount && (
          <Badge className="absolute left-2 top-2 bg-red-500 text-white">Sale</Badge>
        )}
        {product.stock === 0 && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-white text-sm font-medium">
            Hết hàng
          </div>
        )}
      </div>

      <p className="mb-1 line-clamp-2 text-sm font-medium leading-snug">{product.name}</p>

      <div className="mt-auto flex items-center gap-2">
        <span className="font-semibold text-primary">{formatVND(displayPrice)}</span>
        {hasDiscount && (
          <span className="text-xs text-muted-foreground line-through">
            {formatVND(product.price)}
          </span>
        )}
      </div>
    </Link>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add "src/app/[locale]/(shop)/_components/order-status-badge.tsx" "src/app/[locale]/(shop)/_components/product-card.tsx"
git commit -m "feat(shop): add order-status-badge and product-card components"
```

---

## Task 4: Product grid and filters

**Files:**
- Create: `src/app/[locale]/(shop)/_components/product-grid.tsx`
- Create: `src/app/[locale]/(shop)/_components/product-filters.tsx`

- [ ] **Step 1: Create `product-grid.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/product-grid.tsx
"use client";

import { ProductGridSkeleton } from "@/shared/components/skeletons/product-grid-skeleton";
import { ProductCard }         from "./product-card";
import { useProducts }         from "../_lib/hooks";
import type { ProductFilters } from "../_lib/types";

export function ProductGrid({ filters, locale }: { filters: ProductFilters; locale: string }) {
  const { data, isPending } = useProducts(filters);

  if (isPending) return <ProductGridSkeleton />;

  if (!data || data.results.length === 0) {
    return (
      <div className="py-20 text-center text-muted-foreground">
        Không tìm thấy sản phẩm nào.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-4">
      {data.results.map((product) => (
        <ProductCard key={product.id} product={product} locale={locale} />
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Create `product-filters.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/product-filters.tsx
"use client";

import { use, useCallback }     from "react";
import { useRouter, usePathname } from "next/navigation";
import { useDebounce }           from "@/shared/hooks/use-debounce";
import { Input }                 from "@/shared/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select";
import { useCategories }         from "../_lib/hooks";

export function ProductFilters({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | undefined>>;
}) {
  const params   = use(searchParams);
  const router   = useRouter();
  const pathname = usePathname();

  function updateParam(key: string, value: string | undefined) {
    const sp = new URLSearchParams(params as Record<string, string>);
    if (value) sp.set(key, value);
    else sp.delete(key);
    sp.delete("page"); // reset page on filter change
    router.replace(`${pathname}?${sp.toString()}`);
  }

  const { data: categories } = useCategories();

  return (
    <div className="flex flex-wrap gap-3">
      <Input
        placeholder="Tìm kiếm sản phẩm..."
        defaultValue={params.search ?? ""}
        onChange={(e) => updateParam("search", e.target.value || undefined)}
        className="w-full md:w-64"
      />

      <Select
        defaultValue={params.category ?? "all"}
        onValueChange={(v) => updateParam("category", v === "all" ? undefined : v)}
      >
        <SelectTrigger className="w-44">
          <SelectValue placeholder="Danh mục" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Tất cả danh mục</SelectItem>
          {categories?.map((c) => (
            <SelectItem key={c.id} value={c.slug}>{c.name}</SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
        defaultValue={params.ordering ?? "-created_at"}
        onValueChange={(v) => updateParam("ordering", v)}
      >
        <SelectTrigger className="w-44">
          <SelectValue placeholder="Sắp xếp" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="-created_at">Mới nhất</SelectItem>
          <SelectItem value="price">Giá tăng dần</SelectItem>
          <SelectItem value="-price">Giá giảm dần</SelectItem>
          <SelectItem value="rating">Đánh giá cao</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add "src/app/[locale]/(shop)/_components/product-grid.tsx" "src/app/[locale]/(shop)/_components/product-filters.tsx"
git commit -m "feat(shop): add product-grid and product-filters components"
```

---

## Task 5: Product gallery

**Files:**
- Create: `src/app/[locale]/(shop)/_components/product-gallery.tsx`

- [ ] **Step 1: Create `product-gallery.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/product-gallery.tsx
"use client";

import { useState } from "react";
import Image        from "next/image";
import { cn }       from "@/shared/lib/utils";

export function ProductGallery({ images, name }: { images: string[]; name: string }) {
  const [activeIndex, setActiveIndex] = useState(0);

  if (images.length === 0) {
    return (
      <div className="flex aspect-square items-center justify-center rounded-xl bg-muted text-muted-foreground">
        Không có ảnh
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="relative aspect-square overflow-hidden rounded-xl bg-muted">
        <Image
          src={images[activeIndex]}
          alt={name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 50vw"
          priority
        />
      </div>

      {images.length > 1 && (
        <div className="flex gap-2 overflow-x-auto pb-1">
          {images.map((src, i) => (
            <button
              key={i}
              onClick={() => setActiveIndex(i)}
              className={cn(
                "relative h-16 w-16 flex-shrink-0 overflow-hidden rounded-lg border-2 transition",
                i === activeIndex ? "border-primary" : "border-transparent opacity-60 hover:opacity-100",
              )}
            >
              <Image src={src} alt={`${name} ${i + 1}`} fill className="object-cover" sizes="64px" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add "src/app/[locale]/(shop)/_components/product-gallery.tsx"
git commit -m "feat(shop): add product-gallery component"
```

---

## Task 6: Cart components

**Files:**
- Create: `src/app/[locale]/(shop)/_components/add-to-cart-button.tsx`
- Create: `src/app/[locale]/(shop)/_components/cart-item.tsx`
- Create: `src/app/[locale]/(shop)/_components/cart-drawer.tsx`

- [ ] **Step 1: Create `add-to-cart-button.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/add-to-cart-button.tsx
"use client";

import { useState, useTransition } from "react";
import { toast }                   from "sonner";
import { ShoppingCart, Minus, Plus } from "lucide-react";
import { Button }                  from "@/shared/components/ui/button";
import { Input }                   from "@/shared/components/ui/input";
import { useCartStore }            from "@/shared/stores/cart-store";
import type { Product }            from "../_lib/types";

export function AddToCartButton({ product }: { product: Product }) {
  const [qty, setQty]     = useState(1);
  const [, startTransition] = useTransition();
  const addToCart          = useCartStore((s) => s.addToCart);

  function handleAdd() {
    if (product.stock === 0) return;
    startTransition(() => {
      addToCart({
        variantId: String(product.id),
        productId: String(product.id),
        name:      product.name,
        image:     product.images[0] ?? "",
        price:     product.salePrice ?? product.price,
        quantity:  qty,
      });
      toast.success("Đã thêm vào giỏ hàng");
    });
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setQty((q) => Math.max(1, q - 1))}
          disabled={qty <= 1}
        >
          <Minus className="h-4 w-4" />
        </Button>
        <Input
          type="number"
          value={qty}
          min={1}
          max={product.stock}
          onChange={(e) => setQty(Math.min(product.stock, Math.max(1, Number(e.target.value))))}
          className="w-16 text-center"
        />
        <Button
          variant="outline"
          size="icon"
          onClick={() => setQty((q) => Math.min(product.stock, q + 1))}
          disabled={qty >= product.stock}
        >
          <Plus className="h-4 w-4" />
        </Button>
      </div>

      <Button
        className="w-full"
        onClick={handleAdd}
        disabled={product.stock === 0}
      >
        <ShoppingCart className="mr-2 h-4 w-4" />
        {product.stock === 0 ? "Hết hàng" : "Thêm vào giỏ"}
      </Button>
    </div>
  );
}
```

- [ ] **Step 2: Create `cart-item.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/cart-item.tsx
"use client";

import Image                  from "next/image";
import { Trash2, Minus, Plus } from "lucide-react";
import { Button }              from "@/shared/components/ui/button";
import { useCartStore }        from "@/shared/stores/cart-store";
import type { CartItem }       from "../_lib/types";

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

export function CartItemRow({ item }: { item: CartItem }) {
  const updateQuantity = useCartStore((s) => s.updateQuantity);
  const removeCartItem = useCartStore((s) => s.removeCartItem);

  return (
    <div className="flex gap-3 py-3">
      <div className="relative h-16 w-16 flex-shrink-0 overflow-hidden rounded-lg bg-muted">
        {item.image && (
          <Image src={item.image} alt={item.name} fill className="object-cover" sizes="64px" />
        )}
      </div>

      <div className="flex flex-1 flex-col gap-1">
        <p className="line-clamp-2 text-sm font-medium">{item.name}</p>
        <p className="text-sm font-semibold text-primary">{formatVND(item.price)}</p>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="icon"
            className="h-7 w-7"
            onClick={() =>
              item.quantity > 1
                ? updateQuantity(item.variantId, item.quantity - 1)
                : removeCartItem(item.variantId)
            }
          >
            <Minus className="h-3 w-3" />
          </Button>
          <span className="w-6 text-center text-sm">{item.quantity}</span>
          <Button
            variant="outline"
            size="icon"
            className="h-7 w-7"
            onClick={() => updateQuantity(item.variantId, item.quantity + 1)}
          >
            <Plus className="h-3 w-3" />
          </Button>

          <Button
            variant="ghost"
            size="icon"
            className="ml-auto h-7 w-7 text-destructive hover:text-destructive"
            onClick={() => removeCartItem(item.variantId)}
          >
            <Trash2 className="h-3 w-3" />
          </Button>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Create `cart-drawer.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/cart-drawer.tsx
"use client";

import Link                from "next/link";
import { ShoppingCart }    from "lucide-react";
import { Drawer }          from "vaul";
import { Button }          from "@/shared/components/ui/button";
import { Badge }           from "@/shared/components/ui/badge";
import { Separator }       from "@/shared/components/ui/separator";
import { useCartStore }    from "@/shared/stores/cart-store";
import { CartItemRow }     from "./cart-item";

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

export function CartDrawer({ locale }: { locale: string }) {
  const items     = useCartStore((s) => s.items);
  const itemCount = useCartStore((s) => s.itemCount);
  const total     = useCartStore((s) => s.total);

  return (
    <Drawer.Root>
      <Drawer.Trigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <ShoppingCart className="h-5 w-5" />
          {itemCount > 0 && (
            <Badge className="absolute -right-1 -top-1 h-4 w-4 rounded-full p-0 text-[10px]">
              {itemCount > 99 ? "99+" : itemCount}
            </Badge>
          )}
        </Button>
      </Drawer.Trigger>

      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/40" />
        <Drawer.Content className="fixed bottom-0 right-0 top-0 flex w-full max-w-sm flex-col bg-background shadow-xl">
          <div className="flex items-center justify-between border-b px-4 py-3">
            <Drawer.Title className="font-semibold">
              Giỏ hàng ({itemCount})
            </Drawer.Title>
            <Drawer.Close asChild>
              <Button variant="ghost" size="sm">Đóng</Button>
            </Drawer.Close>
          </div>

          <div className="flex-1 overflow-y-auto px-4">
            {items.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center gap-3 text-muted-foreground">
                <ShoppingCart className="h-12 w-12 opacity-30" />
                <p className="text-sm">Giỏ hàng trống</p>
              </div>
            ) : (
              <div className="divide-y">
                {items.map((item) => (
                  <CartItemRow key={item.variantId} item={item} />
                ))}
              </div>
            )}
          </div>

          {items.length > 0 && (
            <div className="border-t p-4">
              <div className="mb-3 flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Tổng cộng</span>
                <span className="font-semibold">{formatVND(total)}</span>
              </div>
              <Drawer.Close asChild>
                <Button className="w-full" asChild>
                  <Link href={`/${locale}/checkout`}>Thanh toán</Link>
                </Button>
              </Drawer.Close>
            </div>
          )}
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add "src/app/[locale]/(shop)/_components/"
git commit -m "feat(shop): add add-to-cart-button, cart-item, cart-drawer components"
```

---

## Task 7: Payment selector and checkout form

**Files:**
- Create: `src/app/[locale]/(shop)/_components/payment-method-selector.tsx`
- Create: `src/app/[locale]/(shop)/_components/checkout-form.tsx`

- [ ] **Step 1: Create `payment-method-selector.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/payment-method-selector.tsx
"use client";

import { cn } from "@/shared/lib/utils";
import type { PaymentMethod } from "../_lib/types";

const METHODS: { value: PaymentMethod; label: string; icon: string }[] = [
  { value: "cod",     label: "Thanh toán khi nhận hàng (COD)", icon: "💵" },
  { value: "vnpay",   label: "VNPay",                           icon: "🏦" },
  { value: "momo",    label: "Momo",                            icon: "🟣" },
  { value: "zalopay", label: "ZaloPay",                         icon: "🔵" },
];

export function PaymentMethodSelector({
  value,
  onChange,
}: {
  value: PaymentMethod;
  onChange: (v: PaymentMethod) => void;
}) {
  return (
    <div className="grid gap-2">
      {METHODS.map((m) => (
        <button
          key={m.value}
          type="button"
          onClick={() => onChange(m.value)}
          className={cn(
            "flex items-center gap-3 rounded-lg border p-3 text-left transition",
            value === m.value ? "border-primary bg-primary/5" : "hover:bg-muted",
          )}
        >
          <span className="text-2xl">{m.icon}</span>
          <span className="text-sm font-medium">{m.label}</span>
          <div
            className={cn(
              "ml-auto h-4 w-4 rounded-full border-2",
              value === m.value ? "border-primary bg-primary" : "border-muted-foreground",
            )}
          />
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Create `checkout-form.tsx`**

```tsx
// src/app/[locale]/(shop)/_components/checkout-form.tsx
"use client";

import { Controller, useForm } from "react-hook-form";
import { zodResolver }          from "@hookform/resolvers/zod";
import { Button }               from "@/shared/components/ui/button";
import { Input }                from "@/shared/components/ui/input";
import { Label }                from "@/shared/components/ui/label";
import { Textarea }             from "@/shared/components/ui/textarea";
import { Separator }            from "@/shared/components/ui/separator";
import { useCartStore }         from "@/shared/stores/cart-store";
import { PaymentMethodSelector } from "./payment-method-selector";
import { useCreateOrder }        from "../_lib/hooks";
import { checkoutSchema }        from "../_lib/schemas";
import type { CheckoutInput }    from "../_lib/schemas";

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

export function CheckoutForm({ locale }: { locale: string }) {
  const createOrder = useCreateOrder(locale);
  const items       = useCartStore((s) => s.items);
  const total       = useCartStore((s) => s.total);

  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<CheckoutInput>({
    resolver:      zodResolver(checkoutSchema),
    defaultValues: { paymentMethod: "cod" },
  });

  return (
    <div className="grid gap-6 md:grid-cols-[1fr_360px]">
      <form
        id="checkout-form"
        onSubmit={handleSubmit((d) => createOrder.mutate(d))}
        className="space-y-5"
      >
        <section>
          <h2 className="mb-3 font-semibold">Thông tin giao hàng</h2>
          <div className="space-y-3">
            <div>
              <Label htmlFor="fullName">Họ và tên</Label>
              <Input id="fullName" placeholder="Nguyễn Văn A" {...register("fullName")} />
              {errors.fullName && <p className="mt-1 text-sm text-destructive">{errors.fullName.message}</p>}
            </div>
            <div>
              <Label htmlFor="phone">Số điện thoại</Label>
              <Input id="phone" placeholder="0901234567" {...register("phone")} />
              {errors.phone && <p className="mt-1 text-sm text-destructive">{errors.phone.message}</p>}
            </div>
            <div>
              <Label htmlFor="address">Địa chỉ</Label>
              <Input id="address" placeholder="Số nhà, tên đường, phường/xã" {...register("address")} />
              {errors.address && <p className="mt-1 text-sm text-destructive">{errors.address.message}</p>}
            </div>
            <div>
              <Label htmlFor="city">Tỉnh/Thành phố</Label>
              <Input id="city" placeholder="Hồ Chí Minh" {...register("city")} />
              {errors.city && <p className="mt-1 text-sm text-destructive">{errors.city.message}</p>}
            </div>
            <div>
              <Label htmlFor="note">Ghi chú (tuỳ chọn)</Label>
              <Textarea id="note" placeholder="Giao hàng giờ hành chính..." {...register("note")} />
            </div>
          </div>
        </section>

        <Separator />

        <section>
          <h2 className="mb-3 font-semibold">Phương thức thanh toán</h2>
          <Controller
            control={control}
            name="paymentMethod"
            render={({ field }) => (
              <PaymentMethodSelector value={field.value} onChange={field.onChange} />
            )}
          />
        </section>
      </form>

      {/* Order summary */}
      <div className="rounded-xl border p-4">
        <h2 className="mb-3 font-semibold">Đơn hàng ({items.length} sản phẩm)</h2>
        <div className="space-y-2 text-sm">
          {items.map((item) => (
            <div key={item.variantId} className="flex justify-between">
              <span className="line-clamp-1 flex-1">{item.name} x{item.quantity}</span>
              <span className="ml-2 font-medium">{formatVND(item.price * item.quantity)}</span>
            </div>
          ))}
        </div>
        <Separator className="my-3" />
        <div className="flex justify-between font-semibold">
          <span>Tổng cộng</span>
          <span className="text-primary">{formatVND(total)}</span>
        </div>
        <Button
          type="submit"
          form="checkout-form"
          className="mt-4 w-full"
          disabled={createOrder.isPending || items.length === 0}
        >
          {createOrder.isPending ? "Đang đặt hàng..." : "Đặt hàng"}
        </Button>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add "src/app/[locale]/(shop)/_components/payment-method-selector.tsx" "src/app/[locale]/(shop)/_components/checkout-form.tsx"
git commit -m "feat(shop): add payment-method-selector and checkout-form components"
```

---

## Task 8: Product pages

**Files:**
- Create: `src/app/[locale]/(shop)/products/page.tsx`
- Create: `src/app/[locale]/(shop)/products/loading.tsx`
- Create: `src/app/[locale]/(shop)/products/[slug]/page.tsx`
- Create: `src/app/[locale]/(shop)/products/[slug]/loading.tsx`
- Create: `src/app/[locale]/(shop)/products/[slug]/not-found.tsx`

- [ ] **Step 1: Create products listing page**

```tsx
// src/app/[locale]/(shop)/products/page.tsx
import { Suspense }             from "react";
import { ProductFilters }        from "../_components/product-filters";
import { ProductGrid }           from "../_components/product-grid";
import { ProductGridSkeleton }   from "@/shared/components/skeletons/product-grid-skeleton";

export default async function ProductsPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | undefined>>;
}) {
  const { locale } = await params;
  const sp         = await searchParams;

  const filters = {
    search:   sp.search,
    category: sp.category,
    ordering: sp.ordering as "-created_at" | "price" | "-price" | "rating" | undefined,
    page:     sp.page ? Number(sp.page) : 1,
  };

  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Sản phẩm</h1>
      <div className="mb-6">
        <ProductFilters searchParams={searchParams} />
      </div>
      <Suspense fallback={<ProductGridSkeleton />}>
        <ProductGrid filters={filters} locale={locale} />
      </Suspense>
    </main>
  );
}
```

- [ ] **Step 2: Create products loading**

```tsx
// src/app/[locale]/(shop)/products/loading.tsx
import { ProductGridSkeleton } from "@/shared/components/skeletons/product-grid-skeleton";

export default function ProductsLoading() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <div className="mb-6 h-8 w-32 animate-pulse rounded bg-muted" />
      <div className="mb-6 h-10 w-full animate-pulse rounded bg-muted" />
      <ProductGridSkeleton />
    </main>
  );
}
```

- [ ] **Step 3: Create product detail page**

```tsx
// src/app/[locale]/(shop)/products/[slug]/page.tsx
import { notFound }          from "next/navigation";
import type { Metadata }     from "next";
import { http }              from "@/shared/lib/http/methods";
import { API }               from "@/shared/constants/api-endpoints";
import type { Product }      from "../../_lib/types";
import { ProductGallery }    from "../../_components/product-gallery";
import { AddToCartButton }   from "../../_components/add-to-cart-button";
import { OrderStatusBadge }  from "../../_components/order-status-badge";

type Props = { params: Promise<{ locale: string; slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  try {
    const product = await http.get<Product>(API.PRODUCTS.DETAIL(slug));
    return {
      title:       product.name,
      description: product.description.slice(0, 160),
      openGraph:   { images: product.images[0] ? [product.images[0]] : [] },
    };
  } catch {
    return { title: "Sản phẩm không tồn tại" };
  }
}

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

export default async function ProductDetailPage({ params }: Props) {
  const { slug, locale } = await params;

  let product: Product;
  try {
    product = await http.get<Product>(API.PRODUCTS.DETAIL(slug));
  } catch {
    notFound();
  }

  const jsonLd = {
    "@context":   "https://schema.org",
    "@type":      "Product",
    name:         product.name,
    description:  product.description,
    image:        product.images,
    offers: {
      "@type":       "Offer",
      price:         product.salePrice ?? product.price,
      priceCurrency: "VND",
      availability:  product.stock > 0 ? "InStock" : "OutOfStock",
    },
  };

  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <div className="grid gap-8 md:grid-cols-2">
        <ProductGallery images={product.images} name={product.name} />

        <div className="flex flex-col gap-4">
          <div>
            <p className="text-sm text-muted-foreground">{product.category.name}</p>
            <h1 className="mt-1 text-2xl font-bold">{product.name}</h1>
          </div>

          <div className="flex items-baseline gap-3">
            <span className="text-3xl font-bold text-primary">
              {formatVND(product.salePrice ?? product.price)}
            </span>
            {product.salePrice !== null && (
              <span className="text-lg text-muted-foreground line-through">
                {formatVND(product.price)}
              </span>
            )}
          </div>

          <p className="text-sm text-muted-foreground">
            {product.stock > 0 ? `Còn ${product.stock} sản phẩm` : "Hết hàng"}
          </p>

          <AddToCartButton product={product} />

          <div className="rounded-lg bg-muted/50 p-4">
            <h2 className="mb-2 font-semibold">Mô tả sản phẩm</h2>
            <p className="text-sm leading-relaxed text-muted-foreground">{product.description}</p>
          </div>
        </div>
      </div>
    </main>
  );
}
```

- [ ] **Step 4: Create detail loading and not-found**

```tsx
// src/app/[locale]/(shop)/products/[slug]/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function ProductDetailLoading() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <div className="grid gap-8 md:grid-cols-2">
        <Skeleton className="aspect-square rounded-xl" />
        <div className="flex flex-col gap-4">
          <Skeleton className="h-6 w-24" />
          <Skeleton className="h-8 w-3/4" />
          <Skeleton className="h-10 w-1/3" />
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-32 w-full" />
        </div>
      </div>
    </main>
  );
}
```

```tsx
// src/app/[locale]/(shop)/products/[slug]/not-found.tsx
import Link   from "next/link";
import { Button } from "@/shared/components/ui/button";

export default function ProductNotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
      <h1 className="text-2xl font-semibold">Sản phẩm không tồn tại</h1>
      <p className="text-muted-foreground">Sản phẩm bạn tìm kiếm không còn tồn tại hoặc đã bị xoá.</p>
      <Button asChild variant="outline">
        <Link href="/vi/products">Xem tất cả sản phẩm</Link>
      </Button>
    </div>
  );
}
```

- [ ] **Step 5: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 6: Commit**

```bash
git add "src/app/[locale]/(shop)/products/"
git commit -m "feat(shop): add product listing and detail pages"
```

---

## Task 9: Cart and checkout pages

**Files:**
- Create: `src/app/[locale]/(shop)/cart/page.tsx`
- Create: `src/app/[locale]/(shop)/cart/loading.tsx`
- Create: `src/app/[locale]/(shop)/checkout/page.tsx`
- Create: `src/app/[locale]/(shop)/checkout/loading.tsx`
- Create: `src/app/[locale]/(shop)/checkout/success/page.tsx`
- Create: `src/app/[locale]/(shop)/checkout/success/loading.tsx`

- [ ] **Step 1: Create cart page**

```tsx
// src/app/[locale]/(shop)/cart/page.tsx
"use client";

import { use }          from "react";
import Link              from "next/link";
import { Button }        from "@/shared/components/ui/button";
import { Separator }     from "@/shared/components/ui/separator";
import { useCartStore }  from "@/shared/stores/cart-store";
import { CartItemRow }   from "../_components/cart-item";

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

export default function CartPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  const items      = useCartStore((s) => s.items);
  const total      = useCartStore((s) => s.total);

  if (items.length === 0) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
        <h1 className="text-xl font-semibold">Giỏ hàng trống</h1>
        <Button asChild variant="outline">
          <Link href={`/${locale}/products`}>Tiếp tục mua sắm</Link>
        </Button>
      </div>
    );
  }

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Giỏ hàng</h1>
      <div className="divide-y rounded-xl border">
        {items.map((item) => (
          <div key={item.variantId} className="px-4">
            <CartItemRow item={item} />
          </div>
        ))}
      </div>
      <div className="mt-6 rounded-xl border p-4">
        <div className="flex justify-between font-semibold">
          <span>Tổng cộng</span>
          <span className="text-primary">{formatVND(total)}</span>
        </div>
        <Button className="mt-4 w-full" asChild>
          <Link href={`/${locale}/checkout`}>Tiến hành thanh toán</Link>
        </Button>
      </div>
    </main>
  );
}
```

- [ ] **Step 2: Create cart loading**

```tsx
// src/app/[locale]/(shop)/cart/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function CartLoading() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <Skeleton className="mb-6 h-8 w-40" />
      <div className="space-y-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-24 w-full rounded-xl" />
        ))}
      </div>
    </main>
  );
}
```

- [ ] **Step 3: Create checkout page**

```tsx
// src/app/[locale]/(shop)/checkout/page.tsx
"use client";

import { use }          from "react";
import { redirect }     from "next/navigation";
import { useCartStore } from "@/shared/stores/cart-store";
import { CheckoutForm } from "../_components/checkout-form";

export default function CheckoutPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  const itemCount  = useCartStore((s) => s.itemCount);

  if (itemCount === 0) {
    redirect(`/${locale}/cart`);
  }

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="mb-8 text-2xl font-bold">Thanh toán</h1>
      <CheckoutForm locale={locale} />
    </main>
  );
}
```

- [ ] **Step 4: Create checkout loading**

```tsx
// src/app/[locale]/(shop)/checkout/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function CheckoutLoading() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <Skeleton className="mb-8 h-8 w-40" />
      <div className="grid gap-6 md:grid-cols-[1fr_360px]">
        <div className="space-y-4">
          {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}
        </div>
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    </main>
  );
}
```

- [ ] **Step 5: Create checkout success page**

```tsx
// src/app/[locale]/(shop)/checkout/success/page.tsx
import Link              from "next/link";
import { CheckCircle }   from "lucide-react";
import { Button }        from "@/shared/components/ui/button";

export default async function CheckoutSuccessPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ orderId?: string }>;
}) {
  const { locale }  = await params;
  const { orderId } = await searchParams;

  return (
    <div className="flex min-h-[70vh] flex-col items-center justify-center gap-6 text-center">
      <CheckCircle className="h-20 w-20 text-green-500" />
      <div>
        <h1 className="text-2xl font-bold">Đặt hàng thành công!</h1>
        {orderId && (
          <p className="mt-1 text-muted-foreground">Mã đơn hàng: #{orderId}</p>
        )}
      </div>
      <p className="max-w-md text-muted-foreground">
        Cảm ơn bạn đã đặt hàng. Chúng tôi sẽ liên hệ xác nhận trong thời gian sớm nhất.
      </p>
      <div className="flex gap-3">
        <Button asChild variant="outline">
          <Link href={`/${locale}/orders`}>Xem đơn hàng</Link>
        </Button>
        <Button asChild>
          <Link href={`/${locale}/products`}>Tiếp tục mua sắm</Link>
        </Button>
      </div>
    </div>
  );
}
```

```tsx
// src/app/[locale]/(shop)/checkout/success/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function CheckoutSuccessLoading() {
  return (
    <div className="flex min-h-[70vh] flex-col items-center justify-center gap-6">
      <Skeleton className="h-20 w-20 rounded-full" />
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-4 w-96" />
      <div className="flex gap-3">
        <Skeleton className="h-10 w-32" />
        <Skeleton className="h-10 w-40" />
      </div>
    </div>
  );
}
```

- [ ] **Step 6: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 7: Commit**

```bash
git add "src/app/[locale]/(shop)/cart/" "src/app/[locale]/(shop)/checkout/"
git commit -m "feat(shop): add cart, checkout, and checkout-success pages"
```

---

## Task 10: Orders and profile pages

**Files:**
- Create: `src/app/[locale]/(shop)/orders/page.tsx`
- Create: `src/app/[locale]/(shop)/orders/loading.tsx`
- Create: `src/app/[locale]/(shop)/orders/[id]/page.tsx`
- Create: `src/app/[locale]/(shop)/orders/[id]/loading.tsx`
- Create: `src/app/[locale]/(shop)/profile/page.tsx`
- Create: `src/app/[locale]/(shop)/profile/loading.tsx`

- [ ] **Step 1: Create orders list page**

```tsx
// src/app/[locale]/(shop)/orders/page.tsx
import Link              from "next/link";
import { http }          from "@/shared/lib/http/methods";
import { API }           from "@/shared/constants/api-endpoints";
import { OrderStatusBadge } from "../_components/order-status-badge";
import type { Order }    from "../_lib/types";

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

async function getOrders(locale: string): Promise<Order[]> {
  try {
    return await http.get<Order[]>(API.ORDERS.LIST);
  } catch {
    return [];
  }
}

export default async function OrdersPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const orders     = await getOrders(locale);

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Đơn hàng của tôi</h1>
      {orders.length === 0 ? (
        <p className="text-center text-muted-foreground">Bạn chưa có đơn hàng nào.</p>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Link
              key={order.id}
              href={`/${locale}/orders/${order.id}`}
              className="block rounded-xl border p-4 transition hover:shadow-sm"
            >
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-medium">Đơn #{order.code}</p>
                  <p className="text-sm text-muted-foreground">
                    {new Date(order.created_at).toLocaleDateString("vi-VN")}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-primary">{formatVND(order.total)}</p>
                  <OrderStatusBadge status={order.status} />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
```

- [ ] **Step 2: Create orders loading**

```tsx
// src/app/[locale]/(shop)/orders/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function OrdersLoading() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <Skeleton className="mb-6 h-8 w-48" />
      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-20 w-full rounded-xl" />
        ))}
      </div>
    </main>
  );
}
```

- [ ] **Step 3: Create order detail page**

```tsx
// src/app/[locale]/(shop)/orders/[id]/page.tsx
"use client";

import { use }                from "react";
import { useOrder, useCancelOrder } from "../../_lib/hooks";
import { OrderStatusBadge }   from "../../_components/order-status-badge";
import { Button }             from "@/shared/components/ui/button";
import { Separator }          from "@/shared/components/ui/separator";

function formatVND(n: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(n);
}

export default function OrderDetailPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { id } = use(params);
  const { data: order, isPending } = useOrder(id);
  const cancelOrder                = useCancelOrder(id);

  if (isPending) {
    return <div className="mx-auto max-w-3xl px-4 py-8 text-center">Đang tải...</div>;
  }
  if (!order) {
    return <div className="mx-auto max-w-3xl px-4 py-8 text-center">Không tìm thấy đơn hàng.</div>;
  }

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold">Đơn #{order.code}</h1>
          <p className="text-sm text-muted-foreground">
            {new Date(order.created_at).toLocaleString("vi-VN")}
          </p>
        </div>
        <OrderStatusBadge status={order.status} />
      </div>

      <div className="space-y-3 rounded-xl border p-4">
        {order.items.map((item) => (
          <div key={item.id} className="flex justify-between text-sm">
            <span>{item.product_name} x{item.quantity}</span>
            <span className="font-medium">{formatVND(item.subtotal)}</span>
          </div>
        ))}
        <Separator />
        <div className="flex justify-between font-semibold">
          <span>Tổng cộng</span>
          <span className="text-primary">{formatVND(order.total)}</span>
        </div>
      </div>

      <div className="mt-4 rounded-xl border p-4 text-sm">
        <p><span className="font-medium">Địa chỉ:</span> {order.address}</p>
        <p><span className="font-medium">Thanh toán:</span> {order.payment_method.toUpperCase()}</p>
        {order.note && <p><span className="font-medium">Ghi chú:</span> {order.note}</p>}
      </div>

      {order.status === "pending" && (
        <Button
          variant="destructive"
          className="mt-4"
          onClick={() => cancelOrder.mutate()}
          disabled={cancelOrder.isPending}
        >
          {cancelOrder.isPending ? "Đang huỷ..." : "Huỷ đơn hàng"}
        </Button>
      )}
    </main>
  );
}
```

- [ ] **Step 4: Create order detail loading**

```tsx
// src/app/[locale]/(shop)/orders/[id]/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function OrderDetailLoading() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <div className="space-y-2">
          <Skeleton className="h-6 w-40" />
          <Skeleton className="h-4 w-32" />
        </div>
        <Skeleton className="h-6 w-24 rounded-full" />
      </div>
      <Skeleton className="h-48 w-full rounded-xl" />
    </main>
  );
}
```

- [ ] **Step 5: Create profile page**

```tsx
// src/app/[locale]/(shop)/profile/page.tsx
"use client";

import { use, useEffect }    from "react";
import { useForm }           from "react-hook-form";
import { zodResolver }       from "@hookform/resolvers/zod";
import { z }                  from "zod";
import { Button }             from "@/shared/components/ui/button";
import { Input }              from "@/shared/components/ui/input";
import { Label }              from "@/shared/components/ui/label";
import { useProfile, useUpdateProfile } from "../_lib/hooks";

const profileSchema = z.object({
  firstName: z.string().min(1, "Vui lòng nhập tên"),
  lastName:  z.string().min(1, "Vui lòng nhập họ"),
  phone:     z.string().optional(),
});

type ProfileInput = z.infer<typeof profileSchema>;

export default function ProfilePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  use(params);
  const { data: profile }  = useProfile();
  const updateProfile      = useUpdateProfile();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<ProfileInput>({
    resolver: zodResolver(profileSchema),
  });

  useEffect(() => {
    if (profile) {
      reset({ firstName: profile.firstName, lastName: profile.lastName, phone: profile.phone ?? "" });
    }
  }, [profile, reset]);

  return (
    <main className="mx-auto max-w-lg px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Thông tin cá nhân</h1>
      <form onSubmit={handleSubmit((d) => updateProfile.mutate(d))} className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label htmlFor="lastName">Họ</Label>
            <Input id="lastName" {...register("lastName")} />
            {errors.lastName && <p className="mt-1 text-sm text-destructive">{errors.lastName.message}</p>}
          </div>
          <div>
            <Label htmlFor="firstName">Tên</Label>
            <Input id="firstName" {...register("firstName")} />
            {errors.firstName && <p className="mt-1 text-sm text-destructive">{errors.firstName.message}</p>}
          </div>
        </div>
        <div>
          <Label htmlFor="phone">Số điện thoại</Label>
          <Input id="phone" placeholder="0901234567" {...register("phone")} />
        </div>
        <Button type="submit" disabled={updateProfile.isPending}>
          {updateProfile.isPending ? "Đang lưu..." : "Lưu thay đổi"}
        </Button>
      </form>
    </main>
  );
}
```

```tsx
// src/app/[locale]/(shop)/profile/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function ProfileLoading() {
  return (
    <main className="mx-auto max-w-lg px-4 py-8">
      <Skeleton className="mb-6 h-8 w-48" />
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
        </div>
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-24" />
      </div>
    </main>
  );
}
```

- [ ] **Step 6: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 7: Commit**

```bash
git add "src/app/[locale]/(shop)/orders/" "src/app/[locale]/(shop)/profile/"
git commit -m "feat(shop): add orders list, order detail, and profile pages"
```

---

## Task 11: API payment routes

**Files:**
- Create: `src/app/api/payment/cod/confirm/route.ts`
- Create: `src/app/api/payment/vnpay/create/route.ts`
- Create: `src/app/api/payment/vnpay/callback/route.ts`
- Create: `src/app/api/payment/momo/create/route.ts`
- Create: `src/app/api/payment/momo/callback/route.ts`
- Create: `src/app/api/payment/zalopay/create/route.ts`
- Create: `src/app/api/payment/zalopay/callback/route.ts`

- [ ] **Step 1: Create COD confirm route**

```ts
// src/app/api/payment/cod/confirm/route.ts
import { cookies } from "next/headers";
import axios       from "axios";

const DJANGO_URL = process.env.DJANGO_API_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  const body        = await request.json();
  const cookieStore = await cookies();
  const token       = cookieStore.get("access_token")?.value;

  try {
    const { data } = await axios.post(
      `${DJANGO_URL}/api/payment/cod/confirm/`,
      body,
      { headers: token ? { Authorization: `Bearer ${token}` } : {} },
    );
    return Response.json(data);
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        { detail: err.response?.data?.detail ?? "Lỗi xác nhận COD" },
        { status: err.response?.status ?? 400 },
      );
    }
    return Response.json({ detail: "Lỗi hệ thống" }, { status: 500 });
  }
}
```

- [ ] **Step 2: Create VNPay routes**

```ts
// src/app/api/payment/vnpay/create/route.ts
import { cookies } from "next/headers";
import { createVNPayUrl } from "@/shared/lib/payment/vnpay";

export async function POST(request: Request) {
  const body        = await request.json();
  const cookieStore = await cookies();
  const token       = cookieStore.get("access_token")?.value;

  if (!token) return Response.json({ detail: "Unauthorized" }, { status: 401 });

  try {
    const paymentUrl = createVNPayUrl({
      orderId:  body.orderId,
      amount:   body.amount,
      orderInfo: body.orderInfo ?? "Thanh toan don hang",
      returnUrl: `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/vnpay/callback`,
    });
    return Response.json({ paymentUrl });
  } catch {
    return Response.json({ detail: "Lỗi tạo URL VNPay" }, { status: 500 });
  }
}
```

```ts
// src/app/api/payment/vnpay/callback/route.ts
import { type NextRequest } from "next/server";
import { verifyVNPayCallback } from "@/shared/lib/payment/vnpay";

export async function GET(request: NextRequest) {
  const params     = request.nextUrl.searchParams;
  const isValid    = verifyVNPayCallback(Object.fromEntries(params.entries()));
  const responseCode = params.get("vnp_ResponseCode");
  const orderId    = params.get("vnp_TxnRef");

  if (!isValid || responseCode !== "00") {
    return Response.redirect(
      new URL(`/vi/orders?payment=failed`, request.nextUrl.origin),
    );
  }

  return Response.redirect(
    new URL(`/vi/checkout/success?orderId=${orderId}`, request.nextUrl.origin),
  );
}
```

- [ ] **Step 3: Create Momo routes**

```ts
// src/app/api/payment/momo/create/route.ts
import { cookies } from "next/headers";
import { createMomoRequest } from "@/shared/lib/payment/momo";

export async function POST(request: Request) {
  const body        = await request.json();
  const cookieStore = await cookies();
  const token       = cookieStore.get("access_token")?.value;
  if (!token) return Response.json({ detail: "Unauthorized" }, { status: 401 });

  try {
    const result = await createMomoRequest({
      orderId:    body.orderId,
      amount:     body.amount,
      orderInfo:  body.orderInfo ?? "Thanh toan Momo",
      redirectUrl: `${process.env.NEXT_PUBLIC_APP_URL}/vi/checkout/success`,
      ipnUrl:      `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/momo/callback`,
    });
    return Response.json(result);
  } catch {
    return Response.json({ detail: "Lỗi tạo request Momo" }, { status: 500 });
  }
}
```

```ts
// src/app/api/payment/momo/callback/route.ts
import axios from "axios";

const DJANGO_URL = process.env.DJANGO_API_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  const body = await request.json();
  try {
    await axios.post(`${DJANGO_URL}/api/payment/momo/ipn/`, body);
    return Response.json({ message: "ok" });
  } catch {
    return Response.json({ detail: "IPN processing failed" }, { status: 500 });
  }
}
```

- [ ] **Step 4: Create ZaloPay routes**

```ts
// src/app/api/payment/zalopay/create/route.ts
import { cookies } from "next/headers";
import { createZaloPayOrder } from "@/shared/lib/payment/zalopay";

export async function POST(request: Request) {
  const body        = await request.json();
  const cookieStore = await cookies();
  const token       = cookieStore.get("access_token")?.value;
  if (!token) return Response.json({ detail: "Unauthorized" }, { status: 401 });

  try {
    const result = await createZaloPayOrder({
      appTransId: body.orderId,
      amount:     body.amount,
      description: body.description ?? "Thanh toan ZaloPay",
      callbackUrl: `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/zalopay/callback`,
    });
    return Response.json(result);
  } catch {
    return Response.json({ detail: "Lỗi tạo đơn ZaloPay" }, { status: 500 });
  }
}
```

```ts
// src/app/api/payment/zalopay/callback/route.ts
import axios from "axios";

const DJANGO_URL = process.env.DJANGO_API_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  const body = await request.json();
  try {
    await axios.post(`${DJANGO_URL}/api/payment/zalopay/callback/`, body);
    return Response.json({ return_code: 1, return_message: "success" });
  } catch {
    return Response.json({ return_code: 0, return_message: "failed" }, { status: 500 });
  }
}
```

- [ ] **Step 5: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 6: Commit**

```bash
git add src/app/api/payment/
git commit -m "feat(shop): add payment API route handlers (COD, VNPay, Momo, ZaloPay)"
```
