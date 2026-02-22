#!/usr/bin/env python3
"""
Unified Opportunity Scorer V2
Ranks ALL opportunities from all scanners using consistent criteria.
"""

import json
from datetime import datetime
from typing import Dict, List, Any


def load_all_opportunities() -> List[Dict[str, Any]]:
    """Load and normalize opportunities from all scanner outputs."""
    all_opps = []
    
    # 1. Viral Trends
    try:
        with open('data/viral_trends_20260221.json') as f:
            viral_data = json.load(f)
        for trend in viral_data.get('all_trends', []):
            all_opps.append({
                'source': 'viral_trend',
                'title': trend.get('topic', trend.get('trend', 'Unknown')),
                'platform': trend.get('platform', ''),
                'category': trend.get('category', ''),
                'viral_score': trend.get('viral_score', 0),
                'volume': trend.get('volume', 0),
                'growth_rate': trend.get('growth_rate', ''),
                'market_size': trend.get('market_size', ''),
                'competition': trend.get('competition', ''),
                'revenue_potential': trend.get('revenue_potential', ''),
                'raw': trend
            })
        print(f"Loaded {len(all_opps)} viral trends")
    except Exception as e:
        print(f"Error loading viral trends: {e}")
    
    # 2. AI Agency Leads
    try:
        with open('data/ai_agency_leads_20260221.json') as f:
            agency_data = json.load(f)
        for seg_name, seg_data in agency_data.get('lead_segments', {}).items():
            if isinstance(seg_data, dict):
                all_opps.append({
                    'source': 'ai_agency_lead',
                    'title': seg_name,
                    'urgency_score': seg_data.get('urgency_score', 0),
                    'market_size': seg_data.get('market_size', 0),
                    'budget': seg_data.get('budget', ''),
                    'timeline': seg_data.get('timeline', ''),
                    'raw': seg_data
                })
        print(f"Loaded {len([o for o in all_opps if o['source'] == 'ai_agency_lead'])} agency leads")
    except Exception as e:
        print(f"Error loading agency leads: {e}")
    
    # 3. Pricing Gaps
    try:
        with open('data/enterprise_pricing_20260221.json') as f:
            pricing_data = json.load(f)
        for gap in pricing_data.get('all_opportunities', []):
            # Parse TAM
            tam_str = gap.get('tam', '0')
            tam_millions = 0
            try:
                if 'B' in tam_str:
                    tam_millions = float(tam_str.replace('$', '').replace('B TAM', '').strip()) * 1000
                elif 'M' in tam_str:
                    tam_millions = float(tam_str.replace('$', '').replace('M TAM', '').strip())
            except:
                pass
            
            all_opps.append({
                'source': 'pricing_gap',
                'title': gap.get('solution', 'Unknown'),
                'category': gap.get('category', ''),
                'tam_millions': tam_millions,
                'opportunity_score': gap.get('opportunity_score', 0),
                'entry_difficulty': gap.get('entry_difficulty', 'Medium'),
                'moats': len(gap.get('competitive_moats', [])),
                'raw': gap
            })
        print(f"Loaded {len([o for o in all_opps if o['source'] == 'pricing_gap'])} pricing gaps")
    except Exception as e:
        print(f"Error loading pricing gaps: {e}")
    
    # 4. Validated SaaS
    try:
        with open('data/micro_saas_validation_20260221.json') as f:
            validation_data = json.load(f)
        for opp in validation_data.get('rankings', []):
            market_data = opp.get('market_data', {})
            tam_millions = market_data.get('market_opportunity', 0) / 1000000
            
            all_opps.append({
                'source': 'validated_saas',
                'title': opp.get('idea_name', 'Unknown'),
                'validation_score': opp.get('weighted_score', 0),
                'go_decision': opp.get('go_decision', {}).get('decision', ''),
                'tam_millions': tam_millions,
                'risk_profile': opp.get('risk_profile', {}).get('overall', ''),
                'raw': opp
            })
        print(f"Loaded {len([o for o in all_opps if o['source'] == 'validated_saas'])} validated ideas")
    except Exception as e:
        print(f"Error loading validated SaaS: {e}")
    
    return all_opps


