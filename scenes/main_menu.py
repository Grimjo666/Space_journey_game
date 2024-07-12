import pygame
import pygame.gfxdraw

import config
from engine import events, scene
from engine.menu import MainMenu


class MainMenuScene(scene.BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        self.background = pygame.image.load('images/main_menu/background/galaxy-space.jpg').convert()

        self.menu = MainMenu()

    def draw(self):
        menu_surface, menu_surface_rect = self.menu.draw()

        self.screen.blit(self.background, (0, 0))

        self.screen.blit(menu_surface, menu_surface_rect)

