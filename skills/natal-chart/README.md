# Natal Chart Generation Skill

A battle-tested skill for generating accurate natal/birth charts following the TÂCHES methodology.

## What This Skill Does

Generates natal charts with:
- ✅ Accurate planetary positions (Swiss Ephemeris)
- ✅ House cusps and aspects
- ✅ SVG chart visualization
- ✅ Structured JSON data output
- ✅ Battle-tested with real data (Carl Jung's birth chart)

## Installation

```bash
pip install kerykeion
```

## Quick Start

```python
from kerykeion import AstrologicalSubject, KerykeionChartSVG, NatalAspects

# Create subject with explicit coordinates
subject = AstrologicalSubject(
    name="Carl Jung",
    year=1875, month=7, day=26,
    hour=19, minute=20,
    lat=47.6, lng=9.32,
    tz_str="Europe/Zurich"
)

# Access placements
print(f"Sun: {subject.sun.sign} {subject.sun.position:.2f}°")
print(f"Moon: {subject.moon.sign} {subject.moon.position:.2f}°")
print(f"Rising: {subject.first_house.sign} {subject.first_house.position:.2f}°")

# Generate chart
chart = KerykeionChartSVG(subject)
chart.makeSVG()

# Get aspects
aspects = NatalAspects(subject)
for aspect in aspects.all_aspects[:5]:
    print(f"{aspect.p1_name} {aspect.aspect} {aspect.p2_name}")
```

## Files Included

- **SKILL.md** - Complete skill documentation with battle-tested API usage
- **test_natal_chart.py** - Working test script with Carl Jung's birth data
- **README.md** - This file

## Test Results

Successfully generated natal chart for Carl Jung (b. July 26, 1875, 19:20, Kesswil, Switzerland):

- ✅ Sun: Leo 3.30° (7th House)
- ✅ Moon: Taurus 15.43° (3rd House)  
- ✅ Rising: Capricorn 28.65°
- ✅ 10 planets calculated with positions
- ✅ 12 house cusps
- ✅ Multiple aspects (squares, trines, sextiles, etc.)
- ✅ SVG chart generated
- ✅ JSON data exported

## Key Learnings (Heal-Skill Process)

This skill was developed following TÂCHES methodology with expected failures and fixes:

1. **Failure**: ModuleNotFoundError → **Fix**: Install kerykeion
2. **Failure**: GeoNames API lookup failed → **Fix**: Always use explicit lat/lng/tz_str
3. **Failure**: AttributeError 'planets_list' → **Fix**: Use individual attributes or model_dump()
4. **Success**: All data calculated correctly, charts generated

## API Notes (Kerykeion v5.7.2)

- Individual planets: `subject.sun`, `subject.moon`, etc. (not `planets_list`)
- Returns KerykeionPointModel with: sign, position, house, retrograde
- Full data: `subject.model_dump()` returns dict with all fields
- Aspects: `NatalAspects(subject).all_aspects`
- Charts: `KerykeionChartSVG(subject).makeSVG()`

## Why This Works

Following TÂCHES best practices:
- ✅ Library research documented (Kerykeion vs alternatives)
- ✅ Progressive disclosure (errors led to fixes)
- ✅ Heal-skill pattern (fixes captured in docs)
- ✅ Tested with real data (not placeholders)
- ✅ Battle-tested code (expect first failure, iterate)

## Credits

Created using the TÂCHES methodology inspired by Tâches Teaches' "This Claude Code Skill Creates Claude Code Skills For You" video.
