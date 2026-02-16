from paper_trade_tracker import PaperTradeTracker
import json
from collections import defaultdict

class ValidationReport:
    """Generate detailed validation reports"""
    
    def __init__(self):
        self.tracker = PaperTradeTracker()
    
    def analyze_by_player(self):
        """Performance breakdown by player"""
        player_stats = defaultdict(lambda: {'bets': 0, 'wins': 0, 'profit': 0})
        
        for trade in self.tracker.trades:
            if trade['status'] in ['won', 'lost']:
                player = trade['player']
                player_stats[player]['bets'] += 1
                if trade['status'] == 'won':
                    player_stats[player]['wins'] += 1
                player_stats[player]['profit'] += trade.get('profit_loss', 0)
        
        print("\n" + "="*70)
        print("👤 PERFORMANCE BY PLAYER")
        print("="*70 + "\n")
        
        for player, stats in sorted(player_stats.items(), key=lambda x: x[1]['profit'], reverse=True):
            win_rate = (stats['wins'] / stats['bets'] * 100) if stats['bets'] > 0 else 0
            print(f"{player}:")
            print(f"  Bets: {stats['bets']} | Wins: {stats['wins']} | Win Rate: {win_rate:.1f}%")
            print(f"  Profit: ${stats['profit']:+.2f}")
            print()
    
    def analyze_by_odds_range(self):
        """Performance breakdown by odds range"""
        ranges = {
            'Heavy Favorite (-200 to -150)': [],
            'Favorite (-149 to -110)': [],
            'Near Even (-109 to +109)': [],
            'Underdog (+110 to +200)': [],
            'Big Underdog (+201+)': []
        }
        
        for trade in self.tracker.trades:
            if trade['status'] not in ['won', 'lost']:
                continue
            
            odds = trade['odds']
            if odds <= -150:
                ranges['Heavy Favorite (-200 to -150)'].append(trade)
            elif odds <= -110:
                ranges['Favorite (-149 to -110)'].append(trade)
            elif odds <= 109:
                ranges['Near Even (-109 to +109)'].append(trade)
            elif odds <= 200:
                ranges['Underdog (+110 to +200)'].append(trade)
            else:
                ranges['Big Underdog (+201+)'].append(trade)
        
        print("\n" + "="*70)
        print("💵 PERFORMANCE BY ODDS RANGE")
        print("="*70 + "\n")
        
        for range_name, trades in ranges.items():
            if not trades:
                continue
            
            wins = sum(1 for t in trades if t['status'] == 'won')
            profit = sum(t.get('profit_loss', 0) for t in trades)
            win_rate = (wins / len(trades) * 100) if trades else 0
            
            print(f"{range_name}:")
            print(f"  Bets: {len(trades)} | Wins: {wins} | Win Rate: {win_rate:.1f}%")
            print(f"  Profit: ${profit:+.2f}")
            print()
    
    def generate_full_report(self):
        """Generate complete validation report"""
        print("\n" + "🏆 "*20)
        print("            PROPPULSE VALIDATION REPORT")
        print("🏆 "*20 + "\n")
        
        # Overall stats
        self.tracker.display_summary()
        
        # Detailed analysis
        self.analyze_by_player()
        self.analyze_by_odds_range()
        
        # Recent performance
        self.tracker.display_recent_trades(20)


def main():
    report = ValidationReport()
    report.generate_full_report()


if __name__ == "__main__":
    main()