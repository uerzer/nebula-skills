#!/usr/bin/env python3
"""
Astrology App - Command Line Interface

Usage:
    python main.py natal --name "John" --date 1977-06-06 --time 09:00 --city "Marinha Grande" --country "Portugal"
    python main.py compare --name1 "Person1" --date1 1977-06-06 --time1 09:00 --city1 "Marinha Grande" --country1 "Portugal" --name2 "Person2" --date2 1982-07-29 --time2 14:00 --city2 "Porto" --country2 "Portugal"
"""

import argparse
import sys
from datetime import datetime
from natal_chart import NatalChart
from compatibility import Compatibility


def parse_date(date_str: str) -> tuple:
    """Parse date string YYYY-MM-DD to (year, month, day)"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.year, dt.month, dt.day
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def parse_time(time_str: str) -> tuple:
    """Parse time string HH:MM to (hour, minute)"""
    try:
        dt = datetime.strptime(time_str, "%H:%M")
        return dt.hour, dt.minute
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}. Use HH:MM (24-hour)")


def natal_command(args):
    """Execute natal chart command"""
    print(f"\nGenerating natal chart for {args.name}...\n")
    
    # Parse date and time
    year, month, day = parse_date(args.date)
    hour, minute = parse_time(args.time)
    
    # Generate chart
    try:
        chart = NatalChart(
            name=args.name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            city=args.city,
            nation=args.country
        )
        
        # Print report
        print(chart.generate_report())
        
        # Optionally save to file
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(chart.generate_report())
            print(f"\nReport saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error generating natal chart: {e}", file=sys.stderr)
        return 1


def compare_command(args):
    """Execute compatibility comparison command"""
    print(f"\nAnalyzing compatibility between {args.name1} and {args.name2}...\n")
    
    # Parse dates and times
    year1, month1, day1 = parse_date(args.date1)
    hour1, minute1 = parse_time(args.time1)
    
    year2, month2, day2 = parse_date(args.date2)
    hour2, minute2 = parse_time(args.time2)
    
    try:
        # Generate both charts
        print(f"Generating chart for {args.name1}...")
        chart1 = NatalChart(
            name=args.name1,
            year=year1,
            month=month1,
            day=day1,
            hour=hour1,
            minute=minute1,
            city=args.city1,
            nation=args.country1
        )
        
        print(f"Generating chart for {args.name2}...")
        chart2 = NatalChart(
            name=args.name2,
            year=year2,
            month=month2,
            day=day2,
            hour=hour2,
            minute=minute2,
            city=args.city2,
            nation=args.country2
        )
        
        # Analyze compatibility
        print("Analyzing compatibility...\n")
        compat = Compatibility(chart1.get_data(), chart2.get_data())
        
        # Print report
        print(compat.generate_report())
        
        # Optionally save to file
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(compat.generate_report())
            print(f"\nReport saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error analyzing compatibility: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Astrology App - Natal Charts & Compatibility Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate natal chart:
    python main.py natal --name "John" --date 1977-06-06 --time 09:00 --city "Marinha Grande" --country "Portugal"
  
  Compare two charts:
    python main.py compare --name1 "Person1" --date1 1977-06-06 --time1 09:00 --city1 "Marinha Grande" --country1 "Portugal" --name2 "Person2" --date2 1982-07-29 --time2 14:00 --city2 "Porto" --country2 "Portugal"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Natal chart command
    natal_parser = subparsers.add_parser('natal', help='Generate natal chart')
    natal_parser.add_argument('--name', required=True, help='Person name')
    natal_parser.add_argument('--date', required=True, help='Birth date (YYYY-MM-DD)')
    natal_parser.add_argument('--time', required=True, help='Birth time (HH:MM, 24-hour)')
    natal_parser.add_argument('--city', required=True, help='Birth city')
    natal_parser.add_argument('--country', required=True, help='Birth country')
    natal_parser.add_argument('--output', '-o', help='Output file path (optional)')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two natal charts')
    compare_parser.add_argument('--name1', required=True, help='First person name')
    compare_parser.add_argument('--date1', required=True, help='First person birth date (YYYY-MM-DD)')
    compare_parser.add_argument('--time1', required=True, help='First person birth time (HH:MM)')
    compare_parser.add_argument('--city1', required=True, help='First person birth city')
    compare_parser.add_argument('--country1', required=True, help='First person birth country')
    
    compare_parser.add_argument('--name2', required=True, help='Second person name')
    compare_parser.add_argument('--date2', required=True, help='Second person birth date (YYYY-MM-DD)')
    compare_parser.add_argument('--time2', required=True, help='Second person birth time (HH:MM)')
    compare_parser.add_argument('--city2', required=True, help='Second person birth city')
    compare_parser.add_argument('--country2', required=True, help='Second person birth country')
    
    compare_parser.add_argument('--output', '-o', help='Output file path (optional)')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == 'natal':
        return natal_command(args)
    elif args.command == 'compare':
        return compare_command(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
