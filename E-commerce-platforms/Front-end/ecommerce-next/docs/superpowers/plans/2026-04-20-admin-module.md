# Admin Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the full admin panel — layout with sidebar, dashboard, product CRUD, order management, user list, and category management.

**Architecture:** Admin layout wraps all admin pages with sidebar + header. All admin pages are under `app/[locale]/(admin)/`. Client-side auth check via `useAuthStore` ensures only `is_staff` users can access. Data tables use `@tanstack/react-table`. `params` is a Promise in Next.js 16 — always `await`.

**Tech Stack:** Next.js 16, React 19, TypeScript, TanStack Query 5, TanStack Table 8, Zustand 5, React Hook Form 7, Zod 4, Lucide React, Tailwind v4, Shadcn/UI (table, dialog, form, badge, card)

---

## File Map

| File                                       | Role                                                                                   |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| `(admin)/layout.tsx`                       | Admin layout: sidebar + header + auth check                                            |
| `(admin)/_lib/types.ts`                    | AdminProduct, AdminOrder, DashboardStats types                                         |
| `(admin)/_lib/query-keys.ts`               | adminProductKeys, adminOrderKeys                                                       |
| `(admin)/_lib/actions.ts`                  | CRUD actions calling Django admin API                                                  |
| `(admin)/_lib/hooks.ts`                    | useAdminProducts, useAdminOrders, useDashboardStats, useAdminUsers, useAdminCategories |
| `(admin)/_components/admin-sidebar.tsx`    | Nav links with active state                                                            |
| `(admin)/_components/admin-header.tsx`     | Breadcrumb + user menu + logout                                                        |
| `(admin)/_components/admin-stats-card.tsx` | Metric card (label, value, icon, trend)                                                |
| `(admin)/_components/data-table.tsx`       | Generic TanStack Table wrapper                                                         |
| `(admin)/dashboard/page.tsx`               | Stats overview                                                                         |
| `(admin)/dashboard/loading.tsx`            | Stats skeleton                                                                         |
| `(admin)/products/page.tsx`                | Product table with filter                                                              |
| `(admin)/products/loading.tsx`             | Table skeleton                                                                         |
| `(admin)/products/_lib/columns.tsx`        | Product column definitions                                                             |
| `(admin)/products/new/page.tsx`            | Create product form                                                                    |
| `(admin)/products/[id]/page.tsx`           | Edit product form                                                                      |
| `(admin)/products/[id]/loading.tsx`        | Edit form skeleton                                                                     |
| `(admin)/orders/page.tsx`                  | Order table with filter                                                                |
| `(admin)/orders/loading.tsx`               | Table skeleton                                                                         |
| `(admin)/orders/_lib/columns.tsx`          | Order column definitions                                                               |
| `(admin)/orders/[id]/page.tsx`             | Order detail + status update                                                           |
| `(admin)/orders/[id]/loading.tsx`          | Order detail skeleton                                                                  |
| `(admin)/users/page.tsx`                   | User list                                                                              |
| `(admin)/users/[id]/page.tsx`              | User detail + order history                                                            |
| `(admin)/categories/page.tsx`              | Category CRUD                                                                          |
| `(admin)/categories/loading.tsx`           | Category skeleton                                                                      |

All paths below are relative to `src/app/[locale]/(admin)/` unless specified.

---

## Task 1: Types, query keys, and actions

**Files:**

- Create: `src/app/[locale]/(admin)/_lib/types.ts`
- Create: `src/app/[locale]/(admin)/_lib/query-keys.ts`
- Create: `src/app/[locale]/(admin)/_lib/actions.ts`

- [ ] **Step 1: Create `types.ts`**

```ts
// src/app/[locale]/(admin)/_lib/types.ts
import { z } from 'zod'
import type { OrderStatus, PaymentMethod, PaymentStatus } from '@/shared/types/order'

export interface AdminProduct {
  id: number
  name: string
  slug: string
  price: number
  salePrice: number | null
  stock: number
  isActive: boolean
  category: { id: number; name: string }
  images: string[]
  createdAt: string
}

export interface AdminOrder {
  id: number
  code: string
  status: OrderStatus
  payment_method: PaymentMethod
  payment_status: PaymentStatus
  total: number
  created_at: string
  customer_name: string
  customer_email: string
}

export interface DashboardStats {
  totalRevenue: number
  totalOrders: number
  totalProducts: number
  totalUsers: number
  revenueChange: number // % change from last period
  ordersChange: number
}

export interface AdminUser {
  id: number
  email: string
  firstName: string
  lastName: string
  isActive: boolean
  is_staff: boolean
  createdAt: string
}

export interface AdminCategory {
  id: number
  name: string
  slug: string
  productCount: number
}

export const adminProductSchema = z.object({
  name: z.string().min(1, 'Tên sản phẩm là bắt buộc'),
  price: z.coerce.number().min(0, 'Giá phải >= 0'),
  salePrice: z.coerce.number().nullable().optional(),
  stock: z.coerce.number().int().min(0),
  categoryId: z.coerce.number().min(1, 'Chọn danh mục'),
  isActive: z.boolean().default(true),
  description: z.string().min(1, 'Mô tả là bắt buộc'),
})

export type AdminProductInput = z.infer<typeof adminProductSchema>
```

- [ ] **Step 2: Create `query-keys.ts`**

