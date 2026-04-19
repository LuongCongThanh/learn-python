# Design System — E-Commerce Next.js

> Tài liệu liên quan: [architecture.md](./architecture.md) · [frontend-guidelines.md](./frontend-guidelines.md)

---

## 1. Brand Colors

### 1.1 Bảng màu tổng quan

| Nhóm | Vai trò | Hue OKLCH |
| --- | --- | --- |
| **Primary** | Cam-đỏ năng động — CTA, button chính, badge | ~25° |
| **Secondary** | Đỏ đậm — hover, accent đậm, flash sale | ~15° |
| **Accent** | Vàng-cam — sale tag, highlight, rating sao | ~55° |
| **Neutral** | Xám ấm — text, border, background | ~30° |
| **Success** | Xanh lá — đơn thành công, in-stock | ~145° |
| **Warning** | Vàng — cảnh báo, sắp hết hàng | ~80° |
| **Error** | Đỏ tươi — lỗi form, out-of-stock | ~10° |
| **Info** | Xanh dương — thông tin, tooltip | ~250° |

### 1.2 Xem trước

| Token | Màu | Dùng cho |
| --- | --- | --- |
| `primary-500` | 🟠 Cam-đỏ | Button, link, badge chính |
| `primary-600` | 🔴 Cam-đỏ đậm | Hover state |
| `secondary-500` | 🔴 Đỏ đậm | Flash sale, accent mạnh |
| `accent-500` | 🟡 Vàng-cam | Sale tag, rating sao |
| `success-500` | 🟢 Xanh lá | Đơn thành công, in-stock |
| `warning-500` | 🟡 Vàng | Sắp hết hàng |
| `error-500` | 🔴 Đỏ tươi | Lỗi, out-of-stock |
| `neutral-900` | ⚫ Xám đen | Text chính |
| `neutral-500` | ⚫ Xám | Muted text |
| `neutral-200` | ⚪ Xám nhạt | Border, divider |

---

## 2. `src/app/globals.css` — Full Config

