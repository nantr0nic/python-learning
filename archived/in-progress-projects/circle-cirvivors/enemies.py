import pygame
from pygame.sprite import Sprite

import config as c


class Enemy(Sprite):
    def __init__(self, x, y, speed, size):
        """Basic attributes."""
        super(Enemy, self).__init__()
        self.speed = speed
        self.size = size
        self.r = c.enemy_color[0]
        self.g = c.enemy_color[1]
        self.b = c.enemy_color[2]
        self.image = pygame.Surface((self.size, self.size))
        self.rect_draw = pygame.Rect(0, 0, self.size, self.size)
        pygame.draw.rect(self.image, (self.r, self.g, self.b), self.rect_draw)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def update(self, player):
        self.current_pos = pygame.math.Vector2(self.x, self.y)
        self.player_pos = pygame.math.Vector2(player.x, player.y)
        self.current_pos.move_towards_ip(self.player_pos, self.speed)
        self.x = self.current_pos.x
        self.y = self.current_pos.y
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Spawn timer
def spawn_timer(current_time, SPAWN_EVENT):
    if current_time - c.last_decrement_time >= c.decrement_interval:
        c.current_spawn_interval = max(
            c.current_spawn_interval - c.spawn_interval_decrement, 100
        )
        pygame.time.set_timer(SPAWN_EVENT, c.current_spawn_interval)
        c.last_decrement_time = current_time
