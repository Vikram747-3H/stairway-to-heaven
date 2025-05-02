import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''a class to manage the ship'''

    def __init__(self,ai_game):
        """initialises ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right= False
        self.moving_left= False
        self.moving_up = False
        self.moving_down = False
        
        
        self.settings = ai_game.settings

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
       
    def update(self):
        """updates the ship postition based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -=self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -=self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y +=self.settings.ship_speed
       
       

        self.rect.x = self.x
        self.rect.y = self.y
        


    def blitme(self):
        """draw ship at its current location"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """Centre the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
       