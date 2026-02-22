#!/usr/bin/env python3
"""
Nebula Newsletter Sender Integration

This script orchestrates the actual sending of newsletters via Nebula's send_email tool.
It loads the newsletter draft and subscriber list, then outputs structured data for 
the orchestrator to call send_email for each recipient.

Usage:
    python send_newsletter.py                    # Send to all subscribers
    python send_newsletter.py --test             # Send only to test address  
    python send_newsletter.py --issue 3          # Send specific issue number
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class NebulaNewsletterSender:
    """Prepares newsletter data for sending via Nebula's send_email tool."""
    
    def __init__(self, base_dir: str = "/home/user/files"):
        self.base_dir = Path(base_dir)
        self.drafts_dir = self.base_dir / "outputs" / "newsletter-drafts"
        self.deliveries_dir = self.base_dir / "outputs" / "newsletter-deliveries"
        self.subscribers_file = self.base_dir / "data" / "newsletter-subscribers.json"
        self.test_recipient = "hax@mailinator.com"
        
        # Create deliveries directory
        self.deliveries_dir.mkdir(parents=True, exist_ok=True)
    
    def find_latest_draft(self, issue_number: int = None):
        """Find the latest newsletter HTML draft."""
        if not self.drafts_dir.exists():
            raise FileNotFoundError(f"Drafts directory not found: {self.drafts_dir}")
        
        if issue_number:
            html_files = list(self.drafts_dir.glob(f"*_{issue_number}.html"))
        else:
            html_files = list(self.drafts_dir.glob("edge_finder_*.html"))
        
        if not html_files:
            raise FileNotFoundError("No newsletter drafts found")
        
        latest_html = max(html_files, key=lambda p: p.stat().st_mtime)
        meta_path = latest_html.with_name(latest_html.stem + "_meta.json")
        
        return latest_html, meta_path
    
    def load_draft(self, html_path: Path, meta_path: Path) -> Dict:
        """Load newsletter content and metadata."""
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        issue_num = metadata.get('issue_number', '?')
        headline = metadata.get('top_story', {}).get('headline', 'Latest Opportunities')
        subject = f"Edge Finder #{issue_num} - {headline[:60]}"
        
        return {
            'html': html_content,
            'subject': subject,
            'issue_number': issue_num,
            'headline': headline,
            'date': metadata.get('generated_at'),
            'metadata': metadata
        }
    
    def load_subscribers(self) -> List[str]:
        """Load active subscriber emails."""
        if not self.subscribers_file.exists():
            return [self.test_recipient]
        
        with open(self.subscribers_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [
            sub['email'] 
            for sub in data.get('subscribers', [])
            if sub.get('status') == 'active'
        ]
    
    def prepare_sends(self, test_mode: bool = False, issue_number: int = None) -> Dict:
        """
        Prepare newsletter send data for Nebula orchestrator.
        
        Returns structured data with:
        - newsletter content
        - list of recipients
        - subject line
        - metadata
        """
        # Find and load draft
        html_path, meta_path = self.find_latest_draft(issue_number)
        draft = self.load_draft(html_path, meta_path)
        
        # Load subscribers
        subscribers = self.load_subscribers()
        if test_mode:
            subscribers = [self.test_recipient]
        
        return {
            'subject': draft['subject'],
            'html_body': draft['html'],
            'recipients': subscribers,
            'issue_number': draft['issue_number'],
            'headline': draft['headline'],
            'timestamp': datetime.now().isoformat(),
            'test_mode': test_mode
        }

def main():
    """Main execution - outputs structured JSON for orchestrator."""
    parser = argparse.ArgumentParser(description='Prepare newsletter for sending')
    parser.add_argument('--test', action='store_true', help='Test mode - single recipient')
    parser.add_argument('--issue', type=int, help='Specific issue number')
    
    args = parser.parse_args()
    
    try:
        sender = NebulaNewsletterSender()
        send_data = sender.prepare_sends(test_mode=args.test, issue_number=args.issue)
        
        # Output structured data for orchestrator
        print("\n" + "="*70)
        print("NEWSLETTER SEND DATA")
        print("="*70)
        print(json.dumps(send_data, indent=2))
        print("\n" + "="*70)
        print(f"Ready to send to {len(send_data['recipients'])} recipients")
        print("="*70)
        
        return send_data
        
    except Exception as e:
        print(f"Error preparing newsletter: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
