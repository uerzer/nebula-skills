#!/usr/bin/env python3
"""
Edge Finder Referral Tracking System

Manages subscriber referrals, tracks conversions, and automates reward delivery.
Milestone rewards:
- 3 referrals = Premium access (1 month)
- 10 referrals = Premium access (1 year) 
- 25 referrals = Lifetime premium

Usage:
    python referral_tracker.py generate <email>           # Create referral link
    python referral_tracker.py track <referral_code> <new_email>  # Record signup
    python referral_tracker.py stats <email>              # Show referral stats
    python referral_tracker.py leaderboard [--limit 10]   # Top referrers
    python referral_tracker.py check-rewards              # Process pending rewards
    python referral_tracker.py upgrade <email> <tier>     # Manual tier upgrade
"""

import json
import hashlib
import secrets
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import sys

# File paths
DATA_DIR = Path("data")
SUBSCRIBERS_FILE = DATA_DIR / "newsletter-subscribers.json"
REFERRALS_FILE = DATA_DIR / "referrals.json"

# Tier definitions
TIERS = {
    "free": {"name": "Free", "price": 0},
    "premium_1m": {"name": "Premium (1 Month)", "price": 49, "duration_days": 30},
    "premium_1y": {"name": "Premium (1 Year)", "price": 588, "duration_days": 365},
    "lifetime": {"name": "Lifetime Premium", "price": 0, "duration_days": None}
}

# Reward milestones
MILESTONES = [
    {"referrals": 3, "tier": "premium_1m", "name": "1 Month Premium"},
    {"referrals": 10, "tier": "premium_1y", "name": "1 Year Premium"},
    {"referrals": 25, "tier": "lifetime", "name": "Lifetime Premium"}
]


