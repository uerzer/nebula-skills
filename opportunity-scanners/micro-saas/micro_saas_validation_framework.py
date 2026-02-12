"""
Micro-SaaS Validation Framework
Pain point extraction, ICP research, and conversion tracking for rapid validation

Key Research Insights (2026):
- 42% of startups fail due to "no market need" (CB Insights)
- 25 customer interviews > 50 if you start with hypothesis
- Top micro-SaaS: $5K-50K MRR, 70-90% margins
- Boring industries: highest willingness to pay, lowest competition
- Validation timeline: 2-4 weeks max before building
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

def transform(data: dict, context: dict) -> dict:
    """
    Validates micro-SaaS ideas through systematic pain point extraction and ICP research.
    
    Input data structure:
    {
        "product_idea": "AI tool for X",
        "target_industry": "SaaS founders",
        "validation_stage": "hypothesis"  # or "interviews", "landing_page", "mvp"
    }
    
    Returns validation checklist, interview scripts, and go/no-go criteria.
    """
    
    # Extract configuration
    idea = data.get("product_idea", "Untitled idea")
    industry = data.get("target_industry", "General")
    stage = data.get("validation_stage", "hypothesis")
    
    # Why Most Micro-SaaS Fails
    failure_analysis = {
        "primary_cause": "No market need (42% of failures)",
        "secondary_causes": [
            "Built solution before validating problem",
            "Targeted too broad an audience",
            "Couldn't articulate who would pay and why",
            "Spent months building before getting one paying customer",
            "Confused 'would use' with 'would pay'"
        ],
        "cost_of_failure": {
            "time_wasted": "3-6 months of development",
            "money_wasted": "$5K-50K in opportunity cost",
            "emotional_toll": "Burnout, loss of confidence"
        }
    }
    
    # The Validation Framework (2-4 Weeks Max)
    validation_framework = {
        "stage_1_hypothesis_building": {
            "timeline": "Days 1-3",
            "objective": "Build a testable hypothesis, not a business plan",
            "components": {
                "icp_profile": {
                    "who": "Specific role + industry + company size",
                    "example": "Not 'small businesses' → 'Solo HVAC contractors with $500K-2M revenue'",
                    "pain_points": "What specific recurring problem costs them time/money?",
                    "current_solution": "What are they using now? (spreadsheet, manual, expensive tool)",
                    "budget_signals": "What do they currently spend on related problems?",
                    "access": "Where can you find 10 of these people?"
                },
                "value_proposition": {
                    "formula": "We help [WHO] do [WHAT] without [PAIN]",
                    "bad_example": "AI-powered automation for businesses",
                    "good_example": "Help solo HVAC contractors schedule appointments 24/7 without missing calls"
                },
                "hypothesis_template": {
                    "problem": "[TARGET] loses [$ AMOUNT] monthly because [SPECIFIC PAIN]",
                    "solution": "A [PRODUCT TYPE] that [OUTCOME] in [TIME]",
                    "willingness_to_pay": "[TARGET] currently pays [$ AMOUNT] for [WORKAROUND]",
                    "example": "Solo dentists lose $8K/month because no-shows waste 40-minute slots. An AI reminder system that reduces no-shows 40% in 30 days. Dentists currently pay $800/mo for office staff to manually call reminders."
                }
            },
            "tools_to_use": [
                "Reddit search: '[industry] + I wish there was'",
                "G2 reviews: 2-3 star reviews of competitors",
                "Upwork: What are people paying freelancers to do?",
                "LinkedIn: Search for your ICP, see what they post about",
                "Industry forums: Scan for recurring complaints"
            ],
            "validation_checkpoint": "Can you name 10 specific people who have this problem?"
        },
        
        "stage_2_customer_discovery": {
            "timeline": "Days 4-14",
            "objective": "Validate the problem (not the solution) with 10-25 interviews",
            "why_25_not_50": {
                "insight": "With a hypothesis from Stage 1, you need fewer interviews",
                "data": "60% of B2B marketers captured ICP elements after 20 interviews with hypothesis",
                "without_hypothesis": "40-50 interviews needed to find patterns"
            },
            "finding_respondents": {
                "tier_1_warm": [
                    "LinkedIn connections in target industry",
                    "Founder Slack communities (Indie Hackers, r/SaaS)",
                    "Twitter/X DMs: 'Researching X problem, mind 10 minutes?'"
                ],
                "tier_2_cold": [
                    "Apollo/Clay: Scrape target company lists",
                    "Cold email (interview, not sales): 10-20% response rate",
                    "UserInterviews.com, Respondent.io (paid)"
                ],
                "tier_3_communities": [
                    "Reddit: Comment in target industry subs, ask for interviews",
                    "Facebook groups: Value-first posts, then interview requests",
                    "Industry conferences: Virtual or in-person networking"
                ]
            },
            "interview_script": {
                "introduction": "Hi [Name], I'm researching [problem area] and would love to understand your workflow. Not selling anything, just learning. 15-20 minutes?",
                "questions": [
                    "How do you currently handle [problem]?",
                    "What's annoying or frustrating about your current approach?",
                    "What have you tried to fix it? What happened?",
                    "What does it cost you (time or money) when [problem] happens?",
                    "Have you looked for tools to solve this? What did you find?",
                    "If there was a solution, what would you be willing to pay?",
                    "What would make you switch next week vs. in 6 months?"
                ],
                "what_NOT_to_ask": [
                    "Would you use this?" (They'll say yes to be nice)",
                    "Do you like my idea?" (Opinion, not commitment)",
                    "Describing your solution upfront (You're biasing them)"
                ],
                "what_to_listen_for": {
                    "pain_urgency": "Is this a 'nice to have' or 'pulling my hair out'?",
                    "current_spend": "Are they paying for workarounds now?",
                    "decision_authority": "Can they buy, or do they need 5 approvals?",
                    "frequency": "Is this daily, weekly, or once-a-year?",
                    "exact_words": "Note their language—use it in your copy"
                }
            },
            "validation_checkpoint": "After 10-15 interviews, can you answer: Who has the most urgent pain? What exact words do they use? What do they pay today?"
        },
        
        "stage_3_landing_page_test": {
            "timeline": "Days 15-18",
            "objective": "Quantify demand with a simple landing page + email capture",
            "no_code_tools": [
                "Carrd.co (fastest, $19/year)",
                "Notion (free, but slower)",
                "Webflow (overkill for early tests)",
                "Wix or Squarespace (middle ground)"
            ],
            "page_structure": {
                "headline": "Use the exact problem language from interviews",
                "example": "Stop Losing $8K/Month to No-Show Patients",
                "subheadline": "Specific outcome in specific time",
                "example": "AI appointment reminders reduce no-shows 40% in 30 days",
                "social_proof": "If you have it (testimonials, logos, case studies)",
                "visual": "Screenshot or mockup (Canva or Figma)",
                "pricing_hint": "Show pricing tier or 'Starting at $X/mo'",
                "cta": "Sign up for early access' or 'Join waitlist'",
                "email_capture": "Mailchimp, ConvertKit, or simple Google Form"
            },
            "traffic_strategy": {
                "budget_0": [
                    "Post in relevant Reddit subs (value-first, not spam)",
                    "Share in Slack/Discord communities you're in",
                    "Personal LinkedIn/Twitter post",
                    "Ask interview participants to check it out"
                ],
                "budget_100_500": [
                    "Google Ads: Search for '[problem] solution'",
                    "Reddit ads: Target specific subreddits",
                    "Facebook/IG ads: If visual product",
                    "Twitter promoted posts to niche audience"
                ],
                "organic_seo": "Blog post on 'How to solve [problem]' linking to landing page"
            },
            "success_metrics": {
                "excellent": "50+ email signups in 7 days, 3+ 'when can I pay?' messages",
                "good": "25-50 signups, clear interest signals in comments",
                "weak": "10-25 signups, mostly curious but no urgency",
                "red_flag": "<10 signups despite 500+ visitors = messaging problem"
            },
            "validation_checkpoint": "Is signup rate >5% of visitors? Are people asking about pricing/launch date?"
        },
        
        "stage_4_pre_sell_or_concierge_mvp": {
            "timeline": "Days 19-30",
            "objective": "Get money BEFORE building the full product",
            "why_this_matters": "People lie about what they'll pay. Money is the only true signal.",
            "concierge_mvp_approach": {
                "concept": "Do the work manually behind the scenes, deliver results",
                "example_dental_reminders": {
                    "offer": "$79/month, I'll send appointment reminders to your patients",
                    "behind_scenes": "You manually text/call using a script and tracking sheet",
                    "deliver": "Weekly report: '24 reminders sent, 21 confirmed, 3 no-shows prevented'",
                    "result": "If 4+ stick for 60 days, build automation"
                },
                "example_hvac_booking": {
                    "offer": "$150/month, I'll handle your after-hours calls",
                    "behind_scenes": "You answer calls, book in their calendar manually",
                    "deliver": "Immediate response, appointments booked 24/7",
                    "result": "Validate volume, pain, and willingness to pay before AI build"
                }
            },
            "pre_sell_approach": {
                "offer": "'Lifetime access for $99' or '50% off first year'",
                "landing_page": "Add payment button (Stripe, Gumroad, LemonSqueezy)",
                "expectation_setting": "'Launches in 4-6 weeks, pay now to lock in price'",
                "refund_policy": "100% refund if not happy at launch",
                "target": "5-10 pre-sales = strong signal to build"
            },
            "validation_checkpoint": "Did 5+ people pay real money? If yes, build. If no, revisit positioning or niche."
        },
        
        "stage_5_build_and_iterate_mvp": {
            "timeline": "Weeks 5-8",
            "objective": "Build only the core feature that solves the core pain",
            "no_code_tools_2026": [
                "Fuzen.io (workflow automation without code)",
                "Bubble, Adalo, FlutterFlow (full apps)",
                "Zapier, Make.com (integrations + light automation)",
                "Airtable + Softr (database + frontend)",
                "Notion + Super.so (documentation + simple sites)"
            ],
            "mvp_scope": {
                "must_have": "One core feature that solves the main pain",
                "example": "Appointment reminder system → Just send SMS reminders",
                "nice_to_have": "Leave for v2 (analytics, integrations, mobile app)",
                "rule": "Can you deliver value in <5 minutes of user onboarding?"
            },
            "launch_to_waitlist": {
                "first_10_users": "From your waitlist, give personal onboarding",
                "track": "Daily usage, feature requests, churn signals",
                "iterate": "Weekly updates based on feedback",
                "goal": "Get 5+ to 'active weekly user' status"
            },
            "validation_checkpoint": "Are 30-50% of users active weekly? Are they asking for more features (good sign)?"
        }
    }
    
    # Boring Industries with High Willingness-to-Pay
    boring_goldmines = {
        "why_boring_wins": {
            "insight": "Tech-savvy markets are saturated. Boring industries are under-served.",
            "advantage": "Low competition, high pain, budget exists, long retention"
        },
        "top_7_niches_2026": [
            {
                "industry": "Manufacturing",
                "pain": "Compliance documentation (avoid $2.5M fines)",
                "tool_idea": "Automated audit trail + inspection checklists",
                "pricing": "$200-500/month per facility",
                "competition": "Low - most use Excel or paper"
            },
            {
                "industry": "HVAC Contractors",
                "pain": "After-hours calls = lost $5K-20K jobs",
                "tool_idea": "24/7 AI booking + emergency routing",
                "pricing": "$150-300/month",
                "competition": "Low - current options are enterprise-focused"
            },
            {
                "industry": "Home Inspectors",
                "pain": "Manual report writing takes 3-4 hours post-inspection",
                "tool_idea": "Tap-to-report mobile app with instant PDF",
                "pricing": "$50-100/month",
                "competition": "Existing tools are clunky and expensive"
            },
            {
                "industry": "Dental Practices",
                "pain": "No-shows cost $200-400 per slot",
                "tool_idea": "AI reminder system via SMS/voice",
                "pricing": "$100-300/month",
                "competition": "Medium - but most require complex integrations"
            },
            {
                "industry": "Florists",
                "pain": "Manual inventory tracking = 30% waste on perishables",
                "tool_idea": "Stem calculator + purchase order automation",
                "pricing": "$30-80/month",
                "competition": "Near-zero - they use spreadsheets"
            },
            {
                "industry": "Marina Operators",
                "pain": "Safety audit scheduling and compliance",
                "tool_idea": "Automated inspection scheduler + reporting",
                "pricing": "$100-250/month",
                "competition": "Zero - highly regulated niche"
            },
            {
                "industry": "Non-Profits",
                "pain": "Grant reporting is manual, time-consuming",
                "tool_idea": "Grant tracking + funder-ready report generator",
                "pricing": "$50-150/month",
                "competition": "Low - most tools are enterprise-focused"
            }
        ]
    }
    
    # ICP Research Framework
    icp_framework = {
        "definition": "Ideal Customer Profile = specific person who has urgent pain + budget + decision authority",
        "bad_icp_examples": [
            "Small businesses",
            "Entrepreneurs",
            "SaaS founders",
            "Marketing agencies"
        ],
        "good_icp_examples": [
            "Solo HVAC contractors in Texas with $500K-2M revenue, 2-5 service trucks",
            "Boutique dental practices with 3+ dentists, office manager handling scheduling",
            "Independent home inspectors doing 10-20 inspections/month",
            "Non-profit program directors managing 3+ federal grants"
        ],
        "icp_research_process": {
            "step_1_demographics": {
                "role": "Who makes the buying decision?",
                "company_size": "Revenue, employees, locations",
                "industry": "Vertical + sub-vertical",
                "geography": "Does location matter for your solution?"
            },
            "step_2_psychographics": {
                "goals": "What are they trying to achieve?",
                "challenges": "What blocks them from reaching goals?",
                "values": "Time-saver? Cost-reducer? Risk-avoider?",
                "tech_savvy": "Do they use Slack or email?"
            },
            "step_3_behavioral": {
                "where_they_hang_out": "LinkedIn groups? Reddit? Industry conferences?",
                "content_they_consume": "Podcasts? Newsletters? YouTube?",
                "buying_patterns": "Monthly SaaS? One-time purchase? Annual contracts?",
                "budget_authority": "Can they swipe card or need approval?"
            }
        },
        "validation_questions": [
            "Can I name 10 specific people who fit this profile?",
            "Do they have budget for this category ($X/month is normal)?",
            "Can I reach 100 of them in the next 30 days?",
            "Do they have urgent, recurring pain (not nice-to-have)?",
            "Can they buy without 5 levels of approval?"
        ]
    }
    
    # Conversion Tracking & Metrics
    conversion_metrics = {
        "landing_page_metrics": {
            "traffic_to_signup": "Target: 5-15% (if lower, messaging problem)",
            "signup_to_activation": "Did they complete onboarding? Target: 30-50%",
            "activation_to_weekly_use": "Are they coming back? Target: 30%+",
            "weekly_use_to_paid": "Free-to-paid conversion: Target: 5-15%"
        },
        "mvp_metrics": {
            "daily_active_users": "How many log in daily?",
            "weekly_active_users": "How many log in weekly?",
            "retention_day_7": "What % return after 7 days? Target: 40%+",
            "retention_day_30": "What % return after 30 days? Target: 20%+",
            "feature_usage": "Which features are actually used?",
            "support_requests": "What are they asking for?"
        },
        "revenue_metrics": {
            "mrr": "Monthly Recurring Revenue",
            "churn_rate": "What % cancel each month? Target: <5%",
            "ltv": "Lifetime Value = MRR × (1 / churn rate)",
            "cac": "Customer Acquisition Cost",
            "ltv_cac_ratio": "Target: 3:1 minimum, 5:1+ ideal"
        },
        "go_no_go_criteria": {
            "strong_go_signals": [
                "10+ email signups in 48 hours",
                "5+ pre-sales or concierge clients",
                "40%+ retention after 7 days",
                "Users asking 'when can I pay?'",
                "CAC < $50 for $50/mo product"
            ],
            "yellow_flags": [
                "Signups but low activation",
                "High interest but low willingness to pay",
                "Feature requests all over the map (unclear core pain)"
            ],
            "red_flags": [
                "<5 signups after 500 visitors",
                "No one willing to pre-pay",
                "High activation but zero retention",
                "No organic word-of-mouth"
            ]
        }
    }
    
    # Path to $100K/Month via Micro-SaaS
    revenue_model = {
        "realistic_expectations": {
            "year_1": "$1K-5K MRR (solo founder, bootstrapped)",
            "year_2": "$5K-20K MRR (with traction + SEO + word-of-mouth)",
            "year_3": "$20K-50K MRR (established product, hiring begins)",
            "outliers": "$100K+ MRR (1-2% of micro-SaaS)"
        },
        "path_to_100k_monthly": {
            "option_a_single_breakout": {
                "customers": "1,000 at $100/mo or 200 at $500/mo",
                "timeline": "3-5 years",
                "probability": "Very low (<1%)",
                "requirements": "Viral growth, strong network effects, or enterprise upsell"
            },
            "option_b_portfolio_approach": {
                "strategy": "5-10 micro-SaaS at $10K-20K MRR each",
                "timeline": "3-5 years",
                "probability": "Medium (requires systemization)",
                "requirements": "Repeatable playbook, VA support, clear niches"
            },
            "option_c_hybrid_services": {
                "strategy": "Micro-SaaS as lead gen for high-ticket services",
                "example": "Free tool → $5K-10K implementation/consulting",
                "timeline": "1-2 years",
                "probability": "High (proven model)",
                "requirements": "Service delivery capacity"
            }
        },
        "reality_check": "Micro-SaaS alone to $100K/month is rare. Use as ONE revenue stream."
    }
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "analysis": "Micro-SaaS Validation Framework",
        "product_idea": idea,
        "target_industry": industry,
        "current_stage": stage,
        "failure_analysis": failure_analysis,
        "validation_framework": validation_framework,
        "boring_goldmines": boring_goldmines,
        "icp_research": icp_framework,
        "conversion_metrics": conversion_metrics,
        "revenue_model": revenue_model,
        "key_insights": [
            "42% of startups fail due to 'no market need' - validate before building",
            "25 customer interviews with hypothesis > 50 without",
            "Boring industries: highest pain + budget, lowest competition",
            "Validation timeline: 2-4 weeks max (hypothesis → interviews → landing page → pre-sell)",
            "Money is the only true validation signal - get pre-sales or concierge clients",
            "MVP scope: ONE core feature that solves core pain, ship in weeks not months",
            "Top micro-SaaS: $5K-50K MRR, 70-90% margins, solo/small team",
            "Go signals: 10+ signups in 48h, 5+ pre-sales, 40%+ retention, low CAC",
            "Red flags: <5 signups per 500 visitors, no willingness to pay, zero retention",
            "$100K/month via micro-SaaS requires portfolio approach or services hybrid"
        ],
        "immediate_action_steps": [
            "1. Define specific ICP (role + industry + size + pain)",
            "2. Build hypothesis: [TARGET] loses [$ AMOUNT] because [PAIN]",
            "3. Find 10 people who match ICP profile (can you name them?)",
            "4. Conduct 10-15 customer discovery interviews (validate problem, not solution)",
            "5. Build landing page with problem language from interviews",
            "6. Drive 100-500 visitors, track signup rate (target: 5-15%)",
            "7. If signups > 25, offer concierge MVP or pre-sell",
            "8. Get 5+ paying customers BEFORE building full product",
            "9. Build MVP with ONE core feature using no-code tools",
            "10. Track retention (40%+ day 7, 20%+ day 30) and iterate"
        ]
    }
