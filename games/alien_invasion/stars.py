import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    """A class to manage stars ."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.star_color
        # Give a random position to the rain particle. 
        self.x_cor = randint(0,self.settings.screen_width)
        self.y_cor = randint(0,self.settings.screen_height)

        #Create a rain particle at a random postion
        self.rect = pygame.Rect(self.x_cor, self.y_cor, self.settings.star_width, self.settings.star_height)
        self.y = float(self.rect.y)

    def update(self):
        """Move the stars down the Screen"""
        # update the exact position of the bullet
        self.y += self.settings.star_speed
        #update the rect position
        self.rect.y = self.y

    def draw(self):
        """Draw the star to the screnn"""
        pygame.draw.rect(self.screen, self.color, self.rect)
