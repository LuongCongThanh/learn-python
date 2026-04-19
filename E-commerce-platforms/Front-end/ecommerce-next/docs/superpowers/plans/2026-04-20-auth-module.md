# Auth Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build complete auth flow — login, register, forgot-password pages with forms, React Query hooks, and Next.js Route Handler proxies to Django.

**Architecture:** Forms use React Hook Form + Zod. Mutations use TanStack Query `useMutation`. API routes proxy to Django and set/clear `access_token` HttpOnly cookie. Types re-export from `shared/types/user.ts` — do not redefine.

**Tech Stack:** Next.js 16, React 19, TypeScript, React Hook Form 7, Zod 4, TanStack Query 5, Axios, Sonner (toast), next/headers (async cookies)

---

## File Map

| File | Role |
|---|---|
| `src/app/[locale]/(auth)/_lib/types.ts` | Re-export shared auth types |
| `src/app/[locale]/(auth)/_lib/schemas.ts` | Zod form schemas (re-export from shared) |
| `src/app/[locale]/(auth)/_lib/actions.ts` | Axios calls to Next.js API routes |
| `src/app/[locale]/(auth)/_lib/hooks.ts` | useMutation hooks |
| `src/app/[locale]/(auth)/_components/login-form.tsx` | RHF login form |
| `src/app/[locale]/(auth)/_components/register-form.tsx` | RHF register form |
| `src/app/[locale]/(auth)/login/page.tsx` | Login page |
| `src/app/[locale]/(auth)/register/page.tsx` | Register page |
| `src/app/[locale]/(auth)/forgot-password/page.tsx` | Forgot password page |
| `src/app/api/auth/login/route.ts` | POST → Django login, sets cookie |
| `src/app/api/auth/register/route.ts` | POST → Django register |
| `src/app/api/auth/logout/route.ts` | POST → clears cookie |
| `src/app/api/auth/refresh/route.ts` | POST → Django refresh, rotates cookie |

---

## Task 1: Types and schemas

**Files:**
- Create: `src/app/[locale]/(auth)/_lib/types.ts`
- Create: `src/app/[locale]/(auth)/_lib/schemas.ts`

- [ ] **Step 1: Create `types.ts`**

Re-export from shared — do not duplicate type definitions.

```ts
// src/app/[locale]/(auth)/_lib/types.ts
export type { LoginInput, RegisterInput, AuthToken, User } from "@/shared/types/user";
```

- [ ] **Step 2: Create `schemas.ts`**

Re-export from shared. Add a ForgotPasswordSchema here since it's auth-module-specific.

```ts
// src/app/[locale]/(auth)/_lib/schemas.ts
import { z } from "zod";

export { LoginSchema, RegisterSchema } from "@/shared/types/user";

export const ForgotPasswordSchema = z.object({
  email: z.string().email("Email không hợp lệ"),
});

export type ForgotPasswordInput = z.infer<typeof ForgotPasswordSchema>;
```

- [ ] **Step 3: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 4: Commit**

```bash
git add "src/app/[locale]/(auth)/_lib/types.ts" "src/app/[locale]/(auth)/_lib/schemas.ts"
git commit -m "feat(auth): add auth types and schemas"
```

---

## Task 2: API Route Handlers

**Files:**
- Create: `src/app/api/auth/login/route.ts`
- Create: `src/app/api/auth/register/route.ts`
- Create: `src/app/api/auth/logout/route.ts`
- Create: `src/app/api/auth/refresh/route.ts`

- [ ] **Step 1: Create login route**

```ts
// src/app/api/auth/login/route.ts
import { cookies } from "next/headers";
import axios from "axios";

const DJANGO_URL = process.env.DJANGO_API_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  const body = await request.json();

  try {
    const { data } = await axios.post(`${DJANGO_URL}/api/auth/login/`, body);
    const cookieStore = await cookies();

    cookieStore.set("access_token", data.access, {
      httpOnly: true,
      secure:   process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge:   60 * 60 * 24,     // 24h
      path:     "/",
    });

    cookieStore.set("refresh_token", data.refresh, {
      httpOnly: true,
      secure:   process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge:   60 * 60 * 24 * 7, // 7 days
      path:     "/",
    });

    return Response.json({ user: data.user });
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        { detail: err.response?.data?.detail ?? "Email hoặc mật khẩu không đúng" },
        { status: err.response?.status ?? 400 },
      );
    }
    return Response.json({ detail: "Lỗi hệ thống" }, { status: 500 });
  }
}
```

- [ ] **Step 2: Create register route**

