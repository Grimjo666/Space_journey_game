import pygame
import pymunk
import pymunk.pygame_util

import config
from engine import space, events, menu, scene


class PauseMenuScene(scene.BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        self.background = space.SpaceBG(screen)

        self.pause_menu = menu.PauseMenu()

    def handle_event(self, event):
        if event.type == events.TO_MAIN_MENU:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.trigger_event(events.CLOSE_PAUSE_MENU)

    def draw(self):
        menu_surface, menu_surface_rect = self.pause_menu.draw()

        self.screen.blit(menu_surface, menu_surface_rect)

