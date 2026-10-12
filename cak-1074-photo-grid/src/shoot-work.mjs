import { fileURLToPath } from "node:url";
import path from "node:path";
import { chromium } from "/home/user/app/node_modules/playwright/index.mjs";
const OUT = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await b.newPage({ viewport: { width: 1340, height: 1200 }, deviceScaleFactor: 2 });
await page.goto(`file://${OUT}/gallery-w2.html`);
await page.evaluate(async () => {
  for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); }
  window.scrollTo(0, 0);
});
await page.waitForTimeout(800);
const h = await page.evaluate(() => Math.ceil(document.body.scrollHeight) + 8);
await page.setViewportSize({ width: 1340, height: h });
await page.waitForTimeout(400);
await page.screenshot({ path: `${OUT}/W1-work-section.png` });
console.log("shot", h);
await b.close();