```ts
// src/app/api/auth/register/route.ts
import axios from "axios";

const DJANGO_URL = process.env.DJANGO_API_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  const body = await request.json();

  try {
    const { data } = await axios.post(`${DJANGO_URL}/api/auth/register/`, body);
    return Response.json(data, { status: 201 });
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        { detail: err.response?.data?.detail ?? "Đăng ký thất bại" },
        { status: err.response?.status ?? 400 },
      );
    }
    return Response.json({ detail: "Lỗi hệ thống" }, { status: 500 });
  }
}
```

- [ ] **Step 3: Create logout route**

```ts
// src/app/api/auth/logout/route.ts
import { cookies } from "next/headers";

export async function POST() {
  const cookieStore = await cookies();
  cookieStore.delete("access_token");
  cookieStore.delete("refresh_token");
  return Response.json({ ok: true });
}
```

- [ ] **Step 4: Create refresh route**

```ts
// src/app/api/auth/refresh/route.ts
import { cookies } from "next/headers";
import axios from "axios";

const DJANGO_URL = process.env.DJANGO_API_URL ?? "http://localhost:8000";

export async function POST() {
  const cookieStore = await cookies();
  const refresh = cookieStore.get("refresh_token")?.value;

  if (!refresh) {
    return Response.json({ detail: "No refresh token" }, { status: 401 });
  }

  try {
    const { data } = await axios.post(`${DJANGO_URL}/api/auth/token/refresh/`, {
      refresh,
    });

    cookieStore.set("access_token", data.access, {
      httpOnly: true,
      secure:   process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge:   60 * 60 * 24,
      path:     "/",
    });

    return Response.json({ access: data.access });
  } catch {
    cookieStore.delete("access_token");
    cookieStore.delete("refresh_token");
    return Response.json({ detail: "Token hết hạn" }, { status: 401 });
  }
}
```

- [ ] **Step 5: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

- [ ] **Step 6: Commit**

```bash
git add src/app/api/auth/
git commit -m "feat(auth): add auth API route handlers (login, register, logout, refresh)"
```

---

## Task 3: Actions and hooks

**Files:**
- Create: `src/app/[locale]/(auth)/_lib/actions.ts`
- Create: `src/app/[locale]/(auth)/_lib/hooks.ts`

- [ ] **Step 1: Create `actions.ts`**

```ts
// src/app/[locale]/(auth)/_lib/actions.ts
import { http } from "@/shared/lib/http/methods";
import type { LoginInput, RegisterInput, User } from "./types";

export async function loginAction(data: LoginInput): Promise<{ user: User }> {
  return http.post("/api/auth/login/", data);
}

export async function registerAction(data: RegisterInput): Promise<void> {
  return http.post("/api/auth/register/", {
    email:     data.email,
    password:  data.password,
    firstName: data.firstName,
    lastName:  data.lastName,
  });
}

export async function logoutAction(): Promise<void> {
  return http.post("/api/auth/logout/");
}

export async function forgotPasswordAction(email: string): Promise<void> {
  return http.post("/api/auth/forgot-password/", { email });
}
```

- [ ] **Step 2: Create `hooks.ts`**

```ts
// src/app/[locale]/(auth)/_lib/hooks.ts
import { useMutation }  from "@tanstack/react-query";
import { useRouter }    from "next/navigation";
import { toast }        from "sonner";
import { useAuthStore } from "@/shared/stores/auth-store";
import { loginAction, registerAction, logoutAction, forgotPasswordAction } from "./actions";
import type { LoginInput, RegisterInput } from "./types";

export function useLogin(locale: string) {
  const router    = useRouter();
  const setUser   = useAuthStore((s) => s.setUser);

  return useMutation({
    mutationFn: (data: LoginInput) => loginAction(data),
    onSuccess: (res) => {
      setUser(res.user);
      toast.success("Đăng nhập thành công");
      router.push(`/${locale}`);
      router.refresh();
    },
  });
}

export function useRegister(locale: string) {
  const router = useRouter();

  return useMutation({
    mutationFn: (data: RegisterInput) => registerAction(data),
    onSuccess: () => {
      toast.success("Đăng ký thành công! Vui lòng đăng nhập.");
      router.push(`/${locale}/login`);
    },
  });
}

export function useLogout(locale: string) {
  const router    = useRouter();
  const clearAuth = useAuthStore((s) => s.clearAuth);

  return useMutation({
    mutationFn: logoutAction,
    onSuccess: () => {
      clearAuth();
      router.push(`/${locale}/login`);
      router.refresh();
    },
  });
}

export function useForgotPassword() {
  return useMutation({
    mutationFn: (email: string) => forgotPasswordAction(email),
    onSuccess: () => {
      toast.success("Email đặt lại mật khẩu đã được gửi");
    },
  });
}
```

