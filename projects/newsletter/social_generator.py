#!/usr/bin/env python3
"""
Edge Finder Social Media Content Generator
Extracts newsletter highlights and generates platform-specific social content
"""

import json
import os
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsletterExtractor:
    """Extract key insights from newsletter markdown and metadata"""
    
    def __init__(self, newsletter_path: Path, meta_path: Path):
        self.newsletter_path = newsletter_path
        self.meta_path = meta_path
        self.content = self._load_newsletter()
        self.metadata = self._load_metadata()
    
    def _load_newsletter(self) -> str:
        """Load newsletter markdown content"""
        with open(self.newsletter_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_metadata(self) -> Dict:
        """Load newsletter metadata"""
        with open(self.meta_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_header(self) -> Dict[str, str]:
        """Extract newsletter header info"""
        date_match = re.search(r'📅 ([\d-]+) \| Issue #(\d+)', self.content)
        return {
            'date': date_match.group(1) if date_match else '',
            'issue_number': date_match.group(2) if date_match else ''
        }
    
    def extract_the_edge(self) -> Optional[Dict[str, Any]]:
        """Extract main opportunity from THE EDGE section"""
        edge_pattern = r'🎯 THE EDGE\n\n(.*?)\n\nOpportunity Score: ([\d/]+)'
        match = re.search(edge_pattern, self.content, re.DOTALL)
        
        if not match:
            return None
        
        full_text = match.group(1)
        opp_score = match.group(2)
        
        # Extract title (first line)
        lines = full_text.strip().split('\n')
        title = lines[0] if lines else "Market Opportunity"
        
        # Extract What/Why/How if present
        what_match = re.search(r'What: (.*?)(?:\n|$)', self.content)
        why_match = re.search(r'Why now: (.*?)(?:\n|$)', self.content)
        how_match = re.search(r'How to play: (.*?)(?:\n|$)', self.content)
        
        return {
            'title': title,
            'score': opp_score,
            'what': what_match.group(1) if what_match else '',
            'why': why_match.group(1) if why_match else '',
            'how': how_match.group(1) if how_match else '',
            'full_text': full_text
        }
    
    def extract_signals(self) -> List[Dict[str, str]]:
        """Extract signal items from SIGNALS section"""
        signals = []
        
        # Pattern for signal items
        signal_pattern = r'(📰|⚙️|🔥|📊|💡) (.*?)\n(.*?)(?:\n→ (.*?))?(?=\n\n|\n📰|\n⚙️|\n🔥|\n📊|\n💡|🛠️ BUILDER BRIEF)'
        
        matches = re.finditer(signal_pattern, self.content, re.DOTALL)
        
        for match in matches:
            emoji = match.group(1)
            title = match.group(2).strip()
            description = match.group(3).strip()
            action = match.group(4).strip() if match.group(4) else ''
            
            signals.append({
                'emoji': emoji,
                'title': title,
                'description': description,
                'action': action
            })
        
        return signals[:4]  # Top 4 signals
    
    def extract_builder_brief(self) -> Optional[str]:
        """Extract builder insight"""
        brief_pattern = r'🛠️ BUILDER BRIEF\n\n(.*?)(?=\n\n👀 WHAT|$)'
        match = re.search(brief_pattern, self.content, re.DOTALL)
        
        if match:
            text = match.group(1).strip()
            # Clean up and extract key insight
            lines = [l for l in text.split('\n') if l.strip() and not l.startswith('[MANUAL')]
            return ' '.join(lines)
        return None
    
    def extract_action_items(self) -> List[str]:
        """Extract action items"""
        action_pattern = r'⚡ ACTION ITEMS\n\n(.*?)(?=\n\n💡|$)'
        match = re.search(action_pattern, self.content, re.DOTALL)
        
        if not match:
            return []
        
        items = []
        for line in match.group(1).split('\n'):
            if line.strip().startswith('→'):
                items.append(line.strip().lstrip('→ ').strip())
        
        return items


class SocialContentGenerator:
    """Generate platform-specific social media content"""
    
    def __init__(self, extractor: NewsletterExtractor):
        self.extractor = extractor
        self.header = extractor.extract_header()
        self.edge = extractor.extract_the_edge()
        self.signals = extractor.extract_signals()
        self.brief = extractor.extract_builder_brief()
        self.actions = extractor.extract_action_items()
    
    def generate_twitter_thread(self) -> List[Dict[str, Any]]:
        """Generate Twitter thread (280 chars per tweet)"""
        thread = []
        
        # Tweet 1: Hook
        hook = f"🔍 Edge Finder #{self.header['issue_number']} is live\n\n"
        if self.edge:
            hook += f"Today's play: {self.edge['title'][:100]}\n\n"
            hook += f"📊 Opportunity Score: {self.edge['score']}\n\n"
        hook += "Thread 🧵"
        
        thread.append({
            'tweet_number': 1,
            'content': hook[:280],
            'char_count': len(hook[:280])
        })
        
        # Tweet 2: The Edge (What + Why)
        if self.edge and self.edge.get('what'):
            edge_tweet = f"What: {self.edge['what']}\n\n"
            if self.edge.get('why'):
                edge_tweet += f"Why now: {self.edge['why'][:150]}"
            
            thread.append({
                'tweet_number': 2,
                'content': edge_tweet[:280],
                'char_count': len(edge_tweet[:280])
            })
        
        # Tweets 3-6: Top Signals (one per tweet)
        for idx, signal in enumerate(self.signals[:4], start=3):
            signal_tweet = f"{signal['emoji']} {signal['title']}\n\n"
            signal_tweet += signal['description'][:200]
            
            if signal.get('action'):
                signal_tweet += f"\n\n→ {signal['action']}"
            
            thread.append({
                'tweet_number': idx,
                'content': signal_tweet[:280],
                'char_count': len(signal_tweet[:280])
            })
        
        # CTA Tweet
        cta_idx = len(thread) + 1
        cta = "Want the full breakdown?\n\n"
        cta += "✅ Detailed market analysis\n"
        cta += "✅ Step-by-step playbooks\n"
        cta += "✅ Private builder community\n\n"
        cta += "Subscribe (FREE) → https://edgefinder.com\n"
        cta += "🎁 Bonus: 50 Validated Micro SaaS Ideas PDF"
        
        thread.append({
            'tweet_number': cta_idx,
            'content': cta[:280],
            'char_count': len(cta[:280])
        })
        
        # Premium upsell
        premium = f"Following Edge Finder has helped 500+ founders spot opportunities early.\n\n"
        premium += "Premium includes live Q&A, Discord access, and exclusive deal flow.\n\n"
        premium += "Start free → https://edgefinder.com\n"
        premium += "Upgrade later → https://edgefinder.com/premium\n\n"
        premium += "#BuildInPublic #Founders #OpportunityScanner"
        
        thread.append({
            'tweet_number': cta_idx + 1,
            'content': premium[:280],
            'char_count': len(premium[:280])
        })
        
        return thread
    
    def generate_linkedin_post(self) -> Dict[str, Any]:
        """Generate LinkedIn post (1200-1500 chars)"""
        post = f"🔍 Edge Finder Weekly Intelligence - Issue #{self.header['issue_number']}\n\n"
        
        # Opening hook
        if self.edge:
            post += f"This week's market opportunity: {self.edge['title']}\n"
            post += f"Score: {self.edge['score']} | "
            post += f"Analysis based on automated market scanning.\n\n"
        
        # Key insights header
        post += "━━━━━━━━━━━━━━━━━━━━\n"
        post += "KEY MARKET SIGNALS\n"
        post += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Top 3 signals
        for idx, signal in enumerate(self.signals[:3], start=1):
            post += f"{idx}. {signal['title']}\n"
            post += f"{signal['description'][:150]}\n"
            if signal.get('action'):
                post += f"→ {signal['action']}\n"
            post += "\n"
        
        # Builder insight
        if self.brief:
            post += "━━━━━━━━━━━━━━━━━━━━\n"
            post += "BUILDER TAKEAWAY\n"
            post += "━━━━━━━━━━━━━━━━━━━━\n\n"
            post += f"{self.brief[:200]}\n\n"
        
        # Value prop
        post += "Edge Finder combines automated market scanning with human analysis "
        post += "to surface mispriced opportunities before they hit mainstream radar.\n\n"
        
        # CTA
        post += "📬 Subscribe (FREE): https://edgefinder.com\n"
        post += "🎁 Instant bonus: 50 Validated Micro SaaS Ideas PDF\n"
        post += "💎 Premium access: https://edgefinder.com/premium\n\n"
        
        # Hashtags
        post += "#Entrepreneurship #MarketIntelligence #Startups #BusinessOpportunities #BuildInPublic"
        
        return {
            'content': post[:3000],  # LinkedIn limit
            'char_count': len(post[:3000]),
            'hashtags': ['Entrepreneurship', 'MarketIntelligence', 'Startups', 'BusinessOpportunities', 'BuildInPublic']
        }
    
    def generate_instagram_caption(self) -> Dict[str, Any]:
        """Generate Instagram/Threads caption"""
        caption = f"🔍 Edge Finder #{self.header['issue_number']}\n"
        caption += f"Market intelligence for builders\n\n"
        
        if self.edge:
            caption += f"THIS WEEK: {self.edge['title'][:80]}\n"
            caption += f"📊 Opportunity Score: {self.edge['score']}\n\n"
        
        caption += "🔥 TOP SIGNALS:\n"
        for signal in self.signals[:3]:
            caption += f"{signal['emoji']} {signal['title'][:50]}\n"
        
        caption += "\n"
        caption += "Automated scanners + human insights = Early mover advantage\n\n"
        caption += "Subscribe FREE → edgefinder.com\n"
        caption += "🎁 Get 50 Micro SaaS Ideas PDF\n\n"
        
        hashtags = "#EdgeFinder #BuildInPublic #Founders #StartupOpportunities "
        hashtags += "#MarketIntelligence #Entrepreneurship #BusinessIdeas #OpportunityScanner"
        
        caption += hashtags
        
        return {
            'content': caption[:2200],  # Instagram limit
            'char_count': len(caption[:2200]),
            'hashtags': ['EdgeFinder', 'BuildInPublic', 'Founders', 'StartupOpportunities', 
                        'MarketIntelligence', 'Entrepreneurship', 'BusinessIdeas', 'OpportunityScanner']
        }
    
    def generate_all_content(self) -> Dict[str, Any]:
        """Generate content for all platforms"""
        return {
            'generated_at': datetime.now().isoformat(),
            'newsletter_issue': self.header['issue_number'],
            'newsletter_date': self.header['date'],
            'platforms': {
                'twitter': {
                    'thread': self.generate_twitter_thread(),
                    'total_tweets': len(self.generate_twitter_thread())
                },
                'linkedin': self.generate_linkedin_post(),
                'instagram': self.generate_instagram_caption()
            },
            'source_data': {
                'opportunity_score': self.edge['score'] if self.edge else 'N/A',
                'signals_count': len(self.signals),
                'has_builder_brief': bool(self.brief)
            }
        }


class SocialOutputGenerator:
    """Generate output files in multiple formats"""
    
    def __init__(self, content: Dict[str, Any], output_dir: Path):
        self.content = content
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        date = content['newsletter_date']
        self.base_filename = f"social_{date}"
    
    def save_json(self) -> Path:
        """Save complete JSON output"""
        json_path = self.output_dir / f"{self.base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.content, f, indent=2, ensure_ascii=False)
        return json_path
    
    def save_twitter_txt(self) -> Path:
        """Save Twitter thread as plain text for copy-paste"""
        txt_path = self.output_dir / f"{self.base_filename}_twitter.txt"
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("TWITTER THREAD - EDGE FINDER\n")
            f.write("=" * 60 + "\n\n")
            
            for tweet in self.content['platforms']['twitter']['thread']:
                f.write(f"Tweet {tweet['tweet_number']} ({tweet['char_count']} chars):\n")
                f.write("-" * 60 + "\n")
                f.write(tweet['content'] + "\n")
                f.write("-" * 60 + "\n\n")
        
        return txt_path
    
    def save_linkedin_txt(self) -> Path:
        """Save LinkedIn post as plain text"""
        txt_path = self.output_dir / f"{self.base_filename}_linkedin.txt"
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("LINKEDIN POST - EDGE FINDER\n")
            f.write("=" * 60 + "\n\n")
            
            linkedin = self.content['platforms']['linkedin']
            f.write(f"Character count: {linkedin['char_count']}\n\n")
            f.write(linkedin['content'] + "\n")
        
        return txt_path
    
    def save_instagram_txt(self) -> Path:
        """Save Instagram caption as plain text"""
        txt_path = self.output_dir / f"{self.base_filename}_instagram.txt"
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("INSTAGRAM/THREADS CAPTION - EDGE FINDER\n")
            f.write("=" * 60 + "\n\n")
            
            instagram = self.content['platforms']['instagram']
            f.write(f"Character count: {instagram['char_count']}\n\n")
            f.write(instagram['content'] + "\n")
        
        return txt_path
    
    def save_markdown_preview(self) -> Path:
        """Save markdown preview of all platforms"""
        md_path = self.output_dir / f"{self.base_filename}_preview.md"
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Edge Finder Social Media Content\n\n")
            f.write(f"**Issue:** #{self.content['newsletter_issue']}\n")
            f.write(f"**Date:** {self.content['newsletter_date']}\n")
            f.write(f"**Generated:** {self.content['generated_at']}\n\n")
            
            f.write("---\n\n")
            
            # Twitter section
            f.write("## Twitter Thread\n\n")
            f.write(f"**Total tweets:** {self.content['platforms']['twitter']['total_tweets']}\n\n")
            
            for tweet in self.content['platforms']['twitter']['thread']:
                f.write(f"### Tweet {tweet['tweet_number']}\n")
                f.write(f"*{tweet['char_count']} characters*\n\n")
                f.write("```\n")
                f.write(tweet['content'])
                f.write("\n```\n\n")
            
            f.write("---\n\n")
            
            # LinkedIn section
            f.write("## LinkedIn Post\n\n")
            linkedin = self.content['platforms']['linkedin']
            f.write(f"*{linkedin['char_count']} characters*\n\n")
            f.write("```\n")
            f.write(linkedin['content'])
            f.write("\n```\n\n")
            
            f.write("---\n\n")
            
            # Instagram section
            f.write("## Instagram/Threads Caption\n\n")
            instagram = self.content['platforms']['instagram']
            f.write(f"*{instagram['char_count']} characters*\n\n")
            f.write("```\n")
            f.write(instagram['content'])
            f.write("\n```\n\n")
        
        return md_path
    
    def save_all(self) -> Dict[str, Path]:
        """Save all output formats"""
        return {
            'json': self.save_json(),
            'twitter_txt': self.save_twitter_txt(),
            'linkedin_txt': self.save_linkedin_txt(),
            'instagram_txt': self.save_instagram_txt(),
            'markdown_preview': self.save_markdown_preview()
        }


def find_latest_newsletter(base_path: Path) -> tuple[Optional[Path], Optional[Path]]:
    """Find the latest newsletter markdown and metadata files"""
    drafts_dir = base_path / "outputs" / "newsletter-drafts"
    
    if not drafts_dir.exists():
        logger.error(f"Newsletter drafts directory not found: {drafts_dir}")
        return None, None
    
    # Find all newsletter markdown files
    md_files = list(drafts_dir.glob("edge_finder_*.md"))
    
    if not md_files:
        logger.error("No newsletter files found")
        return None, None
    
    # Get most recent
    latest_md = max(md_files, key=lambda p: p.stat().st_mtime)
    
    # Find corresponding metadata file
    base_name = latest_md.stem
    meta_file = drafts_dir / f"{base_name}_meta.json"
    
    if not meta_file.exists():
        logger.warning(f"Metadata file not found: {meta_file}")
        return latest_md, None
    
    return latest_md, meta_file


def main():
    parser = argparse.ArgumentParser(
        description='Generate social media content from Edge Finder newsletter'
    )
    parser.add_argument(
        '--newsletter',
        type=str,
        help='Path to newsletter markdown file (default: latest)'
    )
    parser.add_argument(
        '--metadata',
        type=str,
        help='Path to newsletter metadata JSON (default: auto-detect)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs/social-content',
        help='Output directory for social content (default: outputs/social-content)'
    )
    parser.add_argument(
        '--platforms',
        nargs='+',
        choices=['twitter', 'linkedin', 'instagram', 'all'],
        default=['all'],
        help='Platforms to generate content for (default: all)'
    )
    parser.add_argument(
        '--base-path',
        type=str,
        default='.',
        help='Base path for newsletter system (default: current directory)'
    )
    
    args = parser.parse_args()
    
    base_path = Path(args.base_path)
    
    # Find newsletter files
    if args.newsletter:
        newsletter_path = Path(args.newsletter)
        metadata_path = Path(args.metadata) if args.metadata else None
    else:
        logger.info("Finding latest newsletter...")
        newsletter_path, metadata_path = find_latest_newsletter(base_path)
        
        if not newsletter_path:
            logger.error("No newsletter found")
            return 1
        
        logger.info(f"Found newsletter: {newsletter_path.name}")
    
    if not newsletter_path.exists():
        logger.error(f"Newsletter file not found: {newsletter_path}")
        return 1
    
    if not metadata_path or not metadata_path.exists():
        logger.error(f"Metadata file not found: {metadata_path}")
        return 1
    
    # Extract content
    logger.info("Extracting newsletter content...")
    extractor = NewsletterExtractor(newsletter_path, metadata_path)
    
    # Generate social content
    logger.info("Generating social media content...")
    generator = SocialContentGenerator(extractor)
    
    # Filter platforms if specified
    content = generator.generate_all_content()
    
    if 'all' not in args.platforms:
        filtered_platforms = {
            k: v for k, v in content['platforms'].items() 
            if k in args.platforms
        }
        content['platforms'] = filtered_platforms
    
    # Save outputs
    output_dir = Path(args.output_dir)
    logger.info(f"Saving outputs to {output_dir}...")
    
    output_gen = SocialOutputGenerator(content, output_dir)
    files = output_gen.save_all()
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("SOCIAL CONTENT GENERATED SUCCESSFULLY")
    logger.info("=" * 60)
    logger.info(f"Newsletter: Issue #{content['newsletter_issue']}")
    logger.info(f"Date: {content['newsletter_date']}")
    logger.info(f"\nPlatforms: {', '.join(content['platforms'].keys())}")
    
    if 'twitter' in content['platforms']:
        logger.info(f"Twitter: {content['platforms']['twitter']['total_tweets']} tweets")
    
    logger.info("\nOutput files:")
    for file_type, filepath in files.items():
        logger.info(f"  {file_type}: {filepath}")
    
    logger.info("\n✅ Copy content from .txt files and paste directly to platforms")
    logger.info("📋 View markdown preview for formatted overview")
    
    return 0


if __name__ == "__main__":
    exit(main())