```ts
// src/app/[locale]/(admin)/_lib/query-keys.ts
export const adminProductKeys = {
  all: ['admin', 'products'] as const,
  list: (page: number, search?: string) => [...adminProductKeys.all, 'list', page, search] as const,
  detail: (id: string) => [...adminProductKeys.all, 'detail', id] as const,
}

export const adminOrderKeys = {
  all: ['admin', 'orders'] as const,
  list: (page: number, status?: string) => [...adminOrderKeys.all, 'list', page, status] as const,
  detail: (id: string) => [...adminOrderKeys.all, 'detail', id] as const,
}

export const adminUserKeys = {
  all: ['admin', 'users'] as const,
  list: () => [...adminUserKeys.all, 'list'] as const,
  detail: (id: string) => [...adminUserKeys.all, 'detail', id] as const,
}

export const adminCategoryKeys = {
  all: ['admin', 'categories'] as const,
  list: () => [...adminCategoryKeys.all, 'list'] as const,
}

export const dashboardStatsKey = ['admin', 'dashboard'] as const
```

- [ ] **Step 3: Create `actions.ts`**

```ts
// src/app/[locale]/(admin)/_lib/actions.ts
import { http } from '@/shared/lib/http/methods'
import { API } from '@/shared/constants/api-endpoints'
import type {
  AdminProduct,
  AdminOrder,
  DashboardStats,
  AdminUser,
  AdminCategory,
  AdminProductInput,
} from './types'

export const adminProductActions = {
  list: (page: number, search?: string) =>
    http.get<{ results: AdminProduct[]; count: number }>(API.ADMIN.PRODUCTS, { page, search }),
  detail: (id: string) => http.get<AdminProduct>(API.ADMIN.PRODUCT_DETAIL(id)),
  create: (data: AdminProductInput) => http.post<AdminProduct>(API.ADMIN.PRODUCTS, data),
  update: (id: string, data: Partial<AdminProductInput>) =>
    http.patch<AdminProduct>(API.ADMIN.PRODUCT_DETAIL(id), data),
  delete: (id: string) => http.delete<void>(API.ADMIN.PRODUCT_DETAIL(id)),
}

export const adminOrderActions = {
  list: (page: number, status?: string) =>
    http.get<{ results: AdminOrder[]; count: number }>(API.ADMIN.ORDERS, { page, status }),
  detail: (id: string) => http.get<AdminOrder>(API.ADMIN.ORDER_DETAIL(id)),
  updateStatus: (id: string, status: string) =>
    http.patch<AdminOrder>(API.ADMIN.ORDER_STATUS(id), { status }),
}

export const adminUserActions = {
  list: () => http.get<AdminUser[]>(API.ADMIN.USERS),
  detail: (id: string) => http.get<AdminUser>(API.ADMIN.USER_DETAIL(id)),
  toggle: (id: string, isActive: boolean) =>
    http.patch<AdminUser>(API.ADMIN.USER_DETAIL(id), { isActive }),
}

export const adminCategoryActions = {
  list: () => http.get<AdminCategory[]>('/api/admin/categories/'),
  create: (name: string) => http.post<AdminCategory>('/api/admin/categories/', { name }),
  update: (id: number, name: string) =>
    http.patch<AdminCategory>(`/api/admin/categories/${id}/`, { name }),
  delete: (id: number) => http.delete<void>(`/api/admin/categories/${id}/`),
}

export const adminDashboardActions = {
  stats: () => http.get<DashboardStats>(API.ADMIN.DASHBOARD_STATS),
}
```

- [ ] **Step 4: Commit**

```bash
git add "src/app/[locale]/(admin)/_lib/"
git commit -m "feat(admin): add admin types, query keys, and actions"
```

---

## Task 2: Admin hooks

**Files:**

- Create: `src/app/[locale]/(admin)/_lib/hooks.ts`

- [ ] **Step 1: Create `hooks.ts`**

```ts
// src/app/[locale]/(admin)/_lib/hooks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import {
  adminProductActions,
  adminOrderActions,
  adminUserActions,
  adminCategoryActions,
  adminDashboardActions,
} from './actions'
import {
  adminProductKeys,
  adminOrderKeys,
  adminUserKeys,
  adminCategoryKeys,
  dashboardStatsKey,
} from './query-keys'
import type { AdminProductInput } from './types'

export function useDashboardStats() {
  return useQuery({
    queryKey: dashboardStatsKey,
    queryFn: adminDashboardActions.stats,
    staleTime: 5 * 60_000,
  })
}

export function useAdminProducts(page: number, search?: string) {
  return useQuery({
    queryKey: adminProductKeys.list(page, search),
    queryFn: () => adminProductActions.list(page, search),
  })
}

export function useAdminProduct(id: string) {
  return useQuery({
    queryKey: adminProductKeys.detail(id),
    queryFn: () => adminProductActions.detail(id),
  })
}

export function useCreateProduct() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: adminProductActions.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminProductKeys.all })
      toast.success('Tạo sản phẩm thành công')
    },
  })
}

export function useUpdateProduct(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: Partial<AdminProductInput>) => adminProductActions.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminProductKeys.all })
      toast.success('Cập nhật sản phẩm thành công')
    },
  })
}

export function useDeleteProduct() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: adminProductActions.delete,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminProductKeys.all })
      toast.success('Đã xoá sản phẩm')
    },
  })
}

export function useAdminOrders(page: number, status?: string) {
  return useQuery({
    queryKey: adminOrderKeys.list(page, status),
    queryFn: () => adminOrderActions.list(page, status),
  })
}

export function useAdminOrder(id: string) {
  return useQuery({
    queryKey: adminOrderKeys.detail(id),
    queryFn: () => adminOrderActions.detail(id),
  })
}

export function useUpdateOrderStatus(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (status: string) => adminOrderActions.updateStatus(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminOrderKeys.all })
      toast.success('Cập nhật trạng thái đơn hàng thành công')
    },
  })
}

export function useAdminUsers() {
  return useQuery({ queryKey: adminUserKeys.list(), queryFn: adminUserActions.list })
}

export function useAdminUser(id: string) {
  return useQuery({
    queryKey: adminUserKeys.detail(id),
    queryFn: () => adminUserActions.detail(id),
  })
}

export function useToggleUserActive(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (isActive: boolean) => adminUserActions.toggle(id, isActive),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminUserKeys.all })
      toast.success('Cập nhật trạng thái người dùng')
    },
  })
}

export function useAdminCategories() {
  return useQuery({ queryKey: adminCategoryKeys.list(), queryFn: adminCategoryActions.list })
}

export function useCreateCategory() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: adminCategoryActions.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminCategoryKeys.all })
      toast.success('Tạo danh mục thành công')
    },
  })
}

export function useDeleteCategory() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: adminCategoryActions.delete,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: adminCategoryKeys.all })
      toast.success('Đã xoá danh mục')
    },
  })
}
```

