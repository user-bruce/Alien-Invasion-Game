
class Settings:
    """The game settings class"""
    
    def __init__(self):
        """Initialize game variables"""
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230,230,230)
        self.ship_speed = 1.5
        
        #Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)