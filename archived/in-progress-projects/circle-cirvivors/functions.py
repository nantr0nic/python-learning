import pygame
import random
import math

from projectiles import Projectile
from enemies import Enemy
import config as c


def check_events(
    surface,
    player,
    projectiles,
    enemies,
    SHOOT_EVENT,
    SPAWN_EVENT,
    ROUND_TIMER,
    game_state,
):
    pressed = pygame.key.get_pressed()
    if not game_state.paused:
        if pressed[pygame.K_LEFT] and player.rect.left > 0:
            player.x -= 5
        if pressed[pygame.K_RIGHT] and player.rect.right < surface.get_width():
            player.x += 5
        if pressed[pygame.K_UP] and player.rect.top > 0:
            player.y -= 5
        if pressed[pygame.K_DOWN] and player.rect.bottom < surface.get_height():
            player.y += 5
    if pressed[pygame.K_q]:
        return True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state.paused = not game_state.paused
        elif event.type == SHOOT_EVENT:
            shoot_projectiles(player, projectiles)
        elif event.type == SPAWN_EVENT:
            spawn_enemies(
                surface,
                enemies,
                c.enemy_speed,
                c.enemy_size,
            )
        elif event.type == ROUND_TIMER:
            if c.round_time > 0:
                round_countdown(surface)
                c.round_time -= 1
            elif c.round_time <= 0:
                # c.round_running = False
                game_state.state = "new_round"
            if c.round_time == 15:
                c.timer_color = [255, 155, 0]  # orange
                c.timer_size = 50
            elif c.round_time == 5:
                c.timer_color = [255, 0, 0]  # red
                c.timer_size = 60

    return False


def shoot_projectiles(player, projectiles):
    # Shooting is continuous in a circular direction.
    angle = random.uniform(0, 2 * math.pi)  # random angle in radians

    projectiles.add(
        Projectile(
            player.x, player.y, angle, c.projectile_speed, c.projectile_size
        )
    )
    return projectiles


def spawn_enemies(surface, enemies, speed, size):
    spawn_above = (
        random.randint(0, surface.get_width()),
        random.randint(-25, 0),
    )
    spawn_below = (
        random.randint(0, surface.get_width()),
        surface.get_height() + random.randint(0, 25),
    )
    spawn_left = (
        random.randint(-25, 0),
        random.randint(0, surface.get_height()),
    )
    spawn_right = (
        surface.get_width() + random.randint(0, 25),
        random.randint(0, surface.get_height()),
    )
    spawn_location_list = [spawn_above, spawn_below, spawn_left, spawn_right]
    spawn_location = random.choice(spawn_location_list)
    enemies.add(Enemy(spawn_location[0], spawn_location[1], speed, size))
    return enemies


def update_state(surface, projectiles, enemies, player):
    # update state of projectiles
    projectiles.update()
    projectiles.draw(surface)
    # update state of enemies
    enemies.update(player)
    enemies.draw(surface)
    # remove projectiles from Group that pass the edge of the window
    for projectile in projectiles.copy():
        if (
            projectile.rect.right < 0
            or projectile.rect.left > surface.get_width()
            or projectile.rect.bottom < 0
            or projectile.rect.top > surface.get_height()
        ):
            projectiles.remove(projectile)
    # Detect projectile vs enemy collision + remove enemy
    pygame.sprite.groupcollide(projectiles, enemies, False, True)
    # Detect enemy vs player collisions
    if pygame.sprite.spritecollideany(player, enemies):
        c.player_health -= 1
        c.healthbar_width = (c.player_health / 100) * surface.get_width()


# Timer for rounds.
def round_countdown(surface):
    font = pygame.font.SysFont(None, c.timer_size)
    text = font.render(
        f"{c.round_time}",
        True,
        (c.timer_color[0], c.timer_color[1], c.timer_color[2]),
    )
    text_rect = text.get_rect()
    text_rect.centerx = surface.get_width() / 2
    text_rect.top = 5
    surface.blit(text, text_rect)


# Bottom player health bar.
def draw_healthbar(surface):
    healthbar_width = c.healthbar_width
    healthbar_rect = pygame.Rect(
        0, (surface.get_height() - 20), healthbar_width, 10
    )
    pygame.draw.rect(
        surface,
        (c.health_color[0], c.health_color[1], c.health_color[2]),
        healthbar_rect,
    )
    if c.player_health <= 55:
        c.health_color = [255, 155, 0]
    if c.player_health <= 30:
        c.health_color = [255, 0, 0]
