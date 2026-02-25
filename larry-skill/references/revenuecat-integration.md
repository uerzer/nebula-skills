# RevenueCat Integration

This reference covers the RevenueCat API endpoints used by the daily report for conversion attribution.

## Why This Matters

Without RevenueCat: you optimise for views (vanity metrics).
With RevenueCat: you optimise for revenue (actual paying users).

The difference: a post with 200K views and zero conversions is worthless. A post with 5K views and 10 paid subscribers is gold. You can only tell the difference with RevenueCat connected.

---

## Setup

### 1. Install the RevenueCat Skill

```bash
clawhub install revenuecat
```

### 2. Get Your V2 Secret Key

RevenueCat Dashboard → Project Settings → API Keys → Create a new V2 secret key (starts with `sk_`)

⚠️ This is a SECRET key. Never commit to public repos.

### 3. Set Environment Variable

```bash
export RC_API_KEY=sk_your_key_here
```

Or store in `tiktok-marketing/config.json` under `revenuecat.v2SecretKey`.

### 4. Verify Connection

```bash
curl -H "Authorization: Bearer $RC_API_KEY" \
  https://api.revenuecat.com/v2/projects
```

Should return your project list.

---

## API Endpoints Used

Base URL: `https://api.revenuecat.com/v2`
Auth: `Authorization: Bearer YOUR_V2_SECRET_KEY`

### Metrics Overview

```
GET /projects/{projectId}/metrics/overview
```

Returns top-level business metrics. Pulled daily.

**Key fields:**
```json
{
  "mrr": { "value": 670.00, "unit": "USD" },
  "active_subscriptions": { "value": 42 },
  "active_trials": { "value": 8 },
  "churn_rate": { "value": 0.034 },
  "trial_conversion_rate": { "value": 0.41 }
}
```

### Transactions (Conversion Attribution)

```
GET /projects/{projectId}/transactions?start_time=2026-02-13T00:00:00Z&end_time=2026-02-16T00:00:00Z
```

Returns individual purchase events with timestamps. Used to attribute conversions to specific TikTok posts.

**Key fields:**
```json
{
  "items": [
    {
      "id": "txn_abc123",
      "customer_id": "user_xyz",
      "product_id": "weekly_sub",
      "price": { "amount": 4.99, "currency": "USD" },
      "purchased_at": "2026-02-15T14:23:00Z",
      "type": "INITIAL_PURCHASE"
    }
  ]
}
```

### Attribution Logic

Cross-reference transaction timestamps with post publish times:

```javascript
// Attribution window: 24-72 hours after post publish
function getAttributedConversions(post, transactions) {
  const publishTime = new Date(post.publishDate).getTime();
  const windowStart = publishTime + (24 * 60 * 60 * 1000); // 24h after post
  const windowEnd = publishTime + (72 * 60 * 60 * 1000);   // 72h after post

  return transactions.filter(txn => {
    const txnTime = new Date(txn.purchased_at).getTime();
    return txnTime >= windowStart && txnTime <= windowEnd;
  });
}
```

Why 24-72h window? TikTok posts typically peak at 24-48h. Most conversions driven by a post happen within 72h of publish.

---

## What the Daily Report Does With This Data

### MRR Tracking
- Pulls current MRR vs yesterday
- Flags if MRR drops even when views are up (app issue signal)

### Trial-to-Paid Conversion Rate
- If trial conversion rate drops below baseline, flags potential paywall/onboarding issue
- Recommends pausing posting and fixing app experience

### Per-Post Attribution
- For each post in the last 3 days, counts transactions in the 24-72h window
- Tags each post with attributed conversions in `hook-performance.json`

### Business-Level Signals

| Signal | What It Means | Recommended Action |
|--------|--------------|-------------------|
| Views up, MRR flat | Content not converting | Check CTAs, check App Store page |
| Views up, trials up, paid flat | Trial experience broken | Fix onboarding, paywall timing |
| Views flat, MRR up | Efficient audience | Keep current hooks, scale slowly |
| Views up, installs up, trials flat | App store page broken | Fix screenshots, description |
| Churn rate rising | Value not delivered | Product issue — pause marketing |

---

## Snapshots

The daily report saves RC data to `tiktok-marketing/rc-snapshot.json`:

```json
{
  "date": "2026-02-16",
  "mrr": 670.00,
  "activeSubscriptions": 42,
  "activeTrials": 8,
  "churnRate": 0.034,
  "trialConversionRate": 0.41,
  "newTransactions": [
    {
      "id": "txn_abc123",
      "purchasedAt": "2026-02-15T14:23:00Z",
      "amount": 4.99,
      "attributedPostId": "postiz-post-id-xyz"
    }
  ]
}
```

---

## Without RevenueCat

If RevenueCat isn't connected, the feedback loop still works — but only on Postiz view data:
- Can still identify which hooks get views
- Cannot distinguish views-only posts from revenue-driving posts
- Daily report runs view-only diagnostics (no conversion quadrant)

This is fine for early-stage validation. Once you're getting consistent views, connecting RevenueCat is the single highest-leverage thing you can do.
