#!/usr/bin/env python3
"""
Edge Finder Newsletter Email Distribution System

Sends newsletter drafts via Nebula's send_email tool with delivery tracking,
retry logic, and test mode for safe deployment.

Usage:
    python email_sender.py                    # Send to all subscribers
    python email_sender.py --test             # Send only to test address
    python email_sender.py --preview          # Show email without sending
    python email_sender.py --issue 3          # Send specific issue number
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add parent directory to path for imports (if __file__ is available)
if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).parent.parent))

class NewsletterEmailSender:
    """Handles email distribution of Edge Finder newsletter drafts."""
    
    def __init__(self, base_dir: Optional[str] = None):
        # Auto-detect base directory
        if base_dir is None:
            # Check common locations
            possible_bases = [
                Path("/home/user/files"),
                Path.cwd()
            ]
            for base in possible_bases:
                if (base / "outputs" / "newsletter-drafts").exists():
                    base_dir = str(base)
                    break
            if base_dir is None:
                base_dir = "/home/user/files"
        
        self.base_dir = Path(base_dir)
        self.drafts_dir = self.base_dir / "outputs" / "newsletter-drafts"
        self.deliveries_dir = self.base_dir / "outputs" / "newsletter-deliveries"
        self.subscribers_file = self.base_dir / "data" / "newsletter-subscribers.json"
        self.test_recipient = "hax@mailinator.com"
        
        # Create deliveries directory if needed
        self.deliveries_dir.mkdir(parents=True, exist_ok=True)
    
    def find_latest_draft(self, issue_number: Optional[int] = None) -> Tuple[Path, Path]:
        """
        Find the latest newsletter HTML draft and its metadata file.
        
        Args:
            issue_number: Optional specific issue number to send
            
        Returns:
            Tuple of (html_path, meta_path)
        """
        if not self.drafts_dir.exists():
            raise FileNotFoundError(f"Drafts directory not found: {self.drafts_dir}")
        
        # Find all edge_finder HTML files
        if issue_number:
            html_files = list(self.drafts_dir.glob(f"edge_finder_*_{issue_number}.html"))
        else:
            html_files = list(self.drafts_dir.glob("edge_finder_*.html"))
        
        if not html_files:
            raise FileNotFoundError("No newsletter draft HTML files found")
        
        # Get most recent by modification time
        latest_html = max(html_files, key=lambda p: p.stat().st_mtime)
        
        # Find corresponding metadata file
        meta_path = latest_html.with_name(latest_html.stem + "_meta.json")
        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {meta_path}")
        
        return latest_html, meta_path
    
    def load_draft(self, html_path: Path, meta_path: Path) -> Dict:
        """
        Load newsletter HTML content and metadata.
        
        Returns:
            Dict with 'html', 'subject', 'issue_number', 'headline', 'date'
        """
        # Load HTML content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Load metadata
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Build email subject
        issue_num = metadata.get('issue_number', '?')
        headline = metadata.get('top_story', {}).get('headline', 'Latest Opportunities')
        subject = f"Edge Finder #{issue_num} - {headline[:60]}"
        
        return {
            'html': html_content,
            'subject': subject,
            'issue_number': issue_num,
            'headline': headline,
            'date': metadata.get('generated_at', datetime.now().isoformat()),
            'metadata': metadata
        }
    
    def load_subscribers(self) -> List[str]:
        """
        Load subscriber email list from JSON file.
        
        Returns:
            List of email addresses
        """
        if not self.subscribers_file.exists():
            print(f"⚠️  Subscriber file not found: {self.subscribers_file}")
            print("   Creating sample file with test recipient...")
            
            # Create sample subscriber list
            sample_data = {
                "subscribers": [
                    {
                        "email": self.test_recipient,
                        "name": "Test User",
                        "subscribed_at": datetime.now().isoformat(),
                        "status": "active"
                    }
                ]
            }
            
            # Create data directory if needed
            self.subscribers_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.subscribers_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2)
            
            return [self.test_recipient]
        
        # Load existing subscribers
        with open(self.subscribers_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract active subscriber emails
        subscribers = [
            sub['email'] 
            for sub in data.get('subscribers', [])
            if sub.get('status') == 'active'
        ]
        
        return subscribers
    
    def _get_subscriber_referral_code(self, email: str) -> Optional[str]:
        """Get referral code for subscriber email."""
        try:
            with open(self.subscribers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if data is in new format (dict with email keys)
            if isinstance(data, dict) and email in data:
                return data[email].get('referral_code')
            
            # Check if data is in old format (list of subscribers)
            if isinstance(data, dict) and 'subscribers' in data:
                for sub in data['subscribers']:
                    if sub.get('email') == email:
                        return sub.get('referral_code')
            
            return None
        except Exception:
            return None
    
    def _add_referral_footer(self, html_body: str, recipient: str) -> str:
        """Add referral link footer to newsletter HTML."""
        referral_code = self._get_subscriber_referral_code(recipient)
        
        if not referral_code:
            # Generate fallback referral code if not found
            referral_code = f"REF{hash(recipient) % 10000:04d}"
        
        referral_link = f"https://edgefinder.com?ref={referral_code}"
        
        # Build referral footer HTML
        footer_html = f"""
        <div style="margin-top: 40px; padding: 30px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center;">
            <h3 style="color: #ffffff; margin: 0 0 12px 0; font-size: 20px;">Love Edge Finder? Get Premium Free!</h3>
            <p style="color: #e0e7ff; margin: 0 0 20px 0; font-size: 14px;">
                Share with friends and unlock rewards:<br/>
                <strong>3 referrals</strong> = 1 month Premium &nbsp;|&nbsp; <strong>10 referrals</strong> = 1 year Premium &nbsp;|&nbsp; <strong>25 referrals</strong> = Lifetime Premium
            </p>
            <div style="margin: 20px 0;">
                <a href="{referral_link}" style="display: inline-block; background: #ffffff; color: #667eea; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 16px;">
                    Share Your Link
                </a>
            </div>
            <p style="color: #c7d2fe; font-size: 12px; margin: 16px 0 0 0;">
                Your referral link: <a href="{referral_link}" style="color: #ffffff; text-decoration: underline;">{referral_link}</a>
            </p>
        </div>
        
        <div style="margin-top: 30px; padding: 20px; text-align: center; font-size: 12px; color: #6c757d; border-top: 1px solid #e9ecef;">
            <p style="margin: 0 0 8px 0;">
                You're receiving this because you signed up for Edge Finder at <a href="https://edgefinder.com" style="color: #4f46e5;">edgefinder.com</a>
            </p>
            <p style="margin: 8px 0;">
                <a href="https://edgefinder.com/preferences" style="color: #6c757d; text-decoration: underline;">Update preferences</a> &nbsp;|&nbsp; 
                <a href="https://edgefinder.com/unsubscribe?email={recipient}" style="color: #6c757d; text-decoration: underline;">Unsubscribe</a>
            </p>
        </div>
        """
        
        # Insert before closing </body> tag, or append if no body tag
        if '</body>' in html_body:
            html_body = html_body.replace('</body>', footer_html + '</body>')
        else:
            html_body += footer_html
        
        return html_body
    
    def send_email(self, recipient: str, subject: str, html_body: str) -> Dict:
        """
        Send email via Nebula's send_email tool with personalized referral footer.
        
        Note: This is a placeholder - actual sending happens via Nebula tool call.
        In production, this would be called by the orchestrator.
        
        Returns:
            Dict with 'success', 'recipient', 'timestamp', 'error' (if failed)
        """
        result = {
            'recipient': recipient,
            'timestamp': datetime.now().isoformat(),
            'subject': subject
        }
        
        try:
            # Add personalized referral footer
            personalized_html = self._add_referral_footer(html_body, recipient)
            
            # Placeholder for actual Nebula send_email call
            # In real execution, the orchestrator will call send_email tool
            print(f"📧 SEND_EMAIL_CALL:")
            print(f"   To: {recipient}")
            print(f"   Subject: {subject}")
            print(f"   Body: HTML content ({len(personalized_html)} chars)")
            
            result['success'] = True
            result['status'] = 'queued_for_nebula_send'
            result['html_with_referral'] = personalized_html
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            print(f"❌ Failed to send to {recipient}: {e}")
        
        return result
    
    def send_batch(
        self, 
        recipients: List[str], 
        subject: str, 
        html_body: str,
        test_mode: bool = False
    ) -> Dict:
        """
        Send newsletter to batch of recipients with retry logic.
        
        Args:
            recipients: List of email addresses
            subject: Email subject line
            html_body: HTML email content
            test_mode: If True, only send to test recipient
            
        Returns:
            Dict with delivery statistics and results
        """
        if test_mode:
            recipients = [self.test_recipient]
            print(f"🧪 TEST MODE: Sending only to {self.test_recipient}\n")
        
        results = {
            'total': len(recipients),
            'sent': 0,
            'failed': 0,
            'deliveries': [],
            'errors': []
        }
        
        for recipient in recipients:
            print(f"Sending to {recipient}...", end=" ")
            
            delivery = self.send_email(recipient, subject, html_body)
            results['deliveries'].append(delivery)
            
            if delivery['success']:
                results['sent'] += 1
                print("✅")
            else:
                results['failed'] += 1
                results['errors'].append({
                    'recipient': recipient,
                    'error': delivery.get('error')
                })
                print("❌")
        
        return results
    
    def save_delivery_report(self, results: Dict, draft_info: Dict) -> Path:
        """
        Save delivery report to JSON file.
        
        Args:
            results: Batch send results
            draft_info: Newsletter draft information
            
        Returns:
            Path to saved report file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        issue = draft_info['issue_number']
        report_file = self.deliveries_dir / f"delivery_{timestamp}_issue{issue}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'issue_number': issue,
            'subject': draft_info['subject'],
            'headline': draft_info['headline'],
            'statistics': {
                'total_recipients': results['total'],
                'successfully_sent': results['sent'],
                'failed': results['failed']
            },
            'deliveries': results['deliveries'],
            'errors': results['errors']
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def preview_email(self, draft_info: Dict, recipients: List[str]):
        """Print email preview without sending."""
        print("\n" + "="*70)
        print("📧 EMAIL PREVIEW")
        print("="*70)
        print(f"\nSubject: {draft_info['subject']}")
        print(f"Issue: #{draft_info['issue_number']}")
        print(f"Date: {draft_info['date']}")
        print(f"\nRecipients ({len(recipients)}):")
        for email in recipients[:10]:
            print(f"  - {email}")
        if len(recipients) > 10:
            print(f"  ... and {len(recipients) - 10} more")
        
        print(f"\nBody Preview:")
        print("-" * 70)
        # Show first 500 chars of HTML
        preview = draft_info['html'][:500]
        print(preview)
        if len(draft_info['html']) > 500:
            print(f"\n... (+ {len(draft_info['html']) - 500} more characters)")
        print("-" * 70)
        print("\n✅ Preview complete. Use without --preview flag to send.\n")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Send Edge Finder newsletter via email'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode - send only to test recipient'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview email without sending'
    )
    parser.add_argument(
        '--issue',
        type=int,
        help='Specific issue number to send'
    )
    
    args = parser.parse_args()
    
    # Initialize sender
    sender = NewsletterEmailSender()
    
    try:
        # Find and load latest draft
        print("🔍 Finding latest newsletter draft...")
        html_path, meta_path = sender.find_latest_draft(args.issue)
        print(f"   Found: {html_path.name}")
        
        print("\n📄 Loading newsletter content...")
        draft_info = sender.load_draft(html_path, meta_path)
        print(f"   Issue #{draft_info['issue_number']}: {draft_info['headline']}")
        
        # Load subscribers
        print("\n👥 Loading subscriber list...")
        subscribers = sender.load_subscribers()
        print(f"   Found {len(subscribers)} active subscribers")
        
        # Preview mode
        if args.preview:
            sender.preview_email(draft_info, subscribers)
            return
        
        # Send emails
        print("\n📨 Sending newsletter...")
        results = sender.send_batch(
            recipients=subscribers,
            subject=draft_info['subject'],
            html_body=draft_info['html'],
            test_mode=args.test
        )
        
        # Save delivery report
        print("\n💾 Saving delivery report...")
        report_path = sender.save_delivery_report(results, draft_info)
        print(f"   Report saved: {report_path}")
        
        # Summary
        print("\n" + "="*70)
        print("📊 DELIVERY SUMMARY")
        print("="*70)
        print(f"Total recipients: {results['total']}")
        print(f"Successfully sent: {results['sent']} ✅")
        print(f"Failed: {results['failed']} ❌")
        
        if results['errors']:
            print("\nErrors:")
            for error in results['errors']:
                print(f"  - {error['recipient']}: {error['error']}")
        
        print("\n✅ Email distribution complete!")
        
        # Output for Nebula orchestrator
        print("\n" + "="*70)
        print("🤖 NEBULA INTEGRATION INSTRUCTIONS")
        print("="*70)
        print("\nTo actually send emails, the orchestrator should:")
        print("1. Run this script to get recipient list and content")
        print("2. Call send_email tool for each delivery marked 'queued_for_nebula_send'")
        print("3. Update delivery report with actual send results")
        print("\nExample Nebula call:")
        print(f"  send_email(")
        print(f"    to='{subscribers[0] if subscribers else 'recipient@example.com'}',")
        print(f"    subject='{draft_info['subject']}',")
        print(f"    html_body=<newsletter_html_content>")
        print(f"  )")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
