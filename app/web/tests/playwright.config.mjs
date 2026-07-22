import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  timeout: 30_000,
  use: {
    baseURL: process.env.PETSTORE_WEB_URL || "http://localhost:8080",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  outputDir: "/artifacts/playwright",
});
