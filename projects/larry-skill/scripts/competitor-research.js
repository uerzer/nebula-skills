#!/usr/bin/env node
/**
 * competitor-research.js
 * Scaffolds the competitor research JSON file and validates its structure.
 * The actual research is done by the agent via browser — this script
 * handles the data structure and saves findings.
 *
 * Usage:
 *   node scripts/competitor-research.js --init   # Create blank research template
 *   node scripts/competitor-research.js --show   # Display current research findings
 *   node scripts/competitor-research.js --summary # Print niche insights summary
 */

'use strict';

const fs = require('fs');
const path = require('path');

const RESEARCH_PATH = 'tiktok-marketing/competitor-research.json';

// ─── CLI args ─────────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      result[args[i].slice(2)] = args[i + 1] !== undefined && !args[i + 1].startsWith('--') ? args[i + 1] : true;
      if (args[i + 1] && !args[i + 1].startsWith('--')) i++;
    }
  }
  return result;
}

// ─── Template ─────────────────────────────────────────────────────────────────

const BLANK_TEMPLATE = {
  researchDate: new Date().toISOString().slice(0, 10),
  niche: '',
  competitors: [
    {
      name: 'CompetitorApp',
      tiktokHandle: '@competitor',
      appStoreUrl: '',
      followers: 0,
      avgViews: 0,
      bestPost: {
        views: 0,
        hook: '',
        format: 'before-after slideshow',
        cta: 'link in bio',
      },
      topHooks: [],
      formats: [],
      postingFrequency: '',
      bestPostingTimes: [],
      strengths: '',
      weaknesses: '',
      appStoreRating: 0,
      topPositiveReviews: [],
      topNegativeReviews: [],
    },
  ],
  nicheInsights: {
    trendingSounds: [],
    commonFormats: [],
    winningHookPatterns: [],
    gapOpportunities: '',
    avoidPatterns: [],
    optimalPostingTimes: ['07:30', '16:30', '21:00'],
    audienceInsights: '',
  },
  ourStrategy: {
    differentiator: '',
    firstWeekHooks: [],
    formatChoice: '6-slide before-after with locked architecture',
    ctaStrategy: 'Start with "Download [App] — link in bio", test "Search on App Store" in week 2',
  },
};

// ─── Display helpers ──────────────────────────────────────────────────────────

function printSummary(data) {
  console.log('\n' + '═'.repeat(60));
  console.log(`COMPETITOR RESEARCH — ${data.niche || 'Niche not set'}`);
  console.log(`Researched: ${data.researchDate}`);
  console.log('═'.repeat(60));

  console.log(`\nCompetitors analysed: ${data.competitors.length}`);
  for (const c of data.competitors) {
    console.log(`\n  ${c.name} (${c.tiktokHandle})`);
    console.log(`    Followers: ${(c.followers || 0).toLocaleString()}`);
    console.log(`    Avg views: ${(c.avgViews || 0).toLocaleString()}`);
    console.log(`    Best post: ${(c.bestPost?.views || 0).toLocaleString()} views`);
    if (c.bestPost?.hook) console.log(`    Best hook: "${c.bestPost.hook}"`);
    console.log(`    Strengths: ${c.strengths || 'not analysed'}`);
    console.log(`    Weaknesses: ${c.weaknesses || 'not analysed'}`);
  }

  console.log('\nNiche Insights:');
  console.log(`  Gap: ${data.nicheInsights?.gapOpportunities || 'not identified'}`);
  console.log(`  Winning hooks: ${(data.nicheInsights?.winningHookPatterns || []).join(', ') || 'not identified'}`);
  console.log(`  Avoid: ${(data.nicheInsights?.avoidPatterns || []).join(', ') || 'none noted'}`);

  console.log('\nOur Strategy:');
  console.log(`  Differentiator: ${data.ourStrategy?.differentiator || 'not set'}`);
  console.log(`  Week 1 hooks:`);
  for (const h of (data.ourStrategy?.firstWeekHooks || [])) {
    console.log(`    - "${h}"`);
  }
  console.log('═'.repeat(60) + '\n');
}

// ─── Validate ─────────────────────────────────────────────────────────────────

function validateResearch(data) {
  const issues = [];
  if (!data.niche)                                      issues.push('niche not set');
  if (!data.competitors?.length)                        issues.push('no competitors added');
  if (!data.nicheInsights?.gapOpportunities)            issues.push('gap opportunities not identified');
  if (!data.ourStrategy?.firstWeekHooks?.length)        issues.push('first week hooks not planned');
  if (!data.ourStrategy?.differentiator)                issues.push('differentiator not set');

  for (const c of (data.competitors || [])) {
    if (c.name === 'CompetitorApp')                     issues.push('replace placeholder competitor with real data');
    if (!c.topHooks?.length)                            issues.push(`${c.name}: topHooks not filled in`);
  }

  return issues;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs();

  fs.mkdirSync('tiktok-marketing', { recursive: true });

  // ── Init: create blank template ───────────────────────────────────────────
  if (args.init) {
    if (fs.existsSync(RESEARCH_PATH)) {
      console.log(`Research file already exists at ${RESEARCH_PATH}`);
      console.log('Use --show to view current findings or edit the file directly.');
      return;
    }
    fs.writeFileSync(RESEARCH_PATH, JSON.stringify(BLANK_TEMPLATE, null, 2));
    console.log(`\nBlank research template created at ${RESEARCH_PATH}`);
    console.log('\nThe agent will fill this in during the research phase.');
    console.log('You can also edit it directly — the structure is self-documenting.\n');
    return;
  }

  // ── Show: display raw JSON ────────────────────────────────────────────────
  if (args.show) {
    if (!fs.existsSync(RESEARCH_PATH)) {
      console.error(`No research file found at ${RESEARCH_PATH}. Run --init first.`);
      process.exit(1);
    }
    const data = JSON.parse(fs.readFileSync(RESEARCH_PATH, 'utf8'));
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  // ── Summary: human-readable overview ─────────────────────────────────────
  if (args.summary) {
    if (!fs.existsSync(RESEARCH_PATH)) {
      console.error(`No research file found at ${RESEARCH_PATH}. Run --init first.`);
      process.exit(1);
    }
    const data = JSON.parse(fs.readFileSync(RESEARCH_PATH, 'utf8'));
    printSummary(data);

    const issues = validateResearch(data);
    if (issues.length > 0) {
      console.log('⚠️  Research gaps to fill:');
      for (const issue of issues) console.log(`  - ${issue}`);
      console.log('');
    } else {
      console.log('✓ Research complete. Ready to build content strategy.\n');
    }
    return;
  }

  // ── Default: usage ────────────────────────────────────────────────────────
  console.log(`
Competitor Research Helper

Usage:
  node scripts/competitor-research.js --init     Create blank research template
  node scripts/competitor-research.js --show     Print raw JSON
  node scripts/competitor-research.js --summary  Human-readable summary + validation

The agent does the actual research via browser and fills in the JSON.
Run --summary to see what's been found and what gaps remain.
  `);
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
