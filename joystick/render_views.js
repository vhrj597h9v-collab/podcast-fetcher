#!/usr/bin/env node
// Headless renders of out/joystick_viewer.html -> out/views/*.png  (node render_views.js)
// three.min.js is served from a local copy when the CDN is unreachable (THREE_JS=/path/three.min.js).
const path = require("path");
const fs = require("fs");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

const HERE = __dirname;
const OUT = path.join(HERE, "out", "views");
fs.mkdirSync(OUT, { recursive: true });
const viewer = "file://" + path.join(HERE, "out", "joystick_viewer.html");

// Box sits at z 120..166; grip below. Ortho views frame the box + upper grip like a spec sheet.
const SHOTS = [
  { name: "hero",        w: 600, h: 900, q: "view=perspective&theta=-38&phi=8&dist=500&target=0,-10,86&fov=28" },
  { name: "front",       w: 500, h: 450, q: "view=front&span=110&target=0,0,140&grid=0" },
  { name: "top",         w: 500, h: 450, q: "view=top&span=120&target=0,-14,140&grid=0" },
  { name: "left",        w: 333, h: 450, q: "view=left&span=110&target=0,-16,128&grid=0" },
  { name: "right",       w: 333, h: 450, q: "view=right&span=110&target=0,-16,128&grid=0" },
  { name: "back",        w: 334, h: 450, q: "view=back&span=110&target=0,0,128&grid=0" },
  { name: "inside",      w: 500, h: 450, q: "view=perspective&theta=160&phi=12&dist=170&target=0,-8,118&fov=30&grid=0&hide=back_plate" },
  { name: "trigger",     w: 600, h: 450, q: "view=perspective&theta=-30&phi=-28&dist=210&target=0,-22,112&fov=30&grid=0" },
  { name: "thumb",       w: 700, h: 450, q: "view=perspective&theta=-75&phi=4&dist=380&target=0,-14,118&fov=28&grid=0" },
  { name: "exploded",    w: 700, h: 450, q: "view=perspective&theta=150&phi=22&dist=330&target=0,-8,125&fov=30&grid=0&explode=1" },
  { name: "perspective", w: 1200, h: 900, q: "view=perspective&theta=-35&phi=10&dist=540&target=0,-10,86&fov=28" },
];

(async () => {
  const browser = await chromium.launch({
    args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"],
  });
  const ctx = await browser.newContext({ viewport: { width: 800, height: 800 }, deviceScaleFactor: 1 });
  if (process.env.THREE_JS) {
    const js = fs.readFileSync(process.env.THREE_JS, "utf-8");
    await ctx.route("**/three.min.js", route => route.fulfill({ body: js, contentType: "application/javascript" }));
  }
  const page = await ctx.newPage();
  page.on("pageerror", e => console.error("page error:", e.message));
  for (const s of SHOTS) {
    await page.setViewportSize({ width: s.w, height: s.h });
    await page.goto(`${viewer}?shot=1&w=${s.w}&h=${s.h}&${s.q}`);
    await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
    await page.waitForTimeout(150);
    const file = path.join(OUT, `${s.name}.png`);
    await page.screenshot({ path: file, clip: { x: 0, y: 0, width: s.w, height: s.h } });
    console.log("wrote", path.relative(HERE, file));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