- [ ] **Step 2: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 3: Commit**

```bash
git add "src/app/[locale]/(admin)/_lib/hooks.ts"
git commit -m "feat(admin): add admin hooks"
```

---

## Task 3: Admin layout and sidebar

**Files:**

- Create: `src/app/[locale]/(admin)/layout.tsx`
- Create: `src/app/[locale]/(admin)/_components/admin-sidebar.tsx`
- Create: `src/app/[locale]/(admin)/_components/admin-header.tsx`

- [ ] **Step 1: Create `layout.tsx`**

```tsx
// src/app/[locale]/(admin)/layout.tsx
import { AdminSidebar } from './_components/admin-sidebar'
import { AdminHeader } from './_components/admin-header'

export default async function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}) {
  const { locale } = await params

  return (
    <div className="bg-muted/30 flex min-h-screen">
      <AdminSidebar locale={locale} />
      <div className="flex flex-1 flex-col">
        <AdminHeader locale={locale} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Create `admin-sidebar.tsx`**

```tsx
// src/app/[locale]/(admin)/_components/admin-sidebar.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LayoutDashboard, Package, ShoppingBag, Users, Tag, Store } from 'lucide-react'
import { cn } from '@/shared/lib/utils'

const NAV_ITEMS = [
  { href: '/dashboard', label: 'Tổng quan', icon: LayoutDashboard },
  { href: '/products', label: 'Sản phẩm', icon: Package },
  { href: '/orders', label: 'Đơn hàng', icon: ShoppingBag },
  { href: '/users', label: 'Người dùng', icon: Users },
  { href: '/categories', label: 'Danh mục', icon: Tag },
]

