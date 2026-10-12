import { chromium } from "/home/user/app/node_modules/playwright/index.mjs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const OUT = path.dirname(fileURLToPath(import.meta.url));
const JOBS = [
  ["gallery-rp.html", "R1-phone.png", 1340],
  ["gallery-rw.html", "R2-wide.png", 2180],
];

const browser = await chromium.launch({
  executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
});

// A file:// iframe is its own opaque origin, so the gallery cannot read the
// height of what it is framing. Measure each option page on its own instead,
// at the width the gallery will frame it at, and write that height in.
async function measure(src, width) {
  const p = await browser.newPage({ viewport: { width, height: 1200 } });
  await p.goto(`file://${OUT}/${src}`);
  await p.waitForTimeout(150);
  // `main` stretches to the viewport, so measure the last thing actually drawn.
  const h = await p.evaluate(() => {
    const els = [...document.querySelectorAll(".photos, .portrait")];
    return Math.ceil(Math.max(...els.map((e) => e.getBoundingClientRect().bottom))) + 18;
  });
  await p.close();
  return h;
}

for (const [src, png, width] of JOBS) {
  const page = await browser.newPage({ viewport: { width, height: 1200 } });
  await page.goto(`file://${OUT}/${src}`);

  const frames = await page.evaluate(() =>
    [...document.querySelectorAll("iframe")].map((f) => ({
      src: f.getAttribute("src"),
      w: Number(f.getAttribute("width")),
    })),
  );
  const heights = [];
  for (const f of frames) heights.push(await measure(f.src, f.w));
  await page.evaluate((hs) => {
    document.querySelectorAll("iframe").forEach((f, i) => {
      f.setAttribute("height", String(hs[i]));
      f.style.height = hs[i] + "px";
    });
  }, heights);

  // Frames far down the page never paint until they have been scrolled past.
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 500) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 50));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(600);

  // Size the window to the whole page and shoot one frame: Chromium's fullPage
  // stitching duplicates a band when the page is this tall.
  const h = await page.evaluate(() => Math.ceil(document.body.scrollHeight) + 8);
  await page.setViewportSize({ width, height: h });
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${OUT}/${png}` });
  console.log("shot", png, `${width}x${h}`, "frames:", heights.join(","));
  await page.close();
}
await browser.close();
