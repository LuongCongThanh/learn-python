import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin", "vietnamese"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: { default: "E-Commerce Shop", template: "%s | E-Commerce Shop" },
  description: "Mua sắm trực tuyến nhanh chóng, tiện lợi",
  manifest: "/manifest.json",
  themeColor: "#e85d04",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "E-Commerce Shop",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" suppressHydrationWarning className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
