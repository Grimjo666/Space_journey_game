import pygame

import config
from engine import events
from scenes.main_menu import MainMenuScene
from scenes.pause_menu import PauseMenuScene
from scenes.space import SpaceScene
from engine.scene import SceneManager


def main():
    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Space snake")
    icon = pygame.image.load('images/snake_icon.png').convert_alpha()
    pygame.display.set_icon(icon)

    scene_manager = SceneManager()
    scene_manager.add_scene('main_menu_scene', MainMenuScene(screen))
    scene_manager.add_scene('space_scene', SpaceScene(screen), active=False)
    scene_manager.add_scene('pause_menu_scene', PauseMenuScene(screen), active=False)

    running = True
    while running:

        scene_manager.draw_scenes()

        for event in pygame.event.get():
            scene_manager.handle_events(event)

            if event.type == pygame.QUIT:
                scene_manager.stop_all()
                running = False

            elif event.type == events.NEW_GAME:
                scene_manager.get_scene('main_menu_scene').stop()
                scene_manager.get_scene('space_scene').start()

            elif event.type == events.OPEN_PAUSE_MENU:
                # scene_manager.get_scene('space_scene').stop()
                scene_manager.get_scene('pause_menu_scene').start()

            elif event.type == events.CLOSE_PAUSE_MENU:
                scene_manager.get_scene('pause_menu_scene').stop()
                scene_manager.get_scene('space_scene').start()

        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
