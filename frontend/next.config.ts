import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Copy only the production server and its runtime dependencies into the
  // final Docker image, rather than the complete node_modules tree.
  output: "standalone",
  reactStrictMode: true,
};

export default nextConfig;
