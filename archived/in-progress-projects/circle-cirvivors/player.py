import pygame
from pygame.sprite import Sprite

import config as c


class Player(Sprite):
    def __init__(self, surface):
        """Define player attributes."""
        super(Player, self).__init__()
        self.surface = surface
        # player_pos default is center of screen.
        player_pos = pygame.math.Vector2(
            surface.get_width() / 2, surface.get_height() / 2
        )
        self.x = player_pos.x
        self.y = player_pos.y
        # Player appearance is a circle by default.
        self.radius = c.player_size
        # Player color is defined in config.py
        self.r = c.player_color[0]
        self.g = c.player_color[1]
        self.b = c.player_color[2]
        # Movement flags
        # For x-axis -1 is left and 1 is right
        self.moving_x = 0
        # For y-axis -1 is up and 1 is down
        self.moving_y = 0
        # Setup image / rect for Sprite + collision stuff.
        self.image = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image,
            (self.r, self.g, self.b),
            (self.radius, self.radius),
            self.radius,
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, surface):
        """Update player position and movement flags."""
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.draw(surface)

    def draw(self, surface):
        """Draw Player."""
        surface.blit(self.image, self.rect)
