import pygame
import pygame.gfxdraw

from engine import scene, events
from engine.menu import BaseMenu
from game import config


class MainMenu(BaseMenu):
    BUTTON_NAMES = (('Новая игра', events.NEW_GAME),
                    ('Продолжить', ''),
                    ('Загрузить', ''),
                    ('Настройки', ''),
                    ('Выйти', pygame.QUIT))

    BG_SCALE = 450, 400
    BG_POSITION = 20, config.HEIGHT - 420

    def __init__(self):
        super().__init__()

        self.margin_left = 40
        self.margin_top = 30


class MainMenuScene(scene.BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        self.background = pygame.image.load('game/images/main_menu/background/galaxy-space.jpg').convert()

        self.menu = MainMenu()

    def draw(self):
        menu_surface, menu_surface_rect = self.menu.draw()

        self.screen.blit(self.background, (0, 0))

        self.screen.blit(menu_surface, menu_surface_rect)

