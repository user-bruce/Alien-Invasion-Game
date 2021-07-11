import sys
import pygame
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien


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

        # Instantiate a bullet
        self.bullets = pygame.sprite.Group()

        # Instantiate an alien
        self.aliens = pygame.sprite.Group()

        # Create a fleet of aliens
        self._create_fleet()

    def run_game(self):
        """The main game loop"""
        while True:
            """Watch for pygame events"""
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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
        """Fire a bullet.Bullets only exist in groups of three"""
        if len(self.bullets) < self.settings.allowed_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets"""
        self.bullets.update()

        # Remove bullets that are out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
                
    def _update_aliens(self):
        """Update the position of the aliens"""
        self.aliens.update()

    def _update_screen(self):
        """Function to update the screen"""
        self.screen.fill(self.settings.bg_color)

        # Display the ship
        self.ship.blit_ship()

        # Draw the bullet
        for bullet in self.bullets:
            bullet.draw_bullet()

        # Draw the alien
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _create_fleet(self):
        """Create a fleet of aliens """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows vertically
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create an alien and place it in the row
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self, alien_number,row_number):
        """Create an alien and add it to the group"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


# Start the game (entry point)
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
