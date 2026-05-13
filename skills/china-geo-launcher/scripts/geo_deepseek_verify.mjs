#!/usr/bin/env node
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const args = process.argv.slice(2);
function getArg(name, fallback = "") {
  const index = args.indexOf(name);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

const runDir = path.resolve(getArg("--run-dir", "geo-runs/20260513-150527-ai实战案例"));
const userDataDir = path.resolve(getArg("--user-data-dir", ".playwright-profile"));
const query = getArg("--query", "冲量AI是谁？主要分享什么AI内容？");
const outDir = path.join(runDir, "deepseek");
await fs.mkdir(outDir, { recursive: true });

const context = await chromium.launchPersistentContext(userDataDir, {
  headless: false,
  viewport: { width: 1280, height: 900 },
  args: ["--disable-crash-reporter", "--disable-crashpad"],
});

const page = context.pages()[0] || await context.newPage();
await page.goto("https://chat.deepseek.com/", { waitUntil: "domcontentloaded", timeout: 60000 });
await page.waitForTimeout(5000);

async function bodyText() {
  return await page.locator("body").innerText({ timeout: 15000 }).catch((error) => `ERROR: ${error.message}`);
}

async function findComposer() {
  const selectors = [
    "textarea",
    "[contenteditable='true']",
    "div[role='textbox']",
    "input[type='text']",
  ];
  for (const selector of selectors) {
    const locator = page.locator(selector).last();
    if ((await locator.count()) > 0 && await locator.isVisible().catch(() => false)) {
      return locator;
    }
  }
  return null;
}

const beforeText = await bodyText();
const composer = await findComposer();
let status = "blocked";
let blocker = "";
let answerText = "";

if (!composer) {
  blocker = "composer_not_found_or_not_logged_in";
} else {
  await composer.click();
  await page.keyboard.insertText(query);
  await page.keyboard.press("Enter");
  status = "submitted";
  await page.waitForTimeout(30000);
  const afterText = await bodyText();
  answerText = afterText.replace(beforeText, "").trim();
  if (!answerText) {
    answerText = afterText;
  }
}

const screenshotPath = path.join(outDir, "deepseek-verification.png");
await page.screenshot({ path: screenshotPath, fullPage: true });

const evidence = {
  provider: "deepseek",
  method: "playwright",
  query,
  status,
  blocker,
  url: page.url(),
  title: await page.title().catch(() => ""),
  answer_excerpt: answerText.slice(0, 4000),
  mentioned_names: answerText.includes("冲量AI") ? ["冲量AI"] : [],
  citation_urls: [...answerText.matchAll(/https?:\/\/\S+/g)].map((match) => match[0]),
  screenshot: screenshotPath,
  captured_at: new Date().toISOString(),
};

await fs.writeFile(path.join(outDir, "deepseek-evidence.json"), JSON.stringify(evidence, null, 2), "utf8");
console.log(JSON.stringify(evidence, null, 2));
await context.close();
