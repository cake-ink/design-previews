import { fileURLToPath } from "node:url";
import path from "node:path";
import { chromium } from "/home/user/app/node_modules/playwright/index.mjs";
const OUT = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
let bad = 0;
for (let n = 1; n <= 15; n++) {
  const p = await b.newPage({ viewport: { width: 390, height: 1400 } });
  await p.goto(`file://${OUT}/wc-${n}.html`);
  const r = await p.evaluate(() => {
    const g = document.querySelector(".pf");
    const gw = g.getBoundingClientRect().width;
    const gap = parseFloat(getComputedStyle(g).columnGap) || 0;
    const rows = new Map();
    for (const e of g.querySelectorAll(".cell")) {
      const r = e.getBoundingClientRect();
      const k = Math.round(r.top);
      if (!rows.has(k)) rows.set(k, []);
      rows.get(k).push(Math.round(r.width * 10) / 10);
    }
    return [...rows.values()].map((ws) => ({
      n: ws.length,
      filled: Math.abs(ws.reduce((a, c) => a + c, 0) + gap * (ws.length - 1) - gw) < 1.5,
      equal: ws.every((x) => Math.abs(x - ws[0]) < 1.5),
    }));
  });
  const holes = r.filter((x) => !x.filled).length, uneven = r.filter((x) => !x.equal).length;
  if (holes || uneven) bad++;
  console.log(`n=${String(n).padStart(2)}  rows=${r.map((x) => x.n).join("+")}`.padEnd(30) +
    `${holes ? `HOLE x${holes}` : "no holes"}  ${uneven ? `UNEVEN x${uneven}` : "rows even"}`);
  await p.close();
}
console.log(bad ? `\n${bad} FAILED` : "\n1 through 15: every row full, every row even");
await b.close();
