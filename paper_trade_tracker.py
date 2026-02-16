import json
from datetime import datetime
from typing import List, Dict
import os

class PaperTradeTracker:
    """
    Track paper trading results to validate the model
    """
    
    def __init__(self, results_file: str = "paper_trades.json"):
        self.results_file = results_file
        self.trades = self.load_trades()
    
    def load_trades(self) -> List[Dict]:
        """Load existing trades from file"""
        if os.path.exists(self.results_file):
            with open(self.results_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_trades(self):
        """Save trades to file"""
        with open(self.results_file, 'w') as f:
            json.dump(self.trades, f, indent=2)
    
    def log_recommendation(self, bet: Dict, game_id: str = None):
        """
        Log a bet recommendation
        
        Args:
            bet: The bet recommendation from BetFinder
            game_id: Optional NBA game ID
        """
        trade = {
            'id': len(self.trades) + 1,
            'timestamp': datetime.now().isoformat(),
            'player': bet['player'],
            'prop_type': bet['prop_type'],
            'line': bet['line'],
            'odds': bet['odds'],
            'our_probability': bet['our_probability'],
            'implied_probability': bet['implied_probability'],
            'edge': bet['edge'],
            'expected_value': bet['expected_value'],
            'stake': 100.0,  # Simulated $100 bet
            'game_id': game_id,
            'status': 'pending',  # pending, won, lost
            'actual_result': None,
            'profit_loss': None
        }
        
        self.trades.append(trade)
        self.save_trades()
        
        print(f"✅ Logged trade #{trade['id']}: {bet['player']} - {bet['prop_type']}")
        return trade['id']
    
    def update_result(self, trade_id: int, won: bool, actual_result: str = ""):
        """
        Update trade result after game finishes
        
        Args:
            trade_id: The trade ID
            won: True if bet won, False if lost
            actual_result: Description of what happened (e.g., "Made 3/8 3PT")
        """
        for trade in self.trades:
            if trade['id'] == trade_id:
                trade['status'] = 'won' if won else 'lost'
                trade['actual_result'] = actual_result
                
                # Calculate profit/loss
                if won:
                    # Calculate winnings based on odds
                    odds = trade['odds']
                    stake = trade['stake']
                    if odds > 0:
                        profit = stake * (odds / 100.0)
                    else:
                        profit = stake * (100.0 / abs(odds))
                    trade['profit_loss'] = profit
                else:
                    trade['profit_loss'] = -trade['stake']
                
                self.save_trades()
                print(f"✅ Updated trade #{trade_id}: {'WON' if won else 'LOST'} (${trade['profit_loss']:+.2f})")
                return True
        
        print(f"❌ Trade #{trade_id} not found")
        return False
    
    def get_statistics(self) -> Dict:
        """Calculate overall statistics"""
        if not self.trades:
            return {
                'total_bets': 0,
                'completed_bets': 0,
                'pending_bets': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0.0,
                'total_staked': 0.0,
                'total_profit': 0.0,
                'roi': 0.0,
                'avg_ev': 0.0,
                'avg_edge': 0.0
            }
        
        completed = [t for t in self.trades if t['status'] in ['won', 'lost']]
        pending = [t for t in self.trades if t['status'] == 'pending']
        wins = [t for t in completed if t['status'] == 'won']
        losses = [t for t in completed if t['status'] == 'lost']
        
        total_staked = sum(t['stake'] for t in completed)
        total_profit = sum(t.get('profit_loss', 0) for t in completed)
        
        return {
            'total_bets': len(self.trades),
            'completed_bets': len(completed),
            'pending_bets': len(pending),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': (len(wins) / len(completed) * 100) if completed else 0.0,
            'total_staked': total_staked,
            'total_profit': total_profit,
            'roi': (total_profit / total_staked * 100) if total_staked > 0 else 0.0,
            'avg_ev': sum(t['expected_value'] for t in self.trades) / len(self.trades),
            'avg_edge': sum(t['edge'] for t in self.trades) / len(self.trades) * 100
        }
    
    def display_summary(self):
        """Display summary statistics"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("📊 PAPER TRADING RESULTS")
        print("="*70 + "\n")
        
        print(f"Total Bets Tracked:     {stats['total_bets']}")
        print(f"Completed Bets:         {stats['completed_bets']}")
        print(f"Pending Bets:           {stats['pending_bets']}")
        print()
        
        if stats['completed_bets'] > 0:
            print("🎯 PERFORMANCE:")
            print(f"  Wins:                 {stats['wins']}")
            print(f"  Losses:               {stats['losses']}")
            print(f"  Win Rate:             {stats['win_rate']:.1f}%")
            print()
            print("💰 FINANCIAL:")
            print(f"  Total Staked:         ${stats['total_staked']:.2f}")
            print(f"  Total Profit/Loss:    ${stats['total_profit']:+.2f}")
            print(f"  ROI:                  {stats['roi']:+.1f}%")
            print()
            print("📈 MODEL METRICS:")
            print(f"  Average EV:           ${stats['avg_ev']:.2f}")
            print(f"  Average Edge:         {stats['avg_edge']:.1f}%")
            print()
            
            # Validation check
            if stats['completed_bets'] >= 20:
                if stats['win_rate'] >= 55 and stats['roi'] > 0:
                    print("✅ MODEL VALIDATED: Win rate and ROI meet targets!")
                elif stats['win_rate'] >= 50 and stats['roi'] > 0:
                    print("⚠️  MODEL PROMISING: Positive ROI, but win rate could be higher")
                else:
                    print("❌ MODEL NEEDS WORK: Not meeting performance targets yet")
            else:
                print(f"📊 SAMPLE SIZE: Need {20 - stats['completed_bets']} more bets for validation")
        else:
            print("No completed bets yet. Start tracking!")
        
        print("\n" + "="*70 + "\n")
    
    def display_recent_trades(self, n: int = 10):
        """Display most recent trades"""
        recent = self.trades[-n:]
        
        print("\n" + "="*70)
        print(f"📋 LAST {min(n, len(recent))} TRADES")
        print("="*70 + "\n")
        
        for trade in reversed(recent):
            status_emoji = "✅" if trade['status'] == 'won' else "❌" if trade['status'] == 'lost' else "⏳"
            print(f"{status_emoji} Trade #{trade['id']} - {trade['player']} - {trade['prop_type']}")
            print(f"   Odds: {trade['odds']:+d} | Edge: {trade['edge']*100:.1f}% | EV: ${trade['expected_value']:.2f}")
            
            if trade['status'] != 'pending':
                print(f"   Result: {trade['actual_result']}")
                print(f"   P/L: ${trade['profit_loss']:+.2f}")
            else:
                print(f"   Status: Pending")
            print()


def test_tracker():
    """Test the paper trade tracker"""
    tracker = PaperTradeTracker()
    
    # Simulate some bets
    print("Testing Paper Trade Tracker\n")
    
    # Log a bet
    sample_bet = {
        'player': 'Stephen Curry',
        'prop_type': '3PT_MADE',
        'line': 'Over 2.5',
        'odds': 180,
        'our_probability': 0.485,
        'implied_probability': 0.357,
        'edge': 0.128,
        'expected_value': 34.80
    }
    
    trade_id = tracker.log_recommendation(sample_bet)
    
    # Display current stats
    tracker.display_summary()
    tracker.display_recent_trades()


if __name__ == "__main__":
    tracker = PaperTradeTracker()
    tracker.display_summary()
    tracker.display_recent_trades()