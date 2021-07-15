import sys
import pygame
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """Class to manage overall game assets and behaviour"""

    def __init__(self):
        """Constructor"""

        # Initialize pygame
        pygame.init()

        # Instantiate game settings
        self.settings = Settings()

        # Instantiate the game stats object
        self.stats = GameStats(self)

        # Create screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Instantiate a ship object
        self.ship = Ship(self)

        # Instantiate a bullet
        self.bullets = pygame.sprite.Group()

        # Instantiate an alien
        self.aliens = pygame.sprite.Group()

        # Create a fleet of aliens
        self._create_fleet()

        # Create a play button
        self.play_button = Button(self, "Play")

    # The main run loop of the game
    def run_game(self):
        """The main game loop"""
        while True:
            """Watch for pygame events"""
            self._check_events()

            # if the game is active
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # Check the event types
    def _check_events(self):
        """Helper function to manage events"""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                self._check_keydown_events(e)
            elif e.type == pygame.KEYUP:
                self._check_keyup_events(e)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            # Get rid of old aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True

    # Check the keyup events
    def _check_keyup_events(self, event):
        """Handle key up events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Check the keydown events
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

    # Method to fire a bullet
    def _fire_bullet(self):
        """Fire a bullet.Bullets only exist in groups of three"""
        if len(self.bullets) < self.settings.allowed_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # update the bullet position
    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets"""
        self.bullets.update()

        # Remove bullets that are out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    # Check for bullet-alien collisions and respond appropriately
    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # Recreate a new fleet if all aliens in the current fleet are destroyed
        if not self.aliens:
            self.bullets.empty
            self._create_fleet()

    # Update the alien position
    def _update_aliens(self):
        """Update the position of the aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        # check for any alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # check for any aliens that have reached the bottom
        self._check_aliens_bottom()

    # Update the screen
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

        # Display the play button
        if not self.stats.game_active:
            self.play_button.draw_button()

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
                self._create_alien(alien_number, row_number)

    # create an alien and add it to the fleet
    def _create_alien(self, alien_number, row_number):
        """Create an alien and add it to the group"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # Check the fleet edges
    def _check_fleet_edges(self):
        """Check if aliens have reached the edges and change the direction"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_direction()
                break

    # Change the fleet direction
    def _change_direction(self):
        """Drop the entire fleet and change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # Detect ship collision and respond appropriately
    def _ship_hit(self):
        """decrement the ships left restart the game"""
        if self.stats.ships_left > 0:
            self.stats.remove_ship()

            # remove any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and recenter the ship
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False

    # Check if alien has reached the bottom of the screen
    def _check_aliens_bottom(self):
        """If alien reaches the bottom ,act like ship has been hit"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


# Start the game (entry point)
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
