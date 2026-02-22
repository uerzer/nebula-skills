#!/usr/bin/env python3
"""
Edge Finder Signup Handler

Handles newsletter signups from landing page, generates referral codes,
and triggers welcome email with lead magnet.

Can be used as:
1. Flask/FastAPI endpoint for landing page form submissions
2. CLI tool for manual subscriber additions
3. Import module for integration with other systems

Usage:
    # CLI
    python signup_handler.py add --email user@example.com --name "John Doe" --referral REF123

    # As API endpoint (Flask example included)
    python signup_handler.py serve --port 5000
    
    # Or import in your code
    from signup_handler import SignupHandler
    handler = SignupHandler()
    result = handler.process_signup(email, name, referral_code)
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import sys
import subprocess

# Import our existing tools
try:
    from referral_tracker import ReferralTracker
    from lead_magnet_builder import LeadMagnetBuilder
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False
    print("⚠️  Warning: Import referral_tracker and lead_magnet_builder in same directory")

# For Flask API server
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


class SignupHandler:
    def __init__(self):
        self.data_dir = Path("data")
        self.subscribers_file = self.data_dir / "newsletter-subscribers.json"
        self.lead_magnets_dir = Path("outputs/lead-magnets")
        
        if TOOLS_AVAILABLE:
            self.referral_tracker = ReferralTracker()
            self.lead_magnet_builder = LeadMagnetBuilder()
        else:
            self.referral_tracker = None
            self.lead_magnet_builder = None
        
        self._ensure_files()
    
    def _ensure_files(self):
        """Ensure required directories and files exist"""
        self.data_dir.mkdir(exist_ok=True)
        self.lead_magnets_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.subscribers_file.exists():
            with open(self.subscribers_file, 'w') as f:
                json.dump({}, f)
    
    def _load_subscribers(self) -> Dict:
        """Load subscriber database"""
        try:
            with open(self.subscribers_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_subscribers(self, data: Dict):
        """Save subscriber database"""
        with open(self.subscribers_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _send_welcome_email(self, email: str, name: str, referral_link: str) -> bool:
        """Send welcome email with lead magnet"""
        # In production, integrate with your email service (SendGrid, Mailgun, etc.)
        # For now, we'll create a draft email
        
        email_content = f"""
Subject: Welcome to Edge Finder + Your Free Lead Magnet 🎁

Hi {name},

Welcome to Edge Finder! You're now part of 500+ founders finding market gaps before the crowd.

Here's what you'll get every week:
✅ Top 3-5 scored opportunities (AI scanner insights)
✅ Market signals from Reddit, GitHub, Twitter, Product Hunt
✅ Execution playbooks and validation frameworks
✅ Early mover advantage on emerging trends

---

🎁 YOUR BONUS: 50 Validated Micro SaaS Ideas (2026 Edition)

Download your lead magnet here: [LINK TO PDF]

Each idea includes:
- Problem/solution breakdown
- Market size and competition analysis
- Execution difficulty and capital requirements
- Opportunity score (0-10 scale)

---

📈 GROW YOUR NETWORK, GET PREMIUM FREE

Share Edge Finder with friends and unlock rewards:
🎯 3 referrals = 1 month Premium access
🎯 10 referrals = 1 year Premium access
🎯 25 referrals = Lifetime Premium access

Your referral link: {referral_link}

Premium includes raw scanner data, crypto arbitrage alerts, private Discord, and live Q&A sessions.

---

First newsletter drops this Sunday at 6 AM UTC. See you in your inbox!

Best,
Edge Finder Team

