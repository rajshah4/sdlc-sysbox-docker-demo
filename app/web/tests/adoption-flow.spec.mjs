import { expect, test } from "@playwright/test";

test.beforeEach(async ({ request }) => {
  await request.post("/api/demo/reset");
});

test("customer can submit an adoption through the web stack", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Containerized Petstore" })).toBeVisible();
  const mochi = page.locator('li.pet[data-pet-id="pet-100"]');
  await expect(mochi).toContainText("Mochi");
  await mochi.getByRole("button", { name: "Adopt" }).click();
  await expect(page.getByRole("status")).toHaveText("Mochi's adoption request was accepted.");
  await expect(mochi).toHaveCount(0);
  await page.screenshot({ path: "/artifacts/adoption-success.png", fullPage: true });
});
