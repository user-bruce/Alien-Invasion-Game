class GameStats:
    
    def __init__(self,ai_game):
        """Reset statistics when a new game starts"""
        self.settings = ai_game.settings
        self.game_active = True
        self.reset_stats()
        
        
    def reset_stats(self):
        """Reset the game stats"""
        self.ships_left = self.settings.ship_limit