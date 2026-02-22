#!/usr/bin/env node
/**
 * daily-report.js
 * The intelligence core. Runs every morning via cron.
 * Pulls Postiz analytics + RevenueCat conversions, diagnoses each post,
 * and generates a report with specific recommendations.
 *
 * Usage:
 *   node scripts/daily-report.js --config tiktok-marketing/config.json --days 3
 *
 * Output:
 *   tiktok-marketing/reports/YYYY-MM-DD.md
 *   tiktok-marketing/hook-performance.json (updated)
 *   Console summary for agent to relay to user
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const https = require('https');

// ─── CLI args ─────────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { days: 3 };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) { result[args[i].slice(2)] = args[i + 1]; i++; }
  }
  result.days = parseInt(result.days, 10);
  return result;
}

// ─── Config ───────────────────────────────────────────────────────────────────

function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) throw new Error(`Config not found: ${configPath}`);
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// ─── RevenueCat API ───────────────────────────────────────────────────────────

function rcGet(urlPath, apiKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.revenuecat.com',
      path: urlPath,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'X-Platform': 'stripe',
      },
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`RC parse error: ${data.slice(0, 200)}`)); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// ─── Conversion attribution ───────────────────────────────────────────────────
// Attributes a transaction to a post if it happened 0-72h after publish.
// We skip the first 24h for posts that are still ramping up.

function attributeConversions(posts, transactions) {
  const attributed = {};
  for (const post of posts) {
    attributed[post.postId] = 0;
    const publishTime = new Date(post.publishDate).getTime();
    const windowEnd   = publishTime + 72 * 60 * 60 * 1000;
    for (const txn of transactions) {
      const txnTime = new Date(txn.purchased_at || txn.purchasedAt).getTime();
      if (txnTime >= publishTime && txnTime <= windowEnd) {
        attributed[post.postId]++;
      }
    }
  }
  return attributed;
}

// ─── Diagnostic framework ─────────────────────────────────────────────────────

const VIEW_HIGH  = 10000;  // above this = high views
const CONV_HIGH  = 1;      // at least 1 attributed conversion = high conversion

function diagnose(post, conversions) {
  const views = post.views || 0;
  const conv  = conversions[post.postId] || 0;
  const highViews = views >= VIEW_HIGH;
  const highConv  = conv  >= CONV_HIGH;

  if (highViews && highConv)  return { code: 'SCALE',     emoji: '🟢', label: 'SCALE IT',       action: `Make 3 hook variations immediately. ${views.toLocaleString()} views + ${conv} conversion(s). This is working.` };
  if (highViews && !highConv) return { code: 'FIX_CTA',   emoji: '🟡', label: 'FIX THE CTA',   action: `Hook is great (${views.toLocaleString()} views) but CTA isn't converting. Rotate slide 6 CTA. Check App Store page matches the promise.` };
  if (!highViews && highConv) return { code: 'FIX_HOOK',  emoji: '🟡', label: 'FIX THE HOOK',  action: `Content converts (${conv} conversion(s)) but only ${views.toLocaleString()} views. Test radically different hooks. Keep the CTA unchanged.` };
  return                             { code: 'RESET',      emoji: '🔴', label: 'FULL RESET',    action: `Low views (${views.toLocaleString()}) and no conversions. Try a completely different format or audience angle.` };
}

// ─── Hook performance tracker ─────────────────────────────────────────────────

function updateHookPerformance(posts, conversions, config) {
  const hookPath = 'tiktok-marketing/hook-performance.json';
  let data = { hooks: [], ctas: [], rules: { doubleDown: [], testing: [], dropped: [] } };
  if (fs.existsSync(hookPath)) data = JSON.parse(fs.readFileSync(hookPath, 'utf8'));

  for (const post of posts) {
    const existing = data.hooks.find(h => h.postId === post.postId);
    const entry = {
      postId: post.postId,
      publishDate: post.publishDate,
      views: post.views || 0,
      likes: post.likes || 0,
      comments: post.comments || 0,
      shares: post.shares || 0,
      conversions: conversions[post.postId] || 0,
      lastChecked: new Date().toISOString(),
    };

    if (existing) {
      Object.assign(existing, entry);
    } else {
      data.hooks.push(entry);
    }

    // Update decision rules
    if ((post.views || 0) >= 50000 && !data.rules.doubleDown.includes(post.postId)) {
      data.rules.doubleDown.push(post.postId);
    }
    if ((post.views || 0) < 1000) {
      const idx = data.rules.testing.indexOf(post.postId);
      if (idx >= 0) data.rules.testing.splice(idx, 1);
      if (!data.rules.dropped.includes(post.postId)) data.rules.dropped.push(post.postId);
    }
  }

  fs.writeFileSync(hookPath, JSON.stringify(data, null, 2));
  return data;
}

// ─── Report generation ────────────────────────────────────────────────────────

function generateReport(posts, conversions, rcMetrics, config) {
  const date = new Date().toISOString().slice(0, 10);
  const lines = [];

  lines.push(`# Daily Marketing Report — ${date}`);
  lines.push(`\n_Generated by Larry | ${posts.length} posts analysed | ${args.days}-day window_\n`);

  // ── MRR snapshot ──────────────────────────────────────────────────────────
  if (rcMetrics) {
    lines.push('## Business Overview');
    lines.push(`| Metric | Value |`);
    lines.push(`|--------|-------|`);
    lines.push(`| MRR | $${(rcMetrics.mrr?.value || 0).toFixed(2)} |`);
    lines.push(`| Active Subscribers | ${rcMetrics.active_subscriptions?.value || 'N/A'} |`);
    lines.push(`| Active Trials | ${rcMetrics.active_trials?.value || 'N/A'} |`);
    lines.push(`| Trial → Paid Rate | ${rcMetrics.trial_conversion_rate ? (rcMetrics.trial_conversion_rate.value * 100).toFixed(1) + '%' : 'N/A'} |`);
    lines.push(`| Churn Rate | ${rcMetrics.churn_rate ? (rcMetrics.churn_rate.value * 100).toFixed(2) + '%' : 'N/A'} |`);
    lines.push('');
  }

  // ── Per-post diagnostics ──────────────────────────────────────────────────
  lines.push('## Post Performance');
  lines.push('');

  const totalViews = posts.reduce((s, p) => s + (p.views || 0), 0);
  const totalConv  = posts.reduce((s, p) => s + (conversions[p.postId] || 0), 0);

  lines.push(`**Total views (${args.days} days):** ${totalViews.toLocaleString()}`);
  lines.push(`**Total conversions attributed:** ${totalConv}`);
  lines.push('');

  const sorted = [...posts].sort((a, b) => (b.views || 0) - (a.views || 0));

  for (const post of sorted) {
    const diag = diagnose(post, conversions);
    const conv = conversions[post.postId] || 0;
    lines.push(`### ${diag.emoji} Post ${post.postId}`);
    lines.push(`- **Published:** ${new Date(post.publishDate).toLocaleString()}`);
    lines.push(`- **Views:** ${(post.views || 0).toLocaleString()}`);
    lines.push(`- **Engagement:** ${post.likes || 0} likes · ${post.comments || 0} comments · ${post.shares || 0} shares`);
    lines.push(`- **Attributed conversions:** ${conv}`);
    lines.push(`- **Diagnosis:** ${diag.label}`);
    lines.push(`- **Action:** ${diag.action}`);
    lines.push('');
  }

  // ── Business-level signals ────────────────────────────────────────────────
  if (rcMetrics) {
    lines.push('## Business Signals');
    const trialRate = rcMetrics.trial_conversion_rate?.value || 0;
    const churnRate = rcMetrics.churn_rate?.value || 0;

    if (totalViews > 20000 && totalConv === 0) {
      lines.push('⚠️  **High views, zero conversions** — CTAs may need rotating. Check App Store page alignment.');
    }
    if (trialRate < 0.30) {
      lines.push(`⚠️  **Low trial conversion rate (${(trialRate * 100).toFixed(1)}%)** — Consider pausing new content and fixing the app onboarding or paywall.`);
    }
    if (churnRate > 0.05) {
      lines.push(`⚠️  **High churn (${(churnRate * 100).toFixed(2)}%)** — Users are leaving. Investigate app value delivery before scaling marketing.`);
    }
    if (trialRate >= 0.40 && totalViews > 0) {
      lines.push(`✅  **Strong trial conversion (${(trialRate * 100).toFixed(1)}%)** — App experience is solid. Focus on increasing view volume.`);
    }
    lines.push('');
  }

  // ── Hook suggestions ──────────────────────────────────────────────────────
  lines.push('## Suggested Hooks for Today');
  lines.push('');
  const winners = sorted.filter(p => (p.views || 0) >= VIEW_HIGH);
  if (winners.length > 0) {
    lines.push('Based on top performers, try variations of these formats:');
    lines.push('- **Person + conflict + AI result** (highest engagement pattern)');
    lines.push('- **POV format** with specific scenario');
    lines.push('- **Challenge accepted** reaction format');
  } else {
    lines.push('No high performers yet. Keep testing hook categories:');
    lines.push('- **Week 1-2:** Person + conflict format ("I showed my landlord...")');
    lines.push('- **Alternate:** POV format ("POV: AI just redesigned my flat")');
    lines.push('- **Try:** Surprise/disbelief ("Wait... is this the same room??")');
  }

  lines.push('');
  lines.push('## CTA Rotation');
  lines.push('If views are high but conversions are low, try these CTAs in order:');
  lines.push('1. "Download [App] — link in bio"');
  lines.push('2. "[App] is free to try — link in bio"');
  lines.push('3. "I used [App] for this — link in bio"');
  lines.push('4. "Search [App] on the App Store"');
  lines.push('5. No explicit CTA (just app name visible)');

  return lines.join('\n');
}

// ─── Main ─────────────────────────────────────────────────────────────────────

let args;

async function main() {
  args = parseArgs();

  if (!args.config) {
    console.error('Usage: node daily-report.js --config <path> [--days N]');
    process.exit(1);
  }

  const config = loadConfig(args.config);

  // First, run analytics check to ensure snapshot is fresh
  console.log('Running analytics check first...');
  try {
    const { execSync } = require('child_process');
    execSync(`node ${path.join(__dirname, 'check-analytics.js')} --config ${args.config} --days ${args.days} --connect`, {
      stdio: 'inherit',
      timeout: 120000,
    });
  } catch (e) {
    console.warn('Analytics check had issues — using existing snapshot if available');
  }

  // Load snapshot
  const snapshotPath = 'tiktok-marketing/analytics-snapshot.json';
  if (!fs.existsSync(snapshotPath)) {
    console.error('No analytics snapshot found. Run check-analytics.js first.');
    process.exit(1);
  }
  const snapshot = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  const cutoff = new Date(Date.now() - args.days * 24 * 60 * 60 * 1000);
  const posts = (snapshot.posts || []).filter(p => new Date(p.publishDate) >= cutoff && p.status === 'connected');

  console.log(`\nAnalysing ${posts.length} connected posts from last ${args.days} days\n`);

  // ── RevenueCat data ────────────────────────────────────────────────────────
  let rcMetrics = null;
  let transactions = [];

  if (config.revenuecat?.enabled && config.revenuecat?.v2SecretKey) {
    console.log('Fetching RevenueCat data...');
    try {
      const projectId = config.revenuecat.projectId;
      const rcKey = config.revenuecat.v2SecretKey;

      rcMetrics = await rcGet(`/v2/projects/${projectId}/metrics/overview`, rcKey);

      const startDate = cutoff.toISOString().slice(0, 10);
      const endDate = new Date().toISOString().slice(0, 10);
      const txnResponse = await rcGet(`/v2/projects/${projectId}/transactions?start_time=${startDate}T00:00:00Z&end_time=${endDate}T23:59:59Z`, rcKey);
      transactions = txnResponse.items || txnResponse.transactions || [];

      console.log(`  MRR: $${(rcMetrics.mrr?.value || 0).toFixed(2)}`);
      console.log(`  Transactions in window: ${transactions.length}`);

      // Save RC snapshot
      fs.mkdirSync('tiktok-marketing', { recursive: true });
      fs.writeFileSync('tiktok-marketing/rc-snapshot.json', JSON.stringify({
        date: new Date().toISOString().slice(0, 10),
        mrr: rcMetrics.mrr?.value,
        activeSubscriptions: rcMetrics.active_subscriptions?.value,
        activeTrials: rcMetrics.active_trials?.value,
        churnRate: rcMetrics.churn_rate?.value,
        trialConversionRate: rcMetrics.trial_conversion_rate?.value,
        newTransactions: transactions,
      }, null, 2));

    } catch (err) {
      console.warn(`  RevenueCat fetch failed: ${err.message}. Continuing without RC data.`);
    }
  } else {
    console.log('RevenueCat not configured — view-only mode');
  }

  // ── Attribution ────────────────────────────────────────────────────────────
  const conversions = attributeConversions(posts, transactions);

  // ── Update hook performance ────────────────────────────────────────────────
  updateHookPerformance(posts, conversions, config);

  // ── Generate report ────────────────────────────────────────────────────────
  const report = generateReport(posts, conversions, rcMetrics, config);

  const reportDir = 'tiktok-marketing/reports';
  fs.mkdirSync(reportDir, { recursive: true });
  const reportDate = new Date().toISOString().slice(0, 10);
  const reportPath = path.join(reportDir, `${reportDate}.md`);
  fs.writeFileSync(reportPath, report);

  console.log(`\nReport saved to: ${reportPath}`);
  console.log('\n' + '═'.repeat(60));
  console.log(report);
  console.log('═'.repeat(60) + '\n');
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