---
Update preferences: https://edgefinder.com/preferences
Unsubscribe: https://edgefinder.com/unsubscribe
"""
        
        # Save to drafts
        drafts_dir = Path("outputs/email-drafts")
        drafts_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        draft_file = drafts_dir / f"welcome_{email.replace('@', '_at_')}_{timestamp}.txt"
        
        with open(draft_file, 'w') as f:
            f.write(email_content)
        
        print(f"📧 Welcome email draft saved: {draft_file}")
        
        # In production: Actually send via email service
        # send_email(to=email, subject="Welcome to Edge Finder", body=email_content)
        
        return True
    
    def process_signup(self, email: str, name: Optional[str] = None, 
                      referral_code: Optional[str] = None) -> Dict:
        """
        Process new newsletter signup
        
        Returns:
            Dict with success status, subscriber info, and any errors
        """
        if not email:
            return {
                'success': False,
                'error': 'Email is required'
            }
        
        # Validate email format (basic)
        if '@' not in email or '.' not in email.split('@')[1]:
            return {
                'success': False,
                'error': 'Invalid email format'
            }
        
        # Check if already subscribed
        subscribers = self._load_subscribers()
        if email in subscribers:
            return {
                'success': False,
                'error': 'Email already subscribed',
                'existing_subscriber': True
            }
        
        # Generate default name if not provided
        if not name:
            name = email.split('@')[0]
        
        # Process referral if provided
        referral_info = None
        if referral_code and self.referral_tracker:
            referral_result = self.referral_tracker.track_signup(
                referral_code,
                email,
                name
            )
            if referral_result.get('success'):
                referral_info = {
                    'referred_by': referral_result['referrer'],
                    'referrer_count': referral_result['referral_count'],
                    'reward': referral_result.get('reward')
                }
        
        # Generate referral link for new subscriber
        if self.referral_tracker:
            referral_data = self.referral_tracker.generate_referral_link(email, name)
            new_referral_code = referral_data['referral_code']
            new_referral_link = referral_data['referral_link']
        else:
            # Fallback if tools not available
            new_referral_code = f"REF{hash(email) % 10000:04d}"
            new_referral_link = f"https://edgefinder.com?ref={new_referral_code}"
        
        # Send welcome email with lead magnet
        email_sent = self._send_welcome_email(email, name, new_referral_link)
        
        # Generate lead magnet if needed
        lead_magnet_files = list(self.lead_magnets_dir.glob("50_micro_saas_ideas_*.pdf"))
        if not lead_magnet_files:
            print("📄 Generating lead magnet...")
            if self.lead_magnet_builder:
                try:
                    self.lead_magnet_builder.generate_micro_saas_ideas(50)
                except Exception as e:
                    print(f"⚠️  Lead magnet generation failed: {e}")
        
        return {
            'success': True,
            'subscriber': {
                'email': email,
                'name': name,
                'referral_code': new_referral_code,
                'referral_link': new_referral_link,
                'tier': 'free',
                'signup_date': datetime.now().isoformat()
            },
            'referral_info': referral_info,
            'welcome_email_sent': email_sent
        }
    
    def bulk_import(self, csv_file: Path) -> Dict:
        """Import subscribers from CSV file"""
        import csv
        
        if not csv_file.exists():
            return {
                'success': False,
                'error': f'File not found: {csv_file}'
            }
        
        results = {
            'success': True,
            'processed': 0,
            'added': 0,
            'skipped': 0,
            'errors': []
        }
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results['processed'] += 1
                email = row.get('email', '').strip()
                name = row.get('name', '').strip()
                
                if not email:
                    results['errors'].append(f"Row {results['processed']}: Missing email")
                    continue
                
                result = self.process_signup(email, name)
                if result['success']:
                    results['added'] += 1
                else:
                    if result.get('existing_subscriber'):
                        results['skipped'] += 1
                    else:
                        results['errors'].append(f"{email}: {result['error']}")
        
        return results


# Flask API Server
def create_app():
    """Create Flask API server for landing page"""
    if not FLASK_AVAILABLE:
        print("❌ Flask not installed. Install with: pip install flask flask-cors")
        return None
    
    app = Flask(__name__)
    CORS(app)  # Enable CORS for landing page
    
    handler = SignupHandler()
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy', 'service': 'edge-finder-signup'})
    
    @app.route('/api/signup', methods=['POST'])
    def signup():
        """Handle signup form submission"""
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid request data'
            }), 400
        
        email = data.get('email')
        name = data.get('name')
        referral_code = data.get('ref')  # From URL parameter
        
        result = handler.process_signup(email, name, referral_code)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    
    @app.route('/api/stats/<email>', methods=['GET'])
    def stats(email):
        """Get subscriber stats"""
        if not handler.referral_tracker:
            return jsonify({'success': False, 'error': 'Service unavailable'}), 503
        
        stats = handler.referral_tracker.get_stats(email)
        return jsonify(stats)
    
    @app.route('/api/leaderboard', methods=['GET'])
    def leaderboard():
        """Get referral leaderboard"""
        if not handler.referral_tracker:
            return jsonify({'success': False, 'error': 'Service unavailable'}), 503
        
        limit = request.args.get('limit', 10, type=int)
        board = handler.referral_tracker.get_leaderboard(limit)
        return jsonify({'success': True, 'leaderboard': board})
    
    return app


def main():
    parser = argparse.ArgumentParser(description="Edge Finder Signup Handler")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add subscriber
    add_parser = subparsers.add_parser('add', help='Add new subscriber')
    add_parser.add_argument('--email', required=True, help='Subscriber email')
    add_parser.add_argument('--name', help='Subscriber name')
    add_parser.add_argument('--referral', help='Referral code (if referred by someone)')
    
    # Bulk import
    import_parser = subparsers.add_parser('import', help='Import subscribers from CSV')
    import_parser.add_argument('file', help='CSV file path (columns: email, name)')
    
    # Serve API
    serve_parser = subparsers.add_parser('serve', help='Start API server')
    serve_parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    serve_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    handler = SignupHandler()
    
    if args.command == 'add':
        result = handler.process_signup(args.email, args.name, args.referral)
        
        if result['success']:
            print("\n✅ Subscriber added successfully!")
            print(f"\nEmail: {result['subscriber']['email']}")
            print(f"Name: {result['subscriber']['name']}")
            print(f"Referral link: {result['subscriber']['referral_link']}")
            
            if result.get('referral_info'):
                ref_info = result['referral_info']
                print(f"\n📊 Referral credited to: {ref_info['referred_by']}")
                print(f"   Total referrals: {ref_info['referrer_count']}")
                
                if ref_info.get('reward'):
                    reward = ref_info['reward']
                    print(f"\n🎉 REWARD UNLOCKED!")
                    print(f"   {reward['reward']}")
            print()
        else:
            print(f"\n❌ Error: {result['error']}\n")
    
    elif args.command == 'import':
        csv_path = Path(args.file)
        print(f"\n📥 Importing subscribers from {csv_path}...")
        
        result = handler.bulk_import(csv_path)
        
        print(f"\n✅ Import complete!")
        print(f"   Processed: {result['processed']}")
        print(f"   Added: {result['added']}")
        print(f"   Skipped: {result['skipped']}")
        
        if result['errors']:
            print(f"\n⚠️  Errors ({len(result['errors'])}):")
            for error in result['errors'][:10]:
                print(f"   • {error}")
            if len(result['errors']) > 10:
                print(f"   ... and {len(result['errors']) - 10} more")
        print()
    
    elif args.command == 'serve':
        if not FLASK_AVAILABLE:
            print("❌ Flask not installed. Install with: pip install flask flask-cors")
            return
        
        app = create_app()
        if app:
            print(f"\n🚀 Starting API server on {args.host}:{args.port}")
            print(f"   Health check: http://{args.host}:{args.port}/health")
            print(f"   Signup endpoint: http://{args.host}:{args.port}/api/signup")
            print()
            app.run(host=args.host, port=args.port, debug=True)


if __name__ == '__main__':
    main()
