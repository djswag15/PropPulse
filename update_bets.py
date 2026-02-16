from paper_trade_tracker import PaperTradeTracker

tracker = PaperTradeTracker()

# Update Trade #4 - Steph Curry (6/12 from 3PT = HIT)
tracker.update_result(4, won=True, actual_result="6/12 3PT (HIT over 2.5)")

# Update Trade #5 - Luka Doncic (4/6 from 3PT = HIT)
tracker.update_result(5, won=True, actual_result="4/6 3PT (HIT over 3.5)")

# Update Trade #6 - Donovan Mitchell (5/12 from 3PT = HIT)
tracker.update_result(6, won=True, actual_result="5/12 3PT (HIT over 3.5)")

# Update Trade #8 - Luka Doncic (3/9 from 3PT = MISS)
tracker.update_result(8, won=False, actual_result="3/9 3PT (MISS over 3.5)")

# Update Trade #9 - Stephen Curry (2/7 from 3PT = MISS)
tracker.update_result(9, won=False, actual_result="2/7 3PT (MISS over 4.5)")

# Update Trade #10 - Luka Doncic (3/13 from 3PT = MISS)
tracker.update_result(10, won=False, actual_result="3/13 3PT (MISS over 3.5)")

# Update Trade #11 - Stephen Curry (8/15 from 3PT = HIT)
tracker.update_result(11, won=True, actual_result="8/15 3PT (HIT over 4.5)")

# Update Trade #12 - Stephen Curry (3/10 from 3PT = MISS)
tracker.update_result(12, won=False, actual_result="3/10 3PT (MISS over 4.5)")

# Update Trade #13 - Klay Thompson (2/5 from 3PT = MISS)
tracker.update_result(13, won=False, actual_result="2/5 3PT (MISS over 3.5)")

# Update Trade #14 - Stephen Curry (4/10 from 3PT = MISS)
tracker.update_result(14, won=False, actual_result="4/10 3PT (MISS over 4.5)")

# Update Trade #15 - Klay Thompson (4/10 from 3PT = HIT)
tracker.update_result(15, won=True, actual_result="4/10 3PT (HIT over 3.5)")

# Update Trade #16 - Anthony Edwards (5/9 from 3PT = HIT)
tracker.update_result(16, won=True, actual_result="5/9 3PT (HIT over 4.5)")

# Update Trade #17 - Anthony Edwards (4/11 from 3PT = HIT)
tracker.update_result(17, won=True, actual_result="4/11 3PT (HIT over 2.5)")

# Update Trade #18 - Anthony Edwards (4/6 from 3PT = HIT)
tracker.update_result(18, won=True, actual_result="4/6 3PT (HIT over 2.5)")

print("\n✅ All bets updated!")
print("\nUpdated results:")
tracker.display_summary()
tracker.display_recent_trades()