export function AdminSidebar({ locale }: { locale: string }) {
  const pathname = usePathname()

  return (
    <aside className="bg-background flex w-60 flex-col border-r">
      <div className="flex h-14 items-center gap-2 border-b px-4 font-semibold">
        <Store className="text-primary h-5 w-5" />
        <span>Admin Panel</span>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const fullHref = `/${locale}/admin${href}`
          const isActive = pathname.startsWith(fullHref)
          return (
            <Link
              key={href}
              href={fullHref}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground'
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
```

- [ ] **Step 3: Create `admin-header.tsx`**

```tsx
// src/app/[locale]/(admin)/_components/admin-header.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LogOut, User } from 'lucide-react'
import { Button } from '@/shared/components/ui/button'
import { useAuthStore } from '@/shared/stores/auth-store'
import { useLogout } from '@/app/[locale]/(auth)/_lib/hooks'

function getBreadcrumb(pathname: string): string {
  if (pathname.includes('/dashboard')) return 'Tổng quan'
  if (pathname.includes('/products/new')) return 'Thêm sản phẩm'
  if (pathname.includes('/products')) return 'Sản phẩm'
  if (pathname.includes('/orders')) return 'Đơn hàng'
  if (pathname.includes('/users')) return 'Người dùng'
  if (pathname.includes('/categories')) return 'Danh mục'
  return 'Admin'
}

export function AdminHeader({ locale }: { locale: string }) {
  const pathname = usePathname()
  const user = useAuthStore((s) => s.user)
  const logout = useLogout(locale)

  return (
    <header className="bg-background flex h-14 items-center justify-between border-b px-6">
      <h1 className="text-muted-foreground text-sm font-medium">{getBreadcrumb(pathname)}</h1>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-sm">
          <User className="text-muted-foreground h-4 w-4" />
          <span>{user?.name ?? 'Admin'}</span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => logout.mutate()}
          disabled={logout.isPending}
        >
          <LogOut className="mr-1 h-4 w-4" />
          Đăng xuất
        </Button>
      </div>
    </header>
  )
}
```

- [ ] **Step 4: Commit**

```bash
git add "src/app/[locale]/(admin)/layout.tsx" "src/app/[locale]/(admin)/_components/admin-sidebar.tsx" "src/app/[locale]/(admin)/_components/admin-header.tsx"
git commit -m "feat(admin): add admin layout, sidebar, and header"
```

---

## Task 4: Stats card and data table

**Files:**

- Create: `src/app/[locale]/(admin)/_components/admin-stats-card.tsx`
- Create: `src/app/[locale]/(admin)/_components/data-table.tsx`

- [ ] **Step 1: Create `admin-stats-card.tsx`**

```tsx
// src/app/[locale]/(admin)/_components/admin-stats-card.tsx
import { type LucideIcon } from 'lucide-react'
import { cn } from '@/shared/lib/utils'
import { Card } from '@/shared/components/ui/card'

export function AdminStatsCard({
  label,
  value,
  icon: Icon,
  change,
  formatValue,
}: {
  label: string
  value: number
  icon: LucideIcon
  change?: number
  formatValue?: (v: number) => string
}) {
  const displayValue = formatValue ? formatValue(value) : value.toLocaleString('vi-VN')
  const isPositive = (change ?? 0) >= 0

  return (
    <Card className="flex items-start gap-4 p-5">
      <div className="bg-primary/10 rounded-lg p-2.5">
        <Icon className="text-primary h-5 w-5" />
      </div>
      <div className="flex-1">
        <p className="text-muted-foreground text-sm">{label}</p>
        <p className="mt-0.5 text-2xl font-bold">{displayValue}</p>
        {change !== undefined && (
          <p className={cn('mt-0.5 text-xs', isPositive ? 'text-green-600' : 'text-red-500')}>
            {isPositive ? '+' : ''}
            {change}% so với tháng trước
          </p>
        )}
      </div>
    </Card>
  )
}
```

- [ ] **Step 2: Create `data-table.tsx`**

```tsx
// src/app/[locale]/(admin)/_components/data-table.tsx
'use client'

import { type ColumnDef, flexRender, getCoreRowModel, useReactTable } from '@tanstack/react-table'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/shared/components/ui/table'
import { Button } from '@/shared/components/ui/button'

interface DataTableProps<TData> {
  columns: ColumnDef<TData>[]
  data: TData[]
  pageIndex: number
  pageCount: number
  onPrev: () => void
  onNext: () => void
  isLoading?: boolean
}

export function DataTable<TData>({
  columns,
  data,
  pageIndex,
  pageCount,
  onPrev,
  onNext,
  isLoading,
}: DataTableProps<TData>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    pageCount,
  })

  return (
    <div className="space-y-3">
      <div className="rounded-xl border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((hg) => (
              <TableRow key={hg.id}>
                {hg.headers.map((h) => (
                  <TableHead key={h.id}>
                    {h.isPlaceholder ? null : flexRender(h.column.columnDef.header, h.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="text-muted-foreground py-10 text-center"
                >
                  Đang tải...
                </TableCell>
              </TableRow>
            ) : table.getRowModel().rows.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="text-muted-foreground py-10 text-center"
                >
                  Không có dữ liệu
                </TableCell>
              </TableRow>
            ) : (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <div className="text-muted-foreground flex items-center justify-between text-sm">
        <span>
          Trang {pageIndex + 1} / {pageCount}
        </span>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={onPrev} disabled={pageIndex === 0}>
            Trước
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={onNext}
            disabled={pageIndex >= pageCount - 1}
          >
            Sau
          </Button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add "src/app/[locale]/(admin)/_components/admin-stats-card.tsx" "src/app/[locale]/(admin)/_components/data-table.tsx"
git commit -m "feat(admin): add stats-card and data-table components"
```

---

## Task 5: Dashboard page

**Files:**

- Create: `src/app/[locale]/(admin)/dashboard/page.tsx`
- Create: `src/app/[locale]/(admin)/dashboard/loading.tsx`

- [ ] **Step 1: Create dashboard page**

```tsx
// src/app/[locale]/(admin)/dashboard/page.tsx
'use client'

import { TrendingUp, ShoppingBag, Package, Users } from 'lucide-react'
import { AdminStatsCard } from '../_components/admin-stats-card'
import { useDashboardStats } from '../_lib/hooks'

function formatVND(n: number) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n)
}

export default function DashboardPage() {
  const { data: stats, isPending } = useDashboardStats()

  if (isPending) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-muted h-28 animate-pulse rounded-xl" />
        ))}
      </div>
    )
  }

  if (!stats) return null

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">Tổng quan</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <AdminStatsCard
          label="Doanh thu"
          value={stats.totalRevenue}
          icon={TrendingUp}
          change={stats.revenueChange}
          formatValue={formatVND}
        />
        <AdminStatsCard
          label="Đơn hàng"
          value={stats.totalOrders}
          icon={ShoppingBag}
          change={stats.ordersChange}
        />
        <AdminStatsCard label="Sản phẩm" value={stats.totalProducts} icon={Package} />
        <AdminStatsCard label="Người dùng" value={stats.totalUsers} icon={Users} />
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Create dashboard loading**

```tsx
// src/app/[locale]/(admin)/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="bg-muted h-7 w-32 animate-pulse rounded" />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-muted h-28 animate-pulse rounded-xl" />
        ))}
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add "src/app/[locale]/(admin)/dashboard/"
git commit -m "feat(admin): add dashboard page"
```

---

## Task 6: Product management

**Files:**

- Create: `src/app/[locale]/(admin)/products/_lib/columns.tsx`
- Create: `src/app/[locale]/(admin)/products/page.tsx`
- Create: `src/app/[locale]/(admin)/products/loading.tsx`
- Create: `src/app/[locale]/(admin)/products/new/page.tsx`
- Create: `src/app/[locale]/(admin)/products/[id]/page.tsx`
- Create: `src/app/[locale]/(admin)/products/[id]/loading.tsx`

- [ ] **Step 1: Create product columns**

```tsx
// src/app/[locale]/(admin)/products/_lib/columns.tsx
'use client'

import type { ColumnDef } from '@tanstack/react-table'
import Link from 'next/link'
import { Badge } from '@/shared/components/ui/badge'
import { Button } from '@/shared/components/ui/button'
import { Pencil, Trash2 } from 'lucide-react'
import type { AdminProduct } from '../../_lib/types'

function formatVND(n: number) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n)
}

export function buildProductColumns(
  locale: string,
  onDelete: (id: string) => void
): ColumnDef<AdminProduct>[] {
  return [
    {
      accessorKey: 'name',
      header: 'Tên sản phẩm',
      cell: ({ row }) => (
        <span className="max-w-[200px] truncate font-medium">{row.original.name}</span>
      ),
    },
    {
      accessorKey: 'category',
      header: 'Danh mục',
      cell: ({ row }) => row.original.category.name,
    },
    {
      accessorKey: 'price',
      header: 'Giá',
      cell: ({ row }) => formatVND(row.original.salePrice ?? row.original.price),
    },
    {
      accessorKey: 'stock',
      header: 'Kho',
      cell: ({ row }) => (
        <span className={row.original.stock === 0 ? 'text-destructive' : ''}>
          {row.original.stock}
        </span>
      ),
    },
    {
      accessorKey: 'isActive',
      header: 'Trạng thái',
      cell: ({ row }) => (
        <Badge variant={row.original.isActive ? 'default' : 'secondary'}>
          {row.original.isActive ? 'Hiển thị' : 'Ẩn'}
        </Badge>
      ),
    },
    {
      id: 'actions',
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" asChild>
            <Link href={`/${locale}/admin/products/${row.original.id}`}>
              <Pencil className="h-4 w-4" />
            </Link>
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-destructive hover:text-destructive"
            onClick={() => onDelete(String(row.original.id))}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ),
    },
  ]
}
```

