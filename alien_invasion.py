import sys
import pygame
from ship import Ship
from settings import Settings
from bullet import Bullet


class AlienInvasion:
    """Class to manage overal game assets and behaviour"""

    def __init__(self):
        """Constructor"""

        # Initialize pygame
        pygame.init()

        # Instantiate game settings
        self.settings = Settings()

        # Create screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invsion")

        # Instantiate a ship object
        self.ship = Ship(self)
        
        #Instantiate a bullet
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """The main game loop"""
        while True:
            """Watch for pygame events"""
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_screen()

    def _check_events(self):
        """Helper function to manage events"""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                self._check_keydown_events(e)
            elif e.type == pygame.KEYUP:
                self._check_keyup_events(e)

    def _check_keyup_events(self, event):
        """Handle key up events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """Handle keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
            
    def _fire_bullet(self):
        """Fire a bullet"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """Function to update the screen"""
        self.screen.fill(self.settings.bg_color)

        # Display the ship
        self.ship.blit_ship()
        for bullet in self.bullets:
            bullet.draw_bullet()
        pygame.display.flip()


# Start the game (entry point)
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