```css
@import "tailwindcss";

@theme {
  /* ── Primary: Cam-đỏ năng động (hue ~25°) ──────────────────────────── */
  --color-primary-50:  oklch(0.97 0.02 25);
  --color-primary-100: oklch(0.93 0.05 25);
  --color-primary-200: oklch(0.87 0.09 25);
  --color-primary-300: oklch(0.79 0.14 25);
  --color-primary-400: oklch(0.70 0.19 25);
  --color-primary-500: oklch(0.62 0.23 25);   /* ← Màu chính thương hiệu */
  --color-primary-600: oklch(0.54 0.22 25);   /* ← Hover button */
  --color-primary-700: oklch(0.45 0.19 25);
  --color-primary-800: oklch(0.35 0.15 25);
  --color-primary-900: oklch(0.26 0.10 25);
  --color-primary-950: oklch(0.16 0.06 25);

  /* ── Secondary: Đỏ đậm (hue ~15°) ─────────────────────────────────── */
  --color-secondary-50:  oklch(0.97 0.02 15);
  --color-secondary-100: oklch(0.93 0.04 15);
  --color-secondary-200: oklch(0.86 0.08 15);
  --color-secondary-300: oklch(0.77 0.13 15);
  --color-secondary-400: oklch(0.67 0.18 15);
  --color-secondary-500: oklch(0.57 0.22 15);   /* ← Đỏ đậm */
  --color-secondary-600: oklch(0.49 0.21 15);
  --color-secondary-700: oklch(0.41 0.18 15);
  --color-secondary-800: oklch(0.32 0.14 15);
  --color-secondary-900: oklch(0.24 0.09 15);
  --color-secondary-950: oklch(0.15 0.05 15);

  /* ── Accent: Vàng-cam (hue ~55°) ───────────────────────────────────── */
  --color-accent-50:  oklch(0.98 0.02 55);
  --color-accent-100: oklch(0.95 0.05 55);
  --color-accent-200: oklch(0.90 0.10 55);
  --color-accent-300: oklch(0.84 0.15 55);
  --color-accent-400: oklch(0.78 0.19 55);
  --color-accent-500: oklch(0.72 0.22 55);   /* ← Vàng-cam chính */
  --color-accent-600: oklch(0.63 0.20 55);
  --color-accent-700: oklch(0.53 0.17 55);
  --color-accent-800: oklch(0.42 0.13 55);
  --color-accent-900: oklch(0.31 0.09 55);
  --color-accent-950: oklch(0.20 0.05 55);

  /* ── Neutral: Xám ấm (hue ~30°) ────────────────────────────────────── */
  --color-neutral-50:  oklch(0.98 0.004 30);
  --color-neutral-100: oklch(0.96 0.006 30);
  --color-neutral-200: oklch(0.92 0.008 30);
  --color-neutral-300: oklch(0.85 0.010 30);
  --color-neutral-400: oklch(0.72 0.010 30);
  --color-neutral-500: oklch(0.58 0.010 30);
  --color-neutral-600: oklch(0.45 0.008 30);
  --color-neutral-700: oklch(0.35 0.007 30);
  --color-neutral-800: oklch(0.25 0.006 30);
  --color-neutral-900: oklch(0.16 0.004 30);
  --color-neutral-950: oklch(0.10 0.003 30);

  /* ── Semantic ───────────────────────────────────────────────────────── */
  --color-success-50:  oklch(0.97 0.03 145);
  --color-success-500: oklch(0.60 0.18 145);
  --color-success-700: oklch(0.42 0.14 145);

  --color-warning-50:  oklch(0.98 0.03 80);
  --color-warning-500: oklch(0.78 0.18 80);
  --color-warning-700: oklch(0.55 0.15 80);

  --color-error-50:  oklch(0.97 0.02 10);
  --color-error-500: oklch(0.58 0.24 10);
  --color-error-700: oklch(0.42 0.20 10);

  --color-info-50:  oklch(0.97 0.02 250);
  --color-info-500: oklch(0.58 0.18 250);
  --color-info-700: oklch(0.42 0.15 250);

  /* ── Typography ─────────────────────────────────────────────────────── */
  --font-sans: var(--font-inter), "Inter Variable", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.25rem;
  --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;
  --text-4xl:  2.25rem;
  --text-5xl:  3rem;

  --font-weight-normal:    400;
  --font-weight-medium:    500;
  --font-weight-semibold:  600;
  --font-weight-bold:      700;
  --font-weight-extrabold: 800;

  --leading-tight:   1.25;
  --leading-snug:    1.375;
  --leading-normal:  1.5;
  --leading-relaxed: 1.625;

  --tracking-tight:   -0.025em;
  --tracking-normal:   0em;
  --tracking-wide:     0.025em;
  --tracking-widest:   0.1em;

  /* ── Spacing ────────────────────────────────────────────────────────── */
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;

  /* ── Border radius ──────────────────────────────────────────────────── */
  --radius-card: 0.75rem;
  --radius-btn:  0.5rem;

  /* ── Container ──────────────────────────────────────────────────────── */
  --container-max-width: 1280px;
}

/* ── Shadcn/UI CSS Variables ────────────────────────────────────────── */
@layer base {
  :root {
    --background:           oklch(1 0 0);
    --foreground:           oklch(0.16 0.004 30);
    --primary:              oklch(0.62 0.23 25);
    --primary-foreground:   oklch(1 0 0);
    --secondary:            oklch(0.96 0.006 30);
    --secondary-foreground: oklch(0.26 0.10 25);
    --muted:                oklch(0.96 0.006 30);
    --muted-foreground:     oklch(0.58 0.010 30);
    --accent:               oklch(0.72 0.22 55);
    --accent-foreground:    oklch(0.16 0.004 30);
    --destructive:          oklch(0.58 0.24 10);
    --border:               oklch(0.92 0.008 30);
    --ring:                 oklch(0.62 0.23 25);
    --radius:               0.5rem;
  }

  .dark {
    --background:           oklch(0.13 0.004 30);
    --foreground:           oklch(0.96 0.006 30);
    --primary:              oklch(0.70 0.19 25);
    --primary-foreground:   oklch(0.16 0.004 30);
    --secondary:            oklch(0.22 0.006 30);
    --secondary-foreground: oklch(0.96 0.006 30);
    --muted:                oklch(0.22 0.006 30);
    --muted-foreground:     oklch(0.65 0.010 30);
    --accent:               oklch(0.78 0.19 55);
    --accent-foreground:    oklch(0.16 0.004 30);
    --destructive:          oklch(0.65 0.22 10);
    --border:               oklch(0.25 0.008 30);
    --ring:                 oklch(0.70 0.19 25);
  }

  * { @apply border-border; }
  body { @apply bg-background text-foreground; }
}
```

> **Tailwind v4:** Không có `tailwind.config.js`. Không dùng `@apply` cho component styles — chỉ dùng utility class trực tiếp.

---

## 3. Font Setup (`app/layout.tsx`)

```tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-inter',
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html lang="vi" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

---

## 4. Typography Patterns

```tsx
{/* Giá sản phẩm */}
<p className="text-2xl font-bold text-primary-500">1.299.000₫</p>
<p className="text-sm text-neutral-400 line-through">1.599.000₫</p>

{/* Tên sản phẩm */}
<h2 className="text-lg font-semibold text-neutral-900 leading-snug line-clamp-2">
  Áo thun nam basic oversize cotton 100%
</h2>

{/* Sale badge */}
<span className="text-xs font-bold tracking-wide uppercase bg-accent-500 text-white px-2 py-0.5 rounded">
  -30%
</span>

{/* Heading trang */}
<h1 className="text-3xl font-bold tracking-tight text-neutral-900">
  Sản phẩm nổi bật
</h1>