def score_opportunity(opp: Dict[str, Any]) -> float:
    """
    Universal scoring (0-100 scale).
    Weights adjusted per source type.
    """
    source = opp['source']
    score = 0.0
    
    if source == 'viral_trend':
        # Viral score is already 0-100
        viral = opp.get('viral_score', 0)
        # Adjust for competition
        comp = opp.get('competition', 'High')
        if comp == 'Low':
            score = viral * 1.1  # Bonus
        elif comp == 'High':
            score = viral * 0.9  # Penalty
        else:
            score = viral
            
    elif source == 'ai_agency_lead':
        # Based on urgency score
        urgency = opp.get('urgency_score', 0)
        score = urgency * 0.85  # Slight penalty (service business)
        
    elif source == 'pricing_gap':
        # Use opportunity score from pricing tracker
        opp_score = opp.get('opportunity_score', 0)
        # Scale from 0-30 to 0-100
        score = (opp_score / 30) * 100
        
    elif source == 'validated_saas':
        # Use validation score directly (already 0-100)
        score = opp.get('validation_score', 0)
    
    return min(round(score, 1), 100.0)


def rank_opportunities(opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Score and rank all opportunities."""
    
    # Score each
    for opp in opportunities:
        opp['unified_score'] = score_opportunity(opp)
    
    # Sort by score
    ranked = sorted(opportunities, key=lambda x: x['unified_score'], reverse=True)
    
    # Statistics
    stats = {
        'total': len(ranked),
        'average_score': round(sum(o['unified_score'] for o in ranked) / len(ranked), 1) if ranked else 0,
        'by_source': {},
        'score_bands': {
            'excellent_80plus': len([o for o in ranked if o['unified_score'] >= 80]),
            'strong_70to79': len([o for o in ranked if 70 <= o['unified_score'] < 80]),
            'good_60to69': len([o for o in ranked if 60 <= o['unified_score'] < 70]),
            'moderate_50to59': len([o for o in ranked if 50 <= o['unified_score'] < 60]),
            'weak_below50': len([o for o in ranked if o['unified_score'] < 50])
        }
    }
    
    # By source stats
    for opp in ranked:
        src = opp['source']
        if src not in stats['by_source']:
            stats['by_source'][src] = {'count': 0, 'avg_score': 0, 'scores': []}
        stats['by_source'][src]['count'] += 1
        stats['by_source'][src]['scores'].append(opp['unified_score'])
    
    for src in stats['by_source']:
        scores = stats['by_source'][src]['scores']
        stats['by_source'][src]['avg_score'] = round(sum(scores) / len(scores), 1)
        del stats['by_source'][src]['scores']
    
    return {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'statistics': stats,
        'ranked_opportunities': ranked
    }


def generate_markdown_report(results: Dict[str, Any]) -> str:
    """Generate comprehensive report."""
    md = []
    
    md.append("# Unified Opportunity Intelligence Report")
    md.append(f"\nGenerated: {results['generated_at']}\n")
    md.append("---\n")
    
    stats = results['statistics']
    
    md.append("## Executive Summary\n")
    md.append(f"**Total Opportunities Analyzed:** {stats['total']}")
    md.append(f"**Average Score:** {stats['average_score']}/100")
    if results['ranked_opportunities']:
        md.append(f"**Top Score:** {results['ranked_opportunities'][0]['unified_score']}/100 - {results['ranked_opportunities'][0]['title']}\n")
    
    md.append("### Score Distribution\n")
    bands = stats['score_bands']
    md.append(f"- **Excellent (80+):** {bands['excellent_80plus']} opportunities")
    md.append(f"- **Strong (70-79):** {bands['strong_70to79']} opportunities")
    md.append(f"- **Good (60-69):** {bands['good_60to69']} opportunities")
    md.append(f"- **Moderate (50-59):** {bands['moderate_50to59']} opportunities")
    md.append(f"- **Weak (<50):** {bands['weak_below50']} opportunities\n")
    
    md.append("### By Source\n")
    source_names = {
        'viral_trend': 'Viral Trends',
        'ai_agency_lead': 'AI Agency Leads',
        'pricing_gap': 'Pricing Gaps',
        'validated_saas': 'Validated SaaS Ideas'
    }
    for src, data in stats['by_source'].items():
        md.append(f"- **{source_names.get(src, src)}:** {data['count']} opportunities (avg: {data['avg_score']}/100)")
    md.append("\n---\n")
    
    md.append("## Top 15 Ranked Opportunities\n")
    for i, opp in enumerate(results['ranked_opportunities'][:15], 1):
        md.append(f"### {i}. {opp['title']} - {opp['unified_score']}/100\n")
        md.append(f"**Source:** {source_names.get(opp['source'], opp['source'])}\n")
        
        if opp['source'] == 'viral_trend':
            md.append(f"- **Platform:** {opp.get('platform', 'N/A')}")
            md.append(f"- **Category:** {opp.get('category', 'N/A')}")
            md.append(f"- **Viral Score:** {opp.get('viral_score', 0)}/100")
            md.append(f"- **Growth:** {opp.get('growth_rate', 'N/A')}")
            md.append(f"- **Competition:** {opp.get('competition', 'N/A')}")
            md.append(f"- **Revenue Potential:** {opp.get('revenue_potential', 'N/A')}\n")
            
        elif opp['source'] == 'ai_agency_lead':
            md.append(f"- **Urgency Score:** {opp.get('urgency_score', 0)}/100")
            md.append(f"- **Market Size:** {opp.get('market_size', 0):,} businesses")
            md.append(f"- **Budget Range:** {opp.get('budget', 'N/A')}")
            md.append(f"- **Timeline:** {opp.get('timeline', 'N/A')}\n")
            
        elif opp['source'] == 'pricing_gap':
            md.append(f"- **Category:** {opp.get('category', 'N/A')}")
            md.append(f"- **TAM:** ${opp.get('tam_millions', 0):,.0f}M")
            md.append(f"- **Entry Difficulty:** {opp.get('entry_difficulty', 'N/A')}")
            md.append(f"- **Moat Strategies:** {opp.get('moats', 0)}\n")
            
        elif opp['source'] == 'validated_saas':
            md.append(f"- **Validation Score:** {opp.get('validation_score', 0)}/100")
            md.append(f"- **Decision:** {opp.get('go_decision', 'N/A')}")
            md.append(f"- **TAM:** ${opp.get('tam_millions', 0):,.0f}M")
            md.append(f"- **Risk Profile:** {opp.get('risk_profile', 'N/A')}\n")
        
        md.append("---\n")
    
    # Remaining opportunities table
    if len(results['ranked_opportunities']) > 15:
        md.append(f"## Remaining {len(results['ranked_opportunities']) - 15} Opportunities\n")
        md.append("| Rank | Title | Source | Score |\n")
        md.append("|------|-------|--------|-------|\n")
        for i, opp in enumerate(results['ranked_opportunities'][15:], 16):
            md.append(f"| {i} | {opp['title']} | {source_names.get(opp['source'], opp['source'])} | {opp['unified_score']}/100 |\n")
    
    return '\n'.join(md)


if __name__ == '__main__':
    print("Starting unified opportunity scorer v2...\n")
    
    # Load all opportunities
    opportunities = load_all_opportunities()
    print(f"\nTotal loaded: {len(opportunities)} opportunities\n")
    
    # Rank them
    results = rank_opportunities(opportunities)
    
    # Save JSON
    json_path = 'data/unified_opportunity_ranking_20260221.json'
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved JSON: {json_path}")
    
    # Generate and save Markdown
    report = generate_markdown_report(results)
    md_path = 'data/unified_opportunity_ranking_20260221.md'
    with open(md_path, 'w') as f:
        f.write(report)
    print(f"Saved Markdown: {md_path}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"UNIFIED OPPORTUNITY SCORING COMPLETE")
    print(f"{'='*60}")
    print(f"Total Opportunities: {results['statistics']['total']}")
    print(f"Average Score: {results['statistics']['average_score']}/100")
    print(f"\nTOP 5 OPPORTUNITIES:")
    for i, opp in enumerate(results['ranked_opportunities'][:5], 1):
        print(f"{i}. {opp['title'][:50]:<50} {opp['unified_score']:>5.1f}/100 ({opp['source']})")
    print(f"{'='*60}\n")
