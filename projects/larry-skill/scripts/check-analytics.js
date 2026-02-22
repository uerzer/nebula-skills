#!/usr/bin/env node
/**
 * check-analytics.js
 * Connects Postiz posts to their TikTok video IDs, then fetches per-post analytics.
 * Run this daily (handled automatically by daily-report.js cron).
 *
 * Usage:
 *   node scripts/check-analytics.js --config tiktok-marketing/config.json --days 3 --connect
 *
 * Flags:
 *   --days N     How many days back to check (default: 3)
 *   --connect    Also attempt to connect unlinked posts to their TikTok video IDs
 *
 * ⚠️  CRITICAL: Always wait 2+ hours after publishing before running --connect.
 *     TikTok's API has an indexing delay. Connecting too early = permanent wrong ID.
 *     Once a release ID is set via PUT /posts/{id}/release-id it CANNOT be changed.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');

// ─── CLI args ─────────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { connect: false, days: 3 };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--connect') result.connect = true;
    else if (args[i].startsWith('--')) {
      result[args[i].slice(2)] = args[i + 1];
      i++;
    }
  }
  result.days = parseInt(result.days, 10);
  return result;
}

// ─── Config ───────────────────────────────────────────────────────────────────

function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) throw new Error(`Config not found: ${configPath}`);
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// ─── Postiz API ───────────────────────────────────────────────────────────────

function postizGet(urlPath, apiKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.postiz.com',
      path: urlPath,
      method: 'GET',
      headers: { 'Authorization': `Bearer ${apiKey}` },
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`Parse error: ${data}`)); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

function postizPut(urlPath, apiKey, body) {
  return new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const options = {
      hostname: 'api.postiz.com',
      path: urlPath,
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`Parse error: ${data}`)); }
      });
    });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

// ─── Date helpers ─────────────────────────────────────────────────────────────

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  d.setHours(0, 0, 0, 0);
  return d;
}

function hoursAgo(n) {
  return new Date(Date.now() - n * 60 * 60 * 1000);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs();

  if (!args.config) {
    console.error('Usage: node check-analytics.js --config <path> [--days N] [--connect]');
    process.exit(1);
  }

  const config = loadConfig(args.config);
  const { apiKey, integrationIds } = config.postiz;
  const snapshotPath = 'tiktok-marketing/analytics-snapshot.json';

  // Load existing snapshot or start fresh
  let snapshot = { lastUpdated: null, posts: [] };
  if (fs.existsSync(snapshotPath)) {
    snapshot = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  }

  const cutoff = daysAgo(args.days);
  const twoHoursAgo = hoursAgo(2);

  console.log(`\nChecking analytics for last ${args.days} days (since ${cutoff.toDateString()})\n`);

  // ── Fetch recent posts from Postiz ─────────────────────────────────────────
  console.log('Fetching posts from Postiz...');
  const postsResponse = await postizGet(`/posts?page=1&limit=100`, apiKey);
  const allPosts = postsResponse.posts || postsResponse.items || postsResponse || [];

  const recentPosts = allPosts.filter(p => {
    const publishDate = new Date(p.publishDate || p.date || p.createdAt);
    return publishDate >= cutoff;
  });

  console.log(`  Found ${recentPosts.length} posts in the last ${args.days} days\n`);

  const results = [];

  for (const post of recentPosts) {
    const publishDate = new Date(post.publishDate || post.date || post.createdAt);
    const postId = post.id;
    const releaseId = post.releaseId || null;

    console.log(`Post ${postId} (published ${publishDate.toISOString().slice(0, 16)})`);

    // ── Skip posts too recent to be indexed by TikTok ─────────────────────
    if (publishDate > twoHoursAgo) {
      console.log(`  ⚠️  Too recent (< 2 hours old) — skipping to avoid wrong ID connection`);
      results.push({ postId, publishDate: publishDate.toISOString(), status: 'too_recent' });
      continue;
    }

    // ── Connect unlinked posts ─────────────────────────────────────────────
    if (!releaseId && args.connect) {
      console.log(`  No release ID — attempting to connect to TikTok video...`);

      try {
        const missing = await postizGet(`/posts/${postId}/missing`, apiKey);
        const videos = missing.videos || missing || [];

        if (videos.length === 0) {
          console.log(`  No unconnected TikTok videos found`);
          results.push({ postId, publishDate: publishDate.toISOString(), status: 'no_videos_found' });
          continue;
        }

        // Sort videos by ID numerically ascending (lowest ID = oldest video)
        videos.sort((a, b) => {
          const idA = BigInt(a.id);
          const idB = BigInt(b.id);
          return idA < idB ? -1 : idA > idB ? 1 : 0;
        });

        // Match: oldest unconnected Postiz post → lowest unconnected TikTok ID
        // This relies on both Postiz and TikTok maintaining chronological order
        const targetVideo = videos[0];

        console.log(`  Connecting to TikTok video ${targetVideo.id}`);
        console.log(`  Thumbnail: ${targetVideo.thumbnail}`);
        console.log(`  ⚠️  Verify this thumbnail matches your post before proceeding!`);

        await postizPut(`/posts/${postId}/release-id`, apiKey, { releaseId: targetVideo.id });
        console.log(`  ✓ Connected`);

        post.releaseId = targetVideo.id;

      } catch (err) {
        console.error(`  Failed to connect: ${err.message}`);
        results.push({ postId, publishDate: publishDate.toISOString(), status: 'connect_failed', error: err.message });
        continue;
      }
    }

    // ── Fetch per-post analytics ───────────────────────────────────────────
    if (post.releaseId) {
      try {
        const analytics = await postizGet(`/analytics/post/${postId}`, apiKey);
        const entry = {
          postId,
          publishDate: publishDate.toISOString(),
          tiktokId: post.releaseId,
          views: analytics.views || 0,
          likes: analytics.likes || 0,
          comments: analytics.comments || 0,
          shares: analytics.shares || 0,
          bookmarks: analytics.bookmarks || 0,
          lastChecked: new Date().toISOString(),
          status: 'connected',
        };

        console.log(`  Views: ${entry.views.toLocaleString()} | Likes: ${entry.likes} | Comments: ${entry.comments} | Shares: ${entry.shares}`);
        results.push(entry);

        // Update existing entry in snapshot or add new one
        const existingIdx = snapshot.posts.findIndex(p => p.postId === postId);
        if (existingIdx >= 0) {
          snapshot.posts[existingIdx] = { ...snapshot.posts[existingIdx], ...entry };
        } else {
          snapshot.posts.push(entry);
        }

      } catch (err) {
        console.error(`  Failed to fetch analytics: ${err.message}`);
        results.push({ postId, publishDate: publishDate.toISOString(), status: 'analytics_failed', error: err.message });
      }
    } else {
      console.log(`  No release ID — run with --connect flag after publishing`);
      results.push({ postId, publishDate: publishDate.toISOString(), status: 'not_connected' });
    }

    console.log('');
  }

  // ── Save snapshot ──────────────────────────────────────────────────────────
  snapshot.lastUpdated = new Date().toISOString();
  fs.mkdirSync('tiktok-marketing', { recursive: true });
  fs.writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2));

  // ── Summary ────────────────────────────────────────────────────────────────
  const connected = results.filter(r => r.status === 'connected');
  const totalViews = connected.reduce((sum, r) => sum + (r.views || 0), 0);

  console.log('─────────────────────────────────────────────');
  console.log(`Summary: ${connected.length}/${recentPosts.length} posts with analytics`);
  console.log(`Total views (last ${args.days} days): ${totalViews.toLocaleString()}`);
  console.log(`Snapshot saved to: ${snapshotPath}`);
  console.log('─────────────────────────────────────────────\n');
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
