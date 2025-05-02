import sys 
from time import sleep
import json
from pathlib import Path

import pygame

from settings import Settings

from game_stats import GameStats
from button import Button
from difficulty_button import Diffbutton
from scoreboard import Scoreboard

from ship import Ship
from bullet import Bullet
from alien import Alien
from stars import Star

class AlienInvasion:
    
    def __init__(self):
        """initialising the game, and create game resources"""
        pygame.init()
        self.clock=pygame.time.Clock()
        self.settings=Settings()

        self.screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an insatance to store game Statistics.
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        

        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        self._create_fleet()

        #Make the play button.
        self.play_button = Button(self, "play")
        #self.diff_buttom = Diffbutton(self, "1", "2", "3")

        #Start the alien invasion in an inactive state.
        self.game_active = False

        # For the Bonus level
        self.bonus = True

        



    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active :
                self._create_stars()
                self._update_stars()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(165)


    def _update_screen(self):
        """update images on the screen, and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        for star in self.stars:
            star.draw()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
            #self.diff_buttom.draw_button()


        pygame.display.flip()
 

    def _check_events(self):
        """check the events of the screen"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()


    def _start_game(self):
        """Start the game."""
        # Reset the game statistics
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats() 
        self.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        # Get rid of remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)



    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        elif not self.game_active and event.key == pygame.K_p:
            self._start_game()    
        elif event.key == pygame.K_q:
            # Save the high score to the json file
            contents = json.dumps(round(self.stats.high_score, -1))
            self.stats.path.write_text(contents)

            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
         self.ship.moving_left = False
        elif event.key == pygame.K_UP:
         self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
         self.ship.moving_down = False


    def _fire_bullets(self) :
        """Create a bullet group and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    
    
    def _update_bullets(self):
        """update position of the bullets and get rid of old bullets"""
        #Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        self._check_bonus()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, self.bonus , False )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    
    
    def _create_fleet(self):
        """Create the fleet of aliens. """
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alqien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height + 20
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; rest x value, and increment y value.
            current_x = alien_width
            current_y += 2 *alien_height

    
    def _create_alien(self, x_position, y_position):
        """Create a alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

        
    
    def _update_aliens(self):
        """Update the positions of aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an egde."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_stars(self):
        """Create a cluster of random stars"""
        while len(self.stars) < self.settings.stars_allowed:
            new_star = Star(self)
            self.stars.add(new_star)
    
    def _update_stars(self):
        """Update the position of stars and get rid of old stars"""
        # update stars position
        self.stars.update()

        # Get rid of old stars.
        for star in self.stars.copy():
            if star.rect.y >= self.settings.screen_height:
                self.stars.remove(star)

    def _ship_hit(self):
        """Respond to the ship being hit by the alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of remaining bullets and aliens.
            self.bullets.empty() 
            self.aliens.empty()
            
            # Create the new fleet and center the Ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5) 
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for aliens in self.aliens.sprites():
            if aliens.rect.bottom >= self.settings.screen_height:
                # Treat this as if the ship got hit.
                self._ship_hit()
                break

    def _check_bonus(self):
        """A function to check bonus"""
        if self.stats.level % 5 == 0:
            self.bonus = False


        
if __name__=='__main__':
    ai = AlienInvasion() 
    ai.run_game()    
    
# To do list
# use pygame.mixer to add sounds(pending).
# add sheilds, add bullets for aliens(pending).