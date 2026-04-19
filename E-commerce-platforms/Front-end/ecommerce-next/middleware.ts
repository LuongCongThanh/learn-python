import createMiddleware from "next-intl/middleware";
import { NextRequest, NextResponse } from "next/server";

const intlMiddleware = createMiddleware({
  locales: ["vi", "en"],
  defaultLocale: "vi",
});

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

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
