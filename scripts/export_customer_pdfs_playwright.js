#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const EXPORTS_ROOT = path.join(ROOT, "content-elevated-product-os", "exports");
const BATCHES = {
  "phase-1": path.join(EXPORTS_ROOT, "phase-1-payhip-source-package"),
  next: path.join(EXPORTS_ROOT, "next-batch-source-package"),
  standard: path.join(EXPORTS_ROOT, "standard-queue-source-package"),
};

function argValue(name, fallback = "") {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function hasArg(name) {
  return process.argv.includes(name);
}

function readList(name) {
  const index = process.argv.indexOf(name);
  if (index < 0) return [];
  const values = [];
  for (let i = index + 1; i < process.argv.length; i += 1) {
    if (process.argv[i].startsWith("--")) break;
    values.push(process.argv[i]);
  }
  return values;
}

function globToRegExp(pattern) {
  const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*");
  return new RegExp(`^${escaped}$`);
}

function listProducts(batchRoot, only) {
  return fs
    .readdirSync(batchRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((name) => fs.existsSync(path.join(batchRoot, name, "html")))
    .filter((name) => !only.length || only.includes(name))
    .sort();
}

function listHtmlFiles(productRoot, pattern) {
  const htmlRoot = path.join(productRoot, "html");
  const matcher = globToRegExp(pattern || "*.html");
  return fs
    .readdirSync(htmlRoot)
    .filter((name) => matcher.test(name))
    .sort()
    .map((name) => path.join(htmlRoot, name));
}

function copySpreadsheets(productRoot, destinationRoot) {
  const sourceRoot = path.join(productRoot, "spreadsheets");
  if (!fs.existsSync(sourceRoot)) return [];
  const destination = path.join(destinationRoot, "spreadsheets");
  fs.mkdirSync(destination, { recursive: true });
  const copied = [];
  for (const name of fs.readdirSync(sourceRoot).filter((item) => item.endsWith(".xlsx")).sort()) {
    fs.copyFileSync(path.join(sourceRoot, name), path.join(destination, name));
    copied.push(name);
  }
  return copied;
}

async function exportPdf(page, htmlPath, pdfPath, timeout) {
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle", timeout });
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: pdfPath,
    format: "Letter",
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
    timeout,
  });
  const stats = fs.statSync(pdfPath);
  if (stats.size < 10000) throw new Error(`PDF looks too small: ${stats.size} bytes`);
  return stats.size;
}

async function main() {
  const batchKey = argValue("--batch", "phase-1");
  const outputRoot = path.resolve(argValue("--output", path.join(EXPORTS_ROOT, "customer-pdf-playwright-export")));
  const htmlPattern = argValue("--html-pattern", "*.html");
  const only = readList("--only");
  const timeout = Number(argValue("--timeout", "90000"));
  const headful = hasArg("--headful");

  if (!BATCHES[batchKey]) {
    console.error(`Unknown batch: ${batchKey}`);
    process.exit(1);
  }

  const batchRoot = BATCHES[batchKey];
  const products = listProducts(batchRoot, only);
  fs.mkdirSync(outputRoot, { recursive: true });

  const browser = await chromium.launch({ headless: !headful });
  const context = await browser.newContext({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 1 });
  const page = await context.newPage();

  const results = [];
  let errorCount = 0;

  for (const product of products) {
    const productRoot = path.join(batchRoot, product);
    const destinationRoot = path.join(outputRoot, batchKey, product);
    const pdfRoot = path.join(destinationRoot, "pdfs");
    fs.mkdirSync(pdfRoot, { recursive: true });
    console.log(`Exporting ${batchKey}: ${product}`);

    const exported = [];
    const errors = [];
    for (const htmlPath of listHtmlFiles(productRoot, htmlPattern)) {
      const pdfName = `${path.basename(htmlPath, ".html")}.pdf`;
      const pdfPath = path.join(pdfRoot, pdfName);
      process.stdout.write(`  - ${path.basename(htmlPath)} -> ${pdfName}`);
      try {
        const bytes = await exportPdf(page, htmlPath, pdfPath, timeout);
        exported.push({ source: path.basename(htmlPath), pdf: pdfName, bytes });
        console.log(" OK");
      } catch (error) {
        errorCount += 1;
        errors.push(`${path.basename(htmlPath)}: ${error.message}`);
        console.log(` ERROR: ${error.message}`);
      }
    }

    const spreadsheets = copySpreadsheets(productRoot, destinationRoot);
    const lines = [
      `# ${product} Playwright Export Manifest`,
      "",
      `Batch: ${batchKey}`,
      "",
      "## PDFs",
      "",
      ...exported.map((item) => `- \`pdfs/${item.pdf}\` from \`${item.source}\` (${(item.bytes / 1000000).toFixed(1)} MB)`),
      "",
      "## Spreadsheets",
      "",
      ...(spreadsheets.length ? spreadsheets.map((name) => `- \`spreadsheets/${name}\``) : ["- None."]),
    ];
    if (errors.length) lines.push("", "## Errors", "", ...errors.map((error) => `- ${error}`));
    fs.writeFileSync(path.join(destinationRoot, "MANIFEST.md"), `${lines.join("\n")}\n`);
    results.push({ product, pdfs: exported.length, errors: errors.length });
  }

  await browser.close();

  const summary = [
    "# Playwright Customer PDF Export",
    "",
    `Output folder: \`${path.relative(ROOT, outputRoot)}\``,
    "",
    `Products processed: ${results.length}`,
    `Errors: ${errorCount}`,
    "",
    ...results.map((item) => `- ${item.errors ? "Needs review" : "OK"}: \`${batchKey}/${item.product}\` PDFs ${item.pdfs}, errors ${item.errors}`),
  ];
  fs.writeFileSync(path.join(outputRoot, "EXPORT_SUMMARY.md"), `${summary.join("\n")}\n`);
  console.log("");
  console.log(`Export folder: ${path.relative(ROOT, outputRoot)}`);
  console.log(`Products processed: ${results.length}`);
  console.log(`Errors: ${errorCount}`);
  process.exit(errorCount ? 1 : 0);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
