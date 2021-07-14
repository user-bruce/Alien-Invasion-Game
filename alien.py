import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to represent an alien object"""
    
    def __init__(self,ai_game):
        """Construct the alien object"""
        super().__init__()
        
        #Alien properties
        self.screen = ai_game.screen
        
        #Load the image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings
        
        #Position the alien object
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Store the exact horixontal position of the alien
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Check whether the alien has reached either end"""
        screen_rect = self.screen.get_rect()
        
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    def update(self):
        """Update the speed of the Alien"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x