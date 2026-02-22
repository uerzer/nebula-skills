# Larry Skill

> Automate your entire TikTok slideshow marketing pipeline: generate → overlay → post → track → iterate.

Recreated from [clawhub.ai/OllieWazza/larry](https://clawhub.ai/OllieWazza/larry) by Oliver Henry (@oliverhenry on X).

**Proven results:** 7M views on the viral X article · 1M+ TikTok views · $670/month MRR — all from an AI agent on an old gaming PC.

---

## TL;DR

Oliver Henry built an AI agent called Larry that:
1. **Generates** 6-slide TikTok carousels using OpenAI image generation
2. **Overlays** text (hooks, reactions, CTAs) using node-canvas
3. **Posts** to TikTok as drafts via Postiz API — you add trending music manually in 60 seconds
4. **Tracks** per-post analytics via Postiz and attributed revenue via RevenueCat
5. **Self-improves** daily — the agent logs what works, writes new rules, and evolves its own skill files

The key insight: slideshows get **2.9x more comments** and **2.6x more shares** than video. They're also trivially easy for AI to generate consistently. Lock the scene architecture, only change the style between slides.

It generated $670/month MRR with zero daily involvement beyond adding music to drafts.

---

## File Structure

```
larry-skill/
├── SKILL.md                          # Full agent instructions (install this into your AI agent)
├── README.md                         # This file
├── scripts/
│   ├── onboarding.js                 # Config validation + workspace setup
│   ├── generate-slides.js            # Generate 6 portrait images (OpenAI/Stability/Replicate/local)
│   ├── add-text-overlay.js           # Add text overlays using node-canvas (Larry's exact implementation)
│   ├── post-to-tiktok.js             # Upload + post as draft via Postiz API
│   ├── check-analytics.js            # Connect posts to TikTok video IDs + fetch analytics
│   ├── competitor-research.js        # Research competitor TikTok accounts
│   └── daily-report.js               # Intelligence core — daily cron, diagnostics, hook recommendations
└── references/
    ├── slide-structure.md            # The 6-slide formula + hook formulas
    ├── analytics-loop.md             # Postiz API reference + attribution logic
    ├── app-categories.md             # Category-specific prompts (home, beauty, fitness, productivity)
    ├── competitor-research.md        # How to research your niche
    └── revenuecat-integration.md     # RevenueCat API reference + conversion attribution
```

---

## Quick Start

### Prerequisites
- Node.js v18+
- OpenAI API key (for `gpt-image-1.5` image generation)
- [Postiz](https://postiz.pro/oliverhenry) account with TikTok connected
- A TikTok account warmed up in your niche (7-14 days of normal usage before posting)
- (Optional) RevenueCat for conversion tracking

### Setup

```bash
# 1. Init workspace
node scripts/onboarding.js --init

# 2. Fill in tiktok-marketing/config.json with your keys
# (your agent walks you through this conversationally)

# 3. Install node-canvas for text overlays
npm install canvas
# macOS: brew install pkg-config cairo pango libpng jpeg giflib librsvg && npm install canvas
# Ubuntu: sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev && npm install canvas

# 4. Validate config + test API connections
node scripts/onboarding.js --validate --config tiktok-marketing/config.json
```

### Daily Workflow

**Your agent's job (15-30 min of compute):**
```bash
# Generate 6 slides
node scripts/generate-slides.js \
  --config tiktok-marketing/config.json \
  --output tiktok-marketing/posts/2026-02-16-0730/ \
  --prompts prompts.json

# Add text overlays
node scripts/add-text-overlay.js \
  --dir tiktok-marketing/posts/2026-02-16-0730/ \
  --texts texts.json

# Post to TikTok as draft
node scripts/post-to-tiktok.js \
  --config tiktok-marketing/config.json \
  --dir tiktok-marketing/posts/2026-02-16-0730/ \
  --caption "I showed my landlord what AI thinks our kitchen should look like..." \
  --title "Kitchen AI Transformation"
```

**Your job (60 seconds):**
1. Open TikTok → Drafts
2. Add trending sound
3. Hit Publish

### Daily Analytics (runs automatically via cron)
```bash
node scripts/daily-report.js --config tiktok-marketing/config.json --days 3
```

---

## The 6-Slide Structure

| Slide | Purpose | Text |
|-------|---------|------|
| 1 | Hook | Full hook visible — never split across slides |
| 2 | Problem | Relatability — set up the pain point |
| 3 | Discovery | "So I tried..." / "Then I found..." |
| 4 | Transform 1 | First result / early wow moment |
| 5 | Transform 2 | Bigger reaction / deeper proof |
| 6 | CTA | App name + clear next step |

**The rule:** Lock the architecture (same scene, same layout), only change the style between slides.

---

## Image Specs

- **Dimensions:** 1024x1536 (portrait — always)
- **Model:** `gpt-image-1.5` (NEVER `gpt-image-1` — massive quality difference)
- **Prompt:** "iPhone photo of [scene], realistic lighting, natural colors, taken on iPhone 15 Pro. No text, no watermarks."
- **Cost:** ~$0.50/slideshow real-time, ~$0.25 with Batch API

---

## Text Overlay Specs

- **Font size:** 6.5% of image width (dynamic: short text = bigger, long text = smaller)
- **Position:** Centered at 28% from top
- **Style:** White fill + black outline (15% of font size)
- **Safe zones:** Avoid top 10% (status bar) and bottom 20% (TikTok UI)
- **Line breaks:** Use `\n` manually, 4-6 words per line
- **Rule:** REACTIONS not labels — "Wait... this is nice??" not "Modern minimalist"

---

## Diagnostic Framework

| Views | Conversions | Action |
|-------|-------------|--------|
| High | High | 🟢 Make 3 variations immediately |
| High | Low | 🟡 Hook works — rotate the CTA |
| Low | High | 🟡 CTA works — test stronger hooks |
| Low | Low | 🔴 Full reset — new format/angle |
| High downloads, low paid | 🔴 App issue — fix onboarding/paywall |

---

## Hook Formulas (Proven)

**Highest engagement — Person + Conflict + AI:**
- "I showed my landlord what AI thinks our kitchen should look like"
- "My boyfriend said our flat looks like a catalogue — challenge accepted"

**POV format:**
- "POV: AI just redesigned my flat and now I need to move"

**Surprise/disbelief:**
- "Wait... is this the same room??"

**Key rule:** Always include another person and their reaction. Relatability = shareability.

---

## Expected Results

- **Week 1:** 200-5K views/post (learning phase)
- **Week 2-3:** 10K-50K views on good posts
- **Month 2+:** Consistent 50K-100K+, downloads converting to revenue

First posts will underperform. That's normal. The system needs time to learn your niche.

---

## Credits

Original skill by [Oliver Henry](https://x.com/oliverhenry) and his AI agent Larry.
Free on [ClawHub](https://clawhub.ai/OllieWazza/larry).
Runs on [OpenClaw](https://openclaw.ai).
Posting via [Postiz](https://postiz.pro/oliverhenry).
Revenue tracking via [RevenueCat](https://revenuecat.com).