- [ ] **Step 3: Write hook test**

```ts
// src/app/[locale]/(auth)/_lib/hooks.test.ts
import { renderHook, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { server } from "@/__tests__/helpers/mock-handlers";
import { http as mswHttp, HttpResponse } from "msw";
import { renderWithProviders } from "@/__tests__/helpers/render";
import { useLogin } from "./hooks";

// Note: renderWithProviders wraps with QueryClient; useRouter is mocked below
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }),
}));

describe("useLogin", () => {
  it("calls /api/auth/login/ and sets user on success", async () => {
    server.use(
      mswHttp.post("/api/auth/login/", () =>
        HttpResponse.json({ user: { id: 1, email: "a@b.com", name: "Test", is_staff: false } }),
      ),
    );

    const { result } = renderHook(() => useLogin("vi"), {
      wrapper: ({ children }) => renderWithProviders(children as React.ReactElement).container
        .firstChild as React.FC,
    });

    result.current.mutate({ email: "a@b.com", password: "password123" });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
  });
});
```

- [ ] **Step 4: Run test**

```bash
npx vitest run "src/app/\\[locale\\]/\\(auth\\)/_lib/hooks.test.ts" 2>&1 | tail -15
```

- [ ] **Step 5: Commit**

```bash
git add "src/app/[locale]/(auth)/_lib/"
git commit -m "feat(auth): add auth actions, hooks, and hook tests"
```

---

## Task 4: Login form component

**Files:**
- Create: `src/app/[locale]/(auth)/_components/login-form.tsx`

- [ ] **Step 1: Create `login-form.tsx`**

```tsx
// src/app/[locale]/(auth)/_components/login-form.tsx
"use client";

import { useForm }          from "react-hook-form";
import { zodResolver }      from "@hookform/resolvers/zod";
import Link                  from "next/link";
import { Button }            from "@/shared/components/ui/button";
import { Input }             from "@/shared/components/ui/input";
import { Label }             from "@/shared/components/ui/label";
import { LoginSchema }       from "../_lib/schemas";
import { useLogin }          from "../_lib/hooks";
import type { LoginInput }   from "../_lib/types";

export function LoginForm({ locale }: { locale: string }) {
  const login = useLogin(locale);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({ resolver: zodResolver(LoginSchema) });

  return (
    <form onSubmit={handleSubmit((d) => login.mutate(d))} className="space-y-4">
      <div className="space-y-1">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          {...register("email")}
        />
        {errors.email && (
          <p className="text-sm text-destructive">{errors.email.message}</p>
        )}
      </div>

      <div className="space-y-1">
        <Label htmlFor="password">Mật khẩu</Label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          {...register("password")}
        />
        {errors.password && (
          <p className="text-sm text-destructive">{errors.password.message}</p>
        )}
      </div>

      <div className="flex items-center justify-between">
        <Link
          href={`/${locale}/forgot-password`}
          className="text-sm text-primary hover:underline"
        >
          Quên mật khẩu?
        </Link>
      </div>

      <Button type="submit" className="w-full" disabled={login.isPending}>
        {login.isPending ? "Đang đăng nhập..." : "Đăng nhập"}
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Chưa có tài khoản?{" "}
        <Link href={`/${locale}/register`} className="text-primary hover:underline">
          Đăng ký ngay
        </Link>
      </p>
    </form>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add "src/app/[locale]/(auth)/_components/login-form.tsx"
git commit -m "feat(auth): add login form component"
```

---

## Task 5: Register form component

**Files:**
- Create: `src/app/[locale]/(auth)/_components/register-form.tsx`

- [ ] **Step 1: Create `register-form.tsx`**

