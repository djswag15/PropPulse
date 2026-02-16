from paper_trade_tracker import PaperTradeTracker
import json

tracker = PaperTradeTracker()

# Update Trade #7 - Luka (5/12 from 3PT = HIT over 3.5)
tracker.update_result(7, won=True, actual_result="5/12 3PT (HIT over 3.5)")

# Delete trade #10 (if it exists)
tracker.trades = [t for t in tracker.trades if t['id'] != 10]
tracker.save_trades()

print("✅ Updated Trade #7")
print("✅ Deleted Trade #10")
print("\nCurrent trades:")
tracker.display_summary()
tracker.display_recent_trades()