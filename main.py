import pygame

import config
from engine import events
from scenes.main_menu import MainMenuScene
from scenes.pause_menu import PauseMenuScene
from scenes.space import SpaceScene


def main():
    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Space snake")
    icon = pygame.image.load('images/snake_icon.png').convert_alpha()
    pygame.display.set_icon(icon)

    main_menu_scene = MainMenuScene(screen, clock)
    pause_menu_scene = PauseMenuScene(screen, clock)
    space_scene = SpaceScene(screen, clock)

    current_scene = main_menu_scene
    current_scene.start()

    running = True
    while running:

        current_scene.scene()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_scene.stop()
                running = False

            elif event.type == events.NEW_GAME:
                current_scene = space_scene
                current_scene.start()

    pygame.quit()


if __name__ == "__main__":
    main()
