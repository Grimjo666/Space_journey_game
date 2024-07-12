import pygame
import time

import config
from engine import events, scene
from engine.scene import SceneManager

from scenes.main_menu import MainMenuScene
from scenes.pause_menu import PauseMenuScene
from scenes.space import SpaceScene


FIXED_TIME_STEP = 1.0 / 30


def main_menu_events_handler(scene_manager, event):
    if event.type == events.NEW_GAME:
        scene_manager.get_scene('main_menu_scene').stop()
        scene_manager.get_scene('space_scene').start()

    elif event.type == events.TO_MAIN_MENU:
        scene_manager.stop_all()
        scene_manager.get_scene('main_menu_scene').start()


def pause_menu_events_handler(scene_manager, event):
    if event.type == events.OPEN_PAUSE_MENU:
        # scene_manager.get_scene('space_scene').stop()
        scene_manager.get_scene('pause_menu_scene').start()

    elif event.type == events.CLOSE_PAUSE_MENU:
        scene_manager.get_scene('pause_menu_scene').stop()
        scene_manager.get_scene('space_scene').start()


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

    start_time = time.perf_counter()

    running = True
    while running:
        current_time = time.perf_counter()
        frame_time = current_time - start_time
        start_time = current_time
        scene.FPS_STEP_COUNTER += frame_time

        if scene.FPS_STEP_COUNTER >= FIXED_TIME_STEP:
            scene.FPS_STEP_COUNTER = 0

        scene_manager.draw_scenes()

        for event in pygame.event.get():
            scene_manager.handle_events(event)

            main_menu_events_handler(scene_manager, event)
            pause_menu_events_handler(scene_manager, event)

            if event.type == pygame.QUIT:
                scene_manager.stop_all()
                running = False

        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()


if __name__ == "__main__":
    main()