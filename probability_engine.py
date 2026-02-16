import statistics
from typing import Dict, List

class ProbabilityEngine:
    """Calculate player prop probabilities and Expected Value"""
    
    def __init__(self):
        self.weights = {
            'season': 0.40,
            'recent': 0.30,
            'current': 0.20,
            'matchup': 0.10
        }
    
    def calculate_three_point_probability(self, player_data: Dict) -> float:
        """
        Calculate probability player hits next 3-pointer
        
        Args:
            player_data: {
                'season_3pt_pct': 0.42,  # Season average
                'recent_games_3pt': [0.5, 0.33, 0.4, 0.5, 0.25],  # Last 5 games
                'current_game_3pt': 0.6,  # Made 3/5 so far today
                'defender_3pt_allowed': 0.38  # Defender allows 38% normally
            }
        
        Returns:
            float: Probability (0.0 to 1.0)
        """
        
        # Season average
        season_component = player_data.get('season_3pt_pct', 0.35)
        
        # Recent form (average of last 5 games)
        recent_games = player_data.get('recent_games_3pt', [])
        if recent_games:
            recent_component = statistics.mean(recent_games)
        else:
            recent_component = season_component  # Fall back to season avg
        
        # Current game performance
        current_component = player_data.get('current_game_3pt', season_component)
        
        # Matchup factor (how good is defender?)
        defender_allowed = player_data.get('defender_3pt_allowed', 0.35)
        # If defender allows more 3s, player's probability increases
        matchup_boost = (defender_allowed - 0.35) * 0.5  # Scale the impact
        matchup_component = season_component + matchup_boost
        
        # Weighted average
        probability = (
            season_component * self.weights['season'] +
            recent_component * self.weights['recent'] +
            current_component * self.weights['current'] +
            matchup_component * self.weights['matchup']
        )
        
        # Clamp between 0.1 and 0.9 (nothing is certain)
        return max(0.1, min(0.9, probability))
    
    def american_odds_to_decimal(self, american_odds: int) -> float:
        """Convert American odds to decimal odds"""
        if american_odds > 0:
            return (american_odds / 100.0) + 1.0
        else:
            return (100.0 / abs(american_odds)) + 1.0
    
    def american_odds_to_probability(self, american_odds: int) -> float:
        """Convert American odds to implied probability"""
        decimal_odds = self.american_odds_to_decimal(american_odds)
        return 1.0 / decimal_odds
    
    def calculate_expected_value(self, our_probability: float, american_odds: int, stake: float = 100.0) -> Dict:
        """
        Calculate Expected Value of a bet
        
        Args:
            our_probability: Our calculated probability (0.0 to 1.0)
            american_odds: Sportsbook odds (e.g., +180, -150)
            stake: Bet amount in dollars
        
        Returns:
            Dict with EV analysis
        """
        decimal_odds = self.american_odds_to_decimal(american_odds)
        implied_probability = self.american_odds_to_probability(american_odds)
        
        # Potential profit
        potential_profit = stake * (decimal_odds - 1.0)
        
        # Expected Value calculation
        ev = (our_probability * potential_profit) - ((1 - our_probability) * stake)
        ev_percentage = (ev / stake) * 100
        
        # Edge over Vegas
        edge = our_probability - implied_probability
        edge_percentage = edge * 100
        
        # Recommendation
        if ev > 0 and edge > 0.05:  # Must have at least 5% edge
            recommendation = "STRONG BET ✅"
        elif ev > 0:
            recommendation = "SLIGHT EDGE ⚠️"
        else:
            recommendation = "NO BET ❌"
        
        return {
            'our_probability': round(our_probability, 3),
            'implied_probability': round(implied_probability, 3),
            'edge': round(edge, 3),
            'edge_percentage': round(edge_percentage, 1),
            'expected_value': round(ev, 2),
            'ev_percentage': round(ev_percentage, 1),
            'potential_profit': round(potential_profit, 2),
            'recommendation': recommendation
        }
    
    def analyze_prop(self, player_name: str, prop_type: str, player_data: Dict, american_odds: int) -> Dict:
        """
        Full analysis of a player prop bet
        
        Args:
            player_name: "Stephen Curry"
            prop_type: "3PT_MADE" (for now, just 3-pointers)
            player_data: Performance data
            american_odds: Sportsbook odds
        
        Returns:
            Complete analysis
        """
        
        if prop_type == "3PT_MADE":
            probability = self.calculate_three_point_probability(player_data)
        else:
            raise ValueError(f"Prop type {prop_type} not supported yet")
        
        ev_analysis = self.calculate_expected_value(probability, american_odds)
        
        return {
            'player': player_name,
            'prop_type': prop_type,
            'odds': american_odds,
            **ev_analysis
        }


def test_engine():
    """Test the probability engine with examples"""
    engine = ProbabilityEngine()
    
    print("\n" + "="*70)
    print("🧠 PROBABILITY ENGINE TEST")
    print("="*70 + "\n")
    
    # Test Case 1: Stephen Curry
    print("📊 TEST 1: Stephen Curry to hit next 3PT")
    print("-" * 70)
    
    curry_data = {
        'season_3pt_pct': 0.42,  # 42% season average
        'recent_games_3pt': [0.5, 0.4, 0.33, 0.6, 0.5],  # Hot streak
        'current_game_3pt': 0.6,  # 3/5 made today
        'defender_3pt_allowed': 0.40  # Weak defender
    }
    
    curry_analysis = engine.analyze_prop(
        player_name="Stephen Curry",
        prop_type="3PT_MADE",
        player_data=curry_data,
        american_odds=180  # +180 odds
    )
    
    print(f"Player: {curry_analysis['player']}")
    print(f"Odds: +{curry_analysis['odds']}")
    print(f"Our Probability: {curry_analysis['our_probability']*100:.1f}%")
    print(f"Vegas Probability: {curry_analysis['implied_probability']*100:.1f}%")
    print(f"Our Edge: {curry_analysis['edge_percentage']:+.1f}%")
    print(f"Expected Value: ${curry_analysis['expected_value']:+.2f} per $100 bet")
    print(f"EV%: {curry_analysis['ev_percentage']:+.1f}%")
    print(f"Recommendation: {curry_analysis['recommendation']}")
    print()
    
    # Test Case 2: Average shooter, bad odds
    print("📊 TEST 2: Average Player with Bad Odds")
    print("-" * 70)
    
    average_data = {
        'season_3pt_pct': 0.35,
        'recent_games_3pt': [0.33, 0.40, 0.30, 0.35, 0.33],
        'current_game_3pt': 0.33,
        'defender_3pt_allowed': 0.35
    }
    
    average_analysis = engine.analyze_prop(
        player_name="Average Player",
        prop_type="3PT_MADE",
        player_data=average_data,
        american_odds=-150  # -150 odds (have to bet $150 to win $100)
    )
    
    print(f"Player: {average_analysis['player']}")
    print(f"Odds: {average_analysis['odds']}")
    print(f"Our Probability: {average_analysis['our_probability']*100:.1f}%")
    print(f"Vegas Probability: {average_analysis['implied_probability']*100:.1f}%")
    print(f"Our Edge: {average_analysis['edge_percentage']:+.1f}%")
    print(f"Expected Value: ${average_analysis['expected_value']:+.2f} per $100 bet")
    print(f"EV%: {average_analysis['ev_percentage']:+.1f}%")
    print(f"Recommendation: {average_analysis['recommendation']}")
    print()
    
    print("="*70)
    print("✅ ENGINE TEST COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_engine()