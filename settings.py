class Settings:
    """The game settings class"""

    def __init__(self):
        """Initialize game variables"""
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.allowed_bullets = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 80
        self.fleet_direction = 1  # (1 => right), (-1 => left)

        # Ship settings
        self.ship_limit = 3
