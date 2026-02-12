"""
AI Agency Lead Generation System
Identifies high-pain industries, budget signals, and decision-maker tracking

Key Research Insights (2026):
- Top niches: HVAC, dental, roofing, tree removal, med spas, pain clinics, pool maintenance
- Pricing: $2K-$5K/month retainers for high-ticket service businesses
- Average ROI: 3-5x improvement in response rates within 60 days
- Market: $1.48 trillion AI spending expected in 2025 (Gartner)
- Competition: Still low in "boring" verticals with high margins
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

def transform(data: dict, context: dict) -> dict:
    """
    Identifies and ranks AI automation opportunities in high-margin service industries.
    
    Input data structure:
    {
        "target_city": "Austin",  # or multiple cities
        "min_business_revenue": 500000,  # $500K+ annual revenue
        "service_focus": "local_services"  # or "b2b", "healthcare", "professional"
    }
    
    Returns ranked opportunities with outreach templates and pricing guidance.
    """
    
    # Extract configuration
    target_city = data.get("target_city", "Austin")
    min_revenue = data.get("min_business_revenue", 500000)
    focus = data.get("service_focus", "local_services")
    
    # Top 7 "Boring" Niches That Print Money (Cameron England, LinkedIn 2026)
    high_ticket_niches = [
        {
            "industry": "HVAC Contractors",
            "pain_points": [
                "Seasonal lead spikes overwhelm staff",
                "Missed calls = lost revenue ($5K-20K per job)",
                "Manual scheduling causes double-bookings",
                "No automated follow-up for estimates",
                "Technicians waste time on non-qualified leads"
            ],
            "automation_opportunities": {
                "ai_receptionist": {
                    "solves": "24/7 call handling, appointment booking, emergency routing",
                    "tools": ["Synthflow ($29-299/mo)", "Bland AI ($0.09/min)", "Vapi ($0.05/min)"],
                    "client_value": "$10K-30K monthly revenue recovery from missed calls",
                    "your_retainer": "$1,500-$3,000/month"
                },
                "lead_qualification_bot": {
                    "solves": "Pre-qualify leads before technician dispatch",
                    "tools": ["Custom GPT via API", "Intercom", "Zendesk AI"],
                    "client_value": "30% reduction in wasted truck rolls",
                    "your_retainer": "$1,000-$2,000/month"
                },
                "automated_estimate_followup": {
                    "solves": "Systematic follow-up on $5K-$20K quotes",
                    "tools": ["Clay ($149-800/mo)", "Instantly AI ($37-358/mo)", "HubSpot AI"],
                    "client_value": "15-25% conversion lift on pending estimates",
                    "your_retainer": "$800-$1,500/month"
                }
            },
            "typical_business_size": "$1M-$10M annual revenue",
            "decision_maker": "Owner/GM",
            "budget_signals": [
                "Currently paying for Google Ads ($2K-10K/mo)",
                "Has 5+ service trucks",
                "Employs office staff for phones",
                "Reviews mention 'hard to reach' or 'slow callbacks'"
            ],
            "outreach_angle": "Stop losing $5K-$20K jobs to voicemail. AI receptionist books appointments 24/7.",
            "average_deal_size": "$2,000-$5,000/month retainer",
            "churn_risk": "Low - becomes mission-critical infrastructure"
        },
        {
            "industry": "Dental Practices",
            "pain_points": [
                "Appointment no-shows cost $200-400 per slot",
                "Front desk overwhelmed with scheduling calls",
                "Insurance verification is manual and error-prone",
                "Patient recall/reminder systems are clunky",
                "Can't afford full-time marketing coordinator"
            ],
            "automation_opportunities": {
                "appointment_confirmation_bot": {
                    "solves": "Automated reminders via SMS/voice reduce no-shows 40%",
                    "tools": ["Twilio + GPT-4", "Zendesk", "Custom solution"],
                    "client_value": "$8K-$15K monthly revenue saved from no-shows",
                    "your_retainer": "$800-$1,500/month"
                },
                "patient_intake_automation": {
                    "solves": "Digital forms + AI validation before appointment",
                    "tools": ["Typeform + Zapier", "Jotform + Make.com", "Custom GPT"],
                    "client_value": "Save 10-15 admin hours/week",
                    "your_retainer": "$600-$1,200/month"
                },
                "insurance_verification_assistant": {
                    "solves": "Pre-verify coverage before expensive procedures",
                    "tools": ["RPA + GPT-4 for form reading", "API integrations"],
                    "client_value": "Reduce billing errors by 30%, faster payment",
                    "your_retainer": "$1,000-$2,500/month"
                }
            },
            "typical_business_size": "$800K-$5M annual revenue per location",
            "decision_maker": "Practice Owner/Office Manager",
            "budget_signals": [
                "Multi-chair practice (3+ dentists)",
                "Paying for patient management software already",
                "Reviews mention 'long wait times' or 'scheduling issues'",
                "Recently expanded or opening new location"
            ],
            "outreach_angle": "Cut no-shows by 40% and save 15 admin hours weekly with AI automation.",
            "average_deal_size": "$1,500-$3,500/month retainer",
            "churn_risk": "Medium - ROI must be clear within 90 days"
        },
        {
            "industry": "Roofing Companies",
            "pain_points": [
                "Storm leads flood in, then go cold",
                "Sales reps struggle with quote follow-up",
                "Seasonal revenue spikes are chaotic",
                "High-ticket jobs ($10K-$50K) need persistent nurture",
                "Lead quality from online sources is terrible"
            ],
            "automation_opportunities": {
                "storm_lead_response_bot": {
                    "solves": "Instant response to emergency roof damage inquiries",
                    "tools": ["Bland AI for calls", "SMS automation", "Lead routing"],
                    "client_value": "First response in <5 min increases close rate 400%",
                    "your_retainer": "$1,500-$3,000/month"
                },
                "quote_followup_sequence": {
                    "solves": "Multi-touch follow-up on $10K-$50K quotes",
                    "tools": ["Clay", "Instantly AI", "HubSpot workflows"],
                    "client_value": "15-30% lift in quote-to-close rate",
                    "your_retainer": "$1,000-$2,500/month"
                },
                "lead_scoring_qualification": {
                    "solves": "Filter out tire-kickers, prioritize insurance jobs",
                    "tools": ["Custom GPT scoring model", "CRM integration"],
                    "client_value": "Sales reps focus on qualified $20K+ opportunities",
                    "your_retainer": "$800-$1,500/month"
                }
            },
            "typical_business_size": "$2M-$20M annual revenue",
            "decision_maker": "Owner/Sales Manager",
            "budget_signals": [
                "Paying for HomeAdvisor/Angi leads ($500-2K/mo)",
                "Has sales team (not just owner doing sales)",
                "Truck fleet with branding",
                "Google Ads spend $3K+/month"
            ],
            "outreach_angle": "Stop wasting sales time on unqualified leads. AI scores and routes your best $20K+ opportunities.",
            "average_deal_size": "$2,000-$4,000/month retainer",
            "churn_risk": "Low - seasonal but renewable annually"
        },
        {
            "industry": "Med Spas / Aesthetic Clinics",
            "pain_points": [
                "High-value procedures ($2K-10K) need nurture",
                "Booking coordination across multiple providers",
                "Consultation no-shows waste physician time",
                "Manual patient education pre-procedure",
                "Social proof/review management is inconsistent"
            ],
            "automation_opportunities": {
                "consultation_booking_bot": {
                    "solves": "AI-powered scheduling with availability sync",
                    "tools": ["Cal.com + GPT", "Acuity + Zapier", "Custom solution"],
                    "client_value": "Fill $2K-$10K consultation slots automatically",
                    "your_retainer": "$1,200-$2,500/month"
                },
                "pre_procedure_education_bot": {
                    "solves": "Automated Q&A about Botox, fillers, laser treatments",
                    "tools": ["Custom GPT chatbot", "Intercom", "Drift"],
                    "client_value": "Reduce pre-consult anxiety, increase show-up rate 25%",
                    "your_retainer": "$800-$1,500/month"
                },
                "review_request_automation": {
                    "solves": "Systematic review requests post-treatment",
                    "tools": ["Birdeye integration", "Podium", "Custom SMS flow"],
                    "client_value": "2-3x more Google reviews = more organic bookings",
                    "your_retainer": "$600-$1,000/month"
                }
            },
            "typical_business_size": "$500K-$5M annual revenue",
            "decision_maker": "Owner/Marketing Manager",
            "budget_signals": [
                "Active on Instagram with 1K+ followers",
                "Paying for social media ads",
                "Offering high-ticket packages ($5K+)",
                "Multiple treatment providers on staff"
            ],
            "outreach_angle": "Fill your $2K-$10K consultation calendar on autopilot with AI booking.",
            "average_deal_size": "$1,500-$3,000/month retainer",
            "churn_risk": "Medium - competitive market, must show clear ROI"
        },
        {
            "industry": "Tree Removal / Arborist Services",
            "pain_points": [
                "Emergency calls outside business hours",
                "Job size varies wildly ($500-$20K)",
                "Quote accuracy requires site visit",
                "Insurance work has specific documentation needs",
                "Seasonal demand spikes (storm season)"
            ],
            "automation_opportunities": {
                "emergency_call_routing": {
                    "solves": "24/7 emergency tree removal intake and crew dispatch",
                    "tools": ["Bland AI", "Twilio", "Custom GPT routing logic"],
                    "client_value": "$10K-$30K monthly from after-hours emergencies",
                    "your_retainer": "$1,500-$3,000/month"
                },
                "photo_based_quoting": {
                    "solves": "AI estimates tree height, risk, pricing from photos",
                    "tools": ["GPT-4 Vision", "Custom model", "Form integration"],
                    "client_value": "Reduce site visit costs by 40%, faster quotes",
                    "your_retainer": "$1,000-$2,000/month"
                },
                "insurance_documentation": {
                    "solves": "Auto-generate required docs for insurance claims",
                    "tools": ["Document automation", "GPT-4", "PDF generation"],
                    "client_value": "Close insurance jobs 2x faster",
                    "your_retainer": "$800-$1,500/month"
                }
            },
            "typical_business_size": "$800K-$5M annual revenue",
            "decision_maker": "Owner",
            "budget_signals": [
                "Multiple crews/trucks",
                "Specialized equipment (cranes, chippers)",
                "Insurance-heavy client base",
                "Premium pricing ($2K+ per job average)"
            ],
            "outreach_angle": "Capture $10K-$30K in after-hours emergency calls with AI dispatcher.",
            "average_deal_size": "$1,800-$3,500/month retainer",
            "churn_risk": "Low - emergency infrastructure is sticky"
        },
        {
            "industry": "Pain Management Clinics",
            "pain_points": [
                "Complex insurance pre-authorization processes",
                "Referral coordination from primary care",
                "Compliance documentation for controlled substances",
                "Patient intake requires detailed medical history",
                "High no-show rates for follow-up appointments"
            ],
            "automation_opportunities": {
                "insurance_preauth_automation": {
                    "solves": "Auto-submit and track prior authorization requests",
                    "tools": ["RPA + GPT-4", "API integrations with payers"],
                    "client_value": "$20K-$50K monthly revenue acceleration",
                    "your_retainer": "$2,000-$5,000/month"
                },
                "referral_intake_bot": {
                    "solves": "Collect referral info and schedule efficiently",
                    "tools": ["Custom GPT + EHR integration", "HIPAA-compliant hosting"],
                    "client_value": "Process 30% more referrals with same staff",
                    "your_retainer": "$1,500-$3,000/month"
                },
                "compliance_documentation": {
                    "solves": "Automated audit trails for DEA compliance",
                    "tools": ["Document automation", "Secure logging", "Alert systems"],
                    "client_value": "Reduce audit risk, pass inspections easily",
                    "your_retainer": "$1,500-$4,000/month"
                }
            },
            "typical_business_size": "$2M-$20M annual revenue",
            "decision_maker": "Practice Administrator/Compliance Officer",
            "budget_signals": [
                "Multi-physician practice",
                "Complex EHR system already in place",
                "Dedicated billing staff",
                "Dealing with payer mix (Medicare, commercial, workers comp)"
            ],
            "outreach_angle": "Automate insurance pre-auth and accelerate $20K-$50K monthly revenue.",
            "average_deal_size": "$3,000-$7,000/month retainer",
            "churn_risk": "Very Low - healthcare compliance is critical"
        },
        {
            "industry": "Pool Maintenance / Service",
            "pain_points": [
                "Route optimization for service techs",
                "Chemical inventory management",
                "Seasonal contract renewals (50% churn if forgotten)",
                "Customer communication about service visits",
                "Upselling pool repairs and upgrades"
            ],
            "automation_opportunities": {
                "route_optimization": {
                    "solves": "AI-optimized daily routes save fuel and time",
                    "tools": ["Route planning APIs", "Custom optimization", "Maps integration"],
                    "client_value": "Save 10-15 hours weekly, service 20% more pools",
                    "your_retainer": "$800-$1,500/month"
                },
                "seasonal_renewal_automation": {
                    "solves": "Auto-send renewal offers 60 days before season",
                    "tools": ["Email/SMS sequences", "Payment link integration"],
                    "client_value": "Boost renewal rate from 50% to 75%+",
                    "your_retainer": "$600-$1,200/month"
                },
                "upsell_detection": {
                    "solves": "AI flags pools needing repairs based on service notes",
                    "tools": ["GPT-4 analysis of tech notes", "CRM alerts"],
                    "client_value": "$5K-$15K monthly upsell revenue",
                    "your_retainer": "$800-$1,500/month"
                }
            },
            "typical_business_size": "$500K-$3M annual revenue",
            "decision_maker": "Owner/Operations Manager",
            "budget_signals": [
                "50+ recurring service accounts",
                "Multiple service techs",
                "Truck fleet",
                "Offering repair services (not just maintenance)"
            ],
            "outreach_angle": "Boost contract renewals to 75%+ and add $5K-$15K monthly upsell revenue.",
            "average_deal_size": "$1,200-$2,500/month retainer",
            "churn_risk": "Medium - seasonal nature but strong retention if ROI clear"
        }
    ]
    
    # Decision-Maker Research Template
    decision_maker_intel = {
        "primary_contact": "Owner or GM (local services) / Practice Admin (healthcare)",
        "linkedin_search_tips": [
            'title:"Owner" OR title:"General Manager" industry:"HVAC"',
            'title:"Practice Administrator" healthcare location:"Austin"',
            'title:"Operations Manager" industry:"Pool Service"'
        ],
        "buying_signals": [
            "Recently posted job for admin/front desk staff",
            "Mentioned growth or expansion in recent posts",
            "Complained about being too busy on social media",
            "Asking for software recommendations in industry groups",
            "Responding to competitors' ads about automation"
        ],
        "pain_trigger_events": [
            "Seasonal spike starting (HVAC in summer, roofing after storms)",
            "Recent bad reviews mentioning responsiveness",
            "Staff turnover (admin positions advertised)",
            "New competitor opened nearby",
            "Raised prices (signal of demand exceeding capacity)"
        ]
    }
    
    # Outreach Templates
    outreach_framework = {
        "cold_email_structure": {
            "subject_line": "Quick question about [specific pain point]",
            "line_1": "I noticed [specific observation about their business]",
            "line_2": "Most [industry] owners lose [specific $ amount] monthly to [pain point]",
            "line_3": "We built an AI system that [specific outcome] for [competitor/similar business]",
            "cta": "Worth a 15-min call to see if it fits your operation?"
        },
        "linkedin_outreach": {
            "connection_note": "Hi [Name], connecting with [industry] owners in [city]. Love what you're doing at [company].",
            "followup_after_accept": "Thanks for connecting! I work with [industry] companies to [outcome]. Seeing similar challenges?",
            "value_share": "Just created a guide on [industry pain point]. Want me to send it over?"
        },
        "call_script_opener": "Hi [Name], this is [You] - calling [industry] owners about [pain point]. Bad time? [If no] Quick context: we help [industry] companies [outcome]. Sound relevant?"
    }
    
    # Pricing Strategy Based on Research
    pricing_models = {
        "service_retainer_model": {
            "setup_fee": "$1,500-$5,000 one-time",
            "monthly_retainer": "$1,500-$5,000/month",
            "justification": "Client value is $10K-$50K monthly revenue impact",
            "payment_terms": "50% upfront, 50% on completion, then monthly recurring",
            "typical_contract": "6-12 months minimum"
        },
        "performance_based_model": {
            "base_retainer": "$500-$1,000/month",
            "success_fee": "10-20% of revenue generated or saved",
            "example": "HVAC: $1K base + $500/booked job over baseline",
            "risk": "Requires tight tracking and trust"
        },
        "value_based_pricing": {
            "approach": "If we save you $30K/year in missed calls, we charge $5K/year ($417/mo)",
            "conversion_rate": "60-80% when value is clear and measurable"
        }
    }
    
    # Market Size & Opportunity Analysis
    market_intelligence = {
        "total_addressable_market": {
            "global_ai_spending_2025": "$1.48 trillion (Gartner)",
            "customer_service_ai_segment": "$243.7B in 2025, growing to $826.7B by 2030",
            "ai_automation_agency_space": "Under-penetrated in boring verticals"
        },
        "competitive_landscape": {
            "enterprise_focused": "Most AI agencies chase Fortune 500",
            "tech_savvy_verticals": "SaaS, ecommerce, agencies already saturated",
            "blue_ocean_niches": "HVAC, dental, roofing, tree removal = minimal AI competition",
            "your_advantage": "First-mover in local service businesses"
        },
        "success_metrics_to_track": {
            "client_acquisition_cost": "$500-$2,000 (cold outreach + demo)",
            "lifetime_value": "$18K-$60K (12-month average)",
            "ltv_cac_ratio": "9:1 to 30:1 (excellent)",
            "time_to_first_dollar": "2-4 weeks with aggressive outreach",
            "monthly_revenue_at_scale": "$10K-$50K with 5-10 clients"
        }
    }
    
    # Path to $100K/Month Target
    scaling_roadmap = {
        "month_1_3": {
            "goal": "Land 2-3 pilot clients at $1,500-$3,000/mo",
            "revenue": "$4,500-$9,000/month",
            "actions": [
                "Pick ONE niche to start (HVAC recommended - highest pain)",
                "Build 1-2 case studies (even if discounted)",
                "Create outreach list of 100 prospects in target city",
                "Book 10-15 calls, close 2-3 deals"
            ]
        },
        "month_4_6": {
            "goal": "Scale to 5-7 clients, refine delivery",
            "revenue": "$10K-$20K/month",
            "actions": [
                "Systematize delivery (templates, playbooks)",
                "Add second niche or expand geography",
                "Hire VA to handle onboarding ($500-$1K/mo)",
                "Build referral program (20% finder's fee)"
            ]
        },
        "month_7_12": {
            "goal": "Reach $50K-$100K/month",
            "options": [
                "Option A: 15-20 clients at $3K-$5K/month (service model)",
                "Option B: 10 clients + 2-3 higher-ticket enterprise deals ($10K-$20K/mo)",
                "Option C: Productize your service into SaaS ($100-$500/mo, 100-200 customers)"
            ],
            "team_needed": [
                "1-2 delivery specialists ($3K-$5K/mo each)",
                "1 SDR for outbound ($2K-$4K/mo + commission)",
                "You focus on sales and client strategy"
            ]
        },
        "reality_check": {
            "achievable": "Yes, with focus and execution",
            "bottleneck": "Your sales ability and niche clarity",
            "time_investment": "60-80 hours/week months 1-6, then 40-50 with team",
            "biggest_risk": "Trying to serve everyone instead of dominating one niche"
        }
    }
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "analysis": "AI Agency Lead Generation Opportunity Scanner",
        "target_market": {
            "city": target_city,
            "min_business_revenue": min_revenue,
            "focus_area": focus
        },
        "top_7_niches": high_ticket_niches,
        "decision_maker_research": decision_maker_intel,
        "outreach_templates": outreach_framework,
        "pricing_strategy": pricing_models,
        "market_intelligence": market_intelligence,
        "path_to_100k_monthly": scaling_roadmap,
        "key_insights": [
            "Local service businesses have highest pain + budget + low competition",
            "Average retainer: $1,500-$5,000/month per client",
            "LTV:CAC ratio of 9:1 to 30:1 is exceptional",
            "HVAC, dental, and roofing are top 3 niches for immediate traction",
            "Decision-makers are owners/GMs who value time over money",
            "Budget signals: Google Ads spend, multiple locations, staff hiring",
            "First-mover advantage in boring industries with high margins",
            "10-20 clients at $3K-$5K/mo = $30K-$100K/month revenue",
            "Setup fees ($1.5K-$5K) provide immediate cash flow",
            "Referrals are powerful - these industries have tight networks"
        ],
        "immediate_action_steps": [
            "1. Pick ONE niche (recommend HVAC for highest pain + budget)",
            "2. Build list of 100 prospects using Google Maps + LinkedIn",
            "3. Create 1-page offer doc with clear outcome and pricing",
            "4. Send 25 cold emails per day for 2 weeks",
            "5. Book 10 calls, aim to close 2-3 pilot clients",
            "6. Deliver results, get testimonial, then scale outreach",
            "7. Hire VA to handle admin once you hit $10K/month",
            "8. Add second niche or geography at $20K/month",
            "9. Build team and systemize at $30K-$50K/month",
            "10. Consider SaaS productization at $50K+ to reduce delivery labor"
        ]
    }