```tsx
// src/app/[locale]/(auth)/_components/register-form.tsx
"use client";

import { useForm }             from "react-hook-form";
import { zodResolver }         from "@hookform/resolvers/zod";
import Link                     from "next/link";
import { Button }               from "@/shared/components/ui/button";
import { Input }                from "@/shared/components/ui/input";
import { Label }                from "@/shared/components/ui/label";
import { RegisterSchema }       from "../_lib/schemas";
import { useRegister }          from "../_lib/hooks";
import type { RegisterInput }   from "../_lib/types";

export function RegisterForm({ locale }: { locale: string }) {
  const register_ = useRegister(locale);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterInput>({ resolver: zodResolver(RegisterSchema) });

  return (
    <form onSubmit={handleSubmit((d) => register_.mutate(d))} className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <Label htmlFor="lastName">Họ</Label>
          <Input id="lastName" placeholder="Nguyễn" {...register("lastName")} />
          {errors.lastName && (
            <p className="text-sm text-destructive">{errors.lastName.message}</p>
          )}
        </div>
        <div className="space-y-1">
          <Label htmlFor="firstName">Tên</Label>
          <Input id="firstName" placeholder="Văn A" {...register("firstName")} />
          {errors.firstName && (
            <p className="text-sm text-destructive">{errors.firstName.message}</p>
          )}
        </div>
      </div>

      <div className="space-y-1">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" placeholder="you@example.com" {...register("email")} />
        {errors.email && (
          <p className="text-sm text-destructive">{errors.email.message}</p>
        )}
      </div>

      <div className="space-y-1">
        <Label htmlFor="password">Mật khẩu</Label>
        <Input id="password" type="password" placeholder="Tối thiểu 8 ký tự" {...register("password")} />
        {errors.password && (
          <p className="text-sm text-destructive">{errors.password.message}</p>
        )}
      </div>

      <div className="space-y-1">
        <Label htmlFor="confirmPassword">Xác nhận mật khẩu</Label>
        <Input id="confirmPassword" type="password" placeholder="••••••••" {...register("confirmPassword")} />
        {errors.confirmPassword && (
          <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={register_.isPending}>
        {register_.isPending ? "Đang đăng ký..." : "Đăng ký"}
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Đã có tài khoản?{" "}
        <Link href={`/${locale}/login`} className="text-primary hover:underline">
          Đăng nhập
        </Link>
      </p>
    </form>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add "src/app/[locale]/(auth)/_components/register-form.tsx"
git commit -m "feat(auth): add register form component"
```

---

## Task 6: Auth pages

**Files:**
- Create: `src/app/[locale]/(auth)/login/page.tsx`
- Create: `src/app/[locale]/(auth)/register/page.tsx`
- Create: `src/app/[locale]/(auth)/forgot-password/page.tsx`

- [ ] **Step 1: Create login page**

```tsx
// src/app/[locale]/(auth)/login/page.tsx
import { LoginForm } from "../_components/login-form";

export default async function LoginPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <div className="w-full max-w-md rounded-2xl bg-background p-8 shadow-lg">
        <h1 className="mb-2 text-2xl font-bold">Đăng nhập</h1>
        <p className="mb-6 text-sm text-muted-foreground">
          Chào mừng trở lại! Vui lòng đăng nhập để tiếp tục.
        </p>
        <LoginForm locale={locale} />
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create register page**

```tsx
// src/app/[locale]/(auth)/register/page.tsx
import { RegisterForm } from "../_components/register-form";

export default async function RegisterPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <div className="w-full max-w-md rounded-2xl bg-background p-8 shadow-lg">
        <h1 className="mb-2 text-2xl font-bold">Tạo tài khoản</h1>
        <p className="mb-6 text-sm text-muted-foreground">
          Điền thông tin bên dưới để đăng ký tài khoản mới.
        </p>
        <RegisterForm locale={locale} />
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Create forgot-password page**

```tsx
// src/app/[locale]/(auth)/forgot-password/page.tsx
"use client";

import { use }             from "react";
import { useForm }         from "react-hook-form";
import { zodResolver }     from "@hookform/resolvers/zod";
import Link                from "next/link";
import { Button }          from "@/shared/components/ui/button";
import { Input }           from "@/shared/components/ui/input";
import { Label }           from "@/shared/components/ui/label";
import { ForgotPasswordSchema } from "../_lib/schemas";
import { useForgotPassword }    from "../_lib/hooks";
import type { ForgotPasswordInput } from "../_lib/schemas";

export default function ForgotPasswordPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  const forgot = useForgotPassword();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordInput>({ resolver: zodResolver(ForgotPasswordSchema) });

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <div className="w-full max-w-md rounded-2xl bg-background p-8 shadow-lg">
        <h1 className="mb-2 text-2xl font-bold">Quên mật khẩu</h1>
        <p className="mb-6 text-sm text-muted-foreground">
          Nhập email của bạn, chúng tôi sẽ gửi link đặt lại mật khẩu.
        </p>

        <form onSubmit={handleSubmit((d) => forgot.mutate(d.email))} className="space-y-4">
          <div className="space-y-1">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="you@example.com" {...register("email")} />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={forgot.isPending}>
            {forgot.isPending ? "Đang gửi..." : "Gửi email"}
          </Button>
        </form>

        <p className="mt-4 text-center text-sm">
          <Link href={`/${locale}/login`} className="text-primary hover:underline">
            Quay lại đăng nhập
          </Link>
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Verify types**

```bash
npx tsc --noEmit 2>&1 | head -20
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add "src/app/[locale]/(auth)/"
git commit -m "feat(auth): add login, register, forgot-password pages"
```
