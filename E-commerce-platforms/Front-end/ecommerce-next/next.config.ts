import type { NextConfig } from "next";
import withBundleAnalyzer from "@next/bundle-analyzer";
import withPWA from "@ducanh2912/next-pwa";

const withAnalyzer = withBundleAnalyzer({
  enabled: process.env.ANALYZE === "true",
});

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**.amazonaws.com" },
      { protocol: "http", hostname: "localhost" },
    ],
  },
};

export default withAnalyzer(
  withPWA({
    dest: "public",
    disable: process.env.NODE_ENV === "development",
    register: true,
    cacheOnFrontEndNav: true,
    reloadOnOnline: true,
  })(nextConfig),
);