- [ ] **Step 2: Create products page**

```tsx
// src/app/[locale]/(admin)/products/page.tsx
'use client'

import { use, useState } from 'react'
import Link from 'next/link'
import { Plus } from 'lucide-react'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { DataTable } from '../_components/data-table'
import { useAdminProducts, useDeleteProduct } from '../_lib/hooks'
import { buildProductColumns } from './_lib/columns'

export default function AdminProductsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = use(params)
  const [page, setPage] = useState(0)
  const [search, setSearch] = useState('')

  const { data, isPending } = useAdminProducts(page + 1, search || undefined)
  const deleteProduct = useDeleteProduct()
  const pageCount = data ? Math.ceil(data.count / 20) : 1

  const columns = buildProductColumns(locale, (id) => {
    if (confirm('Xác nhận xoá sản phẩm này?')) deleteProduct.mutate(id)
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">Sản phẩm</h1>
        <Button asChild>
          <Link href={`/${locale}/admin/products/new`}>
            <Plus className="mr-2 h-4 w-4" /> Thêm sản phẩm
          </Link>
        </Button>
      </div>

      <Input
        placeholder="Tìm kiếm sản phẩm..."
        value={search}
        onChange={(e) => {
          setSearch(e.target.value)
          setPage(0)
        }}
        className="max-w-sm"
      />

      <DataTable
        columns={columns}
        data={data?.results ?? []}
        pageIndex={page}
        pageCount={pageCount}
        onPrev={() => setPage((p) => p - 1)}
        onNext={() => setPage((p) => p + 1)}
        isLoading={isPending}
      />
    </div>
  )
}
```

- [ ] **Step 3: Create products loading**

```tsx
// src/app/[locale]/(admin)/products/loading.tsx
import { Skeleton } from '@/shared/components/ui/skeleton'

export default function AdminProductsLoading() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Skeleton className="h-7 w-32" />
        <Skeleton className="h-9 w-36" />
      </div>
      <Skeleton className="h-10 w-72" />
      <Skeleton className="h-64 w-full rounded-xl" />
    </div>
  )
}
```

- [ ] **Step 4: Create new product page**

```tsx
// src/app/[locale]/(admin)/products/new/page.tsx
'use client'

import { use } from 'react'
import { useRouter } from 'next/navigation'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { Label } from '@/shared/components/ui/label'
import { Textarea } from '@/shared/components/ui/textarea'
import { Checkbox } from '@/shared/components/ui/checkbox'
import { useCreateProduct } from '../../_lib/hooks'
import { adminProductSchema } from '../../_lib/types'
import type { AdminProductInput } from '../../_lib/types'

export default function NewProductPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = use(params)
  const router = useRouter()
  const create = useCreateProduct()

  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<AdminProductInput>({
    resolver: zodResolver(adminProductSchema),
    defaultValues: { isActive: true },
  })

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-xl font-bold">Thêm sản phẩm mới</h1>

      <form
        onSubmit={handleSubmit((d) =>
          create.mutate(d, { onSuccess: () => router.push(`/${locale}/admin/products`) })
        )}
        className="space-y-4"
      >
        <div>
          <Label htmlFor="name">Tên sản phẩm</Label>
          <Input id="name" {...register('name')} />
          {errors.name && <p className="text-destructive mt-1 text-sm">{errors.name.message}</p>}
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label htmlFor="price">Giá gốc (VNĐ)</Label>
            <Input id="price" type="number" {...register('price')} />
            {errors.price && (
              <p className="text-destructive mt-1 text-sm">{errors.price.message}</p>
            )}
          </div>
          <div>
            <Label htmlFor="salePrice">Giá khuyến mãi (tuỳ chọn)</Label>
            <Input id="salePrice" type="number" {...register('salePrice')} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label htmlFor="stock">Tồn kho</Label>
            <Input id="stock" type="number" {...register('stock')} />
            {errors.stock && (
              <p className="text-destructive mt-1 text-sm">{errors.stock.message}</p>
            )}
          </div>
          <div>
            <Label htmlFor="categoryId">ID Danh mục</Label>
            <Input id="categoryId" type="number" {...register('categoryId')} />
            {errors.categoryId && (
              <p className="text-destructive mt-1 text-sm">{errors.categoryId.message}</p>
            )}
          </div>
        </div>

        <div>
          <Label htmlFor="description">Mô tả</Label>
          <Textarea id="description" rows={4} {...register('description')} />
          {errors.description && (
            <p className="text-destructive mt-1 text-sm">{errors.description.message}</p>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Controller
            control={control}
            name="isActive"
            render={({ field }) => (
              <Checkbox id="isActive" checked={field.value} onCheckedChange={field.onChange} />
            )}
          />
          <Label htmlFor="isActive">Hiển thị sản phẩm</Label>
        </div>

        <div className="flex gap-3">
          <Button type="submit" disabled={create.isPending}>
            {create.isPending ? 'Đang tạo...' : 'Tạo sản phẩm'}
          </Button>
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Huỷ
          </Button>
        </div>
      </form>
    </div>
  )
}
```

