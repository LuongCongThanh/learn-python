# Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build root locale pages (homepage, error, loading, 404), sitemap, robots, and opengraph for the E-commerce Next.js app.

**Architecture:** Next.js 16 App Router with next-intl locale routing. All pages are Server Components by default. `params` and `searchParams` are Promises — must `await` them. `error.tsx` uses `unstable_retry` prop (not `reset`).

**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind v4, next-intl, Shadcn/UI, Lucide React, Framer Motion

---

## File Map

| File | Role |
|---|---|
| `src/app/[locale]/page.tsx` | Homepage — Hero + featured products |
| `src/app/[locale]/loading.tsx` | Locale root Suspense boundary |
| `src/app/[locale]/error.tsx` | Locale root error boundary (client) |
| `src/app/not-found.tsx` | Global 404 |
| `src/app/sitemap.ts` | Dynamic sitemap: `/` + `/products/[slug]` |
| `src/app/robots.ts` | robots.txt |

---

## Task 1: Root loading and error boundaries

**Files:**
- Create: `src/app/[locale]/loading.tsx`
- Create: `src/app/[locale]/error.tsx`

- [ ] **Step 1: Create `loading.tsx`**

```tsx
// src/app/[locale]/loading.tsx
import { Skeleton } from "@/shared/components/ui/skeleton";

export default function LocaleLoading() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-16">
      <Skeleton className="mb-4 h-12 w-1/2" />
      <Skeleton className="mb-8 h-6 w-1/3" />
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="aspect-square rounded-xl" />
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create `error.tsx`**

```tsx
// src/app/[locale]/error.tsx
"use client";

import { useEffect } from "react";
import * as Sentry from "@sentry/nextjs";
import { Button } from "@/shared/components/ui/button";

export default function LocaleError({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
      <h2 className="text-2xl font-semibold">Đã có lỗi xảy ra</h2>
      <p className="max-w-md text-muted-foreground">{error.message}</p>
      <Button onClick={unstable_retry}>Thử lại</Button>
    </div>
  );
}
```

- [ ] **Step 3: Verify types**

```bash
cd E-commerce-platforms/Front-end/ecommerce-next && npx tsc --noEmit 2>&1 | head -20
```

Expected: no errors for these files.

- [ ] **Step 4: Commit**

```bash
git add src/app/[locale]/loading.tsx src/app/[locale]/error.tsx
git commit -m "feat: add locale root loading and error boundaries"
```

---

## Task 2: Global 404 page

**Files:**
- Create: `src/app/not-found.tsx`

- [ ] **Step 1: Create `not-found.tsx`**

```tsx
// src/app/not-found.tsx
import Link from "next/link";
import { Button } from "@/shared/components/ui/button";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6 text-center">
      <p className="text-8xl font-bold text-primary">404</p>
      <h1 className="text-3xl font-semibold">Không tìm thấy trang</h1>
      <p className="max-w-md text-muted-foreground">
        Trang bạn đang tìm kiếm không tồn tại hoặc đã bị di chuyển.
      </p>
      <Button asChild>
        <Link href="/vi">Về trang chủ</Link>
      </Button>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add src/app/not-found.tsx
git commit -m "feat: add global 404 page"
```

---

## Task 3: sitemap.ts and robots.ts

**Files:**
- Create: `src/app/sitemap.ts`
- Create: `src/app/robots.ts`

- [ ] **Step 1: Create `sitemap.ts`**

```ts
// src/app/sitemap.ts
import { MetadataRoute } from "next";
import { http } from "@/shared/lib/http/methods";
import { API } from "@/shared/constants/api-endpoints";
import type { ProductList } from "@/shared/types/product";

