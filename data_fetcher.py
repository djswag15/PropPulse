import requests
import json
from datetime import datetime

class NBADataFetcher:
    """Fetch live NBA game data"""
    
    def __init__(self):
        self.base_url = "https://cdn.nba.com/static/json/liveData"
    
    def get_live_games(self):
        """Get today's games and live scores"""
        try:
            url = f"{self.base_url}/scoreboard/todaysScoreboard_00.json"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            games = data.get('scoreboard', {}).get('games', [])
            
            print(f"\n{'='*60}")
            print(f"🏀 LIVE NBA GAMES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")
            
            if not games:
                print("No games today or games haven't started yet.")
                return []
            
            live_games = []
            for game in games:
                game_info = {
                    'game_id': game.get('gameId'),
                    'status': game.get('gameStatusText'),
                    'home_team': game.get('homeTeam', {}).get('teamName'),
                    'away_team': game.get('awayTeam', {}).get('teamName'),
                    'home_score': game.get('homeTeam', {}).get('score'),
                    'away_score': game.get('awayTeam', {}).get('score'),
                    'period': game.get('period'),
                    'game_clock': game.get('gameClock')
                }
                live_games.append(game_info)
                
                # Print game info
                print(f"Game ID: {game_info['game_id']}")
                print(f"  {game_info['away_team']} @ {game_info['home_team']}")
                print(f"  Score: {game_info['away_score']} - {game_info['home_score']}")
                print(f"  Status: {game_info['status']}")
                if game_info['game_clock']:
                    print(f"  Time: Q{game_info['period']} - {game_info['game_clock']}")
                print()
            
            return live_games
            
        except Exception as e:
            print(f"❌ Error fetching games: {e}")
            return []
    
    def get_player_stats(self, game_id):
        """Get live player stats for a specific game"""
        try:
            url = f"{self.base_url}/boxscore/boxscore_{game_id}.json"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            game_data = data.get('game', {})
            
            home_players = game_data.get('homeTeam', {}).get('players', [])
            away_players = game_data.get('awayTeam', {}).get('players', [])
            
            all_players = []
            
            for player in home_players + away_players:
                stats = player.get('statistics', {})
                player_info = {
                    'name': f"{player.get('firstName')} {player.get('familyName')}",
                    'team': player.get('teamId'),
                    'points': stats.get('points', 0),
                    'rebounds': stats.get('reboundsTotal', 0),
                    'assists': stats.get('assists', 0),
                    'threes_made': stats.get('threePointersMade', 0),
                    'threes_attempted': stats.get('threePointersAttempted', 0),
                    'minutes': stats.get('minutesCalculated', '0:00')
                }
                all_players.append(player_info)
            
            return all_players
            
        except Exception as e:
            print(f"❌ Error fetching player stats: {e}")
            return []
    
    def get_player_3pt_percentage(self, player_name: str, game_id: str = None):
        """
        Get player's 3PT percentage for current game
        Used by bet_finder to get real-time performance
        
        Args:
            player_name: Full player name (e.g., "Stephen Curry")
            game_id: Specific game to check (optional)
        
        Returns:
            float: 3PT percentage (e.g., 0.5 for 50%)
        """
        try:
            if game_id:
                players = self.get_player_stats(game_id)
            else:
                # Get all today's games
                games = self.get_live_games()
                if not games:
                    return None
                
                # Try to find player in any game
                for game in games:
                    players = self.get_player_stats(game['game_id'])
                    for player in players:
                        if player['name'].lower() == player_name.lower():
                            if player['threes_attempted'] > 0:
                                return player['threes_made'] / player['threes_attempted']
                            return None
            
            # Find the specific player
            for player in players:
                if player['name'].lower() == player_name.lower():
                    if player['threes_attempted'] > 0:
                        return player['threes_made'] / player['threes_attempted']
                    return None
            
            return None
            
        except Exception as e:
            print(f"⚠️  Could not fetch live stats for {player_name}: {e}")
            return None


def main():
    """Test the data fetcher"""
    fetcher = NBADataFetcher()
    
    # Get live games
    games = fetcher.get_live_games()
    
    # If games are live, get player stats for first game
    if games and games[0]['status'] not in ['Final', 'TBD']:
        print(f"\n{'='*60}")
        print("📊 PLAYER STATS (First Live Game)")
        print(f"{'='*60}\n")
        
        game_id = games[0]['game_id']
        players = fetcher.get_player_stats(game_id)
        
        if players:
            # Show top 5 scorers
            sorted_players = sorted(players, key=lambda x: x['points'], reverse=True)[:5]
            
            for i, player in enumerate(sorted_players, 1):
                print(f"{i}. {player['name']}")
                print(f"   Points: {player['points']} | Rebounds: {player['rebounds']} | Assists: {player['assists']}")
                print(f"   3PT: {player['threes_made']}/{player['threes_attempted']} | Minutes: {player['minutes']}")
                print()
        else:
            print("No player stats available yet (game may not have started)")
    
    print(f"\n{'='*60}")
    print("✅ DATA TEST COMPLETE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()