- [ ] **Step 5: Create edit product page**

```tsx
// src/app/[locale]/(admin)/products/[id]/page.tsx
'use client'

import { use, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { Label } from '@/shared/components/ui/label'
import { Textarea } from '@/shared/components/ui/textarea'
import { Checkbox } from '@/shared/components/ui/checkbox'
import { useAdminProduct, useUpdateProduct } from '../../_lib/hooks'
import { adminProductSchema } from '../../_lib/types'
import type { AdminProductInput } from '../../_lib/types'

export default function EditProductPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>
}) {
  const { locale, id } = use(params)
  const router = useRouter()
  const { data: product } = useAdminProduct(id)
  const update = useUpdateProduct(id)

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AdminProductInput>({
    resolver: zodResolver(adminProductSchema),
  })

  useEffect(() => {
    if (product) {
      reset({
        name: product.name,
        price: product.price,
        salePrice: product.salePrice,
        stock: product.stock,
        categoryId: product.category.id,
        isActive: product.isActive,
        description: '',
      })
    }
  }, [product, reset])

  if (!product) return <div className="text-muted-foreground py-10 text-center">Đang tải...</div>

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-xl font-bold">Chỉnh sửa: {product.name}</h1>

      <form
        onSubmit={handleSubmit((d) =>
          update.mutate(d, { onSuccess: () => router.push(`/${locale}/admin/products`) })
        )}
        className="space-y-4"
      >
        <div>
          <Label htmlFor="name">Tên sản phẩm</Label>
          <Input id="name" {...register('name')} />
          {errors.name && <p className="text-destructive mt-1 text-sm">{errors.name.message}</p>}
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label htmlFor="price">Giá gốc (VNĐ)</Label>
            <Input id="price" type="number" {...register('price')} />
          </div>
          <div>
            <Label htmlFor="salePrice">Giá khuyến mãi</Label>
            <Input id="salePrice" type="number" {...register('salePrice')} />
          </div>
        </div>

        <div>
          <Label htmlFor="stock">Tồn kho</Label>
          <Input id="stock" type="number" {...register('stock')} />
        </div>

        <div>
          <Label htmlFor="description">Mô tả</Label>
          <Textarea id="description" rows={4} {...register('description')} />
        </div>

        <div className="flex items-center gap-2">
          <Controller
            control={control}
            name="isActive"
            render={({ field }) => (
              <Checkbox id="isActive" checked={field.value} onCheckedChange={field.onChange} />
            )}
          />
          <Label htmlFor="isActive">Hiển thị sản phẩm</Label>
        </div>

        <div className="flex gap-3">
          <Button type="submit" disabled={update.isPending}>
            {update.isPending ? 'Đang lưu...' : 'Lưu thay đổi'}
          </Button>
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Huỷ
          </Button>
        </div>
      </form>
    </div>
  )
}
```

```tsx
// src/app/[locale]/(admin)/products/[id]/loading.tsx
import { Skeleton } from '@/shared/components/ui/skeleton'

export default function EditProductLoading() {
  return (
    <div className="mx-auto max-w-2xl space-y-4">
      <Skeleton className="h-7 w-64" />
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-10 w-full" />
      ))}
    </div>
  )
}
```

- [ ] **Step 6: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 7: Commit**

```bash
git add "src/app/[locale]/(admin)/products/"
git commit -m "feat(admin): add product management pages (list, create, edit)"
```

---

## Task 7: Order management

**Files:**

- Create: `src/app/[locale]/(admin)/orders/_lib/columns.tsx`
- Create: `src/app/[locale]/(admin)/orders/page.tsx`
- Create: `src/app/[locale]/(admin)/orders/loading.tsx`
- Create: `src/app/[locale]/(admin)/orders/[id]/page.tsx`
- Create: `src/app/[locale]/(admin)/orders/[id]/loading.tsx`

- [ ] **Step 1: Create order columns**

```tsx
// src/app/[locale]/(admin)/orders/_lib/columns.tsx
'use client'

import type { ColumnDef } from '@tanstack/react-table'
import Link from 'next/link'
import { Button } from '@/shared/components/ui/button'
import { Eye } from 'lucide-react'
import { OrderStatusBadge } from '@/app/[locale]/(shop)/_components/order-status-badge'
import type { AdminOrder } from '../../_lib/types'

function formatVND(n: number) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n)
}

export function buildOrderColumns(locale: string): ColumnDef<AdminOrder>[] {
  return [
    {
      accessorKey: 'code',
      header: 'Mã đơn',
      cell: ({ row }) => <span className="font-mono text-sm">#{row.original.code}</span>,
    },
    {
      accessorKey: 'customer_name',
      header: 'Khách hàng',
    },
    {
      accessorKey: 'total',
      header: 'Tổng tiền',
      cell: ({ row }) => <span className="font-semibold">{formatVND(row.original.total)}</span>,
    },
    {
      accessorKey: 'status',
      header: 'Trạng thái',
      cell: ({ row }) => <OrderStatusBadge status={row.original.status} />,
    },
    {
      accessorKey: 'created_at',
      header: 'Ngày đặt',
      cell: ({ row }) => new Date(row.original.created_at).toLocaleDateString('vi-VN'),
    },
    {
      id: 'actions',
      cell: ({ row }) => (
        <Button variant="ghost" size="icon" asChild>
          <Link href={`/${locale}/admin/orders/${row.original.id}`}>
            <Eye className="h-4 w-4" />
          </Link>
        </Button>
      ),
    },
  ]
}
```