const BASE_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://example.com";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticRoutes: MetadataRoute.Sitemap = [
    { url: `${BASE_URL}/vi`, lastModified: new Date(), changeFrequency: "daily", priority: 1 },
    { url: `${BASE_URL}/en`, lastModified: new Date(), changeFrequency: "daily", priority: 1 },
    { url: `${BASE_URL}/vi/products`, lastModified: new Date(), changeFrequency: "daily", priority: 0.9 },
    { url: `${BASE_URL}/en/products`, lastModified: new Date(), changeFrequency: "daily", priority: 0.9 },
  ];

  try {
    const data = await http.get<ProductList>(API.PRODUCTS.LIST, { pageSize: 200 });
    const productRoutes: MetadataRoute.Sitemap = data.results.flatMap((p) => [
      {
        url: `${BASE_URL}/vi/products/${p.slug}`,
        lastModified: new Date(p.updatedAt),
        changeFrequency: "weekly" as const,
        priority: 0.8,
      },
      {
        url: `${BASE_URL}/en/products/${p.slug}`,
        lastModified: new Date(p.updatedAt),
        changeFrequency: "weekly" as const,
        priority: 0.8,
      },
    ]);
    return [...staticRoutes, ...productRoutes];
  } catch {
    return staticRoutes;
  }
}
```

- [ ] **Step 2: Create `robots.ts`**

```ts
// src/app/robots.ts
import { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://example.com";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/vi/admin/", "/en/admin/"],
      },
    ],
    sitemap: `${BASE_URL}/sitemap.xml`,
  };
}
```

- [ ] **Step 3: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 4: Commit**

```bash
git add src/app/sitemap.ts src/app/robots.ts
git commit -m "feat: add sitemap and robots.txt"
```

---

## Task 4: Homepage

**Files:**
- Create: `src/app/[locale]/page.tsx`

- [ ] **Step 1: Create homepage**

```tsx
// src/app/[locale]/page.tsx
import Link from "next/link";
import { Button } from "@/shared/components/ui/button";
import { http } from "@/shared/lib/http/methods";
import { API } from "@/shared/constants/api-endpoints";
import type { ProductList } from "@/shared/types/product";

async function getFeaturedProducts() {
  try {
    return await http.get<ProductList>(API.PRODUCTS.LIST, {
      pageSize: 8,
      ordering: "-created_at",
    });
  } catch {
    return null;
  }
}

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const data = await getFeaturedProducts();

  return (
    <main>
      {/* Hero */}
      <section className="bg-gradient-to-r from-primary-500 to-primary-700 py-20 text-white">
        <div className="mx-auto max-w-7xl px-4 text-center">
          <h1 className="mb-4 text-5xl font-bold">
            {locale === "vi" ? "Mua sắm thông minh" : "Smart Shopping"}
          </h1>
          <p className="mb-8 text-xl opacity-90">
            {locale === "vi"
              ? "Hàng nghìn sản phẩm chất lượng, giao hàng nhanh chóng"
              : "Thousands of quality products, fast delivery"}
          </p>
          <Button asChild size="lg" variant="secondary">
            <Link href={`/${locale}/products`}>
              {locale === "vi" ? "Khám phá ngay" : "Explore now"}
            </Link>
          </Button>
        </div>
      </section>

      {/* Featured products */}
      {data && data.results.length > 0 && (
        <section className="mx-auto max-w-7xl px-4 py-16">
          <h2 className="mb-8 text-2xl font-semibold">
            {locale === "vi" ? "Sản phẩm nổi bật" : "Featured Products"}
          </h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {data.results.map((product) => (
              <Link
                key={product.id}
                href={`/${locale}/products/${product.slug}`}
                className="group rounded-xl border p-3 transition hover:shadow-md"
              >
                <div className="mb-3 aspect-square overflow-hidden rounded-lg bg-muted">
                  {product.images[0] && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={product.images[0]}
                      alt={product.name}
                      className="h-full w-full object-cover transition group-hover:scale-105"
                    />
                  )}
                </div>
                <p className="mb-1 line-clamp-2 text-sm font-medium">{product.name}</p>
                <p className="text-sm font-semibold text-primary-600">
                  {new Intl.NumberFormat("vi-VN", {
                    style: "currency",
                    currency: "VND",
                  }).format(product.salePrice ?? product.price)}
                </p>
              </Link>
            ))}
          </div>
          <div className="mt-8 text-center">
            <Button asChild variant="outline">
              <Link href={`/${locale}/products`}>
                {locale === "vi" ? "Xem tất cả sản phẩm" : "View all products"}
              </Link>
            </Button>
          </div>
        </section>
      )}
    </main>
  );
}
```

- [ ] **Step 2: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add src/app/[locale]/page.tsx
git commit -m "feat: add homepage with hero and featured products"
```