{/* Status */}
<span className="text-sm text-success-500">Còn hàng</span>
<span className="text-sm text-error-500">Hết hàng</span>
<span className="text-sm text-warning-500">Còn 3 sản phẩm</span>
```

---

## 5. Responsive Breakpoints

| Breakpoint | Min-width | Thiết bị | Dùng cho |
| --- | --- | --- | --- |
| _(default)_ | 0px | Mobile ≤ 639px | Layout 1 cột, stack |
| `sm` | 640px | Mobile ngang | 2 cột sản phẩm |
| `md` | 768px | Tablet | Sidebar filter xuất hiện |
| `lg` | 1024px | Laptop | 3-4 cột, admin layout |
| `xl` | 1280px | Desktop | Layout đầy đủ |
| `2xl` | 1536px | Wide screen | Max-width container |

**Mobile-first rules:**

| Thành phần | Mobile | `md` | `lg` |
| --- | --- | --- | --- |
| Product grid | 2 cột | 3 cột | 4 cột |
| Heading | `text-2xl` | `text-3xl` | `text-4xl` |
| Filter sidebar | Ẩn (drawer) | Hiện cố định | Hiện cố định |
| Cart | Full page | Full page | Drawer phải |
| Admin sidebar | Ẩn (hamburger) | Icon only | Full text |
| Touch target | ≥ 44×44px | — | — |

**Patterns:**

```tsx
{/* Product grid */}
<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-4 lg:gap-6">
  {products.map(p => <ProductCard key={p.id} product={p} />)}
</div>

{/* Container chuẩn */}
<div className="mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8">
  {children}
</div>
```

---

## 6. Shadcn/UI Setup

**Bước 1 — Init:**

```bash
npx shadcn@latest init
```

**Bước 2 — `components.json`** (alias phải trỏ vào `shared/`):

```json
{
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/shared/components",
    "utils": "@/shared/lib/utils",
    "ui": "@/shared/components/ui",
    "lib": "@/shared/lib",
    "hooks": "@/shared/hooks"
  }
}
```

**Bước 3 — Add components:**

```bash
npx shadcn@latest add button input label textarea select checkbox
npx shadcn@latest add dialog sheet dropdown-menu
npx shadcn@latest add table badge skeleton card avatar
npx shadcn@latest add form alert
```

**Quy tắc:**

| Quy tắc | Lý do |
| --- | --- |
| Không sửa file trong `ui/` | `shadcn add` có thể overwrite |
| Extend qua wrapper component | `shared/components/loading-button.tsx` wrap `ui/button.tsx` |
| Dùng Sonner thay Shadcn Toast | Sonner nhẹ hơn |
| Dùng Vaul cho cart drawer | Sheet không có swipe gesture mobile |

**Wrapper example:**

```tsx
// shared/components/loading-button.tsx
import { Button, ButtonProps } from '@/shared/components/ui/button'
import { Loader2 } from 'lucide-react'

interface LoadingButtonProps extends ButtonProps { isLoading?: boolean }

export function LoadingButton({ isLoading, children, ...props }: LoadingButtonProps) {
  return (
    <Button disabled={isLoading} {...props}>
      {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </Button>
  )
}
```

---

## 7. TanStack Table (Admin)

TanStack Table là headless — không có UI. Kết hợp với `ui/table.tsx` của Shadcn.

**`(admin)/_components/data-table.tsx` — reusable cho mọi trang admin:**

```tsx
'use client'
import { useReactTable, getCoreRowModel, getPaginationRowModel,
  getSortedRowModel, getFilteredRowModel, flexRender,
  ColumnDef, SortingState, ColumnFiltersState } from '@tanstack/react-table'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow }
  from '@/shared/components/ui/table'

export function DataTable<TData>({ columns, data }: { columns: ColumnDef<TData>[]; data: TData[] }) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

  const table = useReactTable({
    data, columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    state: { sorting, columnFilters },
  })

  return (
    <div>
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map(hg => (
            <TableRow key={hg.id}>
              {hg.headers.map(h => (
                <TableHead key={h.id}>{flexRender(h.column.columnDef.header, h.getContext())}</TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.map(row => (
            <TableRow key={row.id}>
              {row.getVisibleCells().map(cell => (
                <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="flex items-center justify-end gap-2 py-4">
        <button onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>Trước</button>
        <span>Trang {table.getState().pagination.pageIndex + 1} / {table.getPageCount()}</span>
        <button onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>Sau</button>
      </div>
    </div>
  )
}
```

**Columns definition (mỗi trang định nghĩa riêng):**

```tsx
// (admin)/products/_lib/columns.tsx
export const productColumns: ColumnDef<AdminProduct>[] = [
  { accessorKey: 'name', header: 'Tên sản phẩm' },
  { accessorKey: 'price', header: 'Giá',
    cell: ({ row }) => formatCurrency(row.getValue('price')) },
  { accessorKey: 'stock', header: 'Tồn kho' },
  { accessorKey: 'status', header: 'Trạng thái',
    cell: ({ row }) => <Badge>{row.getValue('status')}</Badge> },
  { id: 'actions', cell: ({ row }) => <ProductRowActions product={row.original} /> },
]
```

**Dùng trong page:**

```tsx
// (admin)/products/page.tsx — Server Component
export default async function AdminProductsPage() {
  const products = await fetchAdminProducts()
  return <DataTable columns={productColumns} data={products} />
}
```
