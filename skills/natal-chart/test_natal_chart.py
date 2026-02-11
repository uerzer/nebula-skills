#!/usr/bin/env python3
"""
Test script for natal chart generation skill
Following TÂCHES methodology: test with real data, expect failures, iterate
"""

from kerykeion import AstrologicalSubject, KerykeionChartSVG, NatalAspects
import json
from pathlib import Path

def test_natal_chart():
    """Test with Carl Jung's birth data (famous example from astrology)"""
    
    print("Testing natal chart generation...")
    print("=" * 60)
    
    # Carl Jung: July 26, 1875, 19:20, Kesswil, Switzerland
    # Using explicit coordinates due to GeoNames API limitations
    subject = AstrologicalSubject(
        name="Carl Jung",
        year=1875,
        month=7,
        day=26,
        hour=19,
        minute=20,
        lat=47.6,  # Kesswil, Switzerland coordinates
        lng=9.32,
        tz_str="Europe/Zurich"
    )
    
    # Extract key data
    print(f"\n📊 Birth Data:")
    print(f"Name: {subject.name}")
    print(f"Date: {subject.year}-{subject.month:02d}-{subject.day:02d}")
    print(f"Time: {subject.hour:02d}:{subject.minute:02d}")
    print(f"Coordinates: {subject.lat:.4f}, {subject.lng:.4f}")
    print(f"Timezone: {subject.tz_str}")
    
    # Key placements
    print(f"\n🌟 Key Placements:")
    print(f"Sun: {subject.sun.sign} {subject.sun.position:.2f}° (House {subject.sun.house})")
    print(f"Moon: {subject.moon.sign} {subject.moon.position:.2f}° (House {subject.moon.house})")
    print(f"Rising: {subject.first_house.sign} {subject.first_house.position:.2f}°")
    
    # All major planets
    print(f"\n🪐 Planetary Positions:")
    planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    for planet_name in planets:
        planet = getattr(subject, planet_name)
        retro = "℞" if planet.retrograde else ""
        print(f"{planet.name:12} {planet.sign:12} {planet.position:6.2f}° (House {planet.house}) {retro}")
    
    # Houses
    print(f"\n🏠 House Cusps:")
    house_names = ['first_house', 'second_house', 'third_house', 'fourth_house', 'fifth_house', 'sixth_house']
    for i, house_name in enumerate(house_names, 1):
        house = getattr(subject, house_name)
        print(f"House {i:2}: {house.sign:12} {house.position:6.2f}°")
    
    # Aspects
    print(f"\n🔗 Major Aspects:")
    aspects = NatalAspects(subject)
    major_aspects = ['conjunction', 'opposition', 'trine', 'square', 'sextile']
    for aspect_data in aspects.all_aspects[:10]:  # First 10 aspects
        if aspect_data.aspect.lower() in major_aspects:
            print(f"{aspect_data.p1_name:8} {aspect_data.aspect:12} {aspect_data.p2_name:8} (orb: {aspect_data.orbit:.2f}°)")
    
    # Generate SVG chart
    print(f"\n🎨 Generating chart visualization...")
    chart = KerykeionChartSVG(subject)
    chart.makeSVG()
    
    # Find the generated SVG file
    svg_files = list(Path('.').glob('*_natal_chart.svg'))
    if svg_files:
        print(f"✅ Chart saved to: {svg_files[0]}")
    else:
        print("⚠️  SVG file not found in expected location")
    
    # Save JSON data using model_dump
    data_dict = subject.model_dump()
    
    json_output = {
        "name": subject.name,
        "birth_data": {
            "date": f"{subject.year}-{subject.month:02d}-{subject.day:02d}",
            "time": f"{subject.hour:02d}:{subject.minute:02d}",
            "lat": subject.lat,
            "lon": subject.lng,
            "timezone": subject.tz_str
        },
        "placements": {
            "sun": {"sign": subject.sun.sign, "position": subject.sun.position, "house": subject.sun.house},
            "moon": {"sign": subject.moon.sign, "position": subject.moon.position, "house": subject.moon.house},
            "rising": {"sign": subject.first_house.sign, "position": subject.first_house.position}
        },
        "planets": {name: data_dict[name] for name in planets},
        "houses": {f"house_{i}": data_dict[house_names[i-1]] for i in range(1, 7)},
        "aspects": [
            {
                "planet1": asp.p1_name,
                "planet2": asp.p2_name,
                "aspect": asp.aspect,
                "orb": asp.orbit
            } 
            for asp in aspects.all_aspects[:20]
        ]
    }
    
    json_path = Path('natal_chart_data.json')
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    
    print(f"✅ JSON data saved to: {json_path}")
    print("\n" + "=" * 60)
    print("✅ Test completed successfully!")
    
    return json_output

if __name__ == "__main__":
    try:
        result = test_natal_chart()
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