- [ ] **Step 2: Create orders page**

```tsx
// src/app/[locale]/(admin)/orders/page.tsx
'use client'

import { use, useState } from 'react'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/shared/components/ui/select'
import { DataTable } from '../_components/data-table'
import { useAdminOrders } from '../_lib/hooks'
import { buildOrderColumns } from './_lib/columns'

export default function AdminOrdersPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = use(params)
  const [page, setPage] = useState(0)
  const [status, setStatus] = useState<string | undefined>(undefined)

  const { data, isPending } = useAdminOrders(page + 1, status)
  const pageCount = data ? Math.ceil(data.count / 20) : 1
  const columns = buildOrderColumns(locale)

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Đơn hàng</h1>

      <Select
        value={status ?? 'all'}
        onValueChange={(v) => {
          setStatus(v === 'all' ? undefined : v)
          setPage(0)
        }}
      >
        <SelectTrigger className="w-44">
          <SelectValue placeholder="Lọc trạng thái" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Tất cả</SelectItem>
          <SelectItem value="pending">Chờ xác nhận</SelectItem>
          <SelectItem value="confirmed">Đã xác nhận</SelectItem>
          <SelectItem value="processing">Đang xử lý</SelectItem>
          <SelectItem value="shipped">Đang giao</SelectItem>
          <SelectItem value="delivered">Đã giao</SelectItem>
          <SelectItem value="cancelled">Đã huỷ</SelectItem>
        </SelectContent>
      </Select>

      <DataTable
        columns={columns}
        data={data?.results ?? []}
        pageIndex={page}
        pageCount={pageCount}
        onPrev={() => setPage((p) => p - 1)}
        onNext={() => setPage((p) => p + 1)}
        isLoading={isPending}
      />
    </div>
  )
}
```

- [ ] **Step 3: Create orders loading**

```tsx
// src/app/[locale]/(admin)/orders/loading.tsx
import { Skeleton } from '@/shared/components/ui/skeleton'

export default function AdminOrdersLoading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-7 w-32" />
      <Skeleton className="h-10 w-44" />
      <Skeleton className="h-64 w-full rounded-xl" />
    </div>
  )
}
```

- [ ] **Step 4: Create order detail page**

```tsx
// src/app/[locale]/(admin)/orders/[id]/page.tsx
'use client'

import { use } from 'react'
import { OrderStatusBadge } from '@/app/[locale]/(shop)/_components/order-status-badge'
import { Button } from '@/shared/components/ui/button'
import { Separator } from '@/shared/components/ui/separator'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/shared/components/ui/select'
import { useAdminOrder, useUpdateOrderStatus } from '../../_lib/hooks'

function formatVND(n: number) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n)
}

const STATUS_OPTIONS = [
  { value: 'pending', label: 'Chờ xác nhận' },
  { value: 'confirmed', label: 'Đã xác nhận' },
  { value: 'processing', label: 'Đang xử lý' },
  { value: 'shipped', label: 'Đang giao' },
  { value: 'delivered', label: 'Đã giao' },
  { value: 'cancelled', label: 'Đã huỷ' },
]

export default function AdminOrderDetailPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>
}) {
  const { id } = use(params)
  const { data: order } = useAdminOrder(id)
  const updateStatus = useUpdateOrderStatus(id)

  if (!order) return <div className="text-muted-foreground py-10 text-center">Đang tải...</div>

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold">Đơn #{order.code}</h1>
          <p className="text-muted-foreground text-sm">
            {new Date(order.created_at).toLocaleString('vi-VN')}
          </p>
        </div>
        <OrderStatusBadge status={order.status} />
      </div>

      <div className="rounded-xl border p-4">
        <h2 className="mb-3 font-semibold">Thông tin khách hàng</h2>
        <p className="text-sm">{order.customer_name}</p>
        <p className="text-muted-foreground text-sm">{order.customer_email}</p>
      </div>

      <div className="rounded-xl border p-4">
        <h2 className="mb-3 font-semibold">Cập nhật trạng thái</h2>
        <div className="flex items-center gap-3">
          <Select defaultValue={order.status} onValueChange={(v) => updateStatus.mutate(v)}>
            <SelectTrigger className="w-48">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {STATUS_OPTIONS.map((o) => (
                <SelectItem key={o.value} value={o.value}>
                  {o.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {updateStatus.isPending && (
            <span className="text-muted-foreground text-sm">Đang cập nhật...</span>
          )}
        </div>
      </div>

      <div className="rounded-xl border p-4">
        <h2 className="mb-3 font-semibold">Sản phẩm</h2>
        <div className="space-y-2 text-sm">
          {order.total !== undefined && (
            <>
              <Separator />
              <div className="flex justify-between font-semibold">
                <span>Tổng cộng</span>
                <span>{formatVND(order.total)}</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
```

```tsx
// src/app/[locale]/(admin)/orders/[id]/loading.tsx
import { Skeleton } from '@/shared/components/ui/skeleton'

export default function AdminOrderDetailLoading() {
  return (
    <div className="mx-auto max-w-3xl space-y-4">
      <Skeleton className="h-7 w-48" />
      <Skeleton className="h-24 w-full rounded-xl" />
      <Skeleton className="h-20 w-full rounded-xl" />
      <Skeleton className="h-32 w-full rounded-xl" />
    </div>
  )
}
```

- [ ] **Step 5: Commit**

```bash
git add "src/app/[locale]/(admin)/orders/"
git commit -m "feat(admin): add order management pages"
```

---

## Task 8: Users and categories pages

**Files:**

