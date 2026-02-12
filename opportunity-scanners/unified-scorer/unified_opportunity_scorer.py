"""
Unified Opportunity Scoring Dashboard
Ranks all revenue opportunities by potential + speed to $100K/month

Integrates insights from:
- Crypto arbitrage monitoring
- AI agency lead generation
- Viral trend detection
- Enterprise pricing intelligence
- Micro-SaaS validation
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

def transform(data: dict, context: dict) -> dict:
    """
    Scores and ranks all opportunities across multiple revenue streams.
    
    Input data structure:
    {
        "current_capital": 10000,           # Available capital
        "time_available": "full_time",      # "full_time", "part_time", "weekends"
        "risk_tolerance": "medium",         # "low", "medium", "high"
        "target_monthly": 100000            # Revenue goal
    }
    
    Returns ranked opportunities with actionable next steps.
    """
    
    # Extract configuration
    capital = data.get("current_capital", 10000)
    time = data.get("time_available", "full_time")
    risk = data.get("risk_tolerance", "medium")
    target = data.get("target_monthly", 100000)
    
    # Opportunity Scoring Framework
    scoring_criteria = {
        "revenue_potential": {
            "weight": 0.35,
            "scale": "0-100 based on realistic monthly revenue ceiling",
            "calculation": "Path to $100K/month feasibility"
        },
        "speed_to_first_dollar": {
            "weight": 0.25,
            "scale": "0-100 based on days to first revenue",
            "calculation": "Faster = higher score"
        },
        "capital_efficiency": {
            "weight": 0.15,
            "scale": "0-100 based on $ revenue per $ invested",
            "calculation": "ROI potential vs capital required"
        },
        "competitive_moat": {
            "weight": 0.10,
            "scale": "0-100 based on barriers to entry",
            "calculation": "How defensible is this advantage?"
        },
        "execution_complexity": {
            "weight": 0.10,
            "scale": "0-100 (inverted - simpler = higher score)",
            "calculation": "Skills required, team size, infrastructure"
        },
        "market_timing": {
            "weight": 0.05,
            "scale": "0-100 based on market readiness",
            "calculation": "Is this wave rising or fading?"
        }
    }
    
    # All Opportunities Analyzed
    all_opportunities = []
    
    # OPPORTUNITY 1: Crypto Arbitrage
    crypto_arb = {
        "name": "Crypto Arbitrage Trading",
        "category": "Trading",
        "description": "DEX-DEX, CEX-DEX, cross-chain arbitrage opportunities",
        "scores": {
            "revenue_potential": {
                "score": 40,
                "reasoning": "Requires $500K-1M capital for $100K/month at 10-20% monthly returns. With $10K capital, max ~$1K-3K/month.",
                "ceiling": "$1K-3K/month with current capital"
            },
            "speed_to_first_dollar": {
                "score": 85,
                "reasoning": "Can execute first trade within 48 hours if using ArbitrageScanner.io + existing exchange accounts",
                "timeline": "2-7 days"
            },
            "capital_efficiency": {
                "score": 60,
                "reasoning": "5-15% monthly ROI possible, but requires active capital at risk",
                "roi": "60-180% annual if skilled"
            },
            "competitive_moat": {
                "score": 20,
                "reasoning": "Highly competitive, 70% bot-driven, top searchers dominate",
                "barriers": "Very low - anyone can start"
            },
            "execution_complexity": {
                "score": 40,
                "reasoning": "Requires trading knowledge, bot development, risk management, 24/7 monitoring",
                "difficulty": "High"
            },
            "market_timing": {
                "score": 50,
                "reasoning": "Always opportunities, but increasing automation makes retail participation harder",
                "trend": "Neutral to declining for retail"
            }
        },
        "weighted_total_score": 52.5,
        "capital_required": "$5K-10K minimum for profitability",
        "time_to_100k_monthly": "24-36 months (requires scaling capital to $500K+)",
        "next_steps": [
            "1. Start ArbitrageScanner.io 1-day free trial",
            "2. Paper trade for 2 weeks to learn patterns",
            "3. Start with $5K-10K on BSC/Polygon (lower gas fees)",
            "4. Treat as supplemental income stream, not primary path to $100K"
        ],
        "verdict": "SUPPLEMENTAL STREAM - Good for 5-10% monthly returns on capital, but won't reach $100K/month alone"
    }
    all_opportunities.append(crypto_arb)
    
    # OPPORTUNITY 2: AI Agency (Local Services)
    ai_agency = {
        "name": "AI Automation Agency (HVAC/Dental/Roofing)",
        "category": "Services",
        "description": "High-ticket retainers for local service businesses (HVAC, dental, roofing)",
        "scores": {
            "revenue_potential": {
                "score": 95,
                "reasoning": "10-20 clients at $3K-5K/month = $30K-100K/month achievable in 12-18 months",
                "ceiling": "$50K-150K/month"
            },
            "speed_to_first_dollar": {
                "score": 70,
                "reasoning": "Can close first client in 2-4 weeks with aggressive outreach",
                "timeline": "14-30 days"
            },
            "capital_efficiency": {
                "score": 90,
                "reasoning": "Low capital needs ($1K-3K for tools/ads), high margins (60-80%)",
                "roi": "10x-30x LTV:CAC ratio"
            },
            "competitive_moat": {
                "score": 70,
                "reasoning": "First-mover in boring verticals, case studies create barriers, client relationships sticky",
                "barriers": "Medium - requires domain expertise and trust"
            },
            "execution_complexity": {
                "score": 50,
                "reasoning": "Requires sales skill, service delivery, client management, team building at scale",
                "difficulty": "Medium-High"
            },
            "market_timing": {
                "score": 85,
                "reasoning": "AI adoption in local services just beginning, 3-5 year window before saturation",
                "trend": "Strong upward"
            }
        },
        "weighted_total_score": 79.75,
        "capital_required": "$1K-5K (tools, ads, VA support)",
        "time_to_100k_monthly": "12-18 months (15-20 clients at $5K-7K/month avg)",
        "next_steps": [
            "1. Pick ONE niche (HVAC recommended for highest pain + budget)",
            "2. Build list of 100 prospects using Google Maps + LinkedIn",
            "3. Create 1-page offer with clear outcome and pricing",
            "4. Send 25 cold emails per day for 2 weeks",
            "5. Book 10 calls, close 2-3 pilot clients at $1.5K-3K/month",
            "6. Deliver results, get testimonials, scale outreach",
            "7. Hire VA/delivery support at $10K/month revenue",
            "8. Add second niche or geography at $20K-30K/month"
        ],
        "verdict": "PRIMARY PATH - Highest probability to reach $100K/month with moderate capital and 12-18 month timeline"
    }
    all_opportunities.append(ai_agency)
    
    # OPPORTUNITY 3: Viral Product Launch (Micro-SaaS)
    viral_product = {
        "name": "Viral Micro-SaaS Product Launch",
        "category": "Product",
        "description": "Product Hunt + HN launch for AI tool or dev tool with viral potential",
        "scores": {
            "revenue_potential": {
                "score": 60,
                "reasoning": "Top 1%: $500-2K MRR in first 48 hours. Average: $0-100 MRR. $100K/month requires breakout success (rare) or portfolio approach",
                "ceiling": "$5K-50K/month per product (outliers hit $100K+)"
            },
            "speed_to_first_dollar": {
                "score": 50,
                "reasoning": "2-4 weeks to build MVP, 1-3 months to Product Hunt launch, revenue starts at launch",
                "timeline": "30-90 days"
            },
            "capital_efficiency": {
                "score": 75,
                "reasoning": "Low capital needs ($0-2K for MVP with no-code tools), 70-90% margins if hits",
                "roi": "Infinite if bootstrap, but most fail to monetize"
            },
            "competitive_moat": {
                "score": 40,
                "reasoning": "Easy to copy, fast-follow competitors launch within weeks",
                "barriers": "Low unless network effects or unique data"
            },
            "execution_complexity": {
                "score": 60,
                "reasoning": "Requires product sense, design, launch coordination, community building",
                "difficulty": "Medium"
            },
            "market_timing": {
                "score": 70,
                "reasoning": "AI tools saturating fast (2-4 weeks), dev tools slower (6-12 weeks). Timing matters.",
                "trend": "Varies by category"
            }
        },
        "weighted_total_score": 59.0,
        "capital_required": "$0-2K (no-code tools, ads)",
        "time_to_100k_monthly": "18-36 months (portfolio of 5-10 products at $10K-20K MRR each)",
        "next_steps": [
            "1. Research Product Hunt top launches in your category (last 30 days)",
            "2. Identify gap: what problem is discussed but not solved?",
            "3. Run 10-15 customer discovery interviews to validate pain",
            "4. Build landing page, drive traffic, track signups (target: 5-15%)",
            "5. Get 5-10 pre-sales or concierge MVP customers",
            "6. Build MVP in 2-4 weeks using no-code tools",
            "7. Prepare 4-6 week Product Hunt launch playbook",
            "8. Execute launch, track conversion, iterate weekly"
        ],
        "verdict": "PORTFOLIO PLAY - Use as lead magnet for services OR build 5-10 products for diversified $100K/month"
    }
    all_opportunities.append(viral_product)
    
    # OPPORTUNITY 4: Enterprise AI Agent Services
    enterprise_ai = {
        "name": "Enterprise AI Agent Services",
        "category": "Services",
        "description": "High-ticket AI agent implementations for Fortune 500 / mid-market enterprises",
        "scores": {
            "revenue_potential": {
                "score": 100,
                "reasoning": "2 clients at $50K/month = $100K/month. Enterprise pricing supports goal directly.",
                "ceiling": "$100K-500K+/month"
            },
            "speed_to_first_dollar": {
                "score": 25,
                "reasoning": "6-12 month sales cycles, SOC 2 required (6-12 months), first revenue in 9-18 months",
                "timeline": "270-540 days"
            },
            "capital_efficiency": {
                "score": 40,
                "reasoning": "SOC 2 costs $50K-150K, team building required, but margins are 40-60%",
                "roi": "3x-5x over 24 months"
            },
            "competitive_moat": {
                "score": 85,
                "reasoning": "SOC 2, industry expertise, case studies create high barriers. Client contracts are sticky.",
                "barriers": "High - compliance and credibility required"
            },
            "execution_complexity": {
                "score": 30,
                "reasoning": "Requires enterprise sales, compliance, delivery team, legal, infrastructure",
                "difficulty": "Very High"
            },
            "market_timing": {
                "score": 80,
                "reasoning": "Enterprise AI spending growing 36% YoY, $85K/month average spend. Strong demand.",
                "trend": "Strong upward"
            }
        },
        "weighted_total_score": 62.5,
        "capital_required": "$50K-150K (SOC 2, team, infrastructure)",
        "time_to_100k_monthly": "18-24 months (2-3 enterprise clients)",
        "next_steps": [
            "1. Choose vertical specialization (healthcare, finance, logistics)",
            "2. Start SOC 2 Type II certification process (6-12 month lead time)",
            "3. Build 2-3 case studies from any existing work (even discounted pilots)",
            "4. Create RFP response templates",
            "5. Build pipeline of 50-100 enterprise accounts",
            "6. Hire enterprise sales rep with proven track record",
            "7. Partner with consultancies for referrals",
            "8. Close first deal at $30K-60K/month in 9-12 months"
        ],
        "verdict": "LONG GAME - Highest revenue ceiling but longest timeline. Requires significant capital and patience."
    }
    all_opportunities.append(enterprise_ai)
    
    # OPPORTUNITY 5: Boring Industry Micro-SaaS
    boring_saas = {
        "name": "Boring Industry Micro-SaaS (Manufacturing/HVAC/Florists)",
        "category": "Product",
        "description": "Niche SaaS for under-served 'boring' industries with high pain + low competition",
        "scores": {
            "revenue_potential": {
                "score": 75,
                "reasoning": "100-200 customers at $100-500/month = $10K-100K/month achievable in 18-36 months",
                "ceiling": "$20K-100K/month"
            },
            "speed_to_first_dollar": {
                "score": 60,
                "reasoning": "4-8 weeks validation + MVP build, 30-60 days to first paying customer",
                "timeline": "60-120 days"
            },
            "capital_efficiency": {
                "score": 85,
                "reasoning": "Low capital needs ($1K-5K for MVP), 70-90% margins, sticky retention",
                "roi": "10x-20x over 24 months"
            },
            "competitive_moat": {
                "score": 80,
                "reasoning": "Niche focus, domain expertise, integrations create barriers. Most use Excel today.",
                "barriers": "Medium-High - requires industry knowledge"
            },
            "execution_complexity": {
                "score": 55,
                "reasoning": "Requires domain research, customer discovery, product development, support",
                "difficulty": "Medium"
            },
            "market_timing": {
                "score": 75,
                "reasoning": "Boring industries slow to adopt tech, 5-10 year window before saturation",
                "trend": "Steady upward"
            }
        },
        "weighted_total_score": 72.25,
        "capital_required": "$1K-5K (MVP, initial marketing)",
        "time_to_100k_monthly": "24-36 months (500-1000 customers at $100-200/month)",
        "next_steps": [
            "1. Pick ONE boring industry (manufacturing compliance, florist inventory, HVAC scheduling)",
            "2. Run 10-15 customer discovery interviews",
            "3. Build landing page, test demand (target: 25+ signups in 7 days)",
            "4. Get 5-10 pre-sales or concierge MVP customers",
            "5. Build MVP with ONE core feature using no-code tools",
            "6. Track retention (40%+ day 7, 20%+ day 30)",
            "7. Iterate based on feedback, add features quarterly",
            "8. Scale via SEO, word-of-mouth, industry associations"
        ],
        "verdict": "SOLID MIDDLE PATH - Sustainable $20K-50K/month achievable, scalable to $100K with patience"
    }
    all_opportunities.append(boring_saas)
    
    # Sort by weighted score
    all_opportunities.sort(key=lambda x: x["weighted_total_score"], reverse=True)
    
    # Personalized Recommendations Based on Profile
    profile = {
        "capital": capital,
        "time": time,
        "risk": risk,
        "target": target
    }
    
    if capital < 5000:
        capital_filter = "Low capital scenarios - prioritize service models over trading"
        recommended = ["AI Agency", "Boring SaaS", "Viral Product"]
        avoid = ["Crypto Arbitrage (needs $5K+)", "Enterprise AI (needs $50K+)"]
    elif capital < 50000:
        capital_filter = "Medium capital - can pursue any path except enterprise"
        recommended = ["AI Agency", "Boring SaaS", "Viral Product", "Crypto Arbitrage"]
        avoid = ["Enterprise AI (needs $50K+ for SOC 2)"]
    else:
        capital_filter = "High capital - all paths available"
        recommended = ["All opportunities feasible"]
        avoid = []
    
    if time == "part_time" or time == "weekends":
        time_filter = "Limited time - prioritize automation-friendly models"
        time_adjusted_recs = ["Crypto Arbitrage (automated)", "Boring SaaS (after MVP)", "Viral Product (passive after launch)"]
        time_avoid = ["AI Agency (requires active sales + delivery)", "Enterprise AI (requires full-time+ team)"]
    else:
        time_filter = "Full-time available - can pursue high-touch models"
        time_adjusted_recs = ["AI Agency", "Enterprise AI", "Boring SaaS"]
        time_avoid = []
    
    if risk == "low":
        risk_filter = "Risk-averse - prioritize proven service models"
        risk_adjusted_recs = ["AI Agency (proven, fast validation)", "Boring SaaS (slow but steady)"]
        risk_avoid = ["Crypto Arbitrage (capital at risk)", "Viral Product (hit-or-miss)", "Enterprise AI (long runway)"]
    elif risk == "high":
        risk_filter = "High risk tolerance - can swing for home runs"
        risk_adjusted_recs = ["Viral Product (lottery ticket)", "Enterprise AI (big payoff)", "Crypto Arbitrage (active risk)"]
        risk_avoid = []
    else:
        risk_filter = "Moderate risk - balanced approach"
        risk_adjusted_recs = ["AI Agency", "Boring SaaS", "Viral Product portfolio"]
        risk_avoid = ["Crypto Arbitrage (too speculative)", "Enterprise AI (too slow)"]
    
    # Final Recommendation
    if capital >= 5000 and time == "full_time" and risk in ["medium", "high"]:
        primary_rec = "AI Automation Agency (Local Services)"
        secondary_rec = "Boring Industry Micro-SaaS"
        rationale = "Your profile (capital, time, risk tolerance) fits the AI Agency model best. Fastest path to $100K/month in 12-18 months with 15-20 clients."
    elif capital < 5000 and time == "full_time":
        primary_rec = "AI Automation Agency (Start with $0 concierge MVP)"
        secondary_rec = "Viral Product Launch (bootstrap with no-code)"
        rationale = "Low capital but full-time availability. Start AI agency with concierge MVP (no tech build), get first 3-5 clients manually, then automate."
    elif time == "part_time":
        primary_rec = "Boring Industry Micro-SaaS"
        secondary_rec = "Viral Product Launch"
        rationale = "Part-time availability favors productized models. Build once, sell repeatedly. Start with validation, then MVP."
    else:
        primary_rec = "Boring Industry Micro-SaaS"
        secondary_rec = "AI Automation Agency"
        rationale = "Balanced approach - build defensible product in niche market, supplement with service revenue."
    
    # 90-Day Action Plan to First Dollar
    action_plan_90_days = {
        "days_1_30": {
            "primary_focus": "Validation + First Customer",
            "ai_agency_path": [
                "Week 1: Pick niche (HVAC), build prospect list of 100",
                "Week 2-3: Send 25 emails/day, book 10 calls",
                "Week 4: Close 1-2 pilot clients at $1.5K-2K/month",
                "Revenue by Day 30: $1.5K-4K MRR"
            ],
            "boring_saas_path": [
                "Week 1: Pick industry, run 10 customer interviews",
                "Week 2: Build landing page, drive traffic (target: 25+ signups)",
                "Week 3: Offer concierge MVP to 5-10 signups",
                "Week 4: Get 2-5 paying customers at $50-100/month",
                "Revenue by Day 30: $100-500 MRR"
            ]
        },
        "days_31_60": {
            "primary_focus": "Delivery + Expansion",
            "ai_agency_path": [
                "Week 5-6: Deliver results to pilot clients, document wins",
                "Week 7-8: Refine offer, add 2-3 more clients",
                "Revenue by Day 60: $6K-12K MRR"
            ],
            "boring_saas_path": [
                "Week 5-6: Build basic MVP (no-code), migrate concierge customers",
                "Week 7-8: Add 5-10 more customers via word-of-mouth + organic",
                "Revenue by Day 60: $500-1.5K MRR"
            ]
        },
        "days_61_90": {
            "primary_focus": "Scale Systems",
            "ai_agency_path": [
                "Week 9-10: Hire VA for admin, systematize delivery",
                "Week 11-12: Add 2-3 more clients, hit $10K-15K MRR",
                "Revenue by Day 90: $10K-20K MRR"
            ],
            "boring_saas_path": [
                "Week 9-10: Optimize onboarding, reduce churn",
                "Week 11-12: Launch SEO content, partnerships, hit $2K-3K MRR",
                "Revenue by Day 90: $2K-5K MRR"
            ]
        }
    }
    
    # Path from $10K to $100K Monthly
    scaling_roadmap = {
        "ai_agency_10k_to_100k": {
            "current_state": "$10K MRR (3-5 clients at $2K-3K/month)",
            "month_4_9": {
                "goal": "$30K-50K MRR",
                "actions": [
                    "Add 5-10 more clients via referrals + outbound",
                    "Raise prices to $3K-5K/month for new clients",
                    "Hire 1-2 delivery specialists",
                    "Build case studies and testimonials"
                ]
            },
            "month_10_18": {
                "goal": "$100K MRR",
                "actions": [
                    "Total clients: 15-20 at $5K-7K/month average",
                    "Hire SDR for outbound pipeline",
                    "Expand to second niche or geography",
                    "Systematize delivery (playbooks, SOPs)",
                    "Consider productizing common workflows into SaaS"
                ]
            },
            "timeline": "12-18 months from start"
        },
        "boring_saas_5k_to_100k": {
            "current_state": "$5K MRR (50-100 customers at $50-100/month)",
            "month_6_18": {
                "goal": "$20K-40K MRR",
                "actions": [
                    "Scale to 200-400 customers via SEO + word-of-mouth",
                    "Add features based on retention analysis",
                    "Introduce annual plans (discount for upfront payment)",
                    "Build integrations to increase stickiness"
                ]
            },
            "month_19_36": {
                "goal": "$100K MRR",
                "actions": [
                    "Total customers: 500-1000 at $100-200/month",
                    "OR: 200-300 at $300-500/month (enterprise tier)",
                    "Hire support + sales team",
                    "Expand product line or adjacent niches",
                    "Build network effects or viral loops"
                ]
            },
            "timeline": "24-36 months from start"
        }
    }
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "analysis": "Unified Opportunity Scoring Dashboard",
        "profile": profile,
        "scoring_criteria": scoring_criteria,
        "all_opportunities": all_opportunities,
        "top_3_by_score": [opp["name"] for opp in all_opportunities[:3]],
        "personalized_filters": {
            "capital_filter": capital_filter,
            "recommended": recommended,
            "avoid": avoid,
            "time_filter": time_filter,
            "time_adjusted": time_adjusted_recs,
            "risk_filter": risk_filter,
            "risk_adjusted": risk_adjusted_recs
        },
        "final_recommendation": {
            "primary": primary_rec,
            "secondary": secondary_rec,
            "rationale": rationale
        },
        "action_plan_90_days": action_plan_90_days,
        "scaling_roadmap": scaling_roadmap,
        "key_insights": [
            "AI Agency: Highest score (79.75), fastest to $100K/month (12-18 months)",
            "Enterprise AI: Highest ceiling but slowest (18-24 months due to SOC 2 + sales cycles)",
            "Boring SaaS: Strong middle path (72.25 score), 24-36 months to $100K",
            "Viral Product: Hit-or-miss (59.0 score), better as portfolio or lead magnet",
            "Crypto Arbitrage: Supplemental income (52.5 score), won't reach $100K alone",
            "Best combo: AI Agency (primary) + Boring SaaS (long-term asset)",
            "With $10K capital + full-time: AI Agency is optimal path",
            "90-day goal: $10K-20K MRR if focused execution",
            "12-18 month goal: $100K MRR via 15-20 agency clients OR portfolio approach"
        ],
        "immediate_next_steps": [
            "1. Based on your profile, start with: " + primary_rec,
            "2. Follow 90-day action plan above (validation → first customer → scale)",
            "3. Track weekly: revenue, pipeline, delivery capacity",
            "4. At $10K MRR, hire first team member (VA or delivery specialist)",
            "5. At $30K MRR, systematize operations and add sales capacity",
            "6. At $50K MRR, consider second revenue stream or geographic expansion",
            "7. Document everything - build SaaS from agency learnings as long-term asset"
        ]
    }
