class Settings:
    """A Class to store all setings for Alien Invasion"""
    
    def __init__(self):
        # Screen settings
        self.screen_width = 1600
        self.screen_height = 800
        self.bg_color=(230,230,230)
        # Ship settings
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 10
        # Alien settings
        self.fleet_drop_speed = 10
        # Stars settings
        self.star_width = 2
        self.star_height =2
        self.star_color = (60,60,60)
        self.stars_allowed = 100

        # How quickly the game speeds up. 
        self.speedup_scale = 1.1

        # How quickly the alien point values increases.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize setttings that change throughout the game."""
        self.ship_speed= 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.star_speed = 1.5

        # Scoring settings.
        self.alien_points = 50

        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.star_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
    