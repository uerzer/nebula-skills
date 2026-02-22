#!/usr/bin/env node
/**
 * add-text-overlay.js
 * Adds text overlays to slide images using node-canvas.
 * This is the exact code Larry uses for viral TikTok slides.
 *
 * Usage:
 *   node scripts/add-text-overlay.js --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ --texts texts.json
 *
 * texts.json format (use \n for manual line breaks — always prefer manual breaks):
 * [
 *   "I showed my landlord\nwhat AI thinks our\nkitchen should look like",
 *   "She said you can't\nchange anything\nchallenge accepted",
 *   "So I downloaded\nthis app and\ntook one photo",
 *   "Wait... is this\nactually the same\nkitchen??",
 *   "Okay I'm literally\nobsessed with\nthis one",
 *   "Snugly showed me\nwhat's possible\nlink in bio"
 * ]
 *
 * Slide 1 gets the hook overlay. Remaining slides get their corresponding text.
 * Pass null or "" for slides that should have no text.
 *
 * node-canvas install:
 *   npm install canvas
 *   macOS:   brew install pkg-config cairo pango libpng jpeg giflib librsvg && npm install canvas
 *   Ubuntu:  sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev && npm install canvas
 *   Windows: npm install canvas  (auto downloads prebuilt binaries)
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ─── CLI args ────────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      result[args[i].slice(2)] = args[i + 1];
      i++;
    }
  }
  return result;
}

// ─── Core overlay function (exact Larry implementation) ──────────────────────

async function addOverlay(imagePath, text, outputPath) {
  let createCanvas, loadImage;
  try {
    ({ createCanvas, loadImage } = require('canvas'));
  } catch (e) {
    console.error('\n  ERROR: node-canvas is not installed.');
    console.error('  Run: npm install canvas');
    console.error('  macOS: brew install pkg-config cairo pango libpng jpeg giflib librsvg && npm install canvas');
    console.error('  Ubuntu: sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev && npm install canvas\n');
    process.exit(1);
  }

  const img = await loadImage(imagePath);
  const canvas = createCanvas(img.width, img.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);

  // ─── Dynamic font size based on text length ───────────────────────────────
  // Short hooks get bigger text (more impact), long hooks get smaller (still readable)
  const wordCount = text.split(/\s+/).length;
  let fontSizePercent;
  if (wordCount <= 5)       fontSizePercent = 0.075;  // Short:  ~77px on 1024w
  else if (wordCount <= 12) fontSizePercent = 0.065;  // Medium: ~67px
  else                      fontSizePercent = 0.050;  // Long:   ~51px

  const fontSize = Math.round(img.width * fontSizePercent);
  const outlineWidth = Math.round(fontSize * 0.15);  // Thick outline = readable on any background
  const maxWidth = img.width * 0.75;                 // 75% width max — prevents edge crowding
  const lineHeight = fontSize * 1.3;

  ctx.font = `bold ${fontSize}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';

  // ─── Word wrap ────────────────────────────────────────────────────────────
  // Respect manual \n breaks first, then auto-wrap lines that exceed maxWidth
  const lines = [];
  const manualLines = text.split('\n');
  for (const ml of manualLines) {
    const words = ml.trim().split(/\s+/);
    let current = '';
    for (const word of words) {
      const test = current ? `${current} ${word}` : word;
      if (ctx.measureText(test).width <= maxWidth) {
        current = test;
      } else {
        if (current) lines.push(current);
        current = word;
      }
    }
    if (current) lines.push(current);
  }

  // ─── Position: centered vertically around 28% from top ───────────────────
  // Safe zones: top 10% = status bar, bottom 20% = TikTok controls
  // 28% from top keeps the text block in the clear visible zone
  const totalHeight = lines.length * lineHeight;
  const startY = (img.height * 0.28) - (totalHeight / 2);
  const x = img.width / 2;

  // ─── Draw each line with outline then fill ────────────────────────────────
  for (let i = 0; i < lines.length; i++) {
    const y = startY + (i * lineHeight);

    // Black outline first (drawn under the fill)
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = outlineWidth;
    ctx.lineJoin = 'round';
    ctx.miterLimit = 2;
    ctx.strokeText(lines[i], x, y);

    // White fill on top
    ctx.fillStyle = '#FFFFFF';
    ctx.fillText(lines[i], x, y);
  }

  fs.writeFileSync(outputPath, canvas.toBuffer('image/png'));
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs();

  if (!args.dir || !args.texts) {
    console.error('Usage: node add-text-overlay.js --dir <post-dir> --texts <texts.json>');
    process.exit(1);
  }

  const postDir = args.dir;
  const texts = JSON.parse(fs.readFileSync(args.texts, 'utf8'));

  if (!fs.existsSync(postDir)) {
    console.error(`Post directory not found: ${postDir}`);
    process.exit(1);
  }

  // Find all slide images in the directory
  const slides = fs.readdirSync(postDir)
    .filter(f => f.match(/^slide-\d+\.(png|jpg|jpeg)$/i))
    .sort();

  if (slides.length === 0) {
    console.error(`No slide images found in ${postDir}. Run generate-slides.js first.`);
    process.exit(1);
  }

  console.log(`\nAdding text overlays to ${slides.length} slides in ${postDir}\n`);

  for (let i = 0; i < slides.length; i++) {
    const slideFile = slides[i];
    const text = texts[i];
    const inputPath = path.join(postDir, slideFile);

    // Skip slides with no text
    if (!text || text.trim() === '') {
      console.log(`  Slide ${i + 1}: no text — skipping overlay`);
      continue;
    }

    // Output to same file (overlay is destructive — keep originals if needed)
    const outputPath = inputPath;

    console.log(`  Slide ${i + 1}: "${text.replace(/\n/g, ' | ')}"`);
    await addOverlay(inputPath, text, outputPath);
    console.log(`  Slide ${i + 1}: done → ${outputPath}`);
  }

  console.log('\nAll overlays applied.');
  console.log('Next step: node scripts/post-to-tiktok.js --config <config> --dir <post-dir> --caption "..." --title "..."\n');
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
