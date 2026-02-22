# Astrology App - Natal Charts & Compatibility Analysis

A complete, production-ready Python astrology application for generating comprehensive natal charts and relationship compatibility analysis.

## Features

### Natal Chart Module (`natal_chart.py`)
- **Complete planetary positions**: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, North Node, Chiron
- **Big Three**: Sun sign, Moon sign, and Rising sign with degrees and houses
- **Element distribution**: Fire, Earth, Air, Water counts
- **Modality distribution**: Cardinal, Fixed, Mutable counts
- **Stelliums**: Identifies 3+ planets in same sign or house
- **Dominant analysis**: Dominant planet, sign, element, and modality
- **MBTI inference**: Based on elemental and planetary patterns
- **Enneagram inference**: Based on planetary positions and aspects
- **Professional formatted reports**

### Compatibility Module (`compatibility.py`)
- **Overall compatibility score** (0-100)
- **Synastry aspects**: Conjunctions, trines, squares, oppositions, sextiles
- **Element compatibility**: Analysis of elemental pairings
- **Modality compatibility**: Cardinal, Fixed, Mutable interactions
- **MBTI pairing analysis**: Compatibility based on inferred types
- **Enneagram pairing analysis**: Type interaction dynamics
- **Category scores**: Romance, Friendship, Business, Communication, Conflict Resolution
- **Relationship insights**: Strengths, challenges, and predictions
- **Professional formatted reports**

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Generate Natal Chart
```bash
python main.py natal \
  --name "John" \
  --date 1977-06-06 \
  --time 09:00 \
  --city "Marinha Grande" \
  --country "Portugal"
```

#### Compare Two Charts
```bash
python main.py compare \
  --name1 "Person1" \
  --date1 1977-06-06 \
  --time1 09:00 \
  --city1 "Marinha Grande" \
  --country1 "Portugal" \
  --name2 "Person2" \
  --date2 1982-07-29 \
  --time2 14:00 \
  --city2 "Porto" \
  --country2 "Portugal"
```

#### Save Output to File
```bash
python main.py natal --name "John" --date 1977-06-06 --time 09:00 \
  --city "Marinha Grande" --country "Portugal" \
  --output chart_output.txt
```

### Python API

#### Generate Natal Chart
```python
from natal_chart import NatalChart

chart = NatalChart(
    name="John Doe",
    year=1977,
    month=6,
    day=6,
    hour=9,
    minute=0,
    city="Marinha Grande",
    nation="Portugal"
)

# Get structured data
chart_data = chart.get_data()

# Generate formatted report
report = chart.generate_report()
print(report)
```

#### Analyze Compatibility
```python
from natal_chart import NatalChart
from compatibility import Compatibility

# Create two charts
chart1 = NatalChart(name="Person1", year=1977, month=6, day=6, 
                   hour=9, minute=0, city="Marinha Grande", nation="Portugal")
chart2 = NatalChart(name="Person2", year=1982, month=7, day=29,
                   hour=14, minute=0, city="Porto", nation="Portugal")

# Analyze compatibility
compat = Compatibility(chart1.get_data(), chart2.get_data())

# Get structured data
compat_data = compat.get_data()

# Generate formatted report
report = compat.generate_report()
print(report)
```

#### Using Manual Coordinates
```python
chart = NatalChart(
    name="John Doe",
    year=1977,
    month=6,
    day=6,
    hour=9,
    minute=0,
    lat=39.7467,
    lng=-8.9333,
    tz_str="Europe/Lisbon"
)
```

## Data Structure

### Natal Chart Data
```python
{
    'name': str,
    'birth_data': {
        'date': str,
        'time': str,
        'location': str,
        'timezone': str
    },
    'big_three': {
        'sun': {...},
        'moon': {...},
        'rising': {...}
    },
    'planets': {
        'Sun': {'name', 'sign', 'degree', 'house', 'retrograde'},
        'Moon': {...},
        # ... all planets
    },
    'element_distribution': {'Fire': int, 'Earth': int, 'Air': int, 'Water': int},
    'modality_distribution': {'Cardinal': int, 'Fixed': int, 'Mutable': int},
    'stelliums': [{'type', 'location', 'planets', 'count'}, ...],
    'dominants': {'planet', 'sign', 'element', 'modality'},
    'mbti': str,
    'enneagram': {'type': int, 'wing': str}
}
```

### Compatibility Data
```python
{
    'overall_score': float,  # 0-100
    'aspects': [{'planet1', 'planet2', 'aspect', 'orb', 'score'}, ...],
    'element_compatibility': {'dominant_elements', 'score', 'interpretation'},
    'modality_compatibility': {'modalities', 'score', 'interpretation'},
    'mbti_compatibility': {'types', 'score', 'differences', 'interpretation'},
    'enneagram_compatibility': {'types', 'score', 'interpretation'},
    'category_scores': {
        'romance': float,
        'friendship': float,
        'business': float,
        'communication': float,
        'conflict_resolution': float
    },
    'strengths': [str, ...],
    'challenges': [str, ...],
    'predictions': {'best_case': str, 'worst_case': str}
}
```

## Test Data

The app has been tested with three real birth charts:

1. **Chart 1**: June 6, 1977 @ 09:00, Marinha Grande, Portugal
2. **Chart 2**: February 19, 1985 @ 12:00, Lisbon, Portugal
3. **Chart 3**: July 29, 1982 @ 14:00, Porto, Portugal

Test outputs are available in:
- `test_output_natal_chart_1.txt`
- `test_output_natal_chart_2.txt`
- `test_output_natal_chart_3.txt`
- `test_output_compatibility_chart1_chart3.txt`
- `test_output_compatibility_chart1_chart2.txt`

## Requirements

- Python 3.8+
- kerykeion 4.15.0
- pytz

## Technical Notes

- Uses **kerykeion** library for astrological calculations
- Timezone-aware calculations using pytz
- Supports both city/country lookup and manual lat/lng coordinates
- Professional formatting with ASCII art charts
- Comprehensive error handling
- Clean, well-documented code

## License

MIT License - Free to use and modify