- Create: `src/app/[locale]/(admin)/users/page.tsx`
- Create: `src/app/[locale]/(admin)/users/[id]/page.tsx`
- Create: `src/app/[locale]/(admin)/categories/page.tsx`
- Create: `src/app/[locale]/(admin)/categories/loading.tsx`

- [ ] **Step 1: Create users page**

```tsx
// src/app/[locale]/(admin)/users/page.tsx
'use client'

import { Badge } from '@/shared/components/ui/badge'
import { Button } from '@/shared/components/ui/button'
import { useAdminUsers, useToggleUserActive } from '../_lib/hooks'

export default function AdminUsersPage() {
  const { data: users, isPending } = useAdminUsers()

  if (isPending) return <div className="text-muted-foreground py-10 text-center">Đang tải...</div>

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Người dùng ({users?.length ?? 0})</h1>
      <div className="divide-y rounded-xl border">
        {users?.map((user) => (
          <div key={user.id} className="flex items-center justify-between px-4 py-3">
            <div>
              <p className="font-medium">
                {user.firstName} {user.lastName}
              </p>
              <p className="text-muted-foreground text-sm">{user.email}</p>
            </div>
            <div className="flex items-center gap-3">
              {user.is_staff && <Badge>Admin</Badge>}
              <Badge variant={user.isActive ? 'default' : 'secondary'}>
                {user.isActive ? 'Hoạt động' : 'Bị khoá'}
              </Badge>
              <ToggleButton userId={String(user.id)} isActive={user.isActive} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function ToggleButton({ userId, isActive }: { userId: string; isActive: boolean }) {
  const toggle = useToggleUserActive(userId)
  return (
    <Button
      variant="outline"
      size="sm"
      onClick={() => toggle.mutate(!isActive)}
      disabled={toggle.isPending}
    >
      {isActive ? 'Khoá' : 'Mở khoá'}
    </Button>
  )
}
```

- [ ] **Step 2: Create user detail page**

```tsx
// src/app/[locale]/(admin)/users/[id]/page.tsx
'use client'

import { use } from 'react'
import { Badge } from '@/shared/components/ui/badge'
import { useAdminUser } from '../../_lib/hooks'

export default function AdminUserDetailPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>
}) {
  const { id } = use(params)
  const { data: user } = useAdminUser(id)

  if (!user) return <div className="text-muted-foreground py-10 text-center">Đang tải...</div>

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-bold">
          {user.firstName} {user.lastName}
        </h1>
        {user.is_staff && <Badge>Admin</Badge>}
        <Badge variant={user.isActive ? 'default' : 'secondary'}>
          {user.isActive ? 'Hoạt động' : 'Bị khoá'}
        </Badge>
      </div>

      <div className="space-y-2 rounded-xl border p-4 text-sm">
        <div className="flex justify-between">
          <span className="text-muted-foreground">Email</span>
          <span>{user.email}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">Ngày tham gia</span>
          <span>{new Date(user.createdAt).toLocaleDateString('vi-VN')}</span>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Create categories page**

```tsx
// src/app/[locale]/(admin)/categories/page.tsx
'use client'

import { useState } from 'react'
import { Trash2, Plus } from 'lucide-react'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { useAdminCategories, useCreateCategory, useDeleteCategory } from '../_lib/hooks'

export default function AdminCategoriesPage() {
  const [name, setName] = useState('')
  const { data: categories } = useAdminCategories()
  const createCategory = useCreateCategory()
  const deleteCategory = useDeleteCategory()

  function handleCreate() {
    if (!name.trim()) return
    createCategory.mutate(name.trim(), { onSuccess: () => setName('') })
  }

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <h1 className="text-xl font-bold">Danh mục sản phẩm</h1>

      <div className="flex gap-2">
        <Input
          placeholder="Tên danh mục mới..."
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
        />
        <Button onClick={handleCreate} disabled={createCategory.isPending || !name.trim()}>
          <Plus className="mr-1 h-4 w-4" /> Thêm
        </Button>
      </div>

      <div className="divide-y rounded-xl border">
        {categories?.map((cat) => (
          <div key={cat.id} className="flex items-center justify-between px-4 py-3">
            <div>
              <p className="font-medium">{cat.name}</p>
              <p className="text-muted-foreground text-sm">{cat.productCount} sản phẩm</p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="text-destructive hover:text-destructive"
              onClick={() => {
                if (confirm(`Xoá danh mục "${cat.name}"?`)) deleteCategory.mutate(cat.id)
              }}
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
}
```

```tsx
// src/app/[locale]/(admin)/categories/loading.tsx
import { Skeleton } from '@/shared/components/ui/skeleton'

export default function AdminCategoriesLoading() {
  return (
    <div className="mx-auto max-w-xl space-y-4">
      <Skeleton className="h-7 w-40" />
      <div className="flex gap-2">
        <Skeleton className="h-10 flex-1" />
        <Skeleton className="h-10 w-20" />
      </div>
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-14 w-full rounded-xl" />
        ))}
      </div>
    </div>
  )
}
```

- [ ] **Step 4: Verify types — full check**

```bash
npx tsc --noEmit 2>&1 | head -30
```

Expected: no errors. If there are import path errors, fix them before committing.

- [ ] **Step 5: Commit**

```bash
git add "src/app/[locale]/(admin)/users/" "src/app/[locale]/(admin)/categories/"
git commit -m "feat(admin): add users and categories management pages"
```

---

## Final verification

- [ ] **Run full type check**

```bash
npx tsc --noEmit 2>&1 | head -30
```

- [ ] **Run lint**

```bash
npx next lint 2>&1 | head -30
```

- [ ] **Run tests**

```bash
npx vitest run 2>&1 | tail -20
```

- [ ] **Final commit**

```bash
git add -A
git commit -m "feat(admin): complete admin module — dashboard, products, orders, users, categories"
```
