import pygame
from pygame.sprite import Group

import functions as func
import config as c
from player import Player
from enemies import spawn_timer


class GameState:
    def __init__(self, win):
        self.state = "menu"
        self.win = win
        # Pause stuff
        self.paused = False
        # Timer pause vars
        self.shoot_remaining = 0
        self.spawn_remaining = 0
        self.round_remaining = 0

    def pause(self, win):
        font = pygame.font.SysFont(None, 100)
        text = font.render("PAUSED", True, (0, 200, 255))
        text_rect = text.get_rect(
            center=(win.get_width() // 2, win.get_height() // 2)
        )
        win.blit(text, text_rect)

    def new_round(self, win):
        print("New round")
        win.fill((0, 0, 0))
        c.current_round += 1
        font1 = pygame.font.SysFont(None, 100)
        text1 = font1.render("Next Round!", True, (0, 200, 255))
        text1_rect = text1.get_rect(
            center=(win.get_width() // 2, win.get_height() // 2)
        )
        win.blit(text1, text1_rect)
        font2 = pygame.font.SysFont(None, 50)
        text2 = font2.render("Spacebar to continue.", True, (0, 255, 0))
        text2_rect = text2.get_rect()
        text2_rect.top = text1_rect.bottom + 10
        win.blit(text2, text2_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "game"

    def menu(self, win):
        """Menu state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "game"

        win.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Press SPACE to start", True, (0, 0, 0))
        text_rect = text.get_rect(
            center=(win.get_width() // 2, win.get_height() // 2)
        )
        win.blit(text, text_rect)

    def game(self, win):
        """The actual game."""
        clock = pygame.time.Clock()
        # Instantiate Player object.
        player = Player(win)
        # Instantiate projectiles and enemies into sprite groups.
        projectiles = Group()
        enemies = Group()

        # EVENTS for projectiles shooting and enemy spawning. (Check events in functions file)
        SHOOT_EVENT = pygame.USEREVENT + 1
        SPAWN_EVENT = pygame.USEREVENT + 2
        ROUND_TIMER = pygame.USEREVENT + 3
        pygame.time.set_timer(SHOOT_EVENT, c.projectile_reload)
        pygame.time.set_timer(SPAWN_EVENT, c.current_spawn_interval)
        pygame.time.set_timer(ROUND_TIMER, 1000)

        # Optimization. Block all events then allow only necessary ones.
        pygame.event.set_blocked(None)
        pygame.event.set_allowed(
            [pygame.QUIT, pygame.KEYDOWN, SHOOT_EVENT, SPAWN_EVENT, ROUND_TIMER]
        )

        shoot_start = pygame.time.get_ticks()
        spawn_start = pygame.time.get_ticks()
        round_start = pygame.time.get_ticks()

        # Main game loop
        c.round_running = True
        while c.round_running:
            current_time = pygame.time.get_ticks()
            # Bool trick for sane quitting.
            if func.check_events(
                win,
                player,
                projectiles,
                enemies,
                SHOOT_EVENT,
                SPAWN_EVENT,
                ROUND_TIMER,
                self,
            ):
                c.round_running = False

            if not self.paused:
                # Resume timers with remaining time from before pause state
                if self.shoot_remaining:
                    pygame.time.set_timer(SHOOT_EVENT, c.projectile_reload)
                    shoot_start = current_time - (
                        c.projectile_reload - self.shoot_remaining
                    )
                    self.shoot_remaining = 0
                if self.spawn_remaining:
                    pygame.time.set_timer(SPAWN_EVENT, c.current_spawn_interval)
                    spawn_start = current_time - (
                        c.current_spawn_interval - self.spawn_remaining
                    )
                    self.spawn_remaining = 0
                if self.round_remaining:
                    pygame.time.set_timer(ROUND_TIMER, 1000)
                    round_start = current_time - (1000 - self.round_remaining)
                    self.round_remaining = 0
                # Check for events and timer stuff.
                func.check_events(
                    win,
                    player,
                    projectiles,
                    enemies,
                    SHOOT_EVENT,
                    SPAWN_EVENT,
                    ROUND_TIMER,
                    self,
                )

                # Draw black background
                win.fill((0, 0, 0))

                # Draw / update
                player.update(win)
                func.update_state(win, projectiles, enemies, player)

                # Draw / begin round countdown
                func.round_countdown(win)

                # Draw /update health bar
                func.draw_healthbar(win)

                # Spawn frequency timer
                spawn_timer(current_time, SPAWN_EVENT)
                """
                Debug prints
                print(f"Projectiles #: {len(projectiles)}")
                print(f"Projectile speed: {c.projectile_speed} / Size: {c.projectile_size}")
                print(f"Current enemy spawn interval: {current_spawn_interval}")
                print(f"Enemy speed: {c.enemy_speed} / Size: {c.enemy_size}")
                print(f"Player health: {c.player_health}")
                print(f"Player position: {player.x} / {player.y}")
                """
            else:
                if not self.shoot_remaining:
                    # Save remaining time of timer
                    self.shoot_remaining = (
                        c.projectile_reload
                        - (current_time - shoot_start) % c.projectile_reload
                    )
                    # Disable the timer.
                    pygame.time.set_timer(SHOOT_EVENT, 0)
                if not self.spawn_remaining:
                    self.spawn_remaining = (
                        c.current_spawn_interval
                        - (current_time - spawn_start)
                        % c.current_spawn_interval
                    )
                    pygame.time.set_timer(SPAWN_EVENT, 0)
                if not self.round_remaining:
                    self.round_remaining = (
                        1000 - (current_time - round_start) % 1000
                    )
                    pygame.time.set_timer(ROUND_TIMER, 0)

                self.pause(win)
            # Refresh stuff
            pygame.display.flip()
            clock.tick(75)

        return True

    def state_manager(self, win):
        if self.state == "menu":
            return self.menu(win)
        elif self.state == "game":
            return self.game(win)
        elif self.state == "new_round":
            return self.new_round(win)
