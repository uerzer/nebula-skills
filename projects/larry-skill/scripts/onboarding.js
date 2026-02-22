#!/usr/bin/env node
/**
 * onboarding.js
 * Config validation and setup helper.
 * Run with --validate to check your config is complete before first post.
 *
 * Usage:
 *   node scripts/onboarding.js --validate --config tiktok-marketing/config.json
 *   node scripts/onboarding.js --init --config tiktok-marketing/config.json
 *
 * The agent runs this conversationally — this script handles the
 * mechanical parts (validation, directory setup, config writing).
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const https = require('https');

// ─── CLI args ─────────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--validate') result.validate = true;
    else if (args[i] === '--init')     result.init = true;
    else if (args[i].startsWith('--')) { result[args[i].slice(2)] = args[i + 1]; i++; }
  }
  return result;
}

// ─── Default config template ──────────────────────────────────────────────────

const DEFAULT_CONFIG = {
  app: {
    name: '',
    description: '',
    audience: '',
    problem: '',
    differentiator: '',
    appStoreUrl: '',
    category: 'other',
    isMobileApp: true,
  },
  imageGen: {
    provider: 'openai',
    apiKey: '',
    model: 'gpt-image-1.5',
    useBatchAPI: false,
    basePrompt: '',
  },
  postiz: {
    apiKey: '',
    integrationIds: {
      tiktok: '',
      instagram: '',
      youtube: '',
    },
  },
  revenuecat: {
    enabled: false,
    v2SecretKey: '',
    projectId: '',
  },
  posting: {
    privacyLevel: 'SELF_ONLY',
    schedule: ['07:30', '16:30', '21:00'],
    crossPost: [],
  },
  competitors: 'tiktok-marketing/competitor-research.json',
  strategy: 'tiktok-marketing/strategy.json',
};

// ─── Validation ───────────────────────────────────────────────────────────────

function validateConfig(config) {
  const errors = [];
  const warnings = [];

  // Required fields
  if (!config.app?.name)              errors.push('app.name is required');
  if (!config.app?.description)       errors.push('app.description is required');
  if (!config.app?.audience)          errors.push('app.audience is required');
  if (!config.imageGen?.provider)     errors.push('imageGen.provider is required');
  if (!config.imageGen?.apiKey && config.imageGen?.provider !== 'local')
                                      errors.push('imageGen.apiKey is required (unless using local images)');
  if (!config.postiz?.apiKey)         errors.push('postiz.apiKey is required');
  if (!config.postiz?.integrationIds?.tiktok)
                                      errors.push('postiz.integrationIds.tiktok is required');

  // Model check
  if (config.imageGen?.provider === 'openai' && config.imageGen?.model !== 'gpt-image-1.5') {
    errors.push(`imageGen.model must be "gpt-image-1.5" — got "${config.imageGen?.model}". Never use gpt-image-1.`);
  }

  // Warnings (not blocking)
  if (!config.app?.appStoreUrl)       warnings.push('app.appStoreUrl not set — add your App Store link for CTA tracking');
  if (!config.imageGen?.basePrompt)   warnings.push('imageGen.basePrompt not set — agent will prompt for style before first post');
  if (!config.revenuecat?.enabled)    warnings.push('revenuecat.enabled is false — you will only optimise for views, not revenue');
  if (config.posting?.crossPost?.length === 0)
                                      warnings.push('posting.crossPost is empty — consider adding instagram or youtube for more reach');

  return { errors, warnings };
}

// ─── API connectivity tests ───────────────────────────────────────────────────

function testPostiz(apiKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.postiz.com',
      path: '/posts?page=1&limit=1',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${apiKey}` },
    };
    const req = https.request(options, res => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(8000, () => { req.destroy(); resolve(false); });
    req.end();
  });
}

function testRevenueCat(apiKey, projectId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.revenuecat.com',
      path: `/v2/projects/${projectId}/metrics/overview`,
      method: 'GET',
      headers: { 'Authorization': `Bearer ${apiKey}` },
    };
    const req = https.request(options, res => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(8000, () => { req.destroy(); resolve(false); });
    req.end();
  });
}

// ─── Directory setup ──────────────────────────────────────────────────────────

function initDirectories() {
  const dirs = [
    'tiktok-marketing',
    'tiktok-marketing/posts',
    'tiktok-marketing/reports',
  ];
  for (const dir of dirs) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`  Created: ${dir}/`);
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs();
  const configPath = args.config || 'tiktok-marketing/config.json';

  // ── Init mode: create starter config and directories ─────────────────────
  if (args.init) {
    console.log('\nInitialising Larry skill workspace...\n');
    initDirectories();

    if (!fs.existsSync(configPath)) {
      fs.mkdirSync(path.dirname(configPath), { recursive: true });
      fs.writeFileSync(configPath, JSON.stringify(DEFAULT_CONFIG, null, 2));
      console.log(`\nStarter config created at: ${configPath}`);
      console.log('Fill in the values (your agent will walk you through this).');
    } else {
      console.log(`\nConfig already exists at: ${configPath}`);
    }

    console.log('\nNext: Tell your agent about your app and it will complete the config.\n');
    return;
  }

  // ── Validate mode: check config is complete ───────────────────────────────
  if (args.validate) {
    console.log(`\nValidating config: ${configPath}\n`);

    if (!fs.existsSync(configPath)) {
      console.error(`Config not found: ${configPath}`);
      console.error('Run: node scripts/onboarding.js --init');
      process.exit(1);
    }

    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { errors, warnings } = validateConfig(config);

    if (errors.length > 0) {
      console.error('ERRORS (must fix before posting):');
      for (const e of errors) console.error(`  ✗ ${e}`);
    }

    if (warnings.length > 0) {
      console.warn('\nWARNINGS (optional but recommended):');
      for (const w of warnings) console.warn(`  ⚠  ${w}`);
    }

    if (errors.length === 0) {
      console.log('Config structure: ✓ Valid\n');

      // Live connectivity tests
      console.log('Testing API connectivity...');

      const postizOk = await testPostiz(config.postiz.apiKey);
      console.log(`  Postiz API: ${postizOk ? '✓ Connected' : '✗ Failed — check your API key'}`);

      if (config.revenuecat?.enabled && config.revenuecat?.v2SecretKey) {
        const rcOk = await testRevenueCat(config.revenuecat.v2SecretKey, config.revenuecat.projectId);
        console.log(`  RevenueCat API: ${rcOk ? '✓ Connected' : '✗ Failed — check your V2 secret key and project ID'}`);
      }

      if (postizOk) {
        console.log('\n✓ All systems go. Ready to generate your first post.\n');
        console.log('Run: node scripts/generate-slides.js --config ' + configPath + ' --output tiktok-marketing/posts/test/ --prompts prompts.json');
      } else {
        console.error('\nFix Postiz connectivity before proceeding.');
        process.exit(1);
      }

    } else {
      console.error(`\n${errors.length} error(s) found. Fix these before your first post.`);
      process.exit(1);
    }

    return;
  }

  // ── Default: print usage ──────────────────────────────────────────────────
  console.log(`
Larry Skill — Onboarding Helper

Usage:
  node scripts/onboarding.js --init     [--config path]   Create starter config + directories
  node scripts/onboarding.js --validate [--config path]   Check config and test API connections

The agent handles the conversational onboarding. Run --init first,
then tell your agent about your app and it will fill in the config.
Run --validate when done to confirm everything is ready.
  `);
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
