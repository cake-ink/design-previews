import { fileURLToPath } from "node:url";
import path from "node:path";
import { chromium } from "/home/user/app/node_modules/playwright/index.mjs";
const OUT = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const k of ["wt"]) {
  const page = await b.newPage({ viewport: { width: 1340, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto(`file://${OUT}/gallery-wt.html`);
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(900);
  const h = await page.evaluate(() => Math.ceil(document.body.scrollHeight) + 8);
  await page.setViewportSize({ width: 1340, height: h });
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${OUT}/WT-wishlist.png` });
  console.log("shot", k, h);
  await page.close();
}
await b.close();
