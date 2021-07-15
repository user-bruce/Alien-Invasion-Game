class GameStats:
    
    def __init__(self,ai_game):
        """Reset statistics when a new game starts"""
        self.settings = ai_game.settings
        self.game_active = False
        self.reset_stats()
        
        
    def reset_stats(self):
        """Reset the game stats"""
        self.ships_left = self.settings.ship_limit
        
    def remove_ship(self):
        """Remove a ship from the shipsleft variable"""
        self.ships_left -= 1