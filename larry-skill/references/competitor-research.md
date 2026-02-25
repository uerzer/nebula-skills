# Competitor Research Guide

How to research your niche on TikTok before building content strategy.

## Why Research First

You need to know:
- What hooks are already working in your niche
- What formats competitors are using
- What gaps exist (what nobody is doing well)
- What to avoid (what's clearly not working)

Skipping this means guessing. Doing this means starting with a data-driven strategy.

---

## Research Process

### Step 1: TikTok Search

Search for your niche using multiple angles:
- The app category: "interior design app", "fitness app", "meal planning app"
- The pain point: "small flat makeover", "home workout", "what to cook tonight"
- The transformation: "room transformation", "body transformation", "productivity transformation"

### Step 2: Find Competitor Accounts

Look for accounts that:
- Post content similar to what you'll be creating
- Have at least 10K followers (enough data to analyse)
- Have been posting for 3+ months (enough history)
- Are in your specific niche (not just broadly related)

Find 3-5 accounts. More than 5 is diminishing returns at this stage.

### Step 3: Analyse Top Content

For each competitor account, look at their top 10 posts by views. For each:

**Hook analysis:**
- What's the first line of text or spoken word?
- Is it a question, a statement, a reaction, a challenge?
- Does it feature another person (conflict/social hook)?
- What emotion does it trigger? (curiosity, FOMO, relatability, surprise)

**Format analysis:**
- Slideshow vs video
- Number of slides
- Text overlay style (position, size, font)
- Before/after vs listicle vs POV vs tutorial

**Performance analysis:**
- Views on best post vs average post
- Like/view ratio (engagement rate — higher = more resonant content)
- Comment volume and sentiment
- Share count (shares = people finding it valuable enough to send)

**CTA analysis:**
- What CTA do they use on the last slide?
- "Link in bio", "Download [app]", app name only, or no explicit CTA?
- Which CTA correlates with their highest-converting posts?

### Step 4: App Store Research

Check competitor apps in your category:
- Star rating and review count
- What do 5-star reviews say? (what users love)
- What do 1-star reviews say? (pain points you can address in hooks)
- Screenshots — what features do they highlight?
- Description — what promises do they make?

### Step 5: Identify the Gap

The most valuable insight: **what are competitors NOT doing well?**

Common gaps:
- Nobody using conflict/social hooks (just product demos)
- Posting at wrong times for the audience
- Low-quality images (AI-obvious)
- Text overlays too small or positioned badly
- No cross-posting to Instagram/YouTube
- Same hook format every time (no variety)
- Ignoring the comments (engagement opportunity)

---

## Output Format

Save to `tiktok-marketing/competitor-research.json`:

```json
{
  "researchDate": "2026-02-16",
  "niche": "interior design apps",
  "competitors": [
    {
      "name": "CompetitorApp",
      "tiktokHandle": "@competitor",
      "appStoreUrl": "https://apps.apple.com/...",
      "followers": 52000,
      "avgViews": 18000,
      "bestPost": {
        "views": 680000,
        "hook": "I showed my landlord what AI thinks our flat should look like",
        "format": "before-after slideshow",
        "cta": "link in bio"
      },
      "topHooks": [
        "I showed my landlord...",
        "POV: AI redesigned my flat...",
        "My boyfriend said our flat..."
      ],
      "formats": ["before-after slideshow", "transformation slideshow"],
      "postingFrequency": "once daily",
      "bestPostingTimes": ["7am", "9pm"],
      "strengths": "Strong hooks, consistent scene across slides",
      "weaknesses": "CTA too pushy, no cross-posting, same hook style every time",
      "appStoreRating": 4.6,
      "topPositiveReviews": ["Easy to use", "Realistic results", "Love the before/after"],
      "topNegativeReviews": ["Too expensive", "Crashes on older phones", "Limited styles"]
    }
  ],
  "nicheInsights": {
    "trendingSounds": ["[sound name] — [trending reason]"],
    "commonFormats": ["before-after slideshow", "POV transformation"],
    "winningHookPatterns": ["person + conflict + AI", "POV format"],
    "gapOpportunities": "Nobody is using social conflict hooks. Everyone just shows the product. Huge opening.",
    "avoidPatterns": ["direct product demos", "price comparison", "feature lists"],
    "optimalPostingTimes": ["7:30am", "4:30pm", "9pm"],
    "audienceInsights": "Mostly renters aged 25-35, frustrated with landlord restrictions"
  },
  "ourStrategy": {
    "differentiator": "Lead with social conflict hooks — landlord/partner reactions",
    "firstWeekHooks": [
      "I showed my landlord what AI thinks our kitchen should look like",
      "My boyfriend said our flat looks like a catalogue — challenge accepted",
      "POV: AI just redesigned my rented flat and now I'm angry I can't do it for real"
    ],
    "formatChoice": "6-slide before-after with locked architecture",
    "ctaStrategy": "Start with 'Download [App] — link in bio', test 'Search on App Store' in week 2"
  }
}
```

---

## Reading Competitor Weakness Into Your Strategy

| Competitor Weakness | Your Opportunity |
|--------------------|-----------------|
| Generic product demo hooks | Use social conflict hooks (landlord, partner, parent) |
| Obvious AI images | Use gpt-image-1.5 at 1024x1536 for photorealistic results |
| Text too small / badly positioned | Use Larry's exact text overlay specs |
| Same hook format every time | Rotate hook categories weekly |
| No cross-posting | Post to Instagram + YouTube simultaneously via Postiz |
| Pushy CTAs | Conversational CTAs ("I used [App] for this — link in bio") |
| No engagement with comments | Reply to comments in first hour of posting |

---

## Refresh Schedule

Re-run competitor research:
- **Week 4:** Check if competitor strategies have changed
- **Month 3:** Full refresh — new competitors may have emerged, old ones may have pivoted
- **Any time a competitor suddenly spikes** — analyse what changed in their content
