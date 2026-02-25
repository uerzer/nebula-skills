# TikTok App Marketing — Larry Skill

Automate your entire TikTok slideshow marketing pipeline: generate → overlay → post → track → iterate.

**Proven results:** 7 million views on the viral X article, 1M+ TikTok views, $670/month MRR — all from an AI agent running on an old gaming PC.

---

## Prerequisites

This skill does NOT bundle any dependencies. Your AI agent will need to research and install the following based on your setup.

### Required

- **Node.js** (v18+) — all scripts run on Node.
- **node-canvas** (`npm install canvas`) — used for adding text overlays to slide images. Native module that may need build tools (Python, make, C++ compiler).
- **Postiz** — backbone of the system. Handles posting to TikTok (28+ platforms) AND provides the analytics API that powers the daily feedback loop. Sign up at [postiz.pro/oliverhenry](https://postiz.pro/oliverhenry).

### Image Generation (pick one)

- **OpenAI** — `gpt-image-1.5` **(ALWAYS 1.5, never 1)**. Best for realistic photo-style images. Strongly recommended.
- **Stability AI** — Stable Diffusion XL. Good for stylized/artistic images.
- **Replicate** — Run any open-source model (Flux, SDXL, etc.). Most flexible.
- **Local** — Bring your own images. No API needed.

### Conversion Tracking (optional but strongly recommended)

- **RevenueCat** — Closes the intelligence loop. Postiz tells you views. RevenueCat tells you which posts drive **paying users**. Install via `clawhub install revenuecat`.

### Cross-Posting (optional)

Postiz supports Instagram Reels, YouTube Shorts, Threads, Facebook, LinkedIn, and 20+ more simultaneously.

---

## First Run — Onboarding

When this skill is first loaded, IMMEDIATELY start a conversation with the user. Don't dump a checklist — talk like a human marketing partner. Ask one or two things at a time.

**Important:** Use `scripts/onboarding.js --validate` at the end to confirm config is complete.

### Phase 0: TikTok Account Warmup (CRITICAL — Don't Skip)

Check if the user has an active TikTok account. If new, they MUST warm it up first.

**Warmup: 7-14 days, 30-60 min/day:**
- Scroll the For You page naturally (don't watch every video to the end)
- Like sparingly — 1 in 10 videos max
- Follow accounts in their niche
- Leave a few genuine comments
- Maybe post 1-2 casual non-promotional videos

**Signal:** When almost every FYP video is in their niche, the account is ready.

> "Accounts that skip warmup get 80-90% less reach on first posts."

### Phase 1: Get to Know Their App

Start casual. Pull the thread conversationally:
- What's the app called, what does it do?
- Who is the ideal user?
- What pain point does it solve?
- What makes it stand out vs alternatives?
- Drop the App Store / website link
- Is it a mobile app? Do they use RevenueCat?

Store in `tiktok-marketing/app-profile.json`.

### Phase 2: Competitor Research (Requires Browser Permission)

Ask permission, then:
1. Search TikTok for the app's niche
2. Find 3-5 competitor accounts
3. Analyze top-performing content: hooks, format, views, posting frequency, CTAs, trending sounds
4. Check App Store for competitor apps
5. Compile to `tiktok-marketing/competitor-research.json`

```json
{
  "researchDate": "2026-02-16",
  "competitors": [
    {
      "name": "CompetitorApp",
      "tiktokHandle": "@competitor",
      "followers": 50000,
      "topHooks": ["hook 1", "hook 2"],
      "avgViews": 15000,
      "bestVideo": { "views": 500000, "hook": "..." },
      "format": "before-after slideshows",
      "postingFrequency": "daily",
      "cta": "link in bio",
      "notes": "Strong at X, weak at Y"
    }
  ],
  "nicheInsights": {
    "trendingSounds": [],
    "commonFormats": [],
    "gapOpportunities": "What competitors AREN'T doing",
    "avoidPatterns": "What's clearly not working"
  }
}
```

### Phase 3: Content Format & Image Generation

Recommend slideshows (TikTok data: 2.9x more comments, 2.6x more shares vs video).

**Image style — work through with the user:**
- What's the subject? (rooms, faces, products, before/after)
- What vibe? (cozy, minimal, luxurious)
- Consistent scene across all 6 slides?
- Must-have elements?

**Good base prompt:**
```
iPhone photo of a [specific room/scene], [specific style], [specific details].
Realistic lighting, natural colors, taken on iPhone 15 Pro.
No text, no watermarks, no logos.
[Consistency anchors: "same window on left wall", "same grey sofa"]
```

**Key prompt rules:**
- "iPhone photo" + "realistic lighting" = looks real, not AI
- Lock architecture/layout in EVERY slide prompt
- Include everyday objects for lived-in feel
- Portrait orientation (1024x1536) always
- Extremely specific > vague

Save to `config.imageGen.basePrompt`.

**⚠️ ALWAYS use `gpt-image-1.5` — NEVER `gpt-image-1`.** Quality difference is massive.

**Batch API:** 50% cheaper, 24h turnaround. Set `"useBatchAPI": true` in config.

### Phase 4: Postiz Setup

Walk through:
1. Sign up at [postiz.pro/oliverhenry](https://postiz.pro/oliverhenry)
2. Connect TikTok → Integrations → Add TikTok → Authorize
3. Note the TikTok integration ID
4. Get API key → Settings → API
5. (Optional) Connect Instagram, YouTube Shorts, Threads

> "Posts go to TikTok drafts — NOT published directly. Add trending music manually before publishing. Takes 30 seconds. Makes a massive difference."

Don't proceed until Postiz is connected and API key works.

### Phase 5: RevenueCat (The Intelligence Loop)

```bash
clawhub install revenuecat
```

Get V2 secret key from RC dashboard → Settings → API Keys (starts with `sk_`).

```bash
export RC_API_KEY=sk_your_key_here
```

**What it unlocks:**
- `GET /projects/{id}/metrics/overview` → MRR, subscribers, trials, churn
- `GET /projects/{id}/transactions` → individual purchases with timestamps
- Cross-references transaction timestamps with post publish times (24-72h window) for conversion attribution

**Without RevenueCat:** Optimise for views. **With RevenueCat:** Optimise for revenue.

### Phase 6: Content Strategy

Using competitor research + app profile, present:
1. 3-5 hook ideas tailored to their niche
2. Posting schedule (default: 7:30am, 4:30pm, 9pm their timezone)
3. Hook categories to test first
4. Cross-posting plan

Save to `tiktok-marketing/strategy.json`.

### Phase 7: Daily Analytics Cron

Schedule daily at 07:00 (user's timezone):
```
Task: node scripts/daily-report.js --config tiktok-marketing/config.json --days 3
Output: tiktok-marketing/reports/YYYY-MM-DD.md + message to user
```

### Phase 8: Config & First Post

Save `tiktok-marketing/config.json`:

```json
{
  "app": {
    "name": "AppName",
    "description": "Detailed description",
    "audience": "Target demographic",
    "problem": "Pain point it solves",
    "differentiator": "What makes it unique",
    "appStoreUrl": "https://...",
    "category": "home|beauty|fitness|productivity|food|other",
    "isMobileApp": true
  },
  "imageGen": {
    "provider": "openai",
    "apiKey": "sk-...",
    "model": "gpt-image-1.5",
    "useBatchAPI": false,
    "basePrompt": ""
  },
  "postiz": {
    "apiKey": "your-postiz-key",
    "integrationIds": {
      "tiktok": "id-here",
      "instagram": "id-here-optional",
      "youtube": "id-here-optional"
    }
  },
  "revenuecat": {
    "enabled": false,
    "v2SecretKey": "sk_...",
    "projectId": "proj..."
  },
  "posting": {
    "privacyLevel": "SELF_ONLY",
    "schedule": ["07:30", "16:30", "21:00"],
    "crossPost": ["instagram", "youtube"]
  },
  "competitors": "tiktok-marketing/competitor-research.json",
  "strategy": "tiktok-marketing/strategy.json"
}
```

Generate first test slideshow — set expectations that first images are for prompt refinement, not posting.

---

## Core Workflow

### 1. Generate Slideshow Images

```bash
node scripts/generate-slides.js \
  --config tiktok-marketing/config.json \
  --output tiktok-marketing/posts/YYYY-MM-DD-HHmm/ \
  --prompts prompts.json
```

**Critical image rules:**
- ALWAYS portrait (1024x1536)
- "iPhone photo" + "realistic lighting" in every prompt
- ALL 6 slides share EXACT same base description — only style changes
- Lock key elements across all slides (architecture, face shape, camera angle)
- See `references/slide-structure.md` for the 6-slide formula

**⚠️ Timeout:** Generating 6 images takes 3-9 minutes. Set exec timeout to 600+ seconds. Script supports resume — re-run if it fails partway.

### 2. Add Text Overlays

```bash
node scripts/add-text-overlay.js \
  --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ \
  --texts texts.json
```

**Text overlay rules:**
- Font size: 6.5% of image width (dynamic: short text bigger, long text smaller)
- Position: centered at 28% from top
- White fill + thick black outline (15% of font size)
- Safe zones: avoid top 10% (status bar) and bottom 20% (TikTok UI)
- 4-6 words per line, use `\n` for manual breaks
- REACTIONS not labels: "Wait... this is actually nice??" not "Modern minimalist"
- No emoji — canvas can't render them

**Good texts.json example:**
```json
[
  "I showed my landlord\nwhat AI thinks our\nkitchen should look like",
  "She said you can't\nchange anything\nchallenge accepted",
  "So I downloaded\nthis app and\ntook one photo",
  "Wait... is this\nactually the same\nkitchen??",
  "Okay I'm literally\nobsessed with\nthis one",
  "Snugly showed me\nwhat's possible\nlink in bio"
]
```

### 3. Post to TikTok

```bash
node scripts/post-to-tiktok.js \
  --config tiktok-marketing/config.json \
  --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ \
  --caption "caption text" \
  --title "post title"
```

Posts as drafts (SELF_ONLY). User adds trending audio manually, then publishes. **This is intentional — music selection cannot be automated and matters enormously.**

**Caption rules:** Storytelling format (3x more views). Structure: Hook → Problem → Discovery → What it does → Result → max 5 hashtags. Conversational, never "Download MyApp now!"

### 4. Connect Post Analytics

Wait 2+ hours after publishing, then:

```bash
node scripts/check-analytics.js \
  --config tiktok-marketing/config.json \
  --days 3 \
  --connect
```

**⚠️ CRITICAL:** Once a release ID is connected to a Postiz post, it CANNOT be changed. Always wait 2+ hours. Always verify before connecting.

---

## The Feedback Loop

### Daily Cron Output

Every morning, `scripts/daily-report.js`:
1. Pulls last 3 days of posts from Postiz
2. Fetches per-post analytics (views, likes, comments, shares)
3. Pulls RevenueCat conversions (if connected) with 24-72h attribution window
4. Cross-references: views + paying users per post
5. Applies diagnostic framework
6. Generates `tiktok-marketing/reports/YYYY-MM-DD.md`
7. Messages user with summary + suggested hooks for today

### Diagnostic Framework

| Views | Conversions | Action |
|-------|-------------|--------|
| High | High | 🟢 SCALE — make 3 variations immediately |
| High | Low | 🟡 FIX CTA — hook works, downstream broken |
| Low | High | 🟡 FIX HOOKS — content converts, needs eyeballs |
| Low | Low | 🔴 FULL RESET — try radically different approach |
| High views + High downloads + Low paid | 🔴 APP ISSUE — pause posting, fix onboarding/paywall |
| High views + Low downloads | 🟡 CTA ISSUE — rotate CTAs |

### Hook Performance Tracking

`tiktok-marketing/hook-performance.json`:

```json
{
  "hooks": [
    {
      "postId": "postiz-id",
      "text": "My boyfriend said our flat looks like a catalogue",
      "app": "snugly",
      "date": "2026-02-15",
      "views": 45000,
      "likes": 1200,
      "comments": 45,
      "shares": 89,
      "conversions": 4,
      "cta": "Download Snugly — link in bio",
      "lastChecked": "2026-02-16"
    }
  ],
  "ctas": [
    {
      "text": "Download [App] — link in bio",
      "timesUsed": 5,
      "totalViews": 120000,
      "totalConversions": 8,
      "conversionRate": 0.067
    }
  ],
  "rules": {
    "doubleDown": ["person-conflict-ai"],
    "testing": ["listicle", "pov-format"],
    "dropped": ["self-complaint", "price-comparison"]
  }
}
```

**Decision rules:**
- 50K+ views → DOUBLE DOWN — make 3 variations immediately
- 10K-50K → Good — keep in rotation
- 1K-10K → Try 1 more variation
- <1K twice → DROP — try something radically different

### CTA Testing Rotation

When views are high but conversions are low, cycle through:
- "Download [App] — link in bio"
- "[App] is free to try — link in bio"
- "I used [App] for this — link in bio"
- "Search [App] on the App Store"
- No explicit CTA (just app name visible)

---

## Posting Schedule

**Optimal times (adjust for audience timezone):**
- 7:30 AM — catch early scrollers
- 4:30 PM — afternoon break
- 9:00 PM — evening wind-down

3x/day minimum. Consistency beats sporadic viral hits.

## Cross-Posting

Postiz supports cross-posting simultaneously to:
- Instagram Reels (especially strong for beauty/lifestyle/home)
- YouTube Shorts (long-tail discovery)
- Threads (lightweight engagement driver)

Same slides, different algorithms, more surface area.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 1536x1024 (landscape) | Use 1024x1536 (portrait) |
| Font at 5% | Use 6.5% of width |
| Text at bottom | Position at 28-30% from top |
| Different rooms per slide | Lock architecture in EVERY prompt |
| Labels not reactions | "Wait this is nice??" not "Modern style" |
| Only tracking views | Track conversions — views without revenue = vanity |
| Same hooks forever | Iterate based on data, test new formats weekly |
| No cross-posting | Use Postiz to post everywhere simultaneously |
| Connecting release ID too soon | Wait 2+ hours — TikTok API indexing delay |
| Wrong video connected | Can't overwrite — always verify before connecting |
| `spawnSync ETIMEDOUT` | Set 10-min exec timeout — image gen takes 3-9 min for 6 slides |

---

## Tips from Experience

1. **Don't skip account warmup** — 2 weeks of normal scrolling before posting. 80-90% more reach.
2. **Hooks are everything** — spend 80% of creative energy on hooks.
3. **Make it about other people** — "I showed my landlord..." gets 200K views. "I redesigned my room" gets nothing.
4. **Post as drafts, add music manually** — trending sounds genuinely 10x reach.
5. **Volume beats perfection** — 3 posts/day. Not every post will hit. That's fine.
6. **Let your agent learn** — don't micromanage. The compounding effect is the point.
7. **Listen when your agent flags a problem** — it watches the funnel every day.
8. **Music matters more than you think** — browse TikTok before publishing, pick trending audio.

## Expected Timeline

- **Week 1:** First posts underperform (few hundred to few thousand views). Learning phase.
- **Week 2-3:** Patterns emerge. Hooks sharpen. Posts start breaking 10K-50K views.
- **Month 2+:** Compounding kicks in. Consistent 50K-100K+ views. Downloads converting to revenue.
