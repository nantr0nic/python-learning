import pygame

import config as c
from state_manager import GameState


def main():
    clock = pygame.time.Clock()
    # Will need to use dt later, will focus on that once there are more features.
    # dt = 0
    pygame.init()
    # Make window
    win = pygame.display.set_mode(
        (c.window_width, c.window_height), pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Circle Cirvivors")

    game_state = GameState(win)

    main_running = True
    while main_running:
        if game_state.state_manager(win):
            main_running = False

        pygame.display.flip()
        clock.tick(75)

    pygame.quit()


if __name__ == "__main__":
    main()
