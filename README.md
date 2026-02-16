# PropPulse 🚀

**AI-Powered NBA Prop Betting Edge Finder**

PropPulse is a machine learning system that identifies positive expected value (+EV) betting opportunities in NBA player props by calculating true probabilities and comparing them against sportsbook odds.

##  Validated Performance

- **60% Win Rate** (12-8 record)
- **109.2% ROI** over 20 tracked bets
- **Average Edge: 10.2%** per recommendation
- **Total Profit: +$2,185** on $2,000 staked

##  How It Works

1. **Data Collection**: Scrapes player stats, recent performance, and historical data
2. **Probability Modeling**: Uses Poisson distribution and weighted recent form to calculate true probabilities
3. **Edge Detection**: Compares model probabilities vs sportsbook implied odds
4. **EV Calculation**: Identifies bets with positive expected value
5. **Paper Trading**: Tracks all recommendations to validate model accuracy

##  Tech Stack

- **Python**: Core programming language
- **Selenium**: Web scraping for odds data
- **Statistics**: Poisson modeling, Bayesian updating
- **JSON**: Data persistence and tracking

##  Key Features

- Real-time odds scraping from major sportsbooks
- Statistical modeling of player prop probabilities
- Expected value calculation engine
- Paper trading tracker with performance analytics
- Automated bet logging and result tracking

##  Getting Started
```bash
# Clone the repository
git clone https://github.com/djswag15/proppulse.git

# Install dependencies
pip install -r requirements.txt

# Run the bet finder
python bet_finder.py
```

##  Model Validation

The model has been paper-traded with 20 real NBA games, achieving:
- 60% hit rate (vs 50% breakeven)
- Consistent positive EV across all recommendations
- Strong performance across multiple player types and lines

##  Disclaimer

This is an educational project. Sports betting involves risk. Past performance does not guarantee future results. Only bet what you can afford to lose.

##  Future Enhancements

- [ ] Multi-sportsbook comparison
- [ ] Real-time alerts for +EV opportunities
- [ ] Advanced injury/lineup tracking
- [ ] Web dashboard with live tracking
- [ ] Bankroll management optimizer

---

*Built by Darnell Nziga | [LinkedIn](http://www.linkedin.com/in/darnell-nziga-967695265) 
