import pygame

class Ship:
    """Class to manage the ship"""
    
    def __init__(self,ai_game):
        """Initialize ship and set its starting point"""
        self.screen = ai_game.screen
        
        #Load the image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.moving_right = False
        self.moving_left = False
        
        #Place the ship at center
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
    def blit_ship(self):
        """Draw the ship at the specified position"""
        self.screen.blit(self.image,self.rect)
        
    def update(self):
        """Check if the ship is moving right"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x
            