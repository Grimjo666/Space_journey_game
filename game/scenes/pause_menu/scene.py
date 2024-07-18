import pygame

from engine import space, events, menu, scene
from engine.menu import BaseMenu

from game import config
from game.scenes.space.background import SpaceBG


class PauseMenu(BaseMenu):
    BUTTON_NAMES = (('Продолжить', events.CLOSE_PAUSE_MENU),
                    ('Загрузить', ''),
                    ('Настройки', ''),
                    ('В главное меню', events.TO_MAIN_MENU),
                    ('Выйти', pygame.QUIT))

    BG_SCALE = config.WIDTH * 0.8, config.HEIGHT * 0.8
    BG_POSITION = (config.WIDTH - BG_SCALE[0]) / 2, (config.HEIGHT - BG_SCALE[1]) / 2


class PauseMenuScene(scene.BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        # self.background = SpaceBG(screen)

        self.pause_menu = PauseMenu()

    def handle_event(self, event):
        if event.type == events.TO_MAIN_MENU:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.trigger_event(events.CLOSE_PAUSE_MENU)

    def draw(self):
        menu_surface, menu_surface_rect = self.pause_menu.draw()

        self.screen.blit(menu_surface, menu_surface_rect)

