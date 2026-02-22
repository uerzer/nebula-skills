#!/usr/bin/env node
/**
 * post-to-tiktok.js
 * Uploads slideshow images and posts to TikTok as a DRAFT via Postiz API.
 * Cross-posts to any other connected platforms simultaneously.
 *
 * Usage:
 *   node scripts/post-to-tiktok.js \
 *     --config tiktok-marketing/config.json \
 *     --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ \
 *     --caption "storytelling caption here" \
 *     --title "post title"
 *
 * Posts go to TikTok DRAFTS (SELF_ONLY), not published directly.
 * User adds trending audio manually in TikTok app before publishing.
 * This is intentional — music selection cannot be automated and matters enormously.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

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

// ─── Config ──────────────────────────────────────────────────────────────────

function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    throw new Error(`Config not found: ${configPath}. Run onboarding first.`);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// ─── Postiz API helpers ───────────────────────────────────────────────────────

function postizRequest(method, urlPath, apiKey, body) {
  return new Promise((resolve, reject) => {
    const bodyStr = body ? JSON.stringify(body) : null;
    const options = {
      hostname: 'api.postiz.com',
      path: urlPath,
      method,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        ...(bodyStr ? { 'Content-Length': Buffer.byteLength(bodyStr) } : {}),
      },
    };

    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 400) {
            return reject(new Error(`Postiz API error ${res.statusCode}: ${JSON.stringify(json)}`));
          }
          resolve(json);
        } catch (e) {
          reject(new Error(`Failed to parse Postiz response: ${data}`));
        }
      });
    });

    req.on('error', reject);
    if (bodyStr) req.write(bodyStr);
    req.end();
  });
}

// Upload a single image file to Postiz media storage
function uploadMedia(imagePath, apiKey) {
  return new Promise((resolve, reject) => {
    const fileContent = fs.readFileSync(imagePath);
    const filename = path.basename(imagePath);
    const boundary = '----FormBoundary' + Math.random().toString(36).slice(2);

    const header = Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: image/png\r\n\r\n`
    );
    const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
    const body = Buffer.concat([header, fileContent, footer]);

    const options = {
      hostname: 'api.postiz.com',
      path: '/media/upload',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
      },
    };

    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 400) {
            return reject(new Error(`Media upload error ${res.statusCode}: ${JSON.stringify(json)}`));
          }
          resolve(json.id || json.mediaId || json.url);
        } catch (e) {
          reject(new Error(`Failed to parse upload response: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs();

  if (!args.config || !args.dir || !args.caption) {
    console.error('Usage: node post-to-tiktok.js --config <path> --dir <post-dir> --caption "<text>" [--title "<text>"]');
    process.exit(1);
  }

  const config = loadConfig(args.config);
  const postDir = args.dir;
  const caption = args.caption;
  const title = args.title || '';

  const { apiKey, integrationIds } = config.postiz;
  const { schedule, crossPost = [] } = config.posting;

  if (!apiKey) throw new Error('Missing postiz.apiKey in config');
  if (!integrationIds?.tiktok) throw new Error('Missing postiz.integrationIds.tiktok in config');

  // Collect slide images in order
  const slides = fs.readdirSync(postDir)
    .filter(f => f.match(/^slide-\d+\.(png|jpg|jpeg)$/i))
    .sort()
    .map(f => path.join(postDir, f));

  if (slides.length === 0) {
    throw new Error(`No slide images found in ${postDir}`);
  }

  console.log(`\nPosting ${slides.length}-slide slideshow to TikTok (as draft)\n`);

  // ── Upload all images ──────────────────────────────────────────────────────
  console.log('Uploading images to Postiz...');
  const mediaIds = [];
  for (let i = 0; i < slides.length; i++) {
    process.stdout.write(`  Slide ${i + 1}/${slides.length}...`);
    const mediaId = await uploadMedia(slides[i], apiKey);
    mediaIds.push(mediaId);
    console.log(` uploaded (id: ${mediaId})`);
  }

  // ── Build integrations list ────────────────────────────────────────────────
  // Always include TikTok. Add cross-post platforms if configured and available.
  const integrations = [{ id: integrationIds.tiktok }];

  for (const platform of crossPost) {
    if (integrationIds[platform]) {
      integrations.push({ id: integrationIds[platform] });
      console.log(`  Cross-posting to ${platform}`);
    }
  }

  // ── Create the post ────────────────────────────────────────────────────────
  console.log('\nCreating post in Postiz...');

  // Schedule for the next posting slot if a schedule is configured
  let scheduledDate = null;
  if (schedule && schedule.length > 0) {
    const now = new Date();
    const [hours, minutes] = schedule[0].split(':').map(Number);
    const next = new Date();
    next.setHours(hours, minutes, 0, 0);
    if (next <= now) next.setDate(next.getDate() + 1);
    scheduledDate = next.toISOString();
    console.log(`  Scheduled for: ${scheduledDate}`);
  }

  const postPayload = {
    type: 'image_carousel',         // TikTok slideshow format
    content: caption,
    title: title,
    media: mediaIds.map(id => ({ id })),
    integrations,
    settings: {
      tiktok: {
        privacy_level: 'SELF_ONLY', // Post as draft — user adds music and publishes manually
        disable_duet: false,
        disable_comment: false,
        disable_stitch: false,
      },
    },
    ...(scheduledDate ? { date: scheduledDate } : {}),
  };

  const post = await postizRequest('POST', '/posts', apiKey, postPayload);

  console.log(`\n✓ Post created successfully`);
  console.log(`  Post ID: ${post.id}`);
  console.log(`  Status: ${post.status}`);
  if (scheduledDate) console.log(`  Scheduled: ${scheduledDate}`);

  console.log('\n─────────────────────────────────────────────');
  console.log('NEXT STEPS (your 60 seconds of work):');
  console.log('  1. Open TikTok app on your phone');
  console.log('  2. Go to your Drafts inbox');
  console.log('  3. Find this slideshow');
  console.log('  4. Add a trending sound from TikTok\'s library');
  console.log('  5. Hit Publish');
  console.log('─────────────────────────────────────────────');
  console.log('\nAfter publishing, wait 2+ hours then run:');
  console.log('  node scripts/check-analytics.js --config <config> --days 3 --connect\n');

  // Save post metadata for analytics tracking
  const metaPath = path.join(postDir, 'post-meta.json');
  fs.writeFileSync(metaPath, JSON.stringify({
    postId: post.id,
    postDir,
    caption,
    title,
    slideCount: slides.length,
    createdAt: new Date().toISOString(),
    scheduledAt: scheduledDate,
    tiktokIntegrationId: integrationIds.tiktok,
    releaseId: null,    // filled in by check-analytics.js after publishing
    lastChecked: null,
  }, null, 2));

  console.log(`Post metadata saved to ${metaPath}`);
}

main().catch(err => {
  console.error('\nFatal error:', err.message);
  process.exit(1);
});
