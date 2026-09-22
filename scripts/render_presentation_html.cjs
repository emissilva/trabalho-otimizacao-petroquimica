const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const html = path.join(root, 'apresentacao', 'apresentacao.html');
const pdf = path.join(root, 'apresentacao', 'apresentacao.pdf');
const png = path.join('/private/tmp', 'petrochem-presentation-preview.png');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await page.goto(`file://${html}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: png, fullPage: true });
  await page.pdf({
    path: pdf,
    width: '13.333in',
    height: '7.5in',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '0in', right: '0in', bottom: '0in', left: '0in' },
  });
  await browser.close();
  console.log(`HTML renderizado: ${pdf}`);
  console.log(`Preview: ${png}`);
})();
