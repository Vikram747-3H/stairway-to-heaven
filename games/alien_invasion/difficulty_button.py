import pygame.font

class Diffbutton:
    """A class to build difficult buttons for the game"""

    def __init__(self, ai_game, msg, msg_2, msg_3):
        """Initialise button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.play_button = ai_game.play_button

        #Set the dimensions and properties of the button.
        self.width, self.height = 50, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = self.play_button.rect.x
        self.rect.y = self.play_button.rect.y + 60
        self.rect_2 = pygame.Rect(0, 0, self.width, self.height)
        self.rect_2.x = self.play_button.rect.x +60
        self.rect_2.y = self.play_button.rect.y + 60
        self.rect_3 = pygame.Rect(0, 0, self.width, self.height)
        self.rect_3.x = self.play_button.rect.x + 60
        self.rect_3.y = self.play_button.rect.y + 60

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turns msg into a rendered image and center text in the button."""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw a blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)