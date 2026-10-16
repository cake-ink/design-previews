import { fileURLToPath } from "node:url";
import path from "node:path";
import { chromium } from "/home/user/app/node_modules/playwright/index.mjs";
const OUT = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
let bad = 0;
for (const [tag, w] of [["p", 390], ["w", 1000]]) {
  for (let n = 1; n <= 6; n++) {
    const p = await b.newPage({ viewport: { width: w, height: 1400 } });
    await p.goto(`file://${OUT}/r-${tag}${n}.html`);
    const r = await p.evaluate(() => {
      const grid = document.querySelector(".photos");
      const gw = grid.getBoundingClientRect().width;
      const gap = parseFloat(getComputedStyle(grid).columnGap) || 0;
      const rows = new Map();
      for (const e of grid.querySelectorAll(".ph")) {
        const b = e.getBoundingClientRect();
        const key = Math.round(b.top);
        if (!rows.has(key)) rows.set(key, []);
        rows.get(key).push(Math.round(b.width * 100) / 100);
      }
      return [...rows.values()].map((ws) => ({
        widths: ws,
        // a row with no hole spans the grid exactly: widths + the gaps between
        filled: Math.abs(ws.reduce((a, c) => a + c, 0) + gap * (ws.length - 1) - gw) < 1.5,
        equal: ws.every((x) => Math.abs(x - ws[0]) < 1.5),
      }));
    });
    const holes = r.filter((x) => !x.filled).length;
    const uneven = r.filter((x) => !x.equal).length;
    if (holes || uneven) bad++;
    console.log(
      `${tag === "p" ? "phone " : "wide  "} n=${n}  rows=${r.map((x) => x.widths.length).join("+")}` +
      `  widths=[${r.map((x) => x.widths.join("/")).join("] [")}]` +
      `  ${holes ? `HOLE x${holes}` : "no holes"}  ${uneven ? `UNEVEN x${uneven}` : "rows even"}`,
    );
    await p.close();
  }
}
console.log(bad ? `\n${bad} case(s) FAILED` : "\nall 12 cases: every row full, every row even");
await b.close();
