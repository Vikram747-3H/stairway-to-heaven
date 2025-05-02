from pathlib import Path
import json

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self,ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.path = Path('highscore/high_score.json')
        
        self.reset_stats()
        # high score should never be reset
        contents = self.path.read_text()
        self.high_score = json.loads(contents)

    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0
