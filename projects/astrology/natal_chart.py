"""
Natal Chart Generator Module

Generates comprehensive natal chart analysis including:
- Planet positions (sign, degree, house, retrograde)
- Element and modality distributions
- Stelliums and dominants
- MBTI and Enneagram inferences
- Full formatted report
"""

from kerykeion import AstrologicalSubject
from typing import Dict, List, Tuple, Optional
from collections import Counter


class NatalChart:
    """Complete natal chart analysis"""
    
    # Astrological mappings
    ELEMENTS = {
        'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
        'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
        'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
        'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
    }
    
    MODALITIES = {
        'Aries': 'Cardinal', 'Cancer': 'Cardinal', 'Libra': 'Cardinal', 'Capricorn': 'Cardinal',
        'Taurus': 'Fixed', 'Leo': 'Fixed', 'Scorpio': 'Fixed', 'Aquarius': 'Fixed',
        'Gemini': 'Mutable', 'Virgo': 'Mutable', 'Sagittarius': 'Mutable', 'Pisces': 'Mutable'
    }
    
    PLANET_NAMES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 
                    'Saturn', 'Uranus', 'Neptune', 'Pluto', 'True_Node', 'Chiron']
    
    PLANET_WEIGHTS = {
        'Sun': 10, 'Moon': 10, 'Mercury': 5, 'Venus': 5, 'Mars': 5,
        'Jupiter': 3, 'Saturn': 3, 'Uranus': 2, 'Neptune': 2, 'Pluto': 2,
        'True_Node': 1, 'Chiron': 1
    }
    
    def __init__(self, name: str, year: int, month: int, day: int, 
                 hour: int, minute: int, city: str = None, nation: str = None,
                 lat: float = None, lng: float = None, tz_str: str = "UTC"):
        """
        Initialize natal chart calculation
        
        Args:
            name: Person's name
            year, month, day: Birth date
            hour, minute: Birth time (24-hour format)
            city: Birth city (for automatic geocoding)
            nation: Birth country (for automatic geocoding)
            lat, lng: Manual coordinates (if city/nation not provided)
            tz_str: Timezone string (e.g., "Europe/Lisbon")
        """
        self.name = name
        
        # Create astrological subject
        if city and nation:
            self.subject = AstrologicalSubject(
                name=name,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                city=city,
                nation=nation,
                tz_str=tz_str
            )
        elif lat is not None and lng is not None:
            self.subject = AstrologicalSubject(
                name=name,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                lat=lat,
                lng=lng,
                tz_str=tz_str
            )
        else:
            raise ValueError("Must provide either (city, nation) or (lat, lng)")
        
        self.chart_data = self._build_chart_data()
    
    def _get_planet_info(self, planet_name: str) -> Dict:
        """Extract planet information from subject"""
        planet = getattr(self.subject, planet_name.lower(), None)
        if not planet:
            return None
        
        return {
            'name': planet_name.replace('_', ' '),
            'sign': planet['sign'],
            'degree': round(planet['position'], 2),
            'house': planet.get('house', 'Unknown'),
            'retrograde': planet.get('retrograde', False)
        }
    
    def _calculate_distributions(self) -> Tuple[Dict, Dict]:
        """Calculate element and modality distributions"""
        elements = []
        modalities = []
        
        for planet_name in self.PLANET_NAMES:
            info = self._get_planet_info(planet_name)
            if info and info['sign'] in self.ELEMENTS:
                weight = self.PLANET_WEIGHTS.get(planet_name, 1)
                elements.extend([self.ELEMENTS[info['sign']]] * weight)
                modalities.extend([self.MODALITIES[info['sign']]] * weight)
        
        element_dist = dict(Counter(elements))
        modality_dist = dict(Counter(modalities))
        
        return element_dist, modality_dist
    
    def _find_stelliums(self) -> List[Dict]:
        """Find stelliums (3+ planets in same sign or house)"""
        stelliums = []
        
        # Sign stelliums
        sign_planets = {}
        for planet_name in self.PLANET_NAMES:
            info = self._get_planet_info(planet_name)
            if info:
                sign = info['sign']
                if sign not in sign_planets:
                    sign_planets[sign] = []
                sign_planets[sign].append(info['name'])
        
        for sign, planets in sign_planets.items():
            if len(planets) >= 3:
                stelliums.append({
                    'type': 'sign',
                    'location': sign,
                    'planets': planets,
                    'count': len(planets)
                })
        
        # House stelliums
        house_planets = {}
        for planet_name in self.PLANET_NAMES:
            info = self._get_planet_info(planet_name)
            if info and info['house'] != 'Unknown':
                house = info['house']
                if house not in house_planets:
                    house_planets[house] = []
                house_planets[house].append(info['name'])
        
        for house, planets in house_planets.items():
            if len(planets) >= 3:
                stelliums.append({
                    'type': 'house',
                    'location': f"House {house}",
                    'planets': planets,
                    'count': len(planets)
                })
        
        return stelliums
    
    def _find_dominants(self, element_dist: Dict, modality_dist: Dict) -> Dict:
        """Find dominant planet, sign, element, modality"""
        # Dominant element and modality
        dominant_element = max(element_dist, key=element_dist.get) if element_dist else None
        dominant_modality = max(modality_dist, key=modality_dist.get) if modality_dist else None
        
        # Dominant planet (weighted by traditional rulership strength)
        planet_scores = {}
        for planet_name in self.PLANET_NAMES:
            info = self._get_planet_info(planet_name)
            if info:
                score = self.PLANET_WEIGHTS.get(planet_name, 1)
                planet_scores[planet_name] = score
        
        dominant_planet = max(planet_scores, key=planet_scores.get) if planet_scores else None
        
        # Dominant sign (most planets)
        sign_counts = {}
        for planet_name in self.PLANET_NAMES:
            info = self._get_planet_info(planet_name)
            if info:
                sign = info['sign']
                sign_counts[sign] = sign_counts.get(sign, 0) + self.PLANET_WEIGHTS.get(planet_name, 1)
        
        dominant_sign = max(sign_counts, key=sign_counts.get) if sign_counts else None
        
        return {
            'planet': dominant_planet,
            'sign': dominant_sign,
            'element': dominant_element,
            'modality': dominant_modality
        }
    
    def _infer_mbti(self, element_dist: Dict, modality_dist: Dict) -> str:
        """Infer MBTI type based on chart patterns"""
        # E/I: Fire + Air = E, Water + Earth = I
        fire_air = element_dist.get('Fire', 0) + element_dist.get('Air', 0)
        water_earth = element_dist.get('Water', 0) + element_dist.get('Earth', 0)
        ei = 'E' if fire_air > water_earth else 'I'
        
        # N/S: Air + Fire (intuitive) vs Earth (sensing)
        air_fire = element_dist.get('Air', 0) + element_dist.get('Fire', 0)
        earth = element_dist.get('Earth', 0)
        ns = 'N' if air_fire > earth * 1.2 else 'S'
        
        # T/F: Fire + Air (thinking) vs Water (feeling)
        fire = element_dist.get('Fire', 0)
        water = element_dist.get('Water', 0)
        
        # Check Mercury and Venus for refinement
        mercury = self._get_planet_info('Mercury')
        venus = self._get_planet_info('Venus')
        
        thinking_score = fire + element_dist.get('Air', 0) * 0.5
        feeling_score = water
        
        if mercury and self.ELEMENTS.get(mercury['sign']) in ['Air', 'Fire']:
            thinking_score += 5
        if venus and self.ELEMENTS.get(venus['sign']) in ['Water']:
            feeling_score += 5
        
        tf = 'T' if thinking_score > feeling_score else 'F'
        
        # J/P: Cardinal/Fixed vs Mutable
        mutable = modality_dist.get('Mutable', 0)
        cardinal_fixed = modality_dist.get('Cardinal', 0) + modality_dist.get('Fixed', 0)
        jp = 'P' if mutable > cardinal_fixed * 0.8 else 'J'
        
        return f"{ei}{ns}{tf}{jp}"
    
    def _infer_enneagram(self) -> Tuple[int, str]:
        """Infer Enneagram type based on chart patterns"""
        scores = {i: 0 for i in range(1, 10)}
        
        # Get key planets
        sun = self._get_planet_info('Sun')
        moon = self._get_planet_info('Moon')
        mars = self._get_planet_info('Mars')
        venus = self._get_planet_info('Venus')
        saturn = self._get_planet_info('Saturn')
        mercury = self._get_planet_info('Mercury')
        jupiter = self._get_planet_info('Jupiter')
        
        # Type 1: Saturn prominent, Virgo/Capricorn emphasis
        if saturn and saturn['house'] in [1, 10]:
            scores[1] += 3
        if sun and sun['sign'] in ['Virgo', 'Capricorn']:
            scores[1] += 2
        
        # Type 2: Venus prominent, Libra/Cancer emphasis
        if venus and venus['house'] in [1, 7]:
            scores[2] += 3
        if moon and moon['sign'] in ['Cancer', 'Libra']:
            scores[2] += 2
        
        # Type 3: Sun/Mars in 10th, Leo/Aries emphasis
        if sun and sun['house'] == 10:
            scores[3] += 3
        if sun and sun['sign'] in ['Leo', 'Aries', 'Capricorn']:
            scores[3] += 2
        
        # Type 4: Moon in water signs, 4th/8th/12th house emphasis
        if moon and moon['sign'] in ['Cancer', 'Scorpio', 'Pisces']:
            scores[4] += 3
        if moon and moon['house'] in [4, 8, 12]:
            scores[4] += 2
        
        # Type 5: Mercury/Saturn prominent, Aquarius/Virgo emphasis
        if mercury and mercury['house'] in [1, 3, 9]:
            scores[5] += 3
        if sun and sun['sign'] in ['Aquarius', 'Virgo', 'Gemini']:
            scores[5] += 2
        
        # Type 6: Moon prominent, Cancer/Virgo emphasis
        if moon and moon['house'] == 1:
            scores[6] += 3
        if sun and sun['sign'] in ['Cancer', 'Virgo']:
            scores[6] += 2
        
        # Type 7: Jupiter/Sagittarius prominent
        if jupiter and jupiter['house'] in [1, 9]:
            scores[7] += 3
        if sun and sun['sign'] in ['Sagittarius', 'Gemini', 'Aquarius']:
            scores[7] += 2
        
        # Type 8: Mars/Pluto prominent, Scorpio/Aries emphasis
        if mars and mars['house'] in [1, 8, 10]:
            scores[8] += 3
        if sun and sun['sign'] in ['Scorpio', 'Aries']:
            scores[8] += 2
        
        # Type 9: Venus/Neptune, Pisces/Libra emphasis
        if sun and sun['sign'] in ['Pisces', 'Libra', 'Taurus']:
            scores[9] += 2
        if moon and moon['sign'] in ['Pisces', 'Libra']:
            scores[9] += 2
        
        primary_type = max(scores, key=scores.get)
        secondary_type = sorted(scores, key=scores.get, reverse=True)[1]
        
        # Determine wing
        possible_wings = [primary_type - 1, primary_type + 1]
        possible_wings = [w if 1 <= w <= 9 else (9 if w == 0 else 1) for w in possible_wings]
        wing = max(possible_wings, key=lambda w: scores[w])
        
        return primary_type, f"{primary_type}w{wing}"
    
    def _build_chart_data(self) -> Dict:
        """Build complete chart data structure"""
        # Get all planet positions
        planets = {}
        for planet_name in self.PLANET_NAMES:
            info = self._get_planet_info(planet_name)
            if info:
                planets[planet_name] = info
        
        # Calculate distributions
        element_dist, modality_dist = self._calculate_distributions()
        
        # Find stelliums and dominants
        stelliums = self._find_stelliums()
        dominants = self._find_dominants(element_dist, modality_dist)
        
        # Infer personality types
        mbti = self._infer_mbti(element_dist, modality_dist)
        enneagram_type, enneagram_wing = self._infer_enneagram()
        
        # Big Three
        big_three = {
            'sun': planets.get('Sun'),
            'moon': planets.get('Moon'),
            'rising': {
                'sign': self.subject.first_house['sign'],
                'degree': round(self.subject.first_house['position'], 2)
            }
        }
        
        return {
            'name': self.name,
            'birth_data': {
                'date': f"{self.subject.year}-{self.subject.month:02d}-{self.subject.day:02d}",
                'time': f"{self.subject.hour:02d}:{self.subject.minute:02d}",
                'location': f"{self.subject.city}, {self.subject.nation}" if self.subject.city else f"{self.subject.lat}, {self.subject.lng}",
                'timezone': self.subject.tz_str
            },
            'big_three': big_three,
            'planets': planets,
            'element_distribution': element_dist,
            'modality_distribution': modality_dist,
            'stelliums': stelliums,
            'dominants': dominants,
            'mbti': mbti,
            'enneagram': {
                'type': enneagram_type,
                'wing': enneagram_wing
            }
        }
    
    def get_data(self) -> Dict:
        """Return complete chart data"""
        return self.chart_data
    
    def generate_report(self) -> str:
        """Generate formatted text report"""
        data = self.chart_data
        report = []
        
        report.append("=" * 80)
        report.append(f"NATAL CHART ANALYSIS: {data['name'].upper()}")
        report.append("=" * 80)
        
        # Birth data
        bd = data['birth_data']
        report.append(f"\nBirth Date: {bd['date']} at {bd['time']}")
        report.append(f"Location: {bd['location']}")
        report.append(f"Timezone: {bd['timezone']}")
        
        # Big Three
        report.append("\n" + "-" * 80)
        report.append("THE BIG THREE")
        report.append("-" * 80)
        sun = data['big_three']['sun']
        moon = data['big_three']['moon']
        rising = data['big_three']['rising']
        
        report.append(f"Sun: {sun['sign']} {sun['degree']}° (House {sun['house']})")
        report.append(f"Moon: {moon['sign']} {moon['degree']}° (House {moon['house']})")
        report.append(f"Rising (Ascendant): {rising['sign']} {rising['degree']}°")
        
        # All planets
        report.append("\n" + "-" * 80)
        report.append("PLANETARY POSITIONS")
        report.append("-" * 80)
        for planet_name, planet in data['planets'].items():
            retro = " ℞" if planet['retrograde'] else ""
            report.append(f"{planet['name']:12} | {planet['sign']:12} {planet['degree']:6.2f}° | House {planet['house']}{retro}")
        
        # Element & Modality
        report.append("\n" + "-" * 80)
        report.append("ELEMENT & MODALITY DISTRIBUTION")
        report.append("-" * 80)
        
        report.append("\nElements:")
        for element in ['Fire', 'Earth', 'Air', 'Water']:
            count = data['element_distribution'].get(element, 0)
            bar = "█" * (count // 2)
            report.append(f"  {element:8} | {count:3} {bar}")
        
        report.append("\nModalities:")
        for modality in ['Cardinal', 'Fixed', 'Mutable']:
            count = data['modality_distribution'].get(modality, 0)
            bar = "█" * (count // 2)
            report.append(f"  {modality:8} | {count:3} {bar}")
        
        # Dominants
        report.append("\n" + "-" * 80)
        report.append("CHART DOMINANTS")
        report.append("-" * 80)
        dom = data['dominants']
        report.append(f"Dominant Element: {dom['element']}")
        report.append(f"Dominant Modality: {dom['modality']}")
        report.append(f"Dominant Sign: {dom['sign']}")
        report.append(f"Dominant Planet: {dom['planet']}")
        
        # Stelliums
        if data['stelliums']:
            report.append("\n" + "-" * 80)
            report.append("STELLIUMS (3+ planets)")
            report.append("-" * 80)
            for stellium in data['stelliums']:
                planets_str = ", ".join(stellium['planets'])
                report.append(f"{stellium['location']} ({stellium['count']} planets): {planets_str}")
        
        # Personality Inferences
        report.append("\n" + "-" * 80)
        report.append("PERSONALITY TYPE INFERENCES")
        report.append("-" * 80)
        report.append(f"MBTI (inferred): {data['mbti']}")
        report.append(f"Enneagram (inferred): Type {data['enneagram']['type']} (likely {data['enneagram']['wing']})")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


def generate_natal_chart(name: str, year: int, month: int, day: int,
                        hour: int, minute: int, city: str = None, 
                        nation: str = None, lat: float = None, 
                        lng: float = None) -> Dict:
    """
    Convenience function to generate natal chart
    
    Returns: Complete chart data dictionary
    """
    chart = NatalChart(name, year, month, day, hour, minute, 
                      city=city, nation=nation, lat=lat, lng=lng)
    return chart.get_data()