class ReferralTracker:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.subscribers_file = SUBSCRIBERS_FILE
        self.referrals_file = REFERRALS_FILE
        self._ensure_files()
        
    def _ensure_files(self):
        """Create data directory and files if they don't exist"""
        self.data_dir.mkdir(exist_ok=True)
        
        if not self.subscribers_file.exists():
            self._save_subscribers({})
            
        if not self.referrals_file.exists():
            self._save_referrals({})
    
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
    
    def _load_referrals(self) -> Dict:
        """Load referral tracking data"""
        try:
            with open(self.referrals_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_referrals(self, data: Dict):
        """Save referral tracking data"""
        with open(self.referrals_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_referral_code(self, email: str) -> str:
        """Generate unique referral code from email"""
        # Create deterministic but opaque code
        hash_base = hashlib.sha256(email.lower().encode()).hexdigest()[:8]
        random_suffix = secrets.token_urlsafe(4)
        return f"{hash_base}{random_suffix}".upper()
    
    def _calculate_tier_expiry(self, tier: str, current_expiry: Optional[str] = None) -> Optional[str]:
        """Calculate new expiry date for tier upgrade"""
        if tier == "lifetime":
            return None  # Lifetime never expires
        
        duration = TIERS[tier]["duration_days"]
        if current_expiry:
            # Extend from current expiry
            try:
                base_date = datetime.fromisoformat(current_expiry)
            except:
                base_date = datetime.now()
        else:
            base_date = datetime.now()
        
        new_expiry = base_date + timedelta(days=duration)
        return new_expiry.isoformat()
    
    def generate_referral_link(self, email: str, name: Optional[str] = None) -> Dict:
        """Generate referral link for subscriber"""
        subscribers = self._load_subscribers()
        referrals = self._load_referrals()
        
        # Check if subscriber exists
        if email in subscribers:
            # Return existing code
            subscriber = subscribers[email]
            referral_code = subscriber.get("referral_code")
            if not referral_code:
                # Generate code if missing
                referral_code = self._generate_referral_code(email)
                subscriber["referral_code"] = referral_code
                self._save_subscribers(subscribers)
        else:
            # Create new subscriber
            referral_code = self._generate_referral_code(email)
            subscriber = {
                "email": email,
                "name": name or email.split('@')[0],
                "referral_code": referral_code,
                "referred_by": None,
                "tier": "free",
                "tier_expiry": None,
                "signup_date": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            subscribers[email] = subscriber
            self._save_subscribers(subscribers)
        
        # Initialize referral tracking
        if referral_code not in referrals:
            referrals[referral_code] = {
                "owner_email": email,
                "referral_count": 0,
                "referred_emails": [],
                "rewards_claimed": [],
                "created_at": datetime.now().isoformat()
            }
            self._save_referrals(referrals)
        
        referral_link = f"https://edgefinder.com?ref={referral_code}"
        
        return {
            "email": email,
            "referral_code": referral_code,
            "referral_link": referral_link,
            "referral_count": referrals[referral_code]["referral_count"],
            "tier": subscriber["tier"]
        }
    
    def track_signup(self, referral_code: str, new_email: str, new_name: Optional[str] = None) -> Dict:
        """Track new signup from referral link"""
        subscribers = self._load_subscribers()
        referrals = self._load_referrals()
        
        # Validate referral code exists
        if referral_code not in referrals:
            return {
                "success": False,
                "error": "Invalid referral code"
            }
        
        # Check if email already exists
        if new_email in subscribers:
            return {
                "success": False,
                "error": "Email already subscribed"
            }
        
        # Get referrer
        referrer_email = referrals[referral_code]["owner_email"]
        
        # Create new subscriber with referral attribution
        new_referral_code = self._generate_referral_code(new_email)
        new_subscriber = {
            "email": new_email,
            "name": new_name or new_email.split('@')[0],
            "referral_code": new_referral_code,
            "referred_by": referrer_email,
            "tier": "free",
            "tier_expiry": None,
            "signup_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        subscribers[new_email] = new_subscriber
        
        # Update referral tracking
        referrals[referral_code]["referral_count"] += 1
        referrals[referral_code]["referred_emails"].append({
            "email": new_email,
            "signup_date": datetime.now().isoformat()
        })
        
        # Initialize new subscriber's referral tracking
        referrals[new_referral_code] = {
            "owner_email": new_email,
            "referral_count": 0,
            "referred_emails": [],
            "rewards_claimed": [],
            "created_at": datetime.now().isoformat()
        }
        
        self._save_subscribers(subscribers)
        self._save_referrals(referrals)
        
        # Check for milestone rewards
        new_count = referrals[referral_code]["referral_count"]
        reward_info = self._check_milestone_reward(referrer_email, new_count)
        
        return {
            "success": True,
            "new_subscriber": new_email,
            "referrer": referrer_email,
            "referral_count": new_count,
            "reward": reward_info
        }
    
    def _check_milestone_reward(self, email: str, referral_count: int) -> Optional[Dict]:
        """Check if subscriber reached new milestone"""
        subscribers = self._load_subscribers()
        referrals = self._load_referrals()
        
        subscriber = subscribers[email]
        referral_code = subscriber["referral_code"]
        claimed_milestones = set(r["milestone"] for r in referrals[referral_code]["rewards_claimed"])
        
        # Find highest unclaimed milestone
        eligible_milestone = None
        for milestone in reversed(MILESTONES):
            if referral_count >= milestone["referrals"] and milestone["referrals"] not in claimed_milestones:
                eligible_milestone = milestone
                break
        
        if eligible_milestone:
            # Award tier upgrade
            new_tier = eligible_milestone["tier"]
            old_tier = subscriber["tier"]
            
            # Update tier
            subscriber["tier"] = new_tier
            subscriber["tier_expiry"] = self._calculate_tier_expiry(new_tier, subscriber.get("tier_expiry"))
            subscriber["last_updated"] = datetime.now().isoformat()
            
            # Record reward claim
            reward_record = {
                "milestone": eligible_milestone["referrals"],
                "tier": new_tier,
                "claimed_at": datetime.now().isoformat()
            }
            referrals[referral_code]["rewards_claimed"].append(reward_record)
            
            self._save_subscribers(subscribers)
            self._save_referrals(referrals)
            
            return {
                "milestone_reached": eligible_milestone["referrals"],
                "reward": eligible_milestone["name"],
                "old_tier": old_tier,
                "new_tier": new_tier,
                "tier_expiry": subscriber["tier_expiry"]
            }
        
        return None
    
    def get_stats(self, email: str) -> Dict:
        """Get referral statistics for subscriber"""
        subscribers = self._load_subscribers()
        referrals = self._load_referrals()
        
        if email not in subscribers:
            return {
                "success": False,
                "error": "Email not found"
            }
        
        subscriber = subscribers[email]
        referral_code = subscriber["referral_code"]
        referral_data = referrals.get(referral_code, {})
        
        # Calculate next milestone
        current_count = referral_data.get("referral_count", 0)
        next_milestone = None
        for milestone in MILESTONES:
            if current_count < milestone["referrals"]:
                next_milestone = {
                    "referrals_needed": milestone["referrals"],
                    "referrals_remaining": milestone["referrals"] - current_count,
                    "reward": milestone["name"]
                }
                break
        
        return {
            "success": True,
            "email": email,
            "name": subscriber.get("name"),
            "referral_code": referral_code,
            "referral_link": f"https://edgefinder.com?ref={referral_code}",
            "tier": subscriber["tier"],
            "tier_name": TIERS[subscriber["tier"]]["name"],
            "tier_expiry": subscriber.get("tier_expiry"),
            "referral_count": current_count,
            "referred_subscribers": referral_data.get("referred_emails", []),
            "rewards_claimed": referral_data.get("rewards_claimed", []),
            "next_milestone": next_milestone,
            "signup_date": subscriber.get("signup_date")
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top referrers leaderboard"""
        referrals = self._load_referrals()
        subscribers = self._load_subscribers()
        
        # Build leaderboard
        leaderboard = []
        for code, data in referrals.items():
            email = data["owner_email"]
            if email in subscribers:
                subscriber = subscribers[email]
                leaderboard.append({
                    "rank": 0,  # Will be set after sorting
                    "name": subscriber.get("name", email.split('@')[0]),
                    "email": email,
                    "referral_count": data["referral_count"],
                    "tier": subscriber["tier"],
                    "tier_name": TIERS[subscriber["tier"]]["name"]
                })
        
        # Sort by referral count
        leaderboard.sort(key=lambda x: x["referral_count"], reverse=True)
        
        # Assign ranks
        for i, entry in enumerate(leaderboard[:limit], 1):
            entry["rank"] = i
        
        return leaderboard[:limit]
    
    def check_and_process_rewards(self) -> List[Dict]:
        """Process all pending milestone rewards"""
        subscribers = self._load_subscribers()
        referrals = self._load_referrals()
        processed = []
        
        for email, subscriber in subscribers.items():
            referral_code = subscriber.get("referral_code")
            if not referral_code or referral_code not in referrals:
                continue
            
            referral_count = referrals[referral_code]["referral_count"]
            reward_info = self._check_milestone_reward(email, referral_count)
            
            if reward_info:
                processed.append({
                    "email": email,
                    "reward": reward_info
                })
        
        return processed
    
    def upgrade_tier(self, email: str, tier: str, duration_days: Optional[int] = None) -> Dict:
        """Manually upgrade subscriber tier"""
        subscribers = self._load_subscribers()
        
        if email not in subscribers:
            return {
                "success": False,
                "error": "Email not found"
            }
        
        if tier not in TIERS and tier != "custom":
            return {
                "success": False,
                "error": f"Invalid tier. Options: {list(TIERS.keys())}"
            }
        
        subscriber = subscribers[email]
        old_tier = subscriber["tier"]
        
        subscriber["tier"] = tier
        if tier == "custom" and duration_days:
            expiry = datetime.now() + timedelta(days=duration_days)
            subscriber["tier_expiry"] = expiry.isoformat()
        else:
            subscriber["tier_expiry"] = self._calculate_tier_expiry(tier, subscriber.get("tier_expiry"))
        
        subscriber["last_updated"] = datetime.now().isoformat()
        
        self._save_subscribers(subscribers)
        
        return {
            "success": True,
            "email": email,
            "old_tier": old_tier,
            "new_tier": tier,
            "tier_expiry": subscriber["tier_expiry"]
        }


def format_stats_output(stats: Dict):
    """Format stats for terminal output"""
    if not stats.get("success"):
        print(f"❌ Error: {stats.get('error')}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 REFERRAL STATS - {stats['name']} ({stats['email']})")
    print(f"{'='*60}\n")
    
    print(f"🎯 Tier: {stats['tier_name']}")
    if stats['tier_expiry']:
        expiry = datetime.fromisoformat(stats['tier_expiry'])
        print(f"   Expires: {expiry.strftime('%Y-%m-%d')}")
    
    print(f"\n🔗 Referral Link:")
    print(f"   {stats['referral_link']}")
    print(f"   Code: {stats['referral_code']}")
    
    print(f"\n📈 Referrals: {stats['referral_count']}")
    
    if stats['next_milestone']:
        nm = stats['next_milestone']
        print(f"\n🎁 Next Reward: {nm['reward']}")
        print(f"   Need {nm['referrals_remaining']} more referrals (total: {nm['referrals_needed']})")
    else:
        print(f"\n🏆 All milestones achieved!")
    
    if stats['rewards_claimed']:
        print(f"\n✅ Rewards Claimed:")
        for reward in stats['rewards_claimed']:
            claimed_date = datetime.fromisoformat(reward['claimed_at']).strftime('%Y-%m-%d')
            print(f"   • {reward['milestone']} referrals → {TIERS[reward['tier']]['name']} ({claimed_date})")
    
    if stats['referred_subscribers']:
        print(f"\n👥 Referred Subscribers ({len(stats['referred_subscribers'])}):")
        for ref in stats['referred_subscribers'][:5]:
            signup_date = datetime.fromisoformat(ref['signup_date']).strftime('%Y-%m-%d')
            print(f"   • {ref['email']} (joined {signup_date})")
        if len(stats['referred_subscribers']) > 5:
            print(f"   ... and {len(stats['referred_subscribers']) - 5} more")
    
    print(f"\n{'='*60}\n")


def format_leaderboard_output(leaderboard: List[Dict]):
    """Format leaderboard for terminal output"""
    print(f"\n{'='*60}")
    print(f"🏆 REFERRAL LEADERBOARD - TOP {len(leaderboard)}")
    print(f"{'='*60}\n")
    
    if not leaderboard:
        print("No referrals yet. Be the first!")
        return
    
    print(f"{'Rank':<6} {'Name':<20} {'Referrals':<12} {'Tier':<20}")
    print(f"{'-'*60}")
    
    for entry in leaderboard:
        rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(entry['rank'], f"#{entry['rank']}")
        print(f"{rank_emoji:<6} {entry['name']:<20} {entry['referral_count']:<12} {entry['tier_name']:<20}")
    
    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Edge Finder Referral Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate referral link
    gen_parser = subparsers.add_parser('generate', help='Generate referral link for email')
    gen_parser.add_argument('email', help='Subscriber email')
    gen_parser.add_argument('--name', help='Subscriber name', default=None)
    
    # Track signup
    track_parser = subparsers.add_parser('track', help='Track new signup from referral')
    track_parser.add_argument('referral_code', help='Referral code used')
    track_parser.add_argument('new_email', help='New subscriber email')
    track_parser.add_argument('--name', help='New subscriber name', default=None)
    
    # Get stats
    stats_parser = subparsers.add_parser('stats', help='Show referral stats for email')
    stats_parser.add_argument('email', help='Subscriber email')
    
    # Leaderboard
    leader_parser = subparsers.add_parser('leaderboard', help='Show top referrers')
    leader_parser.add_argument('--limit', type=int, default=10, help='Number of top referrers to show')
    
    # Check rewards
    subparsers.add_parser('check-rewards', help='Process pending milestone rewards')
    
    # Upgrade tier
    upgrade_parser = subparsers.add_parser('upgrade', help='Manually upgrade subscriber tier')
    upgrade_parser.add_argument('email', help='Subscriber email')
    upgrade_parser.add_argument('tier', help='New tier (free, premium_1m, premium_1y, lifetime)')
    upgrade_parser.add_argument('--days', type=int, help='Custom duration in days', default=None)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tracker = ReferralTracker()
    
    if args.command == 'generate':
        result = tracker.generate_referral_link(args.email, args.name)
        print(f"\n✅ Referral link generated!")
        print(f"\nEmail: {result['email']}")
        print(f"Code: {result['referral_code']}")
        print(f"Link: {result['referral_link']}")
        print(f"Current referrals: {result['referral_count']}")
        print(f"Tier: {TIERS[result['tier']]['name']}\n")
    
    elif args.command == 'track':
        result = tracker.track_signup(args.referral_code, args.new_email, args.name)
        if result['success']:
            print(f"\n✅ Signup tracked!")
            print(f"\nNew subscriber: {result['new_subscriber']}")
            print(f"Referred by: {result['referrer']}")
            print(f"Total referrals: {result['referral_count']}")
            
            if result['reward']:
                reward = result['reward']
                print(f"\n🎉 MILESTONE REACHED!")
                print(f"Referrer earned: {reward['reward']}")
                print(f"Tier upgraded: {reward['old_tier']} → {reward['new_tier']}")
                if reward['tier_expiry']:
                    expiry = datetime.fromisoformat(reward['tier_expiry'])
                    print(f"Valid until: {expiry.strftime('%Y-%m-%d')}")
            print()
        else:
            print(f"\n❌ Error: {result['error']}\n")
    
    elif args.command == 'stats':
        stats = tracker.get_stats(args.email)
        format_stats_output(stats)
    
    elif args.command == 'leaderboard':
        leaderboard = tracker.get_leaderboard(args.limit)
        format_leaderboard_output(leaderboard)
    
    elif args.command == 'check-rewards':
        processed = tracker.check_and_process_rewards()
        if processed:
            print(f"\n✅ Processed {len(processed)} reward(s):")
            for item in processed:
                reward = item['reward']
                print(f"\n  {item['email']}:")
                print(f"  → {reward['reward']}")
                print(f"  → Tier: {reward['old_tier']} → {reward['new_tier']}")
            print()
        else:
            print("\nNo pending rewards to process.\n")
    
    elif args.command == 'upgrade':
        result = tracker.upgrade_tier(args.email, args.tier, args.days)
        if result['success']:
            print(f"\n✅ Tier upgraded!")
            print(f"\nEmail: {result['email']}")
            print(f"Old tier: {result['old_tier']}")
            print(f"New tier: {result['new_tier']}")
            if result['tier_expiry']:
                expiry = datetime.fromisoformat(result['tier_expiry'])
                print(f"Expires: {expiry.strftime('%Y-%m-%d')}")
            print()
        else:
            print(f"\n❌ Error: {result['error']}\n")


if __name__ == '__main__':
    main()
