import pygame
import pymunk
import pymunk.pygame_util

import config
from engine import space, events, menu, scene


class PauseMenuScene(scene.BaseScene):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)

        self.background = space.SpaceBG(screen)

        self.pause_menu = menu.PauseMenu()

    def handle_event(self, event):
        if event.type == events.TO_MAIN_MENU:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()

    def draw(self):
        self.pause_menu.draw(self.screen)

