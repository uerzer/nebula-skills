---
name: generate-natal-chart
description: Generates natal/birth charts with astronomical calculations, aspects, and interpretations. Takes birth date, time, and location, outputs HTML visualization and structured JSON data.
---

<objective>
Generate accurate natal charts (birth charts) based on astronomical data. Calculates planetary positions, houses, aspects, and provides astrological interpretations. Outputs both visual HTML charts and structured JSON data for further processing.
</objective>

<library_rationale>
This skill uses **Kerykeion 5.7.2** (https://github.com/g-battaglia/kerykeion) for natal chart calculations:

**Why Kerykeion:**
- Actively maintained (last update Feb 2026)
- Built on Swiss Ephemeris (industry standard for astronomical accuracy)
- Native SVG chart generation with customizable themes
- Clean JSON serialization via model_dump()
- Modern Python API (3.9+) with Pydantic models
- Comprehensive documentation
- Largest community (557 stars)

**Evaluated alternatives:**
- natal: Good but smaller community, less features
- immanuel-python: Swiss Ephemeris based but limited visualization
- flatlib: Outdated (last update 2021)
- pyswisseph: Low-level, requires more manual work

**Installation:** `pip install kerykeion`

**API Notes (v5.7.2):**
- Individual planets accessed as attributes: `subject.sun`, `subject.moon`, etc.
- Returns KerykeionPointModel objects with properties: sign, position, house, retrograde
- No `planets_list` attribute - use `model_dump()` to get all data as dict
- Aspects require separate NatalAspects class: `NatalAspects(subject).all_aspects`
</library_rationale>

<inputs>
Required parameters:
- **name**: Person's name (string)
- **year**: Birth year (int, e.g., 1990)
- **month**: Birth month (int, 1-12)
- **day**: Birth day (int, 1-31)
- **hour**: Birth hour (int, 0-23, in local time)
- **minute**: Birth minute (int, 0-59)
- **city**: Birth city (string, used for timezone/coordinates lookup)

Optional parameters:
- **lat**: Latitude (float, if city lookup unavailable)
- **lon**: Longitude (float, if city lookup unavailable)
- **tz_str**: Timezone string (string, e.g., "America/New_York")

Example:
```python
name="John Doe"
year=1990
month=3
day=15
hour=14
minute=30
city="New York"
```
</inputs>

<process>
1. **Install dependencies** (first run only):
   ```bash
   pip install kerykeion
   ```

2. **Import required classes**:
   ```python
   from kerykeion import AstrologicalSubject, KerykeionChartSVG, NatalAspects
   ```

3. **Create AstrologicalSubject** (IMPORTANT: Use explicit coordinates):
   ```python
   subject = AstrologicalSubject(
       name=name,
       year=year,
       month=month,
       day=day,
       hour=hour,
       minute=minute,
       lat=latitude,   # Required - city lookup often fails
       lng=longitude,  # Required
       tz_str=timezone # Required - e.g., "America/New_York"
   )
   ```

4. **Extract structured data**:
   - Individual planets: `subject.sun`, `subject.moon`, `subject.mercury`, etc.
   - Each returns KerykeionPointModel with: sign, position, house, retrograde
   - Houses: `subject.first_house`, `subject.second_house`, etc.
   - Full data dict: `subject.model_dump()` (contains all planets and houses)
   - Aspects: `NatalAspects(subject).all_aspects` (returns list of aspect objects)

5. **Generate SVG visualization**:
   ```python
   chart = KerykeionChartSVG(subject)
   chart.makeSVG()
   # SVG saved to: /root/{name} - Natal Chart.svg
   ```

6. **Return both outputs**:
   - JSON: Structured astronomical data via model_dump()
   - SVG: Visual chart for interpretation
</process>

<output_format>
**JSON Structure:**
```json
{
  "name": "John Doe",
  "birth_data": {
    "date": "1990-03-15",
    "time": "14:30",
    "city": "New York",
    "lat": 40.7128,
    "lon": -74.0060,
    "timezone": "America/New_York"
  },
  "planets": [
    {
      "name": "Sun",
      "sign": "Pisces",
      "position": 24.52,
      "house": 10,
      "retrograde": false
    }
  ],
  "houses": [
    {
      "number": 1,
      "sign": "Cancer",
      "position": 15.32
    }
  ],
  "aspects": [
    {
      "planet1": "Sun",
      "planet2": "Moon",
      "aspect": "Trine",
      "orb": 2.5
    }
  ]
}
```

**Visual Output:**
- SVG file: `{name}_natal_chart.svg`
- Contains zodiac wheel with planetary positions
- Shows aspects (lines between planets)
- Includes house divisions
</output_format>

<common_errors_and_fixes>
**Error: "Missing data from geonames: countryCode, timezonestr, lat, lng"**
- **Cause**: GeoNames API limitations (shared default username, 2000 req/hour limit)
- **Fix**: ALWAYS provide explicit lat/lng/tz_str parameters (don't rely on city lookup)
- Example:
  ```python
  subject = AstrologicalSubject(
      name=name, year=year, month=month, day=day,
      hour=hour, minute=minute,
      lat=40.7128, lng=-74.0060, tz_str="America/New_York"
  )
  ```

**Error: "AstrologicalSubject has no attribute 'planets_list'"**
- **Cause**: API changed in v5.7.2 - no more list attributes
- **Fix**: Use individual planet attributes or model_dump()
  ```python
  # Individual access
  sun_data = subject.sun  # Returns KerykeionPointModel
  
  # Or get all as dict
  all_data = subject.model_dump()
  planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']
  for planet_name in planets:
      planet_data = all_data[planet_name]
  ```

**Error: "cannot import name 'KerykeionChartSVG'"**
- **Fix**: Import from top level, not submodule
  ```python
  from kerykeion import KerykeionChartSVG  # Correct
  # NOT: from kerykeion.charts import KerykeionChartSVG
  ```

**Error: "Swiss Ephemeris files not found"**
- **Fix**: Kerykeion auto-downloads on first run. If fails, check internet connection.

**Chart SVG location:**
- SVG saves to `/root/{name} - Natal Chart.svg` (not current directory)
- Check stderr for actual path: "SVG Generated Correctly in: /path/to/file.svg"
</common_errors_and_fixes>

<example_usage>
**Recommended usage (with explicit coordinates):**
```python
from kerykeion import AstrologicalSubject, KerykeionChartSVG, NatalAspects

# Create subject with explicit coordinates (avoids GeoNames failures)
subject = AstrologicalSubject(
    name="Carl Jung",
    year=1875,
    month=7,
    day=26,
    hour=19,
    minute=20,
    lat=47.6,      # Kesswil, Switzerland
    lng=9.32,
    tz_str="Europe/Zurich"
)

# Access individual placements
print(f"Sun: {subject.sun.sign} {subject.sun.position:.2f}° (House {subject.sun.house})")
print(f"Moon: {subject.moon.sign} {subject.moon.position:.2f}° (House {subject.moon.house})")
print(f"Rising: {subject.first_house.sign} {subject.first_house.position:.2f}°")

# Get all planets
planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']
for planet_name in planets:
    planet = getattr(subject, planet_name)
    retro = "℞" if planet.retrograde else ""
    print(f"{planet.name}: {planet.sign} {planet.position:.2f}° {retro}")

# Get aspects
aspects = NatalAspects(subject)
for aspect in aspects.all_aspects[:5]:
    print(f"{aspect.p1_name} {aspect.aspect} {aspect.p2_name} (orb: {aspect.orbit:.2f}°)")

# Generate chart
chart = KerykeionChartSVG(subject)
chart.makeSVG()
# SVG saved to: /root/Carl Jung - Natal Chart.svg

# Get full data as dict
data = subject.model_dump()
# Access any field: data['sun'], data['first_house'], etc.
```
</example_usage>

<success_criteria>
A successful natal chart generation includes:
- ✅ Accurate planetary positions calculated
- ✅ House cusps determined
- ✅ Aspects between planets identified
- ✅ JSON data structure returned
- ✅ SVG chart file generated
- ✅ No astronomical calculation errors
- ✅ Timezone correctly applied
</success_criteria>

<interpretation_notes>
This skill provides **astronomical calculations** only. Astrological interpretation requires domain expertise. Key data points for interpretation:

- **Sun Sign**: Core identity, ego
- **Moon Sign**: Emotional nature
- **Rising Sign** (1st house): Outward personality
- **Major Aspects**: Conjunctions (0°), Oppositions (180°), Trines (120°), Squares (90°)
- **House Placements**: Life areas where planets express

For full interpretation, consult astrological resources or combine with interpretation libraries.
</interpretation_notes>
