"""
Compatibility Analysis Module

Analyzes relationship compatibility between two natal charts including:
- Synastry aspects (conjunctions, trines, squares, oppositions, sextiles)
- Element and modality compatibility
- MBTI and Enneagram pairing analysis
- Category scores (Romance, Friendship, Business, Communication, Conflict)
- Strengths, challenges, and predictions
"""

from typing import Dict, List, Tuple
import math


class Compatibility:
    """Relationship compatibility analyzer"""
    
    # Aspect orbs (degrees of separation)
    ASPECT_ORBS = {
        'conjunction': 8,
        'opposition': 8,
        'trine': 6,
        'square': 6,
        'sextile': 4
    }
    
    # Aspect angles
    ASPECT_ANGLES = {
        'conjunction': 0,
        'opposition': 180,
        'trine': 120,
        'square': 90,
        'sextile': 60
    }
    
    # Aspect scores (positive = harmonious, negative = challenging)
    ASPECT_SCORES = {
        'conjunction': 5,  # Neutral/intense
        'trine': 8,        # Very harmonious
        'sextile': 6,      # Harmonious
        'opposition': -4,  # Challenging but dynamic
        'square': -6       # Most challenging
    }
    
    # Element compatibility matrix
    ELEMENT_COMPATIBILITY = {
        ('Fire', 'Fire'): 7,
        ('Fire', 'Earth'): 3,
        ('Fire', 'Air'): 8,
        ('Fire', 'Water'): 4,
        ('Earth', 'Earth'): 7,
        ('Earth', 'Air'): 3,
        ('Earth', 'Water'): 8,
        ('Air', 'Air'): 7,
        ('Air', 'Water'): 4,
        ('Water', 'Water'): 7
    }
    
    # MBTI compatibility scores (simplified)
    MBTI_COMPATIBILITY = {
        'same': 6,
        'one_diff': 7,
        'two_diff': 8,
        'three_diff': 5,
        'opposite': 4
    }
    
    # Key planets for relationship analysis
    RELATIONSHIP_PLANETS = ['Sun', 'Moon', 'Venus', 'Mars', 'Mercury']
    
    def __init__(self, chart1: Dict, chart2: Dict):
        """
        Initialize compatibility analysis
        
        Args:
            chart1: First natal chart data (from natal_chart.py)
            chart2: Second natal chart data (from natal_chart.py)
        """
        self.chart1 = chart1
        self.chart2 = chart2
        self.name1 = chart1['name']
        self.name2 = chart2['name']
        
        self.analysis = self._analyze()
    
    def _calculate_angle_difference(self, deg1: float, deg2: float) -> float:
        """Calculate shortest angle between two positions"""
        diff = abs(deg1 - deg2)
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def _find_aspects(self) -> List[Dict]:
        """Find all significant aspects between the two charts"""
        aspects = []
        
        # Convert planet positions to absolute degrees
        def get_absolute_degree(planet_data):
            # This is simplified - in real impl, need to calculate from sign + degree
            # For now, use the degree directly (kerykeion gives absolute position)
            return planet_data['degree']
        
        for planet1_name, planet1_data in self.chart1['planets'].items():
            if planet1_name not in self.RELATIONSHIP_PLANETS:
                continue
                
            for planet2_name, planet2_data in self.chart2['planets'].items():
                if planet2_name not in self.RELATIONSHIP_PLANETS:
                    continue
                
                deg1 = planet1_data['degree']
                deg2 = planet2_data['degree']
                
                # Check each aspect type
                for aspect_name, target_angle in self.ASPECT_ANGLES.items():
                    orb = self.ASPECT_ORBS[aspect_name]
                    angle_diff = self._calculate_angle_difference(deg1, deg2)
                    
                    # Check if within orb
                    if abs(angle_diff - target_angle) <= orb:
                        aspects.append({
                            'planet1': f"{self.name1}'s {planet1_name}",
                            'planet2': f"{self.name2}'s {planet2_name}",
                            'aspect': aspect_name,
                            'orb': abs(angle_diff - target_angle),
                            'score': self.ASPECT_SCORES[aspect_name],
                            'sign1': planet1_data['sign'],
                            'sign2': planet2_data['sign']
                        })
        
        return sorted(aspects, key=lambda x: abs(x['score']), reverse=True)
    
    def _calculate_element_compatibility(self) -> Dict:
        """Calculate element compatibility score"""
        elem1 = self.chart1['dominants']['element']
        elem2 = self.chart2['dominants']['element']
        
        # Get compatibility score
        pair = (elem1, elem2) if (elem1, elem2) in self.ELEMENT_COMPATIBILITY else (elem2, elem1)
        score = self.ELEMENT_COMPATIBILITY.get(pair, 5)
        
        # Distribution similarity
        dist1 = self.chart1['element_distribution']
        dist2 = self.chart2['element_distribution']
        
        compatibility_details = {
            'dominant_elements': f"{elem1} + {elem2}",
            'score': score,
            'interpretation': self._interpret_element_pairing(elem1, elem2)
        }
        
        return compatibility_details
    
    def _interpret_element_pairing(self, elem1: str, elem2: str) -> str:
        """Interpret element pairing"""
        if elem1 == elem2:
            return f"Both {elem1} - Similar energy and approach to life"
        elif (elem1 in ['Fire', 'Air'] and elem2 in ['Fire', 'Air']):
            return "Yang elements - Active, outgoing, mentally/spiritually focused"
        elif (elem1 in ['Earth', 'Water'] and elem2 in ['Earth', 'Water']):
            return "Yin elements - Receptive, grounded, physically/emotionally focused"
        elif (elem1 == 'Fire' and elem2 == 'Air') or (elem1 == 'Air' and elem2 == 'Fire'):
            return "Fire + Air - Highly compatible, stimulating and energizing"
        elif (elem1 == 'Earth' and elem2 == 'Water') or (elem1 == 'Water' and elem2 == 'Earth'):
            return "Earth + Water - Highly compatible, nurturing and stable"
        else:
            return "Complementary elements - Different approaches that can balance or clash"
    
    def _calculate_modality_compatibility(self) -> Dict:
        """Calculate modality compatibility"""
        mod1 = self.chart1['dominants']['modality']
        mod2 = self.chart2['dominants']['modality']
        
        if mod1 == mod2:
            score = 6
            interp = f"Both {mod1} - Similar pace and approach to change"
        elif 'Cardinal' in [mod1, mod2] and 'Mutable' in [mod1, mod2]:
            score = 7
            interp = "Cardinal + Mutable - Initiative meets adaptability"
        elif 'Fixed' in [mod1, mod2] and 'Mutable' in [mod1, mod2]:
            score = 6
            interp = "Fixed + Mutable - Stability meets flexibility"
        else:  # Cardinal + Fixed
            score = 5
            interp = "Cardinal + Fixed - Action meets resistance"
        
        return {
            'modalities': f"{mod1} + {mod2}",
            'score': score,
            'interpretation': interp
        }
    
    def _analyze_mbti_pairing(self) -> Dict:
        """Analyze MBTI compatibility"""
        mbti1 = self.chart1['mbti']
        mbti2 = self.chart2['mbti']
        
        # Count differences
        differences = sum(1 for a, b in zip(mbti1, mbti2) if a != b)
        
        if differences == 0:
            category = 'same'
            interp = "Identical types - Deep understanding but may lack growth tension"
        elif differences == 1:
            category = 'one_diff'
            interp = "Very similar - Easy understanding with slight differences"
        elif differences == 2:
            category = 'two_diff'
            interp = "Complementary - Balanced similarities and differences"
        elif differences == 3:
            category = 'three_diff'
            interp = "Contrasting - Requires effort but can be rewarding"
        else:
            category = 'opposite'
            interp = "Opposite types - Challenging but potentially transformative"
        
        score = self.MBTI_COMPATIBILITY[category]
        
        return {
            'types': f"{mbti1} + {mbti2}",
            'score': score,
            'differences': differences,
            'interpretation': interp
        }
    
    def _analyze_enneagram_pairing(self) -> Dict:
        """Analyze Enneagram compatibility"""
        type1 = self.chart1['enneagram']['type']
        type2 = self.chart2['enneagram']['type']
        
        # Simplified compatibility matrix
        # Certain pairs work better together
        harmonious_pairs = [
            (1, 2), (1, 7), (2, 4), (2, 8), (3, 7), (3, 9),
            (4, 5), (4, 9), (5, 8), (6, 9), (7, 8)
        ]
        
        pair = tuple(sorted([type1, type2]))
        is_harmonious = pair in harmonious_pairs or pair in [(b, a) for a, b in harmonious_pairs]
        
        if type1 == type2:
            score = 6
            interp = f"Both Type {type1} - Deep understanding but may amplify weaknesses"
        elif is_harmonious:
            score = 8
            interp = f"Type {type1} + Type {type2} - Naturally complementary pairing"
        else:
            score = 5
            interp = f"Type {type1} + Type {type2} - Requires conscious effort"
        
        return {
            'types': f"{self.chart1['enneagram']['wing']} + {self.chart2['enneagram']['wing']}",
            'score': score,
            'interpretation': interp
        }
    
    def _calculate_category_scores(self, aspects: List[Dict]) -> Dict:
        """Calculate scores by relationship category"""
        # Base scores from aspects
        aspect_total = sum(a['score'] for a in aspects)
        aspect_avg = aspect_total / len(aspects) if aspects else 0
        
        # Get key aspects
        sun_moon = [a for a in aspects if 'Sun' in a['planet1'] and 'Moon' in a['planet2'] or 
                    'Moon' in a['planet1'] and 'Sun' in a['planet2']]
        venus_mars = [a for a in aspects if 'Venus' in a['planet1'] and 'Mars' in a['planet2'] or
                     'Mars' in a['planet1'] and 'Venus' in a['planet2']]
        mercury = [a for a in aspects if 'Mercury' in a['planet1'] or 'Mercury' in a['planet2']]
        
        # Romance: Venus, Mars, Sun-Moon aspects
        romance = 50 + aspect_avg * 3
        if sun_moon:
            romance += sum(a['score'] * 2 for a in sun_moon)
        if venus_mars:
            romance += sum(a['score'] * 3 for a in venus_mars)
        
        # Friendship: Sun, Mercury aspects
        friendship = 50 + aspect_avg * 3
        if mercury:
            friendship += sum(a['score'] * 2 for a in mercury)
        
        # Business: Saturn, Mars, Sun aspects
        business = 50 + aspect_avg * 2
        business += self._calculate_modality_compatibility()['score'] * 2
        
        # Communication: Mercury aspects
        communication = 50 + aspect_avg * 2
        if mercury:
            communication += sum(a['score'] * 3 for a in mercury)
        
        # Conflict Resolution: Moon, Mars aspects
        conflict = 50 - (aspect_avg * 2) if aspect_avg < 0 else 50 + (aspect_avg * 2)
        
        # Normalize to 0-100
        def normalize(score):
            return max(0, min(100, score))
        
        return {
            'romance': normalize(romance),
            'friendship': normalize(friendship),
            'business': normalize(business),
            'communication': normalize(communication),
            'conflict_resolution': normalize(conflict)
        }
    
    def _identify_strengths(self, aspects: List[Dict], categories: Dict) -> List[str]:
        """Identify relationship strengths"""
        strengths = []
        
        # Check harmonious aspects
        harmonious = [a for a in aspects if a['score'] > 0]
        if len(harmonious) >= 5:
            strengths.append("Multiple harmonious planetary connections")
        
        # Check specific beneficial aspects
        for aspect in harmonious[:3]:  # Top 3
            if aspect['aspect'] == 'trine':
                strengths.append(f"{aspect['planet1']} trine {aspect['planet2']} - Natural flow and ease")
            elif aspect['aspect'] == 'sextile':
                strengths.append(f"{aspect['planet1']} sextile {aspect['planet2']} - Opportunities for growth")
        
        # Check category scores
        if categories['romance'] >= 70:
            strengths.append("Strong romantic chemistry and attraction")
        if categories['communication'] >= 70:
            strengths.append("Excellent communication and understanding")
        if categories['friendship'] >= 70:
            strengths.append("Solid foundation of friendship and mutual respect")
        
        return strengths[:5]  # Top 5
    
    def _identify_challenges(self, aspects: List[Dict], categories: Dict) -> List[str]:
        """Identify relationship challenges"""
        challenges = []
        
        # Check difficult aspects
        difficult = [a for a in aspects if a['score'] < 0]
        
        for aspect in difficult[:3]:  # Top 3 most challenging
            if aspect['aspect'] == 'square':
                challenges.append(f"{aspect['planet1']} square {aspect['planet2']} - Requires conscious effort to harmonize")
            elif aspect['aspect'] == 'opposition':
                challenges.append(f"{aspect['planet1']} opposite {aspect['planet2']} - Need to balance opposing needs")
        
        # Check category scores
        if categories['communication'] < 50:
            challenges.append("Communication styles may differ significantly")
        if categories['conflict_resolution'] < 50:
            challenges.append("Conflict resolution requires patience and effort")
        
        if not challenges:
            challenges.append("No major astrological challenges - focus on personal growth areas")
        
        return challenges[:5]  # Top 5
    
    def _generate_predictions(self, overall_score: int) -> Dict:
        """Generate best/worst case predictions"""
        if overall_score >= 75:
            best = "Deeply fulfilling partnership with natural harmony, mutual growth, and lasting connection"
            worst = "Risk of complacency or taking the relationship for granted"
        elif overall_score >= 60:
            best = "Strong partnership with good potential for long-term success through mutual effort"
            worst = "Occasional friction that requires active communication and compromise"
        elif overall_score >= 45:
            best = "Relationship can work with significant conscious effort and commitment from both parties"
            worst = "Recurring challenges may lead to frustration without strong foundation"
        else:
            best = "Opportunity for significant personal growth through navigating differences"
            worst = "Fundamental differences may create persistent tension and difficulty"
        
        return {
            'best_case': best,
            'worst_case': worst
        }
    
    def _analyze(self) -> Dict:
        """Perform complete compatibility analysis"""
        # Find aspects
        aspects = self._find_aspects()
        
        # Element and modality
        element_compat = self._calculate_element_compatibility()
        modality_compat = self._calculate_modality_compatibility()
        
        # Personality types
        mbti_compat = self._analyze_mbti_pairing()
        enneagram_compat = self._analyze_enneagram_pairing()
        
        # Category scores
        category_scores = self._calculate_category_scores(aspects)
        
        # Calculate overall score
        aspect_score = sum(a['score'] for a in aspects) / len(aspects) if aspects else 0
        aspect_normalized = ((aspect_score + 6) / 12) * 100  # Normalize -6 to +8 range to 0-100
        
        overall_score = (
            aspect_normalized * 0.30 +
            element_compat['score'] * 10 * 0.15 +
            modality_compat['score'] * 10 * 0.10 +
            mbti_compat['score'] * 10 * 0.15 +
            enneagram_compat['score'] * 10 * 0.10 +
            sum(category_scores.values()) / len(category_scores) * 0.20
        )
        
        overall_score = max(0, min(100, overall_score))
        
        # Identify strengths and challenges
        strengths = self._identify_strengths(aspects, category_scores)
        challenges = self._identify_challenges(aspects, category_scores)
        
        # Predictions
        predictions = self._generate_predictions(overall_score)
        
        return {
            'overall_score': round(overall_score, 1),
            'aspects': aspects,
            'element_compatibility': element_compat,
            'modality_compatibility': modality_compat,
            'mbti_compatibility': mbti_compat,
            'enneagram_compatibility': enneagram_compat,
            'category_scores': category_scores,
            'strengths': strengths,
            'challenges': challenges,
            'predictions': predictions
        }
    
    def get_data(self) -> Dict:
        """Return complete compatibility analysis"""
        return self.analysis
    
    def generate_report(self) -> str:
        """Generate formatted compatibility report"""
        data = self.analysis
        report = []
        
        report.append("=" * 80)
        report.append(f"RELATIONSHIP COMPATIBILITY ANALYSIS")
        report.append(f"{self.name1.upper()} & {self.name2.upper()}")
        report.append("=" * 80)
        
        # Overall score
        score = data['overall_score']
        report.append(f"\nOVERALL COMPATIBILITY SCORE: {score}/100")
        
        if score >= 75:
            rating = "EXCELLENT - Highly Compatible"
        elif score >= 60:
            rating = "GOOD - Strong Potential"
        elif score >= 45:
            rating = "MODERATE - Requires Effort"
        else:
            rating = "CHALLENGING - Significant Work Needed"
        
        report.append(f"Rating: {rating}")
        
        # Category scores
        report.append("\n" + "-" * 80)
        report.append("COMPATIBILITY BY CATEGORY")
        report.append("-" * 80)
        
        cats = data['category_scores']
        for category, score in cats.items():
            bar = "█" * int(score / 5)
            report.append(f"{category.replace('_', ' ').title():20} | {score:5.1f}/100 {bar}")
        
        # Element & Modality
        report.append("\n" + "-" * 80)
        report.append("ELEMENT & MODALITY COMPATIBILITY")
        report.append("-" * 80)
        
        elem = data['element_compatibility']
        report.append(f"\nElements: {elem['dominant_elements']}")
        report.append(f"Score: {elem['score']}/10")
        report.append(f"{elem['interpretation']}")
        
        mod = data['modality_compatibility']
        report.append(f"\nModalities: {mod['modalities']}")
        report.append(f"Score: {mod['score']}/10")
        report.append(f"{mod['interpretation']}")
        
        # MBTI & Enneagram
        report.append("\n" + "-" * 80)
        report.append("PERSONALITY TYPE COMPATIBILITY")
        report.append("-" * 80)
        
        mbti = data['mbti_compatibility']
        report.append(f"\nMBTI: {mbti['types']}")
        report.append(f"Score: {mbti['score']}/10")
        report.append(f"{mbti['interpretation']}")
        
        ennea = data['enneagram_compatibility']
        report.append(f"\nEnneagram: {ennea['types']}")
        report.append(f"Score: {ennea['score']}/10")
        report.append(f"{ennea['interpretation']}")
        
        # Key Synastry Aspects
        report.append("\n" + "-" * 80)
        report.append("KEY SYNASTRY ASPECTS")
        report.append("-" * 80)
        
        if data['aspects']:
            # Show top 10 most significant aspects
            for aspect in data['aspects'][:10]:
                score_indicator = "+" if aspect['score'] > 0 else "-"
                report.append(f"{aspect['planet1']:25} {aspect['aspect'].upper():12} {aspect['planet2']:25} [{score_indicator}{abs(aspect['score'])}]")
        else:
            report.append("No major aspects found within standard orbs")
        
        # Strengths
        report.append("\n" + "-" * 80)
        report.append("RELATIONSHIP STRENGTHS")
        report.append("-" * 80)
        for i, strength in enumerate(data['strengths'], 1):
            report.append(f"{i}. {strength}")
        
        # Challenges
        report.append("\n" + "-" * 80)
        report.append("RELATIONSHIP CHALLENGES")
        report.append("-" * 80)
        for i, challenge in enumerate(data['challenges'], 1):
            report.append(f"{i}. {challenge}")
        
        # Predictions
        report.append("\n" + "-" * 80)
        report.append("RELATIONSHIP OUTLOOK")
        report.append("-" * 80)
        
        pred = data['predictions']
        report.append(f"\nBest Case Scenario:")
        report.append(f"  {pred['best_case']}")
        report.append(f"\nWorst Case Scenario:")
        report.append(f"  {pred['worst_case']}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


def analyze_compatibility(chart1: Dict, chart2: Dict) -> Dict:
    """
    Convenience function to analyze compatibility
    
    Args:
        chart1: First natal chart (from natal_chart.generate_natal_chart)
        chart2: Second natal chart (from natal_chart.generate_natal_chart)
    
    Returns: Complete compatibility analysis dictionary
    """
    compat = Compatibility(chart1, chart2)
    return compat.get_data()
