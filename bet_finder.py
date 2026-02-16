from data_fetcher import NBADataFetcher
from odds_scraper import OddsScraper
from probability_engine import ProbabilityEngine
from paper_trade_tracker import PaperTradeTracker
from typing import List, Dict
import time

class BetFinder:
    """
    Complete betting recommendation system
    Combines data fetching, odds scraping, and probability analysis
    """
    
    def __init__(self):
        self.nba_data = NBADataFetcher()
        self.odds_scraper = OddsScraper()
        self.prob_engine = ProbabilityEngine()
        self.tracker = PaperTradeTracker()  # NEW: Add tracker
    
    def get_player_performance_data(self, player_name: str, game_id: str = None) -> Dict:
        """
        Get player's performance data for probability calculation
        
        For MVP: Using simulated realistic data
        In production: Would pull from NBA API + historical database
        """
        
        # Simulated player data based on real NBA stats
        player_database = {
            'Stephen Curry': {
                'season_3pt_pct': 0.42,
                'recent_games_3pt': [0.50, 0.40, 0.45, 0.60, 0.38],
                'current_game_3pt': 0.50,  # 2/4 so far
                'defender_3pt_allowed': 0.38
            },
            'Kevin Durant': {
                'season_3pt_pct': 0.41,
                'recent_games_3pt': [0.33, 0.50, 0.40, 0.43, 0.50],
                'current_game_3pt': 0.40,
                'defender_3pt_allowed': 0.36
            },
            'LeBron James': {
                'season_3pt_pct': 0.38,
                'recent_games_3pt': [0.33, 0.40, 0.25, 0.50, 0.33],
                'current_game_3pt': 0.33,
                'defender_3pt_allowed': 0.37
            },
            'Damian Lillard': {
                'season_3pt_pct': 0.43,
                'recent_games_3pt': [0.50, 0.55, 0.43, 0.60, 0.50],
                'current_game_3pt': 0.60,
                'defender_3pt_allowed': 0.40
            }
        }
        
        return player_database.get(player_name, {
            'season_3pt_pct': 0.35,
            'recent_games_3pt': [0.33, 0.35, 0.33, 0.40, 0.33],
            'current_game_3pt': 0.33,
            'defender_3pt_allowed': 0.35
        })
    
    def find_positive_ev_bets(self, min_edge: float = 0.02, log_bets: bool = True) -> List[Dict]:
        """
        Find all bets with positive expected value
        
        Args:
            min_edge: Minimum edge required (default 5%)
            log_bets: Whether to log bets to paper trade tracker
        
        Returns:
            List of recommended bets sorted by EV
        """
        print("\n" + "="*70)
        print("🔍 SCANNING FOR +EV BETTING OPPORTUNITIES")
        print("="*70 + "\n")
        
        # Get available props from sportsbook
        print("📊 Fetching odds from sportsbooks...")
        all_props = self.odds_scraper.scrape_draftkings_nba_props()
        print(f"✅ Found {len(all_props)} available props\n")
        
        positive_ev_bets = []
        
        print("🧮 Analyzing each prop...\n")
        
        for prop in all_props:
            # Only analyze 3PT props for now
            if prop['prop_type'] != '3PT_MADE':
                continue
            
            player_name = prop['player']
            odds = prop['odds']
            
            # Get player performance data
            player_data = self.get_player_performance_data(player_name)
            
            if not player_data:
                continue
            
            # Calculate EV
            analysis = self.prob_engine.analyze_prop(
                player_name=player_name,
                prop_type='3PT_MADE',
                player_data=player_data,
                american_odds=odds
            )
            
            # Check if it meets our criteria
            if analysis['edge'] >= min_edge and analysis['expected_value'] > 0:
                bet_recommendation = {
                    **analysis,
                    'line': prop['line'],
                    'sportsbook': prop['sportsbook']
                }
                positive_ev_bets.append(bet_recommendation)
                
                # NEW: Log to paper trade tracker
                if log_bets:
                    trade_id = self.tracker.log_recommendation(bet_recommendation)
                    bet_recommendation['trade_id'] = trade_id
                
                # Print as we find them
                print(f"✅ FOUND: {player_name}")
                print(f"   Edge: {analysis['edge_percentage']:+.1f}% | EV: ${analysis['expected_value']:+.2f}")
                if log_bets:
                    print(f"   📝 Logged as Trade #{trade_id}")
        
        # Sort by expected value (highest first)
        positive_ev_bets.sort(key=lambda x: x['expected_value'], reverse=True)
        
        return positive_ev_bets
    
    def display_recommendations(self, bets: List[Dict]):
        """Display betting recommendations in a clean format"""
        
        print("\n" + "="*70)
        print("💰 BETTING RECOMMENDATIONS")
        print("="*70 + "\n")
        
        if not bets:
            print("❌ No positive EV bets found at this time.")
            print("   Check back when games are live or odds change.\n")
            return
        
        print(f"Found {len(bets)} profitable betting opportunities:\n")
        
        for i, bet in enumerate(bets, 1):
            print("="*70)
            print(f"#{i} RECOMMENDED BET")
            if 'trade_id' in bet:
                print(f"📝 Trade ID: {bet['trade_id']} (for tracking results later)")
            print("="*70)
            print(f"Player: {bet['player']}")
            print(f"Prop: {bet['line']}")
            print(f"Odds: {bet['odds']:+d} ({bet['sportsbook']})")
            print()
            print(f"📊 ANALYSIS:")
            print(f"  Our Probability:    {bet['our_probability']*100:.1f}%")
            print(f"  Vegas Probability:  {bet['implied_probability']*100:.1f}%")
            print(f"  Our Edge:           {bet['edge_percentage']:+.1f}%")
            print()
            print(f"💵 VALUE:")
            print(f"  Expected Value:     ${bet['expected_value']:+.2f} per $100 bet")
            print(f"  EV Percentage:      {bet['ev_percentage']:+.1f}%")
            print(f"  Potential Profit:   ${bet['potential_profit']:.2f}")
            print()
            print(f"🎯 RECOMMENDATION: {bet['recommendation']}")
            print()
        
        # Summary
        print("="*70)
        print("📈 PORTFOLIO SUMMARY")
        print("="*70)
        total_ev = sum(bet['expected_value'] for bet in bets)
        avg_edge = sum(bet['edge_percentage'] for bet in bets) / len(bets)
        
        print(f"Total Expected Value: ${total_ev:+.2f} (betting $100 on each)")
        print(f"Average Edge:         {avg_edge:+.1f}%")
        print(f"Number of Bets:       {len(bets)}")
        print()
        
        if len(bets) >= 3:
            print("💡 TIP: Betting on multiple +EV bets increases your chance")
            print("        of profit while reducing variance (law of large numbers)")
        
        print("\n" + "="*70 + "\n")
    
    def run(self, log_bets: bool = True):
        """
        Main entry point - find and display all +EV bets
        
        Args:
            log_bets: Whether to log bets for paper trading (default: True)
        """
        print("\n" + "🚀 "*20)
        print("              PROPPULSE - BET FINDER ENGINE")
        print("🚀 "*20 + "\n")
        
        # Find bets
        bets = self.find_positive_ev_bets(min_edge=0.05, log_bets=log_bets)
        
        # Display recommendations
        self.display_recommendations(bets)
        
        # NEW: Show tracking status
        if log_bets and bets:
            print("="*70)
            print("📊 PAPER TRADING STATUS")
            print("="*70 + "\n")
            print(f"✅ Logged {len(bets)} bets for tracking")
            print(f"📝 Remember to update results after games finish!")
            print(f"   Use: tracker.update_result(trade_id, won=True/False)")
            print()
            
            # Show current paper trading stats
            self.tracker.display_summary()
        
        # Close scraper
        self.odds_scraper.close()
        
        return bets


def main():
    """Run the bet finder"""
    finder = BetFinder()
    finder.run(log_bets=True)  # Set to True to enable tracking


if __name__ == "__main__":
    main()